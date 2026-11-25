"""Verify ordinary Tavern and Square dialogue and qualify Myrine's item rumor."""

from argparse import ArgumentParser
from collections import Counter
from types import FunctionType

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import compare_london_relic_wraps_20261123 as inventory
from scripts import observe_athens_valencia_town_20261123 as run
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.probe_tavern_conversations_v764 import format_case
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, digest, read, reference, sha256, write
from scripts.stage_tavern_nearby_town_wrap_20261123 import town


current = run.current
ARM, COMMON = current.ARM, current.COMMON
OUT = panels.OUT.with_name("athens_valencia_town_20261123.json")
PREFLIGHT = OUT.with_name("athens_item_rumor_preflight_20261123.json")
PREVIEWS = OUT.parent / "athens_item_rumor_previews_20261124"
KEY = 828
ITEM = "Lamenting Jar"
DRAFTS = (
    "%s? Ever heard of it? It's out there somewhere. I hear it's beautiful.",
    "%s? Ever heard of it? It's out there somewhere. Apparently, it's beautiful.",
    "%s? Know it? It's out there somewhere. Apparently, it's beautiful.",
    "%s? Do you know it? It's out there somewhere. Apparently, it's beautiful.",
)
OBSERVED = {
    0: ("Charles Rochefort", (), "Charles's report alerts Hodram to the gathering while leaving its cause uncertain."),
    51: ("Barkeep", (), "A brisk welcome leads into the invitation to order."),
    53: ("Barkeep", (), "Keep the exact five-coin price before the barkeep's first rumor."),
    55: ("Barkeep", ("Myrine",), "The barkeep calls the Athens hostess by name and tells her a customer is waiting."),
    57: ("Myrine", (), "The hostess's brief welcome addresses the customer before she offers another drink."),
    59: ("Myrine", (), "The friendly second-drink offer leads directly to Yes or No."),
    61: ("Barkeep", (), "The second drink costs ten coins, and the line confirms the price before Myrine's rumor."),
    653: ("Shopkeeper", ("Armor",), "The shopkeeper reports current brisk sales for the item held in the original slot."),
    655: ("Shopkeeper", ("Armor",), "The excited suggestion proposes selling the item at a profit."),
    656: ("Shopkeeper", (), "The short reply explains what the Square shop sells at retail."),
    657: ("Shopkeeper", (), "Keep the question and tag together before the referral to the Market for bulk trade."),
    714: ("Shopkeeper", (), "The speaker keeps Valdes's role and the navy's reported title. The full Invincible Armada phrase stays on one line."),
    821: ("Barkeep", (), "Real pull keeps the rough tone and distinguishes influence from fame. Each person, home city and occupation remains the game's own substitution."),
    823: ("Barkeep", ("Crete",), "The barkeep asks about a nearby town and gives the place name as part of the question."),
    KEY: ("Myrine", (ITEM,), "The bare item title sounds awkward after 'heard of' with Lamenting Jar. A question about the item's name can keep the runtime title intact."),
}
INFLUENCE_ARGS = {
    4760: ("Hayreddin", "Alexandria", "pirate"),
    5540: ("Pasha", "Istanbul", "soldier"),
    6320: ("Centurione", "Genoa", "trader"),
}


def context():
    release = read(current.RELEASE)
    assert digest(current.ROM) == release["candidate_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    ctx = inventory.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    cpu, call, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    raster, _, _ = town.font_tools(ctx.image)
    return release, ctx, cpu, call, raster, ctx.image.read_file("/GRP/KANJI.FNT")


def render(cpu, raster, arm, kanji, key, stored, args):
    assert stored.count(b"%s") == len(args)
    if len(args) > 2 or key == KEY:
        assert stored.startswith(b" ")
        layout = format_case(cpu, dict(message_id=key, english=stored[1:].decode("ascii")), [a.encode("ascii") for a in args])
        raw = bytes.fromhex(layout["formatted_hex"])
        assert "four_row_width_bound" not in layout["findings"]
    else:
        raw, lines = town.native_layout(cpu, stored, key, args)
        layout = dict(formatted_hex=raw.hex(), lines=lines)
    pixels, glyphs = town.render_portrait(raster, arm, kanji, raw)
    assert [g["code"] for g in glyphs] == town.glyph_codes(raw) and len(pixels) == 228 * 64
    return layout, bytes(pixels)


def gameplay():
    release, ctx, cpu, _, raster, kanji = context()
    clean = NdsImage.open(CLEAN)
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    installed = common_rows(ctx.common, ctx.arm)
    font = GameAsciiFont.from_arm9(ctx.arm)
    capture = FunctionType(panels.capture.__code__, vars(panels) | {"observed": run})
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    cases, decisions = {}, {}
    for city in run.HISTORIES:
        frames, calls, evidence = capture(city, release)
        counts, figures = Counter(), []
        for a, b in zip(calls[::2], calls[1::2], strict=True):
            assert a["PC"] == 0x0205528C and b == a | {"PC": 0x020534F4}
            key = a["message_ID"]
            frame = min(n for n in frames if n > a["frame"])
            assert frame - a["frame"] <= 360
            speaker, args, reason = OBSERVED[key]
            if key == 821:
                args = INFLUENCE_ARGS[frame]
            jp, en = source[key], installed[key]
            assert jp.text.count(b"%s") == len(args)
            screen = panels.picture(frames[frame])
            shown, plane = render(cpu, raster, ctx.arm, kanji, key, en.text, args)
            assert panels.mask_check(plane, 228, screen), (city, frame, key, shown["lines"])
            name = panels.nameplate(font, speaker, screen)
            figures.append((f"{frame} / {speaker} / COMMON {key}", screen))
            counts[key] += 1
            if key not in decisions:
                gates = dict.fromkeys(GATES, True)
                if key == KEY:
                    gates["formatting"] = False
                decisions[key] = dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON,
                    speaker=speaker, clean_Japanese=jp.text.decode("cp932"), english=en.text.decode("ascii").strip(),
                    source_reference=panels.text_reference(jp), installed_reference=panels.text_reference(en),
                    source_hex=jp.text.hex(), installed_hex=en.text.hex(), localization_note=reason, review=gates,
                    decision="revision proposed" if key == KEY else "retention", holds=[])
            decisions[key]["holds"].append(dict(city=city, capture=frames[frame], requests=[a, b], arguments=args,
                lines=shown["lines"], nameplate=name, complete_body_plane_sha256=sha256(plane).hexdigest()))
        assert frames[9860] and counts
        end = panels.picture(frames[9860])
        panels.find_mask(font, city.title(), end, (50, 11, 114, 35))
        cases[city] = dict(counts=dict(counts), final_Square_shop_selector=frames[9860], evidence=evidence,
            sheets=sheets(f"{city}_ordinary_tavern_and_square", figures, (0, 272, 256, 380)))
    assert len(decisions) == 15 and sum(len(r["holds"]) for r in decisions.values()) == 24
    assert [row["capture"]["frame"] for row in decisions[KEY]["holds"]] == [6320]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_existing_saves=True,
        records=list(decisions.values()), towns=cases, new_contextual_credit=0, build_changed=False,
        unvisited=["Other Tavern rumor choices or gifts", "Other regional shop replies and fortune branches"]))
    print("Verified 24 full dialogue and nameplate holds across 15 shared messages in two towns.")


