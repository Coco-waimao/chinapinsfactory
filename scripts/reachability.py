#!/usr/bin/env python3
"""Reachability graph for the static site.

Builds a link graph over every HTML file, resolves relative hrefs to real
files, then reports for each page: inbound internal links, outbound links,
whether it is reachable from the homepage, and the shortest path that gets
there. Pages that exist but cannot be reached from the homepage are orphans.
"""

import os
import re
import sys
import json
import glob
from collections import deque

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, '..'))

HREF_RE = re.compile(r'(?:href|src)="([^"]+)"')
SKIP_PREFIX = ('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', 'javascript:', '//')


def norm(path):
    return os.path.relpath(os.path.abspath(path), SITE).replace('\\', '/')


def resolve(base_file, href):
    """Resolve an href to a repo-relative file path, or None if not a local file."""
    if href.startswith(SKIP_PREFIX):
        return None
    path = href.split('#')[0].split('?')[0]
    if not path:
        return None
    if path.startswith('/'):
        candidate = os.path.join(SITE, path.lstrip('/'))
    else:
        candidate = os.path.join(os.path.dirname(os.path.join(SITE, base_file)), path)
    if os.path.isdir(candidate):
        candidate = os.path.join(candidate, 'index.html')
    if not os.path.isfile(candidate):
        return None
    return norm(candidate)


def main():
    pages = {}
    for f in sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)):
        rel = norm(f)
        if rel.startswith('.workbuddy') or rel.startswith('node_modules'):
            continue
        text = open(f, encoding='utf-8').read()
        out = set()
        for href in HREF_RE.findall(text):
            t = resolve(rel, href)
            if t and t.endswith('.html') and t != rel:
                out.add(t)
        pages[rel] = out

    # inbound counts
    inbound = {p: 0 for p in pages}
    for src, targets in pages.items():
        for t in targets:
            inbound[t] = inbound.get(t, 0) + 1

    # BFS from homepage
    start = 'index.html'
    dist = {start: 0}
    parent = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        for t in pages.get(cur, ()):
            if t not in dist:
                dist[t] = dist[cur] + 1
                parent[t] = cur
                q.append(t)

    def path_to(p):
        chain = []
        cur = p
        while cur is not None:
            chain.append(cur)
            cur = parent.get(cur)
        return ' -> '.join(reversed(chain))

    print('=' * 78)
    print('REACHABILITY FROM index.html')
    print('=' * 78)
    print(f'{"page":<50}{"in":>4}{"out":>5}{"depth":>7}  status')
    print('-' * 78)
    unreachable = []
    for p in sorted(pages):
        d = dist.get(p)
        status = 'ok' if d is not None else 'ORPHAN'
        if d is None:
            unreachable.append(p)
        print(f'{p:<50}{inbound.get(p,0):>4}{len(pages[p]):>5}{(str(d) if d is not None else "-"):>7}  {status}')

    print()
    print(f'total pages      : {len(pages)}')
    print(f'reachable        : {len(dist)}')
    print(f'orphans          : {len(unreachable)}')
    for p in unreachable:
        print(f'    ORPHAN  {p}  (inbound={inbound.get(p,0)})')

    # 404.html is served by the host on a missing path and thank-you.html is
    # reached by the form handler, so neither is linked from the markup.
    expected = {'404.html', 'thank-you.html'}
    unexpected = [p for p in unreachable if p not in expected]
    if expected & set(unreachable):
        print(f'    (expected, not linked: {", ".join(sorted(expected & set(unreachable)))})')

    # hub page entry check
    print()
    print('=' * 78)
    print('HUB ENTRY CHECK')
    print('=' * 78)
    hubs = ['products/index.html', 'guides/index.html', 'company/index.html']
    ok = True
    for h in hubs:
        if h not in pages:
            print(f'  MISSING HUB {h}')
            ok = False
            continue
        d = dist.get(h)
        srcs = [s for s, ts in pages.items() if h in ts]
        print(f'  {h}')
        print(f'      reachable from homepage : {"yes (depth " + str(d) + ")" if d is not None else "NO"}')
        print(f'      linked from             : {len(srcs)} page(s)')
        for s in sorted(srcs):
            print(f'          {s}')
        if d is None:
            ok = False

    print()
    if ok and not unexpected:
        print('RESULT: PASS - every page is reachable and every hub has entries.')
        return 0
    print('RESULT: FAIL - see above.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
