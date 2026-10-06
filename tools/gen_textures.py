"""
Texture generator for Sniffer Blooms.

Recolors a vanilla Minecraft item texture into one of the 16 fossil dye colors,
preserving the shading and the outline of the original sprite. Instead of painting
a flat color, it measures how dark each pixel is relative to the dominant color of
the source texture, then reproduces that same ratio using the destination color.

    python tools/gen_textures.py                 # everything
    python tools/gen_textures.py dyes            # only the dyes
    python tools/gen_textures.py wool            # only the wool
    python tools/gen_textures.py terracotta      # only the terracotta
    python tools/gen_textures.py glass           # only the stained glass
    python tools/gen_textures.py pane            # only the stained glass pane cap
    python tools/gen_textures.py concrete        # only the solid concrete
    python tools/gen_textures.py concrete_powder # only the concrete powder
    python tools/gen_textures.py candle          # only the unlit candle wax
    python tools/gen_textures.py candle_lit      # only the lit candle wax
    python tools/gen_textures.py candle_item     # only the candle item icon
    python tools/gen_textures.py glass soft_terracotta   # one single color
    python tools/gen_textures.py bed soft_terracotta     # only the bed blanket

The source textures are read straight out of the ForgeGradle cache jar, so there
is no need to extract them by hand.
"""

import glob
import os
import sys
import zipfile

# Allow importing "png" from this same folder when the script is run from the repo root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from png import read_png, write_png  # noqa: E402

# --- The 16 dye colors -------------------------------------------------------
# Single source of truth for the whole mod. Every color is defined once, here.
# Fields: (id, name_es, name_en, hex, closest vanilla dye color)
#
#   id            -> file name and item id, e.g. "soft_terracotta" -> soft_terracotta_dye.png
#   name_es/name_en-> the label shown under the icon in the inventory
#   hex           -> exact RGB the dye should look like
#   vanilla dye   -> the nearest DyeColor, used by systems that cannot store RGB
#                    (signs, sheep, banners, pet collars). See AGENTS.md section 6.
#
# NOTE: the biome each color comes from is deliberately NOT here. That belongs to
# the plant drop tables, which do not exist yet.
COLORS = [
    ("soft_terracotta", "Tinte Terracota Suave", "Soft Terracotta Dye", 0xD98A62, "orange"),
    ("fossil_turquoise", "Tinte Turquesa Fosil", "Fossil Turquoise Dye", 0x62B7AE, "cyan"),
    ("ancient_rose", "Tinte Rosa Antiguo", "Ancient Rose Dye", 0xD889A5, "magenta"),
    ("fern_green", "Tinte Verde Helecho", "Fern Green Dye", 0x658F68, "green"),
    ("pollen_yellow", "Tinte Amarillo Polen", "Pollen Yellow Dye", 0xE5C968, "yellow"),
    ("lavender", "Tinte Lavanda", "Lavender Dye", 0xA58FBE, "purple"),
    ("mist_blue", "Tinte Azul Bruma", "Mist Blue Dye", 0x8EC6D4, "light_blue"),
    ("stone_gray", "Tinte Gris Piedra", "Stone Gray Dye", 0x858783, "gray"),
    ("ash_gray", "Tinte Gris Ceniza", "Ash Gray Dye", 0xB9B7A9, "light_gray"),
    ("clay_red", "Tinte Rojo Arcilla", "Clay Red Dye", 0xB85F5A, "red"),
    ("bark_brown", "Tinte Marron Corteza", "Bark Brown Dye", 0x9A7255, "brown"),
    ("fossil_blue", "Tinte Azul Fosil", "Fossil Blue Dye", 0x668EB8, "blue"),
    ("fossil_ivory", "Tinte Marfil Fosil", "Fossil Ivory Dye", 0xE8E2D0, "white"),
    ("soft_lime", "Tinte Lima Suave", "Soft Lime Dye", 0xA8C875, "lime"),
    ("coral", "Tinte Coral", "Coral Dye", 0xE6A6B8, "pink"),
    ("obsidian", "Tinte Obsidiana", "Obsidian Dye", 0x3D3B3A, "black"),
]

