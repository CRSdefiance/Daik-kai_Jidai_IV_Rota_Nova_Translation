"""Register the two regional Square fixes verified in ordinary gameplay."""

from inspect import getsource
from pathlib import Path

from scripts import reconcile_current_route_coverage_20261123 as routes
from scripts import register_hodram_b261_b310_wrap_fixes_20261123 as parent
from scripts import register_square_rumor_followup_20261122 as prior
from scripts import stage_regional_rumor_wrap_followups_20261123 as staged
from scripts import verify_regional_rumor_wrap_followups_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = parent.base, parent.native, prior.workflow
ARM, COMMON = stage.ARM, stage.COMMON
PROFILE = "all-routes-regional-rumor-wrap-followups-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Regional_Rumor_Wrap_Followups_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_regional_rumor_wrap_followups_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_regional_rumor_wrap_followups_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = staged.observed.OUT
CHECKPOINT = "Registered two regional rumors reflowed after ordinary Valencia and Syracuse visits."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(prior.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(stage.PROSE)


def observed_count():
    return sum(r.get("native_mask_exact", False)
               for rows in base.load(live.LIVE)["observed"].values() for r in rows)


def preserved_shared(old, current, candidate):
    worklist = base.load(staged.observed.shared.SOURCE)
    binding = base.load(staged.observed.shared.OUTPUT)
    assert base.digest(staged.observed.shared.SOURCE) == binding["source_worklist_sha256"]
    assert native.digest(old.read_file(ARM)) == binding["ARM9_sha256"]
    assert native.digest(old.read_file(COMMON)) == binding["COMMON_sha256"]
    getter = staged.observed.shared.paired.prior.entries
    before, after = map(getter, (old, current))
    rows = []
    for row in worklist["records"]:
        key = row["message_ID"]
        a, b = before[key], after[key]
        reference = stage.town.reference
        assert a.text == b.text == bytes.fromhex(row["current_hex"])
        assert reference(a) == row["current_reference"]
        rows.append(dict(message_ID=key, before=reference(a), installed=reference(b), exact_body_retained=True))
    assert len(rows) == 276
    return dict(candidate_sha256=candidate, records=rows, all_stored_bodies_preserved=True,
        changed_locations=[row["message_ID"] for row in rows if row["before"] != row["installed"]],
        earlier_binding_sha256=base.digest(staged.observed.shared.OUTPUT), display_ownership_open=True)


verify_source = checked_text(getsource(prior.verify), {
    'assert viewed == visual["sheets"] == stored["sheets"] | played["sheets"]\n'
    '    assert visual["reviewed_candidate_sha256"] == candidate':
        'assert viewed == visual == stored["sheets"] | played["sheets"]',
    'played["revised_offline_only_records"] == [725]': 'not played["revised_offline_only_records"]',
    'stage.relocate.__globals__["TABLE_END"]': 'staged.prior.relocate.__globals__["TABLE_END"]',
    '    for path in hashes:':
        '    shared_binding = preserved_shared(old, target, candidate)\n'
        '    route_coverage = base.load(routes.OUT)\n'
        '    assert route_coverage["candidate_sha256"] == previous["candidate_sha256"]\n'
        '    assert all(first[p] == final[p] for p in routes.ROUTES)\n'
        '    assert stored["ordinary_discovery_sha256"] == base.digest(DISCOVERY)\n'
        '    for path in hashes:',
    'wording_revisions=3,justified_retentions=18': 'wording_revisions=2,justified_retentions=19',
    'historical_source_credit=dict(by_census_id={},direct_keys=0)':
        'shared_consumer_binding=shared_binding,\n'
        '        retained_four_route_census_sha256=base.digest(routes.OUT),\n'
        '        historical_source_credit=dict(by_census_id={},direct_keys=0)',
})

readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(prior.build, {
    'len(batches) == 1052 and len(checks) == 387': 'len(batches) == 1088 and len(checks) == 423',
    'assert not any(p.exists() for p in (ROOT, PACKAGE, DOC, ledger_backup, ledger_next))':
        'assert not any(p.exists() for p in (ROOT, PACKAGE, DOC, registry_backup, registry_next, ledger_backup, ledger_next))',
    'registry_backup = ROOT /': 'registry_backup = WORK /',
    'registry_next = ROOT /': 'registry_next = WORK /',
    'ledger_backup, ledger_next = ROOT / "ledger_before.json", ROOT / "ledger_after.json"':
        'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"',
    '    ROOT.mkdir()': '    ROOT.mkdir()\n    WORK.mkdir()',
    '    copyfile(base.REGISTRY, registry_backup)\n    copyfile(base.LEDGER, ledger_backup)':
        '    link_snapshot(parent.WORK / "release_stack_with_hodram_b261_b310_wrap_fixes.json", registry_backup, snapshot["registry_before"])\n'
        '    link_snapshot(parent.WORK / "ledger_after.json", ledger_backup, snapshot["ledger_before"])',
    'verified_hodram_opening_reply_predecessor': 'verified_hodram_b261_b310_wrap_fixes_predecessor',
    'contextual_decisions_reused=0': 'contextual_decisions_reused=19',
    'prose_revisions=3': 'prose_revisions=2',
    'justified_retentions=18': 'justified_retentions=19',
    'text_display_revisions=3': 'text_display_revisions=2',
    'ordinary_Valencia_and_Syracuse=True, offline_China_rumor=True': 'ordinary_Valencia_and_Syracuse=True',
    'stage.PROOF, STARTUP, QA, live.LIVE, args.visual_review':
        'stage.PROOF, STARTUP, QA, live.LIVE, DISCOVERY, routes.OUT, args.visual_review',
    'checks["registered_square_rumor_followup_and_complete_parent_inverse"] = True':
        'checks["registered_square_rumor_followup_and_complete_parent_inverse"] = True\n    '
        '    assert len(checks) == 424',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Regional Square rumor wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes revised Square rumors in Valencia and Syracuse. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("square_rumor_followup", "regional_rumor_wrap_followups").replace(
    "regional_rumor_wrap_followups_20261122", "regional_rumor_wrap_followups_20261123")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    'registry_backup = ROOT /': 'registry_backup = WORK /',
    'registry_next = ROOT /': 'registry_next = WORK /',
    'ledger_backup, ledger_next = ROOT / "ledger_before.json", ROOT / "ledger_after.json"':
        'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"',
    '"# Current editorial checkpoint - 2026-11-22': '"# Current editorial checkpoint - 2026-11-23',
    'earlier = [stage.ROM]': 'earlier = []',
    'Preserve the Square rumor candidate, predecessor and staged ROM': 'Preserve the regional rumor candidate and its predecessor',
    old_doc:'''    DOC.write_text(f"""# Regional Square rumor wraps

The review covers all 21 regional rumors. Valencia now keeps “they call it the Invincible Armada” on one line. Syracuse keeps “as if they owned it” together and preserves the shopkeeper's figurative comparison. The other 19 decisions retain their wording with individual reasons. [Exact source and installed review](../{REVIEW.as_posix()})

Both revised pages, both Shopkeeper nameplates and the return to the Square passed on ordinary saves. The checked storage changes preserve all four story archives and the 276 pending shared bodies and leave the original Square formatter code intact. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("square_rumor_followup", "regional_rumor_wrap_followups")

scope = prior.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
