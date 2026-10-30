"""Convert the approved JPG masters into the WebP sizes the site serves.

The site keeps three files per article image: the JPG master, a full width
WebP and a half width WebP for small screens. Existing blog images are
1400x933 and 700x467, so the masters are scaled up to 1400 wide for the
large file and to 700 for the small one.

Masters live in raw-images/<slug>/masters/ and carry a semantic file name,
because the mapping is explicit. Relying on glob order has bitten this
project before: the wrong picture ended up on the wrong slot.

Run this only after the watermark has been removed from the masters.

    python scripts/blog_images.py                    # the default slug
    python scripts/blog_images.py --slug cost-factors
    python scripts/blog_images.py --list             # show the known slugs
"""
import argparse
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
IMAGES = os.path.join(ROOT, 'assets', 'images')

QUALITY = 82

# slug -> the master file names, in the order they appear in the article.
SLUGS = {
    'trade-terms': [
        'blog-trade-terms-cartons',
        'blog-trade-terms-container',
        'blog-trade-terms-paperwork',
    ],
    'cost-factors': [
        'blog-cost-quote',
        'blog-cost-sizes',
        'blog-cost-packaging',
    ],
}

DEFAULT_SLUG = 'cost-factors'


def master_dir(slug):
    return os.path.join(ROOT, 'raw-images', slug, 'masters')


def convert(slug, names):
    for name in names:
        src = os.path.join(master_dir(slug), name + '.jpg')
        if not os.path.isfile(src):
            raise SystemExit('master missing: %s' % src)

        im = Image.open(src).convert('RGB')

        large = im.resize((1400, 933), Image.LANCZOS)

        # the JPG master ships as-is, it is the fallback for old browsers
        out_jpg = os.path.join(IMAGES, name + '.jpg')
        large.save(out_jpg, 'JPEG', quality=88, optimize=True, progressive=True)

        out_large = os.path.join(IMAGES, name + '.webp')
        large.save(out_large, 'WEBP', quality=QUALITY, method=6)

        small = im.resize((700, 467), Image.LANCZOS)
        out_small = os.path.join(IMAGES, name + '-sm.webp')
        small.save(out_small, 'WEBP', quality=QUALITY, method=6)

        for p in (out_jpg, out_large, out_small):
            print('%-46s %6d KB' % (
                os.path.basename(p), os.path.getsize(p) // 1024))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--slug', default=DEFAULT_SLUG,
                    help='the raw-images subfolder holding the masters')
    ap.add_argument('--list', action='store_true',
                    help='print the known slugs and exit')
    args = ap.parse_args()

    if args.list:
        for slug, names in SLUGS.items():
            print('%-14s %s' % (slug, ', '.join(names)))
        return

    if args.slug not in SLUGS:
        print('unknown slug: %s' % args.slug, file=sys.stderr)
        print('known slugs: %s' % ', '.join(SLUGS), file=sys.stderr)
        raise SystemExit(2)

    convert(args.slug, SLUGS[args.slug])


if __name__ == '__main__':
    main()
