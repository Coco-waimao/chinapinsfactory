#!/usr/bin/env python3
"""Pre-commit and pre-push verification for the static site.

Runs the full local check suite in one shot so problems are caught before
anything reaches GitHub. Exits non-zero when a check fails, which blocks the
commit or the push.

Checks
  1. JSON-LD parses on every page
  2. Every internal href/src resolves to a file that exists
  3. Every image reference resolves to a file that exists
  4. ItemList numberOfItems matches the visible card count
  5. FAQPage Question count matches the visible question count
  6. Exactly one H1 per page, exactly one canonical per page
  7. sitemap / feed / llms.txt agree with each other and with the pages
  8. No page is an orphan: everything is reachable from the homepage
  9. Line endings are consistent per file

Usage
  python scripts/check.py            full check, prints a report
  python scripts/check.py --quiet    only print failures (used by the hook)

Exit code 0 means every check passed.
"""

import os
import re
import sys
import json
import glob
import subprocess
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, '..'))
BASE_URL = 'https://www.chinapinsfactory.com'
SITEMAP_NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

QUIET = '--quiet' in sys.argv

failures = []
notes = []


def fail(check, message):
    failures.append((check, message))


def note(message):
    notes.append(message)


def rel(path):
    return os.path.relpath(os.path.abspath(path), SITE).replace('\\', '/')


def html_files():
    out = []
    for f in sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)):
        r = rel(f)
        if r.startswith('.workbuddy') or r.startswith('node_modules') or r.startswith('scripts'):
            continue
        out.append((r, f))
    return out


def load(path):
    return open(path, encoding='utf-8').read()


def resolve(base_rel, href):
    """Resolve an href to a local file.

    Returns the href when it is broken, None when it is external or empty.
    Absolute URLs on our own domain are checked too: a canonical or og:url
    pointing at a page that does not exist is a real fault, not a no-op.
    """
    if href.startswith(('mailto:', 'tel:', '#', 'data:', 'javascript:', '//')):
        return None
    if href.startswith('http://') or href.startswith('https://'):
        if not href.startswith(BASE_URL):
            return None
        path = href[len(BASE_URL):]
        if not path or path.startswith('/') and len(path) == 1:
            path = '/index.html'
        candidate = os.path.join(SITE, path.lstrip('/'))
        if os.path.isdir(candidate):
            candidate = os.path.join(candidate, 'index.html')
        if not os.path.isfile(candidate):
            return href
        return None
    # strip the fragment and query before touching the filesystem
    path = href.split('#')[0].split('?')[0]
    if not path:
        return None
    if path.startswith('/'):
        candidate = os.path.join(SITE, path.lstrip('/'))
    else:
        candidate = os.path.join(os.path.dirname(os.path.join(SITE, base_rel)), path)
    if os.path.isdir(candidate):
        candidate = os.path.join(candidate, 'index.html')
    if not os.path.isfile(candidate):
        return href
    return None


# ---------------------------------------------------------------- 1. JSON-LD
def check_jsonld(pages):
    total = 0
    for r, f in pages:
        text = load(f)
        for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)):
            total += 1
            try:
                json.loads(block)
            except Exception as e:
                fail('jsonld', f'{r} block {i + 1}: {str(e)[:90]}')
    return total


# ------------------------------------------------------- 2/3. links and images
def check_links(pages):
    missing_links = 0
    missing_imgs = 0
    img_total = 0
    for r, f in pages:
        text = load(f)
        for href in re.findall(r'(?:href|src)="([^"]+)"', text):
            bad = resolve(r, href)
            if bad:
                missing_links += 1
                fail('links', f'{r} -> {href}')
        sources = re.findall(r'<img[^>]+src="([^"]+)"', text) + \
                  re.findall(r'<source[^>]+srcset="([^"]+)"', text)
        for src in sources:
            for one in src.split(','):
                p = one.strip().split(' ')[0]
                if not p or p.startswith('http'):
                    continue
                img_total += 1
                bad = resolve(r, p)
                if bad:
                    missing_imgs += 1
                    fail('images', f'{r} -> {p}')
    return missing_links, missing_imgs, img_total


