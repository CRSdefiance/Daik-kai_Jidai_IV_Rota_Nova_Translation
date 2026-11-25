"""Register the parallel tavern and Hodram story fixes after display verification."""

from inspect import getsource

from scripts import register_rafael_diplomacy_and_friends_20261122 as parent
from scripts import register_current_story_wraps_20261122 as template
from scripts import replay_tavern_and_proof_exchanges_20261122 as live
from scripts import stage_tavern_and_proof_exchanges_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-tavern-and-proof-exchanges-v1-20261122"
ROOT = parent.ROOT.with_name("tavern_and_proof_exchanges_registered_20261122")
ROM = ROOT / "Translation_DS_Tavern_And_Proof_Exchanges_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_tavern_and_proof_exchanges_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_tavern_and_proof_exchanges_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL, CHOICES_AND_PAGES = EVIDENCE / "visual_review.json", stage.CHOICES_AND_PAGES
CHECKPOINT = "Registered 32 dialogue and wrap corrections in the tavern and Proof of Conquest exchanges."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


verify_source = checked_text(getsource(template.verify), {
    'observed_count() == 6': 'observed_count() == 15',
    'native_count() == 15': 'native_count() == 33',
    'archives = {f"/data/SC{i}.DK4" for i in range(4)}': 'archives = {"/data/SC1.DK4", "/data/SC3.DK4"}',
    '(live.ARCHIVE, r["id"])': '(live.PATH, r["id"])',
    'len(records) == 72': 'len(records) == 203',
    'base.digest(stage.review.TRIAGE)': 'base.digest(stage.draft.queue.OUTPUT)',
    'wording_revisions=2, wrap_only_revisions=11': 'wording_revisions=14, wrap_only_revisions=18',
    'justified_retentions=59': 'justified_retentions=171',
    '        records.append(row | dict(registered_reference=registered, display_proof=display,':
        '''        if ident == "DK4_MES_B170_R0090":
            assert exact.hex() == row["current_reference"]["exact_command_hex"] and display["layouts"]
            row = row | dict(decision="retention", change_class="retention", protected_phrases=[],
                localization_note="The proposed phrase checks produced the identical stored page. Retain the distinction between knowing the drink and knowing its price as cargo.")
        if ident == "DK4_MES_B173_R0138":
            row = row | dict(localization_note=row["localization_note"] + " The short lead-in to the punch line preserves his pause before saying how a gift wins a woman's heart.")
        records.append(row | dict(registered_reference=registered, display_proof=display,''',
    '    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",':
        '''    assert sum(r["decision"] == "revision" for r in records) == 32
    extra = base.load(CHOICES_AND_PAGES)
    assert extra["candidate_sha256"] == candidate and len(extra["choices"]) == 4
    focus = extra["pagination"]
    assert focus["preexisting_page_count"] == 2 and focus["new_page_count"] == 1
    visited_ids = [r["id"] for r in played["observations"]]
    assert visited_ids[visited_ids.index(focus["id"]) + 1] == focus["next_turn"]
    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",
        retained_choices=extra["choices"], observed_pagination_repair=focus, choices_and_pagination_sha256=base.digest(CHOICES_AND_PAGES),''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1056 and len(checks) == 391": "len(batches) == 1057 and len(checks) == 392",
    "changed_components=1": "changed_components=2",
    "previously_localized_records=268, contextual_records_revisited=268": "previously_localized_records=203, contextual_records_revisited=203",
    "prior_records_reviewed=268": "prior_records_reviewed=203",
    "wrap_only_revisions=15": "wrap_only_revisions=18",
    "justified_retentions=240": "justified_retentions=171",
    "prose_revisions=13": "prose_revisions=14",
    "text_display_revisions=15": "text_display_revisions=18",
    "pagination_fixes=0": "pagination_fixes=1",
    "focused_initialized_Rafael_story_excerpts=True": "focused_initialized_Hodram_tavern_and_recruitment=True",
    "(stage.PROOF, STARTUP, QA, live.LIVE, DISPLAY, args.visual_review,":
        "(stage.PROOF, STARTUP, QA, live.LIVE, DISPLAY, CHOICES_AND_PAGES, args.visual_review,",
    "(live.LIVE, DISPLAY, stage.PROOF)": "(live.LIVE, DISPLAY, stage.PROOF, CHOICES_AND_PAGES)",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Tavern and Proof of Conquest testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes 32 fixes across the Fernando coin game, Julio's tavern recruitment, Mikhail's Proof of Conquest explanation and Yifa's recruitment. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_diplomacy_and_friends", "tavern_and_proof_exchanges").replace(
    "verified_early_story_wraps_predecessor", "verified_rafael_diplomacy_and_friends_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Rafael diplomacy and friends candidate, predecessor and unique focused ROM":
        "Preserve the tavern and Proof candidate, predecessor and unique focused ROM",
    old_doc:'''    DOC.write_text(f"""# Tavern and Proof of Conquest exchanges

Reviewed 203 spoken turns and eight choice labels across Hodram's and Maria's stories. Fourteen turns have new wording, eighteen have wrap fixes and 171 retain their wording for individual reasons. The coin game's stakes and rules stay consistent. The Man and Woman labels describe the couple without assuming marriage or age. Julio and Yifa retain their distinct voices. [Source, installed decisions and retained choices](../{REVIEW.as_posix()})

All 32 changed panels passed the native renderer and visual review. The focused Hodram replay showed fifteen panels with their complete speaker labels. Mikhail's joke now fits on one page, and the replay advanced directly to Hodram's reply. Maria's changes were checked offline. The original story triggers and hardware remain unvisited for these changes. Startup and 17 regressions passed, and the clean-input patch reconstructs the ROM byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_diplomacy_and_friends", "tavern_and_proof_exchanges")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
