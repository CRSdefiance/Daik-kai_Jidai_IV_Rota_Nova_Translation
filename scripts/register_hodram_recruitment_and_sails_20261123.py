"""Register the tested recruitment, Proof warning, and sail-lesson candidate."""

from pathlib import Path
from types import FunctionType

from scripts import cleanup_hodram_midroute_followups_20261123 as checkpoint
from scripts import register_hodram_midroute_followups_20261123 as prior
from scripts import replay_hodram_recruitment_and_sails_20261123 as live
from scripts import review_hodram_recruitment_nameplates_20261123 as labels
from scripts import stage_hodram_recruitment_and_sails_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = prior.base, prior.native, stage.parent
PROFILE = "all-routes-hodram-recruitment-and-sails-v1-20261123"
ROOT, WORK = stage.BATCH.parent / "registered", stage.BATCH.parent / "registration"
ROM = ROOT / "Translation_DS_Hodram_Recruitment_And_Sails_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261123_hodram_recruitment_and_sails_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_hodram_recruitment_and_sails_registered_20261123.md")
DISPLAY, EVIDENCE, GLYPHS, FE, CHOICE, ROLES = stage.NATIVE, stage.ROOT, live.GLYPHS, stage.FE_PROOF, live.CHOICES, labels.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Hodram's three recruitment scenes, the Proof warning, Cristina's dance and the sail lesson."
RUNS = ("route1", *live.RUNS)

startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    panels, choices, roles = map(base.load, (FE, CHOICE, ROLES))
    assert all(proof["candidate_sha256"] == candidate for proof in (panels, choices, roles))
    assert panels["original_modal_consumer"] and panels["complete_stored_page_count"] == 4
    assert len(choices["choices"]) == len(played["original_menu_choices"]) == 2
    file_path = "/data/SC1.DK4"
    chapter = banks[file_path].blocks[171]
    archive_hash = base.load(stage.PROOF)["archive_hashes"][file_path]
    reviewed = {row["id"]: row for row in base.load(stage.REVIEW)["retained_choice_labels"]}
    registered = []
    for capture, label in zip(played["original_menu_choices"], choices["choices"], strict=True):
        row = reviewed.pop(label["id"])
        before = row["current_reference"]
        offset = label["offset"]
        command_at = offset - before["offset"] + before["command_offset"]
        raw, body = (bytes.fromhex(before[key]) for key in ("exact_command_hex", "exact_body_hex"))
        assert raw.hex() == label["exact_command_hex"] and chapter[command_at:command_at + len(raw)] == raw
        assert tuple(capture[key] for key in ("block", "slot", "caption")) == (171, label["slot"], label["caption"])
        assert label["caption"] == row["english"] and chapter[offset:offset + len(body) + 1] == body + b"\x00"
        assert capture["original_branch_executed"]
        ref = before | dict(candidate_sha256=candidate, archive_sha256=archive_hash,
            block_sha256=native.digest(chapter), command_offset=command_at, offset=offset)
        registered.append(row | dict(registered_reference=ref, observed_focused=capture,
            review=row["review"] | {"formatting": True}))
    assert not reviewed and choices["stored_tables_exact"]
    by_id = {row["id"]: row for row in records}
    for panel in panels["records"]:
        owner = by_id[panel["id"]]
        ref = owner["registered_reference"]
        assert owner["decision"] == "retention" and owner["observed_focused"]
        assert not panel["second_page"] and panel["exact_command_hex"] == ref["exact_command_hex"]
        assert panel["stored_offset"] == ref["command_offset"]
    assert roles["offline_native_getters_only"] and roles["new_editorial_credit"] == 0
    assert {role["actor_ID"] for role in roles["records"]} == labels.NOTES.keys()
    for role in roles["records"]:
        assert all(role["review"].values()) and role["decision"] == "retention"
        assert all(by_id[ident]["source_selector"] == role["actor_ID"] for ident in role["context_records"])
    return dict(retained_modal_pages=4, retained_choice_labels=registered, retained_supporting_roles=19,
        modal_proof_sha256=base.digest(FE), choice_proof_sha256=base.digest(CHOICE), role_proof_sha256=base.digest(ROLES))


