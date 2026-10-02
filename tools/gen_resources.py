"""
Genera los recursos JSON de Sniffer Blooms a partir de la tabla de FossilColor.

    python tools/gen_resources.py

Genera:
  assets/sniffer_blooms/items/<id>_dye.json      definicion de item
  assets/sniffer_blooms/models/item/<id>_dye.json modelo
  assets/sniffer_blooms/lang/es_es.json          traduccion
  assets/sniffer_blooms/lang/en_us.json          traduccion
  data/minecraft/recipe/*_from_*.json            recetas vanilla sobrescritas
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "sniffer_blooms")
DATA = os.path.join(ROOT, "src", "main", "resources", "data")
NS = "sniffer_blooms"

# (id, nombre_es, nombre_en, hex, vanilla_dye, bioma)
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


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("   ", os.path.relpath(path, ROOT))


def gen_item_defs():
    print("[items]")
    for cid, _es, _en, _rgb, _vd in COLORS:
        write(os.path.join(ASSETS, "items", f"{cid}_dye.json"), {
            "model": {"type": "minecraft:model", "model": f"{NS}:item/{cid}_dye"}
        })


def gen_models():
    print("[models]")
    for cid, _es, _en, _rgb, _vd in COLORS:
        write(os.path.join(ASSETS, "models", "item", f"{cid}_dye.json"), {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{NS}:item/{cid}_dye"}
        })


def gen_lang():
    print("[lang]")
    for lang, idx in (("es_es", 1), ("en_us", 2)):
        data = {f"item.{NS}.{cid}_dye": row[idx] for row in COLORS for cid in [row[0]]}
        write(os.path.join(ASSETS, "lang", f"{lang}.json"), data)


# Las dos plantas vanilla: Torchflower -> Terracota suave, Pitcher Plant -> Turquesa fosil
# Se sobrescriben las recetas vanilla, conservando el grupo para que sigan apareciendo
# en el libro de recetas junto a las demas recetas de tinte.
VANILLA_RECIPE_OVERRIDES = [
    ("orange_dye_from_torchflower", "torchflower", "soft_terracotta", 1, "orange_dye"),
    ("cyan_dye_from_pitcher_plant", "pitcher_plant", "fossil_turquoise", 2, "cyan_dye"),
]


def gen_recipe_overrides():
    print("[recipes vanilla sobrescritas]")
    for name, ingredient, target, count, group in VANILLA_RECIPE_OVERRIDES:
        write(os.path.join(DATA, "minecraft", "recipe", f"{name}.json"), {
            "type": "minecraft:crafting_shapeless",
            "group": group,
            "ingredients": [f"minecraft:{ingredient}"],
            "result": {"count": count, "id": f"{NS}:{target}_dye"}
        })


if __name__ == "__main__":
    gen_item_defs()
    gen_models()
    gen_lang()
    gen_recipe_overrides()
    print("listo")