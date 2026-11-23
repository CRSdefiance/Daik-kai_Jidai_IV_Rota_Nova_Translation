"""Register Rafael's Proof of Conquest briefing and complete Lisbon financing review."""

from pathlib import Path
from types import FunctionType

from scripts import observe_rafael_proof_financing_opening_20261122 as ordinary
from scripts import register_rafael_athens_and_maria_crew_20261122 as parent
from scripts import replay_rafael_proof_and_financing_20261122 as live
from scripts import stage_rafael_proof_and_financing_20261122 as stage
from scripts import verify_rafael_proof_and_financing_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
PROFILE = "all-routes-rafael-proof-and-financing-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_proof_and_financing_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_Proof_And_Lisbon_Financing_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_proof_and_financing_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_proof_and_financing_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS, FE, CHOICE = display.GLYPH_PROOF, stage.FE_PROOF, stage.CHOICE_PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
EARLIER_CHOICE = Path("translations/editorial_checkpoints/SharedText_20261110_v1/rafael_harbor_exchange_20261121_v2.json")
CHECKPOINT = "Registered Rafael's Proof briefing and Lisbon financing and preparation exchange."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def retained_controls(records, played, candidate, bank):
    modal, choice = map(base.load, (FE, CHOICE))
    assert modal["candidate_sha256"] == choice["candidate_sha256"] == candidate
    assert modal["original_modal_consumer"]
    panel, = [r for r in records if r["id"] == modal["owner"]]
    assert panel["source_selector"] == 254 and panel["decision"] == "retention"
    assert panel["current_reference"]["exact_command_hex"] == panel["registered_reference"]["exact_command_hex"] == modal["exact_command_hex"]
    assert panel["registered_reference"]["command_offset"] == modal["stored_offset"]
    assert choice["native_provider_sha256"] == base.digest(display.MENU_PROOF)
    old = [r for r in base.load(EARLIER_CHOICE)["records"] if r["kind"] == "typed-choice-label"]
    assert len(old) == len(choice["captions"]) == 2
    for prior, retained in zip(old, choice["captions"], strict=True):
        s, r = retained["source_reference"], retained["registered_reference"]
        assert prior["source_reference"]["offset"] == s["offset"] and prior["source_hex"] == s["exact_body_hex"]
        body = bytes.fromhex(r["exact_body_hex"])
        assert r["block_sha256"] == native.digest(bank) and bank[r["offset"]:r["offset"]+len(body)] == body
        assert all(retained["review"].values())
        retained["historical_credit_id"] = prior["id"]
    menu = played["original_menu_choices"]
    expected = [("Ask him.", "DK4_MES_B44_R0464"), ("Prepare alone.", "DK4_MES_B44_R0479")]
    assert [(r["caption"], r["response"]) for r in menu] == expected
    assert all(r["original_branch_executed"] for r in menu)
    return dict(gold_notice=panel["registered_reference"], original_choice=choice, focused_choices=menu)


def ordinary_opening(candidate):
    proof = base.load(ordinary.OUTPUT)
    assert proof["candidate_sha256"] == candidate and proof["ordinary_new_game"] and not proof["synthetic_fixture"]
    assert proof["report_sha256"] == base.digest(ordinary.REPORT)
    assert proof["observations"]
    assert all(base.digest(row["capture"]["path"]) == row["capture"]["PNG_sha256"] for row in proof["observations"])
    return proof


def historical_credit(records):
    earlier = [r for r in base.load(EARLIER_CHOICE)["records"] if r["kind"] != "typed-choice-label"]
    by_offset = {r["source_reference"]["offset"]: r for r in earlier}
    assert len(by_offset) == len(earlier) == 115
    aliases = {}
    for record in (r for r in records if r["block"] == 44):
        source = record["source_reference"]
        prior = by_offset.pop(source["offset"])
        ref = prior["source_reference"]
        assert (ref["archive_sha256"], ref["block_sha256"]) == (source["archive_sha256"], source["block_sha256"])
        assert ref["command_offset"] == source["command_offset"]
        assert prior["source_hex"] == record["source_hex"] and prior["source_selector"] == record["source_selector"]
        if prior["id"] != record["id"]:
            assert record["source_selector"] == 0
            assert int(prior["id"][-4:]) == int(record["id"][-4:]) + 1
            aliases[record["id"]] = prior["id"]
    assert aliases and not by_offset and len(set(aliases.values())) == len(aliases)
    return dict(by_census_id=aliases, direct_keys=len(records)-len(aliases),
                exact_older_review_sha256=base.digest(EARLIER_CHOICE))


