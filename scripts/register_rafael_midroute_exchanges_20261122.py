"""Register the cumulatively verified Rafael midroute candidate."""

from pathlib import Path
from types import FunctionType

from scripts import register_hodram_early_and_midroute_wraps_20261122 as prior
from scripts import replay_rafael_midroute_exchanges_20261122 as live
from scripts import review_rafael_midroute_nameplates_20261122 as labels
from scripts import stage_rafael_midroute_exchanges_20261122 as stage
from scripts import verify_rafael_midroute_exchanges_20261122 as checked
from scripts.source_locked_derivation_v5118 import checked_text

base, native = prior.base, prior.native
parent = stage.active
PROFILE = "all-routes-rafael-midroute-exchanges-v1-20261122"
ROOT = prior.ROOT.with_name("rafael_midroute_exchanges_registered_20261122")
WORK = stage.BATCH.parent / "registration"
ROM = ROOT / "Translation_DS_Rafael_Midroute_Exchanges_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261122_rafael_midroute_exchanges_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_rafael_midroute_exchanges_registered_20261122.md")
DISPLAY, EVIDENCE = stage.NATIVE, stage.ROOT
GLYPHS, FE, CHOICE, ROLES = checked.GLYPHS, stage.FE_PROOF, checked.CHOICES, labels.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 14 Rafael midroute exchanges, including Julio's sailing lesson and the Colosseum riddle."
RUNS = ("0", *live.RUNS)
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    modal, choices, roles = map(base.load, (FE, CHOICE, ROLES))
    assert modal["candidate_sha256"] == choices["candidate_sha256"] == roles["candidate_sha256"] == candidate
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 17
    assert choices["stored_tables_exact"]
    panels = {r["id"]: r for r in modal["records"]}
    owners = {r["id"]: r for r in records if r["source_selector"] == 254}
    assert panels.keys() == owners.keys()
    for ident, panel in panels.items():
        row = owners[ident]
        installed = row["registered_reference"]
        assert installed["exact_command_hex"] == panel["exact_command_hex"]
        assert installed["command_offset"] == panel["stored_offset"]
        assert panel["changed"] == (row["decision"] == "revision")
        if panel["changed"]:
            assert row["observed_focused"] and ident == "DK4_MES_B118_R0125"
        else:
            assert installed["exact_command_hex"] == row["current_reference"]["exact_command_hex"]

    manuscript = base.load(stage.REVIEW)
    reviewed = {r["id"]: r for r in manuscript["retained_choice_labels"]}
    routes = {(r["block"], r["slot"]): r for r in played["original_menu_choices"]}
    assert len(routes) == len(choices["choices"]) == 5
    file_path = "/data/SC0.DK4"
    archive = banks[file_path]
    archive_hash = native.digest(base.NdsImage.open(stage.ROM).read_file(file_path))
    registered_choices = []
    for choice in choices["choices"]:
        row = reviewed.pop(choice["id"])
        block, offset, slot = (choice[k] for k in ("block", "offset", "slot"))
        outcome = routes.pop((block, slot))
        assert outcome["original_branch_executed"] and outcome["caption"] == choice["caption"] == row["english"]
        before = row["current_reference"]
        command_at = offset - before["offset"] + before["command_offset"]
        raw = bytes.fromhex(choice["exact_command_hex"])
        assert raw.hex() == before["exact_command_hex"] and archive.blocks[block][command_at:command_at + len(raw)] == raw
        ref = dict(file_path=file_path, block=block, candidate_sha256=candidate, archive_sha256=archive_hash,
            block_sha256=native.digest(archive.blocks[block]), command_offset=command_at, offset=offset,
            exact_command_hex=raw.hex(), exact_body_hex=before["exact_body_hex"])
        registered_choices.append(row | dict(registered_reference=ref,
            review=row["review"] | {"formatting": True}, observed_focused=outcome))
    assert not routes and not reviewed
    assert roles["offline_native_getters_only"] and roles["new_editorial_credit"] == 0
    assert {row["actor_ID"] for row in roles["records"]} == labels.NOTES.keys()
    assert all(all(row["review"].values()) for row in roles["records"])
    return dict(modal_proof_sha256=base.digest(FE), retained_modal_pages=16, revised_modal_pages=1,
        choice_proof_sha256=base.digest(CHOICE), retained_choice_labels=registered_choices,
        role_proof_sha256=base.digest(ROLES), retained_roles=len(roles["records"]))


