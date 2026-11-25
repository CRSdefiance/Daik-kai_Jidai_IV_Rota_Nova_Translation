"""Register the four Hodram and Lil exchanges and their display proofs."""

from pathlib import Path
from types import FunctionType

from scripts import register_rafael_six_followup_exchanges_20261122 as prior
from scripts import replay_hodram_and_lil_followups_20261122 as live
from scripts import stage_hodram_and_lil_followups_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
parent = stage.paired.active
PROFILE = "all-routes-hodram-and-lil-followups-v1-20261122"
ROOT = prior.ROOT.with_name("hodram_and_lil_followups_registered_20261122")
WORK = Path(".codex-release-work/hodram_and_lil_followups_20261122")
ROM = ROOT / "Translation_DS_Hodram_And_Lil_Followups_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261122_hodram_and_lil_followups_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_hodram_and_lil_followups_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
GLYPHS, FE, CHOICE = live.GLYPHS, stage.FE_PROOF, stage.CHOICE_PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
EARLIER_CAPTIONS = Path("translations/lil_B131_B133_contextual_final_review_v1.json")
CHECKPOINT = "Registered Hodram's Aziza and Cristina exchanges and Lil's Clifford and Rafael exchanges."
RUNS = ("route1", "route2", *live.BRANCHES)
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    modal, choice = map(base.load, (FE, CHOICE))
    assert modal["candidate_sha256"] == choice["candidate_sha256"] == candidate
    assert modal["original_modal_consumer"] and choice["original_choice_consumer"]
    assert modal["complete_stored_page_count"] == len(modal["records"]) == 4
    assert all(not r["second_page"] for r in modal["records"])
    original = {(r["route"], r["id"]): r for r in modal["records"]}
    owners = {(r["route"], r["id"]): r for r in records if r["source_selector"] == 254}
    assert original.keys() == owners.keys()
    for key, row in owners.items():
        panel, ref = original[key], row["registered_reference"]
        assert row["decision"] == "retention"
        assert ref["command_offset"] == panel["stored_offset"]
        assert ref["exact_command_hex"] == panel["exact_command_hex"] == row["current_reference"]["exact_command_hex"]

    bank = banks["/data/SC2.DK4"].blocks[133]
    prior_captions = [r for r in base.load(EARLIER_CAPTIONS)["records"] if r["kind"] == "typed-choice-label"]
    assert len(prior_captions) == len(choice["captions"]) == 2
    for slot, (old, row) in enumerate(zip(prior_captions, choice["captions"], strict=True)):
        source, ref = row["source_reference"], row["registered_reference"]
        assert old["source_hex"] == source["exact_body_hex"]
        assert source["offset"] == old["source_reference"]["offset"]
        assert old["id"] == f'DK4_CHOICE_B133_C{source["command_offset"]}_O{slot}'
        assert row["english"] == old["english"] and all(row["review"].values())
        body = bytes.fromhex(ref["exact_body_hex"])
        assert ref["block_sha256"] == native.digest(bank) and bank[ref["offset"]:ref["offset"]+len(body)] == body
        assert ref["exact_command_hex"] == choice["exact_retained_choice_object"]
        row["earlier_typed_choice_evidence_id"] = old["id"]
    options = played["original_menu_choices"]
    assert choice["both_branches_observed"]
    assert [(r["caption"], r["response"]) for r in options] == [
        ("Hmm... fine, then.", "DK4_MES_B133_R0164"), ("Are you nuts?", "DK4_MES_B133_R0194")]
    assert all(r["original_branch_executed"] for r in options)
    return dict(retained_modal_records=list(original.values()), original_choice=choice, focused_choices=options,
        earlier_choice_review=dict(path=str(EARLIER_CAPTIONS), sha256=base.digest(EARLIER_CAPTIONS)))


verify_source = checked_text(prior.verify_source, {
    'observed_count() == 19': 'observed_count() == 30',
    'played["report_sha256"] == {"0":base.digest(REPORT)}':
        'played["report_sha256"] == {run:base.digest(live.report(run)) for run in RUNS}',
    'native_count() == 17': 'native_count() == 18',
    'archives = {"/data/SC0.DK4"}': 'archives = {"/data/SC1.DK4", "/data/SC2.DK4"}',
    'len(records) == 129': 'len(records) == 288',
    'len(changed) == 16': 'len(changed) == 18',
    'retained_modal_notices=retained_modal(records, candidate),':
        'retained_native_controls=retained_controls(records, played, banks, candidate),',
    'wording_revisions=16, wrap_only_revisions=0': 'wording_revisions=18, wrap_only_revisions=0',
    'justified_retentions=113, historical_source_credit=':
        'justified_retentions=270, choice_label_retentions=2, historical_source_credit=',
})

readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(prior.build, {
    'registry_next = ROOT / "release_stack_with_rafael_six_followup_exchanges.json"':
        'registry_next = WORK / "release_stack_with_rafael_six_followup_exchanges.json"',
    'ledger_backup, ledger_next = ROOT / "ledger_before.json", ROOT / "ledger_after.json"':
        'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"',
    '    assert not any(p.exists() for p in (ROOT, PACKAGE, DOC, ledger_backup, ledger_next))':
        '    assert not any(p.exists() for p in (DOC, registry_next, ledger_backup, ledger_next))\n'
        '    if ROOT.exists() or PACKAGE.exists():\n'
        '        assert set(ROOT.iterdir()) == {registry_backup} and not registry_backup.is_symlink()\n'
        '        assert base.digest(registry_backup) == snapshot["registry_before"]\n'
        '        assert set(PACKAGE.iterdir()) == {VERIFY} and not any(VERIFY.iterdir())',
    '    ROOT.mkdir()\n    VERIFY.mkdir(parents=True)\n    copyfile(base.REGISTRY, registry_backup)':
        '    WORK.mkdir(parents=True, exist_ok=True)\n    ROOT.mkdir(exist_ok=True)\n'
        '    VERIFY.mkdir(parents=True, exist_ok=True)\n'
        '    if not registry_backup.exists():\n        copyfile(base.REGISTRY, registry_backup)',
    "len(batches) == 1071 and len(checks) == 406": "len(batches) == 1072 and len(checks) == 407",
    "previously_localized_records=129, contextual_records_revisited=129": "previously_localized_records=290, contextual_records_revisited=290",
    "prior_records_reviewed=129": "prior_records_reviewed=290",
    "justified_retentions=113, retained_choice_labels=0": "justified_retentions=270, retained_choice_labels=2",
    "prose_revisions=16": "prose_revisions=18",
    "changed_components=1": "changed_components=2",
    "focused_initialized_Rafael=True, retained_modal_pages=3":
        "focused_initialized_Hodram_and_Lil=True, retained_modal_pages=4, original_Lil_branches=2",
    "verified_rafael_lisbon_predecessor": "verified_rafael_followup_predecessor",
    "stage.REVIEW, FE": "stage.REVIEW, FE, CHOICE",
    "DISPLAY, GLYPHS, FE, args.visual_review,": "DISPLAY, GLYPHS, FE, CHOICE, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram and Lil follow-up exchanges

The [testing ROM](../../{ROM.as_posix()}) carries 18 wording revisions and keeps both original Lil choices. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_six_followup_exchanges", "hodram_and_lil_followups")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    'registry_next = ROOT / "release_stack_with_rafael_six_followup_exchanges.json"':
        'registry_next = WORK / "release_stack_with_rafael_six_followup_exchanges.json"',
    'ledger_backup, ledger_next = ROOT / "ledger_before.json", ROOT / "ledger_after.json"':
        'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"',
    'earlier = [Path(base.load(live.scope["receipt"](0))["rom"])]':
        'earlier = [live.route_rom(1), live.route_rom(2), live.CHOICE_ROM]\n'
        '    draft_stage = stage.BATCH.parent / "staged"\n'
        '    draft_fixtures = draft_stage / "focused_gameplay"\n'
        '    earlier.extend(path for path in (draft_stage / stage.ROM.name,\n'
        '        *(draft_fixtures / f"route{route}" / live.route_rom(route).name for route in (1, 2)),\n'
        '        draft_fixtures / "choice" / live.CHOICE_ROM.name) if path.is_file())',
    "Preserve the Rafael follow-up candidate, predecessor and focused ROM":
        "Preserve the Hodram and Lil candidate, predecessor and focused ROM",
    old_doc:'''    DOC.write_text(f"""# Hodram and Lil follow-up exchanges

The clean-Japanese pass covers 288 spoken and system texts and both Lil choice captions. Eighteen passages changed and 270 texts and two captions have individual retention reasons. Hodram's scenes preserve Aziza's account of her father's pirates and Cristina's response to the recruitment offer. Lil's scenes preserve the gossip about Clifford, the awkward dinner, and the separate responses to Rafael's Nantes and Lisbon trade. [Exact review](../{REVIEW.as_posix()})

All 18 revised pages passed exact glyph and line checks. Focused emulator checks verified 30 dialogue and notice holds, the original choice highlighting and both responses. The four story triggers and handheld display remain unvisited on this candidate. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_six_followup_exchanges", "hodram_and_lil_followups")

scope = prior.scope | globals() | {
    name: parent.scope[name] for name in ("guard_spec", "bind_registered_story_percent_guard")
}
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
