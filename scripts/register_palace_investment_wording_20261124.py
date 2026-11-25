"""Register the wording-only Palace batch after the two ordinary playbacks."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_riga_recruitment_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_palace_investment_wording_20261124 as build
from scripts import verify_palace_investment_replay_20261124 as gameplay
from scripts.source_locked_derivation_v5118 import checked_text

review, template = build, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-palace-investment-wording-v1-20261124"
CHECK = "registered_palace_investment_wording_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_palace_investment_wording_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_palace_investment_wording.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
STORED = build.ROOT / "stored_proof.json"
DOC = Path("docs/editorial_palace_investment_wording_registered_20261124.md")
CHECKPOINT = "Registered the Palace investment greeting with an intact trading-contract phrase and the King’s revised commendation."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=STORED)))

verify_source = getsource(parent.verify)
live = verify_source[verify_source.index('    assert live["ordinary_gameplay"]'):verify_source.index('    visual =')]
undo = verify_source[verify_source.index('    undo ='):verify_source.index('    old_rows =')]
verify_source = checked_text(verify_source, {
    live: '''    assert live["ordinary_gameplay"]
    assert live["changed_holds"] == 3 == sum(len(route["revised"]) for route in live["routes"].values())
    assert live["unchanged_holds"] == sum(len(route["unchanged_frames"]) for route in live["routes"].values())
    for city, route in live["routes"].items():
        assert {r["frame"]: (r["message_id"], r["address"]) for r in route["revised"]} == gameplay.HOLDS[city]
    assert packet["native_pages"] == 7
    assert len(packet["sheets"]) == 1 and all(files.digest(r["path"]) == r["sha256"] for r in packet["sheets"])
''',
    "parent.parent.parent.parent.parent.trend.files": "parent.parent.parent.parent.parent.parent.trend.files",
    "== {ARM, COMMON}": "== {COMMON}",
    undo: '''    assert arm == before[ARM] and packet["exact_parent_reserialize"]
''',
    "build.recruit.catalogue": "build.earlier.recruit.catalogue",
    'altered = {r["message_id"] for r in packet["records"] if r["wording_decision"] == "revision"}':
        'altered = {r["message_id"] for r in packet["records"] if r["decision"] == "revision"}',
    "assert altered == {key for key, (draft, _) in build.DRAFTS.items() if draft}": "assert altered == set(build.KEYS)",
    "build.owned_deployment(": "build.earlier.owned_deployment(",
    'instruction_changes=packet["instruction_changes"], changed_COMMON=sorted(altered)':
        'changed_COMMON=sorted(altered), unchanged_ARM9=True',
    "Riga_number_and_dialogue_changes_preserve_startup": "Palace_wording_preserves_startup",
    '    assert len(shared["records"]) == 276': '''    inherited_live = packet["retained_play_evidence"]
    assert files.digest(inherited_live["path"]) == inherited_live["sha256"]
    retained = [row for row in files.read(inherited_live["path"])["dialogue_records"] if row["decision"] == "retention"]
    assert {row["message_ID"] for row in retained} == {63, 1154, 1177, 1178}
    assert all(all(row["review"].values()) and row["installed_reference"]["exact_hex"] == new_rows[row["message_ID"]].text.hex()
               for row in retained)
    assert len(shared["records"]) == 276''',
    "source_credit_added=0,": "source_credit_added=0, retained_dialogue=retained,",
})
exec(compile(verify_source, __file__ + "::registered-Palace-checks", "exec"), vars(parent) | globals(), local_checks := {})
verify = local_checks["verify"]

readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_price_info_digits_predecessor=predecessor, riga_recruitment_release=str(REVIEW)":
        "verified_riga_recruitment_predecessor=predecessor, palace_investment_wording_release=str(REVIEW)",
    "len(batches) == 1138 and len(checks) == 473": "len(batches) == 1139 and len(checks) == 474",
    "assert len(revised) == 10": "assert revised == [f'COMMON_MESSAGE_{k}' for k in build.KEYS]",
    "snapshot_scope=[ARM, COMMON], revised_records": "snapshot_scope=[COMMON], revised_records",
    "riga_recruitment_release_proof=stage.reference(stage.PROOF)": "palace_investment_wording_release_proof=stage.reference(stage.PROOF)",
    '"riga_recruitment_pipeline"': '"palace_investment_wording_pipeline"',
    "registered_manifest_entries=1139, passing_release_checks=474, changed_components=2, changed_internal_files=[ARM, COMMON]":
        "registered_manifest_entries=1140, passing_release_checks=475, changed_components=1, changed_internal_files=[COMMON]",
    "contextual_records_revisited=12, contextual_decisions_reused=0, previously_localized_records=12":
        "contextual_records_revisited=6, contextual_decisions_reused=0, previously_localized_records=6",
    "prose_revisions=9, justified_retentions=3, text_display_revisions=5, phrase_wrap_adjustments=4":
        "prose_revisions=2, justified_retentions=4, text_display_revisions=0, phrase_wrap_adjustments=1",
    'ordinary_Riga_recruitment=True, revised_gameplay_holds=3, native_pages=180, number_call_cases=64, unchanged_gameplay_holds=len(stage.read(gameplay.OUT)["unchanged_frames"])':
        'ordinary_Riga_and_Tunis_Palace=True, revised_gameplay_holds=3, native_pages=7, unchanged_gameplay_holds=stage.read(gameplay.OUT)["unchanged_holds"]',
    "prose_revisions=9, phrase_wrap_adjustments=4, punctuation_fields=0, texts_retained=3":
        "prose_revisions=2, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=4",
    '"riga_recruitment_20261124"': '"palace_investment_wording_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Palace investment testing candidate

The alternate defense greeting keeps “trading contract” together. The King’s reply gives his second compliment as a direct commendation. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Riga recruitment candidate": "Preserve the registered Palace investment wording candidate",
    "1,139 entries and 474 passing checks": "1,140 entries and 475 passing checks",
    doc: '''    DOC.write_text(f"""# Palace military investment

The ruler’s greeting to an investor without a contract now keeps “trading contract” together. The King’s reply keeps both compliments from the Japanese and gives the second its own voice. Four surrounding wordings are retained. Six supplied captain-address cases and the reply passed the native portrait checks. [Clean and installed text](../{REVIEW.as_posix()})

Ordinary Riga and Tunis gameplay verified the three changed holds and the same payments, choices, and returns. Both King nameplates match pixel for pixel. [Paired gameplay](../{VERIFY.as_posix()}/palace_investment_paired.png)

The candidate passed independent startup, 475 registered checks, 17 focused tests, and byte-for-byte reconstruction from clean input. [Testing package](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 16:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for item in reversed(lineage):
        scope.update(vars(item))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::Palace-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()