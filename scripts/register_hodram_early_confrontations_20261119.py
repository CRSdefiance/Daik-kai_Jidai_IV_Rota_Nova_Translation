"""Register Hodram's early battle exchanges and the verified tactics tutorial."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_hodram_early_confrontations_20261119 as game
from scripts import register_naturalist_aliases_and_shield_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as base_register
from scripts import stage_hodram_early_confrontations_20261119 as stage
from scripts import verify_hodram_early_confrontations_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "hodram-early-confrontations-v1-20261119"
ROOT = Path("out/hodram_early_confrontations_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Hodram_Early_Confrontations_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_hodram_early_confrontations_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hodram_early_confrontations_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Hodram’s early confrontations are registered, including the one-page tactics lesson and Pasha’s ambush."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(getsource(base_register.verify), {
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert len(path["speeches"]) == 18 and path["exit_frame"] > 0\n'
        '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 10\n'
        '    assert {r["id"] for r in path["opaque_retained_shouts"]} == offline.OPAQUE\n'
        '    assert playback["tactics_transition"]["revised_pages"] == 1',
    '    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}':
        '    assert viewed == {s["path"]: s["sha256"] for s in sheets}',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {"/data/SC1.DK4": native.digest(after["/data/SC1.DK4"])}',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 13 and len(commands) == len(draft["records"]) == 177',
    'len(revisions) == 19 and len(retentions) == 176': 'len(revisions) == 36 and len(retentions) == 141',
    '        row["initialized_emulator_excerpt_observed"] = (file_path == "/data/SC0.DK4" and block == 127 and\n'
    '            (ident in seen or row["kind"] == "typed-choice-label"))':
        '        row["initialized_emulator_excerpt_observed"] = ident in seen',
    '    validate_natural_dialogue_batch(draft)':
        '    draft["opaque_retention_display"] = painter["opaque_retention_display"]\n'
        '    draft["fresh_retained_proofs"] = {"opaque": [r["id"] for r in path["opaque_retained_shouts"]]}\n'
        '    validate_natural_dialogue_batch(draft)',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 899 and len(manifest["checks"]) == 234':
        'len(manifest["batches"]) == 900 and len(manifest["checks"]) == 235',
    "release_stack_before_naturalist_aliases_shield.json": "release_stack_before_hodram_confrontations.json",
    "release_stack_with_naturalist_aliases_shield.json": "release_stack_with_hodram_confrontations.json",
    "verified_story_short_phrase_wraps_predecessor": "verified_naturalist_aliases_and_shield_predecessor",
    "naturalist_aliases_and_shield_release": "hodram_early_confrontations_release",
    "registered_naturalist_aliases_and_shield_and_complete_parent_inverse":
        "registered_hodram_early_confrontations_and_complete_parent_inverse",
    "naturalist_aliases_and_shield_pipeline": "hodram_early_confrontations_pipeline",
    "changed_components=4": "changed_components=1",
    "prose_revisions=56, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=173":
        "prose_revisions=36, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=141",
    "text_display_revisions=57, pagination_fixes=0": "text_display_revisions=36, pagination_fixes=1",
    "initialized_Rafael_Athens_scene_and_return=True": "initialized_Hodram_tactics_surname_and_Pasha_excerpts=True",
    "previously_localized_records=230": "previously_localized_records=177",
    'ledger["naturalist_aliases_and_shield_20261119"]': 'ledger["hodram_early_confrontations_20261119"]',
    '                  *(stage.ROOT.parent / "research_v1").rglob("*.nds"),\n'
    '                  *(stage.ROOT.parent / "research_v2").rglob("*.nds")]':
        '                  *(p for directory in stage.ROOT.parent.glob("research_v*") if directory != stage.ROOT\n'
        '                    for p in directory.rglob("*.nds"))]',
    "Preserve naturalist and shield rumor ROM, fixture or reconstruction":
        "Preserve Hodram confrontations ROM, fixture or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram Early Confrontations test candidate

The [local ROM](../../{ROM.as_posix()}) carries the revised tactics lesson, early naval confrontations and Pasha’s ambush.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 {candidate} byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Hodram’s early confrontations

The review covers 177 records in 13 exchanges, with 36 wording revisions and 141 justified retentions. Charles’s tactics lesson keeps both approaches and the full volley together on one page. Hodram answers Pasha’s public execution threat with a direct challenge. Sera and Sirwood’s original opaque cries stay intact. The clean Japanese leaves their words indistinct while making the length and intensity of each cry clear. [Exact review ledger](../{REVIEW.as_posix()})

All 36 revised pages passed native and visual verification. An initialized Hodram replay exercised 18 original speech commands from the tactics lesson, Escante’s greeting and Pasha’s ambush. It verified ten revised pages, both opaque cries, the live surname, one press of A from the complete tactics page into the next line, and the original opening exit. Other revised pages received offline checks. Natural battle activation, encounter effects and hardware remain unverified. [Focused emulator replay](../{(VERIFY / 'hodram_playback_1.png').as_posix()})

Only the Hodram story archive changes. The patch rebuilt the cumulative ROM byte for byte. Six startup checkpoints, 24 protected getters and 34 focused tests passed. The release carries forward all 114 accepted layers and the ASCII right-bound correction. All 177 records already had credit, and the 276 shared entries still have open display coverage. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
