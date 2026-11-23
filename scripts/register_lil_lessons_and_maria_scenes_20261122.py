"""Register the source-reviewed Lil and Maria dialogue and the exact patch."""

from inspect import getsource

from scripts import register_current_story_wraps_20261122 as template
from scripts import register_tavern_and_proof_exchanges_20261122 as parent
from scripts import replay_lil_lessons_and_maria_scenes_20261122 as live
from scripts import stage_lil_lessons_and_maria_scenes_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-lil-lessons-and-maria-scenes-v1-20261122"
ROOT = parent.ROOT.with_name("lil_lessons_and_maria_scenes_registered_20261122")
ROM = ROOT / "Translation_DS_Lil_Lessons_And_Maria_Scenes_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_lil_lessons_and_maria_scenes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_lil_lessons_and_maria_scenes_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL, CHOICES_AND_FE = EVIDENCE / "visual_review.json", stage.CHOICES_AND_FE
CHECKPOINT = "Registered 17 revisions in Lil's ship lessons and Maria's story and town scenes."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def retained_six(records):
    prior = {r["id"]: r for r in base.load(template.REVIEW)["records"] if r["file_path"] == "/data/SC2.DK4"}
    wants = {f"DK4_MES_B164_R{n:04d}" for n in (140, 143, 147, 150, 163, 166)}
    bound = []
    for r in (r for r in records if r["id"] in wants):
        assert r["decision"] == "retention"
        original = prior[r["id"]]
        assert original["english"] == r["english"]
        assert original["source_reference"]["exact_body_hex"] == r["source_reference"]["exact_body_hex"]
        assert original["registered_reference"]["exact_command_hex"] == r["current_reference"]["exact_command_hex"]
        bound.append(r["id"])
    assert len(bound) == 6
    return dict(path=template.REVIEW.as_posix(), sha256=base.digest(template.REVIEW), reused_record_ids=bound)


verify_source = checked_text(getsource(template.verify), {
    'observed_count() == 6': 'observed_count() == 25',
    'played["report_sha256"] == base.digest(live.REPORT)':
        '(played["lil_report_sha256"], played["maria_report_sha256"]) == (base.digest(live.REPORT), base.digest(live.MARIA_REPORT))',
    'native_count() == 15': 'native_count() == 18',
    'archives = {f"/data/SC{i}.DK4" for i in range(4)}': 'archives = {"/data/SC2.DK4", "/data/SC3.DK4"}',
    '(live.ARCHIVE, r["id"])': '(r["file_path"], r["id"])',
    'len(records) == 72': 'len(records) == 227',
    'base.digest(stage.review.TRIAGE)': 'base.digest(stage.draft.checkpoint.QUEUE)',
    'wording_revisions=2, wrap_only_revisions=11': 'wording_revisions=8, wrap_only_revisions=9',
    'justified_retentions=59': 'justified_retentions=210',
    '    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",':
        '''    extra = base.load(CHOICES_AND_FE)
    assert extra["candidate_sha256"] == candidate and len(extra["choices"]) == len(extra["retained_FE"]) == 3
    assert sum(r["decision"] == "revision" for r in records) == 17
    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",
        retained_choices=extra["choices"], retained_FE=extra["retained_FE"], previous_proof_reuse=retained_six(records),''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1057 and len(checks) == 392": "len(batches) == 1058 and len(checks) == 393",
    "previously_localized_records=203, contextual_records_revisited=203": "previously_localized_records=227, contextual_records_revisited=221",
    "prior_records_reviewed=203": "prior_records_reviewed=227",
    "contextual_decisions_reused=0": "contextual_decisions_reused=6",
    "wrap_only_revisions=18": "wrap_only_revisions=9",
    "justified_retentions=171": "justified_retentions=210",
    "prose_revisions=14": "prose_revisions=8",
    "text_display_revisions=18": "text_display_revisions=9",
    "pagination_fixes=1": "pagination_fixes=0",
    "focused_initialized_Hodram_tavern_and_recruitment=True": "focused_initialized_Lil_and_Maria=True",
    "CHOICES_AND_PAGES": "CHOICES_AND_FE",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Lil lessons and Maria scenes testing candidate

The [testing ROM](../../{ROM.as_posix()}) updates Lil's lessons and Maria's story and town scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("tavern_and_proof_exchanges", "lil_lessons_and_maria_scenes").replace(
    "verified_rafael_diplomacy_and_friends_predecessor", "verified_tavern_and_proof_exchanges_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "earlier = [live.ROM]": "earlier = [live.ROM, live.MARIA_ROM]",
    "Preserve the tavern and Proof candidate, predecessor and unique focused ROM":
        "Preserve the Lil and Maria candidate, predecessor and unique focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Lil's lessons and Maria's story and town scenes

The review covers 224 spoken turns, three speakerless notices or effects, and six choice labels. Eight turns have revised wording and nine have wrap fixes. The 210 main-record retentions include six continuing decisions in Cesare's ship-buying lesson. Manuel now describes repair work in the Lumber Room, while the Shipwright's two sail definitions keep their terms and full meaning. The Genoa Owner and Cook stay in their established roles, and the original tomato forecast and Basra effect and forecast are byte-exact. [Exact source, installed references and decisions](../{REVIEW.as_posix()})

All 17 changed panels passed native and visual review, including Camille's maximum-width name substitution. Focused emulator runs showed 25 Lil and Maria dialogue panels, including the Basra Shopkeeper's private joke. Lil's host returned to port. Maria's host advanced to its original “Xien Yan joined!” notice. Original event activation and hardware remain outside this replay evidence. Startup and 17 regressions passed, and the clean-input patch reconstructs the ROM byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("tavern_and_proof_exchanges", "lil_lessons_and_maria_scenes")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