def preflight():
    release, ctx, cpu, call, raster, kanji = context()
    observed = read(OUT)
    assert observed["candidate_sha256"] == release["candidate_sha256"]
    row, = [r for r in observed["records"] if r["message_ID"] == KEY]
    names, _ = inventory.providers(cpu, call)
    assert len(names) == 218 and ITEM in {r["name"] for r in names}
    original = bytes.fromhex(row["installed_hex"])
    templates = (original, *(b" " + text.encode("ascii") for text in DRAFTS))
    assert all(len(t) <= len(original) and t.count(b"%s") == 1 for t in templates)
    drafts = []
    for template in templates:
        results, name_splits, short_end, phrase_splits, observed_splits = [], 0, 0, 0, 0
        stored = template.ljust(len(original), b" ")
        for item in names:
            name = item["name"]
            expanded = format_case(cpu, dict(message_id=KEY, english=stored[1:].decode("ascii")), [name.encode("ascii")])
            lines = expanded["lines"]
            assert "four_row_width_bound" not in expanded["findings"]
            assert 1 <= len(lines) <= 4 and all(0 < len(line) <= 35 for line in lines)
            name_splits += not any(name in line for line in lines)
            short_end += len(lines[-1]) <= 8
            folded = [line.lower() for line in lines]
            split = sum(phrase in " ".join(folded) and not any(phrase in line for line in folded) for phrase in
                ("ever heard of it?", "do you know it?", "know it?", "out there somewhere", "i hear it's", "they say",
                 "apparently, it's beautiful."))
            phrase_splits += split
            if name in (ITEM, "Rainbow Marbles"):
                observed_splits += split
            results.append(item | dict(layout=expanded))
        drafts.append(dict(text=stored.decode("ascii").strip(), stored_hex=stored.hex(),
            split_item_names=name_splits, short_final_rows=short_end, phrase_splits=phrase_splits,
            observed_item_phrase_splits=observed_splits, layouts=results))
        print(stored.decode("ascii").strip(), name_splits, observed_splits, phrase_splits, short_end, flush=True)
    winner = min(drafts[1:], key=lambda r: (r["split_item_names"], r["observed_item_phrase_splits"],
                                             r["short_final_rows"], r["phrase_splits"]))
    assert winner["split_item_names"] < drafts[0]["split_item_names"]
    assert winner["short_final_rows"] <= drafts[0]["short_final_rows"]
    longest = max(names, key=lambda row: len(row["name"]))["name"]
    samples = (ITEM, "Rainbow Marbles", longest)
    pages = []
    for name in samples:
        for label, draft in (("previous", drafts[0]), ("revised", winner)):
            layout, pixels = render(cpu, raster, ctx.arm, kanji, KEY, bytes.fromhex(draft["stored_hex"]), (name,))
            pages.append((f"{KEY} / {name} / {label}", pixels))
    PREVIEWS.mkdir(exist_ok=True)
    sheets = town.portrait_sheets(PREVIEWS, pages)
    assert drafts[0]["layouts"][next(i for i, r in enumerate(names) if r["name"] == ITEM)]["layout"]["lines"] == row["holds"][0]["lines"]
    write(PREFLIGHT, dict(candidate_sha256=release["candidate_sha256"], recorded_gameplay=reference(OUT),
        source_reference=row["source_reference"], drafts=drafts, selected_template=winner["text"],
        checked_names=len(names), sheets=sheets, samples=samples, ROM_changed=False))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("gameplay", "preflight"))
    globals()[cli.parse_args().action]()
