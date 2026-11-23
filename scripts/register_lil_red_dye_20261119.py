"""Register Lil's connected Red Dye exchanges on the cumulative item-titles build."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_lil_red_dye_20261119 as game
from scripts import register_current_item_story_terms_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as template
from scripts import stage_lil_red_dye_20261119 as stage
from scripts import verify_lil_red_dye_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-lil-red-dye-v1-20261119"
ROOT = Path("out/lil_red_dye_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Lil_Red_Dye_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_lil_red_dye_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_lil_red_dye_20261119.md")
STARTUP, QA = game.play.STARTUP_PROOF, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
TITLE = stage.review.ROOT / "title_consistency.json"
CHECKPOINT = "Lil’s alliance and Amsterdam exchanges now use Red Dye consistently with the inventory."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(getsource(template.verify), {
    '    path, = playback["paths"]\n'
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert playback["initialized_fixture"] and playback["normal_return_result"][0] == 0\n'
        '    assert len(playback["speeches"]) == 26 and playback["revised_pages_verified"] == 2',
    'sheets = painter["contact_sheets"] + path["sheets"]': 'sheets = painter["contact_sheets"] + playback["sheets"]',
    '    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}':
        '    assert viewed == {s["path"]: s["sha256"] for s in sheets}',
    '[34, 0, 0, 0]': '[22, 0, 0, 0]',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {"/data/SC2.DK4": native.digest(after["/data/SC2.DK4"])}',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 4 and len(commands) == len(draft["records"]) == 87',
    'len(revisions) == 19 and len(retentions) == 176':
        'len(revisions) == 7 and len(retentions) == 80\n'
        '    item = base.load(TITLE)\n'
        '    assert item["candidate_sha256"] == candidate and item["exact_clean_and_current_literal_counts"] == 8',
    'seen = set(path["speeches"])': 'seen = set(playback["speeches"])',
    'file_path == "/data/SC0.DK4" and block == 127': 'file_path == "/data/SC2.DK4" and block == 129',
    'shared_storage_scope=prior["shared_storage_scope"])':
        'shared_storage_scope=prior["shared_storage_scope"], item_title_review=item)',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
evidence = publish[publish.index("    for source in ("):publish.index("                   *(Path(p) for p in base.load(args.visual_review))):")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 912 and len(manifest["checks"]) == 247':
        'len(manifest["batches"]) == 913 and len(manifest["checks"]) == 248',
    "verified_hodram_mihwa_crown_predecessor": "verified_story_item_titles_predecessor",
    "story_item_titles": "lil_red_dye",
    evidence: "    for source in (stage.PROOF, stage.review.SOURCE, stage.review.OUTPUT, TITLE, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review,\n",
    "changed_components=2": "changed_components=1",
    "prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=71":
        "prose_revisions=7, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=80",
    "text_display_revisions=12": "text_display_revisions=7",
    "name_consistency_revisions=10": "name_consistency_revisions=3",
    "initialized_complete_Rafael_glassmaking_exchange=True": "initialized_complete_Lil_amsterdam_conversation=True",
    "previously_localized_records=83": "previously_localized_records=87",
    "Preserve story item title ROM or reconstruction": "Preserve Red Dye ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Lil’s Red Dye candidate

The [local ROM](../../{ROM.as_posix()}) includes the alliance, Amsterdam and Old Parchment dialogue revisions.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Lil’s Red Dye exchanges

Reread 87 records in four linked exchanges from the clean Japanese, with seven revisions and 80 justified retentions. Clifford’s offer and directions and Lil’s first reaction in Amsterdam now use Red Dye. The barkeep recognizes her after reading Clifford’s letter, and Lil describes pouring the dye onto the Old Parchment. The alliance terms and the researcher’s polder conversation keep their original wording. [Exact review](../{REVIEW.as_posix()})

All eight direct source mentions use the inventory title across the current story archives. The seven revised pages passed native glyph, wrap, bounds and visual checks. An initialized emulator replay observed 26 Amsterdam speeches and matched both revised pages, their nameplates and the original return. The unselected reply and the other three exchanges received offline checks. Natural event activation and hardware remain unverified. [Emulator replay](../{VERIFY.as_posix()}/amsterdam_playback_1.png) · [Title evidence](../{VERIFY.as_posix()}/title_consistency.json)

The clean-input patch reconstructs the ROM byte for byte. Only the four reviewed SC2 blocks change. Help, shared text, the ASCII right-bound correction and all 114 accepted layers carry forward. Six startup holds, 24 protected name getters and 22 focused tests passed. The ledger still credits 27,700 reviews, with 276 shared entries open for display classification. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = template.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