# ------------------------------------------------------- 4/5. structured counts
def check_counts(pages):
    """Verify every ItemList entry is visibly present on its own page.

    Google requires structured data to describe content a visitor can actually
    see. An ItemList entry may point at an anchor, a table row or a card, so
    counting class="card" is not a valid test. Instead each entry's URL or
    name has to appear somewhere in the visible markup.
    """
    itemlist_checked = 0
    faq_checked = 0
    for r, f in pages:
        text = load(f)
        m = re.search(r'"@type":\s*"ItemList".*?"itemListElement":\s*\[(.*?)\]', text, re.S)
        if m:
            block = m.group(1)
            items = re.findall(
                r'\{[^{}]*?"@type":\s*"ListItem".*?\}', block, re.S)
            n_declared = re.search(
                r'"@type":\s*"ItemList".*?"numberOfItems":\s*(\d+)', text, re.S)
            declared = int(n_declared.group(1)) if n_declared else -1
            itemlist_checked += 1

            if declared != len(items):
                fail('itemlist',
                     f'{r}: numberOfItems={declared} but {len(items)} ListItem entries')

            # visible markup = the page minus its own structured data
            visible = re.sub(
                r'<script type="application/ld\+json">.*?</script>', '', text, flags=re.S)
            for item in items:
                url = re.search(r'"url":\s*"([^"]+)"', item)
                name = re.search(r'"name":\s*"([^"]+)"', item)
                probe = None
                if url:
                    probe = url.group(1).split('#')[-1]
                    if probe and probe in visible:
                        continue
                    probe = url.group(1)
                if name and name.group(1).strip() in visible:
                    continue
                label = (name.group(1) if name else url.group(1) if url else '?')
                fail('itemlist',
                     f'{r}: ListItem entry not visible on page: {label[:60]}')
        if '"FAQPage"' in text:
            faq_checked += 1
            n = len(re.findall(r'"@type":\s*"Question"', text))
            vis = len(re.findall(r'class="faq__item"', text))
            if n != vis:
                fail('faq', f'{r}: Question={n} but visible faq items={vis}')
    return itemlist_checked, faq_checked


# ------------------------------------------------------------ 6. h1 + canonical
def check_head(pages):
    for r, f in pages:
        text = load(f)
        h1 = len(re.findall(r'<h1[\s>]', text))
        if h1 != 1:
            fail('h1', f'{r}: found {h1} H1 elements, expected 1')
        can = re.findall(r'<link rel="canonical" href="([^"]+)"', text)
        if len(can) != 1:
            fail('canonical', f'{r}: found {len(can)} canonical tags, expected 1')
        elif not can[0].startswith(BASE_URL):
            fail('canonical', f'{r}: canonical points off-site: {can[0]}')


# ----------------------------------------------------------- 7. machine layer
def check_machine_layer(pages):
    sm_path = os.path.join(SITE, 'sitemap.xml')
    if not os.path.isfile(sm_path):
        fail('sitemap', 'sitemap.xml missing')
        return
    try:
        sm = ET.parse(sm_path).getroot().findall(SITEMAP_NS + 'url')
    except Exception as e:
        fail('sitemap', f'parse error: {e}')
        return
    sm_locs = [u.find(SITEMAP_NS + 'loc').text for u in sm]

    for loc in sm_locs:
        if not loc.startswith(BASE_URL):
            fail('sitemap', f'loc not on site domain: {loc}')

    # every page file should appear in the sitemap
    for r, f in pages:
        if r in ('404.html', 'thank-you.html'):
            continue
        url_variants = {BASE_URL + '/' + r, BASE_URL + '/' + r.replace('index.html', '')}
        if not (url_variants & set(sm_locs)):
            fail('sitemap', f'page not listed: {r}')

    # feed
    feed_path = os.path.join(SITE, 'feed.xml')
    if not os.path.isfile(feed_path):
        fail('feed', 'feed.xml missing')
    else:
        try:
            feed = ET.parse(feed_path).getroot()
            items = feed.findall('.//item')
            for it in items:
                link = it.find('link').text
                if link not in sm_locs:
                    fail('feed', f'link not in sitemap: {link}')
            for it in items:
                title = it.find('title')
                if title is None or not (title.text or '').strip():
                    fail('feed', 'item without title')
            note(f'feed.xml: {len(items)} items')
        except Exception as e:
            fail('feed', f'parse error: {e}')

    # llms.txt
    llms_path = os.path.join(SITE, 'llms.txt')
    if not os.path.isfile(llms_path):
        fail('llms', 'llms.txt missing')
    else:
        text = load(llms_path)
        urls = set(re.findall(r'https://www\.chinapinsfactory\.com/[^\s\)]+', text))
        sm_set = {u.rstrip('/') for u in sm_locs}
        for u in urls:
            if u.rstrip('/') not in sm_set:
                fail('llms', f'URL not in sitemap: {u}')
        note(f'llms.txt: {len(urls)} URLs')

    # robots.txt must point at the sitemap
    rb_path = os.path.join(SITE, 'robots.txt')
    if os.path.isfile(rb_path):
        rb = load(rb_path)
        if 'Sitemap:' not in rb:
            fail('robots', 'no Sitemap: directive')

    note(f'sitemap.xml: {len(sm_locs)} URLs')


