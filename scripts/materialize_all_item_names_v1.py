from __future__ import annotations

import json
import struct
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds"
OUTPUT = ROOT / "translations/all_item_names_arm9_v1.json"
GUILD_SOURCE = ROOT / "translations/guild_inn_arm9_v1.json"
GUILD_UI_OUTPUT = ROOT / "translations/guild_inn_ui_arm9_v2.json"
TABLE = 0x11E210
COUNT = 218
FREE_START = 0x171E48
FREE_SIZE = 1564

# Concise display names are intentional: the DS list view is narrow, while the
# relocation pool lets names remain complete instead of being byte-truncated.
ENGLISH = [
    "Pumpkin Seeds", "Tomato Seedling", "Banana Tree", "Beehive", "Baby Shark",
    "Pepper Plant", "Clove Plant", "Cinnamon Tree", "Pimento Plant", "Coffee Tree",
    "Tea Plant", "Cacao Seeds", "Tobacco Plant", "Alchemy Book", "Glassmaking Guide",
    "Silkworms", "Loom", "Pearl Oyster", "Herbalist's Bible", "Mangosteen Seeds",
    "Golden Cat", "Lime Drops", "Hermes' Prayer", "Hua Tuo's Tonic",
    "Black Rapier", "Laocoon Sword", "Lohengrin Saber", "Crescent Shotel",
    "Hero's Scimitar", "Golden Cutlass", "Valiant Bec de Corbin", "Azure Talwar",
    "Sweeping Katzbalger", "Loyal Falchion", "Fallen Angel Katar", "White Flamberge",
    "Bloodstained Shamshir", "Judas' Demonblade", "Zhao Yun's Spear", "Orcrist of Atonement",
    "Red-Haired Pirate Sword", "Minotaur Axe", "Namahage Cleaver", "Tlaloc Knife",
    "Vepar Halberd", "Kublai's Greatsword", "Holy Spear of Ares", "Excalibur",
    "Muramasa", "Blue Oak Shield", "Armadillo Hide", "Silver Sallet",
    "Phoenix Bascinet", "Giant Tortoise Shield", "Spirit Dress", "Bladebreaker Gi",
    "Cooling Armor", "Kanem Warrior Shield", "Zealot Cuirass", "Crimson Ringmail",
    "Timur's Chainmail", "Peacock Mail", "Tula Warrior Helm", "Ninja Garb",
    "Amber Brigandine", "Jaguar God's Vest", "Bandit's Mail", "Empress Gown",
    "Noritsune's Armor", "Attila Suit", "Medusa Shield", "Saladin's Silver Armor",
    "Charles Martel Armor", "Minerva Shield", "Magic Leather Gloves", "Tireless Hawser",
    "Milky Way Chart", "Starlight Globe", "Horace's Poems", "Arabian Nights",
    "World Pun Book", "Golden Dividers", "Pocket Watch", "Rocco's Sailing Guide",
    "Heavenly Wristband", "Guiding Staff", "Warrior Ocarina", "Boastful Beak",
    "Travels of Marco Polo", "War Drum", "Poseidon's Roar", "Gallic Wars",
    "Alexander's Campaigns", "Miracle Bullet Charm", "Gunpowder Manual", "Demon-Piercing Arrow",
    "Lion-Fang Saw", "Phidias' Chisel", "Self-Sharpening Plane", "Herophilus' Medicine",
    "Da Vinci Anatomy", "Canon of Medicine", "Hestia's Pot", "Pink Apron",
    "Gauze Mask", "Stylish Boots", "Gregory's Crown", "Illustrated Bible",
    "Ancient Cross", "Art of War", "Gupta Spirit Beast", "Hannibal's Campaigns",
    "Kinokuniya Abacus", "Vezas' Scales", "Eagle Figurehead", "Piglet Figurehead",
    "Orca Figurehead", "White Whale Figurehead", "Dragon Figurehead", "Dolphin Figurehead",
    "Maiden Figurehead", "Demon Figurehead", "King Figurehead", "Madonna Figurehead",
    "Compass", "Sextant", "Aristarchus Telescope", "Frozen Rose", "Rainbow Marbles",
    "Gold Dust", "Bread Millstone", "Huizong Art", "Celestial Turban", "Sappho's Poems",
    "Lamenting Jar", "Venus de Milo", "Stained-Glass Flower", "Silla Gold Crown",
    "Ceramic Earrings", "Jade Jewel", "Shakuntala", "Shosoin Pitcher", "Black Glass Bowl",
    "Embroidered Carpet", "Snow-Silk Robe", "Goryeo Incense Burner", "Supreme Loupe",
    "Rainbow Parrot", "Ullr's Bow", "Cambyses' Crown", "Aksum Gold Seal", "Rigveda",
    "Kediri Talisman", "Qin Palace Lamp", "Crystal Skull", "Thales Paper Map",
    "Cleobulus Cloth Map", "Periander Stone Map", "Solon Leaf Map", "Bias Coin Map",
    "Chiron Bamboo Map", "Pittacus Blade Map", "Stone Circle Map", "Arena Map",
    "Cave Village Map", "Sahara Map", "Royal Mosque Map", "Mughal Empire Map",
    "Ancient Temple Map", "Beijing Map", "Royal Tomb Map", "Golden Temple Map",
    "Ancient City Map", "Aztec Pictorial Map", "Old Parchment", "Patterned Cloth",
    "Upper Stone Tablet", "Evergreen Lotus Leaf", "Ancient Kingdom Coin", "Tang Bamboo Craft",
    "Ceremonial Knife", "Red Dye", "Brass Lamp", "Lower Stone Tablet", "Kushan Platter",
    "Lotion Jar", "Bamboo Assembly Plan", "Sun-Crest Sheath", "Lion's Eye", "Cursed Blade",
    "Serpent Stone Mask", "Star Rose Quartz", "Rutilated Phantom", "Jiganemaru",
    "Ruinous Siren", "Dragon Horn", "Prydwen", "Gajarg",
    "Ancient Map 1", "Ancient Map 2", "Ancient Map 3", "Ancient Map 4",
    "Ancient Map 1", "Ancient Map 2", "Ancient Map 3", "Ancient Map 4",
    "Ancient Map 1", "Ancient Map 2", "Ancient Map 3", "Ancient Map 4",
    "Ancient Map 1", "Ancient Map 2", "Ancient Map 3", "Ancient Map 4",
    "Ancient Map 1", "Ancient Map 2", "Ancient Map 3", "Ancient Map 4",
]