# Vanilla texture used as the base for each content type. The dye sprite is a plain
# blob shape, so recoloring white_dye gives us a correct silhouette for free.
SOURCE_DYE = "assets/minecraft/textures/item/white_dye.png"
SOURCE_PLANT = "assets/minecraft/textures/item/pitcher_pod.png"
SOURCE_WOOL = "assets/minecraft/textures/block/white_wool.png"
SOURCE_TERRACOTTA = "assets/minecraft/textures/block/orange_terracotta.png"
SOURCE_GLASS = "assets/minecraft/textures/block/orange_stained_glass.png"
SOURCE_PANE = "assets/minecraft/textures/block/orange_stained_glass_pane_top.png"
SOURCE_CONCRETE = "assets/minecraft/textures/block/orange_concrete.png"
SOURCE_CONCRETE_POWDER = "assets/minecraft/textures/block/orange_concrete_powder.png"
SOURCE_CANDLE = "assets/minecraft/textures/block/orange_candle.png"
SOURCE_CANDLE_LIT = "assets/minecraft/textures/block/orange_candle_lit.png"
SOURCE_CANDLE_ITEM = "assets/minecraft/textures/item/orange_candle.png"
SOURCE_SHULKER = "assets/minecraft/textures/entity/shulker/shulker_white.png"
SOURCE_BED_FOOT_EAST = "assets/minecraft/textures/block/red_bed_foot_east.png"
SOURCE_BED_FOOT_SOUTH = "assets/minecraft/textures/block/red_bed_foot_south.png"
SOURCE_BED_FOOT_UP = "assets/minecraft/textures/block/red_bed_foot_up.png"
SOURCE_BED_FOOT_WEST = "assets/minecraft/textures/block/red_bed_foot_west.png"
SOURCE_BED_HEAD_EAST = "assets/minecraft/textures/block/red_bed_head_east.png"
SOURCE_BED_HEAD_UP = "assets/minecraft/textures/block/red_bed_head_up.png"
SOURCE_BED_HEAD_WEST = "assets/minecraft/textures/block/red_bed_head_west.png"
SOURCE_HARNESS = "assets/minecraft/textures/item/orange_harness.png"
SOURCE_BUNDLE = "assets/minecraft/textures/item/orange_bundle.png"
SOURCE_BUNDLE_OPEN_BACK = "assets/minecraft/textures/item/orange_bundle_open_back.png"
SOURCE_BUNDLE_OPEN_FRONT = "assets/minecraft/textures/item/orange_bundle_open_front.png"
SOURCE_GLAZED_TERRACOTTA = "assets/minecraft/textures/block/{color}_glazed_terracotta.png"


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "src", "main", "resources", "assets", "sniffer_blooms", "textures")
CACHE = os.path.expanduser(r"~\.gradle\caches\minecraftforge\forgegradle\mavenizer\caches")


def find_in_cache(entry):
    """Return the bytes of a file stored inside any jar of the ForgeGradle cache.

    Minecraft's own assets live in a jar, not loose on disk. Rather than telling
    the user to unzip it by hand, walk the cache and return the first match.
    """
    for jar in glob.glob(os.path.join(CACHE, "**", "*.jar"), recursive=True):
        try:
            with zipfile.ZipFile(jar) as z:
                if entry in z.namelist():
                    return z.read(entry)
        except Exception:
            # A jar that cannot be opened is not our file, keep looking.
            continue
    raise FileNotFoundError(f"no se encontro {entry} en la cache de ForgeGradle")


def luminance(r, g, b):
    """Perceived brightness of an RGB triple, on a 0..255 scale.

    Uses the standard weighted formula so green counts more than blue, which
    matches how the eye reads the shading of the sprite.
    """
    return 0.299 * r + 0.587 * g + 0.114 * b


def dominant_color(pixels, alpha_min=128):
    """Find the main flat color of a texture.
    Tints are mostly one solid color plus darker shading and an outline. The most
    frequent opaque color is that main color, and it is the reference point used to
    measure how dark every other pixel is.
    """
    counts = {}
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < alpha_min:
            continue  # skip transparent pixels
        key = pixels[i:i + 3]
        counts[key] = counts.get(key, 0) + 1
    return max(counts.items(), key=lambda kv: kv[1])[0]


