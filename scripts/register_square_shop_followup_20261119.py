"""Register the Square shopkeeper review and its byte-exact clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer

from scripts import audit_square_shop_followup_20261119 as game
from scripts import register_fleet_encounter_dialogue_20261119 as template
from scripts import register_rafael_iberian_aftermath_20261119 as parent
from scripts import stage_square_shop_followup_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-square-shop-followup-v1-20261119"
ROOT = Path("out/square_shop_followup_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Square_Shops_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_square_shop_followup_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_square_shop_followup_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
PENDING = template.PENDING
CHECKPOINT = "The Square shopkeeper’s bulk-trade tip now names Market, with five revised pages and 25 justified retentions."
verified = SimpleNamespace(LIVE=game.PROOF)

def help_facility_references(source, current):
    originals, installed = (IlnkContainer.parse(data).blocks for data in (source, current))
    term = "交易所".encode("cp932")
    assert originals[21].startswith(term) and installed[21].startswith(b"Market\n")
    records = []
    for topic in (119, 148, 191, 194):
        jp, en = originals[topic], installed[topic]
        row = dict(topic=topic, source_offset=jp.index(term), source_term_hex=term.hex(),
                   current_offset=en.index(b"Trade House"), current_term_hex=b"Trade House".hex(),
                   source_block_sha256=native.digest(jp), current_block_sha256=native.digest(en))
        records.append(row)
    return dict(file_path="/COMMON/HELP.DK4", clean_archive_sha256=native.digest(source),
                current_archive_sha256=native.digest(current), active_help_heading=21, followup=records)


verification = checked_text(getsource(template.verify), {
    'stored["parent_sha256"]': 'stored["previous_sha256"]',
    'stored["source_proofs"]': 'stored["evidence"]',
    '    assert playback["original_sequences_initialized"] and not playback["natural_random_selection_verified"] and not playback["hardware"]\n'
    '    assert [r["event"] for r in playback["outcomes"]] == ["dolphins", "sirens", "mermaid"]\n'
    '    assert [len(r["observed"]) for r in playback["outcomes"]] == [3, 2, 2]\n'
    '    assert all(r["selector_restored"] for r in playback["outcomes"])':
        '    assert playback["original_shop_choices_replayed"] and playback["ordinary_input"] and not playback["hardware"]\n'
        '    assert sum(map(len, playback["complete_holds"].values())) == 7 and len(playback["transitions"]) == 2\n'
        '    assert playback["observed_changed_keys"] == [657] and playback["offline_only_changed_keys"] == [683, 693, 696, 705]',
    'stage.workflow.': 'stage.precedent.',
    'prior_review["verified_shared_text_storage"]["sha256"]': 'prior_review["shared_storage_scope"]["evidence_sha256"]',
    '    observed = {x["message_ID"] for a in playback["outcomes"] for x in a["observed"]}\n'
    '    assert observed & set(changed) == {449, 2366}':
        '    observed = {int(n) for n in playback["complete_holds"]}\n'
        '    assert observed & set(changed) == {657}',
    '    assert len(records) == 46 and len(changed) == 10':
        '    assert len(records) == 30 and len(changed) == 5\n'
        '    assert [row["message_ID"] for row in records if row["finding"] == "wrap"] == [683]',
    'row["initialized_emulator_excerpt_observed"]': 'row["ordinary_emulator_excerpt_observed"]',
    '    validate_natural_dialogue_batch(review)':
        '    review["native_facility_caption"] = stored["facility_caption"]\n'
        '    help_path = "/COMMON/HELP.DK4"\n'
        '    review["help_facility_term_followup"] = help_facility_references(clean.read_file(help_path), after[help_path])\n'
        '    validate_natural_dialogue_batch(review)',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 907 and len(manifest["checks"]) == 242':
        'len(manifest["batches"]) == 908 and len(manifest["checks"]) == 243',
    "release_stack_before_rafael_iberian_aftermath.json": "release_stack_before_square_shop_followup.json",
    "release_stack_with_rafael_iberian_aftermath.json": "release_stack_with_square_shop_followup.json",
    "verified_rafael_north_sea_predecessor": "verified_rafael_iberian_aftermath_predecessor",
    "rafael_iberian_aftermath_release": "square_shop_followup_release",
    "registered_rafael_iberian_aftermath_and_complete_parent_inverse":
        "registered_square_shop_followup_and_complete_parent_inverse",
    "rafael_iberian_aftermath_pipeline": "square_shop_followup_pipeline",
    "owned_story_records": "owned_shared_records",
    "story_archive_sha256=archives)": "target_COMMON_sha256=archives[stage.COMMON])",
    "stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review,":
        "stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review,",
    "native_display_sha256=base.digest(verified.PROOF)": "native_display_sha256=base.digest(stage.PROOF)",
    "changed_components=1,": "target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON], changed_components=2,",
    'ARM9_sha256=previous["target_ARM9_sha256"], COMMON_sha256=previous["target_COMMON_sha256"],':
        "ARM9_sha256=archives[stage.ARM], COMMON_sha256=archives[stage.COMMON],",
    "prose_revisions=25, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=92":
        "prose_revisions=4, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=25",
    "text_display_revisions=25, pagination_fixes=1": "text_display_revisions=5, pagination_fixes=0",
    "initialized_Sofala_fixture_and_modal_transitions=True": "ordinary_Amsterdam_Square_shop_choices_and_menu_returns=True",
    "fixture_dependencies_rebound=True, natural_activation=False, hardware=False": "natural_activation=True, hardware=False",
    "previously_localized_records=117": "previously_localized_records=30",
    'ledger["rafael_iberian_aftermath_20261119"]': 'ledger["square_shop_followup_20261119"]',
    "Preserve Rafael Sofala ROM, fixture or reconstruction": "Preserve Square shop ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Square shops test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Square shop dialogue and carries forward the Sofala build.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Square shop replies and briefings

Compared 30 Square records with the clean Japanese, including the retail and bulk-trade replies, the different answers about business, and the region-specific briefings. Four prose revisions align the referral with the original 交易所 building’s English hover label, Market, restore the hearsay in the Spanish briefing, and clarify the former city and empire names and Yi Seong-gye’s title. The epidemic reply keeps its wording and moves the verb next to its subject. The other 25 records have individual retention reasons. [Exact review ledger](../{REVIEW.as_posix()})

All five revised pages passed native and visual checks. The ordinary Amsterdam replay showed seven complete dialogue holds, six Shopkeeper nameplates, and two menu returns. It displayed both complete lines of the revised bulk-trade referral in the Jewelry Shop. The other four revised pages received offline checks. Hardware remains unverified. [Emulator and display evidence](../{VERIFY.as_posix()})

The release changes only the shared text and its directory entries. The original code, four story archives, 114 accepted layers, ASCII right-bound correction and 276 pending shared text payloads and locations carry forward. The clean-input patch reconstructs the ROM byte for byte. Six startup checkpoints, 24 protected name getters and 34 focused tests passed. These records already carried credit, and the ledger stays at 27,700. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

The ledger also identifies four Help topics, 119, 148, 191 and 194, that still say Trade House for the same Japanese term. The original Market Help topic and town caption confirm the wording to use in a separate Help pass. [Exact Help references](../{REVIEW.as_posix()})
""", encoding="utf-8", newline="\\n")
''',
})
env = template.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
