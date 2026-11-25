"""Register the source-reviewed first-voyage lesson and its cumulative patch."""

from inspect import getsource
from pathlib import Path

from scripts import register_rafael_deck_lesson_20261119 as workflow
from scripts import stage_rafael_first_voyage_20261119 as stage
from scripts import verify_rafael_first_voyage_20261119 as verified
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
parent = workflow
PROFILE = "all-routes-rafael-first-voyage-v1-20261119"
ROOT = Path("out/rafael_first_voyage_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_First_Voyage_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_first_voyage_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_first_voyage_20261119.md")
STARTUP, QA = verified.STARTUP, stage.ROOT / "supported_qa.xml"
PRIOR_WRAP = Path("releases/all_routes_editorial_20261111_rafael_early_wraps_candidate/verification/registered_review.json")
CHECKPOINT = "Rafael's first-voyage lesson has 21 revised turns and seven exact retentions, including a one-page supply warning."


def retained_review(row, older, evidence):
    ident = row["id"]
    path = PRIOR_WRAP if ident in ("DK4_MES_B42_R0026", "DK4_MES_B42_R0036") else workflow.PRIOR
    if path == PRIOR_WRAP:
        older, = (r for r in base.load(path)["records"] if r["id"] == ident)
        stored = older["registered_reference"]["raw_hex"]
    else:
        stored = older["planned_integrated_reference"]["exact_stored_hex"]
    assert all(older["review"].values()) and older["source_hex"] == row["source_hex"]
    assert stored == row["current_hex"] == evidence["exact_stored_hex"]
    return dict(path=path.as_posix(), sha256=base.digest(path), id=ident)


verification = checked_text(getsource(workflow.verify), {
    'len(game["holds"]) == 9': 'len(game["holds"]) == 10',
    '{SC0: [43]}': '{SC0: [42]}',
    'if a != b] == [43]': 'if a != b] == [42]',
    '    parent.verify_runtime(arm, previous)': '    workflow.parent.verify_runtime(arm, previous)',
    '    assert shared["candidate_sha256"] == queue["candidate_sha256"] == previous["candidate_sha256"]':
        '''    prior_review = base.load(parent.REVIEW)
    assert prior_review["candidate_sha256"] == previous["candidate_sha256"]
    assert shared["candidate_sha256"] == queue["candidate_sha256"] == base.load(workflow.parent.RELEASE)["candidate_sha256"]
    assert prior_review["verified_shared_text_storage"]["sha256"] == base.digest(SHARED)
    assert prior_review["verified_prior_wrap_queue"]["sha256"] == base.digest(WRAP_QUEUE)''',
    'r["block"] == 43 for r in queue["records"]': 'r["block"] == 42 for r in queue["records"]',
    'if r["block"] == 43': 'if r["block"] == 42',
    '== len(prior_rows) == 12': '== len(prior_rows) == 28',
    '["DK4_MES_B43_R0030"]': '["DK4_MES_B42_R0019"]',
    'new_blocks[43]': 'new_blocks[42]',
    'block=43': 'block=42',
    '''            older = prior_rows[ident]
            assert older["source_hex"] == row["source_hex"] and all(older["review"].values())
            assert older["planned_integrated_reference"]["exact_stored_hex"] == row["current_hex"] == evidence["exact_stored_hex"]
            row["retained_display_review"] = dict(path=PRIOR.as_posix(), sha256=base.digest(PRIOR), id=ident)''':
        '            row["retained_display_review"] = retained_review(row, prior_rows[ident], evidence)',
    '            assert ident in observed and evidence["page"]["native_independent_plane_equal"]':
        '            assert all(x["page"]["native_independent_plane_equal"] for x in evidence["layouts"])',
    'The original painter and replay show the complete revised English on one page.':
        'The original painter verifies the complete revised English on one page.',
    'sum(r["decision"] == "revision" for r in draft["records"]) == 7':
        '''sum(r["decision"] == "revision" for r in draft["records"]) == 21
    assert sum(r["decision"] == "revision" and r["id"] in observed for r in draft["records"]) == 8
    macro = checked["DK4_MES_B42_R0080"]
    assert len(macro["layouts"]) == 4 and "DK4_MES_B42_R0080" in observed''',
    'original_queue_records_outside_SC0_B43=True': 'original_queue_records_outside_SC0_B42_and_B43=True',
})
publish = workflow.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 891 and len(manifest["checks"]) == 226':
        'len(manifest["batches"]) == 892 and len(manifest["checks"]) == 227',
    "release_stack_before_rafael_deck_lesson.json": "release_stack_before_rafael_first_voyage.json",
    "release_stack_with_rafael_deck_lesson.json": "release_stack_with_rafael_first_voyage.json",
    "verified_save_location_labels_predecessor": "verified_rafael_deck_lesson_predecessor",
    "rafael_deck_lesson_release": "rafael_first_voyage_release",
    "registered_rafael_deck_lesson_and_complete_parent_inverse": "registered_rafael_first_voyage_and_complete_parent_inverse",
    "rafael_deck_lesson_pipeline": "rafael_first_voyage_pipeline",
    "prose_revisions=7, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=5":
        "prose_revisions=21, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7",
    "text_display_revisions=7": "text_display_revisions=21",
    "initialized_Rafael_deck_lesson_excerpt=True": "initialized_Rafael_first_voyage_excerpt=True",
    "previously_localized_records=12": "previously_localized_records=28",
    'ledger["rafael_deck_lesson_20261119"]': 'ledger["rafael_first_voyage_20261119"]',
    "Preserve Rafael Deck lesson ROM, excerpt or clean reconstruction":
        "Preserve Rafael first-voyage ROM, excerpt or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael first-voyage test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised first-voyage dialogue and the previous cumulative fixes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's first voyage

Reviewed all 28 turns from the clean Japanese. Julio explains how to resupply at the Port when money is short and what declining the offer lets you adjust. The supply warning fits on one page. Clau's pirate boast and Janus's teasing give way to Julio's practical advice on ports, recruiting and trade. Rafael still takes Julio's reminder about the money seriously before Julio laughs it off. The review records 21 revisions and seven exact retentions. [Exact review](../{REVIEW.as_posix()})

All 21 revised pages and three additional name-width samples passed native rendering and direct visual review. An initialized Rafael excerpt displayed ten pages, including the full supply warning, the game's own Rafael substitution and Julio's reassurance after Rafael promises to repay him. Thirteen revised lines received offline checks only. Natural scene activation and hardware remain unverified. [Native pages](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Emulator excerpt](../{(VERIFY / 'rafael_live_1.png').as_posix()})

Only Rafael's first-voyage block changes. The clean-input patch reconstructs the candidate byte for byte. It preserves the Deck lesson, all 114 accepted layers and the ASCII right-bound correction. Six startup holds, 24 protected getters and 34 focused tests passed. The ledger stays at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = workflow.env | globals()
exec(compile(verification, __file__ + "::first-voyage-proof", "exec"), env)
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
