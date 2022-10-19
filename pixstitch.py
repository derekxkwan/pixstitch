import sys
from PIL import Image, ImageDraw
import argparse

psr = argparse.ArgumentParser(description="Stitch images together.")
psr.add_argument('imgs', metavar='imgpath', type=str, nargs='+',
        help='path to image(s)')
psr.add_argument('--row', dest='row', type=int, const=float('inf'),
        default=float('inf'), nargs='?',
        help='number of images per row (default: inf)')
psr.add_argument('--out', dest='outpath', type=str,
        default='out.png', const='out.png', nargs='?',
        help='output destination file (default: out.png)')
psr.add_argument('--border', dest='border', type=int,
        const=0, default=0, nargs='?',
        help='border size between images in px (default: 0)')

argv = psr.parse_args()



border = argv.border
im_path = argv.imgs
num_im = len(im_path)
per_row = min(argv.row, num_im)
out_path = argv.outpath

im = []
hts = []
w = 0
h = 0
bg = (255,255,255,255)
cur_ims = []
row_w = 0
row_h = 0
cur_count = 0
for i,arg in enumerate(im_path):
    cur_im = Image.open(arg)
    cur_w = cur_im.size[0]
    cur_h = cur_im.size[1]
    cur_count += 1
    row_w += cur_w
    row_h = max(row_h, cur_h)
    cur_ims.append(cur_im)
    if (i < (num_im - 1)) and cur_count < per_row:
        row_w += border
    else:
        im.append(cur_ims)
        hts.append(row_h)
        w = max(row_w, w)
        h += row_h
        if i < (num_im - 1):
            h+= border
        row_w = 0
        row_h = 0
        cur_count = 0
        cur_ims = []
if len(im) > 0:
    new_im = Image.new("RGBA", (w,h))

    cur_d = ImageDraw.Draw(new_im)
    cur_d.rectangle([(0,0), (w,h)], bg)
    acc_w = 0
    acc_h = 0
    for i,cur_imrow in enumerate(im):
        for j,cur_im in enumerate(cur_imrow):
            new_im.paste(cur_im, (acc_w, acc_h))
            acc_w += (cur_im.size[0] + border)
            if j == len(cur_imrow) - 1:
                acc_w = 0
                acc_h += border + hts[i]
    new_im.save(out_path)
