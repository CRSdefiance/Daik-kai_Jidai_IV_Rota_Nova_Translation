"""Register the Amsterdam Tavern price rendering correction over Hamburg."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_tavern_round_digits_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_damaged_save_digits_20261120 as precedent
from scripts import stage_tavern_round_digits_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, parent = stage.base, stage.batch, stage.parent
PROFILE = "all-routes-tavern-round-digits-v1-20261120"
ROOT = Path("out/tavern_round_digits_registered_20261120_v1")
ROM = ROOT / "Translation_DS_Tavern_Round_Digits_20261120_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261120_tavern_round_digits_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_tavern_round_digits_registered_20261120.md")
STARTUP, QA = (stage.ROOT / name for name in ("own_startup_verification.json", "qa.xml"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered regular-width price digits for Treat Everyone in the Tavern."


def verify(registry, previous, viewed):
    stored, result, offline, getter = map(base.load, (stage.PROOF, game.PROOF, game.NATIVE, game.GETTER))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == result["candidate_sha256"] == offline["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["parent_sha256"] == result["parent_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    assert stored["whole_parent_inverse"] and stored["clean_input_patch_byte_exact"]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / "translation.xdelta") == stored["clean_input_patch_sha256"]
    assert base.digest(stage.tavern.OUTPUT) == stored["prior_gameplay_sha256"]
    assert viewed == result["sheets"] and len(viewed) == len(offline["sheets"]) + 1
    assert all(base.digest(p) == sha for p, sha in (viewed | result["evidence"]).items())
    assert [r["frame"] for r in result["observed_holds"] if r["changed_body_bounds"]] == list(game.CONFIRMATIONS)
    assert (result["declined_wallet"], result["accepted_wallet"], result["price"]) == (34980, 34712, 268)
    assert result["physically_identical_other_samples"] and result["ordinary_Amsterdam_gameplay"]
    assert len(offline["native_ring_cases"]) == 256 and len(offline["offline_rendered_pages"]) == 56
    assert len(offline["original_voice_selector"]) == 8 and len(offline["initialized_stock_town_growth"]) == 90
    assert getter["candidate_sha256"] == candidate
    assert [row["message_ID"] for row in getter["original_getter_cases"]] == list(game.RECORDS)
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [32, 0, 0, 2]

    clean, prior, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM, stage.COMMON}
    arm, common = after[stage.ARM], after[stage.COMMON]
    rebuilt, change = stage.patch(before[stage.ARM], clean.read_file(stage.ARM))
    assert rebuilt == arm and change == stored["changed_call"] and batch.digest(arm) == stored["target_ARM9_sha256"]
    expected, table, allocations = stage.deploy_text(before[stage.COMMON], arm)
    assert expected == common and {str(n): slot for n, slot in allocations.items()} == stored["COMMON_allocations"]
    assert batch.digest(common) == stored["target_COMMON_sha256"]
    assert batch.digest(before[stage.COMMON]) == previous["target_COMMON_sha256"]
    target.replace_file(stage.ARM, before[stage.ARM])
    target.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    directory = batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET])
    previous_table = batch.owned_entries(before[stage.COMMON], arm, directory)
    pending = base.load(precedent.WORKLIST)["records"]
    assert len(pending) == 276
    for item in pending:
        entry = table[item["message_ID"]]
        assert batch.reference(entry) == item["current_reference"] and entry.text.hex() == item["current_hex"]

    records = result["records"]
    assert [r["message_ID"] for r in records] == [*game.RECORDS, 866, 872, 874, 880]
    for row in records:
        n = row["message_ID"]
        predecessor, final = previous_table[n], table[n]
        assert batch.reference(predecessor) == row["current_reference"] and predecessor.text.hex() == row["current_hex"]
        assert batch.reference(final) == row["final_reference"] and final.text.hex() == row["final_hex"]
        assert (row["decision"] == "revision") == (n in stage.REVISIONS)
        row["registered_reference"] = row["final_reference"] | {"candidate_sha256": candidate}
    assert all(row["exact_installed_hex"] == table[row["message_ID"]].text.hex() for row in getter["original_getter_cases"])
    records.append(dict(id="DK4_TAVERN_ROUND_PRICE_DIGITS", file_path=stage.ARM, decision="revision",
        speaker="Sailor", english="{price}", context="The original Tavern helper supplies an estimate to the original confirmation menu.",
        source_meaning="The selected round costs the original computed gold amount, subject to captain approval.",
        localization_note="Use a regular-width price in the same number buffer and preserve the amount, voice choice and transactions.",
        source_reference={"call": stage.CALL, "target": stage.runtime.NUMBER, "hex": change["previous_hex"]},
        current_reference=change | {"candidate_sha256": candidate}, review=dict.fromkeys(batch.GATES, True)))
    draft = result | dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=batch.GATES, records=records,
        checked_story_format_guard=controls, shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],
        unchanged_pending_records=276, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    startup = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                           {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})
    startup(previous, candidate, arm)
    return stored, draft, {stage.ARM: batch.digest(arm), stage.COMMON: batch.digest(common)}


template = precedent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 945 and len(manifest["checks"]) == 280':
        'len(manifest["batches"]) == 947 and len(manifest["checks"]) == 282',
    "stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review,":
        "stage.PROOF, STARTUP, QA, game.NATIVE, game.GETTER, game.PROOF, args.visual_review,",
    "release_stack_before_damaged_save_digits.json": "release_stack_before_tavern_round_digits.json",
    "release_stack_with_damaged_save_digits.json": "release_stack_with_tavern_round_digits.json",
    "verified_market_bargaining_predecessor=predecessor, damaged_save_digits_release=str(REVIEW)":
        "verified_hamburg_ceramics_predecessor=predecessor, tavern_round_digits_release=str(REVIEW)",
    "registered_damaged_save_digits_and_complete_parent_inverse": "registered_tavern_round_digits_and_complete_parent_inverse",
    'manifest["damaged_save_digits_pipeline"]': 'manifest["tavern_round_digits_pipeline"]',
    '''    ids = manifest["changed_records"][stage.ARM]
    new_ids = [row['id'] for row in draft['records'] if row['decision'] == 'revision']
    assert all(key not in ids for key in new_ids)
    ids.extend(new_ids)''': '''    for row in draft["records"]:
        key, file = row["id"], row["file_path"]
        if file == stage.COMMON:
            assert (file, key) in credited
        ids = manifest["changed_records"][file]
        if row["decision"] == "revision" and key not in ids:
            ids.append(key)''',
    'owned_number_call=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM]':
        'owned_number_call=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM], owned_common_slots=stored["COMMON_allocations"]',
    "changed_components=1, target_ARM9_sha256=archives[stage.ARM]":
        "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]",
    'MESFILE_sha256=previous["target_COMMON_sha256"]': 'MESFILE_sha256=archives[stage.COMMON]',
    "previously_localized_records=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1":
        "previously_localized_records=11, new_contextual_records=0, prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7",
    "Continue_checksum_warning_scripted_inputs=True, copied_save_checksum_fixture=True,\n                                       ordinary_live_menu_transitions=True, retail_hardware_tested=False":
        "ordinary_Amsterdam_Tavern_round=True, declined_and_accepted_branches=True,\n                                       six_alternate_price_lines_offline=True",
    'ledger["damaged_save_digits_20261120"]': 'ledger["tavern_round_digits_20261120"]',
    "prior_records_reviewed=1, actual_paired_states=2, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1, text_display_revisions=1":
        "prior_records_reviewed=11, actual_paired_states=6, new_contextual_credit=0,\n        prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7, text_display_revisions=1",
    "    checkpoint = CHECKPOINT": '''    ledger["amsterdam_tavern_round_20261120"].update(
        separate_pending_price_glyph=False, registered_correction=str(REVIEW))
    checkpoint = CHECKPOINT''',
    "Preserve the Continue checksum-warning ROM or reconstruction": "Preserve the Tavern round candidate or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tavern round testing candidate

The [testing ROM](../../{ROM.as_posix()}) shows the Treat Everyone price in the regular English font and improves four alternate confirmation lines. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Tavern round price and patron exchange

**Treat Everyone** now shows the price in regular-width digits. Four confirmation lines keep the amount and “gold” together and let each question read as a complete thought. Seven other lines retain their established English, including the four observed follow-up lines. The original price calculation divides the town’s growth by 25, discards the remainder and adds 100 gold. [Exact source references and decisions](../{REVIEW.as_posix()})

Paired ordinary Amsterdam runs verified the complete 268-gold confirmation, cancellation at 34,980 gold, and acceptance at 34,712 gold. The round announcement, the patron’s thanks and the tip about Clifford’s fleet heading to Bristol matched in both runs. Offline checks covered the original voice selector, 256 number-buffer cases and 56 complete rendered panels. [Emulator comparison](../{(VERIFY / game.SHEET.name).as_posix()})

Six startup frames, 24 protected getters and 30 focused tests passed. Two optional historical tests skipped. The clean-input patch rebuilds the cumulative ROM byte for byte. Other voice variants received offline coverage, and hardware was outside this pass. The ledger retains 27,700 credited records and 276 stored shared keys open for display-owner review. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = precedent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