def recolor(src_pixels, target_rgb, alpha_min=128):
    """Redraw a texture in the target color, keeping the original shading.

    For every pixel, work out how much darker it is than the dominant color
    (a ratio between 0 and 1), then multiply the target color by that ratio. A
    shadow pixel keeps being a shadow, just in the new hue. Fully transparent
    pixels are copied untouched so the outline and the silhouette stay correct.
    """
    base = dominant_color(src_pixels, alpha_min)
    base_l = luminance(base[0], base[1], base[2]) or 1.0  # avoid divide by zero
    tr = (target_rgb >> 16) & 0xFF  # unpack 0xRRGGBB into R, G, B
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF

    out = bytearray(src_pixels)
    for i in range(0, len(src_pixels), 4):
        if src_pixels[i + 3] < alpha_min:
            continue  # keep transparency as it is
        scale = luminance(src_pixels[i], src_pixels[i + 1], src_pixels[i + 2]) / base_l
        out[i] = max(0, min(255, round(tr * scale)))
        out[i + 1] = max(0, min(255, round(tg * scale)))
        out[i + 2] = max(0, min(255, round(tb * scale)))
    return bytes(out)


# --- Bed textures: blanket-only recolor ------------------------------------
# Vanilla beds share one wooden frame (brown) and one white pillow across every
# color; only the blanket differs. Recoloring the whole sprite stained the wood
# and pillow too, which looked wrong. Instead we repaint only the pixels whose
# hue/saturation match the blanket (a red bed has a cleanly separated red
# blanket), leaving the browns and whites untouched.
#
# The blanket band is defined by hue and saturation: the red blanket pixels sit
# at H ~ 0-5 with S >= 0.77, the brown wood at H ~ 35-40 and the white pillow
# at S <= 0.1, so this band cleanly hits only the blanket.
BED_RED_HUE_MAX = 12.0
BED_RED_HUE_MIN = 348.0  # hue wraps around 360, so the red band is [348, 360) U [0, 12]
BED_RED_SAT_MIN = 0.35
# Lightest blanket pixel in red_bed is #B53129 (V=181/255); map it onto the dye
# color itself so the brightest blanket pixel matches the dye, keeping shading.
BED_SOURCE_RED_V = 181.0 / 255.0


def rgb_to_hsv(r, g, b):
    """Standard RGB -> HSV, hue in 0..360, sat/val in 0..1."""
    r /= 255.0
    g /= 255.0
    b /= 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    d = mx - mn
    v = mx
    s = 0.0 if mx == 0 else d / mx
    h = 0.0
    if d > 0:
        if mx == r:
            h = 60.0 * (((g - b) / d) % 6)
        elif mx == g:
            h = 60.0 * (((b - r) / d) + 2)
        else:
            h = 60.0 * (((r - g) / d) + 4)
    if h < 0:
        h += 360.0
    return h, s, v


def hsv_to_rgb(h, s, v):
    """Standard HSV -> RGB, h in 0..360, s/v in 0..1. Returns (r, g, b) ints."""
    c = v * s
    x = c * (1.0 - abs((h / 60.0) % 2.0 - 1.0))
    m = v - c
    if h < 60:
        r, g, b = c, x, 0.0
    elif h < 120:
        r, g, b = x, c, 0.0
    elif h < 180:
        r, g, b = 0.0, c, x
    elif h < 240:
        r, g, b = 0.0, x, c
    elif h < 300:
        r, g, b = x, 0.0, c
    else:
        r, g, b = c, 0.0, x
    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)


def recolor_bed(src_pixels, target_rgb, alpha_min=128):
    """Repaint only the blanket of a bed sprite in the target dye color.

    Keeps the wooden frame (brown) and the pillow (white) exactly as they are;
    only pixels in the blanket hue/saturation band get the new color. The hue
    and saturation come from the dye, and each blanket pixel keeps its own
    brightness (scaled so the lightest blanket pixel equals the dye color).
    """
    tr = (target_rgb >> 16) & 0xFF
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF
    th, ts, _tv = rgb_to_hsv(tr, tg, tb)
    vs = _tv / BED_SOURCE_RED_V

    out = bytearray(src_pixels)
    for i in range(0, len(src_pixels), 4):
        if src_pixels[i + 3] < alpha_min:
            continue  # keep transparency as it is
        h, s, v = rgb_to_hsv(src_pixels[i], src_pixels[i + 1], src_pixels[i + 2])
        is_blanket = s >= BED_RED_SAT_MIN and (h <= BED_RED_HUE_MAX or h >= BED_RED_HUE_MIN)
        if not is_blanket:
            continue  # wood frame and pillow stay untouched
        nr, ng, nb = hsv_to_rgb(th, ts, min(1.0, v * vs))
        out[i], out[i + 1], out[i + 2] = nr, ng, nb
    return bytes(out)


