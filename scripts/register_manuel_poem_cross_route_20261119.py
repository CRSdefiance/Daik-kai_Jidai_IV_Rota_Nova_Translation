"""Register the cross-route poem, story reactions and exact clean-input patch."""

from pathlib import Path
from types import SimpleNamespace

from scripts import audit_manuel_poem_cross_route_20261119 as game
from scripts import register_hodram_early_confrontations_20261119 as publisher
from scripts import register_rafael_contract_and_proof_20261119 as parent
from scripts import stage_manuel_poem_cross_route_20261119 as stage
from scripts import verify_manuel_poem_cross_route_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-manuel-poem-v1-20261119"
ROOT = Path("out/manuel_poem_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Manuel_Poem_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_manuel_poem_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_manuel_poem_cross_route_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
CHECKPOINT = "Manuel’s verse now reads consistently across all four routes, with the crew reactions preserved."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(publisher.verification, {
    '    assert len(path["speeches"]) == 18 and path["exit_frame"] > 0\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 10\n'
    '    assert {r["id"] for r in path["opaque_retained_shouts"]} == offline.OPAQUE\n'
    '    assert playback["tactics_transition"]["revised_pages"] == 1':
        '    assert len(path["speeches"]) == 15 and path["exit_frame"] > 0\n'
        '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 8\n'
        '    assert not path["rendered_mismatches"] and playback["each_stanza_advanced_once_by_A"]\n'
        '    assert playback["actual_FI_substitution"] == dict(record="DK4_MES_B11_R0066", name="Lil", exact_visible_glyphs=True)\n'
        '    terminal = base.load(game.play.ROOT / "route2_English/terminal.json")\n'
        '    trace = base.load(terminal["observer"])\n'
        '    conditions = [(r["source"]["instruction_offset"], r["result_words"]) for r in trace["rows"]\n'
        '                  if r["kind"] == "after_command" and r["source"].get("first_word") == 0x8000\n'
        '                  and (r["source"].get("route"), r["source"].get("block")) == (2, 22)]\n'
        '    assert conditions == [(76, [2, 1]), (796, [2, 1])]\n'
        '    assert painter["displayed_native_plans"] == 28',
    'archives = {"/data/SC1.DK4": native.digest(after["/data/SC1.DK4"])}':
        'archives = {f"/data/SC{n}.DK4": native.digest(after[f"/data/SC{n}.DK4"]) for n in range(4)}',
    'len(stored["groups"]) == 13 and len(commands) == len(draft["records"]) == 177':
        'len(stored["groups"]) == 4 and len(commands) == len(draft["records"]) == 60',
    'len(revisions) == 36 and len(retentions) == 141': 'len(revisions) == 24 and len(retentions) == 36',
    'row["initialized_emulator_excerpt_observed"] = ident in seen':
        'row["initialized_emulator_excerpt_observed"] = row["route"] == 2 and ident in seen',
    '    draft["opaque_retention_display"] = painter["opaque_retention_display"]\n'
    '    draft["fresh_retained_proofs"] = {"opaque": [r["id"] for r in path["opaque_retained_shouts"]]}':
        '    variants = [[r for r in draft["records"] if r["source_selector"] == 23 and r["route"] == route]\n'
        '                for route in range(4)]\n'
        '    assert all(tuple(r["english"] for r in entries) == stage.review.VERSE_LINES for entries in variants)\n'
        '    assert all([r["source_hex"] for r in entries] == [r["source_hex"] for r in variants[0]] for entries in variants)\n'
        '    one_page = [r["id"] for r in draft["records"] if r["decision"] == "revision"\n'
        '                and bytes.fromhex(r["current_hex"]).count(b"\\n") >= 4]\n'
        '    assert one_page == ["DK4_MES_B18_R0036"]\n'
        '    draft["same_clean_and_localized_manuel_turns_per_route"] = 6\n'
        '    draft["observed_lil_original_condition_results"] = conditions\n'
        '    draft["one_page_repairs"] = one_page',
})

publish = publisher.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 900 and len(manifest["checks"]) == 235':
        'len(manifest["batches"]) == 904 and len(manifest["checks"]) == 239',
    "release_stack_before_hodram_confrontations.json": "release_stack_before_manuel_poem.json",
    "release_stack_with_hodram_confrontations.json": "release_stack_with_manuel_poem.json",
    "verified_naturalist_aliases_and_shield_predecessor": "verified_rafael_contract_and_proof_predecessor",
    "hodram_early_confrontations_release": "manuel_poem_cross_route_release",
    "registered_hodram_early_confrontations_and_complete_parent_inverse":
        "registered_manuel_poem_cross_route_and_complete_parent_inverse",
    "hodram_early_confrontations_pipeline": "manuel_poem_cross_route_pipeline",
    "changed_components=1": "changed_components=4",
    "prose_revisions=36": "prose_revisions=24",
    "justified_retentions=141": "justified_retentions=36",
    "text_display_revisions=36": "text_display_revisions=24",
    "initialized_Hodram_tactics_surname_and_Pasha_excerpts=True": "initialized_Lil_aftermath_and_name_substitution=True",
    "previously_localized_records=177": "previously_localized_records=60",
    'ledger["hodram_early_confrontations_20261119"]': 'ledger["manuel_poem_cross_route_20261119"]',
    "Preserve Hodram confrontations ROM, fixture or reconstruction": "Preserve four-route poem ROM, fixture or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Manuel’s poem test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised aftermath dialogue on all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte. The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Manuel’s poem across all four routes

Compared all 60 turns in the four aftermath scenes, with 24 revisions and 36 individually justified retentions. The six identical Japanese turns spoken by Manuel now share their English, including all three stanzas. The refrain and the reported resemblance in sound and writing survive. Rafael still wants to set the poem to music. Hodram is surprised by Manuel’s talent. Camille teases Lil about her lack of wonder, and Xien’s exception follows the crew member’s call for a feast. [Exact review ledger](../{REVIEW.as_posix()})

All 24 revised records passed offline native and direct visual checks. Maria’s first stanza fits on one page. The Lil replay exercised all 15 turns and showed eight revised pages, both original conditions, three stanzas with one press of A apiece, the live Lil substitution in Camille’s reply, and the return to port. The fixture started the original aftermath block from Lil’s New Game prelude and kept the original branch conditions. The other routes received offline coverage for this batch. [Replay and display evidence](../{VERIFY.as_posix()})

Only the four story archives changed. The clean-input patch reconstructs the candidate byte for byte. Six startup holds, 24 protected name getters and 34 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger still credits 27,700 records and keeps 276 shared keys open for other consumers. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = publisher.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