verify_source = checked_text(parent.verify_source, {
    'checked["sheets"] + base.load(FE)["sheets"] + played["sheets"]':
        'checked["sheets"] + base.load(FE)["sheets"] + base.load(CHOICE)["sheets"] + played["sheets"] + ordinary_opening(candidate)["sheets"]',
    'observed_count() == 29': 'observed_count() == 21',
    'played["report_sha256"] == {str(r):base.digest(live.report_path(r)) for r in live.SAMPLE}':
        'played["report_sha256"] == {run:base.digest(live.report(run)) for run in live.RUNS}',
    'native_count() == 21': 'native_count() == 17',
    'archives = {"/data/SC0.DK4", "/data/SC3.DK4"}': 'archives = {"/data/SC0.DK4"}',
    'for r in played["observations"] if r["page"] == 1': 'for r in played["observations"]',
    'len(records) == 132': 'len(records) == 142',
    'len(changed) == 19': 'len(changed) == 16',
    'assert sum(r["change_class"] == "wrap_only" for r in changed) == 1':
        'assert all(r["change_class"] == "prose" for r in changed)',
    'retained_modal_pages=retained_modal(records, candidate),':
        'retained_native_controls=retained_controls(records, played, candidate, banks["/data/SC0.DK4"].blocks[44]),\n'
        '        ordinary_lisbon_opening=ordinary_opening(candidate),',
    'wording_revisions=18, wrap_only_revisions=1': 'wording_revisions=16, wrap_only_revisions=0',
    'justified_retentions=113': 'justified_retentions=126, choice_label_retentions=2',
    'historical_source_credit=dict(by_census_id={}, direct_keys=0)':
        'historical_source_credit=historical_credit(records)',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1069 and len(checks) == 404": "len(batches) == 1070 and len(checks) == 405",
    "previously_localized_records=132, contextual_records_revisited=132": "previously_localized_records=144, contextual_records_revisited=144",
    "prior_records_reviewed=132": "prior_records_reviewed=144",
    "justified_retentions=113, retained_choice_labels=0": "justified_retentions=126, retained_choice_labels=2",
    "prose_revisions=18": "prose_revisions=16",
    "wrap_only_revisions=1": "wrap_only_revisions=0",
    "changed_components=2": "changed_components=1",
    "focused_initialized_Rafael_and_Maria=True, retained_modal_pages=10":
        "focused_initialized_Rafael=True, retained_modal_pages=1, original_preparation_branches=2, ordinary_Lisbon_opening=True",
    "verified_hodram_reconciliation_predecessor": "verified_rafael_athens_predecessor",
    "stage.maria.OUTPUT, FE": "stage.paired.OUTPUT, FE, CHOICE, display.MENU_PROOF, ordinary.OUTPUT",
    "DISPLAY, GLYPHS, FE, args.visual_review,": "DISPLAY, GLYPHS, FE, CHOICE, display.MENU_PROOF, ordinary.OUTPUT, args.visual_review,",
    '        pending = value(data, "pending_shared_consumer_checkpoint_20261114", 1)':
        '        assert all(("/data/SC0.DK4", row["historical_credit_id"]) in credited\n'
        '                   for row in draft["retained_native_controls"]["original_choice"]["captions"])\n'
        '        pending = value(data, "pending_shared_consumer_checkpoint_20261114", 1)',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's Proof briefing and Lisbon financing

The [testing ROM](../../{ROM.as_posix()}) carries 16 wording revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_athens_and_maria_crew", "rafael_proof_and_financing")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'earlier = [Path(base.load(live.receipt(r))["rom"]) for r in live.SAMPLE] + [TRIAL]':
        'earlier = [Path(base.load(live.ROOT / kind / "fixture.json")["rom"]) for kind in ("speech", "choice")]',
    "Preserve the Rafael and Maria candidate, predecessor, retained trial and focused ROMs":
        "Preserve the Rafael financing candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael's Proof briefing and Lisbon financing

The clean-source pass covers 142 spoken and system texts and both original preparation captions. It revises 16 lines and records 126 individual text retentions and two caption retentions. Hans distinguishes his theory about the ruins from the strengths the crew thinks a ruler must have. The loan terms and the original 30,000 gold notice are preserved. Janus states both ways to prepare for sailing in two complete lines. [Coverage ledger](../{REVIEW.as_posix()})

All 17 revised native variants passed the font and bounds checks. Focused controller replays verified 21 dialogue or modal holds and both original choice responses. Selecting Ask him leads to Julio's directions to the Market. Selecting Prepare alone opens his independent reply. Ordinary New Game play reached the opening of the Lisbon exchange. Natural activation of the Proof briefing, the preparation menu in ordinary play, and handheld display remain unvisited on this candidate. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_athens_and_maria_crew", "rafael_proof_and_financing")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
