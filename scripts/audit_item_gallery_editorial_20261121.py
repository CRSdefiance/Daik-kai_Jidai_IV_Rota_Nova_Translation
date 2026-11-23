"""Bind current item cards to reviewed Japanese and verify representative Gallery pages."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_KANJI_FONT_SHA256, GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE
from scripts import register_gallery_historic_sites_menu_20261121 as current
from scripts.review_source_item_cards_and_coin_v1 import GETTER, LOOKUP, PAINT, PAINTER, branch_target
from scripts.verify_all_items_gallery_v535 import glyph_pixels, tooltip
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_characters_gallery_v525 import report
from scripts.verify_item_interface_research import expected_draws


base = current.base
stage = current.stage
ROOT = Path("work/item_gallery_editorial_20261121")
DONOR = Path("work/analysis/item_gallery_v535")
ITEMS = Path("work/analysis/item_interface_plan.json")
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUTPUT = BOOK / "item_gallery_editorial_20261121_v1.json"
FIRST, COUNT = 2815, 218
SOURCE_116 = Path("translations/shachihoko_item116_contextual_final_review_v1.json")
REVIEW_FAMILIES = (
    "source_item_cards_and_coin", "utility_weapon_item_cards", "armor_item_cards",
    "crew_equipment_item_cards", "figurehead_navigation_gift_cards", "relic_map_item_cards",
    "promotional_item_cards",
)
WRAP_DRAFTS = {
    3: (("Honeybees build this hive with care.", "It is packed with nourishing nectar",
         "they gather from flowers."), "Keep the origin of the nectar with the action of gathering it."),
    18: (("An Eastern medical text of unknown authorship.", "It describes how to make medicines",
          "from herbs and bark."), "Keep both ingredients in one phrase."),
    44: (("A fine yet eerie axe", "with a black handle and twisted tip."), "Keep both physical details together."),
    108: (("Made the year Christ died, this miraculous", "cross resurfaced after",
           "over a thousand years underground."), "Keep the full measure of time together."),
    120: (("This figurehead of an innocent maiden", "brings people comfort and peace",
           "with its delicate beauty."), "Keep the description of the figurehead's beauty with its preposition."),
    132: (("A beautiful woman is said to have", "come from Heaven. She forgot this turban",
           "when she went back."), "Keep the departure clause together."),
    154: (("A polished crystal skull", "whose creation remains a mystery."), "Keep the complete relative clause."),
    174: (("A blank piece of parchment.", "Its purpose is a mystery."), "Keep each complete sentence on its own row."),
}


def review_sources():
    selected, evidence = {}, {}
    for family in REVIEW_FAMILIES:
        path = Path(f"releases/all_routes_editorial_20261111_{family}_candidate/verification/registered_review.json")
        payload = base.load(path)
        assert payload["translation_policy"] == "natural-dialogue-v2"
        evidence[str(path)] = base.digest(path)
        for row in payload["records"]:
            number = row.get("message_ID", 0)
            if FIRST <= number < FIRST + COUNT:
                assert number not in selected and all(row["review"].values())
                selected[number] = (path, row, row["registered_reference"]["exact_stored_hex"])
    number = FIRST + 116
    special, = base.load(SOURCE_116)["records"]
    assert number not in selected and special["id"] == f"COMMON_MESSAGE_{number}" and all(special["review"].values())
    selected[number] = (SOURCE_116, special, special["current_reference"]["text_hex"])
    evidence[str(SOURCE_116)] = base.digest(SOURCE_116)
    assert set(selected) == set(range(FIRST, FIRST + COUNT))
    return selected, evidence


def card_records(clean, active, ram):
    clean_arm, arm = (image.read_file(stage.ARM) for image in (clean, active))
    common = active.read_file(stage.COMMON)
    workflow = stage.workflow
    directory = stage.native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    source = workflow.common_message_entries(clean.read_file(stage.COMMON), clean_arm)
    installed = workflow.owned_entries(common, arm, directory)
    sections = MainCodeFile(arm, BASE).sections
    staged, = (bytes(section.data[:-48]) for section in sections if section.ramAddress == STAGE)
    assert len(staged) == 123264 and ram[POOL - BASE:POOL - BASE + len(staged)] == staged
    assert all(branch_target(arm, site) == GETTER for site in LOOKUP)
    assert all(branch_target(arm, site) == PAINTER for site in PAINT)
    getter = GETTER - POOL
    assert unpack_from("<I", staged, getter + 20)[0] == 0xE35400DA
    table = unpack_from("<I", staged, getter + 44)[0]
    assert table == 0x0238C6C4
    pointers = unpack_from(f"<{COUNT}I", staged, table - POOL)
    registered, proof_paths = review_sources()
    records = []
    for index, pointer in enumerate(pointers):
        number = FIRST + index
        review_path, row, exact = registered[number]
        assert source[number].text.hex() == row["source_hex"]
        assert installed[number].text.hex() == exact
        if pointer >= POOL:
            data, offset = staged, pointer - POOL
            owner = "copied item catalogue"
        else:
            section, = (s for s in sections if s.ramAddress <= pointer < s.ramAddress + len(s.data))
            assert section.ramAddress == 0x01FFD000
            data, offset = section.data, pointer - section.ramAddress
            owner = "resident item catalogue"
        raw = bytes(data[offset:data.index(b"\0\0", offset) + 2])
        if pointer >= POOL:
            assert ram[pointer - BASE:pointer - BASE + len(raw)] == raw
        lines = raw[:-2].decode("ascii").split("\0")
        assert 1 <= len(lines) <= 3 and all(1 <= len(line) <= 47 for line in lines)
        english = " ".join(lines)
        assert english == row["english"] and english == installed[number].text.decode("ascii")
        decision = dict(file_path=stage.COMMON, item_ID=index, message_ID=number,
            source_reference=workflow.reference(source[number]), source_hex=row["source_hex"],
            current_reference=workflow.reference(installed[number]), current_hex=exact,
            current_projection=dict(pointer=pointer, pointer_field=table + index * 4,
                                    stored_hex=raw.hex(), lines=lines, storage=owner,
                                    verified_in_main_RAM=pointer >= POOL),
            English=english, previous_review=str(review_path),
            previous_decision=row.get("decision", row.get("editorial_decision")),
            previous_reason=row["localization_note"], review=row["review"])
        if index in WRAP_DRAFTS:
            draft, reason = WRAP_DRAFTS[index]
            assert " ".join(draft) == english and list(draft) != lines and all(0 < len(line) <= 47 for line in draft)
            compiled = "\0".join(draft).encode("ascii") + b"\0\0"
            assert len(compiled) == len(raw)
            decision["open_wrap"] = dict(proposed_rows=list(draft), stored_hex=compiled.hex(), reason=reason, installed=False)
        records.append(decision)
    return records, proof_paths


def actual_rows(image, expected, y, left, right):
    actual = {(x, row) for row in range(y, y + 12) for x in range(left, right)
              if image.getpixel((x, row)) == (230, 230, 230)}
    assert actual == expected, (y, len(actual), len(expected), list(actual ^ expected)[:5])
    return len(actual)


def verify_cards(image, ram, records, arm, observed, *, workspace=ROOT):
    sample = base.load(workspace / "sample.json")
    captures = shots(observed)
    font = GameAsciiFont.from_arm9(arm)
    kanji = image.read_file("/GRP/KANJI.FNT")
    assert stage.native.digest(kanji) == REFERENCE_KANJI_FONT_SHA256
    mapping = unpack_from("<3340H", arm, 0x125EC4)
    plan = base.load(ITEMS)
    for i, row in enumerate(plan["item_advice_projection"]):
        slot = records[i]["current_projection"]
        row.update(compiled="\n".join(slot["lines"]), pointer=slot["pointer"])
    for projection in plan["item_only_projection"]:
        kind = projection["kind"]
        for i, pointer in enumerate(projection["compiled_pointers"]):
            label = next(r for r in plan["records"] if r.get("kind") == kind and r["index"] == i)
            offset = pointer - BASE
            label["compiled"] = ram[offset:ram.index(0, offset)].decode("ascii")
    rows, previews = [], []
    for case in sample["cases"]:
        i, frame = case["item_id"], case["frame"]
        screen = captured(captures[frame])
        draws = expected_draws(arm, plan, "main", (0, 4), item_index=i)
        name = draws[1]["text"]
        assert name.isascii() and name.strip() == name
        info = {}
        for draw in draws[1:]:
            source_y = draw["y"]
            nominal_y = 24 if source_y == 0 else 64 if source_y == 12 else 80 if source_y == 24 else 112 + (source_y - 36) // 12 * 16
            x = 56 if source_y == 0 else draw["x"] + 8
            glyph_y = nominal_y + int(draw["text"].isascii())
            info.setdefault(nominal_y, set()).update(glyph_pixels(font, kanji, mapping, draw["text"], x, glyph_y))
        info[2] = glyph_pixels(font, kanji, mapping, "Items", 116, 3)
        for y in (112, 128, 144):
            info.setdefault(y, set())
        masks = [
            dict(row_y=y, complete_ink_pixels=actual_rows(screen, expected, y,
                 116 if y == 2 else 56 if y == 24 else 8, 144 if y == 2 else 248))
            for y, expected in sorted(info.items())
        ]
        rows.append(case | dict(name=name, capture=captures[frame], masks=masks, tooltip=tooltip(font, screen, name)))
        previews.append((name, screen.crop((0, 0, 256, 160))))
    assert {row["page"] for row in rows} == {case["page"] for case in sample["cases"]}
    first = captured(captures[sample["cases"][0]["frame"]])
    wrap = captured(captures[sample["wrap"]])
    assert first.crop((0, 0, 256, 192)).tobytes() == wrap.crop((0, 0, 256, 192)).tobytes()
    tooltip(font, wrap, rows[0]["name"])
    back = captured(captures[sample["back"]])
    from scripts.verify_gallery_historic_sites_menu_20261121 import menu_mask
    menu_mask(font, back, "Historic Sites")
    sheets = {}
    for start in range(0, len(previews), 8):
        group = previews[start:start + 8]
        sheet = Image.new("RGB", (1024, ((len(group) + 1) // 2) * 340), "#222c36")
        for idx, (label, crop) in enumerate(group):
            x, y = idx % 2 * 512, idx // 2 * 340
            ImageDraw.Draw(sheet).text((x + 7, y + 4), label, fill="white")
            sheet.paste(crop.resize((512, 320), Image.Resampling.NEAREST), (x, y + 19))
        path = workspace / f"items_part_{start // 8 + 1}.png"
        sheet.save(path)
        sheets[str(path)] = base.digest(path)
    return rows, sheets


def main():
    assert not OUTPUT.exists()
    release, ledger = map(base.load, (current.RELEASE, base.LEDGER))
    digest = base.digest(current.ROM)
    assert digest == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(stage.CLEAN) == release["clean_input_sha256"]
    clean, active = map(base.NdsImage.open, (stage.CLEAN, current.ROM))
    observed = report(ROOT / "capture", digest)
    assert observed["frames"] == 23000 and not observed["earned_unlock_verified"]
    assert observed["scripted_input_schedule"] == base.load(DONOR / "all_inputs.json")
    snapshot = observed["read_only_RAM_snapshot"]
    ram_path = Path(snapshot["path"])
    assert snapshot["read_only_export"] and snapshot["sha256"] == base.digest(ram_path)
    ram = ram_path.read_bytes()
    cards, paths = card_records(clean, active, ram)
    actual, sheets = verify_cards(active, ram, cards, active.read_file(stage.ARM), observed)
    assert {case["page"] for case in actual} == set(range(1, 15))
    watched = {case["item_id"] for case in actual}
    for rec in cards:
        rec["viewed_in_this_replay"] = rec["item_ID"] in watched
    evidence = paths | {str(path): base.digest(path) for path in (current.RELEASE, ITEMS, ROOT/"sample.json",
                                      ROOT/"capture/capture_report.json", ROOT/"fixture.json", ram_path)}
    base.save(OUTPUT, dict(candidate_sha256=digest, registered_release=str(current.RELEASE), records=cards,
        verified_consumer_calls=dict(getter=list(LOOKUP), layout=list(PAINT)), current_emulator_samples=actual,
        ordinary_grid_controls=True, initialized_collection=True, wrapped=True, back=True, hardware=False,
        changed_rom=False, new_credit=0, sheets=sheets, evidence=evidence))
    print(f"Bound {len(cards)} current item descriptions and verified {len(actual)} current Gallery cards.")


if __name__ == "__main__":
    main()
