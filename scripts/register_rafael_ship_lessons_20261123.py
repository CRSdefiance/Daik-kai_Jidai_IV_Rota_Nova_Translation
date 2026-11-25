"""Register Rafael's recruitment and ship lessons after the complete release checks."""

from pathlib import Path
from types import FunctionType

from scripts import register_rafael_basra_and_map_keys_20261123 as parent
from scripts import stage_rafael_ship_lessons_20261123 as stage
from scripts import verify_rafael_ship_lessons_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-rafael-recruitment-and-ship-lessons-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Rafael_Recruitment_And_Ship_Lessons_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_rafael_ship_lessons_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_ship_lessons_registered_20261123.md")
DISPLAY, EVIDENCE = stage.NATIVE, stage.ROOT
GLYPHS, FE, CHOICE, ROLES = live.GLYPHS, stage.FE_PROOF, live.CHOICES, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's recruitment scenes and ship lessons."
RUNS = ("0",)
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
guard_spec = parent.guard_spec
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())


def observed_count():
    return len(base.load(live.LIVE)["observations"])


def retained_controls(records, played, banks, candidate):
    modal, choices, roles = map(base.load, (FE, CHOICE, ROLES))
    assert modal["candidate_sha256"] == choices["candidate_sha256"] == roles["candidate_sha256"] == candidate
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 1
    assert choices["stored_tables_exact"] and len(choices["choices"]) == 8
    panel, = modal["records"]
    row, = [row for row in records if row["source_selector"] == 254]
    installed = row["registered_reference"]
    assert panel["id"] == row["id"] == "DK4_MES_B177_R0114" and row["decision"] == "retention"
    assert installed["exact_command_hex"] == panel["exact_command_hex"] == row["current_reference"]["exact_command_hex"]
    assert installed["command_offset"] == panel["stored_offset"] and not panel["second_page"]
    assert row["observed_focused"]["reused_exact_stored_command_and_runtime"]

    reviewed = {row["id"]: row for row in base.load(stage.REVIEW)["retained_choice_labels"]}
    routes = {(row["block"], row["slot"]): row for row in played["original_menu_choices"]}
    assert routes.keys() == {(180, 0), (180, 1)} and played["original_sailing_menu_prefix_byte_exact"]
    file_path = "/data/SC0.DK4"
    archive = banks[file_path]
    archive_hash = native.digest(base.NdsImage.open(stage.ROM).read_file(file_path))
    registered_choices = []
    for choice in choices["choices"]:
        row = reviewed.pop(choice["id"])
        block, offset, slot = (choice[k] for k in ("block", "offset", "slot"))
        outcome = routes.pop((block, slot), None)
        assert choice["caption"] == row["english"]
        if outcome is not None:
            assert outcome["caption"] == choice["caption"] and outcome["original_branch_executed"]
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
    assert {row["actor_ID"] for row in roles["records"]} == live.NOTES.keys()
    assert all(all(row["review"].values()) for row in roles["records"])
    return dict(modal_proof_sha256=base.digest(FE), retained_modal_pages=1, revised_modal_pages=0,
        choice_proof_sha256=base.digest(CHOICE), retained_choice_labels=registered_choices,
        role_proof_sha256=base.digest(ROLES), retained_roles=len(roles["records"]))


