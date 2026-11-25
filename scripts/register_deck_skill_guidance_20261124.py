"""Register the verified Deck View tutorial clarification over Cargo Setup."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from scripts import register_cargo_storage_warning_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_deck_skill_guidance_20261124 as build
from scripts import verify_riga_trade_deck_20261124 as paired
from scripts.source_locked_derivation_v5118 import checked_text

review, template = build, parent.template
gameplay = SimpleNamespace(OUT=paired.PAIRED, SHEET=paired.PAIRED_SHEET, panels=paired.panels)
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-deck-skill-guidance-v1-20261124"
CHECK = "registered_deck_skill_guidance_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_deck_skill_guidance_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_deck_skill_guidance.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
STORED = build.ROOT / "stored_proof.json"
DOC = Path("docs/editorial_deck_skill_guidance_registered_20261124.md")
CHECKPOINT = "Registered clearer Deck View instructions for navigator skill requirements."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=STORED)))


previous_verify = parent.verify_source
live = previous_verify[previous_verify.index('    assert live["ordinary_gameplay"]'):previous_verify.index("    visual =")]
inverse = previous_verify[previous_verify.index("    assert arm == before[ARM]"):previous_verify.index("    inherited =")]
retentions = previous_verify[previous_verify.index('    retained = packet["baseline"]'):previous_verify.index('    assert len(shared["records"])')]
verify_source = checked_text(previous_verify, {
    live: '''    assert live["ordinary_gameplay"] and live["full_help_ink_verified"]
    assert live["changed_holds"] == 5 and tuple(r["frame"] for r in live["revised"]) == build.HOLDS
    assert 17600 in live["unchanged_frames"] and live["sea_level_up"]["actual_text"] == "Gerhard leveled up!"
    assert packet["native_pages"] == 1
    assert len(packet["sheets"]) == 1 and all(files.digest(r["path"]) == r["sha256"] for r in packet["sheets"])
    proof = packet["native_proof"]
    assert files.digest(proof["path"]) == proof["sha256"]
    assert files.read(proof["path"])["all_words_keep_one_row_all_glyphs_fit_and_first_last_letters_present"]
''',
    "parent.parent.parent.parent.parent.parent.parent.trend.files": "parent.parent.parent.parent.parent.parent.parent.parent.trend.files",
    "== {COMMON}": "== {ARM}",
    inverse: '''    assert common == before[COMMON] and packet["exact_parent_reserialize"]
    span = packet["exact_arm_span"]
    at = span["offset"]
    current, installed = (bytes.fromhex(span[field]) for field in ("current_hex", "installed_hex"))
    assert len(current) == len(installed)
    assert before[ARM][at:at + len(current)] == current and arm[at:at + len(installed)] == installed
    restored = arm[:at] + current + arm[at + len(installed):]
    assert restored == before[ARM]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert build.cache_plan(arm) == build.cache_plan(restored)
    old_rows, new_rows = (paired.base.common_rows(common, value) for value in (restored, arm))
    assert old_rows == new_rows
    altered = set()
    new.replace_file(ARM, restored)
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]
    files.write(STORED, dict(candidate_sha256=candidate, predecessor_sha256=previous["candidate_sha256"],
        whole_parent_inverse=True, target_ARM9_sha256=packet["target_ARM9_sha256"],
        target_COMMON_sha256=packet["target_COMMON_sha256"], proof=files.reference(build.OUT),
        unchanged_COMMON=True, exact_arm_span=span))

''',
    "Cargo_storage_warning_preserves_startup": "Deck_skill_guidance_preserves_startup",
    retentions: '''    nearby_ref = live["original_trace_gameplay"]
    assert files.digest(nearby_ref["path"]) == nearby_ref["sha256"]
    nearby = files.read(nearby_ref["path"])
    assert nearby["ordinary_gameplay"] and nearby["candidate_sha256"] == previous["candidate_sha256"]
    retained = nearby["records"] + [live["sea_level_up"]]
    assert len(retained) == 10 and all(all(r["review"].values()) for r in retained)
    for row in retained:
        expected = row["installed_reference"]
        if row["file_path"] == COMMON:
            assert paired.source_ref(new_rows[row["message_ID"]]) == expected
        else:
            at = expected["offset"]
            raw = bytes.fromhex(expected["exact_hex"])
            assert arm[at:at + len(raw)] == raw
''',
})
exec(compile(verify_source, __file__ + "::registered-deck-checks", "exec"),
     vars(parent.parent.parent) | vars(parent.parent) | vars(parent) | globals(), local_checks := {})
verify = local_checks["verify"]


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_palace_investment_wording_predecessor=predecessor, cargo_storage_warning_release=str(REVIEW)":
        "verified_cargo_storage_warning_predecessor=predecessor, deck_skill_guidance_release=str(REVIEW)",
    "len(batches) == 1140 and len(checks) == 475": "len(batches) == 1141 and len(checks) == 476",
    "assert revised == [f'COMMON_MESSAGE_{build.KEY}']":
        "assert revised == [r['id'] for r in outcome['records'] if r['field'] == build.FIELD] and len(revised) == 1",
    "snapshot_scope=[COMMON]": "snapshot_scope=[ARM]",
    "cargo_storage_warning_release_proof=stage.reference(stage.PROOF)": "deck_skill_guidance_release_proof=stage.reference(stage.PROOF)",
    '"cargo_storage_warning_pipeline"': '"deck_skill_guidance_pipeline"',
    "registered_manifest_entries=1141, passing_release_checks=476, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1142, passing_release_checks=477, changed_components=1, changed_internal_files=[ARM]",
    "contextual_records_revisited=5, contextual_decisions_reused=0, previously_localized_records=5":
        "contextual_records_revisited=15, contextual_decisions_reused=0, previously_localized_records=15",
    "prose_revisions=1, justified_retentions=4, text_display_revisions=0, phrase_wrap_adjustments=0":
        "prose_revisions=1, justified_retentions=14, text_display_revisions=0, phrase_wrap_adjustments=0",
    "ordinary_Riga_Cargo_Setup=True, revised_gameplay_holds=2": "ordinary_Riga_Market_Deck_and_departure=True, revised_gameplay_holds=5",
    "prose_revisions=1, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=4":
        "prose_revisions=1, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=14",
    '"cargo_storage_warning_20261124"': '"deck_skill_guidance_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Deck View testing candidate

Deck View now states the skill requirements for navigator duties. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Cargo Setup warning candidate": "Preserve the registered Deck View skill guidance candidate",
    "1,141 entries and 476 passing checks": "1,142 entries and 477 passing checks",
    doc: '''    DOC.write_text(f"""# Deck View navigator skill requirements

Deck View now says each duty has skill requirements and explains that higher skill improves performance. The assignment instructions and the original filter labels retain their wording. The revised paragraph uses its existing allocation and the three existing rows. [Clean and installed text](../{REVIEW.as_posix()})

Paired ordinary Riga gameplay verified five Deck help holds. Thirty-three other screens matched, including the mixed Trade settlement, two departure warnings, Manuel's Helm remark, and Gerhard's at-sea level-up. [Paired Deck view](../{VERIFY.as_posix()}/deck_skill_guidance_paired.png) · [Riga Trade and departure evidence](../translations/editorial_checkpoints/shared_display_20261123/riga_trade_and_departure_20261124.json)

The candidate passed independent startup, 477 registered checks, 17 focused tests, and byte-for-byte reconstruction from the clean input. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::deck-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