verify_source = checked_text(prior.verify_source, {
    'observed_count() == 36': 'observed_count() == 50',
    'native_count() == 24': 'native_count() == 32',
    'archives = {"/data/SC1.DK4"}': 'archives = {"/data/SC0.DK4"}',
    'bool(display and display["layouts"])': 'bool(display and (display["layouts"] or display.get("modal_consumer")))',
    'len(records) == 278': 'len(records) == 275',
    'len(changed) == 24': 'len(changed) == 31',
    'assert all(r["change_class"] == "prose" for r in changed)':
        'assert sum(r["change_class"] == "prose" for r in changed) == 30\n'
        '    assert [r["id"] for r in changed if r["change_class"] == "wrap_only"] == ["DK4_MES_B118_R0125"]',
    'wording_revisions=24, wrap_only_revisions=0': 'wording_revisions=30, wrap_only_revisions=1',
    'justified_retentions=254, choice_label_retentions=4': 'justified_retentions=244, choice_label_retentions=5',
    '        full_editorial_goal_complete=False, hardware=False)':
        '        speaker_roles_sha256=base.digest(ROLES), full_editorial_goal_complete=False, hardware=False)',
})

readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(prior.build, {
    'registry_backup = ROOT /': 'registry_backup = WORK /',
    'assert set(ROOT.iterdir()) == {registry_backup} and not registry_backup.is_symlink()':
        'assert not any(ROOT.iterdir()) and not registry_backup.is_symlink()',
    "len(batches) == 1075 and len(checks) == 410": "len(batches) == 1076 and len(checks) == 411",
    "previously_localized_records=282, contextual_records_revisited=282":
        "previously_localized_records=280, contextual_records_revisited=280",
    "prior_records_reviewed=282": "prior_records_reviewed=280",
    "justified_retentions=254, retained_choice_labels=4": "justified_retentions=244, retained_choice_labels=5",
    "prose_revisions=24": "prose_revisions=30",
    "wrap_only_revisions=0": "wrap_only_revisions=1",
    "focused_initialized_Hodram=True, default_substitution_panels=2, retained_modal_pages=20, native_choice_outcomes=4":
        "focused_initialized_Rafael=True, default_substitution_panels=2, retained_modal_pages=16, revised_modal_pages=1, native_choice_outcomes=5",
    "verified_fleet_and_crew_predecessor": "verified_hodram_early_and_midroute_predecessor",
    "(live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE)":
        "(live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE, ROLES)",
    "DISPLAY, GLYPHS, FE, CHOICE, args.visual_review,":
        "DISPLAY, GLYPHS, FE, CHOICE, ROLES, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's midroute exchanges

The [testing ROM](../../{ROM.as_posix()}) includes Rafael's revised dialogue and the reflowed Colosseum award. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_early_and_midroute_wraps", "rafael_midroute_exchanges")

pins_start = prior.commit.index("    earlier = ")
pins_end = prior.commit.index("    research = ")
old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    'registry_backup = ROOT /': 'registry_backup = WORK /',
    prior.commit[pins_start:pins_end]:'''    excerpt_rom = Path(base.load(live.excerpt_scope["receipt"](0))["rom"])
    earlier = [excerpt_rom, *(live.choice_paths(block)[1] for block in live.PROMPTS)]
''',
    "Preserve the Hodram early and midroute candidate, predecessor and focused ROMs":
        "Preserve the Rafael midroute candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael's midroute exchanges

The clean-Japanese review covers 280 texts across 14 complete exchanges. Thirty prose changes and one modal reflow address 21 flagged wraps and related issues. The ledger records 244 individual dialogue and panel retentions, five choice labels and the exact fields for 15 names and roles. [Exact review](../{REVIEW.as_posix()})

Thirty-two progressive display cases and all 17 modal panels passed native layout checks. Focused emulator gameplay verified 50 displays, both original menus and all five outcomes. Ordinary activation of the story scenes and handheld display remain unverified. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_early_and_midroute_wraps", "rafael_midroute_exchanges")

scope = prior.scope | globals() | {
    name: parent.scope[name] for name in ("guard_spec", "bind_registered_story_percent_guard")
}
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
