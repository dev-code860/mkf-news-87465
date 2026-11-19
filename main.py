import os, struct, zlib

W, H = 1024, 768
FONT = {}

def _add(ch, rows):
    FONT[ch] = rows

F = {
'A':["01110","10001","10001","11111","10001","10001","10001"],
'B':["11110","10001","10001","11110","10001","10001","11110"],
'C':["01110","10001","10000","10000","10000","10001","01110"],
'D':["11110","10001","10001","10001","10001","10001","11110"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'G':["01110","10000","10000","10111","10001","10001","01110"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'I':["01110","00100","00100","00100","00100","00100","01110"],
'J':["00111","00010","00010","00010","00010","10010","01100"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'M':["10001","11011","10101","10101","10001","10001","10001"],
'N':["10001","11001","10101","10011","10001","10001","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'P':["11110","10001","10001","11110","10000","10000","10000"],
'Q':["01110","10001","10001","10001","10101","10010","01101"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'S':["01111","10000","10000","01110","00001","00001","11110"],
'T':["11111","00100","00100","00100","00100","00100","00100"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'V':["10001","10001","10001","10001","10001","01010","00100"],
'W':["10001","10001","10001","10101","10101","11011","10001"],
'X':["10001","10001","01010","00100","01010","10001","10001"],
'Y':["10001","10001","01010","00100","00100","00100","00100"],
'Z':["11111","00001","00010","00100","01000","10000","11111"],
'0':["01110","10001","10011","10101","11001","10001","01110"],
'1':["00100","01100","00100","00100","00100","00100","01110"],
'2':["01110","10001","00001","00110","01000","10000","11111"],
'3':["11110","00001","00001","01110","00001","00001","11110"],
'4':["00010","00110","01010","10010","11111","00010","00010"],
'5':["11111","10000","11110","00001","00001","10001","01110"],
'6':["00110","01000","10000","11110","10001","10001","01110"],
'7':["11111","00001","00010","00100","01000","01000","01000"],
'8':["01110","10001","10001","01110","10001","10001","01110"],
'9':["01110","10001","10001","01111","00001","00010","01100"],
' ':"0000000",
'-':["00000","00000","00000","11111","00000","00000","00000"],
':':["00000","00100","00000","00000","00000","00100","00000"],
'.':["00000","00000","00000","00000","00000","00110","00110"],
',':["00000","00000","00000","00000","00000","00100","01000"],
'%':["11001","11010","00010","00100","01000","01011","10011"],
'$':["00100","01111","10100","01110","00101","11110","00100"],
'&':["01100","10010","10100","01000","10101","10010","01101"],
'!':["00100","00100","00100","00100","00100","00000","00100"],
"'":["00100","00100","00000","00000","00000","00000","00000"],
'(':["00010","00100","01000","01000","01000","00100","00010"],
')':["01000","00100","00010","00010","00010","00100","01000"],
'?':["01110","10001","00001","00110","00100","00000","00100"],
'*':["00000","10101","01110","11111","01110","10101","00000"],
'#':["01010","01010","11111","01010","11111","01010","01010"],
'@':["01110","10001","10111","10101","10111","10000","01110"],
'=':["00000","00000","11111","00000","11111","00000","00000"],
'+':["00000","00100","00100","11111","00100","00100","00000"],
'_':["00000","00000","00000","00000","00000","00000","11111"],
'>':["01000","00100","00010","00001","00010","00100","01000"],
'<':["00010","00100","01000","10000","01000","00100","00010"],
'|':["00100","00100","00100","00100","00100","00100","00100"],
'/':["00001","00010","00010","00100","01000","01000","10000"],
'\\':["10000","01000","01000","00100","00010","00010","00001"],
'"':["01010","01010","00000","00000","00000","00000","00000"],
'^':["00100","01010","00000","00000","00000","00000","00000"],
'`':["01000","00100","00000","00000","00000","00000","00000"],
'~':["00000","00000","01000","10101","00010","00000","00000"],
'}':["01100","00010","00010","00100","00010","00010","01100"],
'{':["00110","01000","01000","00100","01000","01000","00110"],
']':["01100","00010","00010","00010","00010","00010","01100"],
'[':["01100","01000","01000","01000","01000","01000","01100"],
';':["00000","00100","00000","00000","00000","00100","01000"],
}
for k, v in F.items():
    if isinstance(v, str):
        v = [v[i*5:(i+1)*5] for i in range(7)]
    _add(k, v)

# ---- raster ----
INK    = (24, 24, 24)
PAPER  = (243, 238, 223)
CREAM  = (250, 246, 234)
RED    = (158, 27, 27)
TEAL   = (20, 82, 84)
GOLD   = (198, 156, 62)
SLATE  = (52, 62, 72)
GREY   = (120, 120, 112)

def put(buf, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y*W + x)*4
        buf[i] = c[0]; buf[i+1] = c[1]; buf[i+2] = c[2]; buf[i+3] = 255

def rect(buf, x, y, w, h, c):
    for yy in range(y, y+h):
        row = yy*W*4
        for xx in range(x, x+w):
            i = row + xx*4
            buf[i] = c[0]; buf[i+1] = c[1]; buf[i+2] = c[2]; buf[i+3] = 255

def frame(buf, x, y, w, h, t, c):
    rect(buf, x, y, w, t, c)
    rect(buf, x, y+h-t, w, t, c)
    rect(buf, x, y, t, h, c)
    rect(buf, x+w-t, y, t, h, c)

def hline(buf, x, y, w, t, c):
    rect(buf, x, y, w, t, c)

def drawtext(buf, x, y, s, scale, color=INK, track=1):
    cx = x
    for ch in s.upper():
        rows = FONT.get(ch, FONT['?'])
        for ry, row in enumerate(rows):
            for rx, b in enumerate(row):
                if b == '1':
                    rect(buf, cx+rx*scale, y+ry*scale, scale, scale, color)
        cx += (5 + track)*scale
    return cx

def textw(s, scale, track=1):
    return max(0, len(s)*(5+track)*scale - track*scale)

def fit(s, scale, width, track=1):
    if textw(s, scale, track) <= width:
        return s
    out = ''
    for ch in s:
        if textw(out+ch, scale, track) > width - textw('...', scale, track):
            return out+'...'
        out += ch
    return out

def wrap(s, scale, width, maxlines):
    lines, cur = [], ''
    for word in s.split():
        t = (cur+' '+word).strip()
        if textw(t, scale) <= width:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines[:maxlines]

# ---- PNG ----
def write_png(path, buf):
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    raw = b''.join(b'\x00' + buf[y*W*4:(y+1)*W*4] for y in range(H))
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 6, 0, 0, 0)
    data = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(data)

# ---- page ----
MARGIN = 26
COLGAP = 14
LINEH  = 16

KICKER  = 'LIVE DESK / FRONT PAGE, FINAL EDITION'
DECK    = ('A one-page digest of the day: the GTA VI launch-day console rollout, '
           'markets, the climate summit, technology and sport.')

STORIES = [
    ('GTA VI GOES ON SALE AS NEW CONSOLES HIT SHELVES', 2, RED,
     'The long-awaited game launches at midnight with a dedicated console '
     'edition; retailers report queues and sell-out within hours.'),
    ('STOCKS MIXED AS INVESTORS PRICE IN SPENDING WAVE', 2, TEAL,
     'Wall Street steadies while European and Asian indices swing on '
     'retail and chip shares; the dollar firms and gold slips.'),
    ('CLIMATE SUMMIT: DRAFT DEAL EXTENDS COAL DEADLINE', 2, SLATE,
     'Negotiators in Geneva agree a revised text that pushes phase-out '
     'dates back; island states call the compromise far too weak.'),
    ('AI CHIPS: NEW FAB CAPACITY TO EASE THE SHORTAGE', 2, GOLD,
     'A fresh supply agreement promises more accelerator unit volume '
     'next year, easing datacentre build-out and cloud prices.'),
    ('WORLD CUP PLAYOFFS: UNDERDOGS STUN SEEDS IN EXTRA TIME', 1, RED,
     'Underdogs stun the seeded sides in the intercontinental play-off '
     'finals; both ties level after extra time, decided on penalties.'),
    ('SPACE: CREW DOCKS WITH STATION ON FIRST COMMERCIAL FLIGHT', 1, TEAL,
     'The capsule arrives six hours after launch, carrying experimen'
     'and supplies for the next six-month expedition.'),
]

def headline_block(buf, x, y, w, title, big, accent, body):
    # rule + accent tab
    rect(buf, x, y, w, 4, accent)
    yy = y + 14
    sc = 3 if big else 2
    lw = w
    tl = fit(title, sc, lw)
    lines = wrap(tl, sc, lw, 2 if big else 1)
    if len(lines) > 1 and big:
        sc = 2
        lines = wrap(tl, sc, lw, 2)
    for ln in lines:
        drawtext(buf, x, yy, ln, sc, INK)
        yy += sc*7 + 6
    yy += 4
    hline(buf, x, yy, w, 1, GREY)
    yy += 8
    bl = wrap(body, 1, w, 4)
    for ln in bl:
        drawtext(buf, x, yy, ln, 1, SLATE)
        yy += LINEH
    return yy

def build():
    buf = bytearray(W*H*4)
    for i in range(W*H):
        buf[i*4:i*4+4] = bytes(PAPER) + b'\xff'
    # outer paper border
    frame(buf, 8, 8, W-16, H-16, 2, INK)
    frame(buf, 12, 12, W-24, H-24, 1, GREY)

    # masthead
    rect(buf, 16, 16, W-32, 58, INK)
    drawtext(buf, MARGIN+6, 24, 'WORLD NEWS', 4, CREAM)
    drawtext(buf, MARGIN+6, 52, 'THURSDAY 19 NOVEMBER 2026', 1, GOLD)
    drawtext(buf, W-MARGIN-6-textw('NO. 87465', 2), 52, 'NO. 87465', 1, CREAM)

    # red rule under masthead
    rect(buf, 16, 76, W-32, 4, RED)

    # dateline strip
    yy = 88
    drawtext(buf, MARGIN, yy, KICKER, 1, RED)
    drawtext(buf, W-MARGIN-textw('LATE EDITION', 1), yy, 'LATE EDITION', 1, SLATE)
    yy += 18
    hline(buf, MARGIN, yy, W-2*MARGIN, 2, INK)

    # deck (subhead paragraph)
    yy += 10
    for ln in wrap(DECK, 1, W-2*MARGIN, 2):
        drawtext(buf, MARGIN, yy, ln, 1, SLATE)
        yy += LINEH
    yy += 8

    # headline grid: 2 columns
    colw = (W - 2*MARGIN - COLGAP)//2
    colx = [MARGIN, MARGIN+colw+COLGAP]
    grid_top = yy
    tops = [yy, yy]
    for idx, (title, big, accent, body) in enumerate(STORIES):
        c = idx % 2
        if tops[c] + 90 > H - MARGIN:
            continue
        ybot = headline_block(buf, colx[c], tops[c], colw, title, big, accent, body)
        tops[c] = ybot + 16

    # column divider between the two news columns
    grid_bottom = max(tops) - 16
    rect(buf, MARGIN+colw+COLGAP//2, grid_top, 1, max(0, grid_bottom-grid_top), GREY)

    # footer
    fy = H - MARGIN - 12
    hline(buf, MARGIN, fy-8, W-2*MARGIN, 1, GREY)
    drawtext(buf, MARGIN, fy, 'WORLD NEWS / THURSDAY 19 NOVEMBER 2026 / PAGE 1', 1, GREY)
    drawtext(buf, W-MARGIN-textw('DEV-CODE860', 1), fy, 'DEV-CODE860', 1, GREY)
    return buf

def main():
    out = os.environ.get('MAKEFUN_OUTPUT_DIR') or 'out'
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'entry.png')
    write_png(p, build())
    print('wrote', p, os.path.getsize(p))

if __name__ == "__main__":
    main()
