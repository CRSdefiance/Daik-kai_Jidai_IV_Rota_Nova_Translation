"""Compile and verify five connected Market and Source Item articles."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.dialogue import reviewed_help_pages_v16 as compiler
from dk4tool.dialogue.help_source_links import readable_source, source_links
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_early_HELP23_native_pages as renderer
from scripts import register_square_shop_followup_20261119 as parent
from scripts.source_locked_derivation_v5118 import checked_text

base = parent.base
CLEAN = base.CLEAN
HELP = "/COMMON/HELP.DK4"
ARM = "/__arm9__.bin"
ROOT = Path("work/help_market_terms_20261119_v1")
ROM = ROOT / "HELP_Market_Staged.nds"
PROOF = ROOT / "native_help_pages.json"
PLAN = ROOT / "plan.json"
ARTICLES = {
    119: ("Purser's Office",
          "This is where the fleet keeps its accounts. Assign an officer with Finance 100 or higher to serve as Purser. "
          "A Purser can sometimes get you a discount at the Market or buy up all available stock at twice the price. "
          "You cannot sell goods at twice the price.",
          "Keeps the role, skill threshold, conditional discount and buyout, and the restriction on selling at double price."),
    148: ("Growth",
          "Growth measures how developed a city is. It rises when you make [[23|commercial investments]] at the Market. "
          "Higher Growth may add to the city's specialties. It also affects how many sailors you can recruit and which cannon you can equip.",
          "Keeps the commercial investment link and the effects on specialties, recruitment and cannon."),
    152: ("Specialties",
          "Specialties are the trade goods sold in a city. A city may offer more as it develops or when someone brings in "
          "a Source Item. Stock is replenished each [[24|arrival month]]. See [[194|Source Item]].",
          "Distinguishes finished specialties from Source Items and preserves the stock replenishment rule and both links."),
    191: ("Trade Goods",
          "Trade goods are bought and sold at the Market. The goods a city sells are its specialties, and every city has its own selection. "
          "Prices vary from city to city and rise or fall with market conditions. Base prices vary by cultural region. "
          "See [[192|Types]] and [[193|Quality Grades]].",
          "Keeps the distinction among city specialties, local price fluctuations and regional base prices."),
    194: ("Source Item",
          "A Source Item can give a city a new specialty. Bring one to the Market in a suitable city with fewer than five specialties. "
          "More than one city can be a good fit for the same item. Choose a city that suits your plans, such as one where your faction has "
          "a high [[150|market share]].",
          "Matches the active item category. Keeps city suitability, the five-specialty cap, the possibility of several suitable cities and the advice about market share."),
}
RETAIN = {
    21: "Already names Market and Source Item consistently and explains the offer and handover. Keeps its original navigation.",
    23: "Already explains investment units, cost and Growth and share conditions with the original cross-references.",
    110: "The Workrooms directory already names the Purser's Office correctly and preserves the other room links.",
}


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    caption = base.load(parent.REVIEW)["help_facility_term_followup"]
    clean, canonical, image = map(base.NdsImage.open, (CLEAN, Path("out/raphael_natural_v2_accepted_base.nds"), parent.ROM))
    resources = {key: rom.read_file(HELP) for key, rom in (("clean", clean), ("canonical", canonical), ("current", image))}
    blocks = {key: IlnkContainer.parse(raw).blocks for key, raw in resources.items()}
    assert caption["clean_archive_sha256"] == sha(resources["clean"])
    assert caption["current_archive_sha256"] == sha(resources["current"])
    assert blocks["current"][21].startswith(b"Market\n") and b"Source Item" in blocks["current"][21]
    for lead in caption["followup"]:
        topic = lead["topic"]
        assert sha(blocks["clean"][topic]) == lead["source_block_sha256"]
        assert sha(blocks["current"][topic]) == lead["current_block_sha256"]
    coverage = {(r["file_path"], r["id"]) for r in base.load(base.LEDGER)[base.CONTEXT]["integrated_record_keys"]}
    records = []
    for topic in sorted(ARTICLES.keys() | RETAIN.keys()):
        ident = f"HELP_TOPIC_{topic}"
        assert (HELP, ident) in coverage
        original = blocks["clean"][topic]
        current = blocks["current"][topic]
        links = [link["topic_id"] for link in source_links(original)]
        assert links == [link["topic_id"] for link in source_links(current)]
        row = dict(id=ident, topic_id=topic, file_path=HELP, original_link_IDs=links,
                   source_reference=dict(archive_sha256=sha(resources["clean"]), block=topic, block_sha256=sha(original)),
                   current_reference=dict(archive_sha256=sha(resources["current"]), block=topic, block_sha256=sha(current)),
                   source_Japanese=readable_source(original), previous_English=readable_source(current),
                   review={gate: True for gate in ("source", "context", "localization", "naturalness")} | {"formatting": False},
                   **{f"{key}_source_hex": data[topic].hex() for key, data in blocks.items()})
        if topic in ARTICLES:
            title, english, note = ARTICLES[topic]
            row.update(heading=title, english=english, localization_note=note, decision="revision")
        else:
            row.update(localization_note=RETAIN[topic], decision="retention", review=row["review"] | {"formatting": True})
        records.append(row)

    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", file_path=HELP,
                      records=[r for r in records if r["decision"] == "revision"],
                      **{f"source_{key}_HELP_sha256": sha(raw) for key, raw in resources.items()})
    source = checked_text(compiler.SOURCE, {
        "topics!=(set(range(133,202))-{181,184})": "topics!={119,148,152,191,194}",
        "Exact remaining67 Help articles": "Exact Market and Source Item follow-up articles",
        "148:['Trade House'],152:['Products'],189:['Coerce'],191:['Trade House'],194:['Products','Trade House','five specialties']":
            "119:['Finance 100','Market','twice the price'],148:['Market'],152:['Source Item'],189:['Coerce'],191:['Market'],194:['Market','five specialties']",
        "title!='Products (Raw Materials)'": "title!='Source Item'",
    })
    scope = compiler.plan_articles.__globals__.copy()
    exec(compile(source, __file__ + "::market_terms_help_pages", "exec"), scope)
    target, plan = scope["plan_articles"](manuscript, *resources.values(), require_formatting=False)
    assert len(plan["pages"]) == len(ARTICLES) and plan["target_topic_count"] == 217
    assert plan["owned_topic_ids"] == list(ARTICLES) and not plan["compiler_generated_navigation_pairs"]
    assert b"Trade House" not in target
    candidate = base.NdsImage.open(parent.ROM)
    candidate.replace_file(HELP, target)
    result = bytes(candidate.rom.save())
    candidate.replace_file(HELP, resources["current"])
    assert bytes(candidate.rom.save()) == parent.ROM.read_bytes()

    ROOT.mkdir(parents=True)
    ROM.write_bytes(result)
    (ROOT / "HELP.DK4").write_bytes(target)
    base.save(ROOT / "manuscript.json", manuscript)
    base.save(PLAN, plan)
    base.save(ROOT / "qualification.json", dict(research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM)))

    env = renderer.original.verify.__globals__.copy()
    exec(compile(renderer.ADAPTER, __file__ + "::original_help_parser", "exec"), env)
    arm = image.read_file(ARM)
    images = []
    for page in plan["pages"]:
        topic = page["topic_id"]
        record = next(row for row in records if row["topic_id"] == topic)
        receipt, picture = env["verify"](arm, page)
        path = ROOT / f"topic_{topic}.png"
        picture.save(path)
        images.append((topic, picture))
        record.update(native_display=receipt, registered_hex=page["encoded_hex"], visible_lines=page["visible_lines"],
                      preview=str(path), preview_sha256=base.digest(path))

    sheets = []
    label_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
    for first in range(0, len(images), 4):
        group = images[first:first + 4]
        sheet = Image.new("RGB", (1512, 800 if len(group) > 2 else 400), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (topic, picture) in enumerate(group):
            x, y = i % 2 * 756, i // 2 * 400
            draw.text((x + 6, y + 5), f"Help {topic}", font=label_font, fill="white")
            sheet.paste(picture.resize((756, 360), Image.Resampling.NEAREST), (x, y + 30))
        path = ROOT / f"sheet_{first // 4 + 1}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    base.save(PROOF, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", records=records,
                         candidate_sha256=base.digest(ROM), previous_sha256=base.digest(parent.ROM),
                         clean_input_sha256=base.digest(CLEAN), target_HELP_sha256=sha(target),
                         complete_parent_inverse=True, sheets=sheets,
                         evidence={str(p): base.digest(p) for p in (PLAN, parent.REVIEW, Path(__file__))}))
    for page in plan["pages"]:
        print(page["topic_id"], "\n".join(page["visible_lines"]), sep="\n")


if __name__ == "__main__":
    main()
