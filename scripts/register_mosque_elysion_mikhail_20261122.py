"""Register the revised mosque, Elysion and Mikhail dialogue."""

from scripts import register_trade_house_charles_and_earrings_20261122 as parent
from scripts import replay_mosque_elysion_mikhail_20261122 as live
from scripts import stage_mosque_elysion_mikhail_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-mosque-elysion-mikhail-v1-20261122"
ROOT = parent.ROOT.with_name("mosque_elysion_mikhail_registered_20261122")
ROM = ROOT / "Translation_DS_Mosque_Elysion_Mikhail_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_mosque_elysion_mikhail_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_mosque_elysion_mikhail_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's mosque exchange and Hodram's Elysion and Mikhail scenes."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.parent.parent.template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def exact_display_retentions(records):
    held = [r for r in records if r["source_selector"] == 254 or (r["route"], r["id"]) == (1, "DK4_MES_B168_R0096")]
    assert len(held) == 8 and all(r["decision"] == "retention" for r in held)
    for row in held:
        assert row["current_reference"]["exact_command_hex"] == row["registered_reference"]["exact_command_hex"]
    return [r["registered_reference"] for r in held]


verify_source = checked_text(parent.verify_source, {
    'observed_count() == 17': 'observed_count() == 19',
    'native_count() == 28': 'native_count() == 29',
    'len(records) == 119': 'len(records) == 180',
    'retained_choice_objects=check_retained_choices(b, candidate),':
        'exact_display_retentions=exact_display_retentions(records),',
    'justified_retentions=92': 'justified_retentions=153',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1061 and len(checks) == 396": "len(batches) == 1062 and len(checks) == 397",
    "previously_localized_records=123, contextual_records_revisited=123": "previously_localized_records=180, contextual_records_revisited=180",
    "prior_records_reviewed=123": "prior_records_reviewed=180",
    "justified_retentions=92, retained_choice_labels=4": "justified_retentions=153",
    "DISPLAY, stage.CHOICE_PROOF, args.visual_review,": "DISPLAY, args.visual_review,",
    "(live.LIVE, DISPLAY, stage.PROOF, stage.CHOICE_PROOF)": "(live.LIVE, DISPLAY, stage.PROOF)",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Mosque, Elysion and Mikhail testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 27 editorial improvements. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("trade_house_charles_and_earrings", "mosque_elysion_mikhail").replace(
    "verified_rafael_confrontations_and_maria_wraps_predecessor", "verified_trade_house_charles_and_earrings_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the trade-house candidate, predecessor and unique focused ROMs":
        "Preserve the mosque and Hodram candidate, predecessor and unique focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Mosque, Elysion and Mikhail dialogue review

The review covers 180 dialogue and tutorial records. It clarifies the tablet deduction, keeps Maria's argument grounded in the source, makes Cesare's ownership reply sound natural, and cleans up Hodram's introduction and Mikhail's offer to explain items. The release has 24 wording revisions, three wrap fixes and 153 justified retentions. [Coverage ledger](../{REVIEW.as_posix()})

Focused cold-boot replays verified 19 story pages and their original nameplates. The new substitution layouts passed native checks with default and maximum widths for company and personal names. Seven speakerless commands and Cesare's comic string of symbols are byte-exact. The symbol panel received direct visual review in the replay. The other 18 replayed pages matched their native glyph planes. The company line keeps its original substitution without producing two periods after Castor Co. Natural story activation and handheld behavior remain unvisited. Startup and 17 regressions passed. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("trade_house_charles_and_earrings", "mosque_elysion_mikhail")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
