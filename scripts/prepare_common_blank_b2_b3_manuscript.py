"""Restore complete native commodity groups containing missing B2/B3 messages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    164: ("Dried saffron stigmas, used as a spice to flavor and color seafood dishes such as bouillabaisse.", "Dried stigmas from saffron stamens; a spice used to flavor and color seafood dishes, including bouillabaisse."),
    165: ("Fermented vanilla fruit from the New World. Its sweet, distinctive aroma is extracted with alcohol for use as a flavoring.", "Fermented vanilla fruit, native to the New World, has a distinctive sweet aroma; alcohol extracts are used for flavoring."),
    167: ("Roasted, ground coffee beans are boiled or filtered to make a drink with a strong aroma and bitter taste.", "Seeds of the coffee tree are roasted and ground, then boiled or filtered to make a drink; their aroma and bitterness are strong."),
    168: ("Tea from young buds and leaves: unfermented green tea, partly fermented oolong or fermented black tea, depending on how it's made.", "Tea is a beverage made from young tea-tree buds and leaves. Processing yields unfermented green tea, partly fermented oolong or fermented black tea."),
    172: ("Spirits distilled from fruit. Cognac, a famous grape brandy, is distilled from wine. About 40 percent alcohol.", "Fruit-based distilled spirits as a category; cognac is a famous grape brandy distilled from wine, with alcohol content around 40 percent."),
    173: ("A sweet-smelling spirit distilled from sugarcane juice or molasses. Contains 40 to 80 percent alcohol.", "A distilled spirit characterized by a sweet aroma, made from sugarcane juice or molasses, with alcohol content of 40 to 80 percent."),
    184: ("Thread made by combining fibers unwound from silkworm cocoons. Stiff and dull to the touch, it is the raw yarn for silk fabrics.", "Several fibers unwound from silkworm cocoons are combined into thread. It feels stiff, lacks luster and is used as raw yarn for silk textiles."),
    185: ("Strong stem fibers from hemp, flax or Manila hemp, used for clothes, ropes and mats. They absorb and release moisture quickly.", "Fibers from stems of hemp, flax and Manila hemp are used for clothing, ropes and mats. Tensile strength is high, and moisture absorption and release are rapid."),
    206: ("Gems formed inside pearl oysters and other shellfish. White, pink-silver or black; perfectly round pink pearls are the finest.", "Pearls form inside akoya oysters and similar shellfish. Colors include white, pink-silver and black; perfectly round pinkish pearls are best."),
    207: ("Clear gems prized for their brilliance and high refraction. Graded by carat, cut, color and clarity; bluish-white ones rank highest.", "Colorless transparent gems with a high refractive index and strong sparkle. Rated by carat, cut, color and clarity; bluish-white stones are considered highest grade."),
    211: ("A translucent indigo gem with a glassy luster, also called azure stone or ruri in Japan. Prized in ancient Egypt before the Common Era.", "An indigo, translucent gemstone with vitreous luster; also called blue-gold stone and ruri in Japanese. Valued in Egypt before the Common Era."),
    212: ("Powdered rhinoceros horn tips, used to reduce fevers and as a disinfectant.", "Powder made from the tip of a rhinoceros's nasal horn, used for fever reduction and disinfection according to the source."),
    225: ("Blades and swords. They sell well during wars.", "Swords and blades sell well in wartime."),
    226: ("Armor and helmets. They sell well during wars.", "Armor and helmets sell well in wartime."),
    227: ("Rock containing iron, processed into steel, stainless steel and other materials.", "Rock containing the raw material for iron, processed into stainless steel, steel and similar products."),
    228: ("Rock containing copper, a good conductor of heat and electricity. Used to make coins, pipes and rods.", "Rock containing copper; copper has high thermal and electrical conductivity and is made into currency, pipes, rods and similar products."),
    229: ("Rock containing tin, a white, easily worked metal with a low melting point. Used to make tinplate and solder.", "Rock containing tin; tin is white, has a low melting point and is ductile. Processed into tinplate, solder and similar products."),
    234: ("Pale yellow beeswax from honeycombs, used to make candles and other products.", "Wax making up honeybee nests, also called beeswax. Pale yellow and used for candles and similar products."),
    235: ("A raw material for gum, made by boiling down the sap of the sapodilla tree.", "Raw material for gum: sap of the sapodilla tree concentrated by boiling."),
    239: ("Canary-yellow quartz mined in Rio de Janeiro, a gemstone paradise with many quartz mines.", "Canary-colored quartz mined in Rio de Janeiro, called a gemstone paradise and home to many quartz mines."),
    240: ("Rare intestinal secretions from male sperm whales, found in only 1-2 per 100 whales. Mixed into perfume, it enhances scents and makes them last.", "Secretions from male sperm whales' intestines, found in only one or two per hundred whales. Mixed with fragrance, enhances the aroma and prolongs it."),
}


REVISIONS = {
    164: "Dried saffron stigmas. This spice adds flavor and color to seafood dishes such as bouillabaisse.",
    165: "New World vanilla fruit, fermented for its sweet, distinct aroma. Extracts made with alcohol are used as flavoring.",
    167: "Roasted, ground coffee beans are boiled or filtered into a fragrant, strongly bitter drink.",
    184: "Thread made by combining fibers unwound from silkworm cocoons. It feels stiff, has no luster and is used to weave silk fabrics.",
    207: "Colorless, clear gems with high refraction and brilliance. Graded by carat, cut, color and clarity. Bluish-white stones rank best.",
    211: "A glassy, translucent indigo gem, also called blue-gold stone or ruri in Japan. Prized in Egypt before the Common Era.",
    212: "Powder from rhinoceros horn tips. Used to reduce fevers and disinfect.",
    229: "Rock containing tin, a ductile white metal with a low melting point. Used for tinplate and solder.",
    235: "Boiled-down sap of the sapodilla tree. Used to make gum.",
    239: "Canary-yellow quartz from Rio de Janeiro, home to many quartz mines and known as a gemstone paradise.",
    240: "Male sperm whales' intestinal secretions, found in only 1-2 per 100 whales. Enhances perfume scents and makes them last.",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v105_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] in {2, 3}}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B2/B3 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Commodity description narrator",
            "context": f"Independent commodity description {message_id}, COMMON B{source.block} R{source.record_index}. Packed neighbors are separate descriptions.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source prose preserves material properties, origins, preparation, uses, grades, uncertainty and numerical ranges. Historical source claims are localized faithfully. Commodity names supplied by the surrounding UI are not invented in the prose. Reserved capital I/F use the existing narrow set of full-width Latin glyphs. Complete native repack and exact-font review remain required.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b2_b3_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed commodity descriptions; formatting pending")


if __name__ == "__main__":
    main()