def dominant_colors(pixels, n=2, alpha_min=128):
    """Return the top-n most frequent opaque colors in the texture."""
    counts = {}
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < alpha_min:
            continue
        key = (pixels[i], pixels[i + 1], pixels[i + 2])
        counts[key] = counts.get(key, 0) + 1
    return [c for c, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:n]]


def recolor_glazed(src_pixels, target_rgb, vanilla_dye_rgb, alpha_min=128):
    """
    Recolor a glazed terracotta texture by swapping its two main colors.

    The vanilla glazed texture has two dominant colors (pattern + background).
    We map:
      - most common color -> target_rgb (our mod color)
      - second most common -> vanilla_dye_rgb (the vanilla dye color)
    This preserves the pattern structure while using our palette.
    """
    # Find the two dominant colors in the source
    cols = dominant_colors(src_pixels, n=2, alpha_min=alpha_min)
    if len(cols) < 2:
        return recolor(src_pixels, target_rgb, alpha_min)  # fallback

    color1, color2 = cols[0], cols[1]
    tr, tg, tb = (target_rgb >> 16) & 0xFF, (target_rgb >> 8) & 0xFF, target_rgb & 0xFF
    vr, vg, vb = (vanilla_dye_rgb >> 16) & 0xFF, (vanilla_dye_rgb >> 8) & 0xFF, vanilla_dye_rgb & 0xFF

    out = bytearray(src_pixels)
    for i in range(0, len(src_pixels), 4):
        if src_pixels[i + 3] < alpha_min:
            continue
        r, g, b = src_pixels[i], src_pixels[i + 1], src_pixels[i + 2]
        if (r, g, b) == color1:
            out[i], out[i + 1], out[i + 2] = tr, tg, tb
        elif (r, g, b) == color2:
            out[i], out[i + 1], out[i + 2] = vr, vg, vb
        # Other colors (minor accents) left untouched
    return bytes(out)