verify_source = checked_text(parent.prior.verify_source, {
    'observed_count() == 50': 'observed_count() == 32 and played["reused_count"] == 17',
    'native_count() == 32': 'native_count() == 20',
    'base.digest(live.report(run))': 'base.digest(live.scope["report_path"](int(run)))',
    'len(records) == 275': 'len(records) == 209',
    'len(changed) == 31': 'len(changed) == 20',
    '    assert sum(r["change_class"] == "prose" for r in changed) == 30\n'
    '    assert [r["id"] for r in changed if r["change_class"] == "wrap_only"] == ["DK4_MES_B118_R0125"]':
        '    assert sum(r["change_class"] == "prose" for r in changed) == 16\n'
        '    assert sum(r["change_class"] == "wrap_only" for r in changed) == 4\n'
        '    lateen, = [r for r in changed if r["id"] == stage.LATEEN_ID]\n'
        '    assert lateen["english"] == base.load(stage.LATEEN)["english"]\n'
        '    assert lateen["display_proof"]["layouts"][0]["lines"][1] == "at just the right angle."\n'
        '    assert lateen["observed_focused"] and "reused_exact_stored_command_and_runtime" not in lateen["observed_focused"]',
    'base.digest(stage.draft.checkpoint.QUEUE)': 'base.digest(stage.checkpoint.QUEUE)',
    'wording_revisions=30, wrap_only_revisions=1': 'wording_revisions=16, wrap_only_revisions=4',
    'justified_retentions=244, choice_label_retentions=5': 'justified_retentions=189, choice_label_retentions=8',
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    "len(batches) == 1079 and len(checks) == 414": "len(batches) == 1080 and len(checks) == 415",
    '        checks["registered_rafael_basra_and_map_keys_and_complete_parent_inverse"] = True':
        '        assert "registered_rafael_ship_lessons_and_complete_parent_inverse" not in checks\n'
        '        checks["registered_rafael_ship_lessons_and_complete_parent_inverse"] = True\n'
        '        assert len(checks) == 416',
    "verified_hodram_recruitment_and_sails_predecessor": "verified_rafael_basra_and_map_keys_predecessor",
    "previously_localized_records=213, contextual_records_revisited=213, contextual_decisions_reused=0":
        "previously_localized_records=217, contextual_records_revisited=217, contextual_decisions_reused=117",
    "prior_records_reviewed=213, contextual_decisions_reused=0": "prior_records_reviewed=217, contextual_decisions_reused=117",
    "justified_retentions=192, retained_choice_labels=6": "justified_retentions=189, retained_choice_labels=8",
    "prose_revisions=15": "prose_revisions=16",
    "wrap_only_revisions=0": "wrap_only_revisions=4",
    "default_substitution_panels=2, retained_modal_pages=2, revised_modal_pages=0, native_choice_outcomes=6":
        "default_substitution_panels=0, retained_modal_pages=1, revised_modal_pages=0, native_choice_outcomes=2",
    "FE, CHOICE, ROLES, stage.GUARD, stage.GUARD_SC0": "FE, CHOICE, ROLES, stage.LATEEN",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's recruitment and ship lessons

The [testing ROM](../../{ROM.as_posix()}) includes the revised conversations around recruiting Jam, Cesare, Fernando and Manuel. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_basra_and_map_keys_pipeline", "rafael_ship_lessons_pipeline").replace(
    "rafael_basra_and_map_keys_release", "rafael_ship_lessons_release",
).replace("release_stack_before_rafael_basra_and_map_keys", "release_stack_before_rafael_ship_lessons").replace(
    "release_stack_with_rafael_basra_and_map_keys", "release_stack_with_rafael_ship_lessons",
).replace('"rafael_basra_and_map_keys_20261123"', '"rafael_ship_lessons_20261123"')

pins = parent.commit[parent.commit.index("    excerpt_rom = "):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins:'''    excerpt_rom = Path(base.load(live.scope["receipt"](0))["rom"])
    earlier = [excerpt_rom, live.OLD.ROM, Path(base.load(live.prototype.excerpt_scope["receipt"](0))["rom"])]
    for receipt in live.OLD.ROOT.glob("focused_gameplay/*/fixture.json"):
        evidence = base.load(receipt)
        fixture = Path(evidence["rom"])
        assert base.digest(fixture) == evidence["rom_sha256"]
        if fixture not in earlier:
            earlier.append(fixture)
''',
    "Preserve the Rafael Basra and Map Key candidate, predecessor and focused ROMs":
        "Preserve the Rafael ship lessons candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael's recruitment and ship lessons

The clean-Japanese pass covers 217 texts across five exchanges. Sixteen wording changes and four wrap-only revisions address eleven queued wrap records and related issues. The ledger gives individual reasons for retaining 189 speech or notice records and all eight choice captions. [Exact review](../{REVIEW.as_posix()})

All 20 revised pages, one extra-armor notice and eleven names or roles passed native checks. The staged emulator replays cover 15 fresh holds. Seventeen earlier holds, including both sailing choices, carry forward after exact comparison of the relevant stored commands and runtime. Natural story activation and handheld display remain unvisited. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("release_stack_before_rafael_basra_and_map_keys", "release_stack_before_rafael_ship_lessons").replace(
    "release_stack_with_rafael_basra_and_map_keys", "release_stack_with_rafael_ship_lessons",
)

scope = parent.scope | globals()
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
