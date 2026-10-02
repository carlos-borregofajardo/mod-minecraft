"""Lector/escritor minimo de PNG (indice 1/2/4/8 bits, grayscale, RGB, RGBA, paleta)."""
import struct
import zlib


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "no es PNG"
    pos = 8
    idat = plte = trns = b""
    w = h = bitdepth = colortype = interlace = None
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bitdepth, colortype, _comp, _filt, interlace = struct.unpack(">IIBBBBB", chunk[:13])
        elif typ == b"PLTE":
            plte = chunk
        elif typ == b"tRNS":
            trns = chunk
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    assert interlace == 0, "PNG entrelazado no soportado"
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[colortype]
    bpp = max(1, (channels * bitdepth + 7) // 8)
    stride = (w * channels * bitdepth + 7) // 8

    raw = zlib.decompress(idat)
    out = bytearray()
    prev = bytearray(stride)
    p = 0
    for _ in range(h):
        ft = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            x = line[i]
            if ft == 1:
                line[i] = (x + a) & 0xFF
            elif ft == 2:
                line[i] = (x + b) & 0xFF
            elif ft == 3:
                line[i] = (x + (a + b) // 2) & 0xFF
            elif ft == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (x + pr) & 0xFF
        out += line
        prev = line

    # Desempaquetar indices si bitdepth < 8
    if bitdepth < 8:
        mask = (1 << bitdepth) - 1
        idx = bytearray()
        per_byte = 8 // bitdepth
        for b_ in out:
            for k in range(per_byte):
                shift = 8 - bitdepth * (k + 1)
                idx.append((b_ >> shift) & mask)
        out = idx[:w * h]

    rgba = bytearray()
    if colortype in (3, 0, 4):
        for v in out:
            if colortype == 3:
                i = v * 3
                r, g, b = (plte[i], plte[i + 1], plte[i + 2]) if i + 2 < len(plte) else (0, 0, 0)
                a = trns[v] if v < len(trns) else 255
            else:
                r = g = b = v
                a = 255
            rgba += bytes((r, g, b, a))
    elif colortype == 2:
        for i in range(0, len(out), 3):
            rgba += bytes((out[i], out[i + 1], out[i + 2], 255))
    else:
        for i in range(0, len(out), 4):
            rgba += bytes((out[i], out[i + 1], out[i + 2], out[i + 3]))
    return w, h, bytes(rgba)


def write_png(path, w, h, pixels):
    """pixels: bytes RGBA (len = w*h*4)."""
    raw = b"".join(b"\x00" + pixels[y * w * 4:(y + 1) * w * 4] for y in range(h))

    def chunk(typ, payload):
        return (struct.pack(">I", len(payload)) + typ + payload
                + struct.pack(">I", zlib.crc32(typ + payload) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)