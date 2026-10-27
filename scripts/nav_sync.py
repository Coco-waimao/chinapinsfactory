#!/usr/bin/env python3
"""Single source of truth for the header navigation.

The header nav is site chrome. It has to read the same on all 23 pages,
apart from the relative prefix and the page that is marked as current.
Editing it by hand in 23 files is how a site ends up with three different
menus, so the menu is defined once here and written out by this script.

Structure
    Products    dropdown, hub page plus the product line pages
    Guides      dropdown, hub page plus the buying guides
    Our Factory dropdown, hub page plus the factory and contact pages
    Journal     flat link to the journal hub

The parent link of each dropdown points at the directory hub, so the hub is
one click away and every leaf page below it is still a real anchor in the
markup of all 23 pages.

The journal is deliberately a flat link rather than a dropdown. Journal
pages arrive one at a time and the hub already lists them, so putting every
article in the menu would make the entry layer grow with each publication.
The same rule keeps the quote page out of the menu: the header button is
the only quote entry.

Usage
    python scripts/nav_sync.py            rewrite the nav block on every page
    python scripts/nav_sync.py --check    list pages whose nav differs
"""

import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, '..'))

NAV_RE = re.compile(
    r'[ \t]*<nav class="nav" id="mainNav" aria-label="Primary">.*?</nav>',
    re.S)

# ---------------------------------------------------------------- menu model
# Each group: id, label, hub path, child pages as (path, label) pairs.
NAV_GROUPS = [
    {
        'id': 'products',
        'label': 'Products',
        'hub': 'products/index.html',
        'children': [
            ('products/custom-enamel-pins.html', 'Custom enamel pins'),
            ('products/custom-metal-swag.html', 'Challenge coins, medals and swag'),
            ('products/custom-metal-badges.html', 'Custom metal badges'),
            ('products/samples.html', 'Samples and prototyping'),
        ],
    },
    {
        'id': 'guides',
        'label': 'Guides',
        'hub': 'guides/index.html',
        'children': [
            ('guides/bulk-order-guide.html', 'How to order in bulk from China'),
            ('guides/design-file-specs.html', 'Design file specifications'),
            ('guides/process-comparison.html', 'Five processes, side by side'),
            ('guides/faq.html', 'Frequently asked questions'),
        ],
    },
    {
        'id': 'company',
        'label': 'Our Factory',
        'hub': 'company/index.html',
        'children': [
            ('company/factory.html', 'Our factory and quality control'),
            ('company/contact.html', 'Contact our export desk'),
        ],
    },
]

# Flat entries: (path, label)
NAV_FLAT = [
    ('blog/index.html', 'Journal'),
]

# Pages that are deliberately not in the menu.
#   products/request-a-quote.html  the header button is the quote entry
#   journal articles               the journal hub lists them
NAV_EXEMPT = {
    'products/request-a-quote.html': 'the header button is the quote entry',
}


def is_exempt(page_rel):
    if page_rel in NAV_EXEMPT:
        return True
    if page_rel.startswith('blog/') and page_rel != 'blog/index.html':
        return True
    return False


def nav_targets():
    """Repo-relative paths the menu points at."""
    out = set()
    for g in NAV_GROUPS:
        out.add(g['hub'])
        for path, _ in g['children']:
            out.add(path)
    for path, _ in NAV_FLAT:
        out.add(path)
    return out


def rel_href(page_rel, target):
    """Relative href from a page to a target, in the site's own style."""
    page_dir = os.path.dirname(page_rel).replace('\\', '/')
    if not page_dir:
        return target
    rel = os.path.relpath(target.replace('\\', '/'), page_dir)
    return rel.replace('\\', '/')


def detect_indent(block):
    """Reuse the indentation already used by the page's nav block."""
    m = re.search(r'\n([ \t]*)<nav class="nav"', block)
    if m:
        return m.group(1)
    return '      '


def eol_of(text):
    return '\r\n' if '\r\n' in text else '\n'


def build_nav(page_rel, indent='      '):
    """Return the nav block for one page."""
    i = indent
    last_group = NAV_GROUPS[-1]['id'] if NAV_GROUPS else None
    out = []
    out.append(f'{i}<nav class="nav" id="mainNav" aria-label="Primary">')
    out.append(f'{i}  <ul class="nav__list">')

    for g in NAV_GROUPS:
        hub_href = rel_href(page_rel, g['hub'])
        in_group = page_rel == g['hub'] or any(
            page_rel == c[0] for c in g['children'])
        active = ' is-active' if in_group else ''
        hub_current = ' aria-current="page"' if page_rel == g['hub'] else ''
        edge = ' nav__item--edge' if g['id'] == last_group else ''

        out.append(f'{i}    <li class="nav__item nav__item--group{active}{edge}">')
        out.append(f'{i}      <a class="nav__link nav__link--parent"'
                   f' href="{hub_href}"{hub_current}>{g["label"]}</a>')
        out.append(f'{i}      <button class="nav__caret" type="button"'
                   f' aria-expanded="false" aria-controls="nav-menu-{g["id"]}"'
                   f' aria-label="Toggle the {g["label"]} submenu">'
                   f'<span class="nav__caret-icon" aria-hidden="true"></span>'
                   f'</button>')
        out.append(f'{i}      <ul class="nav__menu" id="nav-menu-{g["id"]}">')
        for path, label in g['children']:
            href = rel_href(page_rel, path)
            cur = ' aria-current="page"' if page_rel == path else ''
            out.append(f'{i}        <li><a class="nav__sublink"'
                       f' href="{href}"{cur}>{label}</a></li>')
        out.append(f'{i}      </ul>')
        out.append(f'{i}    </li>')

    for path, label in NAV_FLAT:
        href = rel_href(page_rel, path)
        active = ' is-active' if page_rel == path else ''
        cur = ' aria-current="page"' if page_rel == path else ''
        out.append(f'{i}    <li class="nav__item{active}">')
        out.append(f'{i}      <a class="nav__link" href="{href}"{cur}>'
                   f'{label}</a>')
        out.append(f'{i}    </li>')

    out.append(f'{i}  </ul>')
    out.append(f'{i}</nav>')
    return '\n'.join(out)


def html_files():
    out = []
    for f in sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, SITE).replace('\\', '/')
        if rel.startswith('.workbuddy') or rel.startswith('node_modules'):
            continue
        if rel.startswith('scripts/'):
            continue
        out.append((rel, f))
    return out


def main():
    check_only = '--check' in sys.argv
    changed = []
    for rel, path in html_files():
        with open(path, encoding='utf-8', newline='') as fh:
            text = fh.read()
        m = NAV_RE.search(text)
        if not m:
            print(f'  no nav block: {rel}')
            continue
        block = m.group(0)
        eol = eol_of(text)
        indent = detect_indent(block)
        want = build_nav(rel, indent).replace('\n', eol)
        if block == want:
            continue
        changed.append(rel)
        if not check_only:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(text[:m.start()] + want + text[m.end():])

    verb = 'differs on' if check_only else 'rewrote'
    print(f'nav_sync: {verb} {len(changed)} page(s)')
    for rel in changed:
        print(f'    {rel}')
    if check_only and changed:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
