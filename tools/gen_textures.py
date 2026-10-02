"""
Generador de texturas de Sniffer Blooms.

Recolorea texturas vanilla de Minecraft al hex del color, preservando el
sombreado y el detalle del sprite original. En vez de pintar un color plano,
mide el brillo de cada pixel respecto al color dominante de la textura base y
reproduce ese ratio con el color de destino.

Uso:
    python tools/gen_textures.py            # genera todo
    python tools/gen_textures.py dyes       # solo tintes
    python tools/gen_textures.py plants     # solo plantas

Requiere la textura fuente vanilla, que se extrae de la cache de ForgeGradle.
"""

import glob
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from png import read_png, write_png  # noqa: E402

# --- Los 16 colores (mod.txt) ---------------------------------------------
# (id, nombre_es, nombre_en, hex, vanilla_dye_equivalente, bioma)
COLORS = [
    ("soft_terracotta", "Tinte Terracota Suave", "Soft Terracotta Dye", 0xD98A62, "orange", "Desierto"),
    ("fossil_turquoise", "Tinte Turquesa Fosil", "Fossil Turquoise Dye", 0x62B7AE, "cyan", "Playa"),
    ("ancient_rose", "Tinte Rosa Antiguo", "Ancient Rose Dye", 0xD889A5, "magenta", "Bosque floral"),
    ("fern_green", "Tinte Verde Helecho", "Fern Green Dye", 0x658F68, "green", "Jungla"),
    ("pollen_yellow", "Tinte Amarillo Polen", "Pollen Yellow Dye", 0xE5C968, "yellow", "Sabana"),
    ("lavender", "Tinte Lavanda", "Lavender Dye", 0xA58FBE, "purple", "Pantano"),
    ("mist_blue", "Tinte Azul Bruma", "Mist Blue Dye", 0x8EC6D4, "light_blue", "Taiga"),
    ("stone_gray", "Tinte Gris Piedra", "Stone Gray Dye", 0x858783, "gray", "Picos pedregosos"),
    ("ash_gray", "Tinte Gris Ceniza", "Ash Gray Dye", 0xB9B7A9, "light_gray", "Bosque de abedules"),
    ("clay_red", "Tinte Rojo Arcilla", "Clay Red Dye", 0xB85F5A, "red", "Bosque oscuro"),
    ("bark_brown", "Tinte Marron Corteza", "Bark Brown Dye", 0x9A7255, "brown", "Taiga de pinos"),
    ("fossil_blue", "Tinte Azul Fosil", "Fossil Blue Dye", 0x668EB8, "blue", "Playa fria / nevada"),
    ("fossil_ivory", "Tinte Marfil Fosil", "Fossil Ivory Dye", 0xE8E2D0, "white", "Llanuras nevadas"),
    ("soft_lime", "Tinte Lima Suave", "Soft Lime Dye", 0xA8C875, "lime", "Pradera"),
    ("coral", "Tinte Coral", "Coral Dye", 0xE6A6B8, "pink", "Pantano de manglares"),
    ("obsidian", "Tinte Obsidiana", "Obsidian Dye", 0x3D3B3A, "black", "Deep Dark"),
]

# Textura vanilla usada como base para cada tipo de contenido
SOURCE_DYE = "assets/minecraft/textures/item/white_dye.png"
SOURCE_PLANT = "assets/minecraft/textures/item/pitcher_pod.png"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "src", "main", "resources", "assets", "sniffer_blooms", "textures")
CACHE = os.path.expanduser(r"~\.gradle\caches\minecraftforge\forgegradle\mavenizer\caches")


def find_in_cache(entry):
    """Localiza una entrada dentro de los jar de la cache de ForgeGradle."""
    for jar in glob.glob(os.path.join(CACHE, "**", "*.jar"), recursive=True):
        try:
            with zipfile.ZipFile(jar) as z:
                if entry in z.namelist():
                    return z.read(entry)
        except Exception:
            continue
    raise FileNotFoundError(f"no se encontro {entry} en la cache de ForgeGradle")


def luminance(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b


def dominant_color(pixels):
    """Color opaco mas frecuente de la textura."""
    counts = {}
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] < 128:
            continue
        key = pixels[i:i + 3]
        counts[key] = counts.get(key, 0) + 1
    return max(counts.items(), key=lambda kv: kv[1])[0]


def recolor(src_pixels, target_rgb):
    """Reaplica el sombreado de src_pixels con el color target_rgb."""
    base = dominant_color(src_pixels)
    base_l = luminance(base[0], base[1], base[2]) or 1.0
    tr = (target_rgb >> 16) & 0xFF
    tg = (target_rgb >> 8) & 0xFF
    tb = target_rgb & 0xFF

    out = bytearray(src_pixels)
    for i in range(0, len(src_pixels), 4):
        if src_pixels[i + 3] < 128:
            continue
        scale = luminance(src_pixels[i], src_pixels[i + 1], src_pixels[i + 2]) / base_l
        out[i] = max(0, min(255, round(tr * scale)))
        out[i + 1] = max(0, min(255, round(tg * scale)))
        out[i + 2] = max(0, min(255, round(tb * scale)))
    return bytes(out)


def generate(kind, source_entry, folder, prefix, suffix="", only_ids=None):
    data = find_in_cache(source_entry)
    tmp = os.path.join(os.environ.get("TEMP", "."), "_sb_src.png")
    open(tmp, "wb").write(data)
    w, h, src = read_png(tmp)

    outdir = os.path.join(RES, folder)
    os.makedirs(outdir, exist_ok=True)
    print(f"[{kind}] base {source_entry} ({w}x{h}) -> {outdir}")

    for cid, _es, _en, rgb, _vd, _bioma in COLORS:
        if only_ids and cid not in only_ids:
            continue
        dest = os.path.join(outdir, f"{prefix}{cid}{suffix}.png")
        write_png(dest, w, h, recolor(src, rgb))
        print(f"   {os.path.relpath(dest, ROOT)}  #{rgb:06X}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "dyes"):
        generate("tintes", SOURCE_DYE, "item", "", "_dye")
    if what in ("all", "plants"):
        generate("plantas", SOURCE_PLANT, "item", "plant_")