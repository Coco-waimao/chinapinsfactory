"""Remove the review-only skin switcher from the whole site.

Phase 4 item 13 in SITE-STRUCTURE.md. The switcher is a review tool; it must
not ship. The ink palette is already pinned to :root in styles.css, so the
pages keep the exact same look after the switcher goes.

Three things have to go together, or the site breaks:
  * the switcher markup in every page
  * the inline script that restores a stored theme from localStorage (leave it
    and returning visitors keep seeing the graphite skin)
  * the switcher script and styles
"""

import glob
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ROOT, '..'))

INLINE = ("<script>try{var s=localStorage.getItem('cpf-skin');"
          "if(s)document.documentElement.setAttribute('data-theme',s);}"
          "catch(e){}</script>")


def strip_switcher(html):
    """Remove the .skin block, balancing the div tags by hand."""
    start = html.find('<div class="skin" id="skinSwitcher">')
    if start == -1:
        return html, False
    depth = 0
    i = start
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1
            i += 4
            continue
        if html.startswith('</div>', i):
            depth -= 1
            i += 6
            if depth == 0:
                break
            continue
        i += 1
    # take the trailing newline with the block
    end = i
    while end < len(html) and html[end] in '\r\n':
        end += 1
    return html[:start] + html[end:], True


def html_files():
    out = []
    for f in sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, SITE).replace('\\', '/')
        if rel.startswith('.workbuddy') or rel.startswith('node_modules') or rel.startswith('scripts/'):
            continue
        out.append((rel, f))
    return out


def main():
    changed = []
    for rel, path in html_files():
        with open(path, encoding='utf-8', newline='') as fh:
            text = fh.read()
        original = text

        text, hit = strip_switcher(text)
        inline_hits = text.count(INLINE)
        text = text.replace(INLINE + '\r\n', '').replace(INLINE + '\n', '').replace(INLINE, '')

        if text != original:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(text)
            changed.append((rel, hit, inline_hits))

    for rel, hit, inline_hits in changed:
        print('  %-42s switcher=%s inline=%s' % (rel, hit, inline_hits))
    print('%d page(s) cleaned' % len(changed))


if __name__ == '__main__':
    main()
