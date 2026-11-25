"""Register the verified Aziza dialogue and the ordinary town observations."""

from scripts import observe_tripoli_copenhagen_20261122 as town
from scripts import register_mosque_elysion_mikhail_20261122 as parent
from scripts import replay_aziza_shamshir_20261122 as live
from scripts import stage_aziza_shamshir_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-aziza-shamshir-v1-20261122"
ROOT = parent.ROOT.with_name("aziza_shamshir_registered_20261122")
ROM = ROOT / "Translation_DS_Aziza_Shamshir_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_aziza_shamshir_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_aziza_shamshir_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
ORDINARY = town.ROOT / "verified_visits.json"
CHECKPOINT = "Registered the complete Rafael and Aziza dialogue review and recorded new town gameplay."
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.parent.parent.parent.template.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def substitution_receipt(records):
    old = base.load(stage.checkpoint.FOLLOWUP)
    previous, = old["records"]
    row, = (r for r in records if r["id"] == previous["id"])
    assert old["candidate_sha256"] == row["current_reference"]["candidate_sha256"]
    assert row["source_reference"]["exact_command_hex"] == previous["source_reference"]["exact_command_hex"]
    assert row["current_reference"]["exact_command_hex"] == previous["current_reference"]["exact_command_hex"]
    assert "Castor Co.." in previous["offline_name_expansion"]
    default, maximum = row["display_proof"]["layouts"]
    value = bytes.fromhex(default["expanded_hex"])
    assert b"Castor Co.," in value and b".." not in value
    assert maximum["scope"] == "maximum widths"
    hold = row["observed_focused"]["capture"]
    assert base.digest(hold["path"]) == hold["PNG_sha256"]
    return dict(id=row["id"], earlier_expansion=previous["offline_name_expansion"],
        current_default=default["lines"], maximum=maximum["lines"], replay_hold=hold)


def verify_town(candidate):
    result = base.load(ORDINARY)
    assert result["candidate_sha256"] == candidate and result["ordinary_saved_gameplay"]
    assert set(result["visits"]) == set(town.PORTS)
    assert all(base.digest(p) == sha for p, sha in result["evidence"].items())
    return result


verify_source = checked_text(parent.verify_source, {
    'observed_count() == 19': 'observed_count() == 11',
    '(played["rafael_report_sha256"], played["hodram_report_sha256"]) == (base.digest(live.REPORT), base.digest(live.HODRAM_REPORT))':
        'played["report_sha256"] == base.digest(live.REPORT)',
    'native_count() == 29': 'native_count() == 15',
    'checked["sheets"] + played["sheets"]':
        'checked["sheets"] + played["sheets"] + verify_town(candidate)["sheets"]',
    'archives = {"/data/SC0.DK4", "/data/SC1.DK4"}': 'archives = {"/data/SC0.DK4"}',
    '(r["file_path"], r["id"]): r for r in played["observations"]':
        '("/data/SC0.DK4", r["id"]): r for r in played["observations"]',
    'len(records) == 180': 'len(records) == 78',
    'len(changed) == 27': 'len(changed) == 14',
    'assert sum(r["change_class"] == "wrap_only" for r in changed) == 3':
        'assert all(r["change_class"] == "prose" for r in changed)',
    'exact_display_retentions=exact_display_retentions(records),':
        'fixed_company_period=substitution_receipt(records), ordinary_town_visits=verify_town(candidate),',
    'wording_revisions=24, wrap_only_revisions=3': 'wording_revisions=14, wrap_only_revisions=0',
    'justified_retentions=153': 'justified_retentions=64',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1062 and len(checks) == 397": "len(batches) == 1063 and len(checks) == 398",
    "previously_localized_records=180, contextual_records_revisited=180": "previously_localized_records=78, contextual_records_revisited=78",
    "prior_records_reviewed=180": "prior_records_reviewed=78",
    "changed_components=2": "changed_components=1",
    "justified_retentions=153": "justified_retentions=64",
    "prose_revisions=24": "prose_revisions=14",
    "wrap_only_revisions=3": "wrap_only_revisions=0",
    "text_display_revisions=3": "text_display_revisions=0",
    "punctuation_glyph_corrections=0": "punctuation_glyph_corrections=1",
    "focused_initialized_Rafael_and_Hodram=True, natural_activation=False":
        "focused_initialized_Rafael=True, natural_story_activation=False, ordinary_saved_town_visits=True",
    "(live.LIVE, DISPLAY, stage.PROOF)": "(live.LIVE, DISPLAY, stage.PROOF, ORDINARY)",
    "DISPLAY, args.visual_review,": "DISPLAY, ORDINARY, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Aziza and the Bloodstained Shamshir testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 14 revisions in the complete Rafael and Aziza exchange. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("mosque_elysion_mikhail", "aziza_shamshir").replace(
    "verified_trade_house_charles_and_earrings_predecessor", "verified_mosque_elysion_mikhail_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the mosque and Hodram candidate, predecessor and unique focused ROMs":
        "Preserve the Aziza candidate, predecessor and unique focused ROM",
    "earlier = [live.ROM, live.HODRAM_ROM]": "earlier = [live.ROM]",
    old_doc:'''    DOC.write_text(f"""# Rafael and Aziza dialogue review

The source comparison covers all 78 turns. Fourteen lines have new wording and 64 have specific retention reasons. Snake's accusation about the Bloodstained Shamshir preserves the original company slot and now reads cleanly when the default expands to Castor Co. [Coverage ledger](../{REVIEW.as_posix()})

The focused Rafael replay verified 11 story panels and their original speaker labels. All 14 changed lines passed native formatting and visual review. The company name also passed at the maximum supported width offline. The original Aziza story trigger and handheld display remain unvisited. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)

Ordinary input from preserved saves observed both Squares and the Copenhagen Tavern. Tripoli selected the Hayreddin rumor through the original menu. The visit report binds actual dialogue to native requests and separates these observations from the scripted Rafael excerpt. [Town gameplay and source references](../{ORDINARY.as_posix()})
""",encoding="utf-8")
''',
}).replace("mosque_elysion_mikhail", "aziza_shamshir")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
