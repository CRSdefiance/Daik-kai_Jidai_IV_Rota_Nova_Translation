"""Register the verified reveal and recruitment dialogue checkpoint."""

from inspect import getsource

from scripts import register_current_story_wraps_20261122 as template
from scripts import register_lil_lessons_and_maria_scenes_20261122 as parent
from scripts import replay_camille_and_maria_reveals_20261122 as live
from scripts import stage_camille_and_maria_reveals_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-camille-and-maria-reveals-v1-20261122"
ROOT = parent.ROOT.with_name("camille_and_maria_reveals_registered_20261122")
ROM = ROOT / "Translation_DS_Camille_And_Maria_Reveals_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_camille_and_maria_reveals_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_camille_and_maria_reveals_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 12 dialogue and wrap revisions across Camille's reveal, Fernando's lesson and Maria's story."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def seal_replayed_wraps(records):
    old = base.load(stage.draft.checkpoint.FOLLOWUP)
    assert old["candidate_sha256"] == base.digest(parent.ROM)
    earlier = {r["id"]: r for r in base.load(parent.REVIEW)["records"]
               if r["file_path"] == "/data/SC3.DK4" and r["block"] == 36}
    leads = {r["id"]: r for r in old["rows"]}
    reuse, repaired = [], []
    for row in (r for r in records if r["file_path"] == "/data/SC3.DK4" and r["block"] == 36):
        ident = row["id"]
        assert earlier[ident]["english"] == row["english"]
        assert earlier[ident]["registered_reference"]["exact_command_hex"] == row["current_reference"]["exact_command_hex"]
        assert earlier[ident]["source_reference"]["exact_command_hex"] == row["source_reference"]["exact_command_hex"]
        if ident not in leads:
            assert row["decision"] == "retention"
            reuse.append(ident)
            continue
        lead = leads[ident]
        observed = row["observed_focused"]
        assert observed and observed["changed"] and row["change_class"] == "wrap_only"
        assert base.digest(lead["initialized_replay_hold"]["path"]) == lead["initialized_replay_hold"]["PNG_sha256"]
        assert base.digest(observed["capture"]["path"]) == observed["capture"]["PNG_sha256"]
        assert any(lead["proposed_protected_phrase"] in ln for ln in row["display_proof"]["layouts"][0]["lines"])
        repaired.append(lead | {"new_focused_hold": observed["capture"], "new_reference": row["registered_reference"]})
    assert len(reuse) == 14 and len(repaired) == 2
    return dict(earlier_review=parent.REVIEW.as_posix(), earlier_review_sha256=base.digest(parent.REVIEW),
                reused_record_ids=reuse, repaired_wraps=repaired)


verify_source = checked_text(getsource(template.verify), {
    'observed_count() == 6': 'observed_count() == 22',
    'played["report_sha256"] == base.digest(live.REPORT)':
        '(played["lil_report_sha256"], played["maria_report_sha256"]) == (base.digest(live.REPORT), base.digest(live.MARIA_REPORT))',
    'native_count() == 15': 'native_count() == 12',
    'archives = {f"/data/SC{i}.DK4" for i in range(4)}': 'archives = {"/data/SC2.DK4", "/data/SC3.DK4"}',
    '(live.ARCHIVE, r["id"])': '(r["file_path"], r["id"])',
    'len(records) == 72': 'len(records) == 192',
    'base.digest(stage.review.TRIAGE)': 'base.digest(stage.draft.checkpoint.QUEUE)',
    'wording_revisions=2, wrap_only_revisions=11': 'wording_revisions=2, wrap_only_revisions=10',
    'justified_retentions=59': 'justified_retentions=180',
    '    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",':
        '''    assert sum(r["decision"] == "revision" for r in records) == 12
    assert all(r["registered_reference"]["exact_command_hex"] != r["current_reference"]["exact_command_hex"]
               for r in records if r["decision"] == "revision")
    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",
        observed_maria_wraps_and_reference_reuse=seal_replayed_wraps(records),''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1058 and len(checks) == 393": "len(batches) == 1059 and len(checks) == 394",
    "previously_localized_records=227, contextual_records_revisited=221": "previously_localized_records=192, contextual_records_revisited=178",
    "prior_records_reviewed=227": "prior_records_reviewed=192",
    "contextual_decisions_reused=6": "contextual_decisions_reused=14",
    "wrap_only_revisions=9": "wrap_only_revisions=10",
    "justified_retentions=210": "justified_retentions=180",
    "prose_revisions=8": "prose_revisions=2",
    "text_display_revisions=9": "text_display_revisions=10",
    ', CHOICES_AND_FE': '',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Camille and Maria reveals testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 12 refinements across Lil's and Maria's stories, including the two replay-reported wraps. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("lil_lessons_and_maria_scenes", "camille_and_maria_reveals").replace(
    "verified_tavern_and_proof_exchanges_predecessor", "verified_lil_lessons_and_maria_scenes_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Lil and Maria candidate, predecessor and unique focused ROMs":
        "Preserve the Camille and Maria reveals candidate, predecessor and unique focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Camille's reveal and Maria's story follow-up

The review covers 191 spoken turns and the Osaka Glass forecast. Two turns have revised wording, ten keep their wording with better wraps, and 180 have justified retentions. The new lines distinguish Fernando's luck from watching closely and make it explicit that Aziza learned by imitating her father's crew. Camille remains the name his companions know, and Marinus Kuhn remains the name he reveals. [Exact source, installed text and decisions](../{REVIEW.as_posix()})

Two paired emulator holds verify the repairs to “the people of Southeast Asia” and “for all you're worth.” The two focused route replays sampled 22 dialogue panels and original speaker labels. The remaining changed panels passed native and visual checks offline. The original story eligibility and hardware remain unvisited for these changes. Startup and 17 regressions passed, and the patch rebuilds the ROM byte for byte. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("lil_lessons_and_maria_scenes", "camille_and_maria_reveals")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
