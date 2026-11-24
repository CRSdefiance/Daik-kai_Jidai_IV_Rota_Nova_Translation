"""Review and stage all stock Promised Words clues through the native formatter."""

from argparse import ArgumentParser
from pathlib import Path
from struct import iter_unpack, unpack_from
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan
from dk4tool.patch.village_portrait_wrap import MANUSCRIPT, paragraph
from scripts import register_narvik_lookout_20261124 as parent
from scripts import stage_sea_approach_village_review_v1 as portrait
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts.inventory_arm9_text import components
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_village_promised_words_research import caller


ARM, COMMON, RELEASE = parent.ARM, parent.COMMON, parent.RELEASE
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_village_clue_punctuation")
ROM = ROOT / "Village_Clues_STAGED.nds"
STORED, OUT = ROOT / "stored_proof.json", ROOT / "village_clue_review_20261124.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
played = SimpleNamespace(RELEASE=RELEASE)
LEAD = "They say it means"
BEFORE = LEAD + " %s."
AFTER = LEAD + ' %s"'
TEMPLATE = "VILLAGE_MESSAGE_1"
LITERAL_PLAN = Path("work/analysis/village_promised_words_plan.json")
CONTEXT = ("After the officer relays the chief's request, the player enters and confirms the promised words. "
           "Acceptance produces the clue followed by permission to use the village facilities on the next visit. "
           "A failed answer can lead to the notice that the chief has left.")
PHRASES = {
    0: ("the stairway to heaven",),
    1: ("the mountain of fire",),
    2: ("bell-shaped rock", "jutting out into the sea."),
    4: ("stone statues",),
    5: ("the great land.",),
    6: ("Frenchman", "visited this land."),
    7: ("the man who named this land.",),
    8: ("the mountain that breathes fire.",),
    10: ("the hero who discovered this land.",),
    11: ('"the name of the island."',),
    12: ('"the name of the lake."',),
    14: ('"the beautiful valley."',),
    16: ("covered with sandstone.",),
    18: ("of a god.",),
    19: ("of stone pillars.",),
    20: ("the mysterious stone pillars.",),
    21: ('"the land that never thaws."',),
    23: ('"the elusive giant bird."',),
}
MESSAGE_REASONS = {
    0: "The officer's request preserves the original address Admiral and clearly attributes the request to the chief.",
    4: "The keyboard instruction repeats the chief's term and gives the player a clear action.",
    5: "The keyboard title uses the same short term as the request and instruction.",
    2: "The notice keeps the next-visit timing and names both the trading post and tavern.",
    3: "The brief outcome preserves the chief's departure without adding a reason or a promise to return.",
}


def cstring(data, start):
    stop = data.index(0, start, start + 255)
    return bytes(data[start:stop])


def compiled_clue(row):
    quote = row["english"]
    assert quote.startswith('"') and quote.endswith('"') and quote.count('"') == 2
    full = LEAD + " " + quote[:-1] + '."'
    marked = full
    for phrase in PHRASES.get(row["index"], ()):
        assert marked.count(phrase) == 1 and "_" not in full
        marked = marked.replace(phrase, phrase.replace(" ", "_"))
    formatted = paragraph(marked).replace("_", " ")
    assert formatted.startswith(LEAD) and formatted.endswith('."')
    assert " ".join(formatted.split()) == full
    for phrase in PHRASES.get(row["index"], ()):
        assert any(phrase in line for line in formatted.splitlines())
    # The stored template supplies a space before the argument. If a complete
    # quotation starts on the second row, this space stays blank on row one.
    if formatted.startswith(LEAD + "\n"):
        formatted = LEAD + " " + formatted[len(LEAD):]
    assert formatted.startswith(LEAD + " ")
    return full, formatted[len(LEAD) + 1:-1], formatted