def generate(kind, source_entry, folder, prefix, suffix="", only=None, alpha_min=128):
    """Recolor one vanilla texture into all 16 colors and save the results.

    kind          -> label printed in the console, e.g. "dyes"
    source_entry  -> path of the vanilla texture inside the cache jar
    folder        -> subfolder of assets/sniffer_blooms/textures to write into
    prefix/suffix -> wrapped around the color id to build the file name
    only          -> color id to generate, None for all 16
    alpha_min     -> lowest alpha value that still gets recolored. Glass is mostly
                     semi transparent, so it needs 1 instead of the usual 128.
    """
    data = find_in_cache(source_entry)
    tmp = os.path.join(os.environ.get("TEMP", "."), "_sb_src.png")
    open(tmp, "wb").write(data)  # read_png works on a path, so drop it on disk first
    w, h, src = read_png(tmp)

    outdir = os.path.join(RES, folder)
    os.makedirs(outdir, exist_ok=True)
    print(f"[{kind}] base {source_entry} ({w}x{h}) -> {outdir}")

    for cid, _name_es, _name_en, rgb, _vanilla in COLORS:
        if only and cid != only:
            continue
        dest = os.path.join(outdir, f"{prefix}{cid}{suffix}.png")
        write_png(dest, w, h, recolor(src, rgb, alpha_min))
        print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    color = sys.argv[2] if len(sys.argv) > 2 else None
    if what in ("all", "dyes"):
        generate("dyes", SOURCE_DYE, "item", "", "_dye", color)
    if what in ("all", "wool"):
        generate("wool", SOURCE_WOOL, "block", "", "_wool", color)
    if what in ("all", "terracotta"):
        generate("terracotta", SOURCE_TERRACOTTA, "block", "", "_terracotta", color)
    if what in ("all", "glass"):
        generate("glass", SOURCE_GLASS, "block", "", "_stained_glass", color, 1)
    if what in ("all", "pane"):
        generate("pane", SOURCE_PANE, "block", "", "_stained_glass_pane_top", color)
    if what in ("all", "concrete"):
        generate("concrete", SOURCE_CONCRETE, "block", "", "_concrete", color)
    if what in ("all", "concrete_powder"):
        generate("concrete_powder", SOURCE_CONCRETE_POWDER, "block", "", "_concrete_powder", color)
    if what in ("all", "candle"):
        generate("candle", SOURCE_CANDLE, "block", "", "_candle", color)
    if what in ("all", "candle_lit"):
        generate("candle_lit", SOURCE_CANDLE_LIT, "block", "", "_candle_lit", color)
    if what in ("all", "candle_item"):
        generate("candle_item", SOURCE_CANDLE_ITEM, "item", "", "_candle", color)
    if what in ("all", "shulker"):
        os.makedirs(os.path.join(RES, "entity", "shulker"), exist_ok=True)
        generate("shulker", SOURCE_SHULKER, "entity/shulker", "shulker_", "", color)
    if what in ("all", "bed"):
        bed_dir = os.path.join(RES, "block")
        os.makedirs(bed_dir, exist_ok=True)
        for name, src in [
            ("bed_foot_east", SOURCE_BED_FOOT_EAST),
            ("bed_foot_south", SOURCE_BED_FOOT_SOUTH),
            ("bed_foot_up", SOURCE_BED_FOOT_UP),
            ("bed_foot_west", SOURCE_BED_FOOT_WEST),
            ("bed_head_east", SOURCE_BED_HEAD_EAST),
            ("bed_head_up", SOURCE_BED_HEAD_UP),
            ("bed_head_west", SOURCE_BED_HEAD_WEST),
        ]:
            data = find_in_cache(src)
            tmp = os.path.join(os.environ.get("TEMP", "."), "_sb_bed.png")
            open(tmp, "wb").write(data)
            w, h, srcpix = read_png(tmp)
            for cid, _name_es, _name_en, rgb, _vanilla in COLORS:
                if color and cid != color:
                    continue
                dest = os.path.join(bed_dir, f"{cid}_{name}.png")
                write_png(dest, w, h, recolor_bed(srcpix, rgb))
                print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X}")
        sys.exit(0)
    if what in ("all", "harness"):
        os.makedirs(os.path.join(RES, "item"), exist_ok=True)
        generate("harness", SOURCE_HARNESS, "item", "", "_harness", color)
        sys.exit(0)
    if what in ("all", "bundle"):
        os.makedirs(os.path.join(RES, "item"), exist_ok=True)
        generate("bundle", SOURCE_BUNDLE, "item", "", "_bundle", color)
        generate("bundle_back", SOURCE_BUNDLE_OPEN_BACK, "item", "", "_bundle_open_back", color)
        generate("bundle_front", SOURCE_BUNDLE_OPEN_FRONT, "item", "", "_bundle_open_front", color)
        sys.exit(0)
    if what in ("all", "glazed"):
        os.makedirs(os.path.join(RES, "block"), exist_ok=True)
        for cid, _name_es, _name_en, rgb, vanilla in COLORS:
            if color and cid != color:
                continue
            vanilla_rgb = {
                "white": 0xFFFFFF, "orange": 0xF9801D, "magenta": 0xC74EBD, "light_blue": 0x3AB3DA,
                "yellow": 0xFFEC9D, "lime": 0x80C71F, "pink": 0xF4B5CB, "gray": 0x36393D,
                "light_gray": 0xCCD0D2, "cyan": 0x157788, "purple": 0x8932B8, "blue": 0x2C2E8F,
                "brown": 0x835432, "green": 0x495B24, "red": 0xB02E26, "black": 0x1D1D21,
            }[vanilla]
            src = SOURCE_GLAZED_TERRACOTTA.format(color=vanilla)
            data = find_in_cache(src)
            tmp = os.path.join(os.environ.get("TEMP", "."), "_sb_glazed.png")
            open(tmp, "wb").write(data)
            w, h, srcpix = read_png(tmp)
            dest = os.path.join(RES, "block", f"{cid}_glazed_terracotta.png")
            write_png(dest, w, h, recolor_glazed(srcpix, rgb, vanilla_rgb))
            print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X} (swap {vanilla})")
        sys.exit(0)