"""Stage a contextual wrap follow-up for the native mutiny exchanges."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_mutiny_review_v1 as source
from scripts import register_sea_event_dialogue_followup_20261118 as parent
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import portrait_case, portrait_sheets, render_portrait

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = source.ARM, source.COMMON, source.CLEAN
ROOT = Path("work/mutiny_dialogue_followup_20261119")
ROM = ROOT / "Mutiny_Dialogue_RESEARCH_ONLY.nds"
PROOF = ROOT / "staged.json"
REVISIONS = {
    517: ("The crew's about to boil over.", "What should we do, Admiral?"),
    520: ("Admiral! The crew's furious!", "They're ready to use force!", "What should we do?"),
    523: ("Admiral! The crew's really mad!", "They want us to go to port!", "What do we do?"),
    524: ("Admiral, the crew's had enough.", "How shall we handle this?"),
    535: ("...Admiral, we have to find a port.", "I feel kind of sorry for the crew."),
    539: ("What a relief...", "But everyone's still on edge.", "We'd better dock soon, Admiral."),
    544: ("Admiral! Without a Boarding Leader,", "it's reckless to quell the mutiny."),
}
NOTES = {
    517: "Keep the imminent loss of control and fold the respectful address into the complete question.",
    520: "Keep the alarm, anger and threat of force. Give the question its own beat before the response menu.",
    523: "Keep this voice's excited 'really mad' and the demand to reach port. Let the demand and question finish on their own rows.",
    524: "The crew has reached its limit. Use a natural warning followed by the measured question from the existing voice.",
    535: "Keep the call to find a port and the young speaker's tentative sympathy. Give each thought a complete sentence.",
    539: "Keep the relief, the concern that tension remains, and the prompt advice to dock. Put the address inside the advice.",
    544: "Lead with the missing Boarding Leader. Keep the warning that trying to suppress the mutiny would be reckless.",
}


def logical(raw):
    return " ".join(raw.decode("ascii").split())


def group_map(historical, clean, arm):
    old = {g["first_ID"]: g for g in historical["exact_native_crew_groups"]}
    groups = {}
    for start, end, table, literal, sites, consumer, role, _ in source.GROUPS:
        group = old[start]
        slots = group["table_slots"]
        assert unpack_from(f"<{len(slots)}i", clean, table) == unpack_from(f"<{len(slots)}i", arm, table) == tuple(slots)
        bindings = [source.caller_binding(clean, arm, pc, call, literal, source.BASE + table, consumer) for pc, call in sites]
        assert group["native_callers"] == bindings and group["original_role_argument"] == role
        groups.update((n, group) for n in range(start, end))
    assert source.exact_singles(clean, arm) == {int(n): row for n, row in historical["native_sailor_calls"].items()}
    return groups


def actors(group, n):
    if group is None:
        return [None]
    if group["consumer"] == 0x02053BD8:
        return [group["table_slots"].index(n)]
    choices = [i for i, _, choice in group["original_voice_choices"] if choice == n]
    return choices if n in source.PRONOUN_IDS else choices[:1]


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    arm, common = runtime.arm, runtime.common
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    japanese = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    original = owned_entries(common, arm, directory)
    historical = base.load(source.OUTPUT)
    groups = group_map(historical, clean_arm, arm)
    prior = {r["message_ID"]: r for r in historical["records"]}
    assert set(prior) == set(source.IDS)
    edited = {n: (" " + "\n  ".join(lines)).encode("ascii") for n, lines in REVISIONS.items()}
    assert all(max(map(len, lines)) <= 35 for lines in REVISIONS.values())
    assert all(original[n].text != body for n, body in edited.items())
    deployed, entries, slots = owned_deployment(common, arm, original, edited)
    staged = with_components(runtime, arm, deployed)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    records, pictures = [], []
    for n in source.IDS:
        prior_row = prior[n]
        clean_row, current_row, staged_row = japanese[n], original[n], entries[n]
        assert reference(clean_row) == prior_row["source_reference"] and clean_row.text.hex() == prior_row["source_hex"]
        assert logical(current_row.text) == prior_row["english"], n
        assert b"%" not in clean_row.text and b"%" not in current_row.text and b"%" not in staged_row.text
        group = groups.get(n)
        selected = actors(group, n)
        assert selected
        cases = [portrait_case(staged, prior_row, group, staged_row.text, i) for i in selected]
        bodies = [case.pop("display") for case in cases]
        display, = set(bodies)
        visible = [line.strip() for line in display.decode("ascii").splitlines()]
        english = logical(staged_row.text)
        assert " ".join(visible) == english and 0 < len(visible) <= 4
        assert all(0 < len(line) <= 36 for line in visible)
        pixels, glyphs = render_portrait(raster, arm, kanji, display)
        assert [g["code"] for g in glyphs] == glyph_codes(display)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(english[0]), ord(english[-1]))
        if n in edited:
            assert tuple(visible) == REVISIONS[n]
            before = portrait_case(runtime, prior_row, group, current_row.text, selected[0]).pop("display")
            assert display != before
            old_pixels, _ = render_portrait(raster, arm, kanji, before)
            pictures.extend([(f"{n} before", old_pixels), (f"{n} after", pixels)])
        else:
            before = display
        row = {k: prior_row[k] for k in ("id", "message_ID", "file_path", "speaker", "context", "source_Japanese",
            "source_meaning", "source_reference", "source_hex", "source_native_macros", "native_substitution_localization")}
        row.update(current_reference=reference(current_row), staged_reference=reference(staged_row),
            previous_English=logical(current_row.text), english=english, current_hex=current_row.text.hex(),
            staged_hex=staged_row.text.hex(), before_display_hex=before.hex(), display_hex=display.hex(),
            decision="revision" if n in edited else "retention",
            localization_note=NOTES.get(n, prior_row["localization_note"]), visible_lines=visible,
            formatting_evidence=dict(cases=cases, glyph_count=len(glyphs), native_ink_sha256=sha256(pixels).hexdigest(),
                complete_first_and_last_glyphs=True, pages=1),
            review=dict.fromkeys(source.GATES, True) | {"formatting": False})
        records.append(row)
    assert sum(len(r["formatting_evidence"]["cases"]) for r in records) == 77
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, deployed)
    ROOT.mkdir()
    image.save(ROM)
    assert base.NdsImage.open(ROM).read_file(COMMON) == deployed
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheets = portrait_sheets(ROOT, pictures)
    base.save(PROOF, dict(candidate=str(ROM), candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=native.digest(deployed), entire_parent_inverse=True, allocations=slots,
        preserved_entries=len(entries) - len(edited), font=font, sheets=sheets, translation_policy="natural-dialogue-v2",
        target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=list(source.GATES), records=records))
    print(f"{len(records)} contextual mutiny turns, {len(edited)} revised native pages, 77 portrait cases.")


if __name__ == "__main__":
    main()