def exclusive_owners(image, edited, arm):
    """Find aliases to live text and any adjoining NUL byte owned by an edit."""
    addresses = {address for row in edited for address in range(row["pointer"], row["pointer"] + row["extent"])}
    expected = {BASE + row["field"]: row["pointer"] for row in edited}
    template, = [row["pointer"] for row in edited if row["id"] == TEMPLATE]
    literal = read(LITERAL_PLAN)["literal_wrapper"]
    signature = bytes.fromhex(literal["payload_hex"])
    assert len(signature) == literal["size"] and arm.count(signature) == 1
    tail = arm.index(signature) + len(signature) - 4 * len(literal["exact_template_pointers"])
    slot = literal["exact_template_pointers"].index(template)
    expected[BASE + tail + 4 * slot] = template
    found = {}
    for component, base, raw in components(image):
        for phase in range(4):
            data = memoryview(raw)[phase:phase + ((len(raw) - phase) // 4) * 4]
            for index, (pointer,) in enumerate(iter_unpack("<I", data)):
                if pointer not in addresses:
                    continue
                address = base + phase + 4 * index
                assert component == "arm9" and address not in found
                found[address] = pointer
    assert found == expected, (found, expected)
    # The loaded pool references come through the same main ARM9 literal table
    # used by the original clue consumer before formatted dialogue preparation.
    assert all(unpack_from("<I", arm, field - BASE)[0] == pointer for field, pointer in expected.items())
    return [{"field_address": field, "text_address": pointer} for field, pointer in sorted(found.items())]


def build_edits(parent_arm, clean_arm, image, prior):
    code = MainCodeFile(parent_arm, BASE)
    assert bytes(code.save()) == parent_arm and code.sections[3].ramAddress == STAGE
    stage = code.sections[3]
    pool = bytes(stage.data)
    assert cache_plan(parent_arm)["payload_bytes"] == len(pool) - 48
    target_pool, rows, edits, layouts = bytearray(pool), [], [], []
    names = {row["index"]: row["english"] for row in prior["records"] if row["kind"] == "ANSWER"}
    for row in prior["records"]:
        field, key, kind = row["field"], row["id"], row["kind"]
        ja_pointer, pointer = (unpack_from("<I", arm, field)[0] for arm in (clean_arm, parent_arm))
        source = cstring(clean_arm, ja_pointer - BASE)
        current = cstring(pool, pointer - POOL)
        assert ja_pointer == row["source_pointer"] and source.hex() == row["source_hex"]
        assert source.decode("cp932") == row["japanese"]
        logical = " ".join(current.decode("ascii").split())
        revision = kind == "CLUE" or key == TEMPLATE
        if kind == "CLUE":
            assert logical == row["english"]
            english, argument, formatted = compiled_clue(row)
            new = argument.encode("ascii")
            layouts.append(dict(index=row["index"], answer=names[row["index"]], old_argument=current.decode("ascii"),
                                new_argument=argument, previous=BEFORE % current.decode("ascii"), proposed=formatted))
            reason = ("Keep the description and its distinct answer " + names[row["index"]] +
                      ". Place the sentence period inside the closing quotation mark.")
            if formatted.count("\n") and [len(x.strip()) for x in formatted.splitlines()] != [
                    len(x.strip()) for x in (BEFORE % current.decode("ascii")).splitlines()]:
                reason += " Where possible, place the grouped clue phrase on a complete row."
        elif key == TEMPLATE:
            assert logical == BEFORE and source.count(b"%s") == 1
            english, new = AFTER, AFTER.encode("ascii")
            reason = "Keep the officer's reported explanation and one original string argument. Finish each quotation after its period."
        else:
            english = logical
            new = current
            assert logical == row["english"].replace("Captain,", "Admiral,", 1)
            reason = (f"Retain the observed stock answer {logical!r} so the player can enter the same accepted word."
                      if kind == "ANSWER" else MESSAGE_REASONS[row["index"]])
        if revision:
            offset = pointer - POOL
            size = max(len(new), len(current)) + 1
            assert 0 <= offset < offset + size < len(pool) - 48
            extent = pool[offset:offset + size]
            assert extent == current.ljust(size, b"\0"), (key, current, new, extent)
            replacement = new.ljust(size, b"\0")
            target_pool[offset:offset + size] = replacement
            edits.append(dict(id=key, field=field, pointer=pointer, extent=size, pool_offset=offset,
                              before_hex=extent.hex(), after_hex=replacement.hex()))
        row_source = dict(ARM9_file_offset=field, native_text_address=ja_pointer, exact_hex=source.hex())
        row_current = dict(ARM9_file_offset=field, native_text_address=pointer, exact_hex=current.hex())
        rows.append(dict(id=key, file_path=ARM, speaker="System" if kind == "ANSWER" or row["index"] in (4, 5) and kind == "MESSAGE" else "Original village officer",
            context=CONTEXT, source_Japanese=row["japanese"], source_meaning=row["source_meaning"],
            english=english, localization_note=reason, decision="revision" if revision else "retention",
            source_reference=row_source, current_reference=row_current,
            installed_reference=row_current | dict(exact_hex=new.hex()), review=dict.fromkeys(GATES, True)))
    assert len(rows) == 54 and len(edits) == 25 and len(layouts) == 24
    intervals = [(r["pool_offset"], r["pool_offset"] + r["extent"]) for r in sorted(edits, key=lambda edit: edit["pool_offset"])]
    assert all(stop <= next_start for (_, stop), (next_start, _) in zip(intervals, intervals[1:]))
    owners = exclusive_owners(image, edits, parent_arm)
    stage.data = target_pool
    target = bytes(code.save())
    restored = bytearray(target_pool)
    for edit in edits:
        at, length = edit["pool_offset"], edit["extent"]
        restored[at:at + length] = bytes.fromhex(edit["before_hex"])
    assert bytes(restored) == pool
    stage.data = restored
    assert bytes(code.save()) == parent_arm and cache_plan(target) == cache_plan(parent_arm)
    return target, rows, edits, owners, layouts


def verify_clues(arm, image, layouts):
    raster, _, _ = portrait.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    pages, native = [], []
    for layout in layouts:
        index, complete = layout["index"], layout["proposed"]
        proof = caller(arm, 0x78B8C, index, 13, complete, clue=layout["new_argument"])
        assert proof["buffer_canaries_intact"] and proof["complete_prepared_text"] == complete
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, complete.encode("ascii"))
        assert all(0 <= event["x"] < 216 and 0 <= event["y"] < 64 for event in glyphs)
        assert tuple(event["code"] for event in glyphs[-2:]) == (ord("."), ord('"'))
        pages.append((f"{index} {layout['answer']}", pixels))
        native.append(layout | dict(portrait=proof, native_exact_font_ink_sha256=sha256(pixels).hexdigest(),
                                    page_count=1, rows=complete.splitlines()))
    return native, pages


def stage():
    previous = read(RELEASE)
    assert digest(REGISTRY) == previous["registry_sha256"]
    assert digest(CLEAN) == previous["clean_input_sha256"] and digest(previous["candidate"]) == previous["candidate_sha256"]
    image, clean = (NdsImage.open(path) for path in (previous["candidate"], CLEAN))
    arm, clean_arm = image.read_file(ARM), clean.read_file(ARM)
    common = image.read_file(COMMON)
    assert sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert sha256(common).hexdigest() == previous["target_COMMON_sha256"]
    assert arm[0x78B8C:0x78BD0] == clean_arm[0x78B8C:0x78BD0]
    assert arm[0x788C0:0x78904] == clean_arm[0x788C0:0x78904]
    target, rows, edits, owners, layouts = build_edits(arm, clean_arm, image, read(MANUSCRIPT))
    assert parent.template.right_bound(arm, previous["right_bound_configuration"]) == parent.template.right_bound(
        target, previous["right_bound_configuration"])
    native, pages = verify_clues(target, image, layouts)
    statement = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=rows, source_reviews=reference(MANUSCRIPT), literal_wrapper=reference(LITERAL_PLAN),
        candidate_sha256=previous["candidate_sha256"], source_sha256=previous["clean_input_sha256"],
        native_cases=native, pointer_owners=owners, owned_pool_spans=edits, native_caller_and_pointer_tables_unchanged=True,
        release_pending=True, no_new_review_credit=True)
    validate_natural_dialogue_batch(statement)
    before = parent.trend.files(image)
    image.replace_file(ARM, target)
    after = parent.trend.files(image)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    proposed = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert sha256(image.rom.save()).hexdigest() == previous["candidate_sha256"]
    ROOT.mkdir(exist_ok=True)
    with ROM.open("xb") as handle:
        handle.write(proposed)
    assert sha256(proposed).hexdigest() == digest(ROM)
    assert NdsImage.open(ROM).read_file(ARM) == target
    statement["visuals"] = portrait.portrait_sheets(ROOT, pages)
    write(OUT, statement)
    write(STORED, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"], target_ARM9_sha256=sha256(target).hexdigest(),
        target_COMMON_sha256=previous["target_COMMON_sha256"], source_preflight=reference(OUT),
        whole_parent_inverse=True, changed_files=[ARM], pool_bytes=cache_plan(target)["payload_bytes"],
        changed_pool_spans=edits, proposed_views=statement["visuals"]))
    print(f"Staged {len(edits)} owned fields and verified {len(native)} native clue layouts. {digest(ROM)}")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    else:
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(STORED), action)