verify_source = checked_text(prior.verify_source, {
    ' + base.load(STYLES)["sheets"]': '',
    'played["initialized_excerpts"] and not played["natural_story_triggers_claimed"] and observed_count() == 47':
        'played["initialized_excerpts"] and played["ordinary_story_evidence"]["original_town_trigger"] and observed_count() == 18',
    'native_count() == 23': 'native_count() == 19',
    '    banks = {p: native.IlnkContainer.parse(b[p]) for p in archives}':
        '    ordinary = {(r["file_path"], r["id"]): r for r in played["ordinary_story_observations"]}\n'
        '    assert len(ordinary) == 9\n'
        '    banks = {p: native.IlnkContainer.parse(b[p]) for p in archives}',
    'observed_focused=observed.pop((path, ident), None)))':
        'observed_focused=observed.pop((path, ident), None), observed_ordinary=ordinary.pop((path, ident), None)))',
    'len(records) == 293': 'not ordinary and len(records) == 194',
    'len(changed) == 25': 'len(changed) == 18',
    'stage.draft.checkpoint.QUEUE': 'checkpoint.QUEUE',
    'wording_revisions=25': 'wording_revisions=18',
    'justified_retentions=268, choice_label_retentions=8': 'justified_retentions=176, choice_label_retentions=2',
})

readme = prior.main[prior.main.index('    (PACKAGE / "README.md").write_text'):prior.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(prior.main, {
    'len(batches) == 1077 and len(checks) == 412': 'len(batches) == 1078 and len(checks) == 413',
    'verified_rafael_midroute_predecessor': 'verified_hodram_midroute_predecessor',
    'previously_localized_records=306, contextual_records_revisited=306, contextual_decisions_reused=0':
        'previously_localized_records=196, contextual_records_revisited=196, contextual_decisions_reused=44',
    'prior_records_reviewed=306, contextual_decisions_reused=0': 'prior_records_reviewed=196, contextual_decisions_reused=44',
    'prose_revisions=25': 'prose_revisions=18',
    'justified_retentions=268, retained_choice_labels=8, retained_style_variants=5':
        'justified_retentions=176, retained_choice_labels=2, retained_style_variants=0',
    'retained_modal_pages=8, revised_modal_pages=2, native_choice_outcomes=8, natural_story_activation=False':
        'retained_modal_pages=4, revised_modal_pages=0, native_choice_outcomes=2, natural_story_activation=True, ordinary_story_holds=9',
    'FE, CHOICE, ROLES, STYLES': 'FE, CHOICE, ROLES',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram recruitment and sail lesson

The [testing ROM](../../{ROM.as_posix()}) includes the refreshed exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_midroute_followups", "hodram_recruitment_and_sails")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    'stage.BATCH.parent / "first_staging" / "staged"': 'stage.BATCH.parent / "staged"',
    'Preserve Hodram midroute testing and prototype ROMs, predecessor and focused ROMs':
        'Preserve Hodram recruitment and sail testing, prototype, predecessor and focused ROMs',
    old_doc:'''    DOC.write_text(f"""# Hodram's recruitment scenes and sail lesson

The source review covers 196 texts in six complete exchanges. Eighteen revisions address eight queued wraps, five breaks observed during Angelo's recruitment and the priest's spoken warning. The ledger also records 176 retentions and both sail-lesson captions. [Exact review](../{REVIEW.as_posix()})

All 19 changed progressive layouts, both original choices, four speakerless panels and 19 speaker names or role labels passed their native checks. Normal Istanbul gameplay verified nine revised Angelo panels. The focused runs exercised both sail-lesson decisions and the other revised exchanges. Julio's optional recruitment line was checked offline. Handheld testing remains open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_midroute_followups", "hodram_recruitment_and_sails")

scope = prior.scope | globals() | {name: parent.scope[name]
                                  for name in ("guard_spec", "bind_registered_story_percent_guard")}
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