# --------------------------------------------------------------- 8. orphans
def check_reachability(pages):
    page_set = {r for r, _ in pages}
    graph = {}
    for r, f in pages:
        text = load(f)
        out = set()
        for href in re.findall(r'(?:href|src)="([^"]+)"', text):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', '//')):
                continue
            path = href.split('#')[0].split('?')[0]
            if not path:
                continue
            if path.startswith('/'):
                candidate = os.path.join(SITE, path.lstrip('/'))
            else:
                candidate = os.path.join(os.path.dirname(os.path.join(SITE, r)), path)
            if os.path.isdir(candidate):
                candidate = os.path.join(candidate, 'index.html')
            if os.path.isfile(candidate):
                t = rel(candidate)
                if t in page_set and t != r:
                    out.add(t)
        graph[r] = out

    dist = {'index.html': 0}
    queue = ['index.html']
    while queue:
        cur = queue.pop(0)
        for t in graph.get(cur, ()):
            if t not in dist:
                dist[t] = dist[cur] + 1
                queue.append(t)

    # these are reached by the server or by the form handler, not by a link
    expected_orphans = {'404.html', 'thank-you.html'}
    orphans = sorted(p for p in page_set if p not in dist and p not in expected_orphans)
    for o in orphans:
        inbound = sum(1 for s, ts in graph.items() if o in ts)
        fail('reachability', f'orphan page not reachable from homepage: {o} (inbound={inbound})')
    note(f'reachability: {len(dist)}/{len(page_set)} pages reachable from homepage')

    # every directory hub must be reachable and must have entries
    hubs = ['products/index.html', 'guides/index.html', 'company/index.html']
    for h in hubs:
        if h not in page_set:
            fail('hubs', f'hub page missing: {h}')
            continue
        if h not in dist:
            fail('hubs', f'hub page not reachable from homepage: {h}')
        inbound = sum(1 for s, ts in graph.items() if h in ts)
        if inbound < 2:
            fail('hubs', f'hub page has too few entries: {h} (inbound={inbound})')
        note(f'hub {h}: {inbound} inbound links')


# ------------------------------------------------------------ 9. breadcrumbs
DIR_LABELS = {
    'products': 'Products',
    'guides': 'Guides',
    'company': 'Company',
    'blog': 'Journal',
}


def check_crumbs(pages):
    """Every page inside a directory must show a breadcrumb naming the
    directory and linking to its hub page.

    The hub page shows the directory as the current item. The homepage,
    the 404 page and the thank-you page have no breadcrumb.
    """
    checked = 0
    for r, f in pages:
        text = load(f)
        m = re.search(r'<nav class="crumbs".*?</nav>', text, re.S)
        if not m:
            if r not in ('index.html', '404.html', 'thank-you.html'):
                fail('crumbs', f'{r}: no visible breadcrumb')
            continue
        checked += 1
        body = m.group(0)

        d = os.path.dirname(r).replace('\\', '/')
        if d not in DIR_LABELS:
            continue
        label = DIR_LABELS[d]
        is_hub = os.path.basename(r) == 'index.html'

        if f'>{label}</a>' not in body and f'>{label}</span>' not in body:
            fail('crumbs', f'{r}: breadcrumb is missing the "{label}" level')
            continue

        if is_hub:
            if f'>{label}</a>' in body:
                fail('crumbs', f'{r}: hub breadcrumb links to itself')
        else:
            if f'<a href="index.html">{label}</a>' not in body:
                fail('crumbs', f'{r}: breadcrumb does not link to the {d}/ hub page')
            if body.count('aria-current="page"') != 1:
                fail('crumbs', f'{r}: breadcrumb must have exactly one current item')
    note(f'breadcrumbs: {checked} pages carry a visible trail')


# --------------------------------------------------------------- 11. navigation
NAV_ITEMS = ['Custom Pins', 'Metal Swag', 'Guides', 'Our Factory', 'Journal']