def c_string(data: bytes, offset: int) -> bytes:
    end = data.index(0, offset)
    return data[offset:end]


def main() -> None:
    if len(ENGLISH) != COUNT:
        raise ValueError(f"expected {COUNT} names, got {len(ENGLISH)}")
    arm9 = NdsImage.open(BASE).read_file("/__arm9__.bin")
    records: list[dict[str, object]] = []
    pool = bytearray()
    item_rows: list[tuple[int, int, int, str, bytes]] = []
    slots: dict[int, int] = {}
    for index, english in enumerate(ENGLISH):
        pointer_offset = TABLE + index * 0x18
        source_offset = struct.unpack_from("<I", arm9, pointer_offset)[0] - 0x02000000
        source = c_string(arm9, source_offset)
        source.decode("cp932")
        slots[source_offset] = len(source) + 1
        item_rows.append((index, pointer_offset, source_offset, english, english.encode("ascii") + b"\0"))

    # Repack the original item-name allocations globally. This is safe because
    # every runtime item pointer is redirected below, and it saves enough space
    # to keep the relocation pool inside the verified trailing zero run.
    available = sorted((capacity, offset) for offset, capacity in slots.items())
    targets: dict[str, int] = {}
    payloads: dict[int, bytes] = {}
    for english, encoded in sorted({(row[3], row[4]) for row in item_rows}, key=lambda row: len(row[1]), reverse=True):
        choices = [(capacity, offset, pos) for pos, (capacity, offset) in enumerate(available) if capacity >= len(encoded)]
        if choices:
            capacity, offset, pos = min(choices)
            available.pop(pos)
            targets[english] = offset
            payloads[offset] = encoded.ljust(capacity, b"\0")
        else:
            targets[english] = FREE_START + len(pool)
            pool.extend(encoded)

    for offset, replacement in sorted(payloads.items()):
        records.append({
            "id": f"DK4_ITEM_NAME_STORAGE_{offset:06X}",
            "offset": offset,
            "source_hex": arm9[offset:offset + len(replacement)].hex().upper(),
            "replacement_hex": replacement.hex().upper(),
            "context": "Repacked global English item-name storage.",
        })

    for index, pointer_offset, _source_offset, english, _encoded in item_rows:
        target_offset = targets[english]
        records.append({
            "id": f"DK4_ITEM_POINTER_{index:03d}",
            "offset": pointer_offset,
            "source_hex": arm9[pointer_offset:pointer_offset + 4].hex().upper(),
            "replacement_hex": struct.pack("<I", 0x02000000 + target_offset).hex().upper(),
            "english": english,
            "context": f"Redirect global item catalogue entry {index} to its complete English name.",
        })

    if len(pool) > FREE_SIZE:
        raise ValueError(f"English relocation pool needs {len(pool)} bytes; only {FREE_SIZE} are verified free")
    records.append({
        "id": "DK4_ITEM_NAME_RELOCATION_POOL",
        "offset": FREE_START,
        "source_hex": arm9[FREE_START:FREE_START + FREE_SIZE].hex().upper(),
        "replacement_hex": bytes(pool).ljust(FREE_SIZE, b"\0").hex().upper(),
        "context": "Complete English names that exceed their original fixed Shift-JIS allocations.",
        "notes": f"Uses {len(pool)} of {FREE_SIZE} verified zero bytes.",
    })

    OUTPUT.write_text(json.dumps({
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": "/__arm9__.bin",
        "source_file_sha256": sha256(arm9).hexdigest(),
        "target_locale": "en-US",
        "scope": "All 218 runtime item names, with complete-name pointer relocation",
        "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    guild = json.loads(GUILD_SOURCE.read_text(encoding="utf-8"))
    guild["scope"] = "Shared Guild and Inn menus and role nameplates; item names are supplied by the global catalogue batch"
    guild["records"] = [record for record in guild["records"] if record["id"] != "DK4_ITEM_RAINBOW_MARBLES"]
    GUILD_UI_OUTPUT.write_text(json.dumps(guild, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} patches; relocation pool {len(pool)}/{FREE_SIZE} bytes")


if __name__ == "__main__":
    main()
