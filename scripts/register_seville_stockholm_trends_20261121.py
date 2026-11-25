"""Register the two reviewed town exchanges over the current cumulative candidate."""

from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_final_early_wrap_leads_20261121 as parent
from scripts import replay_seville_stockholm_trends_20261121 as game
from scripts import stage_seville_stockholm_trends_20261121 as stage
from scripts import verify_seville_stockholm_trends_20261121 as offline
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
live = SimpleNamespace(PROOF=game.LIVE)
NATIVE = offline.PROOF
PROFILE = "all-routes-seville-stockholm-trends-v1-20261121"
ROOT = Path("out/seville_stockholm_trends_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Seville_Stockholm_Trends_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_seville_stockholm_trends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_seville_stockholm_trends_registered_20261121.md")
STARTUP, QA = (stage.ROOT / name for name in ("own_startup_verification.json", "qa_passed.xml"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered the Seville banana and Stockholm fur exchanges across all four routes."


def verify(registry, previous, viewed):
    stored, display, actual = map(base.load, (stage.PROOF, offline.PROOF, game.LIVE))
    draft, source = map(base.load, (stage.review.OUTPUT, stage.review.SOURCE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == display["candidate_sha256"] == actual["candidate_sha256"]
    assert stored["predecessor_sha256"] == base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    assert base.digest(stage.review.OUTPUT) == stored["manuscript_sha256"]
    assert base.digest(stage.review.SOURCE) == draft["source_packet_sha256"]
    assert base.digest(stage.PROOF) == display["stage_proof_sha256"]
    assert len(viewed) == 5 and viewed == {s["path"]: s["sha256"] for s in display["contact_sheets"]} | actual["sheet"]
    assert all(base.digest(p) == digest for p, digest in (viewed | actual["evidence"]).items())
    assert stored["whole_parent_inverse"] and (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert actual["initialized_scene"] and not actual["natural_town_trigger"] and not actual["hardware"]
    assert [len(v["records"]) for v in actual["cases"].values()] == [10, 8]
    assert all(len(v["matched_entry_and_return_framebuffers"]) == 4 for v in actual["cases"].values())
    assert display["displayed_native_plans"] == 26 and display["exact_retentions"] == 46
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, prior, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (prior, target))
    assert before.keys() == after.keys()
    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}
    assert archives.keys() == {name for name in before if before[name] != after[name]}
    assert native.digest(after[native.ARM]) == previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls == stored["source25"]
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    banks = {path: [native.IlnkContainer.parse(payload).blocks for payload in
                    (clean.read_file(path), before[path], after[path])] for path in archives}
    for route, (path, (_, old, new)) in enumerate(banks.items()):
        assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == list(stage.review.BLOCKS[route])
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()

    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    verified = {(r["file_path"], r["id"]): r for r in display["receipts"]}
    observed = {r["id"] for c in actual["cases"].values() for r in c["records"]}
    for group, indexed in zip(stored["groups"], source["groups"], strict=True):
        path, n = group["file_path"], group["block"]
        original, previous_bank, new = banks[path]
        assert native.digest(original[n]) == group["source"] == indexed["source_block_sha256"]
        assert native.digest(previous_bank[n]) == group["before"] == indexed["current_block_sha256"]
        assert native.digest(new[n]) == group["after"]
        for cmd in group["commands"]:
            offset, raw = cmd["stored_offset"], bytes.fromhex(cmd["stored"])
            assert new[n][offset:offset + len(raw)] == raw
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row, receipt = rows[path, ident], verified[path, ident]
            body = raw[5:raw.index(0, 6)]
            assert body[0] == row["source_selector"]
            if row["decision"] == "revision":
                assert receipt["target_hex"] == body.hex() and len(receipt["pages"]) == 1
            else:
                assert receipt["kept_complete_command"] == cmd and body.hex() == row["current_hex"]
            row["review"]["formatting"] = True
            row["registered_reference"] = dict(candidate_sha256=candidate, file_path=path, block=n,
                command_offset=offset, offset=offset + 5, exact_stored_hex=body.hex())
            row["initialized_emulator_excerpt_observed"] = group["route"] == 2 and ident in observed
    assert len(rows) == len(verified) == 72 and rows.keys() == verified.keys()
    assert Counter(r["finding"] for r in rows.values()) == {"prose": 23, "wrap": 3, "retention": 46}
    assert sum(r["initialized_emulator_excerpt_observed"] for r in rows.values()) == 18
    assert all(r["review"]["formatting"] for r in rows.values())
    validate_natural_dialogue_batch(draft)
    startup_proof = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                                 {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})
    startup_proof(previous, candidate, after[native.ARM])
    draft.update(candidate_sha256=candidate, checked_story_format_guard=controls, paired_coverage=actual,
                 formatting_and_registration_pending=False, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],
                 unchanged_COMMON_and_ARM9=True, new_contextual_credit=0, native_proof_sha256=base.digest(offline.PROOF))
    return stored, draft, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 959 and len(manifest["checks"]) == 294':
        'len(manifest["batches"]) == 960 and len(manifest["checks"]) == 295',
    "release_stack_before_final_early_wrap_leads.json": "release_stack_before_seville_stockholm_trends.json",
    "release_stack_with_final_early_wrap_leads.json": "release_stack_with_seville_stockholm_trends.json",
    "verified_item_advice_predecessor=predecessor, final_early_wrap_leads_release=str(REVIEW)":
        "verified_early_wrap_predecessor=predecessor, seville_stockholm_trends_release=str(REVIEW)",
    "registered_final_early_wrap_leads_and_complete_parent_inverse": "registered_seville_stockholm_trends_and_complete_parent_inverse",
    'manifest["final_early_wrap_leads_pipeline"]': 'manifest["seville_stockholm_trends_pipeline"]',
    'owned_message_IDs=sorted(stage.EDITS), target_COMMON_sha256=archives[stage.COMMON]':
        'owned_story_blocks=stored["changed_blocks"], target_story_archive_sha256=archives',
    'changed_components=1, target_COMMON_sha256=archives[stage.COMMON]': 'changed_components=4',
    "previously_localized_records=37, new_contextual_records=0, prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=32":
        "previously_localized_records=72, new_contextual_records=0, prose_revisions=23, spacing_revisions=0, wrap_only_revisions=3, justified_retentions=46",
    "focused_shark_dialogue=3, revised_replies_observed=1, original_raise_choice_and_sailing_return=True":
        "initialized_Lil_town_panels=18, revised_replies_observed=4, original_scene_returns=True, natural_town_trigger=False",
    'ledger["final_early_wrap_leads_20261121"]': 'ledger["seville_stockholm_trends_20261121"]',
    "prior_records_reviewed=37, actual_gameplay_records=3":
        "prior_records_reviewed=72, initialized_emulator_records=18",
    "prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=32, text_display_revisions=0":
        "prose_revisions=23, spacing_revisions=0, wrap_only_revisions=3, justified_retentions=46, text_display_revisions=0",
    "                  parent.ROM]": '                  parent.ROM, *stage.review.ROOT.rglob("*.nds")]',
    "Preserve the early-wrap candidate or reconstruction": "Preserve the town dialogue candidate or research fixture",
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Seville and Stockholm town dialogue candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised Seville and Stockholm town scenes on all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Seville bananas and Stockholm furs

Reviewed all 18 turns of the two scenes in each storyline. The Seville exchange keeps the cook's change from courtesy to dry acknowledgment and the owner's confidence and laugh. The Stockholm exchange preserves the wish for a fur coat and the reported sales and price increases. Retained the native Owner, Cook, Man and Woman nameplates. The ledger has 23 wording revisions, three wrap-only changes and 46 individual retentions. [Record-level review](../{REVIEW.as_posix()})

All 26 revised pages passed native and visual review. The paired Lil replays used the original scene commands after the original startup prelude. All 18 panels matched their expected holds, including four revised panels and both scene returns. Natural town triggers and hardware remain unvisited in this batch. [Display and replay evidence](../{VERIFY.as_posix()})

The patch reconstructs the ROM exactly. Six startup holds, 24 protected getters and 17 focused tests passed. All 114 accepted layers and the existing ASCII right-bound rule carry forward. The ledger remains at 27,700 credited records with 276 shared entries open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
