"""Register Rafael's departure and debrief with verified original New Game evidence."""

from pathlib import Path
from types import SimpleNamespace

from scripts import audit_rafael_first_voyage_debrief_20261119 as game
from scripts import register_hodram_early_confrontations_20261119 as publisher
from scripts import register_manuel_poem_cross_route_20261119 as parent
from scripts import stage_rafael_first_voyage_debrief_20261119 as stage
from scripts import verify_rafael_first_voyage_debrief_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "rafael-first-voyage-debrief-v1-20261119"
ROOT = Path("out/rafael_first_voyage_debrief_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_Departure_and_Debrief_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_departure_and_debrief_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_first_voyage_debrief_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Rafael’s departure and debrief are registered, with the financing and command exchanges revised and the guided opening replayed from New Game."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(publisher.verification, {
    '    assert not playback["natural_activation"] and not playback["hardware"]':
        '    assert playback["natural_activation"] and not playback["hardware"]',
    '    assert len(path["speeches"]) == 18 and path["exit_frame"] > 0\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 10\n'
    '    assert {r["id"] for r in path["opaque_retained_shouts"]} == offline.OPAQUE\n'
    '    assert playback["tactics_transition"]["revised_pages"] == 1':
        '    assert len(path["speeches"]) == 114 and path["exit_frame"] > 0\n'
        '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 33\n'
        '    shown = {r["id"] for r in path["checked_revisions"]}\n'
        '    assert {f"DK4_MES_B44_R{i:04}" for i in game.REQUIRED} <= shown\n'
        '    assert playback["guided_choice"]["selected"] == 0\n'
        '    assert playback["guided_choice"]["labels"] == ["Ask him.", "Prepare alone."]\n'
        '    assert playback["actual_stock_names"] == offline.STOCK\n'
        '    assert len(painter["native_macro_checks"]) == 5',
    'archives = {"/data/SC1.DK4": native.digest(after["/data/SC1.DK4"])}':
        'archives = {"/data/SC0.DK4": native.digest(after["/data/SC0.DK4"])}',
    'len(stored["groups"]) == 13 and len(commands) == len(draft["records"]) == 177':
        'len(stored["groups"]) == 2 and len(commands) == len(draft["records"]) == 132',
    'len(revisions) == 36 and len(retentions) == 141': 'len(revisions) == 39 and len(retentions) == 93',
    '    seen = set(path["speeches"])':
        '    clean_banks = native.IlnkContainer.parse(clean.read_file("/data/SC0.DK4")).blocks\n'
        '    seen = set(path["speeches"])',
    '        if key not in coverage and row["kind"] == "typed-choice-label":':
        '        if block == 44 and word == 0x4000 and selector == 0:\n'
        '            clean_block = clean_banks[block]\n'
        '            source_at = source["offset"]\n'
        '            assert clean_block[source_at] == 0 and clean_block[:source_at].count(0) == source["record_index"]\n'
        '            # The opening ledger counted through the original zero-valued selector.\n'
        '            row["id"] = f"DK4_MES_B44_R{source[\'record_index\'] + 1:04}"\n'
        '        if key not in coverage and row["kind"] == "typed-choice-label":',
    '        row["initialized_emulator_excerpt_observed"] = ident in seen':
        '        row["ordinary_New_Game_command_observed"] = (ident in seen or\n'
        '            (block == 44 and row["kind"] == "typed-choice-label"))\n'
        '        row["ordinary_New_Game_revised_page_verified"] = ident in shown',
    '    draft["opaque_retention_display"] = painter["opaque_retention_display"]\n'
    '    draft["fresh_retained_proofs"] = {"opaque": [r["id"] for r in path["opaque_retained_shouts"]]}':
        '    for block in (44, 47):\n'
        '        exact_keys = {(r["file_path"], r["id"]) for r in draft["records"] if r["block"] == block}\n'
        '        assert exact_keys == {key for key in coverage if key[0] == "/data/SC0.DK4"\n'
        '                              and key[1].startswith(f"DK4_MES_B{block}_R")}\n'
        '    one_page = [r["id"] for r in draft["records"] if r["decision"] == "revision"\n'
        '                and bytes.fromhex(r["current_hex"]).count(b"\\n") >= 4]\n'
        '    assert one_page == ["DK4_MES_B47_R0053"]\n'
        '    assert len(revisions[("/data/SC0.DK4", one_page[0])]["pages"]) == 1\n'
        '    draft["one_page_repairs"] = one_page\n'
        '    draft["verified_native_name_substitutions"] = painter["native_macro_checks"]',
})

publish = publisher.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 900 and len(manifest["checks"]) == 235':
        'len(manifest["batches"]) == 905 and len(manifest["checks"]) == 240',
    "release_stack_before_hodram_confrontations.json": "release_stack_before_rafael_first_voyage_debrief.json",
    "release_stack_with_hodram_confrontations.json": "release_stack_with_rafael_first_voyage_debrief.json",
    "verified_naturalist_aliases_and_shield_predecessor": "verified_manuel_poem_predecessor",
    "hodram_early_confrontations_release": "rafael_first_voyage_debrief_release",
    "registered_hodram_early_confrontations_and_complete_parent_inverse":
        "registered_rafael_first_voyage_debrief_and_complete_parent_inverse",
    "hodram_early_confrontations_pipeline": "rafael_first_voyage_debrief_pipeline",
    "prose_revisions=36": "prose_revisions=39",
    "justified_retentions=141": "justified_retentions=93",
    "text_display_revisions=36": "text_display_revisions=39",
    "initialized_Hodram_tactics_surname_and_Pasha_excerpts=True":
        "ordinary_Rafael_New_Game_departure_and_guided_preparation=True",
    "natural_activation=False, hardware=False": "natural_activation=True, hardware=False",
    "previously_localized_records=177": "previously_localized_records=132",
    'ledger["hodram_early_confrontations_20261119"]': 'ledger["rafael_first_voyage_debrief_20261119"]',
    ', game.play.FIXTURE,': ',',
    "Preserve Hodram confrontations ROM, fixture or reconstruction": "Preserve Rafael departure and debrief ROM or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael’s departure and debrief test candidate

The [local ROM](../../{ROM.as_posix()}) includes revised early dialogue and carries forward the previous registered candidate.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael’s departure and debrief

Compared 132 records across the departure and debrief from the clean Japanese. The review produced 39 revisions and 93 justified retentions. The loan terms and command responsibilities read as a conversation among the crew, including Julio’s teasing and trust in Rafael. The later warning about Pasha and the Ottoman fleet now fits on one page. The original guided preparation choice, reward and branch commands carry forward. [Exact review ledger](../{REVIEW.as_posix()})

All 39 revised pages passed offline native checks and direct visual review. Five revised records retain the original runtime name substitutions. Revising the last sentence of Julio’s announcement prevents a second period after the default company name. An ordinary Rafael New Game replay exercised 114 departure speech commands and verified {draft["initialized_gameplay"]["revised_pages_verified"]} revised pages, both choice captions, the guided choice and the return to Lisbon with 30,000 gold. The alternate branch and later debrief received offline coverage. Hardware remains unverified. [Display and replay evidence](../{VERIFY.as_posix()})

Only the Rafael story archive changed. The clean-input patch reconstructs the candidate byte for byte. Six startup checks, 24 protected name getters and 34 focused tests passed. This release carries 114 accepted layers and the ASCII right-bound correction. The ledger preserves 27,700 credited records and 276 shared keys with open display coverage. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = publisher.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
