"""
Texture generator for Sniffer Blooms.

Recolors a vanilla Minecraft item texture into one of the 16 fossil dye colors,
preserving the shading and the outline of the original sprite. Instead of painting
a flat color, it measures how dark each pixel is relative to the dominant color of
the source texture, then reproduces that same ratio using the destination color.

    python tools/gen_textures.py            # everything
    python tools/gen_textures.py dyes       # only the dyes
    python tools/gen_textures.py plants     # only the plants

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


def dominant_color(pixels):
    """Find the main flat color of a texture.

    Tints are mostly one solid color plus darker shading and an outline. The most
    frequent opaque color is that main color, and it is the reference point used to
    measure how dark every other pixel is.
    """
    counts = {}
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < 128:
            continue  # skip transparent pixels
        key = pixels[i:i + 3]
        counts[key] = counts.get(key, 0) + 1
    return max(counts.items(), key=lambda kv: kv[1])[0]


def recolor(src_pixels, target_rgb):
    """Redraw a texture in the target color, keeping the original shading.

    For every pixel, work out how much darker it is than the dominant color
    (a ratio between 0 and 1), then multiply the target color by that ratio. A
    shadow pixel keeps being a shadow, just in the new hue. Fully transparent
    pixels are copied untouched so the outline and the silhouette stay correct.
    """
    base = dominant_color(src_pixels)
    base_l = luminance(base[0], base[1], base[2]) or 1.0  # avoid divide by zero
    tr = (target_rgb >> 16) & 0xFF  # unpack 0xRRGGBB into R, G, B
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF

    out = bytearray(src_pixels)
    for i in range(0, len(src_pixels), 4):
        if src_pixels[i + 3] < 128:
            continue  # keep transparency as it is
        scale = luminance(src_pixels[i], src_pixels[i + 1], src_pixels[i + 2]) / base_l
        out[i] = max(0, min(255, round(tr * scale)))
        out[i + 1] = max(0, min(255, round(tg * scale)))
        out[i + 2] = max(0, min(255, round(tb * scale)))
    return bytes(out)


def generate(kind, source_entry, folder, prefix, suffix=""):
    """Recolor one vanilla texture into all 16 colors and save the results.

    kind          -> label printed in the console, e.g. "dyes"
    source_entry  -> path of the vanilla texture inside the cache jar
    folder        -> subfolder of assets/sniffer_blooms/textures to write into
    prefix/suffix -> wrapped around the color id to build the file name
    """
    data = find_in_cache(source_entry)
    tmp = os.path.join(os.environ.get("TEMP", "."), "_sb_src.png")
    open(tmp, "wb").write(data)  # read_png works on a path, so drop it on disk first
    w, h, src = read_png(tmp)

    outdir = os.path.join(RES, folder)
    os.makedirs(outdir, exist_ok=True)
    print(f"[{kind}] base {source_entry} ({w}x{h}) -> {outdir}")

    for cid, _name_es, _name_en, rgb, _vanilla in COLORS:
        dest = os.path.join(outdir, f"{prefix}{cid}{suffix}.png")
        write_png(dest, w, h, recolor(src, rgb))
        print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "dyes"):
        generate("dyes", SOURCE_DYE, "item", "", "_dye")
    if what in ("all", "plants"):
        generate("plants", SOURCE_PLANT, "item", "plant_")