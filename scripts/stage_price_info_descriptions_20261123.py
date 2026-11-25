"""Review Price Info prose and compile it within the original message allocations."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_recruitment_shortfall_20261123 as parent
from scripts import stage_price_info_wraps_20261115 as price
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


ROOT = Path(".codex-release-work/price_info_descriptions_20261123")
ROM = ROOT / "Price_Info_Descriptions_STAGED.nds"
STORED = ROOT / "stored_proof.json"
MANUSCRIPT = Path("translations/editorial_checkpoints/shared_display_20261123/price_info_descriptions_review_20261123.json")
PRIOR = Path("releases/all_routes_editorial_20261111_trade_good_descriptions_candidate/verification/registered_review.json")

REVIEWS = {
    143: ("Beef", "Beef can be boiled or grilled. Some cultures don't eat beef at all.",
          ("Some cultures", "at all"), "Beef is boiled or grilled. Some cultures abstain from it.",
          "Keep both preparations and the cultural distinction. Give the second sentence its own line."),
    146: ("Tomato", None, (), "A New World nightshade, with an alternate name, eaten raw or cooked.",
          "The existing entry gives the region, family, alternate name and both preparations in straightforward prose."),
    166: ("Chili", "Dried chilies from the New World, also known as red pepper. Very hot.",
          ("the New World", "red pepper"), "Dried New World chilies, also called red pepper, with a strong bite.",
          "Keep origin and alternate name. The short heat note suits a commodity entry and stays with the preceding thought."),
    203: ("Amber", "Resin fossilized underground. Yellowish, clear to translucent. Used in brooches and other jewelry.",
          ("Resin fossilized underground.", "Yellowish, clear to translucent.", "Used in brooches and other jewelry."),
          "Ancient resin fossilized underground, yellowish and clear or translucent, used for brooches and other ornaments.",
          "Keep the formation, appearance and use in complete rows, with brooches as the original example."),
    208: ("Sapphires", "Clear blue gems long held sacred. Christian clergy wore them in rings. Only diamonds are harder or rarer.",
          ("long held sacred", "Christian clergy", "in rings", "harder or rarer"),
          "Clear blue gems long regarded as sacred, worn in clergy rings, second to diamonds in hardness and rarity.",
          "Keep the historical practice separate from the game’s comparison of both properties."),
    216: ("Cordyceps", "Parasitic fungus on insects. A prized tonic.", ("on insects", "A prized tonic."),
          "A fungus that parasitizes insects and is prized as a tonic.",
          "Name the parasitic relationship explicitly. The preceding English could suggest people grow it deliberately on insects."),
    225: ("Blades", None, ("Blades and swords.", "They sell well during wars."),
          "Blades and swords that sell well during wars.",
          "Keep the established description and give the wartime demand statement its own complete row."),
    226: ("Armor", None, ("Armor and helmets.", "They sell well during wars."),
          "Armor and helmets that sell well during wars.",
          "Keep the two products and give the wartime demand statement its own complete row."),
    227: ("Iron Ore", "Ore containing iron. Used to make steel, stainless steel, and more.",
          ("Ore containing iron.", "stainless steel"),
          "Iron-bearing rock processed into steel, stainless steel and other materials.",
          "Keep the raw and processed goods distinct, and retain both named examples as part of a broader list."),
    233: ("Leather", "Tanned hide with the hair removed. Strong, absorbent and breathable. Used for handbags, belts, and shoes.",
          ("Tanned hide with the hair removed.", "Strong, absorbent and breathable.", "Used for handbags, belts, and shoes."),
          "Hair is removed and the hide is tanned. It is strong, absorbent and breathable, and used for handbags, belts and shoes.",
          "Keep preparation, the three material qualities and the three source examples in separate rows."),
    234: ("Wax", "Pale yellow beeswax from honeycombs. Used for candles and other goods.",
          ("from honeycombs", "candles and other goods"), "Pale yellow beeswax from honeycombs, used for candles and similar products.",
          "State the bee source and color together. Keep the entire example sentence together."),
    236: ("Guano", "On tropical shores and islands, seabird droppings pile up. Used as a fertilizer with nitrogen and phosphate.",
          ("On tropical shores and islands,", "seabird droppings pile up.", "nitrogen and phosphate"),
          "Seabird droppings accumulate on tropical shores and islands and contain nitrogen and phosphate. They serve as fertilizer.",
          "Keep the location together and retain both nutrients and the original use."),
    242: ("Salmon", None, (), "King salmon are the largest and longest-lived, spawning throughout the year and spending a long period returning upriver.",
          "Keep the species and the in-game explanation intact across four full rows."),
    243: ("Whale Meat", None, (), "Whale meat looks like horse meat and has long been prized in Japan.",
          "The straightforward comparison and historical use keep the original cultural context."),
    244: ("Black Wool", None, (), "Wool sheared from black sheep.",
          "The single sentence defines the good without adding a quality or processing claim."),
    245: ("Fire and Ice Rubies", "Rubies from Iceland. Ruby is the red variety of corundum.",
          ("Rubies from Iceland.", "Ruby is the red variety of corundum."),
          "Rubies from Iceland in the game. Ruby is the red form of corundum.",
          "Keep the game's stated origin and the mineral distinction in two complete sentences."),
    246: ("Desert Diamonds", None, (), "Diamonds attributed to the world's largest mine in the northern Kalahari.",
          "The wording preserves the in-game claim as a description, with both the region and superlative intact."),
    247: ("Mead", None, (), "Fermented honey enjoyed by Celts and Vikings for nourishment and warmth.",
          "The existing wording presents both cultures and both reasons without suggesting that only those peoples drank it."),
}


def main():
    release = read(parent.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"]
    earlier = {137 + row["commodity_index"]: row for row in read(PRIOR)["records"]}
    producer = checked_text(getsource(price.main), {
        "assert set(REVIEWS) == {i for i in range(137, 261) if old[i].text.count(b'\\n') >= 4}":
            "assert set(REVIEWS) <= earlier.keys()",
        "        body = compile_body(prior.text, draft, phrases, env['plan'])":
            """        previous = earlier[n]
        assert previous['source_reference'] == reference(source) and previous['source_hex'] == source.text.hex()
        assert previous['commodity_name'] == name and all(previous['review'].values())
        body = compile_body(prior.text, draft, phrases, env['plan'])""",
        "    image.save(ROM)": """    assert len(slots) == 12 and sum(len(row['pages']) for row in rows) == 18
    image.save(ROM)""",
    })
    scope = vars(price) | dict(ROOT=ROOT, ROM=ROM, STORED=STORED, MANUSCRIPT=MANUSCRIPT, earlier=earlier,
        REVIEWS=REVIEWS, parent=SimpleNamespace(RELEASE=parent.RELEASE, ROM=parent.ROM))
    scope["native_proof"] = FunctionType(price.native_proof.__code__, scope)
    exec(compile(producer, __file__ + "::price-info-current", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
