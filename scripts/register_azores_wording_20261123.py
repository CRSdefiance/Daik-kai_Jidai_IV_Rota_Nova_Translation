"""Register the compact Azores wording repair as a cumulative testing candidate."""

from contextlib import contextmanager
from gzip import GzipFile, open as gzip_open
from hashlib import file_digest
from os import fsync
from pathlib import Path
from shutil import copyfile as copy_bytes
from subprocess import run
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_supply_ratio_hint_20261123 as parent
from scripts import stage_azores_wording_20261123 as azores
from scripts import verify_azores_wording_20261123 as display
from scripts.check_azores_release_inputs_20261123 import PATCH as RESEARCH_PATCH, REBUILT, STARTUP_CAPTURE
from scripts.reconcile_editorial_acceptance_20261123 import right_bound
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow, routes, audit = parent.base, parent.native, parent.workflow, parent.routes, parent.audit
ARM, COMMON = azores.ARM, azores.COMMON
stage = SimpleNamespace(ROM=azores.ROM, PROOF=azores.PROOF, native=native)
EVIDENCE, DISPLAY = display.OUTPUT.parent, display.OUTPUT
PROFILE = "all-routes-azores-wording-v1-20261123"
ROOT, WORK = azores.ROOT / "registered", azores.ROOT / "registration"
LEDGER_NEXT = Path("E:/Rota Nova translations/Generated/work/azores_wording_registration_20261123/ledger_after.json.gz")
ROM = ROOT / "Translation_DS_Azores_Wording_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_azores_wording_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_azores_wording_registered_20261123.md")
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
CHECKPOINT = "Registered the corrected Azores discovery, docking voices and chief's request."
REGISTRY_BACKUP = parent.WORK / "release_stack_with_supply_ratio_hint.json"
LEDGER_BACKUP = parent.WORK / "ledger_after.json"
previous_plan = base.load(parent.VERIFY / "registration_mutation_plan.json")
storage = dict(candidate_sha256=base.load(parent.RELEASE)["candidate_sha256"],
               registry_sha256=previous_plan["registry_after"], ledger_sha256=previous_plan["ledger_after"])
guard_spec, link_snapshot = parent.guard_spec, parent.link_snapshot


def snapshot_digest(path):
    if path.suffix != ".gz":
        return base.digest(path)
    with gzip_open(path, "rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


@contextmanager
def mapped(path):
    if path.suffix == ".gz":
        with gzip_open(path, "rb") as stream:
            yield stream.read()
    else:
        with parent.scope["mapped"](path) as data:
            yield data


class PreparedOutput:
    def __init__(self, path):
        self.path = path

    @contextmanager
    def open(self, mode):
        assert mode == "xb"
        compressed = self.path.suffix == ".gz"
        if not self.path.exists():
            with self.path.open(mode) as raw:
                if compressed:
                    with GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
                        yield stream
                else:
                    yield raw
            return

        class Resume:
            def __init__(self, stream):
                self.stream = stream

            def write(self, payload):
                prior = self.stream.read(len(payload))
                assert payload.startswith(prior), "Existing transaction prefix differs"
                if len(prior) < len(payload):
                    assert not compressed, "A complete compressed snapshot is required"
                    assert self.stream.write(payload[len(prior):]) == len(payload) - len(prior)
                return len(payload)

        opened = gzip_open(self.path, "rb") if compressed else self.path.open("r+b")
        with opened as stream:
            yield Resume(stream)
            assert not stream.read(1), "Existing transaction contains trailing data"


def write_update(data, path, edits):
    parent.scope["write_update"](data, PreparedOutput(path), edits)


def copyfile(source, target):
    if not target.exists():
        copy_bytes(source, target)
    assert base.digest(source) == base.digest(target)


def reuse_link(source, target, expected):
    if not target.exists():
        link_snapshot(source, target, expected)
    assert target.samefile(source) and base.digest(target) == expected


def copy_in_place(source, destination):
    if source.suffix != ".gz":
        parent.copy_in_place(source, destination)
        return
    expected = snapshot_digest(source)
    with gzip_open(source, "rb") as original, destination.open("r+b") as live:
        position = 0
        while payload := original.read(1 << 20):
            live.seek(position)
            if live.read(len(payload)) != payload:
                live.seek(position)
                assert live.write(payload) == len(payload)
            position += len(payload)
        if destination.stat().st_size != position:
            live.truncate(position)
        live.flush()
        fsync(live.fileno())
    assert base.digest(destination) == expected

startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_source = checked_text(parent.startup_source, {
    "only_supply_ratio_hint_slot_changed": "compact_azores_payload_exact_and_startup_extent_preserved",
})
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["native_name_layouts"])