def check_nav(pages):
    """The header nav is a fixed set of intent entries.

    The quote entry used to live in the nav as well as in the header button,
    which put the same destination twice next to each other. The nav must not
    grow a second quote entry, and every page must carry the same five items.
    """
    for r, f in pages:
        text = load(f)
        m = re.search(r'<ul class="nav__list">(.*?)</ul>', text, re.S)
        if not m:
            fail('nav', f'{r}: no navigation list found')
            continue
        items = re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S)
        names = []
        for it in items:
            a = re.search(r'>([^<]+)</a>', it)
            if a:
                names.append(a.group(1).strip())
        if names != NAV_ITEMS:
            fail('nav', f'{r}: nav items are {names}, expected {NAV_ITEMS}')
        # the quote page must not reappear in the nav next to the header button
        for it in items:
            if 'request-a-quote' in it:
                fail('nav', f'{r}: nav contains a second quote entry next to the header button')
        # exactly one item may be marked current
        marked = [it for it in items if 'is-active' in it]
        if len(marked) > 1:
            fail('nav', f'{r}: {len(marked)} nav items marked as current')
        # the header button must still be the quote entry point
        cta = re.search(r'<div class="header__cta">(.*?)</div>', text, re.S)
        if not cta:
            fail('nav', f'{r}: header CTA button missing')
        elif 'request-a-quote' not in cta.group(1):
            fail('nav', f'{r}: header CTA does not point to the quote page')
    note(f'navigation: {len(NAV_ITEMS)} fixed items on every page')


# ------------------------------------------------------------ 10. line endings
def check_eol(pages):
    """Guard against accidental line ending flips.

    The repo is mixed by design: README.md is LF, SITE-STRUCTURE.md and the
    HTML are CRLF. A flip in either direction produces a huge diff for no
    reason, so each file is compared against the style recorded in git HEAD.
    """
    targets = [rel(f) for _, f in pages]
    targets += ['sitemap.xml', 'feed.xml', 'llms.txt', 'robots.txt',
                'README.md', 'SITE-STRUCTURE.md',
                'assets/css/styles.css', 'assets/js/main.js']

    def style(data):
        crlf = data.count(b'\r\n')
        lf = data.count(b'\n')
        if crlf == lf and crlf > 0:
            return 'CRLF'
        if crlf == 0 and lf > 0:
            return 'LF'
        if crlf == 0 and lf == 0:
            return 'EMPTY'
        return 'MIXED'

    for name in targets:
        path = os.path.join(SITE, name)
        if not os.path.isfile(path):
            continue
        cur = style(open(path, 'rb').read())
        if cur == 'MIXED':
            fail('eol', f'{name}: mixed line endings')
            continue
        head = git_blob(name)
        if head is None:
            continue
        old = style(head)
        if old in ('LF', 'CRLF') and cur != old:
            fail('eol', f'{name}: line endings flipped {old} -> {cur}')


def git_blob(name):
    """Return the committed bytes of a file, or None if it is not in HEAD."""
    try:
        out = subprocess.run(
            ['git', 'show', f'HEAD:{name}'],
            cwd=SITE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            timeout=20)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def main():
    pages = html_files()
    if not pages:
        print('no HTML pages found', file=sys.stderr)
        return 1

    ld_total = check_jsonld(pages)
    missing_links, missing_imgs, img_total = check_links(pages)
    itemlist_checked, faq_checked = check_counts(pages)
    check_head(pages)
    check_machine_layer(pages)
    check_reachability(pages)
    check_crumbs(pages)
    check_nav(pages)
    check_eol(pages)

    if not QUIET:
        print('=' * 62)
        print('LOCAL CHECK')
        print('=' * 62)
        print(f'pages                : {len(pages)}')
        print(f'JSON-LD blocks       : {ld_total}')
        print(f'internal links       : {missing_links} missing')
        print(f'image references     : {img_total} checked, {missing_imgs} missing')
        print(f'ItemList checked     : {itemlist_checked}')
        print(f'FAQPage checked      : {faq_checked}')
        for n in notes:
            print(f'{n}')
        print()

    if failures:
        if not QUIET:
            print('=' * 62)
        print(f'FAILED: {len(failures)} problem(s)', file=sys.stderr)
        for check, message in failures:
            print(f'  [{check}] {message}', file=sys.stderr)
        return 1

    if not QUIET:
        print('=' * 62)
        print('PASS: all local checks passed')
        print('=' * 62)
    else:
        print('local check: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
