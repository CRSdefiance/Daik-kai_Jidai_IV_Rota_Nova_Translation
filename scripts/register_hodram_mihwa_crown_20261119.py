"""Register the Golden Crown exchange over the exact story Market candidate."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_hodram_mihwa_crown_20261119 as game
from scripts import register_story_market_terms_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as template
from scripts import stage_hodram_mihwa_crown_20261119 as stage
from scripts import verify_hodram_mihwa_crown_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-hodram-mihwa-crown-v1-20261119"
ROOT = Path("out/hodram_mihwa_crown_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Hodram_Crown_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_hodram_mihwa_crown_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hodram_mihwa_crown_20261119.md")
STARTUP, QA = game.play.STARTUP_PROOF, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Hodram’s Silla Gold Crown exchange now uses the names shown on Mihwa’s nameplate and the item card."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(getsource(template.verify), {
    '    path, = playback["paths"]\n'
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert playback["initialized_fixture"] and playback["normal_return_result"][0] == 0\n'
        '    assert len(playback["speeches"]) == 18 and playback["revised_pages_verified"] == 7',
    'sheets = painter["contact_sheets"] + path["sheets"]': 'sheets = painter["contact_sheets"] + playback["sheets"]',
    '    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}':
        '    assert viewed == {s["path"]: s["sha256"] for s in sheets}',
    '[34, 0, 0, 0]': '[22, 0, 0, 0]',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {"/data/SC1.DK4": native.digest(after["/data/SC1.DK4"])}\n'
        '    assert b"Meihua" not in after["/data/SC1.DK4"]',
    '    assert prior["shared_storage_scope"]["pending_records"] == 276':
        '    assert prior["shared_storage_scope"]["pending_records"] == 276\n'
        '    binding = base.load(stage.review.BINDINGS)\n'
        '    assert binding["scene_name_consistency_findings"] == 1 and binding["current_installed_name"] == "Mihwa"\n'
        '    item = base.load(stage.review.ROOT / "silla_crown_item_binding.json")\n'
        '    assert item["candidate_sha256"] == candidate and item["all_sixty_literal_Japanese_mentions_accounted_for"]\n'
        '    assert item["item_ID"] == 137 and item["installed_name_mentions"] == 52\n'
        '    actors = base.load(stage.review.NAMES)\n'
        '    assert actors["whole_original_getter_execution"] and len(actors["records"]) == 207\n'
        '    assert actors["runtime"]["ARM9_sha256"] == previous["target_ARM9_sha256"]\n'
        '    assert base.digest(stage.review.NAMES) == binding["current_getter_evidence_sha256"]',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 1 and len(commands) == len(draft["records"]) == 18',
    'len(revisions) == 19 and len(retentions) == 176': 'len(revisions) == 7 and len(retentions) == 11',
    'seen = set(path["speeches"])': 'seen = set(playback["speeches"])',
    'file_path == "/data/SC0.DK4" and block == 127': 'file_path == "/data/SC1.DK4" and block == 89',
    'shared_storage_scope=prior["shared_storage_scope"])':
        'shared_storage_scope=prior["shared_storage_scope"], localized_name_evidence=binding, item_name_evidence=item)',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 910 and len(manifest["checks"]) == 245':
        'len(manifest["batches"]) == 911 and len(manifest["checks"]) == 246',
    "verified_help_market_terms_predecessor": "verified_story_market_terms_predecessor",
    "story_market_terms": "hodram_mihwa_crown",
    "stage.review.SOURCE, stage.review.OUTPUT, stage.review.ROOT / \"city_alias_storage_recheck.json\"":
        "stage.review.SOURCE, stage.review.OUTPUT, stage.review.BINDINGS, stage.review.NAMES, stage.review.ROOT / \"actor_field_storage_current.json\", stage.review.ROOT / \"silla_crown_item_binding.json\"",
    "changed_components=3": "changed_components=1",
    "prose_revisions=34, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=168":
        "prose_revisions=7, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=11",
    "text_display_revisions=34": "text_display_revisions=7",
    "name_consistency_revisions=0": "name_consistency_revisions=4",
    "initialized_Lisbon_trade_lesson_and_market_share_choice=True": "initialized_complete_Hodram_crown_exchange=True",
    "previously_localized_records=202": "previously_localized_records=18",
    "Preserve story Market ROM or reconstruction": "Preserve Crown dialogue ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Hodram’s Golden Crown dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the Mihwa correction, the Silla Gold Crown name and the surrounding dialogue revisions.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Mihwa in Hodram’s Golden Crown exchange

Reviewed all 18 records in the exchange from the clean Japanese. Julian is embarrassed to face Mihwa after Hodram finds the Silla Gold Crown first. His request now uses the same name as both of the bartender’s original name getters and the other direct story references. The first emulator replay exposed a second inconsistency. Three speeches now match the Silla Gold Crown label on the item card. The source-to-current scan confirms 52 uses of that English name and eight justified short references to the same crown. The other revisions sharpen Hodram’s admiration, Julian’s disappointment and Hodram’s generous reply. Eleven retained lines keep their original controls, wording and individual reasons. [Review and exact name references](../{REVIEW.as_posix()})

All seven revised pages passed complete native glyph, wrap, bounds and visual checks. An initialized Hodram replay observed all 18 speech commands, matched all seven revised pages and nameplates, and reached the original return. Natural activation and physical hardware remain unverified. [Emulator playback](../{VERIFY.as_posix()}/crown_playback_1.png)

The clean-input patch reconstructs the ROM byte for byte. Only SC1 block 89 changes. Help, shared text, the actor table, the ASCII right-bound correction and all 114 accepted layers carry forward. Six startup frames, 24 protected name getters and 22 focused tests passed. Review credit remains 27,700, with 276 entries open for shared display classification. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = template.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
