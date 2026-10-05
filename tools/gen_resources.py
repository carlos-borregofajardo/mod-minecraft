"""
JSON resource generator for Sniffer Blooms.

Writes the data files the game needs to display and use the 16 dyes: item
definitions, item models and the two vanilla recipe overrides.

    python tools/gen_resources.py

Output:
  assets/sniffer_blooms/items/<id>_dye.json       item definition
  assets/sniffer_blooms/models/item/<id>_dye.json item model
  data/minecraft/recipe/*_from_*.json             overridden vanilla recipes

Do not edit the generated files by hand, they get overwritten on every run.

The translation files are NOT generated here, they are edited by hand. This script
used to write lang/en_us.json and lang/es_es.json from scratch, which wiped out
every block name that had been added to them, because the blocks are registered one
by one and only the dyes were listed below. Keep it that way: add new names to
lang/en_us.json and lang/es_es.json manually.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "sniffer_blooms")
DATA = os.path.join(ROOT, "src", "main", "resources", "data")
NS = "sniffer_blooms"

# Fields: (id, name_es, name_en, hex, closest vanilla dye color)
# Mirrors COLORS in gen_textures.py. Kept in sync by hand, so change both together.
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
    """Save a Python object as a pretty-printed JSON file.

    ensure_ascii=False keeps the accented Spanish names readable instead of
    turning them into \\uXXXX escapes.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("   ", os.path.relpath(path, ROOT))


def gen_item_defs():
    """Write one item definition per dye.

    This is the file that tells the game "an item called sniffer_blooms:soft_terracotta_dye
    exists, and it is drawn with this model". Without it, registering the item in Java
    makes it exist in code but invisible in the game.
    """
    print("[items]")
    for cid, _name_es, _name_en, _rgb, _vanilla in COLORS:
        write(os.path.join(ASSETS, "items", f"{cid}_dye.json"), {
            "model": {"type": "minecraft:model", "model": f"{NS}:item/{cid}_dye"}
        })


def gen_models():
    """Write the item model per dye, which points at the PNG texture.

    The parent "item/generated" is the vanilla template for flat 2D sprites, the
    same one every vanilla dye uses.
    """
    print("[models]")
    for cid, _name_es, _name_en, _rgb, _vanilla in COLORS:
        write(os.path.join(ASSETS, "models", "item", f"{cid}_dye.json"), {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{NS}:item/{cid}_dye"}
        })


def gen_lang():
    """Removed on purpose, see the note at the top of the file.

    It rewrote both lang files from scratch, so running the script deleted the name of
    every block that had been added to them. Translations are maintained by hand now.
    """
    raise SystemExit(
        "gen_lang() esta deshabilitado a proposito: las traducciones se editan a mano "
        "en assets/sniffer_blooms/lang/en_us.json y es_es.json"
    )


# The two vanilla plants are repurposed so their recipes yield our first two dyes.
# Fields: (recipe file name, vanilla ingredient, our color id, amount, recipe group)
# The recipe path is written under data/minecraft/, which replaces the vanilla recipe
# of the same name. The original group is kept so they still show up together in the
# recipe book, and the original yield amount is preserved.
VANILLA_RECIPE_OVERRIDES = [
    ("orange_dye_from_torchflower", "torchflower", "soft_terracotta", 1, "orange_dye"),
    ("cyan_dye_from_pitcher_plant", "pitcher_plant", "fossil_turquoise", 2, "cyan_dye"),
]


def gen_recipe_overrides():
    """Write the two recipes that replace the vanilla torchflower and pitcher ones.

    Torchflower now gives the terracotta dye, pitcher plant the turquoise one. This is
    the only change the mod makes to vanilla behavior so far, and the 16 vanilla dyes
    themselves are left untouched.
    """
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
    gen_recipe_overrides()
    print("listo")