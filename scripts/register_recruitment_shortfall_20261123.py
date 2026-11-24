"""Register the verified required-crew prompts over the cumulative capacity candidate."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_recruitment_capacity_20261123 as parent
from scripts import replay_recruitment_shortfall_20261123 as checks
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_recruitment_shortfall_20261123 as build
from scripts import verify_recruitment_shortfall_20261123 as played
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-recruitment-shortfall-wraps-v1-20261123"
CHECK = "registered_recruitment_shortfall_original_loader_wrap_and_complete_parent_inverse"
ARM, COMMON, ROM, WORK = build.ARM, build.COMMON, build.ROM, build.ROOT
PATCH, PATCH_PROOF, REBUILT = checks.PATCH, checks.PATCH_PROOF, checks.REBUILT
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_recruitment_shortfall_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
MANIFEST = ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_recruitment_shortfall.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
STARTUP_CAPTURE = checks.STARTUP_CAPTURE
DOC = Path("docs/editorial_recruitment_shortfall_registered_20261123.md")
CHECKPOINT = "Fixed the two required-crew line breaks and verified Manuel's 12-sailor shortfall in a focused replay."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=played.SHEET, PROOF=build.PROOF)))


verify_code = checked_text(getsource(parent.verify), {
    'len(stored["records"]) == 14': 'len(stored["records"]) == 7',
    '''    live = gameplay["ordinary_play"]
    assert [live[key]["message_ID"] for key in ("azores", "istanbul")] == [1048, 1042]
    assert sum(len(row["holds"]) for row in live.values()) == 3''':
        '''    assert gameplay["message_ID"] == 1041 and gameplay["live_shortfall"] == 12
    assert gameplay["ordinary_actions_after_fixture"] and len(gameplay["pages"]) == 2
    assert gameplay["fixture"]["crew_after"] == 9 and gameplay["fixture"]["all_other4MiB_bytes_exact"]
    assert len(gameplay["unchanged_frames"]) == 8''',
    'assert len(records) == 12 and [row["message_id"] for row in followups] == [1039, 1041]':
        'assert len(records) == 7 and not followups',
    'build.recruitment.catalogue': 'build.capacity.recruitment.catalogue',
    'build.batch.reference': 'build.capacity.batch.reference',
})
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_developed_azores_predecessor=predecessor, recruitment_capacity_release=str(REVIEW)":
        "verified_recruitment_capacity_predecessor=predecessor, recruitment_shortfall_release=str(REVIEW)",
    "len(batches) == 1108 and len(checks) == 443": "len(batches) == 1109 and len(checks) == 444",
    "recruitment_capacity_release_proof": "recruitment_shortfall_release_proof",
    '"recruitment_capacity_pipeline"': '"recruitment_shortfall_pipeline"',
    "registered_manifest_entries=1109, passing_release_checks=444": "registered_manifest_entries=1110, passing_release_checks=445",
    "contextual_records_revisited=14, contextual_decisions_reused=5, previously_localized_records=14":
        "contextual_records_revisited=7, contextual_decisions_reused=5, previously_localized_records=7",
    "prose_revisions=7, justified_retentions=5, text_display_revisions=7":
        "prose_revisions=2, justified_retentions=5, text_display_revisions=2",
    "ordinary_azores_and_istanbul_tavern=True": "focused_azores_tavern_after_single_crew_field_setup=True",
    "capacity_voices_revised=7, dialogue_retained=5, separate_shortfall_leads=2":
        "shortfall_voices_revised=2, dialogue_retained=5",
    '"recruitment_capacity_20261123"': '"recruitment_shortfall_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Recruit Crew shortfall testing candidate

Two required-crew prompts now keep their recruitment verbs together and preserve the exact shortage. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Recruit Crew capacity candidate": "Preserve the registered Recruit Crew shortfall candidate",
    "1,109 entries and 444 passing checks": "1,110 entries and 445 passing checks",
    doc: '''    DOC.write_text(f"""# Recruit Crew shortfall dialogue

Two required-crew prompts now keep **round up** and **recruit more?** together, with the original shortage amount and the officers' tone preserved. Five other shortfall voices retain their wording with individual reasons. The two revised variants passed native layout and glyph checks at all 14 supplied headcounts. [Exact source and installed records](../{REVIEW.as_posix()})

The paired Azores Tavern replay set the Vestaros starting crew to nine through its original setter. Only one byte changed at setup. The game played its normal recruitment exchange and Manuel asked about a shortage of 12. The complete nameplate and choice controls matched. Declining advanced to Assign Sailors with 38,633 gold on both ROMs. The other eight complete screen samples matched. The other revised voice is covered offline. [Paired gameplay and fixture disclosure](../{VERIFY.as_posix()}/{played.SHEET.name})

The registered candidate passed six startup frame comparisons, 24 protected name getters, eight ASCII right-bound spans, and all 17 focused tests. Its clean-input patch reconstructs the exact candidate. [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = parent.template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    # The inherited startup and registry helpers refer to the common template.
    scope = vars(parent.template) | vars(parent) | globals() | dict(template=parent.template)
    exec(compile(verify_code + "\n" + prepare + "\n" + finish, __file__ + "::registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
