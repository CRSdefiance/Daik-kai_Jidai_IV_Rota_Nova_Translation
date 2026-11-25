"""Register the verified mutiny dialogue and exact clean-input patch."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from scripts import register_sea_event_dialogue_followup_20261118 as parent
from scripts import stage_mutiny_dialogue_followup_20261119 as stage
from scripts import verify_mutiny_dialogue_followup_20261119 as verified
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
PROFILE = "all-routes-mutiny-dialogue-followup-v1-20261119"
ROOT = Path("out/mutiny_dialogue_followup_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Mutiny_Dialogue_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_mutiny_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_mutiny_dialogue_followup_20261119.md")
STARTUP, QA = verified.STARTUP, stage.ROOT / "supported_qa.xml"
LAYOUT = stage.ROOT / "portrait_sheet_01.png"
CHECKPOINT = "Seven mutiny lines are revised, and the Quell Mutiny warning and return to the choice menu are verified."


CHOICE_NOTES = (
    "Quell Mutiny states the direct intervention and matches the branch that requires a Boarding Leader.",
    "Appease Crew describes the captain's conciliatory approach before the meal offer is shown.",
    "Do Nothing keeps the inactive choice explicit and clearly distinct from the two interventions.",
)


def choice_retentions(arm, clean_arm, game):
    history = base.load(verified.HISTORICAL)
    choices = base.load(stage.source.OUTPUT)["original_choice_menu"]["records"]
    slots = history["menu_allocation"]["changes"]
    code = MainCodeFile(arm, stage.source.BASE)
    rows = []
    for row, slot, note in zip(choices, slots, CHOICE_NOTES, strict=True):
        index, field = row["choice_index"], slot["field"]
        assert index == slot["index"] and row["source_reference"]["pointer_field"] == stage.source.BASE + field
        pointer = unpack_from("<I", arm, field)[0]
        assert pointer == slot["target_pointer"]
        assert unpack_from("<I", clean_arm, field)[0] == slot["original_pointer"]
        raw = bytes.fromhex(slot["target_terminated_hex"])
        original = bytes.fromhex(slot["source_terminated_hex"])
        assert row["source_hex"] == original.hex()
        at = row["source_reference"]["literal_offset"]
        assert clean_arm[at:at + len(original)] == original
        storage, = [s for s in code.sections if s.ramAddress <= pointer < s.ramAddress + len(s.data)]
        start = pointer - storage.ramAddress
        assert bytes(storage.data[start:start + len(raw)]) == raw == row["english"].encode("ascii") + b"\0"
        masks = [r for r in game["choice_masks"] if r["option"] == index]
        assert len(masks) == 3 and all(r["english"] == row["english"] for r in masks)
        rows.append(row | dict(decision="retention", localization_note=note, current_hex=raw.hex(),
            current_English=row["english"], current_reference=dict(ARM9_sha256=native.digest(arm),
                pointer_field=stage.source.BASE + field, runtime_pointer=pointer, allocation_offset=start),
            display_evidence=masks, review=dict.fromkeys(stage.source.GATES, True)))
    return rows


verify_source = checked_text(getsource(parent.verify), {
    'stored["preserved_entries"] == 3662': 'stored["preserved_entries"] == 3661',
    'len(sheet["messages"]) == 12': 'len(sheet["messages"]) == 14',
    '[457, 463, 469, 470, 478]': '[516, 517, 541]',
    '[457]': '[517]',
    '{457}': '{517}',
    "    assert boot[\"cold_boot\"]": (
        "    assert len(game[\"choice_masks\"]) == 9 and game[\"original_A_selects_quell\"]\n"
        "    assert game[\"absent_boarding_leader_warning\"] and game[\"response_menu_return\"]\n"
        "    assert boot[\"cold_boot\"]"),
    '[41, 0, 0, 0]': '[35, 0, 0, 0]',
    '    validate_natural_dialogue_batch(review)':
        '    review["retained_choices"] = choice_retentions(after[stage.ARM], clean.read_file(stage.ARM), game)\n'
        '    validate_natural_dialogue_batch(review | {"records": review["records"] + review["retained_choices"]})',
    '    earlier = stored["earlier_review"]\n'
    '    assert base.digest(earlier["path"]) == earlier["sha256"]\n'
    '    source = {r["message_ID"]: r for r in base.load(earlier["path"])["records"]}':
        '    assert len(stored["records"]) == 65\n'
        '    assert sum(len(r["formatting_evidence"]["cases"]) for r in stored["records"]) == 77\n'
        '    source = {r["message_ID"]: r for r in base.load(stage.source.OUTPUT)["records"]}',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
pins = publish[publish.index("    candidates = ["):publish.index("    for path in candidates:")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 887 and len(manifest["checks"]) == 222':
        'len(manifest["batches"]) == 888 and len(manifest["checks"]) == 223',
    "release_stack_before_sea_event_dialogue.json": "release_stack_before_mutiny_dialogue.json",
    "release_stack_with_sea_event_dialogue.json": "release_stack_with_mutiny_dialogue.json",
    "verified_sailing_mode_prose_predecessor": "verified_sea_event_dialogue_predecessor",
    "sea_event_dialogue_followup_release": "mutiny_dialogue_followup_release",
    "registered_sea_event_dialogue_followup_and_complete_parent_inverse":
        "registered_mutiny_dialogue_followup_and_complete_parent_inverse",
    "sea_event_dialogue_followup_pipeline": "mutiny_dialogue_followup_pipeline",
    "repository_tests=41": "repository_tests=35",
    "text_display_revisions=6": "text_display_revisions=7",
    "initialized_sea_foam_exchange=True": "initialized_mutiny_quell_missing_role_and_menu_return=True",
    "prose_revisions=4, wrap_only_revisions=2, justified_retentions=25":
        "prose_revisions=7, wrap_only_revisions=0, justified_retentions=58",
    "previously_reviewed_records=31": "previously_reviewed_records=65",
    "sea_event_dialogue_followup_20261118": "mutiny_dialogue_followup_20261119",
    "Preserve sea-event dialogue ROM or clean reconstruction": "Preserve mutiny dialogue ROM or clean reconstruction",
    "# Current editorial checkpoint - 2026-11-18": "# Current editorial checkpoint - 2026-11-19",
    pins: '''    candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds"]\n''',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Mutiny dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) includes seven revised mutiny lines.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Mutiny dialogue and phrase breaks

Reviewed the 65 shared mutiny turns as one exchange with alternate voices and outcomes. Seven revisions keep commands, questions and warnings together. The warnings still escalate from the crew's demand to the threat of force. The existing choice labels stay short, and the warning about the missing Boarding Leader now states the condition before the consequence. The ledger records the reasons for keeping the other 58 turns and the existing choices. [Exact review ledger](../{REVIEW.as_posix()})

All seven revised pages passed complete glyph, width and slot checks and received visual review. The focused emulator replay used a copied voyage save and the established one-instruction event selector. It showed the revised lead-in and all three choices. Quell Mutiny displayed the original missing-role branch and returned to the response menu. The six other revisions received offline native checks. Natural mutiny activation and hardware remain unobserved in this pass. [Native pages](../{(VERIFY / LAYOUT.name).as_posix()}) · [Emulator replay](../{(VERIFY / verified.SHEET.name).as_posix()})

The cumulative candidate passes six startup comparisons, 24 protected name getters and 35 focused tests. The clean-input patch rebuilds the ROM byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. The 65 turns already had credit. The ledger stands at 27,700, with 276 mapped shared keys still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verify_source, __file__ + "::verify", "exec"), env)
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()

