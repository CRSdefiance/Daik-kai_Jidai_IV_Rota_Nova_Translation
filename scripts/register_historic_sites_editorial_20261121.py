"""Register the source-reviewed Historic Sites Gallery pass."""

from pathlib import Path
from inspect import getsource
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_hangzhou_veracruz_trends_20261121 as parent
from scripts import register_sailing_help_20261120 as startup_release
from scripts import stage_historic_sites_editorial_20261121 as stage
from scripts.checkpoint_shared_display_worklist_20261120 import COMMON
from scripts.reconcile_shared_display_20261121 import OUTPUT as PENDING, workflow as shared
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
PROFILE = "all-routes-historic-sites-editorial-v1-20261121"
ROOT = Path("out/historic_sites_editorial_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Historic_Sites_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_historic_sites_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_historic_sites_registered_20261121.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
QA = stage.ROOT / "qa_passed.xml"
live = SimpleNamespace(PROOF=stage.LIVE)
CHECKPOINT = "Registered six Historic Sites prose corrections and seven wrap fixes after reviewing all 19 Gallery pages."


def verify(registry, previous, viewed):
    draft, observed = map(base.load, (stage.PROOF, stage.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == draft["candidate_sha256"] == observed["candidate_sha256"]
    assert base.digest(stage.CLEAN) == draft["clean_input_sha256"] == previous["clean_input_sha256"]
    assert base.digest(parent.ROM) == draft["parent_sha256"] == previous["candidate_sha256"]
    assert observed["actual_original_viewer"] and observed["carousel_wrap"] and observed["initialized_collection"]
    assert not observed["natural_site_discoveries_observed"] and not observed["hardware"]
    assert viewed == observed["sheets"] and len(viewed) == 4
    assert all(base.digest(path) == value for group in (viewed, observed["evidence"], draft["source_proofs"])
               for path, value in group.items())
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, predecessor, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (predecessor, target))
    assert before.keys() == after.keys() and {k for k in before if before[k] != after[k]} == {stage.ARM}
    arm, common = after[stage.ARM], after[COMMON]
    expected, staged_records, unused = stage.transform(clean.read_file(stage.ARM), before[stage.ARM])
    assert arm == expected and draft["records"] == staged_records and unused == draft["unused_ranges"]
    assert native.digest(arm) == draft["target_ARM9_sha256"]
    assert native.digest(common) == previous["target_COMMON_sha256"]
    old_sections = MainCodeFile(before[stage.ARM], stage.BASE).sections
    new_sections = MainCodeFile(arm, stage.BASE).sections
    assert [(section.ramAddress, len(section.data), section.bssSize) for section in old_sections] == [
        (section.ramAddress, len(section.data), section.bssSize) for section in new_sections
    ]
    assert all(a.data == b.data for a, b in zip(old_sections[1:], new_sections[1:], strict=True))
    itcm, = (section.data for section in new_sections if section.ramAddress == 0x01FFC000)
    bounds = base.load(Path(previous["right_bound_configuration"]))["proof"]["patches"]
    old_itcm_physical = bounds[0]["offset"] - 0x21C
    for patch in bounds:
        at, data = patch["offset"], bytes.fromhex(patch["after_hex"])
        if old_itcm_physical <= at < old_itcm_physical + len(itcm):
            offset = at - old_itcm_physical
            assert itcm[offset:offset + len(data)] == data
        else:
            assert arm[at:at + len(data)] == data
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    directory = native.digest(arm[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    installed = shared.owned_entries(common, arm, directory)
    pending = base.load(PENDING)
    assert pending["candidate_sha256"] == previous["candidate_sha256"] and len(pending["records"]) == 276
    for row in pending["records"]:
        now = installed[row["message_ID"]]
        assert shared.reference(now) == row["current_reference"] and now.text.hex() == row["current_hex"]

    startup = startup_release.env["startup_check"].startup_proof
    env = startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE}
    startup_program = checked_text(getsource(startup), {
        "original_ARM9_and_overlay_preserved=True, hardware=False,":
            "original_ARM9_and_overlay_preserved=False, ARM9_text_and_pointer_change_only=True, "
            "original_overlay_preserved=True, hardware=False,",
    })
    exec(compile(startup_program, __file__ + "::startup", "exec"), env)
    env["startup_proof"](previous, candidate, arm)
    pages = {row["site_id"]: row for row in observed["pages"]}
    assert len(pages) == 19 == len(staged_records)
    assert [sum(row["finding"] == value for row in staged_records)
            for value in ("prose", "wrap", "exact retention")] == [6, 7, 6]
    for row in staged_records:
        page = pages[row["site_id"]]
        assert page["complete_title"] and page["native_page"]["lines"] == row["native_lines"]
        row["review"]["formatting"] = True
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": candidate}
        row["gameplay_frame"] = page["frame"]
        title = row["caption"]
        title_at = unpack_from("<I", arm, title["pointer_field"])[0] - stage.BASE
        exact = stage.c_string(arm, title_at)
        assert exact == title["english"].encode("ascii") + b"\0"
        title.update(registered_offset=title_at, registered_hex=exact.hex(), review=row["review"].copy())
    review = draft | dict(encoder="dialogue-relocatable-v1", native_formatter=draft["encoder"],
                         records=staged_records, checked_story_format_guard=controls,
                         observed_gameplay=observed, direct_visual_review=viewed, new_contextual_credit=0,
                         unchanged_pending_records=276, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(review)
    return draft, review, {stage.ARM: draft["target_ARM9_sha256"]}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
credit_rows = template[template.index('    for row in draft["records"]:'):template.index('    manifest["hangzhou_veracruz_trends_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 964 and len(manifest["checks"]) == 299':
        'len(manifest["batches"]) == 965 and len(manifest["checks"]) == 300',
    'live.PROOF, NATIVE, args.visual_review': 'live.PROOF, args.visual_review',
    'release_stack_before_hangzhou_veracruz_trends.json': 'release_stack_before_historic_sites.json',
    'release_stack_with_hangzhou_veracruz_trends.json': 'release_stack_with_historic_sites.json',
    'verified_havana_calicut_istanbul_predecessor=predecessor, hangzhou_veracruz_trends_release=str(REVIEW)':
        'verified_hangzhou_veracruz_predecessor=predecessor, historic_sites_editorial_release=str(REVIEW)',
    'registered_hangzhou_veracruz_trends_and_complete_parent_inverse': 'registered_historic_sites_editorial_and_complete_parent_inverse',
    'manifest["hangzhou_veracruz_trends_pipeline"]': 'manifest["historic_sites_editorial_pipeline"]',
    credit_rows: '''    ids = manifest["changed_records"][stage.ARM]
    for row in draft["records"]:
        if row["display_changed"] and row["id"] not in ids:
            ids.append(row["id"])
''',
    'owned_story_blocks=stored["changed_blocks"], target_story_archive_sha256=archives':
        'original_gallery_pool=True, target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=4,': 'changed_components=1, target_ARM9_sha256=archives[stage.ARM],',
    'previously_localized_records=125, new_contextual_records=0, prose_revisions=48, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=76':
        'previously_localized_records=19, new_contextual_records=0, prose_revisions=6, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=6',
    'initialized_Maria_dialogue_panels=31, host_route="Lil", revised_replies_observed=16, dialogue_exits=True, natural_town_trigger=False':
        'initialized_discovery_collection=True, original_Gallery_pages=19, changed_pages=13, carousel_wrap_and_back=True, natural_discovery=False',
    'ledger["hangzhou_veracruz_trends_20261121"]': 'ledger["historic_sites_editorial_20261121"]',
    'prior_records_reviewed=125, initialized_emulator_records=31, new_contextual_credit=0,\n        prose_revisions=48, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=76':
        'prior_records_reviewed=19, initialized_emulator_records=19, new_contextual_credit=0,\n        prose_revisions=6, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=6',
    'parent.ROM, *stage.ROOT.rglob("*.nds"), *(p for p in stage.review.ROOT.rglob("*.nds") if p.stat().st_size > 512)':
        'parent.ROM, *(path for stage_root in (stage.PREVIEW, *stage.LAYOUT_TRIALS) for path in stage_root.glob("*.nds"))',
    'Preserve the town dialogue candidate or research fixture': 'Preserve the Historic Sites candidate or its earlier stage',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Historic Sites Gallery testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the complete Historic Sites editorial pass. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Historic Sites Gallery editorial review

Reviewed all 19 available descriptions and their titles from the clean Japanese. Six descriptions change, seven keep the wording with improved wrapping, and six retain their exact text bytes. The Parthenon description now specifies Athena's statue. The Colosseum description restores the arena's capacity for large crowds. The revised wrapping keeps the relevant dates and influence amounts together. [Exact references and decisions](../{REVIEW.as_posix()})

The original Gallery drew all 19 titles and pages in paired cold boots using a copied save initialized with the supported collection. Complete glyph masks, carousel wrap and Back passed. Natural discovery and hardware were outside these replays. Two original slots have no Gallery image. Their placeholders carry forward. [Emulator evidence](../{VERIFY.as_posix()})

The candidate uses the existing Gallery allocation and reconstructs byte for byte from the clean ROM. Six startup holds, 24 protected getters and 17 focused tests passed. Five older Gallery tests require the unavailable V157 fixture. The current Gallery replay covers the affected screen. All 276 pending shared entries remain intact. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
