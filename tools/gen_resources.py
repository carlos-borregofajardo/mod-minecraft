"""
Genera todos los recursos JSON de Sniffer Blooms para los 16 colores.

    python tools/gen_resources.py            # solo los archivos que faltan
    python tools/gen_resources.py --force    # regenera todo (incluido soft_terracotta)

Genera, por color:
  blockstates, models/block, models/item, items, recipe, loot_table/blocks
Y, compartidos:
  lang/es_es.json, lang/en_us.json, data/minecraft/tags/*

La fuente de verdad de los colores (id, nombre_es, nombre_en, hex, dye vanilla)
es exactamente la misma tabla que usa gen_textures.py.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "sniffer_blooms")
DATA = os.path.join(ROOT, "src", "main", "resources", "data")
NS = "sniffer_blooms"

# (id, nombre_es, nombre_en, hex, vanilla_dye)
# Los nombres son el "color" en si (el que va en "Lana X", "Cama X", ...),
# sin el prefijo "Tinte " ni el sufijo " Dye".
COLORS = [
    ("soft_terracotta", "Terracota Suave", "Soft Terracotta", 0xD98A62, "orange"),
    ("fossil_turquoise", "Turquesa Fosil", "Fossil Turquoise", 0x62B7AE, "cyan"),
    ("ancient_rose", "Rosa Antiguo", "Ancient Rose", 0xD889A5, "magenta"),
    ("fern_green", "Verde Helecho", "Fern Green", 0x658F68, "green"),
    ("pollen_yellow", "Amarillo Polen", "Pollen Yellow", 0xE5C968, "yellow"),
    ("lavender", "Lavanda", "Lavender", 0xA58FBE, "purple"),
    ("mist_blue", "Azul Bruma", "Mist Blue", 0x8EC6D4, "light_blue"),
    ("stone_gray", "Gris Piedra", "Stone Gray", 0x858783, "gray"),
    ("ash_gray", "Gris Ceniza", "Ash Gray", 0xB9B7A9, "light_gray"),
    ("clay_red", "Rojo Arcilla", "Clay Red", 0xB85F5A, "red"),
    ("bark_brown", "Marron Corteza", "Bark Brown", 0x9A7255, "brown"),
    ("fossil_blue", "Azul Fosil", "Fossil Blue", 0x668EB8, "blue"),
    ("fossil_ivory", "Marfil Fosil", "Fossil Ivory", 0xE8E2D0, "white"),
    ("soft_lime", "Lima Suave", "Soft Lime", 0xA8C875, "lime"),
    ("coral", "Coral", "Coral", 0xE6A6B8, "pink"),
    ("obsidian", "Obsidiana", "Obsidian", 0x3D3B3A, "black"),
]

# Orden canonical del enum DyeColor vanilla; se usa para excluir el equivalente
# del color en las recetas bed_from_dye / harness_from_dye.
DYE_COLOR_ORDER = [
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink",
    "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black",
]

BLOCK_PRODUCTS = ["wool", "carpet", "terracotta", "glazed_terracotta", "stained_glass",
                  "stained_glass_pane", "concrete", "concrete_powder", "candle",
                  "shulker_box", "bed", "candle_cake", "torchflower", "pitcher_plant"]
ITEM_PRODUCTS = ["dye", "harness", "bundle"]

# The 16 fossil colors do not all become both flowers: warm hues become the
# torchflower, cool hues become the pitcher plant (see gen_textures.py).
TORCHFLOWER_COLORS = {"soft_terracotta", "ancient_rose", "pollen_yellow", "clay_red",
                      "bark_brown", "fossil_ivory", "coral", "ash_gray"}
PITCHER_COLORS = {"fossil_turquoise", "fern_green", "lavender", "mist_blue",
                  "stone_gray", "fossil_blue", "soft_lime", "obsidian"}

PREFIX_ES = {
    "dye": "Tinte ", "wool": "Lana ", "carpet": "Alfombra ", "terracotta": "",
    "glazed_terracotta": "Azulejo ", "stained_glass": "Cristal ", "stained_glass_pane": "Panel de Cristal ",
    "concrete": "Hormigón ", "concrete_powder": "Polvo de Hormigón ", "candle": "Vela ",
    "shulker_box": "Cofre de Shulker ", "bed": "Cama ", "harness": "Arnés ",
    "bundle": "Saco ", "candle_cake": "Tarta con Vela ",
    "torchflower": "Torchflower de ", "pitcher_plant": "Planta de Jarro de ",
    "torchflower_seeds": "Semillas de Torchflower de ", "pitcher_seeds": "Semillas de Planta de Jarro de ",
}
SUFFIX_EN = {
    "dye": " Dye", "wool": " Wool", "carpet": " Carpet", "terracotta": "",
    "glazed_terracotta": " Glazed Terracotta", "stained_glass": " Stained Glass",
    "stained_glass_pane": " Stained Glass Pane", "concrete": " Concrete",
    "concrete_powder": " Concrete Powder", "candle": " Candle", "shulker_box": " Shulker Box",
    "bed": " Bed", "harness": " Harness", "bundle": " Bundle", "candle_cake": " Candle Cake",
    "torchflower": " Torchflower", "pitcher_plant": " Pitcher Plant",
    "torchflower_seeds": " Torchflower Seeds", "pitcher_seeds": " Pitcher Plant Seeds",
}


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("   ", os.path.relpath(path, ROOT))


def safe_write(path, data, force=False):
    if os.path.exists(path) and not force:
        return
    write(path, data)


def model_ref(name):
    return f"{NS}:{name}"


def block_ref(cid, kind):
    return model_ref(f"block/{cid}_{kind}")


def item_ref(cid, kind):
    return model_ref(f"item/{cid}_{kind}")


# --- blockstates ------------------------------------------------------------


def blockstate_bed(cid):
    yrots = {"east": 90, "north": 0, "south": 180, "west": 270}
    variants = {}
    for facing, y in yrots.items():
        for part in ("foot", "head"):
            entry = {"model": block_ref(cid, f"bed_{part}")}
            if y:
                entry["y"] = y
            variants[f"facing={facing},part={part}"] = entry
    return {"variants": variants}


def blockstate_candle(cid):
    names = {1: "one_candle", 2: "two_candles", 3: "three_candles", 4: "four_candles"}
    variants = {}
    for count, name in names.items():
        for lit in ("false", "true"):
            lit_suffix = "_lit" if lit == "true" else ""
            variants[f"candles={count},lit={lit}"] = {"model": block_ref(cid, name + lit_suffix)}
    return {"variants": variants}


def blockstate_candle_cake(cid):
    return {
        "variants": {
            "lit=false": {"model": block_ref(cid, "candle_cake")},
            "lit=true": {"model": block_ref(cid, "candle_cake_lit")},
        }
    }


def blockstate_simple(cid, kind):
    return {"variants": {"": {"model": block_ref(cid, kind)}}}


def blockstate_glazed(cid):
    return {
        "variants": {
            "facing=north": {"model": block_ref(cid, "glazed_terracotta"), "y": 180},
            "facing=south": {"model": block_ref(cid, "glazed_terracotta")},
            "facing=east": {"model": block_ref(cid, "glazed_terracotta"), "y": 90},
            "facing=west": {"model": block_ref(cid, "glazed_terracotta"), "y": 270},
        }
    }


def blockstate_glass_pane(cid):
    glass = block_ref(cid, "stained_glass")
    return {
        "multipart": [
            {"apply": {"model": block_ref(cid, "stained_glass_pane_post")}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_side")}, "when": {"north": "true"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_side"), "y": 90}, "when": {"east": "true"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_side_alt")}, "when": {"south": "true"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_side_alt"), "y": 90}, "when": {"west": "true"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_noside")}, "when": {"north": "false"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_noside_alt")}, "when": {"east": "false"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_noside_alt"), "y": 90}, "when": {"south": "false"}},
            {"apply": {"model": block_ref(cid, "stained_glass_pane_noside"), "y": 270}, "when": {"west": "false"}},
        ]
    }


def gen_blockstates(force):
    print("[blockstates]")
    for cid, *_ in COLORS:
        base = os.path.join(ASSETS, "blockstates")
        safe_write(os.path.join(base, f"{cid}_bed.json"), blockstate_bed(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle.json"), blockstate_candle(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle_cake.json"), blockstate_candle_cake(cid), force)
        for kind in ("carpet", "concrete", "concrete_powder", "terracotta", "wool", "shulker_box", "stained_glass"):
            safe_write(os.path.join(base, f"{cid}_{kind}.json"), blockstate_simple(cid, kind), force)
        safe_write(os.path.join(base, f"{cid}_glazed_terracotta.json"), blockstate_glazed(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass_pane.json"), blockstate_glass_pane(cid), force)


# --- models/block -----------------------------------------------------------


def model_bed_foot(cid):
    return {
        "parent": "minecraft:block/template_bed_foot",
        "textures": {
            "east": block_ref(cid, "bed_foot_east"),
            "south": block_ref(cid, "bed_foot_south"),
            "up": block_ref(cid, "bed_foot_up"),
            "west": block_ref(cid, "bed_foot_west"),
        },
    }


def model_bed_head(cid):
    return {
        "parent": "minecraft:block/template_bed_head",
        "textures": {
            "east": block_ref(cid, "bed_head_east"),
            "up": block_ref(cid, "bed_head_up"),
            "west": block_ref(cid, "bed_head_west"),
        },
    }


def model_candle_cake(cid, lit):
    return {
        "parent": "minecraft:block/template_cake_with_candle",
        "textures": {
            "bottom": "minecraft:block/cake_bottom",
            "candle": block_ref(cid, "candle" + ("_lit" if lit else "")),
            "particle": "minecraft:block/cake_side",
            "side": "minecraft:block/cake_side",
            "top": "minecraft:block/cake_top",
        },
    }


def model_candles(cid, count, lit):
    names = {1: "candle", 2: "two_candles", 3: "three_candles", 4: "four_candles"}
    return {
        "parent": f"minecraft:block/template_{names[count]}",
        "textures": {
            "all": block_ref(cid, "candle" + ("_lit" if lit else "")),
            "particle": block_ref(cid, "candle" + ("_lit" if lit else "")),
        },
    }


def model_cube_all(cid, kind):
    return {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": block_ref(cid, kind)},
    }


def model_carpet(cid):
    return {
        "parent": "minecraft:block/carpet",
        "textures": {"wool": block_ref(cid, "wool")},
    }


def model_glazed(cid):
    return {
        "parent": "minecraft:block/template_glazed_terracotta",
        "textures": {"pattern": block_ref(cid, "glazed_terracotta")},
    }


def model_shulker_box(cid):
    return {"textures": {"particle": block_ref(cid, "shulker_box")}}


def translucent_sprite(sprite):
    return {"force_translucent": True, "sprite": sprite}


def model_glass(cid):
    return {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": translucent_sprite(block_ref(cid, "stained_glass"))},
    }


def model_glass_pane(cid, orientation):
    return {
        "parent": f"minecraft:block/template_glass_pane_{orientation}",
        "textures": {
            "edge": translucent_sprite(block_ref(cid, "stained_glass_pane_top")),
            "pane": translucent_sprite(block_ref(cid, "stained_glass")),
        },
    }


def gen_block_models(force):
    print("[models/block]")
    base = os.path.join(ASSETS, "models", "block")
    for cid, *_ in COLORS:
        safe_write(os.path.join(base, f"{cid}_bed_foot.json"), model_bed_foot(cid), force)
        safe_write(os.path.join(base, f"{cid}_bed_head.json"), model_bed_head(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle_cake.json"), model_candle_cake(cid, False), force)
        safe_write(os.path.join(base, f"{cid}_candle_cake_lit.json"), model_candle_cake(cid, True), force)
        for count in (1, 2, 3, 4):
            names = {1: "one_candle", 2: "two_candles", 3: "three_candles", 4: "four_candles"}
            safe_write(os.path.join(base, f"{cid}_{names[count]}.json"), model_candles(cid, count, False), force)
            safe_write(os.path.join(base, f"{cid}_{names[count]}_lit.json"), model_candles(cid, count, True), force)
        safe_write(os.path.join(base, f"{cid}_carpet.json"), model_carpet(cid), force)
        for kind in ("concrete", "concrete_powder", "terracotta", "wool"):
            safe_write(os.path.join(base, f"{cid}_{kind}.json"), model_cube_all(cid, kind), force)
        safe_write(os.path.join(base, f"{cid}_glazed_terracotta.json"), model_glazed(cid), force)
        safe_write(os.path.join(base, f"{cid}_shulker_box.json"), model_shulker_box(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass.json"), model_glass(cid), force)
        for orientation in ("noside", "noside_alt", "post", "side", "side_alt"):
            safe_write(os.path.join(base, f"{cid}_stained_glass_pane_{orientation}.json"), model_glass_pane(cid, orientation), force)


# --- models/item ------------------------------------------------------------


def model_item_generated(cid, kind, texture=None):
    return {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": texture or item_ref(cid, kind)},
    }


def model_item_glazed(cid):
    return {
        "parent": block_ref(cid, "glazed_terracotta"),
        "display": {
            "gui": {"rotation": [30, 225, 0], "translation": [0, 0, 0], "scale": [0.625, 0.625, 0.625]},
            "ground": {"rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [0.25, 0.25, 0.25]},
            "fixed": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.5, 0.5, 0.5]},
        },
    }


def model_item_shulker_box(cid):
    return {
        "parent": "minecraft:item/template_shulker_box",
        "textures": {"particle": block_ref(cid, "shulker_box")},
    }


def gen_item_models(force):
    print("[models/item]")
    base = os.path.join(ASSETS, "models", "item")
    for cid, *_ in COLORS:
        safe_write(os.path.join(base, f"{cid}_bundle.json"), model_item_generated(cid, "bundle"), force)
        safe_write(os.path.join(base, f"{cid}_bundle_open_back.json"),
                   model_item_generated(cid, "bundle_open_back"), force)
        safe_write(os.path.join(base, f"{cid}_bundle_open_front.json"),
                   model_item_generated(cid, "bundle_open_front"), force)
        safe_write(os.path.join(base, f"{cid}_candle.json"), model_item_generated(cid, "candle"), force)
        safe_write(os.path.join(base, f"{cid}_dye.json"), model_item_generated(cid, "dye"), force)
        safe_write(os.path.join(base, f"{cid}_glazed_terracotta.json"), model_item_glazed(cid), force)
        safe_write(os.path.join(base, f"{cid}_harness.json"), model_item_generated(cid, "harness"), force)
        safe_write(os.path.join(base, f"{cid}_shulker_box.json"), model_item_shulker_box(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass_pane.json"),
                   model_item_generated(cid, "stained_glass_pane", block_ref(cid, "stained_glass")), force)


# --- items ------------------------------------------------------------------


def item_bed(cid):
    return {
        "model": {
            "type": "minecraft:composite",
            "models": [
                {"type": "minecraft:model", "model": block_ref(cid, "bed_head")},
                {
                    "type": "minecraft:model",
                    "model": block_ref(cid, "bed_foot"),
                    "transformation": {
                        "left_rotation": [0.0, 0.0, 0.0, 1.0],
                        "right_rotation": [0.0, 0.0, 0.0, 1.0],
                        "scale": [1.0, 1.0, 1.0],
                        "translation": [0.0, 0.0, 1.0],
                    },
                },
            ],
        }
    }


def item_bundle(cid):
    return {
        "model": {
            "type": "minecraft:select",
            "cases": [
                {
                    "model": {
                        "type": "minecraft:condition",
                        "on_false": {"type": "minecraft:model", "model": item_ref(cid, "bundle")},
                        "on_true": {
                            "type": "minecraft:composite",
                            "models": [
                                {"type": "minecraft:model", "model": item_ref(cid, "bundle_open_back")},
                                {"type": "minecraft:bundle/selected_item"},
                                {"type": "minecraft:model", "model": item_ref(cid, "bundle_open_front")},
                            ],
                        },
                        "property": "minecraft:bundle/has_selected_item",
                    },
                    "when": "gui",
                }
            ],
            "fallback": {"type": "minecraft:model", "model": item_ref(cid, "bundle")},
            "property": "minecraft:display_context",
        }
    }


def item_simple(cid, kind):
    return {"model": {"type": "minecraft:model", "model": model_ref(f"block/{cid}_{kind}")}}


def item_glazed(cid):
    return {"model": {"type": "minecraft:model", "model": item_ref(cid, "glazed_terracotta")}}


def item_item(cid, kind):
    return {"model": {"type": "minecraft:model", "model": item_ref(cid, kind)}}


def item_shulker_box(cid):
    return {
        "model": {
            "type": "minecraft:special",
            "base": item_ref(cid, "shulker_box"),
            "model": {
                "type": "minecraft:shulker_box",
                "texture": f"{NS}:shulker_{cid}",
            },
            "transformation": {
                "left_rotation": [1.0, 0.0, 0.0, 0.0],
                "right_rotation": [-0.0, -0.0, -0.0, 1.0],
                "scale": [0.9995, 0.9995, 0.9995],
                "translation": [0.5, 1.4995, 0.5],
            },
        }
    }


def gen_items(force):
    print("[items]")
    base = os.path.join(ASSETS, "items")
    for cid, *_ in COLORS:
        safe_write(os.path.join(base, f"{cid}_bed.json"), item_bed(cid), force)
        safe_write(os.path.join(base, f"{cid}_bundle.json"), item_bundle(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle.json"), item_item(cid, "candle"), force)
        safe_write(os.path.join(base, f"{cid}_carpet.json"), item_simple(cid, "carpet"), force)
        safe_write(os.path.join(base, f"{cid}_concrete.json"), item_simple(cid, "concrete"), force)
        safe_write(os.path.join(base, f"{cid}_concrete_powder.json"), item_simple(cid, "concrete_powder"), force)
        safe_write(os.path.join(base, f"{cid}_dye.json"), item_item(cid, "dye"), force)
        safe_write(os.path.join(base, f"{cid}_glazed_terracotta.json"), item_glazed(cid), force)
        safe_write(os.path.join(base, f"{cid}_harness.json"), item_item(cid, "harness"), force)
        safe_write(os.path.join(base, f"{cid}_shulker_box.json"), item_shulker_box(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass.json"), item_simple(cid, "stained_glass"), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass_pane.json"), item_item(cid, "stained_glass_pane"), force)
        safe_write(os.path.join(base, f"{cid}_terracotta.json"), item_simple(cid, "terracotta"), force)
        safe_write(os.path.join(base, f"{cid}_wool.json"), item_simple(cid, "wool"), force)


# --- recipes -----------------------------------------------------------------


def vanilla_equivalent_list(suffix, exclude):
    return [f"minecraft:{name}_{suffix}" for name in DYE_COLOR_ORDER if name != exclude]


def recipe_bed(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "group": "bed",
        "key": {
            "#": f"{NS}:{cid}_wool",
            "X": "#minecraft:planks",
        },
        "pattern": ["###", "XXX"],
        "result": {"id": f"{NS}:{cid}_bed"},
    }


def recipe_bed_from_dye(cid, exclude):
    return {
        "type": "minecraft:crafting_shapeless",
        "group": "bed_dye",
        "ingredients": [f"{NS}:{cid}_dye", vanilla_equivalent_list("bed", exclude)],
        "result": {"id": f"{NS}:{cid}_bed"},
    }


def recipe_bundle(cid):
    return {
        "type": "minecraft:crafting_transmute",
        "category": "equipment",
        "group": "bundle_dye",
        "input": "#minecraft:bundles",
        "material": f"{NS}:{cid}_dye",
        "result": {"id": f"{NS}:{cid}_bundle"},
    }


def recipe_candle_from_dye(cid):
    return {
        "type": "minecraft:crafting_shapeless",
        "group": "dyed_candle",
        "ingredients": ["minecraft:candle", f"{NS}:{cid}_dye"],
        "result": {"id": f"{NS}:{cid}_candle"},
    }


def recipe_carpet(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "carpet",
        "key": {"#": f"{NS}:{cid}_wool"},
        "pattern": ["##"],
        "result": {"count": 3, "id": f"{NS}:{cid}_carpet"},
    }


def recipe_carpet_from_dye(cid):
    return {
        "type": "minecraft:crafting_shapeless",
        "category": "building",
        "group": "carpet_dye",
        "ingredients": [f"{NS}:{cid}_dye", "minecraft:white_carpet"],
        "result": {"id": f"{NS}:{cid}_carpet"},
    }


def recipe_concrete_powder(cid):
    return {
        "type": "minecraft:crafting_shapeless",
        "category": "building",
        "group": "concrete_powder",
        "ingredients": [f"{NS}:{cid}_dye"]
        + ["minecraft:sand"] * 4
        + ["minecraft:gravel"] * 4,
        "result": {"count": 8, "id": f"{NS}:{cid}_concrete_powder"},
    }


def recipe_from_dye(cid):
    return {
        "type": "minecraft:crafting_shapeless",
        "category": "building",
        "group": "wool",
        "ingredients": [f"{NS}:{cid}_dye", "minecraft:white_wool"],
        "result": {"id": f"{NS}:{cid}_wool"},
    }


def recipe_glazed_terracotta(cid):
    return {
        "type": "minecraft:smelting",
        "category": "misc",
        "experience": 0.1,
        "cookingtime": 200,
        "ingredient": f"{NS}:{cid}_terracotta",
        "result": f"{NS}:{cid}_glazed_terracotta",
    }


def recipe_harness(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "equipment",
        "group": "harness",
        "key": {
            "#": f"{NS}:{cid}_wool",
            "G": "minecraft:glass",
            "L": "minecraft:leather",
        },
        "pattern": ["LLL", "G#G"],
        "result": {"id": f"{NS}:{cid}_harness"},
    }


def recipe_harness_from_dye(cid, exclude):
    return {
        "type": "minecraft:crafting_shapeless",
        "category": "equipment",
        "group": "harness_dye",
        "ingredients": [f"{NS}:{cid}_dye", vanilla_equivalent_list("harness", exclude)],
        "result": {"id": f"{NS}:{cid}_harness"},
    }


def recipe_stained_glass(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "stained_glass",
        "key": {"#": "minecraft:glass", "X": f"{NS}:{cid}_dye"},
        "pattern": ["###", "#X#", "###"],
        "result": {"count": 8, "id": f"{NS}:{cid}_stained_glass"},
    }


def recipe_stained_glass_pane(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "stained_glass_pane",
        "key": {"#": f"{NS}:{cid}_stained_glass"},
        "pattern": ["###", "###"],
        "result": {"count": 16, "id": f"{NS}:{cid}_stained_glass_pane"},
    }


def recipe_stained_glass_pane_from_glass_pane(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "stained_glass_pane",
        "key": {"#": "minecraft:glass_pane", "$": f"{NS}:{cid}_dye"},
        "pattern": ["###", "#$#", "###"],
        "result": {"count": 8, "id": f"{NS}:{cid}_stained_glass_pane"},
    }


def recipe_terracotta(cid):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "group": "stained_terracotta",
        "key": {"#": "minecraft:terracotta", "X": f"{NS}:{cid}_dye"},
        "pattern": ["###", "#X#", "###"],
        "result": {"count": 8, "id": f"{NS}:{cid}_terracotta"},
    }


def gen_recipes(force):
    print("[recipes s/n]")
    base = os.path.join(DATA, "sniffer_blooms", "recipe")
    for row in COLORS:
        cid, _, _, _, vanilla = row
        safe_write(os.path.join(base, f"{cid}_bed.json"), recipe_bed(cid), force)
        safe_write(os.path.join(base, f"{cid}_bed_from_dye.json"), recipe_bed_from_dye(cid, vanilla), force)
        safe_write(os.path.join(base, f"{cid}_bundle.json"), recipe_bundle(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle_from_dye.json"), recipe_candle_from_dye(cid), force)
        safe_write(os.path.join(base, f"{cid}_carpet.json"), recipe_carpet(cid), force)
        safe_write(os.path.join(base, f"{cid}_carpet_from_dye.json"), recipe_carpet_from_dye(cid), force)
        safe_write(os.path.join(base, f"{cid}_concrete_powder.json"), recipe_concrete_powder(cid), force)
        safe_write(os.path.join(base, f"{cid}_from_dye.json"), recipe_from_dye(cid), force)
        safe_write(os.path.join(base, f"{cid}_glazed_terracotta.json"), recipe_glazed_terracotta(cid), force)
        safe_write(os.path.join(base, f"{cid}_harness.json"), recipe_harness(cid), force)
        safe_write(os.path.join(base, f"{cid}_harness_from_dye.json"), recipe_harness_from_dye(cid, vanilla), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass.json"), recipe_stained_glass(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass_pane.json"), recipe_stained_glass_pane(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass_pane_from_glass_pane.json"),
                   recipe_stained_glass_pane_from_glass_pane(cid), force)
        safe_write(os.path.join(base, f"{cid}_terracotta.json"), recipe_terracotta(cid), force)
        if cid in TORCHFLOWER_COLORS:
            safe_write(os.path.join(base, f"{cid}_torchflower_from_seed.json"),
                       recipe_flower_from_seed(cid, "torchflower", "torchflower_seeds"), force)
            safe_write(os.path.join(base, f"{cid}_torchflower_to_dye.json"),
                       recipe_dye_from_flower(cid, "torchflower"), force)
        if cid in PITCHER_COLORS:
            safe_write(os.path.join(base, f"{cid}_pitcher_plant_from_seed.json"),
                       recipe_flower_from_seed(cid, "pitcher_plant", "pitcher_seeds"), force)
            safe_write(os.path.join(base, f"{cid}_pitcher_plant_to_dye.json"),
                       recipe_dye_from_flower(cid, "pitcher_plant"), force)


def recipe_flower_from_seed(cid, kind, seed):
    return {
        "type": "minecraft:crafting_shaped",
        "key": {"X": f"{NS}:{cid}_{seed}"},
        "pattern": ["X"],
        "result": {"id": f"{NS}:{cid}_{kind}"},
    }


def recipe_dye_from_flower(cid, kind):
    return {
        "type": "minecraft:crafting_shaped",
        "key": {"X": f"{NS}:{cid}_{kind}"},
        "pattern": ["X"],
        "result": {"count": 2, "id": f"{NS}:{cid}_dye"},
    }


# --- loot tables --------------------------------------------------------------


def loot_block_item(cid, item_name, sequence):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "conditions": [{"condition": "minecraft:survives_explosion"}],
                "entries": [{"type": "minecraft:item", "name": item_name}],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{NS}:blocks/{cid}_{sequence}",
    }


def loot_bed(cid):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "conditions": [
                            {
                                "block": f"{NS}:{cid}_bed",
                                "condition": "minecraft:block_state_property",
                                "properties": {"part": "head"},
                            }
                        ],
                        "name": f"{NS}:{cid}_bed",
                    }
                ],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{NS}:blocks/{cid}_bed",
    }


def loot_candle(cid):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "functions": [
                            {
                                "conditions": [
                                    {
                                        "block": f"{NS}:{cid}_candle",
                                        "condition": "minecraft:block_state_property",
                                        "properties": {"candles": "2"},
                                    }
                                ],
                                "count": 2.0,
                                "function": "minecraft:set_count",
                            },
                            {
                                "conditions": [
                                    {
                                        "block": f"{NS}:{cid}_candle",
                                        "condition": "minecraft:block_state_property",
                                        "properties": {"candles": "3"},
                                    }
                                ],
                                "count": 3.0,
                                "function": "minecraft:set_count",
                            },
                            {
                                "conditions": [
                                    {
                                        "block": f"{NS}:{cid}_candle",
                                        "condition": "minecraft:block_state_property",
                                        "properties": {"candles": "4"},
                                    }
                                ],
                                "count": 4.0,
                                "function": "minecraft:set_count",
                            },
                            {"function": "minecraft:explosion_decay"},
                        ],
                        "name": f"{NS}:{cid}_candle",
                    }
                ],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{NS}:blocks/{cid}_candle",
    }


def loot_silk_touch(cid, kind):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "conditions": [
                    {
                        "condition": "minecraft:match_tool",
                        "predicate": {
                            "predicates": {
                                "minecraft:enchantments": [
                                    {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}
                                ]
                            }
                        },
                    }
                ],
                "entries": [{"type": "minecraft:item", "name": f"{NS}:{kind}"}],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{NS}:blocks/{kind}",
    }


def loot_shulker_box(cid):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "functions": [
                            {
                                "function": "minecraft:copy_components",
                                "include": [
                                    "minecraft:custom_name",
                                    "minecraft:container",
                                    "minecraft:lock",
                                    "minecraft:container_loot",
                                ],
                                "source": "block_entity",
                            }
                        ],
                        "name": f"{NS}:{cid}_shulker_box",
                    }
                ],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{NS}:blocks/{cid}_shulker_box",
    }


def gen_loot(force):
    print("[loot]")
    base = os.path.join(DATA, "sniffer_blooms", "loot_table", "blocks")
    for cid, *_ in COLORS:
        safe_write(os.path.join(base, f"{cid}_bed.json"), loot_bed(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle.json"), loot_candle(cid), force)
        safe_write(os.path.join(base, f"{cid}_candle_cake.json"),
                   loot_block_item(cid, f"{NS}:{cid}_candle", "candle_cake"), force)
        for kind, seq in (("carpet", "carpet"), ("concrete", "concrete"),
                          ("concrete_powder", "concrete_powder"), ("terracotta", "terracotta"),
                          ("wool", "wool")):
            safe_write(os.path.join(base, f"{cid}_{kind}.json"),
                       loot_block_item(cid, f"{NS}:{cid}_{kind}", seq), force)
        safe_write(os.path.join(base, f"{cid}_shulker_box.json"), loot_shulker_box(cid), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass.json"),
                   loot_silk_touch(cid, f"{cid}_stained_glass"), force)
        safe_write(os.path.join(base, f"{cid}_stained_glass_pane.json"),
                   loot_silk_touch(cid, f"{cid}_stained_glass_pane"), force)


# --- flowers ------------------------------------------------------------------
# The fossil torchflower / pitcher plant varieties. Faithful to vanilla:
# the torchflower is a single cross block (roots like dandelion) that drops
# itself; the pitcher is a two-block tall plant whose upper half is our flower
# and whose lower half is the vanilla stem (its loot drops only from the lower
# half, exactly like vanilla pitcher_plant). Vanilla also has a potted variant
# of the torchflower, so each fossil torchflower gets its own flower pot.


def blockstate_potted_torchflower(cid):
    return {"variants": {"": {"model": model_ref(f"block/potted_{cid}_torchflower")}}}


def blockstate_pitcher(cid):
    return {
        "variants": {
            "half=lower": {"model": "minecraft:block/pitcher_plant_bottom"},
            "half=upper": {"model": block_ref(cid, "pitcher_plant_top")},
        }
    }


def model_torchflower(cid):
    return {
        "parent": "minecraft:block/cross",
        "textures": {"cross": block_ref(cid, "torchflower")},
    }


def model_pitcher_top(cid):
    # Reuses the vanilla pitcher drawing but paints it with our flower texture.
    tex = block_ref(cid, "pitcher_plant")
    return {
        "parent": "minecraft:block/pitcher_plant_top",
        "textures": {"particle": tex, "top": tex},
    }


def model_potted_torchflower(cid):
    return {
        "parent": "minecraft:block/flower_pot_cross",
        "textures": {"plant": block_ref(cid, "torchflower")},
    }


def loot_torchflower(cid):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "functions": [{"function": "minecraft:explosion_decay"}],
                        "name": f"{NS}:{cid}_torchflower",
                    }
                ],
                "rolls": 1.0,
            },
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "functions": [
                            {
                                "count": {"max": 2.0, "min": 1.0, "type": "minecraft:uniform"},
                                "function": "minecraft:set_count",
                            },
                            {"function": "minecraft:explosion_decay"},
                        ],
                        "name": f"{NS}:{cid}_torchflower_seeds",
                    }
                ],
                "rolls": 1.0,
            },
        ],
        "random_sequence": f"{NS}:blocks/{cid}_torchflower",
    }


def loot_pitcher(cid):
    lower = {
        "block": f"{NS}:{cid}_pitcher_plant",
        "condition": "minecraft:block_state_property",
        "properties": {"half": "lower"},
    }
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "conditions": [lower],
                        "functions": [{"function": "minecraft:explosion_decay"}],
                        "name": f"{NS}:{cid}_pitcher_plant",
                    }
                ],
                "rolls": 1.0,
            },
            {
                "entries": [
                    {
                        "type": "minecraft:item",
                        "conditions": [lower],
                        "functions": [
                            {
                                "count": {"max": 2.0, "min": 1.0, "type": "minecraft:uniform"},
                                "function": "minecraft:set_count",
                            },
                            {"function": "minecraft:explosion_decay"},
                        ],
                        "name": f"{NS}:{cid}_pitcher_seeds",
                    }
                ],
                "rolls": 1.0,
            },
        ],
        "random_sequence": f"{NS}:blocks/{cid}_pitcher_plant",
    }


def gen_flowers(force):
    print("[flowers]")
    bstate_dir = os.path.join(ASSETS, "blockstates")
    bmodel_dir = os.path.join(ASSETS, "models", "block")
    imodel_dir = os.path.join(ASSETS, "models", "item")
    items_dir = os.path.join(ASSETS, "items")
    loot_dir = os.path.join(DATA, "sniffer_blooms", "loot_table", "blocks")
    for cid, *_ in COLORS:
        if cid in TORCHFLOWER_COLORS:
            safe_write(os.path.join(bstate_dir, f"{cid}_torchflower.json"),
                       blockstate_simple(cid, "torchflower"), force)
            safe_write(os.path.join(bstate_dir, f"potted_{cid}_torchflower.json"),
                       blockstate_potted_torchflower(cid), force)
            safe_write(os.path.join(bmodel_dir, f"{cid}_torchflower.json"),
                       model_torchflower(cid), force)
            safe_write(os.path.join(bmodel_dir, f"potted_{cid}_torchflower.json"),
                       model_potted_torchflower(cid), force)
            safe_write(os.path.join(imodel_dir, f"{cid}_torchflower.json"),
                       model_item_generated(cid, "torchflower", block_ref(cid, "torchflower")), force)
            safe_write(os.path.join(items_dir, f"{cid}_torchflower.json"),
                       item_item(cid, "torchflower"), force)
            safe_write(os.path.join(loot_dir, f"{cid}_torchflower.json"),
                       loot_torchflower(cid), force)
        if cid in PITCHER_COLORS:
            safe_write(os.path.join(bstate_dir, f"{cid}_pitcher_plant.json"),
                       blockstate_pitcher(cid), force)
            safe_write(os.path.join(bmodel_dir, f"{cid}_pitcher_plant_top.json"),
                       model_pitcher_top(cid), force)
            safe_write(os.path.join(imodel_dir, f"{cid}_pitcher_plant.json"),
                       model_item_generated(cid, "pitcher_plant", block_ref(cid, "pitcher_plant")), force)
            safe_write(os.path.join(items_dir, f"{cid}_pitcher_plant.json"),
                       item_item(cid, "pitcher_plant"), force)
            safe_write(os.path.join(loot_dir, f"{cid}_pitcher_plant.json"),
                       loot_pitcher(cid), force)


def gen_seeds(force):
    print("[seeds]")
    imodel_dir = os.path.join(ASSETS, "models", "item")
    items_dir = os.path.join(ASSETS, "items")
    for cid, *_ in COLORS:
        if cid in TORCHFLOWER_COLORS:
            safe_write(os.path.join(imodel_dir, f"{cid}_torchflower_seeds.json"),
                       model_item_generated(cid, "torchflower_seeds"), force)
            safe_write(os.path.join(items_dir, f"{cid}_torchflower_seeds.json"),
                       item_item(cid, "torchflower_seeds"), force)
        if cid in PITCHER_COLORS:
            safe_write(os.path.join(imodel_dir, f"{cid}_pitcher_seeds.json"),
                       model_item_generated(cid, "pitcher_seeds"), force)
            safe_write(os.path.join(items_dir, f"{cid}_pitcher_seeds.json"),
                       item_item(cid, "pitcher_seeds"), force)


# --- lang ----------------------------------------------------------------------


def product_key(cid, product):
    if product in ("dye", "harness", "bundle", "torchflower_seeds", "pitcher_seeds"):
        return f"item.{NS}.{cid}_{product}"
    return f"block.{NS}.{cid}_{product}"


def gen_lang():
    print("[lang]")
    es, en = {}, {}
    for row in COLORS:
        cid, es_name, en_name, *_ = row
        products = ["dye", "wool", "carpet", "terracotta", "glazed_terracotta",
                    "stained_glass", "stained_glass_pane", "concrete", "concrete_powder",
                    "candle", "shulker_box", "bed", "harness", "bundle", "candle_cake"]
        if cid in TORCHFLOWER_COLORS:
            products.append("torchflower")
            products.append("torchflower_seeds")
        if cid in PITCHER_COLORS:
            products.append("pitcher_plant")
            products.append("pitcher_seeds")
        for product in products:
            key = product_key(cid, product)
            es[key] = PREFIX_ES[product] + es_name
            en[key] = en_name + SUFFIX_EN[product]
    write(os.path.join(ASSETS, "lang", "es_es.json"), es)
    write(os.path.join(ASSETS, "lang", "en_us.json"), en)


# --- tags -----------------------------------------------------------------------


def vanilla_colored(suffix):
    return [f"minecraft:{name}_{suffix}" for name in DYE_COLOR_ORDER]


def gen_tags():
    print("[tags]")
    candles = ["minecraft:candle"] + vanilla_colored("candle") \
        + [f"{NS}:{cid}_candle" for cid, *_ in COLORS]
    cakes = ["minecraft:candle_cake"] + vanilla_colored("candle_cake") \
        + [f"{NS}:{cid}_candle_cake" for cid, *_ in COLORS]
    dyes = [f"{NS}:{cid}_dye" for cid, *_ in COLORS]

    write(os.path.join(DATA, "minecraft", "tags", "block", "candles.json"), {"values": candles})
    write(os.path.join(DATA, "minecraft", "tags", "block", "candle_cakes.json"), {"values": cakes})
    write(os.path.join(DATA, "minecraft", "tags", "item", "candles.json"), {"values": candles})
    write(os.path.join(DATA, "minecraft", "tags", "item", "dyes.json"), {"values": dyes})


if __name__ == "__main__":
    force = "--force" in sys.argv
    gen_blockstates(force)
    gen_block_models(force)
    gen_item_models(force)
    gen_items(force)
    gen_recipes(force)
    gen_loot(force)
    gen_flowers(force)
    gen_seeds(force)
    gen_lang()
    gen_tags()
    print("listo")