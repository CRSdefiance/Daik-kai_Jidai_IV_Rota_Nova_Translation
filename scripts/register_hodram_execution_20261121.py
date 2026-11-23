"""Register the reviewed Hodram execution scene in the cumulative testing ROM."""

from inspect import getsource
from pathlib import Path

from scripts import register_moonlit_violin_20261121 as parent
from scripts import replay_hodram_execution_20261121 as live
from scripts import stage_hodram_execution_20261121 as stage
from scripts import verify_hodram_execution_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-hodram-execution-v1-20261121"
ROOT = Path("out/hodram_execution_registered_20261121")
ROM = ROOT / "Translation_DS_Hodram_Execution_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_hodram_execution_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hodram_execution_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
CHECKPOINT = "Reviewed the 30 records in Hodram’s interrupted execution, registering one prose revision, two phrase wraps and 27 retentions."


verification = checked_text(getsource(parent.verify), {
    "stage.PROOF, stage.review.OUTPUT": "stage.PROOF, stage.author.OUTPUT",
    'stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)':
        'stored["manuscript_sha256"] == base.digest(stage.author.PROGRESSIVE)',
    'draft["decisions"] == {"revision": 5, "retention": 32}':
        'draft["decisions"] == {"revision": 3, "retention": 27}',
    'rendered["newly_rendered_pages"] == 5': 'rendered["newly_rendered_pages"] == 4',
    'len(playback["holds"]) == 21 and {h["route"] for h in playback["holds"]} == {0, 1}':
        'len(playback["holds"]) == 11 and {h["route"] for h in playback["holds"]} == {1}',
    'and len(viewed) == 3': 'and len(viewed) == 2',
    'groups.keys() == {"/data/SC0.DK4", "/data/SC1.DK4"}': 'groups.keys() == {"/data/SC1.DK4"}',
    'after[stage.review.shared.COMMON]': 'after["/COMMON/MESFILE.DK4"]',
    '    assert stage.review.bind_movie(clean, target, (source[native.ARM], arm))["sha256"] == draft["artwork"]["sha256"]':
        '    assert rendered["full_review_sha256"] == base.digest(stage.author.OUTPUT)\n'
        '    assert rendered["exact_styled_variants"] == 8 and len(rendered["verified_source_script_cries"]) == 2',
    'len(checked) == len(draft["records"]) == 37': 'len(checked) == len(draft["records"]) == 30',
    '        row["native_formatting_evidence"] = result':
        '        row["native_formatting_evidence"] = result\n'
        '        if row["kind"] == "styled":\n'
        '            src = row["source_reference"]\n'
        '            body_offset = src["offset"] - src["command_offset"] - 20\n'
        '            row["draft_ID"] = ident\n'
        '            row["id"] = f"SC1_B40_STYLE_{src[\'command_offset\']}_{body_offset}"',
})

main_source = getsource(parent.main)
package_prose = main_source[main_source.index('    (PACKAGE / "README.md").write_text'):main_source.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(main_source, {
    "verified_search_forage_wrap_predecessor": "verified_moonlit_violin_predecessor",
    "len(batches) == 979 and len(checks) == 314": "len(batches) == 980 and len(checks) == 315",
    'original_name_substitution_order=True, archive_hashes=archives, source_movie_preserved=True':
        'original_name_substitution_order=True, archive_hashes=archives, exact_original_alternate_voice_object=True',
    'changed_components=2': 'changed_components=1',
    'previously_localized_records=37, new_contextual_records=0, prose_revisions=4':
        'previously_localized_records=30, new_contextual_records=0, prose_revisions=1',
    'wrap_only_revisions=0, justified_retentions=32, name_label_revisions=0, text_display_revisions=1':
        'wrap_only_revisions=2, justified_retentions=27, name_label_revisions=0, text_display_revisions=0',
    'initialized_Rafael_and_Hodram_excerpts=True':
        'initialized_Hodram_excerpt=True',
    'native_revised_pages=5, observed_panels=21': 'native_revised_pages=4, observed_panels=11',
    'prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5':
        'prior_records_reviewed=30, actual_Hodram_panels=11, offline_pages=4',
    'prose_revisions=4, justified_retentions=32, text_display_revisions=1':
        'prose_revisions=1, justified_retentions=27, wrap_only_revisions=2',
    package_prose: '''    (PACKAGE / "README.md").write_text(f"""# Hodram execution scene testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed dialogue and phrase wraps. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
})
# Preserve the actual predecessor field while applying this release's receipt names.
build = build.replace("moonlit_violin", "hodram_execution").replace(
    "verified_hodram_execution_predecessor", "verified_moonlit_violin_predecessor")

commit_source = getsource(parent.commit)
checkpoint_prose = commit_source[commit_source.index("    DOC.write_text"):commit_source.index("    prefix =")]
commit_candidate = checked_text(commit_source, {
    "Preserve the violin candidate or replay ROM": "Preserve the Hodram execution candidate or replay ROM",
    checkpoint_prose: '''    DOC.write_text(f"""# Hodram’s interrupted execution

Reviewed all 30 records from the ambush through Hodram’s challenge. The Pasha’s taunt now uses the dismissive surname question in the Japanese. The full-speed retreat order and the Pasha’s final threat each stay on one row. The 27 retentions include all eight crew alarms and both deliberately unintelligible cries. [Exact source and registered dialogue](../{REVIEW.as_posix()})

All four revised layouts passed visual and native checks, including a 16-character surname. The initialized Hodram replay displayed 11 complete panels covering the revised lines and the default surname substitution. Natural scene activation and hardware remain unverified. [Emulator excerpts](../{(VERIFY / 'hodram_verified_revisions.png').as_posix()})

Six startup frames, 24 protected name getters and 17 focused tests passed. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("moonlit_violin", "hodram_execution")

scope = vars(parent) | globals()
for program in (verification, build, commit_candidate):
    exec(compile(program, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
