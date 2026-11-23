"""Register Hodram's reviewed exchanges, original menus, and modal panels."""

from pathlib import Path
from types import FunctionType

from scripts import register_rafael_fleet_and_crew_exchanges_20261122 as prior
from scripts import replay_hodram_early_and_midroute_wraps_20261122 as live
from scripts import stage_hodram_early_and_midroute_wraps_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
parent = stage.active
PROFILE = "all-routes-hodram-early-and-midroute-wraps-v1-20261122"
ROOT = prior.ROOT.with_name("hodram_early_and_midroute_wraps_registered_20261122")
WORK = stage.BATCH.parent / "registration"
ROM = ROOT / "Translation_DS_Hodram_Early_And_Midroute_Wraps_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261122_hodram_early_and_midroute_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_hodram_early_and_midroute_wraps_registered_20261122.md")
DISPLAY, EVIDENCE, GLYPHS, FE, CHOICE = stage.NATIVE, stage.ROOT, live.GLYPHS, stage.FE_PROOF, stage.CHOICE_PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 18 early and midroute Hodram exchanges, including Janus's offer and the sailor's miracle question."
RUNS = ("route1", *live.RUNS)
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    modal, choice = map(base.load, (FE, CHOICE))
    assert candidate == modal["candidate_sha256"] == choice["candidate_sha256"]
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 20
    assert choice["original_choice_consumer"] and choice["both_branches_observed"]
    panels = {r["id"]:r for r in modal["records"]}
    owners = {r["id"]:r for r in records if r["source_selector"] == 254}
    assert panels.keys() == owners.keys()
    for ident, owner in owners.items():
        panel, installed = panels[ident], owner["registered_reference"]
        assert not panel["second_page"] and owner["decision"] == "retention"
        assert panel["stored_offset"] == installed["command_offset"]
        assert panel["exact_command_hex"] == installed["exact_command_hex"] == owner["current_reference"]["exact_command_hex"]
    adjusted = {ident for ident, r in panels.items() if r["maximum_name"] is not None}
    assert adjusted == {"DK4_MES_B91_R0084", "DK4_MES_B91_R0103"}
    assert all(owners[ident]["observed_focused"] for ident in adjusted)

    options = played["original_menu_choices"]
    assert len(options) == len(choice["captions"]) == 4
    assert all(r["original_branch_executed"] for r in options)
    by_key = {(r["block"], r["selected"]):r for r in options}
    originals = banks["/data/SC1.DK4"].blocks
    for row in choice["captions"]:
        cur = row["registered_reference"]
        block, slot = cur["block"], row["slot"]
        payload = originals[block]
        at = cur["command_offset"]
        raw = bytes.fromhex(cur["exact_command_hex"])
        assert all(row["review"].values()) and row["decision"] == "retention"
        assert cur["block_sha256"] == native.digest(payload) and payload[at:at + len(raw)] == raw
        assert by_key[block, slot]["caption"] == row["english"]
        assert by_key[block, slot]["response"] == live.prior.record_id(block, live.RESPONSES[block][slot])
    return dict(modal_proof_sha256=base.digest(FE), retained_modal_pages=len(owners),
                choice_proof_sha256=base.digest(CHOICE), retained_choice_labels=choice["captions"],
                branch_outcomes=options)


verify_source = checked_text(prior.verify_source, {
    'observed_count() == 25': 'observed_count() == 36',
    'native_count() == 15': 'native_count() == 24',
    'archives = {"/data/SC0.DK4"}': 'archives = {"/data/SC1.DK4"}',
    'len(records) == 224': 'len(records) == 278',
    'len(changed) == 12': 'len(changed) == 24',
    'retained_roles_and_modal_panels=retained_roles_and_panels(records, candidate),':
        'retained_native_controls=retained_controls(records, played, banks, candidate),',
    'wording_revisions=12, wrap_only_revisions=0': 'wording_revisions=24, wrap_only_revisions=0',
    'justified_retentions=212, choice_label_retentions=0': 'justified_retentions=254, choice_label_retentions=4',
})

readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(prior.build, {
    "len(batches) == 1074 and len(checks) == 409": "len(batches) == 1075 and len(checks) == 410",
    "previously_localized_records=224, contextual_records_revisited=224": "previously_localized_records=282, contextual_records_revisited=282",
    "prior_records_reviewed=224": "prior_records_reviewed=282",
    "justified_retentions=212, retained_choice_labels=0": "justified_retentions=254, retained_choice_labels=4",
    "prose_revisions=12": "prose_revisions=24",
    "focused_initialized_Rafael=True, default_substitution_panels=3, retained_modal_pages=4, supporting_roles=9":
        "focused_initialized_Hodram=True, default_substitution_panels=2, retained_modal_pages=20, native_choice_outcomes=4",
    "verified_charlotte_east_asia_predecessor": "verified_fleet_and_crew_predecessor",
    "stage.REVIEW, FE, ROLES": "stage.REVIEW, FE, CHOICE",
    "DISPLAY, GLYPHS, FE, ROLES, args.visual_review,": "DISPLAY, GLYPHS, FE, CHOICE, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram's early and midroute exchanges

The [testing ROM](../../{ROM.as_posix()}) carries 24 dialogue revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_fleet_and_crew_exchanges", "hodram_early_and_midroute_wraps")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    '    earlier = [Path(base.load(live.scope["receipt"](0))["rom"])]':
        '    earlier = [live.route_rom(1), *(live.choice_paths(block)[1] for block in live.PROMPTS)]\n'
        '    reviewed_draft = stage.BATCH.parent / "release" / "staged"\n'
        '    draft_proof = base.load(reviewed_draft / stage.PROOF.name)\n'
        '    original_draft = reviewed_draft / stage.ROM.name\n'
        '    assert base.digest(original_draft) == draft_proof["candidate_sha256"] != candidate\n'
        '    assert draft_proof["whole_parent_inverse"]\n'
        '    earlier.append(original_draft)\n'
        '    for path in (live.route_rom(1), *(live.choice_paths(block)[1] for block in live.PROMPTS)):\n'
        '        draft_fixture = reviewed_draft / path.relative_to(stage.ROOT)\n'
        '        assert draft_fixture.is_file()\n'
        '        earlier.append(draft_fixture)',
    "Preserve the Rafael fleet and crew candidate, predecessor and focused ROM":
        "Preserve the Hodram early and midroute candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Hodram's early and midroute exchanges

The clean-Japanese review covers 282 texts in 18 complete exchanges. Twenty-four revisions address flagged wraps, 254 spoken or system texts have individual retention reasons, and four original choice labels retain their wording and slots. The dialogue keeps Janus's 1,000-gold request, the sailor's contrasting outcomes, and Gerhard's account of the lost Katzbalger. [Exact review](../{REVIEW.as_posix()})

All 24 revised pages and 20 retained system panels passed native layout checks. Two extra maximum-name cases verify the Luck and Spirit notices. Focused emulator gameplay verified 36 displayed holds, both choices in each original menu, and the return to port. Ordinary activation of the story scenes and handheld display remain unverified. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_fleet_and_crew_exchanges", "hodram_early_and_midroute_wraps")

scope = prior.scope | globals() | {
    name: parent.scope[name] for name in ("guard_spec", "bind_registered_story_percent_guard")
}
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
