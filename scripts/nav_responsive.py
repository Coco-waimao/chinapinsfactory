#!/usr/bin/env python3
"""Responsive check for the header navigation.

Drives a headless Chrome over CDP and, for every page and every breakpoint,
records:

  * whether the document scrolls sideways
  * whether the nav, the header button and the mobile toggle are laid out
    the way the breakpoint expects
  * where the dropdown panel sits when it is opened, and whether it stays
    inside the viewport
  * whether the mobile drawer expands a group into an accordion

Usage
    python scripts/nav_responsive.py
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, '..'))

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = 9333

# width, the breakpoint that applies, what the header must look like there
BREAKPOINTS = [
    (1920, 'wide'),
    (1440, 'wide'),
    (1280, 'wide'),
    (1100, 'wide'),
    (1024, 'wide'),
    (900, 'mid'),
    (860, 'mobile'),
    (768, 'mobile'),
    (375, 'mobile'),
]

PAGES = [
    'index.html',
    'products/index.html',
    'products/custom-enamel-pins.html',
    'products/materials.html',
    'products/plating-finishes.html',
    'products/backings.html',
    'guides/index.html',
    'guides/bulk-order-guide.html',
    'company/index.html',
    'company/factory.html',
    'blog/index.html',
    'blog/lapel-pin-sizes-guide.html',
    'legal/privacy-policy.html',
]


def start_chrome(port):
    """Launch a headless Chrome and wait for its debugging endpoint."""
    profile = os.path.join(os.environ.get('TEMP', '/tmp'), 'cpf-cdp-profile')
    subprocess.Popen([
        CHROME,
        '--headless=new',
        f'--remote-debugging-port={port}',
        '--remote-allow-origins=*',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-gpu',
        '--hide-scrollbars',
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


def main():
    if not os.path.isfile(CHROME):
        print('chrome not found, skipping')
        return 0

    if not start_chrome(PORT):
        print('could not start chrome')
        return 1

    # A page target has its own debugging socket, so connect straight to it
    # and skip the session indirection.
    import socket
    from urllib.parse import urlparse
    import base64
    import os as _os
    import struct

    with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/list') as r:
        targets = json.load(r)
    page = next(t for t in targets if t['type'] == 'page')

    u = urlparse(page['webSocketDebuggerUrl'])
    sock = socket.create_connection((u.hostname, u.port or 80))
    key = base64.b64encode(_os.urandom(16)).decode()
    req = (f'GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\n'
           f'Upgrade: websocket\r\nConnection: Upgrade\r\n'
           f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n')
    sock.send(req.encode())
    buf = b''
    while b'\r\n\r\n' not in buf:
        buf += sock.recv(4096)
    sock.settimeout(40)

    state = {'id': 0, 'buf': b''}

    def _fill(n):
        while len(state['buf']) < n:
            chunk = sock.recv(65536)
            if not chunk:
                raise IOError('connection closed')
            state['buf'] += chunk

    def recv():
        """Read one websocket frame and return the payload."""
        _fill(2)
        b1, b2 = state['buf'][0], state['buf'][1]
        opcode = b1 & 0x0f
        masked = b2 & 0x80
        length = b2 & 0x7f
        offset = 2
        if length == 126:
            _fill(4)
            length = struct.unpack('>H', state['buf'][2:4])[0]
            offset = 4
        elif length == 127:
            _fill(10)
            length = struct.unpack('>Q', state['buf'][2:10])[0]
            offset = 10
        if masked:
            _fill(offset + 4)
            mask = state['buf'][offset:offset + 4]
            offset += 4
        _fill(offset + length)
        payload = state['buf'][offset:offset + length]
        state['buf'] = state['buf'][offset + length:]
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 0x8:
            raise IOError('websocket closed by peer')
        if opcode == 0x9:  # ping, answer with a pong
            return recv()
        return payload.decode('utf-8')

    def send(method, params=None):
        state['id'] += 1
        mid = state['id']
        payload = json.dumps({'id': mid, 'method': method,
                              'params': params or {}}).encode('utf-8')
        mask = _os.urandom(4)
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
        sock.send(bytes(header) + masked)
        while True:
            msg = json.loads(recv())
            if msg.get('id') == mid:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})

    send('Page.enable')
    send('Runtime.enable')

    def evaluate(expr):
        res = send('Runtime.evaluate', {
            'expression': expr,
            'returnByValue': True,
            'awaitPromise': True,
        })
        r = res.get('result', {})
        if res.get('exceptionDetails'):
            return {'__error__': str(res['exceptionDetails'])[:200]}
        return r.get('value')

    def goto(url):
        send('Page.navigate', {'url': url})
        for _ in range(120):
            ready = evaluate('document.readyState')
            if ready == 'complete':
                return True
            time.sleep(0.15)
        return False

    def set_width(w):
        send('Emulation.setDeviceMetricsOverride', {
            'width': w, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False,
        })

    problems = []
    combos = 0

    for rel in PAGES:
        url = 'file:///' + os.path.join(SITE, rel).replace('\\', '/')
        for w, mode in BREAKPOINTS:
            combos += 1
            set_width(w)
            if not goto(url):
                problems.append(f'{rel} @{w}: page did not finish loading')
                continue

            base = evaluate("""
              (function () {
                var doc = document.documentElement;
                var nav = document.getElementById('mainNav');
                var toggle = document.getElementById('navToggle');
                var cta = document.querySelector('.header__cta .btn--primary');
                var crumbs = document.querySelector('.crumbs');
                function vis(el) {
                  if (!el) return false;
                  /* An element inside a display:none parent still reports its own
                     display value, so read the real rendering state instead. */
                  if (el.checkVisibility) {
                    return el.checkVisibility({checkVisibilityCSS: true, checkOpacity: false});
                  }
                  var s = getComputedStyle(el);
                  return s.display !== 'none' && s.visibility !== 'hidden';
                }
                return {
                  scrollW: doc.scrollWidth,
                  clientW: doc.clientWidth,
                  navVisible: vis(nav),
                  toggleVisible: vis(toggle),
                  ctaVisible: vis(cta),
                  crumbH: crumbs ? Math.round(crumbs.getBoundingClientRect().height) : -1,
                  navH: Math.round(nav.getBoundingClientRect().height),
                  headerH: Math.round(document.querySelector('.header__inner').getBoundingClientRect().height)
                };
              })()
            """)

            if not base or '__error__' in (base or {}):
                problems.append(f'{rel} @{w}: evaluate failed {base}')
                continue

            if base['scrollW'] > base['clientW'] + 1:
                problems.append(
                    f'{rel} @{w}: horizontal overflow '
                    f'{base["scrollW"]} > {base["clientW"]}')

            if mode == 'mobile':
                if base['navVisible']:
                    problems.append(f'{rel} @{w}: nav drawer visible before opening')
                if not base['toggleVisible']:
                    problems.append(f'{rel} @{w}: mobile toggle button missing')
            else:
                if not base['navVisible']:
                    problems.append(f'{rel} @{w}: nav is not visible')
                if base['toggleVisible']:
                    problems.append(f'{rel} @{w}: mobile toggle shown on a wide screen')

            # the header quote button is visible above 880px and hidden below
            if w > 880 and not base['ctaVisible']:
                problems.append(f'{rel} @{w}: header quote button missing')
            if w <= 880 and base['ctaVisible']:
                problems.append(f'{rel} @{w}: header quote button should be hidden')

            # the breadcrumb bar must keep the same height at every width
            if base['crumbH'] > 0 and base['crumbH'] != 47:
                problems.append(
                    f'{rel} @{w}: breadcrumb height changed to {base["crumbH"]}')

            # Open every dropdown and check that each panel stays on screen.
            # The panel fades in, so the measurement has to wait for the
            # transition to finish before the position is final.
            if mode != 'mobile':
                opened = evaluate("""
                  (function () {
                    var groups = document.querySelectorAll('.nav__item--group');
                    var out = [];
                    for (var i = 0; i < groups.length; i++) {
                      groups[i].classList.add('is-open');
                    }
                    var results = groups.length;
                    for (var j = 0; j < groups.length; j++) {
                      var m = groups[j].querySelector('.nav__menu');
                      var r = m.getBoundingClientRect();
                      out.push({
                        label: groups[j].querySelector('.nav__link--parent').textContent.trim(),
                        left: Math.round(r.left),
                        right: Math.round(r.right),
                        top: Math.round(r.top),
                        width: Math.round(r.width),
                        visible: getComputedStyle(m).visibility === 'visible',
                        opacity: getComputedStyle(m).opacity
                      });
                    }
                    for (var k = 0; k < groups.length; k++) {
                      groups[k].classList.remove('is-open');
                    }
                    return {ok: true, panels: out, vw: window.innerWidth};
                  })()
                """)

                # let the fade finish, then measure again
                time.sleep(0.35)
                settled = evaluate("""
                  (function () {
                    var groups = document.querySelectorAll('.nav__item--group');
                    var out = [];
                    for (var i = 0; i < groups.length; i++) {
                      groups[i].classList.add('is-open');
                    }
                    var results = groups.length;
                    return {count: results};
                  })()
                """)
                time.sleep(0.35)
                measured = evaluate("""
                  (function () {
                    var groups = document.querySelectorAll('.nav__item--group');
                    var out = [];
                    for (var i = 0; i < groups.length; i++) {
                      var m = groups[i].querySelector('.nav__menu');
                      var r = m.getBoundingClientRect();
                      out.push({
                        label: groups[i].querySelector('.nav__link--parent').textContent.trim(),
                        left: Math.round(r.left),
                        right: Math.round(r.right),
                        top: Math.round(r.top),
                        width: Math.round(r.width),
                        visible: getComputedStyle(m).visibility === 'visible',
                        opacity: getComputedStyle(m).opacity
                      });
                    }
                    for (var k = 0; k < groups.length; k++) {
                      groups[k].classList.remove('is-open');
                    }
                    return {panels: out, vw: window.innerWidth};
                  })()
                """)
                if measured and measured.get('panels'):
                    for panel in measured['panels']:
                        if not panel['visible']:
                            problems.append(
                                f'{rel} @{w}: dropdown under {panel["label"]} did not open')
                        if panel['left'] < -1:
                            problems.append(
                                f'{rel} @{w}: dropdown under {panel["label"]} runs off '
                                f'the left edge ({panel["left"]})')
                        if panel['right'] > measured['vw'] + 1:
                            problems.append(
                                f'{rel} @{w}: dropdown under {panel["label"]} runs off '
                                f'the right edge ({panel["right"]} > {measured["vw"]})')
                        if panel['top'] < 0:
                            problems.append(
                                f'{rel} @{w}: dropdown under {panel["label"]} is '
                                f'positioned above the header ({panel["top"]})')
                else:
                    problems.append(f'{rel} @{w}: no dropdown group found')
                opened = None

            # mobile: the drawer expands a group into an accordion
            if mode == 'mobile':
                acc = evaluate("""
                  (function () {
                    var t = document.getElementById('navToggle');
                    t.click();
                    var g = document.querySelector('.nav__item--group');
                    var caret = g.querySelector('.nav__caret');
                    var m = g.querySelector('.nav__menu');
                    var before = getComputedStyle(m).display;
                    caret.click();
                    var after = getComputedStyle(m).display;
                    var links = m.querySelectorAll('a').length;
                    var expanded = caret.getAttribute('aria-expanded');
                    var parent = g.querySelector('.nav__link--parent');
                    return {
                      before: before, after: after,
                      links: links, expanded: expanded,
                      parentHref: parent ? parent.getAttribute('href') : null,
                      navH: Math.round(document.getElementById('mainNav').getBoundingClientRect().height)
                    };
                  })()
                """)
                if acc:
                    if acc['before'] != 'none':
                        problems.append(
                            f'{rel} @{w}: submenu was not collapsed before the tap')
                    if acc['after'] == 'none':
                        problems.append(
                            f'{rel} @{w}: submenu did not expand when the caret was tapped')
                    if acc['links'] < 2:
                        problems.append(
                            f'{rel} @{w}: expanded submenu has {acc["links"]} links')
                    if acc['expanded'] != 'true':
                        problems.append(
                            f'{rel} @{w}: caret aria-expanded not updated')
                    if not acc['parentHref']:
                        problems.append(
                            f'{rel} @{w}: parent entry is not a link to the hub')
                else:
                    problems.append(f'{rel} @{w}: accordion test failed')

    print(f'combinations tested: {combos}')
    if problems:
        print(f'FAILED: {len(problems)} problem(s)')
        for p in problems:
            print('  ', p)
        return 1
    print('PASS: navigation is sound at every breakpoint')
    return 0


if __name__ == '__main__':
    sys.exit(main())
