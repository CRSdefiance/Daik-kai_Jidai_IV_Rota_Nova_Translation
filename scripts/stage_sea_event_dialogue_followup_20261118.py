"""Review the sudden-storm warnings and complete sea-foam exchange."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as source
from scripts import register_sailing_mode_prose_20261118 as parent
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.stage_sea_event_review_v1 import native_stored

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = source.ARM, source.COMMON, native.CLEAN
ROOT = Path("work/sea_event_dialogue_followup_20261118")
ROM = ROOT / "Sea_Event_Dialogue_Followup_RESEARCH_ONLY.nds"
PROOF = ROOT / "staged.json"
NUMBERS = (*range(409, 416), *range(457, 481))
REVISIONS = {
    411: ("Storm, Admiral!", "It was just sunny..."),
    412: ("Admiral, a storm!", "It was so clear..."),
    413: ("A storm! That's odd.", "It was just so clear."),
    415: ("Aah, a storm!", "The sun was just out..."),
    457: ("Admiral, please look over there!", "Odd bubbles on the water!"),
    462: ("Admiral, look!", "Weird bubbles on the water!"),
}
NOTES = {
    411: "Restore the admiral as the addressee. Keep the casual surprise at how recently it was sunny.",
    412: "Restore the admiral as the addressee. Give the contrast with the clear sky a complete second row.",
    413: "Keep the original wording. Give the change in weather a complete sentence on the second row.",
    415: "Keep the drawn-out alarm and the observation about the sun. Break between the two sentences.",
    457: "Keep the polite request, the indication of where to look and the sighting at the surface. Give each beat its own row.",
    462: "The informal speaker points out the bubbles excitedly. Drop the filler 'there are' so the sighting reads as one exclamation.",
}


def logical(raw):
    return " ".join(raw.decode("ascii").split())


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(CLEAN)
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    clean_arm = clean.read_file(ARM)
    japanese = common_message_entries(clean.read_file(COMMON), clean_arm)
    arm, common = runtime.arm, runtime.common
    assert native.digest(arm) == release["target_ARM9_sha256"]
    assert native.digest(common) == release["target_COMMON_sha256"]
    old = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    historical = base.load(source.OUTPUT)
    prior = {r["message_ID"]: r for r in historical["records"]}
    groups = {g["first_ID"]: g for g in historical["exact_native_event_groups"]}
    group_by_number = {}
    for start, stop, table, pool, pc, call, consumer, role, context in source.GROUPS:
        if start not in NUMBERS:
            continue
        group = groups[start]
        rows = 4 if start == 477 else 8
        if table:
            end = table + rows * 4
            assert arm[table:end] == clean_arm[table:end]
        assert group["source_native_caller"] == source.caller_binding(
            clean_arm, arm, pc, call, pool, source.BASE + table if table else start, consumer)
        assert group["original_role_argument"] == role
        group_by_number.update((n, (group, context)) for n in range(start, stop))
    assert set(group_by_number) == set(NUMBERS)
    edited = {n: (" " + "\n  ".join(lines)).encode("ascii") for n, lines in REVISIONS.items()}
    assert all(max(map(len, lines)) <= 35 for lines in REVISIONS.values())
    assert all(old[n].text != raw for n, raw in edited.items())
    deployed, entries, slots = owned_deployment(common, arm, old, edited)
    changed = with_components(runtime, arm, deployed)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    pages, records = [], []
    for n in NUMBERS:
        previous, current, original = old[n], entries[n], japanese[n]
        group, context = group_by_number[n]
        reviewed = prior[n]
        assert reference(original) == reviewed["source_reference"]
        assert original.text.hex() == reviewed["source_hex"]
        assert logical(previous.text) == reviewed["english"]
        assert original.text.count(b"%") == previous.text.count(b"%") == current.text.count(b"%") == 0
        case = native_stored(changed, reviewed, group, current.text)
        display = case.pop("display")
        lines = [line.strip() for line in display.decode("ascii").splitlines()]
        assert 1 <= len(lines) <= 4 and all(0 < len(line) <= 36 for line in lines)
        english = logical(current.text)
        assert " ".join(lines) == english
        pixels, glyphs = render_portrait(raster, arm, kanji, display)
        assert [g["code"] for g in glyphs] == glyph_codes(display)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(english[0]), ord(english[-1]))
        if n in edited:
            assert tuple(lines) == REVISIONS[n]
            before = native_stored(runtime, reviewed, group, previous.text).pop("display")
            assert before != display
            baseline, _ = render_portrait(raster, arm, kanji, before)
            pages.extend([(f"{n} before", baseline), (f"{n} after", pixels)])
        else:
            before = display
        note = NOTES.get(n) or reviewed["localization_note"]
        records.append(dict(id=f"COMMON_MESSAGE_{n}", message_ID=n, file_path=COMMON,
            speaker=reviewed["speaker"], context=context, clean_Japanese=original.text.decode("cp932"),
            english=english, previous_English=logical(previous.text), localization_note=note,
            decision="retention" if n not in edited else "wrap revision" if english == logical(previous.text) else "revision",
            source_reference=reference(original), current_reference=reference(previous), staged_reference=reference(current),
            source_hex=original.text.hex(), current_hex=previous.text.hex(), staged_hex=current.text.hex(),
            before_display_hex=before.hex(), display_hex=display.hex(), visible_lines=lines,
            formatting_evidence=dict(native_call=case, glyph_count=len(glyphs), pages=1,
                all_glyphs_and_edges_verified=True, no_runtime_substitutions=True),
            review=dict.fromkeys(parent.GATES, True) | {"formatting": False}))
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, deployed)
    ROOT.mkdir()
    image.save(ROM)
    assert base.NdsImage.open(ROM).read_file(COMMON) == deployed
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheets = portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(candidate=str(ROM), candidate_sha256=base.digest(ROM),
        parent_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        target_ARM9_sha256=release["target_ARM9_sha256"], target_COMMON_sha256=native.digest(deployed),
        entire_parent_inverse=True, allocations=slots, preserved_entries=len(entries) - len(edited),
        earlier_review=dict(path=str(source.OUTPUT), sha256=base.digest(source.OUTPUT)),
        font=font, sheets=sheets, translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=parent.GATES, records=records))
    print(f"{len(records)} exact reviews, {len(edited)} revised native pages.")


if __name__ == "__main__":
    main()

