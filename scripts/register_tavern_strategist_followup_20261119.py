"""Register the revised Tavern dialogue and its exact clean-input patch."""

from pathlib import Path
from types import SimpleNamespace

from scripts import audit_tavern_strategist_followup_20261119 as game
from scripts import register_hodram_early_confrontations_20261119 as parent
from scripts import register_market_followup_20261119 as publisher
from scripts import stage_tavern_strategist_followup_20261119 as stage
from scripts import verify_tavern_strategist_followup_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native, PENDING = stage.base, stage.native, stage.PENDING
PROFILE = "all-routes-tavern-strategist-followup-v1-20261119"
ROOT = Path("out/tavern_strategist_followup_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Tavern_Strategist_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_tavern_strategist_followup_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_tavern_strategist_followup_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
CHECKPOINT = "The Tavern and Strategist follow-up is registered with 15 revisions, 91 retentions and verified London menu returns."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(publisher.verification, {
    "stored, playback, boot = map(base.load, (stage.PROOF, game.PROOF, STARTUP))":
        "stored, playback, boot, painter = map(base.load, (stage.PROOF, game.PROOF, STARTUP, offline.PROOF))",
    '== playback["candidate_sha256"] == boot["candidate_sha256"]':
        '== playback["candidate_sha256"] == boot["candidate_sha256"] == painter["candidate_sha256"]',
    'stored["parent_sha256"]': 'stored["previous_sha256"]',
    'assert all(base.digest(p) == sha for p, sha in stored["source_proofs"].items())':
        'assert all(base.digest(p) == sha for p, sha in stored["prior_evidence"].items())\n'
        '    assert base.digest(stage.review.OUTPUT) == stored["manuscript_sha256"]\n'
        '    assert base.digest(stage.PROOF) == painter["stage_proof_sha256"]\n'
        '    assert painter["native_layout_cases"] == 20532 and painter["original_catalogue_sizes"] == [20, 114, 4]\n'
        '    assert painter["retained_template_count"] == 91 and painter["unchanged_source_arguments"]\n'
        '    assert all(preview["independent_full_plane_exact"] for r in painter["revisions"]\n'
        '               for preview in r["representative_previews"])',
    '    assert playback["original_sequences_initialized"] and not playback["natural_random_selection_verified"] and not playback["hardware"]\n'
    '    assert [r["event"] for r in playback["outcomes"]] == ["market_recommendation"]\n'
    '    assert [len(r["observed"]) for r in playback["outcomes"]] == [3]\n'
    '    assert all(r["original_return_screen_matches"] for r in playback["outcomes"])':
        '    assert not playback["natural_eligibility"] and not playback["hardware"]\n'
        '    assert len(playback["holds"]) == 9 and all(r["complete_body_mask"] for r in playback["holds"])\n'
        '    assert playback["same_tavern_menu_after_cancellation"] == [18000, 24000, 30400]\n'
        '    assert list(playback["cash_at_each_cancellation"].values()) == [40644] * 4\n'
        '    assert playback["terminal_town"]["frame"] == 31200',
    'stored["sheets"] + playback["sheets"]': 'painter["contact_sheets"] + playback["sheets"]',
    "list(stage.EDITS)": "list(stage.review.EDITS)",
    'observed = {x["message_ID"] for a in playback["outcomes"] for x in a["observed"]}':
        'observed = {x["message_ID"] for x in playback["holds"]}',
    'assert observed & set(changed) == {775}':
        'assert observed & set(changed) == set(playback["revised_IDs"]) == {909, 915, 927, 941, 957}\n'
        '    display_checks = {r["message_ID"]: r for r in painter["revisions"]}\n'
        '    assert display_checks.keys() == set(changed)',
    'len(records) == 22 and len(changed) == 4': 'len(records) == 106 and len(changed) == 15',
    '        assert (ident in changed) == (row["decision"] == "revision")':
        '        assert (ident in changed) == (row["decision"] == "revision")\n'
        '        assert stage.workflow.reference(original[ident]) == row["source_reference"]\n'
        '        assert stage.workflow.reference(old_entries[ident]) == row["current_reference"]\n'
        '        assert stage.workflow.reference(entries[ident]) == row["staged_reference"]\n'
        '        assert old_entries[ident].text.hex() == row["current_hex"]\n'
        '        assert stage.workflow.logical(entries[ident].text) == row["english"]\n'
        '        if ident in display_checks:\n'
        '            check = display_checks[ident]\n'
        '            assert check["template_hex"] == row["staged_hex"]\n'
        '            row["native_display_cases"] = check["tested_cases"]\n'
        '            row["stock_names_wrapping_between_words"] = len(check["wrap_advisories"])\n'
        '        else:\n'
        '            assert row["current_hex"] == row["staged_hex"] and row["review"]["formatting"]\n'
        '            row["retained_formatting_dependency_sha256"] = stored["prior_evidence"][stage.review.PRIOR.as_posix()]',
    'source_and_native_dependency_proofs=stored["source_proofs"], observed_gameplay=playback,':
        'source_and_native_dependency_proofs=stored["prior_evidence"], observed_gameplay=playback,\n'
        '        native_display_sha256=base.digest(offline.PROOF), native_display_cases=painter["native_layout_cases"],\n'
        '        stock_names_wrapping_between_words=sum(len(r["wrap_advisories"]) for r in painter["revisions"]),',
})

publish = publisher.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 897 and len(manifest["checks"]) == 232':
        'len(manifest["batches"]) == 901 and len(manifest["checks"]) == 236',
    '    stored, draft, archives = verify(registry, previous, base.load(args.visual_review))':
        '    assert "tavern_strategist_followup_20261119" not in ledger\n'
        '    assert "registered_tavern_strategist_followup_and_complete_parent_inverse" not in manifest["checks"]\n'
        '    stored, draft, archives = verify(registry, previous, base.load(args.visual_review))',
    "release_stack_before_market_followup.json": "release_stack_before_tavern_strategist_followup.json",
    "release_stack_with_market_followup.json": "release_stack_with_tavern_strategist_followup.json",
    "verified_battle_dialogue_followup_predecessor": "verified_hodram_early_confrontations_predecessor",
    "market_followup_release": "tavern_strategist_followup_release",
    "registered_market_followup_and_complete_parent_inverse": "registered_tavern_strategist_followup_and_complete_parent_inverse",
    "market_followup_pipeline": "tavern_strategist_followup_pipeline",
    "(stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review,": "(stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review,",
    "prose_revisions=4": "prose_revisions=15",
    "justified_retentions=18": "justified_retentions=91",
    "text_display_revisions=4": "text_display_revisions=15",
    "initialized_Market_recommendation_and_return=True": "initialized_London_Schemes_and_cancellations=True",
    "previously_localized_records=22": "previously_localized_records=106",
    'ledger["market_followup_20261119"]': 'ledger["tavern_strategist_followup_20261119"]',
    'candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates = [ROM, stage.ROM, stage.ROOT / "clean_rebuilt.nds",\n'
        '                  *(p for directory in stage.ROOT.parent.glob("research_v*") if directory != stage.ROOT\n'
        '                    for p in directory.rglob("*.nds"))]',
    "Preserve Market follow-up ROM or clean reconstruction": "Preserve Tavern follow-up ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tavern and Strategist test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Tavern recruitment and Schemes exchanges alongside the prior cumulative fixes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte. The candidate is available for acceptance testing. Hardware verification remains open.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Tavern and Strategist follow-up

Reviewed all 106 records in COMMON 883–988 in their recruitment, town-rumor and Schemes exchanges. Fifteen revisions restore or clarify gold costs, tighten questions, and carry the faction owning the fleet and the destination through all eight voices. The 91 retained lines preserve the confirmations, results, rumors and the different speakers' reactions. [Exact review ledger](../{REVIEW.as_posix()})

All {draft['native_display_cases']:,} native formatting cases passed. Direct visual review covered all 15 revised templates with representative and width-bound pages. Across the stock substitutions, {draft['stock_names_wrapping_between_words']:,} layouts still wrap a multiword town name at an ordinary word boundary. Every word and glyph remains present within bounds. [Native formatting evidence](../{(VERIFY / verified.PROOF.name).as_posix()})

A focused London replay on the candidate rendered five revised records and two retained confirmations. Lure Fleet, Forge Papers and Bad Rumors all returned to the same Tavern menu when cancelled. Funds reflected two drinks and zero scheme charges. The final screen was the London town menu. The replay used a copied save with bounded qualification inputs. Natural qualification, scheme success and hardware remain unverified. [London replay, part one](../{(VERIFY / 'london_schemes_replay_1.png').as_posix()}) and [part two](../{(VERIFY / 'london_schemes_replay_2.png').as_posix()})

The exact clean-input patch preserves the 114 accepted layers and the ASCII right-bound correction. Six startup holds, 24 protected getters and 34 focused tests passed. The 106 records already held credit, and the count remains 27,700. All 276 open shared payloads and locations match the previous candidate byte for byte. The new build awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = publisher.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
