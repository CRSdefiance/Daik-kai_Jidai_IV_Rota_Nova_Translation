"""Register the North Sea exchanges with native pages and bound prior scene evidence."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_rafael_first_voyage_debrief_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as workflow_template
from scripts import stage_rafael_north_sea_20261119 as stage
from scripts import verify_rafael_north_sea_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "rafael-north-sea-v1-20261119"
ROOT = Path("out/rafael_north_sea_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_North_Sea_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_north_sea_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_north_sea_20261119.md")
STARTUP, QA = offline.STARTUP_PROOF, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Rafael’s North Sea encounters and the summons to Lisbon have 18 revisions and 94 justified retentions in the registered candidate."
verified = SimpleNamespace(PROOF=offline.PROOF)

HISTORICAL_TRANSITIONS = {
    49: (
        "Rafael_B49_actual_v8107/paired_source_English_observed_path_complete_pages_names_C281_andreturn.json",
        "actual_source_English_single_page_speeches_C281_command_andfollowing_return_preserved",
        (0xA000, 0xC281),
    ),
    50: (
        "Rafael_B50_actual_v8156/paired_source_English_all28_pages_three_names_4821_departure_andreturn.json",
        "actual_source_English_all28_single_page_speeches_4821_4720_4681_A000_andnormal_return_preserved",
        (0xA000, 0x4821, 0x4720, 0x4681),
    ),
}


def historical_transition_receipts(stored):
    receipts = []
    for block, (filename, result, words) in HISTORICAL_TRANSITIONS.items():
        path = Path("work/analysis") / filename
        evidence = base.load(path)
        assert evidence[result] and not evidence["unresolved"]
        assert evidence["no_excluded_complete_page_masks_orforced_gameplay_conditions"]
        replay, = (g for g in evidence["groups"] if g["version"] == "English")
        assert replay["native_terminal_result"] == [0, 0]
        assert set(words[1:]) <= {cmd["word"] for cmd in replay["command_pairs"]
                                  if cmd["exchange_command_ordinal"] is not None}
        group, = (g for g in stored["groups"] if g["block"] == block)
        controls = [cmd for cmd in group["commands"] if cmd["word"] in words]
        assert set(words) == {cmd["word"] for cmd in controls}
        assert all(cmd["stored"] == cmd["current"] for cmd in controls)
        assert [cmd["stored"] for cmd in controls] == [
            cmd["whole_command_hex"] for cmd in replay["fixture"]["all_original_exchange_commands"]
            if cmd["word"] in words
        ]
        receipts.append(dict(block=block, fixture_path=str(path), fixture_sha256=base.digest(path),
                             stage_unchanged_control_bytes=controls, edited_pages_observed=False))
    return receipts


verification = checked_text(getsource(workflow_template.verify), {
    '    stored, painter, playback, boot, draft = map(base.load, (\n'
    '        stage.PROOF, offline.PROOF, game.PROOF, STARTUP, stage.review.OUTPUT))':
        '    stored, painter, boot, draft = map(base.load, (stage.PROOF, offline.PROOF, STARTUP, stage.review.OUTPUT))',
    '(stored, painter, playback, boot)': '(stored, painter, boot)',
    '    assert not playback["natural_activation"] and not playback["hardware"]\n'
    '    path, = playback["paths"]\n'
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert not painter["actual_gameplay"] and len(painter["native_macro_checks"]) == 2\n'
        '    historical = historical_transition_receipts(stored)',
    '    assert all(base.digest(p) == sha for receipt in (playback, boot) for p, sha in receipt["evidence"].items())':
        '    assert all(base.digest(p) == sha for p, sha in boot["evidence"].items())',
    '    sheets = painter["contact_sheets"] + path["sheets"]': '    sheets = painter["contact_sheets"]',
    '    assert len(sheets) == 5': '    assert len(sheets) == 3',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {"/data/SC0.DK4": native.digest(after["/data/SC0.DK4"])}',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 4 and len(commands) == len(draft["records"]) == 112',
    'len(revisions) == 19 and len(retentions) == 176': 'len(revisions) == 18 and len(retentions) == 94',
    '    seen = set(path["speeches"])': '    assert all(len(row["pages"]) == 1 for row in revisions.values())',
    '        row["initialized_emulator_excerpt_observed"] = (file_path == "/data/SC0.DK4" and block == 127 and\n'
    '            (ident in seen or row["kind"] == "typed-choice-label"))':
        '        row["revised_page_observed_in_gameplay"] = False',
    'reviewed_native_and_live_sheets=viewed, checked_story_format_guard=controls, initialized_gameplay=playback,\n'
    '        shared_storage_scope=prior["shared_storage_scope"])':
        'reviewed_native_sheets=viewed, checked_story_format_guard=controls, actual_new_scene_pages_observed=0,\n'
        '        historical_scene_transitions=historical, shared_storage_scope=prior["shared_storage_scope"])',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 905 and len(manifest["checks"]) == 240':
        'len(manifest["batches"]) == 906 and len(manifest["checks"]) == 241',
    "release_stack_before_rafael_first_voyage_debrief.json": "release_stack_before_rafael_north_sea.json",
    "release_stack_with_rafael_first_voyage_debrief.json": "release_stack_with_rafael_north_sea.json",
    "verified_manuel_poem_predecessor": "verified_rafael_first_voyage_debrief_predecessor",
    "rafael_first_voyage_debrief_release": "rafael_north_sea_release",
    "registered_rafael_first_voyage_debrief_and_complete_parent_inverse":
        "registered_rafael_north_sea_and_complete_parent_inverse",
    "rafael_first_voyage_debrief_pipeline": "rafael_north_sea_pipeline",
    "prose_revisions=39": "prose_revisions=18",
    "justified_retentions=93": "justified_retentions=94",
    "text_display_revisions=39, pagination_fixes=1": "text_display_revisions=18, pagination_fixes=0",
    "ordinary_Rafael_New_Game_departure_and_guided_preparation=True": "historical_unchanged_North_Sea_transition_controls=True",
    "natural_activation=True, hardware=False": "new_story_gameplay=False, hardware=False",
    "previously_localized_records=132": "previously_localized_records=112",
    "verified.PROOF, verified.LIVE, args.visual_review,": "verified.PROOF, args.visual_review,",
    'ledger["rafael_first_voyage_debrief_20261119"]': 'ledger["rafael_north_sea_20261119"]',
    "Preserve Rafael departure and debrief ROM or reconstruction": "Preserve Rafael North Sea ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael’s North Sea test candidate

The [local ROM](../../{ROM.as_posix()}) includes the reviewed North Sea exchanges and carries forward the verified departure build.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael’s North Sea encounters

Reviewed 112 records in Lil’s confrontation and handover, Rafael’s encounter with Sera and Hodram, and the summons to Lisbon. The draft became 18 revisions and 94 justified retentions. Lil presses her case with sharper spoken phrasing, the New World stays together, and the messenger’s company-name question fits on one line. The existing silent encounter with Sera and Hodram works in context and carries forward in full. [Exact review ledger](../{REVIEW.as_posix()})

All 18 revised pages passed native and visual checks. The revisions in these optional scenes received offline coverage. Earlier initialized emulator captures cover the unchanged confrontation transition and dye card controls. The current ROM received six startup checks and 24 protected name getter checks. Hardware remains unverified. [Display and startup evidence](../{VERIFY.as_posix()})

Only three blocks in Rafael’s story archive changed. The clean-input patch reconstructs the candidate byte for byte, and all 34 focused tests passed. The release retains 114 accepted layers and the ASCII right-bound correction. The ledger preserves 27,700 credited records and 276 shared keys with open display coverage. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
