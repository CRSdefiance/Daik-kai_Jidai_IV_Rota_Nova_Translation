"""Register Rafael's reviewed Pereira, Eirene and Charlotte dialogue."""

from inspect import getsource

from scripts import register_current_story_wraps_20261122 as parent
from scripts import replay_rafael_diplomacy_and_friends_20261122 as live
from scripts import stage_rafael_diplomacy_and_friends_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON, ARCHIVE = parent.ARM, parent.COMMON, stage.draft.ARCHIVE
PROFILE = "all-routes-rafael-diplomacy-and-friends-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_diplomacy_and_friends_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_Diplomacy_And_Friends_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_diplomacy_and_friends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_diplomacy_and_friends_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 28 revisions in Rafael's Pereira, Eirene and Charlotte scenes."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


verify_source = checked_text(getsource(parent.verify), {
    'observed_count() == 6': 'observed_count() == 10',
    'native_count() == 15': 'native_count() == 28',
    'archives = {f"/data/SC{i}.DK4" for i in range(4)}': 'archives = {ARCHIVE}',
    '(live.ARCHIVE, r["id"])': '(ARCHIVE, r["id"])',
    'len(records) == 72': 'len(records) == 268',
    'base.digest(stage.review.TRIAGE)': 'base.digest(stage.draft.established.TRIAGE)',
    '        records.append(row | dict(registered_reference=registered, display_proof=display,':
        '''        if ident == "DK4_MES_B60_R0071":
            row = row | {"localization_note": "Pereira asks one direct question and tells Rafael to think before answering. The existing wording preserves the pressure of that challenge."}
        records.append(row | dict(registered_reference=registered, display_proof=display,''',
    'wording_revisions=2, wrap_only_revisions=11': 'wording_revisions=13, wrap_only_revisions=15',
    'justified_retentions=59': 'justified_retentions=240',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1055 and len(checks) == 390": "len(batches) == 1056 and len(checks) == 391",
    "changed_components=4": "changed_components=1",
    "previously_localized_records=72, contextual_records_revisited=72": "previously_localized_records=268, contextual_records_revisited=268",
    "prior_records_reviewed=72": "prior_records_reviewed=268",
    "wrap_only_revisions=11": "wrap_only_revisions=15",
    "justified_retentions=59": "justified_retentions=240",
    "prose_revisions=2": "prose_revisions=13",
    "text_display_revisions=11": "text_display_revisions=15",
    "focused_initialized_Maria_lesson_and_battle=True": "focused_initialized_Rafael_story_excerpts=True",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael diplomacy and friends testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes 28 revisions to Rafael's negotiations with Pereira and conversations with Eirene and Charlotte. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("early_story_wraps", "rafael_diplomacy_and_friends").replace(
    "verified_square_rumor_wraps_predecessor", "verified_early_story_wraps_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the early story wrap candidate, predecessor and unique focused ROM":
        "Preserve the Rafael diplomacy and friends candidate, predecessor and unique focused ROM",
    old_doc:'''    DOC.write_text(f"""# Rafael, Pereira, Eirene and Charlotte

The three complete story objects have 268 source-paired decisions, with 13 dialogue revisions, 15 wrap fixes and 240 individual retentions. Pereira's threat assessment distinguishes securing their rear from asking him to stay and fight. Eirene's health is the reason Clau gives for watching out for her. Charlotte uses Romani to identify her community and describes the trader's low offer without implying a completed sale. [Exact Japanese and installed text](../{REVIEW.as_posix()})

All 28 changed pages passed native formatting, complete glyph and visual checks. A focused Rafael replay sampled ten panels with their speaker labels in an initialized story scene. The original branch triggers and hardware remain unvisited for these changes. Ordinary startup and 17 regressions passed. The clean-input patch reconstructs the candidate byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("early_story_wraps", "rafael_diplomacy_and_friends")
scope = parent.scope | globals()
for function in (verify_source, build, commit):
    exec(compile(function, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
