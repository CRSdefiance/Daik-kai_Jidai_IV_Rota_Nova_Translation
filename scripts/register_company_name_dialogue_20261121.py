"""Register the four-route company-name editorial pass."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import observe_company_name_dialogue_20261121 as observed
from scripts import register_all_routes_continuing_phrase_wraps_20261118 as story
from scripts import register_stock_encounter_names_20261121 as parent
from scripts import stage_company_name_dialogue_20261121 as stage
from scripts import verify_company_name_dialogue_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-company-name-dialogue-v1-20261121"
ROOT = Path("out/company_name_dialogue_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Company_Name_Dialogue_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_company_name_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_company_name_dialogue_registered_20261121.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CLEAN = stage.native.CLEAN
QA = stage.ROOT / "qa_passed.xml"
live = SimpleNamespace(PROOF=observed.LIVE)
CHECKPOINT = "Revised 12 company-name lines across four routes and removed four doubled-punctuation cases in Lil’s story."


RAFAEL_DEPARTURE_REVIEW = Path(
    "releases/all_routes_editorial_20261119_rafael_departure_and_debrief_candidate/verification/registered_review.json"
)
RAFAEL_RETENTION_ALIASES = {
    "DK4_MES_B44_R0312": "DK4_MES_B44_R0313",
    "DK4_MES_B44_R0320": "DK4_MES_B44_R0321",
}


def credited_key(row, credited):
    path, ident = row["file_path"], row["id"]
    if (path, ident) in credited:
        return path, ident
    assert path == "/data/SC0.DK4" and row["decision"] == "retention"
    alias = RAFAEL_RETENTION_ALIASES[ident]
    prior, = [r for r in base.load(RAFAEL_DEPARTURE_REVIEW)["records"] if r["id"] == alias]
    assert prior["source_reference"] == row["source_reference"]
    assert prior["source_hex"] == row["source_hex"] and prior["english"] == row["english"]
    for field in ("command_offset", "offset", "exact_stored_hex"):
        assert prior["registered_reference"][field] == row["current_reference"][field]
    return path, alias


def verify(registry, previous, viewed):
    stored, draft, report, playback = map(base.load, (stage.PROOF, stage.review.OUTPUT, display.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == report["candidate_sha256"] == playback["candidate_sha256"]
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert stored["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert report["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert report["revision_count"] == 12 and report["fresh_page_count"] == 48 and report["retention_count"] == 61
    assert len(report["punctuation_fixes"]) == 4 and len(playback["holds"]) == 10 and playback["initialized_Lil"]
    assert playback["actual_company_substitution"] and not playback["natural_activation"] and not playback["hardware"]
    assert viewed == {s["path"]: s["sha256"] for s in report["contact_sheets"] + playback["sheets"]} and len(viewed) == 8
    for p, sha in (viewed | playback["evidence"]).items():
        assert base.digest(p) == sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(CLEAN) == previous["clean_input_sha256"]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, prior, target = map(base.NdsImage.open, (CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (prior, target))
    paths = {f"/data/SC{i}.DK4" for i in range(4)}
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == paths
    assert stored["whole_parent_inverse"] and set(stored["changed_blocks"]) == paths
    archives = {p: native.digest(after[p]) for p in paths}
    for path in paths:
        a, b = [native.IlnkContainer.parse(data).blocks for data in (before[path], after[path])]
        assert [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y] == stored["changed_blocks"][path]
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    arm = after[stage.native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]

    startup = parent.parent.startup_release.env["startup_check"].startup_proof
    context = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    exec(compile(getsource(startup), __file__ + "::startup", "exec"), context)
    context["startup_proof"](previous, candidate, arm)

    plans = {(g["file_path"], k): p for g in stored["groups"] for k, p in g["plans"].items()}
    for row in report["checked_records"]:
        qa = plans[row["file_path"], row["id"]]["diagnostics"]
        assert all(w["severity"] == "warning" and w["code"] == "line-break-count" for w in qa)
        row["informational_source_row_differences"] = qa
    binding = checked_text(story.bind, {
        "stage.paired.text_records": "stage.review.paired.precedent.text_records",
        'stage.stage.SPEECH': 'stage.stage.SPEECH',
        "len(retentions) == 134": "len(retentions) == 61",
        'scope += " and initialized Rafael, Lil or Maria excerpt replay"': 'scope += " and initialized Lil excerpt replay"',
        "    name_order(draft, target)\n": "",
    })
    env = story.env | globals() | {"GATES": stage.review.GATES}
    exec(compile(binding, __file__ + "::registered-dialogue", "exec"), env)
    reviewed = env["bind"](draft, stored, report, playback, after, archives)
    reviewed.update(checked_story_format_guard=controls, direct_visual_review=viewed,
        formatting_and_registration_pending=False, retained_count=61, revision_count=12,
        punctuation_fixes=report["punctuation_fixes"], new_contextual_credit=0,
        unresolved_companion_source_pairings=base.load(stage.review.SOURCE)["additional_command_alignment_needed"],
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(reviewed)
    return stored, reviewed, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
changed = template[template.index("    ids = manifest"):template.index('    manifest["stock_encounter_names_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 969 and len(manifest["checks"]) == 304':
        'len(manifest["batches"]) == 970 and len(manifest["checks"]) == 305',
    'release_stack_before_stock_encounter_names.json': 'release_stack_before_company_name_dialogue.json',
    'release_stack_with_stock_encounter_names.json': 'release_stack_with_company_name_dialogue.json',
    'stage.ROOT / "research.xdelta"': 'stage.ROOT / "translation.xdelta"',
    'live.PROOF, args.visual_review,': 'live.PROOF, display.PROOF, observed.SETUP, args.visual_review,',
    'verified_maria_starter_ship_names_predecessor=predecessor, stock_encounter_names_release=str(REVIEW)':
        'verified_stock_encounter_names_predecessor=predecessor, company_name_dialogue_release=str(REVIEW)',
    'registered_stock_encounter_names_and_complete_parent_inverse': 'registered_company_name_dialogue_and_complete_parent_inverse',
    'manifest["stock_encounter_names_pipeline"]': 'manifest["company_name_dialogue_pipeline"]',
    changed: '''    for row in draft["records"]:
        path, ident = row["file_path"], row["id"]
        assert credited_key(row, credited) in credited
        if row["decision"] == "revision" and ident not in manifest["changed_records"][path]:
            manifest["changed_records"][path].append(ident)
''',
    'original_ship_model_ids=True, target_ARM9_sha256=archives[stage.ARM]':
        'original_company_substitution_order=True, archive_hashes=archives, Rafael_retention_credit_aliases=RAFAEL_RETENTION_ALIASES, target_ARM9_sha256=previous["target_ARM9_sha256"]',
    'changed_components=1, target_ARM9_sha256=archives[stage.ARM]':
        'changed_components=4, target_ARM9_sha256=previous["target_ARM9_sha256"]',
    'reviewed_UI_labels=5, previously_localized_records=5, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'reviewed_UI_labels=0, previously_localized_records=73, new_contextual_records=0, prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=61',
    'name_label_revisions=5, text_display_revisions=0, pagination_fixes=0, name_consistency_revisions=5':
        'name_label_revisions=0, text_display_revisions=4, pagination_fixes=0, name_consistency_revisions=0',
    'initialized_Ghost_Ship_inspection=True, native_victory_portraits=25, natural_victory=False':
        'initialized_Lil_company_name_dialogue=True, native_default_and_stress_pages=48, natural_activation=False',
    'ledger["stock_encounter_names_20261121"]': 'ledger["company_name_dialogue_20261121"]',
    'prior_records_reviewed=5, actual_inspection_control=1, offline_victory_portraits=25, new_contextual_credit=0, name_label_revisions=5':
        'prior_records_reviewed=73, actual_Lil_panels=10, offline_pages=48, new_contextual_credit=0',
    'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0, text_display_revisions=0)':
        'prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=61, text_display_revisions=4)',
    'parent.ROM]\n    for path in candidates:': 'parent.ROM, observed.ROM]\n    for path in candidates:',
    'Preserve the stock encounter names candidate or research ROM': 'Preserve the company-name editorial candidate or replay ROM',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Company-name dialogue testing candidate

The [testing ROM](../../{ROM.as_posix()}) improves 12 company-name lines across all four routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Company-name dialogue and wraps

The pass reviewed 73 turns, revised 12 and retained 61. Four Lil lines now place Argot Co. inside a sentence without adding extra periods to the company name. Rafael and Lil hear the same Genoa guild message. Hodram and Maria hear the same recognition and permission at the gate. [Exact source and registered references](../{REVIEW.as_posix()})

All 48 default and width-stress pages passed native checks and visual review. An initialized Lil excerpt displayed ten panels, including all four punctuation fixes, then advanced into the following tutorial. The other revised lines and the alternate name widths received offline coverage. Two additional source blocks with inserted commands remain outside this review. Natural scene activation and hardware remain open.

The release preserves all accepted layers and the ASCII right-bound correction. Six startup holds, 24 protected name getters and 17 focused tests passed. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
