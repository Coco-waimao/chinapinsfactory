"""Sync the Related articles rail across every blog article.

The rule is simple: each article lists every OTHER article, newest first.
So adding one article means every existing article gains a line and the new
article lists the rest without itself.

Run this after a new article is written and before the site is checked.

    python scripts/related_sync.py
"""
import io
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BLOG = os.path.join(ROOT, 'blog')

# slug -> (title shown in the rail, date shown in the rail)
ARTICLES = {
    'factory-vs-trading-company': ('Factory or trading company', '7 Nov 2026'),
    'club-and-team-lapel-pins': ('Club and team pins', '5 Nov 2026'),
    'lapel-pin-vs-challenge-coin-vs-badge': ('Pins, coins or badges', '3 Nov 2026'),
    'lapel-pin-quality-inspection-guide': ('How pins are inspected', '1 Nov 2026'),
    'lapel-pin-cost-factors-guide': ('What drives the price', '30 Oct 2026'),
    'trade-terms-fob-cif-ddp-guide': ('FOB, CIF or DDP', '28 Oct 2026'),
    'how-to-order-custom-lapel-pins-from-china': ('Ordering pins from China', '18 Oct 2026'),
    'hard-enamel-vs-soft-enamel-pins': ('Hard vs soft enamel pins', '12 Oct 2026'),
    'lapel-pin-sizes-guide': ('Lapel pin sizes', '5 Oct 2026'),
    'custom-challenge-coin-sizes-guide': ('Challenge coin sizes', '28 Sep 2026'),
}

ITEM = (
    '              <li>\n'
    '                <a href="%s.html">%s</a>\n'
    '                <span>%s</span>\n'
    '              </li>'
)


def related_list(current):
    """Every other article, newest first."""
    rows = []
    for slug, (title, date) in ARTICLES.items():
        if slug == current:
            continue
        rows.append((slug, title, date))
    return '\n'.join(ITEM % (s, t, d) for s, t, d in rows)


def main():
    changed = []
    for slug in ARTICLES:
        path = os.path.join(BLOG, slug + '.html')
        if not os.path.isfile(path):
            continue
        text = io.open(path, encoding='utf-8', newline='').read()
        crlf = '\r\n' in text
        src = text.replace('\r\n', '\n')

        pattern = re.compile(
            r'(<ul class="rail__related">\n).*?(\n            </ul>)', re.S)
        m = pattern.search(src)
        if not m:
            print('no rail found in %s' % slug)
            continue

        new = m.group(1) + related_list(slug) + m.group(2)
        if new == m.group(0):
            continue
        src = src[:m.start()] + new + src[m.end():]

        out = src.replace('\n', '\r\n') if crlf else src
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
        changed.append(slug)

    print('updated: %s' % (', '.join(changed) if changed else 'nothing'))


if __name__ == '__main__':
    main()
