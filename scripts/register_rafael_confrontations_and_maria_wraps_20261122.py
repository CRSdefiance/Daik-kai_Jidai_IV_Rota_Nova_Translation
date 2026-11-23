"""Register the verified Rafael confrontations and Maria phrase repairs."""

from scripts import register_camille_and_maria_reveals_20261122 as parent
from scripts import replay_rafael_confrontations_and_maria_wraps_20261122 as live
from scripts import stage_rafael_confrontations_and_maria_wraps_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-rafael-confrontations-and-maria-wraps-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_confrontations_and_maria_wraps_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_Confrontations_And_Maria_Wraps_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_confrontations_and_maria_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_confrontations_and_maria_wraps_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 32 revisions spanning Charlotte's celebration, Valdes's intervention, Cristina's recruitment and Maria's warning."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def finalize_decisions(records):
    unchanged = {"DK4_MES_B69_R0251", "DK4_MES_B82_R0103", "DK4_MES_B82_R0201"}
    rechecked = set()
    for row in records:
        if row["decision"] != "revision":
            continue
        if row["registered_reference"]["exact_command_hex"] != row["current_reference"]["exact_command_hex"]:
            continue
        assert row["route"] == 0 and row["id"] in unchanged and row["change_class"] == "wrap_only"
        row.update(decision="retention", change_class="retention", layout_rechecked_byte_exact=True,
                   localization_note=row["localization_note"] + " Native reflow reproduced the existing readable layout byte for byte.")
        rechecked.add(row["id"])
    assert rechecked == unchanged
    assert sum(row["decision"] == "revision" for row in records) == 32
    assert sum(row["change_class"] == "wrap_only" for row in records) == 7


def seal_maria_repairs(records):
    old = base.load(stage.draft.OBSERVED)
    earlier = {(r["file_path"], r["id"]): r for r in base.load(parent.REVIEW)["records"] if r["block"] == 36}
    assert old["candidate_sha256"] == base.digest(parent.ROM)
    leads = {r["id"]: r for r in old["rows"]}
    reused, repaired = [], []
    for row in (r for r in records if r["file_path"] == "/data/SC3.DK4"):
        path, ident = row["file_path"], row["id"]
        prior = earlier[path, ident]
        assert row["english"] == prior["english"]
        assert row["source_reference"]["exact_command_hex"] == prior["source_reference"]["exact_command_hex"]
        assert row["current_reference"]["exact_command_hex"] == prior["registered_reference"]["exact_command_hex"]
        if ident not in leads:
            assert row["decision"] == "retention"
            reused.append(ident)
            continue
        lead = leads[ident]
        hold = row["observed_focused"]["capture"]
        assert row["observed_focused"]["changed"] and row["change_class"] == "wrap_only"
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        assert any(lead["protected_phrase_to_check"] in line for line in row["display_proof"]["layouts"][0]["lines"])
        repaired.append(lead | {"new_focused_hold": hold, "new_reference": row["registered_reference"]})
    assert len(reused) == 14 and len(repaired) == 2
    return dict(previous_review=parent.REVIEW.as_posix(), previous_review_sha256=base.digest(parent.REVIEW),
                reused_record_ids=reused, repaired_wraps=repaired)


verify_source = checked_text(parent.verify_source, {
    'observed_count() == 22': 'observed_count() == 18',
    'played["lil_report_sha256"]': 'played["rafael_report_sha256"]',
    'native_count() == 12': 'native_count() == 35',
    'archives = {"/data/SC2.DK4", "/data/SC3.DK4"}': 'archives = {"/data/SC0.DK4", "/data/SC3.DK4"}',
    'len(records) == 192': 'len(records) == 207',
    '''    assert sum(r["decision"] == "revision" for r in records) == 12
    assert all(r["registered_reference"]["exact_command_hex"] != r["current_reference"]["exact_command_hex"]
               for r in records if r["decision"] == "revision")''':
        '    finalize_decisions(records)\n    assert sum(r["source_selector"] == 254 and r["decision"] == "retention" for r in records) == 5',
    'seal_replayed_wraps(records)': 'seal_maria_repairs(records)',
    'wording_revisions=2, wrap_only_revisions=10': 'wording_revisions=25, wrap_only_revisions=7',
    'justified_retentions=180': 'justified_retentions=175',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1059 and len(checks) == 394": "len(batches) == 1060 and len(checks) == 395",
    "previously_localized_records=192, contextual_records_revisited=178": "previously_localized_records=207, contextual_records_revisited=191",
    "prior_records_reviewed=192": "prior_records_reviewed=207",
    "contextual_decisions_reused=14": "contextual_decisions_reused=16",
    "wrap_only_revisions=10": "wrap_only_revisions=7",
    "justified_retentions=180": "justified_retentions=175",
    "prose_revisions=2": "prose_revisions=25",
    "text_display_revisions=10": "text_display_revisions=7",
    "focused_initialized_Lil_and_Maria": "focused_initialized_Rafael_and_Maria",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael and Maria testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 32 editorial improvements. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("camille_and_maria_reveals", "rafael_confrontations_and_maria_wraps").replace(
    "verified_lil_lessons_and_maria_scenes_predecessor", "verified_camille_and_maria_reveals_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Camille and Maria reveals candidate, predecessor and unique focused ROMs":
        "Preserve the Rafael and Maria candidate, predecessor and unique focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael’s confrontations and Maria’s wrap repairs

The contextual review covers Charlotte's celebration, Simon's challenge and Valdes's intervention, Cristina's recruitment, and Maria's warning to Lil. It records 25 wording revisions, seven wrap repairs and 175 justified retentions across 207 records. Three retentions reproduced the installed layout byte for byte. Five original alternate portrait payloads are exact. [Coverage ledger](../{REVIEW.as_posix()})

The two previously observed breaks in “tell you the truth” and “making things up” are repaired. Focused cold-boot replays checked 18 pages with their original speaker labels. The remaining changed pages passed offline native and visual checks. These replays selected original speech commands after game initialization. Their natural story triggers and handheld behavior were unvisited. Startup and 17 regressions passed. [Test ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("camille_and_maria_reveals", "rafael_confrontations_and_maria_wraps")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
