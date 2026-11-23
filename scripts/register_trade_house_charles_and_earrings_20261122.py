"""Register the revised trade-house, recruitment and earrings exchanges."""

from scripts import register_rafael_confrontations_and_maria_wraps_20261122 as parent
from scripts import replay_trade_house_charles_and_earrings_20261122 as live
from scripts import stage_trade_house_charles_and_earrings_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-trade-house-charles-and-earrings-v1-20261122"
ROOT = parent.ROOT.with_name("trade_house_charles_and_earrings_registered_20261122")
ROM = ROOT / "Translation_DS_Trade_House_Charles_And_Earrings_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_trade_house_charles_and_earrings_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_trade_house_charles_and_earrings_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's trade-house discussion, Eirene exchange and Charles recruitment alongside Hodram's Ceramic Earrings offer."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.parent.template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def check_retained_choices(image, candidate):
    proof = base.load(stage.CHOICE_PROOF)
    assert proof["candidate_sha256"] == candidate and proof["offline_exact"]
    bank = native.IlnkContainer.parse(image["/data/SC1.DK4"]).blocks[210]
    rows = proof["choices"]
    assert len(rows) == 2 and sum(len(row["english"]) for row in rows) == 4
    for row in rows:
        assert all(row["review"].values()) and row["decision"] == "retention"
        at, raw = row["installed_offset"], bytes.fromhex(row["installed_command_hex"])
        assert native.digest(bank) == row["installed_block_sha256"] and bank[at:at+len(raw)] == raw
    return rows


verify_source = checked_text(parent.verify_source, {
    'observed_count() == 18': 'observed_count() == 17',
    '(played["rafael_report_sha256"], played["maria_report_sha256"]) == (base.digest(live.REPORT), base.digest(live.MARIA_REPORT))':
        '(played["rafael_report_sha256"], played["hodram_report_sha256"]) == (base.digest(live.REPORT), base.digest(live.HODRAM_REPORT))',
    'native_count() == 35': 'native_count() == 28',
    'archives = {"/data/SC0.DK4", "/data/SC3.DK4"}': 'archives = {"/data/SC0.DK4", "/data/SC1.DK4"}',
    'len(records) == 207': 'len(records) == 119',
    '''    finalize_decisions(records)
    assert sum(r["source_selector"] == 254 and r["decision"] == "retention" for r in records) == 5''':
        '''    changed = [r for r in records if r["decision"] == "revision"]
    assert len(changed) == 27 and all(r["registered_reference"]["exact_command_hex"] != r["current_reference"]["exact_command_hex"]
                                      for r in changed)
    assert sum(r["change_class"] == "wrap_only" for r in changed) == 3''',
    'observed_maria_wraps_and_reference_reuse=seal_maria_repairs(records),':
        'retained_choice_objects=check_retained_choices(b, candidate),',
    'wording_revisions=25, wrap_only_revisions=7': 'wording_revisions=24, wrap_only_revisions=3',
    'justified_retentions=175': 'justified_retentions=92',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1060 and len(checks) == 395": "len(batches) == 1061 and len(checks) == 396",
    "previously_localized_records=207, contextual_records_revisited=191": "previously_localized_records=123, contextual_records_revisited=123",
    "prior_records_reviewed=207": "prior_records_reviewed=123",
    "contextual_decisions_reused=16": "contextual_decisions_reused=0",
    "wrap_only_revisions=7": "wrap_only_revisions=3",
    "justified_retentions=175": "justified_retentions=92, retained_choice_labels=4",
    "prose_revisions=25": "prose_revisions=24",
    "text_display_revisions=7": "text_display_revisions=3",
    "focused_initialized_Rafael_and_Maria": "focused_initialized_Rafael_and_Hodram",
    "(stage.PROOF, STARTUP, QA, live.LIVE, DISPLAY, args.visual_review,": "(stage.PROOF, STARTUP, QA, live.LIVE, DISPLAY, stage.CHOICE_PROOF, args.visual_review,",
    "(live.LIVE, DISPLAY, stage.PROOF)": "(live.LIVE, DISPLAY, stage.PROOF, stage.CHOICE_PROOF)",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Trade-house, Charles and Ceramic Earrings testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 27 editorial improvements. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_confrontations_and_maria_wraps", "trade_house_charles_and_earrings").replace(
    "verified_camille_and_maria_reveals_predecessor", "verified_rafael_confrontations_and_maria_wraps_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Rafael and Maria candidate, predecessor and unique focused ROMs":
        "Preserve the trade-house candidate, predecessor and unique focused ROMs",
    "earlier = [live.ROM, live.MARIA_ROM]": "earlier = [live.ROM, live.HODRAM_ROM]",
    old_doc:'''    DOC.write_text(f"""# Trade house, Charles and Ceramic Earrings review

Three Rafael exchanges and Hodram's Ceramic Earrings offer account for 119 dialogue records and four choice labels. The release has 24 wording revisions, three wrap fixes, 92 justified dialogue retentions and four exact choice-label retentions. The trader's sales pitch keeps the dancer's legend, the 9,000-coin asking price and the separate refusal branches. [Coverage ledger](../{REVIEW.as_posix()})

Focused cold-boot replays verified 17 dialogue pages and original nameplates. Clau's new greeting was checked with the default Rafael in the emulator and the maximum supported name width offline. Both choice objects retained their complete original command bytes. Natural story triggers, choice selection and handheld behavior remain unvisited in this batch. Startup and 17 regressions passed. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_confrontations_and_maria_wraps", "trade_house_charles_and_earrings")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
