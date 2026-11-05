#!/usr/bin/env python3
"""Render audit for a single page.

Drives a headless Chrome over CDP and reports:

  * horizontal overflow at each width
  * the real rendered contrast of the closing CTA text against the background
    it actually sits on (reading computed styles, not the markup)
  * screenshots at desktop and mobile width

Usage
    python scripts/audit_page.py blog/club-and-team-lapel-pins.html
"""

import base64
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, '..'))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = 9344

WIDTHS = [1440, 1024, 768, 390]


def start_chrome(port):
    profile = os.path.join(os.environ.get('TEMP', '/tmp'), 'cpf-audit-profile')
    subprocess.Popen([
        CHROME, '--headless=new',
        f'--remote-debugging-port={port}',
        '--remote-allow-origins=*',
        '--no-first-run', '--no-default-browser-check',
        '--disable-gpu', '--hide-scrollbars',
        f'--user-data-dir={profile}',
        'about:blank',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        try:
            with urllib.request.urlopen(
                    f'http://127.0.0.1:{port}/json/version', timeout=1) as r:
                json.load(r)
            return True
        except Exception:
            time.sleep(0.5)
    return False


class Chrome(object):
    def __init__(self, port):
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list') as r:
            targets = json.load(r)
        page = next(t for t in targets if t['type'] == 'page')
        u = urlparse(page['webSocketDebuggerUrl'])
        self.sock = socket.create_connection((u.hostname, u.port or 80))
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f'GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\n'
               f'Upgrade: websocket\r\nConnection: Upgrade\r\n'
               f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n')
        self.sock.send(req.encode())
        buf = b''
        while b'\r\n\r\n' not in buf:
            buf += self.sock.recv(4096)
        self.sock.settimeout(40)
        self.buf = b''
        self.id = 0

    def _fill(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise IOError('connection closed')
            self.buf += chunk

    def _recv(self):
        self._fill(2)
        b1, b2 = self.buf[0], self.buf[1]
        opcode = b1 & 0x0f
        masked = b2 & 0x80
        length = b2 & 0x7f
        offset = 2
        if length == 126:
            self._fill(4)
            length = struct.unpack('>H', self.buf[2:4])[0]
            offset = 4
        elif length == 127:
            self._fill(10)
            length = struct.unpack('>Q', self.buf[2:10])[0]
            offset = 10
        if masked:
            self._fill(offset + 4)
            mask = self.buf[offset:offset + 4]
            offset += 4
        self._fill(offset + length)
        payload = self.buf[offset:offset + length]
        self.buf = self.buf[offset + length:]
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 0x8:
            raise IOError('websocket closed by peer')
        if opcode == 0x9:
            return self._recv()
        return payload.decode('utf-8')

    def send(self, method, params=None):
        self.id += 1
        mid = self.id
        payload = json.dumps({'id': mid, 'method': method,
                              'params': params or {}}).encode('utf-8')
        mask = os.urandom(4)
        n = len(payload)
        header = bytearray([0x81])
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += n.to_bytes(2, 'big')
        else:
            header.append(0x80 | 127)
            header += n.to_bytes(8, 'big')
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.send(bytes(header) + masked)
        while True:
            msg = json.loads(self._recv())
            if msg.get('id') == mid:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})

    def evaluate(self, expr):
        res = self.send('Runtime.evaluate', {
            'expression': expr, 'returnByValue': True, 'awaitPromise': True})
        if res.get('exceptionDetails'):
            return {'__error__': str(res['exceptionDetails'])[:300]}
        return res.get('result', {}).get('value')

    def goto(self, url):
        self.send('Page.navigate', {'url': url})
        for _ in range(120):
            if self.evaluate('document.readyState') == 'complete':
                return True
            time.sleep(0.15)
        return False

    def width(self, w):
        self.send('Emulation.setDeviceMetricsOverride', {
            'width': w, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})

    def shot(self, path, full=True):
        params = {'format': 'png'}
        if full:
            params['captureBeyondViewport'] = True
            # A full page capture does not trigger lazy loading, so scroll the
            # document once first or every image below the fold is blank.
            h = self.evaluate('document.documentElement.scrollHeight') or 0
            for y in range(0, h, 800):
                self.evaluate("window.scrollTo({top:%d,behavior:'instant'})" % y)
                time.sleep(0.12)
            self.evaluate('window.scrollTo({top:0,behavior:"instant"})')
            time.sleep(0.3)
        data = self.send('Page.captureScreenshot', params)['data']
        with open(path, 'wb') as f:
            f.write(base64.b64decode(data))
        return path


CONTRAST_JS = r"""
(function () {
  function parse(c) {
    var m = c.match(/[\d.]+/g);
    if (!m) return null;
    return [parseFloat(m[0]), parseFloat(m[1]), parseFloat(m[2]),
            m.length > 3 ? parseFloat(m[3]) : 1];
  }
  function over(fg, bg) {
    var a = fg[3];
    return [fg[0]*a + bg[0]*(1-a), fg[1]*a + bg[1]*(1-a), fg[2]*a + bg[2]*(1-a), 1];
  }
  function lum(c) {
    var v = [c[0]/255, c[1]/255, c[2]/255].map(function (x) {
      return x <= 0.03928 ? x/12.92 : Math.pow((x+0.055)/1.055, 2.4);
    });
    return 0.2126*v[0] + 0.7152*v[1] + 0.0722*v[2];
  }
  function ratio(a, b) {
    var l1 = lum(a), l2 = lum(b);
    return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
  }
  function bgOf(el) {
    var node = el;
    while (node) {
      var s = getComputedStyle(node);
      var c = parse(s.backgroundColor);
      if (c && c[3] > 0) {
        var stack = [c];
        var p = node.parentElement;
        while (p) {
          var pc = parse(getComputedStyle(p).backgroundColor);
          if (pc && pc[3] > 0) stack.push(pc);
          p = p.parentElement;
        }
        var acc = stack[stack.length-1];
        for (var i = stack.length-2; i >= 0; i--) acc = over(stack[i], acc);
        return acc;
      }
      node = node.parentElement;
    }
    return [255,255,255,1];
  }
  var out = [];
  var ink = document.querySelector('section.section--ink');
  if (!ink) return {missing: true, items: []};
  var targets = ink.querySelectorAll('.lede--light, .section__title, h2, p, .btn--primary, .btn--ghost, a');
  for (var i = 0; i < targets.length; i++) {
    var el = targets[i];
    if (!el.checkVisibility || !el.checkVisibility({checkVisibilityCSS:true})) continue;
    var s = getComputedStyle(el);
    var fg = parse(s.color);
    if (!fg) continue;
    var bg = bgOf(el);
    var f = fg[3] < 1 ? over(fg, bg) : fg;
    var text = (el.innerText || '').trim().slice(0, 60);
    out.push({
      tag: el.tagName,
      cls: el.className,
      text: text,
      color: s.color,
      bg: 'rgb(' + Math.round(bg[0]) + ',' + Math.round(bg[1]) + ',' + Math.round(bg[2]) + ')',
      ratio: Math.round(ratio(f, bg) * 100) / 100
    });
  }
  return {missing: false, items: out};
})()
"""


def main():
    if len(sys.argv) < 2:
        print('usage: audit_page.py <page.html>')
        return 1
    rel = sys.argv[1]
    page = os.path.join(SITE, rel)
    if not os.path.isfile(page):
        print('not found: %s' % page)
        return 1

    if not start_chrome(PORT):
        print('could not start chrome')
        return 1
    c = Chrome(PORT)
    c.send('Page.enable')
    c.send('Runtime.enable')

    url = 'file:///' + page.replace('\\', '/')
    problems = []

    for w in WIDTHS:
        c.width(w)
        if not c.goto(url):
            problems.append('%s @%d: did not load' % (rel, w))
            continue
        base = c.evaluate("""
          (function () {
            var d = document.documentElement;
            return {scrollW: d.scrollWidth, clientW: d.clientWidth};
          })()
        """)
        if base.get('scrollW', 0) > base.get('clientW', 0) + 1:
            problems.append('%s @%d: horizontal overflow %s > %s'
                            % (rel, w, base['scrollW'], base['clientW']))
        print('width %4d  scrollW=%s clientW=%s' % (w, base.get('scrollW'), base.get('clientW')))

    # contrast on the closing CTA
    c.width(1440)
    c.goto(url)
    res = c.evaluate(CONTRAST_JS)
    if res.get('missing'):
        problems.append('%s: no section.section--ink closing CTA found' % rel)
    else:
        print('\nclosing CTA contrast (rendered values):')
        for it in res['items']:
            flag = 'LOW ' if it['ratio'] < 4.5 else '    '
            print('  %s%-46s %-22s on %-18s %6.2f'
                  % (flag, it['text'] or ('<' + it['tag'] + '>'), it['color'],
                     it['bg'], it['ratio']))
            if it['ratio'] < 4.5 and it['text']:
                problems.append('%s: CTA text "%s" contrast %.2f below 4.5'
                                % (rel, it['text'][:40], it['ratio']))

    # screenshots
    outdir = os.path.join(SITE, '.workbuddy', 'audit')
    os.makedirs(outdir, exist_ok=True)
    slug = rel.replace('/', '_').replace('.html', '')
    for w, tag in ((1440, 'desktop'), (390, 'mobile')):
        c.width(w)
        c.goto(url)
        p = c.shot(os.path.join(outdir, '%s-%s.png' % (slug, tag)))
        print('shot: %s' % p)

    print()
    if problems:
        print('PROBLEMS:')
        for p in problems:
            print('  - %s' % p)
        return 1
    print('PASS: no overflow, CTA contrast is fine')
    return 0


if __name__ == '__main__':
    sys.exit(main())
