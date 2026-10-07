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
    python tools/gen_textures.py harness         # only the harness kerchief
    python tools/gen_textures.py glass soft_terracotta   # one single color
    python tools/gen_textures.py bed soft_terracotta     # only the bed blanket
    python tools/gen_textures.py glazed       # only the glazed terracotta tiles
    python tools/gen_textures.py glazed soft_terracotta   # only one tile
    python tools/gen_textures.py flowers      # only the fossil flowers (petals)

The source textures are read straight out of the ForgeGradle cache jar, so there
is no need to extract them by hand.
"""

import glob
import json
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
# the sniffer digging loot table (data/minecraft/loot_table/gameplay/sniffer_digging.json).
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
SOURCE_SHULKER_BLOCK = "assets/minecraft/textures/block/orange_shulker_box.png"
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

# --- Flowers: the fossil torchflower / pitcher plant varieties ----------------
# The two prehistoric Sniffer plants. We recolor only the FLOWER part, never the
# stem/leaves:
#   torchflower -> the vanilla `torchflower.png` sprite holds petals, the yellow
#                  heart, the stem and the leaves in one drawing. Only the petal
#                  colors are repainted; heart (yellow) and greens stay vanilla.
#   pitcher      -> its flower part is the whole mature top sprite
#                  (pitcher_crop_top_stage_4); the bottom/stem stays vanilla.
SOURCE_FLOWER_TORCHFLOWER = "assets/minecraft/textures/block/torchflower.png"
SOURCE_FLOWER_PITCHER = "assets/minecraft/textures/block/pitcher_crop_top_stage_4.png"
SOURCE_TORCHFLOWER_SEEDS = "assets/minecraft/textures/item/torchflower_seeds.png"
SOURCE_PITCHER_POD = "assets/minecraft/textures/item/pitcher_pod.png"

# The vanilla torchflower petals: purple + warm red accents. The yellow heart
# (FCE257/F6B927/DE8B25) and every green/shadow pixel are deliberately NOT here.
TORCHFLOWER_FLOWER_COLORS = {
    (0x65, 0x2D, 0x70),
    (0xE8, 0x72, 0x72),
    (0xD0, 0x31, 0x14),
    (0xA1, 0x26, 0x10),
}

# Which fossil colors become which flower. Warm hues -> torchflower, cool -> pitcher.
TORCHFLOWER_FLOWERS = {"soft_terracotta", "ancient_rose", "pollen_yellow", "clay_red",
                       "bark_brown", "fossil_ivory", "coral", "ash_gray"}
PITCHER_FLOWERS = {"fossil_turquoise", "fern_green", "lavender", "mist_blue",
                   "stone_gray", "fossil_blue", "soft_lime", "obsidian"}


def recolor_flower_part(src_pixels, target_rgb, part_colors, alpha_min=128):
    """Repaint only the pixels whose RGB is in `part_colors` (the flower part).

    The whole plant keeps its drawing; the flower part gets the target hue and
    saturation and every petal pixel keeps its own brightness, scaled so the
    brightest petal pixel equals the target color (no white speculars from
    clamping). Everything outside `part_colors` (yellow heart, stem, leaves,
    shadow pixels) stays byte-for-byte vanilla.
    """
    tr = (target_rgb >> 16) & 0xFF
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF
    th, ts, tv = rgb_to_hsv(tr, tg, tb)
    ref = max(
        rgb_to_hsv(src_pixels[i], src_pixels[i + 1], src_pixels[i + 2])[2]
        for i in range(0, len(src_pixels), 4)
        if src_pixels[i + 3] >= alpha_min
        and (src_pixels[i], src_pixels[i + 1], src_pixels[i + 2]) in part_colors
    ) or 1.0
    vs = tv / ref

    out = bytearray(src_pixels)
    for i in range(0, len(src_pixels), 4):
        if out[i + 3] < alpha_min:
            continue  # keep transparency as it is
        if (out[i], out[i + 1], out[i + 2]) not in part_colors:
            continue  # heart, stem and leaves stay untouched
        _h, _s, v = rgb_to_hsv(out[i], out[i + 1], out[i + 2])
        nr, ng, nb = hsv_to_rgb(th, ts, min(1.0, v * vs))
        out[i], out[i + 1], out[i + 2] = nr, ng, nb
    return bytes(out)


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "src", "main", "resources", "assets", "sniffer_blooms", "textures")
CACHE = os.path.expanduser(r"~\.gradle\caches\minecraftforge\forgegradle\mavenizer\caches")


def find_in_cache(entry):
    """Return the bytes of a file stored inside any jar of the ForgeGradle cache.

    Minecraft's own assets live in a jar, not loose on disk. Rather than telling
    the user to unzip it by hand, walk the cache and return the first match.
    """
    if entry in _CACHE_BYTES:
        return _CACHE_BYTES[entry]
    for jar in glob.glob(os.path.join(CACHE, "**", "*.jar"), recursive=True):
        try:
            with zipfile.ZipFile(jar) as z:
                if entry in z.namelist():
                    _CACHE_BYTES[entry] = z.read(entry)
                    return _CACHE_BYTES[entry]
        except Exception:
            # A jar that cannot be opened is not our file, keep looking.
            continue
    raise FileNotFoundError(f"no se encontro {entry} en la cache de ForgeGradle")


_CACHE_BYTES = {}
_PNG_CACHE = {}


def vanilla_png(entry):
    """Read a vanilla texture from the cache and cache the decoded pixels too.

    The harness mask needs all 16 harness sprites, and walking the whole
    ForgeGradle cache once per sprite would be needlessly slow.
    """
    if entry not in _PNG_CACHE:
        data = find_in_cache(entry)
        tmp = os.path.join(os.environ.get("TEMP", "."), "_sb_src.png")
        open(tmp, "wb").write(data)  # read_png works on a path, so drop it on disk first
        _PNG_CACHE[entry] = read_png(tmp)
    return _PNG_CACHE[entry]


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


# --- Harness: kerchief-only recolor -----------------------------------------
# Vanilla harnesses share the leather straps and the buckles; only the coloured
# kerchief differs between dye colours (34 of the 256 pixels, in three shade
# levels of 19/6/9 pixels). Repainting the whole sprite (as the generic
# `recolor` does) also tints the leather, which is why our old 16 sprites all
# looked fully recolored. The kerchief mask is computed from the vanilla
# sprites themselves: positions where the 16 dyes disagree and at least one of
# them is saturated (grey/shaded leather pixels vary only in white's highlight
# and stay outside the mask).
HARNESS_VANILLA_DYES = [
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
    "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black",
]
HARNESS_SAT_MIN = 0.12
_HARNESS_MASK = None


def harness_fabric_mask():
    """Pixel indices covered by the coloured kerchief of a harness (0-255)."""
    global _HARNESS_MASK
    if _HARNESS_MASK is None:
        sprites = [vanilla_png(f"assets/minecraft/textures/item/{n}_harness.png")[2]
                   for n in HARNESS_VANILLA_DYES]
        mask = []
        for p in range(len(sprites[0]) // 4):
            rgba = {s[p * 4:p * 4 + 4] for s in sprites}
            if len(rgba) == 1:
                continue
            if any(rgb_to_hsv(*s[p * 4:p * 4 + 3])[1] > HARNESS_SAT_MIN for s in sprites):
                mask.append(p)
        _HARNESS_MASK = mask
    return _HARNESS_MASK


def recolor_harness(src_pixels, target_rgb, alpha_min=128):
    """Repaint only the kerchief of a harness in the target dye color.

    Leather, buckles and shading stay byte-for-byte identical to vanilla; the
    hue and saturation come from the dye, and each kerchief pixel keeps its own
    brightness (scaled so the brightest kerchief pixel equals the dye color).
    """
    tr = (target_rgb >> 16) & 0xFF
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF
    th, ts, tv = rgb_to_hsv(tr, tg, tb)
    ref = max(rgb_to_hsv(*src_pixels[p * 4:p * 4 + 3])[2] for p in harness_fabric_mask()) or 1.0
    vs = tv / ref

    out = bytearray(src_pixels)
    for p in harness_fabric_mask():
        i = p * 4
        if out[i + 3] < alpha_min:
            continue  # keep transparency as it is
        _h, _s, v = rgb_to_hsv(out[i], out[i + 1], out[i + 2])
        nr, ng, nb = hsv_to_rgb(th, ts, min(1.0, v * vs))
        out[i], out[i + 1], out[i + 2] = nr, ng, nb
    return bytes(out)


# --- Bundles: pouch-only recolor (keep the vanilla cord) ---------------------
# The generic recolor tinted the whole sprite, rope included, so our bundles had
# a colored cord that reads badly against the pouch. Vanilla keeps the drawstring
# the same brown on all 16 dyed bundles (the only pixels whose RGBA is identical
# across every color), so we only repaint the pouch: positions where the 16
# vanilla bundles disagree. Each variant (closed / open_back / open_front) has
# its own cord mask, computed from the vanilla sprites themselves.
_BUNDLE_CORD = {}


def bundle_cord_mask(suffix):
    """Pixel indices shared by every vanilla bundle (the rope) for one variant."""
    if suffix not in _BUNDLE_CORD:
        sprites = [vanilla_png(f"assets/minecraft/textures/item/{n}_bundle{suffix}.png")[2]
                   for n in HARNESS_VANILLA_DYES]
        n = len(sprites[0]) // 4
        _BUNDLE_CORD[suffix] = {p for p in range(n) if len({s[p * 4:p * 4 + 4] for s in sprites}) == 1}
    return _BUNDLE_CORD[suffix]


def recolor_bundle(src_pixels, target_rgb, suffix="", alpha_min=128):
    """Repaint only the pouch of a bundle in the target color.

    The rope (and every other pixel vanilla shares across colors) stays
    byte-for-byte identical; the pouch keeps its own shading, scaled so the
    brightest pouch pixel equals the target color.
    """
    tr = (target_rgb >> 16) & 0xFF
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF
    th, ts, tv = rgb_to_hsv(tr, tg, tb)
    cord = bundle_cord_mask(suffix)
    pouch = (p for p in range(len(src_pixels) // 4)
             if p not in cord and src_pixels[p * 4 + 3] >= alpha_min)
    ref = max(rgb_to_hsv(*src_pixels[p * 4:p * 4 + 3])[2] for p in pouch) or 1.0
    vs = tv / ref

    out = bytearray(src_pixels)
    for p in range(len(src_pixels) // 4):
        i = p * 4
        if out[i + 3] < alpha_min or p in cord:
            continue  # keep transparency and the rope as they are
        _h, _s, v = rgb_to_hsv(out[i], out[i + 1], out[i + 2])
        nr, ng, nb = hsv_to_rgb(th, ts, min(1.0, v * vs))
        out[i], out[i + 1], out[i + 2] = nr, ng, nb
    return bytes(out)


# Recoloring each vanilla tile into a fossil color (the old recolor_glazed plus
# the orange/teal swap) was mangling the pattern, so glazed tiles moved to a
# different trick: the tile keeps a vanilla drawing but painted with the palette
# of a different vanilla tile. Each mod color has a "vanilla family" (the
# `vanilla` field of COLORS), so to make the dye and the tile of the same name
# match, every tile is named after its own palette: the file cid_i is painted
# with the palette of its own family and borrows the DRAWING of the mirror
# partner 15-i (soft_terracotta <-> obsidian, fossil_turquoise <-> coral, ...).
# The 16 paintings are exactly the mirror set, only their names are reordered.
#
# The "main colors" of a tile are its K most frequent colors (16x16-quantized
# buckets). The drawing's buckets and the palette buckets are aligned by
# luminance (dark <-> dark, light <-> light); every pixel is recolored to the
# target color scaled by its own brightness relative to the drawing bucket it
# belongs to, so the drawing's shading is preserved exactly.
GLAZED_K = 4
GLAZED_BUCKET = 16
GLAZED_MIN_COUNT = 6


def glazed_buckets(pixels, alpha_min=128):
    """Top-k color buckets of a glazed tile as (r, g, b, luminance)."""
    counts = {}
    members = {}
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < alpha_min:
            continue
        key = (pixels[i] // GLAZED_BUCKET * GLAZED_BUCKET,
               pixels[i + 1] // GLAZED_BUCKET * GLAZED_BUCKET,
               pixels[i + 2] // GLAZED_BUCKET * GLAZED_BUCKET)
        counts[key] = counts.get(key, 0) + 1
        members.setdefault(key, []).append((pixels[i], pixels[i + 1], pixels[i + 2]))
    out = []
    for key, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        if count < GLAZED_MIN_COUNT:
            continue
        ms = members[key]
        n = len(ms)
        bucket = tuple(sum(x[c] for x in ms) // n for c in range(3))
        lum = (bucket[0] * 299 + bucket[1] * 587 + bucket[2] * 114) // 1000
        out.append(bucket + (lum,))
        if len(out) >= GLAZED_K:
            break
    return out


def palette_transfer(draw_pixels, pal_pixels, alpha_min=128):
    """Repaint `draw_pixels` keeping its drawing, using the palette of `pal_pixels`.

    The drawing buckets and the palette buckets are matched by luminance rank;
    every pixel takes the partner's color scaled by how bright it is compared
    to its own drawing bucket, so the raster stays identical in shape.
    """
    draw = glazed_buckets(draw_pixels)
    pal = glazed_buckets(pal_pixels)
    m = min(len(draw), len(pal))
    draw = sorted(draw[:m], key=lambda c: c[3])
    pal = sorted(pal[:m], key=lambda c: c[3])

    out = bytearray(draw_pixels)
    for i in range(0, len(draw_pixels), 4):
        if draw_pixels[i + 3] < alpha_min:
            continue  # keep the antialiased fringe as it is
        r, g, b = draw_pixels[i], draw_pixels[i + 1], draw_pixels[i + 2]
        best = min(range(m), key=lambda j: (r - draw[j][0]) ** 2 + (g - draw[j][1]) ** 2 + (b - draw[j][2]) ** 2)
        base_lum = draw[best][3] or 1.0
        pr, pg, pb, _pl = pal[best]
        scale = (r * 299 + g * 587 + b * 114) / 1000.0 / base_lum
        out[i] = max(0, min(255, round(pr * scale)))
        out[i + 1] = max(0, min(255, round(pg * scale)))
        out[i + 2] = max(0, min(255, round(pb * scale)))
    return bytes(out)


# --- Dyes: blob-only recolor, one vanilla drawing per color ------------------
# Vanilla dye items are not one shape recolored 16 times: each of the 16 dyes is
# its own drawing (blob + hand-drawn shading) plus a set of outline/shadow
# pixels whose RGBA is byte-identical across all 16 dyes (26 pixels, the "rest
# of the object"). Our 16 dyes used to be white_dye recolored 16 times, so they
# all shared the same drawing. Now each color copies the vanilla dye it maps to
# (the `vanilla` field of COLORS) and repaints only its blob: target hue and
# saturation for every blob pixel, keeping each pixel's own brightness scaled so
# the brightest blob pixel equals the target color. The shared outline/shadow
# pixels stay byte-for-byte as vanilla.
_DYE_OUTLINE = None


def dye_outline_mask():
    """Pixel indices whose RGBA is identical across the 16 vanilla dyes."""
    global _DYE_OUTLINE
    if _DYE_OUTLINE is None:
        sprites = [vanilla_png(f"assets/minecraft/textures/item/{n}_dye.png")[2]
                   for n in HARNESS_VANILLA_DYES]
        n = len(sprites[0]) // 4
        _DYE_OUTLINE = {p for p in range(n) if len({s[p * 4:p * 4 + 4] for s in sprites}) == 1}
    return _DYE_OUTLINE


def recolor_dye(src_pixels, target_rgb, alpha_min=128):
    """Repaint the dye blob in the target color, keeping the vanilla drawing.

    The blob pixels get the target hue/saturation; the shared outline/shadow
    pixels (and the antialiased fringe) are copied untouched.
    """
    tr = (target_rgb >> 16) & 0xFF
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF
    th, ts, tv = rgb_to_hsv(tr, tg, tb)
    outline = dye_outline_mask()
    opaque = (p for p in range(len(src_pixels) // 4)
              if p not in outline and src_pixels[p * 4 + 3] >= alpha_min)
    ref = max(rgb_to_hsv(*src_pixels[p * 4:p * 4 + 3])[2] for p in opaque) or 1.0
    vs = tv / ref

    out = bytearray(src_pixels)
    for p in range(len(src_pixels) // 4):
        i = p * 4
        if out[i + 3] < alpha_min or p in outline:
            continue  # keep transparency and the shared outline as they are
        _h, _s, v = rgb_to_hsv(out[i], out[i + 1], out[i + 2])
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


# --- Glazed terracotta: orange / teal swap --------------------------------
# The vanilla orange glazed pattern carries teal accents (small cubes in the
# swirl) that recolor_glazed leaves untouched, so the soft_terracotta glazed
# tile ends up painted in both orange and blue. Swap those two families for any
# tile that actually contains both colors: where it is orange put teal, where it
# is teal put orange. Shading (S and V) is preserved; grey/white pixels stay.
#
# The orange family needs a minimum brightness on top of its hue: brown and dark
# red share the orange hue band, and yellow sits just above it, so without the
# V/S limits tiles like bark_brown or fossil_ivory would be swapped too. Real
# orange is bright (V >= 0.75) and saturated, which is what we actually mean.
GLAZED_SWAP_SAT_MIN = 0.45       # ignore near-grey pixels (white highlights)
GLAZED_SWAP_VAL_MIN = 0.75       # only bright colors count as orange (no browns)
GLAZED_ORANGE_HUE_MAX = 40.0     # the orange family, [0, 40); yellow is 45+
GLAZED_TEAL_HUE_MIN = 150.0      # the teal/blue family
GLAZED_TEAL_HUE_MAX = 215.0
GLAZED_SWAP_MIN_PIXELS = 12      # both families must be present enough
GLAZED_ORANGE_HUE = 30.0         # hue used where the teal pixels were
GLAZED_TEAL_HUE = 185.0          # hue used where the orange pixels were


def swap_orange_and_blue(pixels, alpha_min=128):
    """Swap the orange and teal families of a glazed tile, if both are present."""
    n_orange = n_teal = 0
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < alpha_min:
            continue
        h, s, v = rgb_to_hsv(pixels[i], pixels[i + 1], pixels[i + 2])
        if s < GLAZED_SWAP_SAT_MIN:
            continue
        if h < GLAZED_ORANGE_HUE_MAX and v >= GLAZED_SWAP_VAL_MIN:
            n_orange += 1
        elif GLAZED_TEAL_HUE_MIN <= h <= GLAZED_TEAL_HUE_MAX:
            n_teal += 1
    if n_orange < GLAZED_SWAP_MIN_PIXELS or n_teal < GLAZED_SWAP_MIN_PIXELS:
        return pixels  # this tile is not orange + blue, leave it alone

    out = bytearray(pixels)
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < alpha_min:
            continue
        r, g, b = pixels[i], pixels[i + 1], pixels[i + 2]
        h, s, v = rgb_to_hsv(r, g, b)
        if s < GLAZED_SWAP_SAT_MIN:
            continue
        if h < GLAZED_ORANGE_HUE_MAX and v >= GLAZED_SWAP_VAL_MIN:
            nr, ng, nb = hsv_to_rgb(GLAZED_TEAL_HUE, s, v)
        elif GLAZED_TEAL_HUE_MIN <= h <= GLAZED_TEAL_HUE_MAX:
            nr, ng, nb = hsv_to_rgb(GLAZED_ORANGE_HUE, s, v)
        else:
            continue
        out[i], out[i + 1], out[i + 2] = nr, ng, nb
    return bytes(out)


def generate(kind, source_entry, folder, prefix, suffix="", only=None, alpha_min=128, recolor_fn=recolor):
    """Recolor one vanilla texture into all 16 colors and save the results.

    kind          -> label printed in the console, e.g. "dyes"
    source_entry  -> path of the vanilla texture inside the cache jar
    folder        -> subfolder of assets/sniffer_blooms/textures to write into
    prefix/suffix -> wrapped around the color id to build the file name
    only          -> color id to generate, None for all 16
    alpha_min     -> lowest alpha value that still gets recolored. Glass is mostly
                     semi transparent, so it needs 1 instead of the usual 128.
    recolor_fn    -> pixels colormap to apply (generic `recolor` by default,
                     kerchief-only `recolor_harness` for harnesses).
    """
    _w, _h, src = vanilla_png(source_entry)

    outdir = os.path.join(RES, folder)
    os.makedirs(outdir, exist_ok=True)
    print(f"[{kind}] base {source_entry} ({_w}x{_h}) -> {outdir}")

    for cid, _name_es, _name_en, rgb, _vanilla in COLORS:
        if only and cid != only:
            continue
        dest = os.path.join(outdir, f"{prefix}{cid}{suffix}.png")
        write_png(dest, _w, _h, recolor_fn(src, rgb, alpha_min))
        print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    color = sys.argv[2] if len(sys.argv) > 2 else None
    if what in ("all", "dyes"):
        os.makedirs(os.path.join(RES, "item"), exist_ok=True)
        for cid, _name_es, _name_en, rgb, vanilla in COLORS:
            if color and cid != color:
                continue
            _w, _h, src = vanilla_png(f"assets/minecraft/textures/item/{vanilla}_dye.png")
            dest = os.path.join(RES, "item", f"{cid}_dye.png")
            write_png(dest, _w, _h, recolor_dye(src, rgb))
            print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X} (base {vanilla})")
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
        os.makedirs(os.path.join(RES, "block"), exist_ok=True)
        generate("shulker_box_tex", SOURCE_SHULKER_BLOCK, "block", "", "_shulker_box", color)
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
    if what in ("all", "harness"):
        os.makedirs(os.path.join(RES, "item"), exist_ok=True)
        generate("harness", SOURCE_HARNESS, "item", "", "_harness", color, recolor_fn=recolor_harness)
    if what in ("all", "bundle"):
        item_dir = os.path.join(RES, "item")
        os.makedirs(item_dir, exist_ok=True)
        for src, suf in ((SOURCE_BUNDLE, ""),
                         (SOURCE_BUNDLE_OPEN_BACK, "_open_back"),
                         (SOURCE_BUNDLE_OPEN_FRONT, "_open_front")):
            _w, _h, srcpix = vanilla_png(src)
            for cid, _name_es, _name_en, rgb, _vanilla in COLORS:
                if color and cid != color:
                    continue
                dest = os.path.join(item_dir, f"{cid}_bundle{suf}.png")
                write_png(dest, _w, _h, recolor_bundle(srcpix, rgb, suffix=suf))
                print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X} (cuerda vanilla)")
    if what in ("all", "glazed"):
        os.makedirs(os.path.join(RES, "block"), exist_ok=True)
        for i, (cid, _name_es, _name_en, _rgb, vanilla) in enumerate(COLORS):
            if color and cid != color:
                continue
            partner = COLORS[15 - i][4]
            _w, _h, draw = vanilla_png(SOURCE_GLAZED_TERRACOTTA.format(color=partner))
            _w2, _h2, pal = vanilla_png(SOURCE_GLAZED_TERRACOTTA.format(color=vanilla))
            dest = os.path.join(RES, "block", f"{cid}_glazed_terracotta.png")
            write_png(dest, _w, _h, palette_transfer(draw, pal))
            print(f"   {os.path.relpath(dest, ROOT)}  (dibujo {partner}, paleta {vanilla})")
    if what in ("all", "flowers"):
        os.makedirs(os.path.join(RES, "block"), exist_ok=True)
        os.makedirs(os.path.join(RES, "item"), exist_ok=True)
        for cid, _name_es, _name_en, rgb, _vanilla in COLORS:
            if color and cid != color:
                continue
            if cid in TORCHFLOWER_FLOWERS:
                _w, _h, src = vanilla_png(SOURCE_FLOWER_TORCHFLOWER)
                dest = os.path.join(RES, "block", f"{cid}_torchflower.png")
                write_png(dest, _w, _h, recolor_flower_part(src, rgb, TORCHFLOWER_FLOWER_COLORS))
                print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X} (petalos, centro vanilla)")
                mdata = os.path.join(RES, "block", f"{cid}_torchflower.png.mcmeta")
                with open(mdata, "w", encoding="utf-8") as f:
                    json.dump({"texture": {"mipmap_strategy": "strict_cutout"}}, f)
                print(f"   {os.path.relpath(mdata, ROOT)}")
                _w, _h, ssrc = vanilla_png(SOURCE_TORCHFLOWER_SEEDS)
                sdest = os.path.join(RES, "item", f"{cid}_torchflower_seeds.png")
                write_png(sdest, _w, _h, recolor(ssrc, rgb))
                print(f"   {os.path.relpath(sdest, ROOT)}  #{rgb:06X} (semillas)")
            elif cid in PITCHER_FLOWERS:
                _w, _h, src = vanilla_png(SOURCE_FLOWER_PITCHER)
                dest = os.path.join(RES, "block", f"{cid}_pitcher_plant.png")
                write_png(dest, _w, _h, recolor(src, rgb))
                print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X} (flor entera)")
                _w, _h, ssrc = vanilla_png(SOURCE_PITCHER_POD)
                sdest = os.path.join(RES, "item", f"{cid}_pitcher_seeds.png")
                write_png(sdest, _w, _h, recolor(ssrc, rgb))
                print(f"   {os.path.relpath(sdest, ROOT)}  #{rgb:06X} (semillas)")