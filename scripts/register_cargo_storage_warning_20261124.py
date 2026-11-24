"""Register the Cargo Setup wording when replay, startup, and patch checks pass."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from scripts import register_palace_investment_wording_20261124 as parent
from scripts import stage_cargo_storage_warning_20261124 as build
from scripts import stage_cartridge_title_20261123 as files
from scripts.source_locked_derivation_v5118 import checked_text

review, template = build, parent.template
gameplay = SimpleNamespace(OUT=build.PAIRED, SHEET=build.ROOT / "cargo_storage_paired.png", panels=build.panels)
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-cargo-storage-warning-v1-20261124"
CHECK = "registered_cargo_storage_warning_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_cargo_storage_warning_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_cargo_storage_warning.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
STORED = build.ROOT / "stored_proof.json"
DOC = Path("docs/editorial_cargo_storage_warning_registered_20261124.md")
CHECKPOINT = "Registered the Cargo Setup warning with the correct Temporary Storage location."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=STORED)))


prior_verify = parent.verify_source
live = prior_verify[prior_verify.index('    assert live["ordinary_gameplay"]'):prior_verify.index("    visual =")]
retention = prior_verify[prior_verify.index('    inherited_live ='):prior_verify.index('    assert len(shared["records"])')]
verify_source = checked_text(prior_verify, {
    live: '''    assert live["ordinary_gameplay"] and 16000 in live["unchanged_frames"]
    assert live["changed_holds"] == 2 and tuple(r["frame"] for r in live["revised"]) == build.HOLDS
    assert all(r["message_id"] == build.KEY and r["choices_exact"] for r in live["revised"])
    assert packet["native_pages"] == 1
    assert len(packet["sheets"]) == 1 and all(files.digest(r["path"]) == r["sha256"] for r in packet["sheets"])
''',
    "parent.parent.parent.parent.parent.parent.trend.files": "parent.parent.parent.parent.parent.parent.parent.trend.files",
    "build.earlier.recruit.catalogue": "build.tools.recruit.catalogue",
    "assert altered == set(build.KEYS)": "assert altered == {build.KEY}",
    "build.earlier.owned_deployment(": "build.tools.owned_deployment(",
    "Palace_wording_preserves_startup": "Cargo_storage_warning_preserves_startup",
    retention: '''    retained = packet["baseline"]["retained"]
    assert packet["baseline"]["ordinary_gameplay"] and {r["message_ID"] for r in retained} == set(build.KEEP)
    assert all(all(r["review"].values()) and r["installed_reference"] == build.text_ref(new_rows[r["message_ID"]])
               for r in retained)
''',
})
exec(compile(verify_source, __file__ + "::registered-cargo-checks", "exec"),
     vars(parent.parent) | vars(parent) | globals(), local_checks := {})
verify = local_checks["verify"]


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_riga_recruitment_predecessor=predecessor, palace_investment_wording_release=str(REVIEW)":
        "verified_palace_investment_wording_predecessor=predecessor, cargo_storage_warning_release=str(REVIEW)",
    "len(batches) == 1139 and len(checks) == 474": "len(batches) == 1140 and len(checks) == 475",
    "assert revised == [f'COMMON_MESSAGE_{k}' for k in build.KEYS]": "assert revised == [f'COMMON_MESSAGE_{build.KEY}']",
    "palace_investment_wording_release_proof=stage.reference(stage.PROOF)": "cargo_storage_warning_release_proof=stage.reference(stage.PROOF)",
    '"palace_investment_wording_pipeline"': '"cargo_storage_warning_pipeline"',
    "registered_manifest_entries=1140, passing_release_checks=475": "registered_manifest_entries=1141, passing_release_checks=476",
    "contextual_records_revisited=6, contextual_decisions_reused=0, previously_localized_records=6":
        "contextual_records_revisited=5, contextual_decisions_reused=0, previously_localized_records=5",
    "prose_revisions=2, justified_retentions=4, text_display_revisions=0, phrase_wrap_adjustments=1":
        "prose_revisions=1, justified_retentions=4, text_display_revisions=0, phrase_wrap_adjustments=0",
    "ordinary_Riga_and_Tunis_Palace=True, revised_gameplay_holds=3, native_pages=7":
        "ordinary_Riga_Cargo_Setup=True, revised_gameplay_holds=2, native_pages=1",
    "prose_revisions=2, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=4":
        "prose_revisions=1, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=4",
    '"palace_investment_wording_20261124"': '"cargo_storage_warning_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Cargo Setup warning testing candidate

Finish now identifies remaining cargo as being in storage. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Palace investment wording candidate": "Preserve the registered Cargo Setup warning candidate",
    "1,140 entries and 475 passing checks": "1,141 entries and 476 passing checks",
    doc: '''    DOC.write_text(f"""# Cargo Setup warning and Riga shops

The Finish prompt now reads “There's cargo in storage. Finish?” and uses the same No and Yes choices. The clean Japanese says cargo remains and asks to continue. In Riga, the two lots were in Temporary Storage when the warning appeared. No kept both lots available. Yes returned to the Port, and reopening Cargo Setup confirmed there was no cargo left. Four nearby wordings were retained, including the Square shopkeeper's retail line and the Kalmar Union rumor. [Clean and installed text](../{REVIEW.as_posix()})

The native modal fit the complete sentence and question on one row. The paired ordinary gameplay replay verified both changed holds and identical choices and state transitions. [Paired play](../{VERIFY.as_posix()}/cargo_storage_paired.png)

The candidate passed independent startup, 476 registered checks, 17 focused tests, and byte-for-byte reconstruction from the clean input. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::cargo-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