def observed_count():
    return sum(len(case["complete_revised_pages"]) for case in base.load(DISPLAY)["ordinary_replays"].values())


def verify(registry, previous, viewed):
    stored, observed, proof = map(base.load, (stage.PROOF, DISPLAY, EVIDENCE / "clean_patch_proof.json"))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == observed["candidate_sha256"] == proof["candidate_sha256"]
    assert stage.ROM.samefile(REBUILT) and proof["exact_byte_roundtrip"]
    assert base.digest(RESEARCH_PATCH) == proof["patch_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["predecessor"]["sha256"]
    assert stored["whole_parent_inverse"] and storage["candidate_sha256"] == previous["candidate_sha256"]
    sheets = [*observed["native_context_sheets"], *(case["sheet"] for case in observed["ordinary_replays"].values())]
    assert viewed == {sheet["path"]: sheet["sha256"] for sheet in sheets}
    assert all(base.digest(path) == expected for path, expected in viewed.items())
    for case in observed["ordinary_replays"].values():
        record = case["capture"]
        assert base.digest(record["path"]) == record["sha256"]
    assert native_count() == 168 and observed_count() == 6
    assert observed["native_getter_and_call_site_flag_cases"] == 768
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"] == proof["clean_input_sha256"]
    clean, old, new = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, old, new))
    stored["changed_files"] = stored["modified_paths"]
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == {ARM, COMMON}
    hashes = {path: native.digest(after[path]) for path in (ARM, COMMON, *routes.ROUTES)}
    assert hashes[ARM] == stored["target_ARM9_sha256"] and hashes[COMMON] == stored["target_COMMON_sha256"]
    assert right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    for path in stored["changed_files"]:
        new.replace_file(path, before[path])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = bind_registered_story_percent_guard(guard)(source, after)
    assert checks["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous, candidate, after[ARM])

    earlier = base.load(parent.REVIEW)
    binding = earlier["shared_consumer_binding"]
    assert len(binding["records"]) == 276 and binding["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(routes.OUT) == earlier["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == earlier["retained_editorial_coverage_sha256"]
    census = base.load(routes.OUT)
    assert all(hashes[path] == census["routes"][path]["installed_archive_sha256"] for path in routes.ROUTES)
    original = azores.common_rows(before[COMMON], before[ARM])
    installed = azores.common_rows(after[COMMON], after[ARM])
    japanese = common_message_entries(source[COMMON], source[ARM])
    assert all(original[row["message_ID"]] == installed[row["message_ID"]] for row in binding["records"])
    records = observed["staged_source_reviewed_records"]
    for record in records:
        if record["file_path"] == COMMON:
            key = record["message_ID"]
            assert record["source_hex"] == japanese[key].text.hex()
            assert record["installed_hex"] == original[key].text.hex()
            assert record["staged_hex"] == installed[key].text.hex()
        record["source_review_decision"] = record["decision"]
        record["decision"] = "revision" if record["decision"].startswith("revise ") else "retention"
    result = observed | dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(records[0]["review"]), records=records,
        visual_review=viewed, checked_story_format_guard=checks, registered_installation_pending=False,
        shared_consumer_binding=binding | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=base.digest(routes.OUT), retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), justified_retentions=5,
        ordinary_cases="Hodram's Azores voyage, both Promised Words outcomes",
        unvisited="Other five docking voices in ordinary play, naturally earned shortages, physical hardware",
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return stored, result, hashes


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    '    assert not any(p.exists() for p in (ROOT, PACKAGE, DOC, registry_next, ledger_next))':
        '    assert not DOC.exists() and not (VERIFY / "registration_mutation_plan.json").exists()',
    '    ROOT.mkdir()': '    ROOT.mkdir(exist_ok=True)',
    '    WORK.mkdir()': '    WORK.mkdir(exist_ok=True)\n    LEDGER_NEXT.parent.mkdir(parents=True, exist_ok=True)',
    '    VERIFY.mkdir(parents=True)': '    VERIFY.mkdir(parents=True, exist_ok=True)\n    run(["compact.exe", "/C", f"/S:{ROOT}"], check=True)',
    '    link_snapshot(REBUILT, ROM, candidate)': '    reuse_link(REBUILT, ROM, candidate)',
    '        assert not target.exists()\n        copyfile(source, target)': '        copyfile(source, target)',
    'registry_sha = base.digest(registry_next)': 'registry_sha = snapshot_digest(registry_next)',
    'ledger_after=base.digest(ledger_next)': 'ledger_after=snapshot_digest(ledger_next)',
    '    archive(registry_next, PACKAGE / "build_release_stack.json.gz")':
        '    reuse_link(registry_next, PACKAGE / "build_release_stack.json.gz", base.digest(registry_next))\n'
        '    assert snapshot_digest(PACKAGE / "build_release_stack.json.gz") == registry_sha',
    'len(batches) == 1100 and len(checks) == 435': 'len(batches) == 1101 and len(checks) == 436',
    'assert len(checks) == 436\n': 'assert len(checks) == 437\n',
    'changed_components=1': 'changed_components=2',
    'repository_tests=17, legacy_fixture_tests_skipped=0, reviewed_UI_labels=1': 'repository_tests=17, legacy_fixture_tests_skipped=0, reviewed_UI_labels=0',
    'previously_localized_records=0, contextual_records_revisited=1, contextual_decisions_reused=0, new_contextual_records=1, prose_revisions=0':
        'previously_localized_records=8, contextual_records_revisited=8, contextual_decisions_reused=8, new_contextual_records=0, prose_revisions=3',
    'new_reviewed_UI_slots=1, contextual_decisions_reused=0, observed_supply_ratio_holds':
        'new_reviewed_UI_slots=0, contextual_decisions_reused=8, observed_azores_holds',
    'prose_revisions=0, spacing_revisions=0, punctuation_glyph_corrections=0, ui_label_revisions=1, justified_retentions=0':
        'prose_revisions=3, spacing_revisions=0, punctuation_glyph_corrections=0, ui_label_revisions=0, justified_retentions=5',
    'wrap_only_revisions=0, justified_retentions=0, name_label_revisions=0, text_display_revisions=1':
        'wrap_only_revisions=0, justified_retentions=5, name_label_revisions=0, text_display_revisions=7',
    'focused_supply_ratio_fixture=True': 'ordinary_azores_replays=True',
    'verified_sound_play_stop_predecessor': 'verified_supply_ratio_hint_predecessor',
    '    archive(ledger_backup, ROOT / "editorial_ledger_before.json.gz")':
        '    assert base.digest(ledger_backup) == snapshot["ledger_before"]',
    'stage.PROOF, STARTUP, QA, DISPLAY, routes.OUT': 'stage.PROOF, STARTUP, QA, DISPLAY, EVIDENCE / "clean_patch_proof.json", routes.OUT',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Azores wording testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses **the Azores** in discovery and docking and restores Manuel's **Admiral**. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("supply_ratio_hint_release", "azores_wording_release").replace("registered_supply_ratio_hint_and", "registered_azores_wording_and").replace(
    "supply_ratio_hint_pipeline", "azores_wording_pipeline").replace("release_stack_with_supply_ratio_hint.json",
    "release_stack_with_azores_wording.json.gz").replace('added_field(data, "supply_ratio_hint_20261123"', 'added_field(data, "azores_wording_20261123"').replace(
        'WORK / "ledger_after.json"', 'LEDGER_NEXT')

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'base.digest(registry_next)': 'snapshot_digest(registry_next)',
    'base.digest(ledger_next)': 'snapshot_digest(ledger_next)',
    "Preserve the Supply Ratio candidate and its predecessor": "Preserve the Azores wording candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Azores discovery and docking wording

Two ordinary controller replays from the Lisbon save verify **Discovered the Azores.**, **Shall we stop at the Azores?** and Manuel's address **Admiral**. The original choices and both Promised Words outcomes remain visible. Offline checks cover all 24 villages, seven templates and the register and flag behavior at both name call sites. Five template retentions explain the source and voice. [Source and visual evidence](../{REVIEW.as_posix()})

The first test build reproduced the known startup stall after extending the late-copy pool. The registered build reuses exactly 64 bytes from an earlier startup routine that has no external literal or branch references in the current image. The original pool size, arena bounds and active startup routine stay exact. Six cold-start frames, 24 protected getters, all 17 focused tests and the complete clean-input byte comparison passed. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("release_stack_with_supply_ratio_hint.json", "release_stack_with_azores_wording.json.gz").replace(
    'WORK / "ledger_after.json"', 'LEDGER_NEXT')

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
