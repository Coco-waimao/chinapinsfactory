"""Convert the approved JPG masters into the WebP sizes the site serves.

The site keeps three files per article image: the JPG master, a full width
WebP and a half width WebP for small screens. Existing blog images are
1400x933 and 700x467, so the masters are scaled up to 1400 wide for the
large file and to 700 for the small one.

Run this only after the watermark has been removed from the masters.
"""
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MASTERS = os.path.join(ROOT, 'raw-images', 'trade-terms', 'masters')
IMAGES = os.path.join(ROOT, 'assets', 'images')

NAMES = ['blog-trade-terms-cartons', 'blog-trade-terms-container', 'blog-trade-terms-paperwork']

QUALITY = 82


def main():
    for name in NAMES:
        src = os.path.join(MASTERS, name + '.jpg')
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


if __name__ == '__main__':
    main()
