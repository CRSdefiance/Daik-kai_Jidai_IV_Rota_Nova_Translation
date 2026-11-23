"""Register Rafael's Sofala and adjacent exchanges with qualified display evidence."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_rafael_iberian_aftermath_20261119 as game
from scripts import register_rafael_north_sea_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as template
from scripts import stage_rafael_iberian_aftermath_20261119 as stage
from scripts import verify_rafael_iberian_aftermath_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "rafael-iberian-aftermath-v1-20261119"
ROOT = Path("out/rafael_iberian_aftermath_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_Sofala_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_iberian_aftermath_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_iberian_aftermath_20261119.md")
STARTUP, QA = offline.STARTUP, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Rafael’s Sofala confrontation and five adjacent exchanges are registered with 25 revisions and 92 justified retentions."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.REBOUND)

verification = checked_text(getsource(template.verify), {
    "game.PROOF": "game.REBOUND",
    '    assert not playback["natural_activation"] and not playback["hardware"]\n'
    '    path, = playback["paths"]\n'
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert playback["initialized_fixture"] and not playback["natural_activation"] and not playback["hardware"]\n'
        '    assert playback["replays_on_current_rom"] == 0 and len(playback["speeches"]) == 24\n'
        '    assert len(playback["checked_pages"]) == 6 and playback["revised_pages_verified"] == 5\n'
        '    assert playback["original_commands_observed"] == 56 and playback["normal_return_result"] == [0, 0]\n'
        '    assert playback["retained_reward"] == offline.REWARD and len(playback["distinct_modal_transitions"]) == 2\n'
        '    assert len(painter["native_macro_checks"]) == 3 and len(painter["reused_identical_pages"]) == 22',
    '    sheets = painter["contact_sheets"] + path["sheets"]': '    sheets = painter["contact_sheets"] + playback["sheets"]',
    'len(sheets) == 5': 'len(sheets) == 6',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {"/data/SC0.DK4": native.digest(after["/data/SC0.DK4"])}',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 6 and len(commands) == len(draft["records"]) == 117',
    'len(revisions) == 19 and len(retentions) == 176': 'len(revisions) == 25 and len(retentions) == 92',
    '    seen = set(path["speeches"])':
        '    seen = set(playback["speeches"])\n'
        '    pictured = {r["id"] for r in playback["checked_pages"]}\n'
        '    for n, digest in playback["exact_unchanged_blocks_needed_by_fixture_and_return"].items():\n'
        '        assert native.digest(banks["/data/SC0.DK4"][int(n)]) == digest',
    '        row["initialized_emulator_excerpt_observed"] = (file_path == "/data/SC0.DK4" and block == 127 and\n'
    '            (ident in seen or row["kind"] == "typed-choice-label"))':
        '        row["initialized_emulator_excerpt_observed"] = ident in seen\n'
        '        row["exact_body_and_name_or_modal_mask_observed"] = ident in pictured',
    '    validate_natural_dialogue_batch(draft)':
        '    one_page = [r["id"] for r in draft["records"] if r["decision"] == "revision"\n'
        '                and bytes.fromhex(r["current_hex"]).count(b"\\n") >= 4]\n'
        '    assert one_page == ["DK4_MES_B55_R0044"]\n'
        '    assert len(revisions[("/data/SC0.DK4", one_page[0])]["pages"]) == 1\n'
        '    draft["one_page_repairs"] = one_page\n'
        '    draft["verified_runtime_name_substitutions"] = painter["native_macro_checks"]\n'
        '    validate_natural_dialogue_batch(draft)',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 906 and len(manifest["checks"]) == 241':
        'len(manifest["batches"]) == 907 and len(manifest["checks"]) == 242',
    "release_stack_before_rafael_north_sea.json": "release_stack_before_rafael_iberian_aftermath.json",
    "release_stack_with_rafael_north_sea.json": "release_stack_with_rafael_iberian_aftermath.json",
    "verified_rafael_first_voyage_debrief_predecessor": "verified_rafael_north_sea_predecessor",
    "rafael_north_sea_release": "rafael_iberian_aftermath_release",
    "registered_rafael_north_sea_and_complete_parent_inverse":
        "registered_rafael_iberian_aftermath_and_complete_parent_inverse",
    "rafael_north_sea_pipeline": "rafael_iberian_aftermath_pipeline",
    "prose_revisions=18": "prose_revisions=25",
    "justified_retentions=94": "justified_retentions=92",
    "text_display_revisions=18, pagination_fixes=0": "text_display_revisions=25, pagination_fixes=1",
    "historical_unchanged_North_Sea_transition_controls=True": "initialized_Sofala_fixture_and_modal_transitions=True",
    "new_story_gameplay=False, hardware=False": "fixture_dependencies_rebound=True, natural_activation=False, hardware=False",
    "previously_localized_records=112": "previously_localized_records=117",
    "verified.PROOF, args.visual_review,": "verified.PROOF, verified.LIVE, args.visual_review,",
    'ledger["rafael_north_sea_20261119"]': 'ledger["rafael_iberian_aftermath_20261119"]',
    "Preserve Rafael North Sea ROM or reconstruction": "Preserve Rafael Sofala ROM, fixture or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael’s Sofala test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Sofala dispute, Emilio’s injury and Uddin’s handover and carries forward the registered North Sea work.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael’s Sofala dispute and adjacent exchanges

The review covers 117 records from the clean Japanese. It records 25 revisions and 92 justified retentions across the summons, Sofala gossip, Fernan’s appointment, the town’s gift, Emilio’s injury and Uddin’s handover. The loss notice specifies whose shares Silveira Company took. Fernan’s reward speech keeps the deduction and its punch line on one page. Emilio’s visitors and Uddin retain their own voices. The established Proof of Conquest and Evergreen Lotus Leaf wording stays intact. [Exact review ledger](../{REVIEW.as_posix()})

All 25 revised pages passed native layout and visual checks. An initialized Sofala fixture ran 24 of the 30 speech commands and verified five revised pages, including the share loss, the separate 3,000-gold panel, Fernan’s nameplate and the original return. The final layout changes affect two other blocks, and the fixture evidence was rebound to exact matching scene and runtime bytes. Unvisited revisions received offline checks. Natural optional-event activation and hardware remain unverified. [Emulator and display evidence](../{VERIFY.as_posix()})

Only six blocks in Rafael’s story archive changed. The clean-input patch reconstructs the ROM byte for byte. Six startup checkpoints, 24 protected name getters and 34 focused tests passed. The candidate retains all 114 accepted layers and the ASCII right-bound correction. The ledger preserves 27,700 credited records and 276 shared keys with open display coverage. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
