"""Check the revised spare-berth prompt in the current native formatter."""

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import stage_recruitment_capacity_wraps_20261123 as capacity
from scripts import verify_nagasaki_tavern_20261124 as tavern
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write


KEY = 1045
OUT = tavern.OUT.with_name("nagasaki_tavern_recruitment_preflight_20261124.json")
KEY_CASES = tuple(sorted({*capacity.COUNTS, 29}))


def main():
    active = tavern.play.current
    release = read(active.RELEASE)
    packet = read(tavern.OUT)
    assert packet["candidate_sha256"] == release["candidate_sha256"] and packet["ordinary_gameplay"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    ctx = RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=3)
    assert sha256(ctx.arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(ctx.common).hexdigest() == release["target_COMMON_sha256"]
    clean = NdsImage.open(CLEAN)
    source = tavern.common_message_entries(clean.read_file(active.COMMON), clean.read_file(active.ARM))[KEY]
    before_rows = tavern.common_rows(ctx.common, ctx.arm)
    current = before_rows[KEY]
    review, = [row for row in packet["verified_common_records"] if row["message_ID"] == KEY]
    assert tavern.panels.text_reference(source) == review["source"]
    assert tavern.panels.text_reference(current) == review["installed"]
    assert review["proposed_english"] == tavern.PROPOSED
    template = (b" " + tavern.PROPOSED.encode("ascii")).ljust(len(current.text), b" ")
    assert len(template) == len(current.text) and all(text.count(b"%s") == text.count(b"%") == 1
        for text in (source.text, current.text, template))
    assert current.text.startswith(b" ") and b"\r" not in template and b"\n" not in template
    common, records, allocations = capacity.owned_deployment(ctx.common, ctx.arm, before_rows, {KEY: template})
    assert records[KEY].text == template and not allocations[KEY]["new_null_fields"]
    after_rows = tavern.common_rows(common, ctx.arm)
    assert [new.message_id for old, new in zip(before_rows, after_rows, strict=True) if old != new] == [KEY]

    layout = capacity.native_formatter()
    cpu, _ = capacity.get_machine(ctx.arm, ctx.raw)
    raster, _, _ = capacity.recruitment.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    row = dict(id=f"COMMON_MESSAGE_{KEY}", message_id=KEY, speaker="Sailor", english=tavern.PROPOSED,
        context="After 57 sailors volunteer, the sailor reports the free berths and asks whether to recruit again.",
        source_meaning="There is still space aboard for the specified number of people. Shall we recruit more?",
        localization_note="Keep the spoken offer and the exact remaining capacity while dropping the repeated word.",
        English_argument_source_indices=[0], review=dict.fromkeys(GATES, True))
    cases, pages = [], []
    for count in KEY_CASES:
        values = (str(count).encode("ascii"),)
        before = layout(cpu, row, values, current.text)
        after = layout(cpu, row, values, template)
        expected = tavern.PROPOSED % count
        statement, question = expected.split(". ", 1)
        assert after["lines"] == [statement + ".", question], (count, after["lines"])
        assert not after["findings"] and str(count) in after["lines"][0]
        formatted = bytes.fromhex(after["formatted_hex"])
        plane, glyphs = capacity.recruitment.render_portrait(raster, ctx.arm, kanji, formatted)
        codes = [glyph["code"] for glyph in glyphs]
        assert codes == capacity.recruitment.glyph_codes(formatted) and (codes[0], codes[-1]) == (ord(expected[0]), ord("?"))
        cases.append(dict(count=count, before=before, after=after, native_plane_sha256=sha256(bytes(plane)).hexdigest()))
        pages.append((f"{KEY} / {count} berths", plane))
    gameplay_case, = [case for case in cases if case["count"] == 29]
    assert gameplay_case["before"]["lines"] == review["display_lines"]
    preview_folder = OUT.with_suffix("")
    preview_folder.mkdir(exist_ok=True)
    sheets = capacity.recruitment.portrait_sheets(preview_folder, pages)
    policy = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=[row])
    validate_natural_dialogue_batch(policy)
    write(OUT, policy | dict(candidate_sha256=release["candidate_sha256"], source=review["source"], installed=review["installed"],
        proposed_stored_hex=template.hex(), allocation=allocations[KEY], native_cases=cases, sheets=sheets,
        current_ROM_native_offline_fixture=True, source_review=reference(tavern.OUT),
        native_input=ctx.receipt() | {"captain": ctx.startup["actual_captain_getter"]}, ROM_changed=False))
    print(f"Passed {len(cases)} native spare-berth formatting cases, including the observed 29.")


if __name__ == "__main__":
    main()
