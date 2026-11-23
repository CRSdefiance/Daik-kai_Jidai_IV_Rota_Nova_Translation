"""Register the revised Rafael story and its exact clean-input reconstruction."""

from pathlib import Path
from types import SimpleNamespace

from scripts import audit_rafael_contract_and_proof_20261119 as game
from scripts import register_item_category_labels_20261119 as parent
from scripts import register_hodram_early_confrontations_20261119 as publisher
from scripts import stage_rafael_contract_and_proof_20261119 as stage
from scripts import verify_rafael_contract_and_proof_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "rafael-contract-and-proof-v1-20261119"
ROOT = Path("out/rafael_contract_and_proof_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Rafael_Contract_and_Proof_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_rafael_contract_and_proof_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_contract_and_proof_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT / "supported_qa.xml"
CHECKPOINT = "Rafael’s Ceuta trade contract lesson and four nearby story exchanges have 37 revisions and 92 justified retentions."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)

verification = checked_text(publisher.verification, {
    '    assert len(path["speeches"]) == 18 and path["exit_frame"] > 0\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 10\n'
    '    assert {r["id"] for r in path["opaque_retained_shouts"]} == offline.OPAQUE\n'
    '    assert playback["tactics_transition"]["revised_pages"] == 1':
        '    assert len(path["speeches"]) == 12 and path["exit_frame"] > 0\n'
        '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 4\n'
        '    assert not path["rendered_mismatches"]\n'
        '    assert {r["id"] for r in path["checked_revisions"]} == {\n'
        '        f"DK4_MES_B45_R{n:04}" for n in (29, 33, 37, 58)}',
    'archives = {"/data/SC1.DK4": native.digest(after["/data/SC1.DK4"])}':
        'archives = {"/data/SC0.DK4": native.digest(after["/data/SC0.DK4"])}',
    '    sheets = painter["contact_sheets"] + path["sheets"]':
        '    share = base.load(game.SHARE)\n'
        '    assert share["candidate_sha256"] == candidate and share["prior_complete_bitmap_equal"]\n'
        '    assert share["actual_company"] == "Castor Co." and share["absent_nameplate"]\n'
        '    assert all(base.digest(p) == sha for p, sha in share["evidence"].items())\n'
        '    shot = share["capture"]\n'
        '    sheets = painter["contact_sheets"] + path["sheets"] + [dict(path=shot["path"], sha256=shot["PNG_sha256"])]',
    'len(stored["groups"]) == 13 and len(commands) == len(draft["records"]) == 177':
        'len(stored["groups"]) == 5 and len(commands) == len(draft["records"]) == 129',
    'len(revisions) == 36 and len(retentions) == 141': 'len(revisions) == 37 and len(retentions) == 92',
    '    draft["opaque_retention_display"] = painter["opaque_retention_display"]\n'
    '    draft["fresh_retained_proofs"] = {"opaque": [r["id"] for r in path["opaque_retained_shouts"]]}':
        '    one_page_repairs = {row["id"] for row in draft["records"]\n'
        '                        if row["decision"] == "revision"\n'
        '                        and bytes.fromhex(row["current_hex"]).count(b"\\n") >= 4}\n'
        '    assert one_page_repairs == {"DK4_MES_B25_R0033", "DK4_MES_B41_R0131",\n'
        '                                 "DK4_MES_B86_R0075", "DK4_MES_B120_R0056"}\n'
        '    draft["one_page_repairs"] = sorted(one_page_repairs)\n'
        '    draft["retained_market_share_notice"] = share',
})

publish = publisher.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 900 and len(manifest["checks"]) == 235':
        'len(manifest["batches"]) == 903 and len(manifest["checks"]) == 238',
    "release_stack_before_hodram_confrontations.json": "release_stack_before_rafael_contract_and_proof.json",
    "release_stack_with_hodram_confrontations.json": "release_stack_with_rafael_contract_and_proof.json",
    "verified_naturalist_aliases_and_shield_predecessor": "verified_item_category_labels_predecessor",
    "hodram_early_confrontations_release": "rafael_contract_and_proof_release",
    "registered_hodram_early_confrontations_and_complete_parent_inverse":
        "registered_rafael_contract_and_proof_and_complete_parent_inverse",
    "hodram_early_confrontations_pipeline": "rafael_contract_and_proof_pipeline",
    "prose_revisions=36": "prose_revisions=37",
    "justified_retentions=141": "justified_retentions=92",
    "text_display_revisions=36, pagination_fixes=1": "text_display_revisions=37, pagination_fixes=4",
    "initialized_Hodram_tactics_surname_and_Pasha_excerpts=True": "initialized_Rafael_trade_contract_lesson_and_return=True",
    "previously_localized_records=177": "previously_localized_records=129",
    "(stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review,":
        "(stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, game.SHARE, args.visual_review,",
    'ledger["hodram_early_confrontations_20261119"]': 'ledger["rafael_contract_and_proof_20261119"]',
    "Preserve Hodram confrontations ROM, fixture or reconstruction": "Preserve Rafael story ROM, fixture or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael Contract and Proof test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Ceuta contract lesson, Proof clues, Manuel’s poem at sea and Charles’s recruitment. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte. The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael’s trade contract and Proof dialogue

The five complete exchanges contain 129 decisions, including 37 revisions and 92 justified retentions. Julio explains the Ceuta trading fee and the Palace or Governor’s Office in three complete lines. Four speeches now fit on one page each, including Manuel’s first stanza, Hans’s advice on earning trust, the local’s description of Charles’s factory and the account of the clan’s flight northeast. [Exact review ledger](../{REVIEW.as_posix()})

All 37 revised pages passed native and direct visual checks. The initialized emulator replay exercised all 12 turns of the contract lesson, verified four revised pages and reached the original market return. The retained notice displayed Castor Co. through the original substitution, with 20 percent and the original blank nameplate. The fixture ran the original Ceuta lesson after Rafael’s New Game prelude in Lisbon. The other exchanges received offline checks. [Replay and display evidence](../{VERIFY.as_posix()})

The clean source also places Manuel’s three stanzas in Hodram block 16, Lil block 11 and Maria block 18. Those complete exchanges have a separate follow-up for the shared verse and its route-specific reactions.

Only the Rafael story archive changed. The clean-input patch reconstructs the candidate byte for byte. Six startup holds, 24 protected name getters and 34 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger still credits 27,700 records and keeps 276 shared entries open for other consumers. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = publisher.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
