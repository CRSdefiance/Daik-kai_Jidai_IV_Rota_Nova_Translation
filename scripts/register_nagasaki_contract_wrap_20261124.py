"""Register the source-reviewed Nagasaki contract wrap after the matching replay."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import reconcile_archived_message_arguments_20261124 as archived
from scripts import register_cartridge_title_20261123 as template
from scripts import register_tavern_buy_a_round_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_nagasaki_contract_wrap_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


PROFILE = "all-routes-nagasaki-contract-wrap-v1-20261124"
CHECK = "registered_nagasaki_contract_wrap_and_complete_parent_inverse"
ARM, COMMON, KEY = build.ARM, build.COMMON, build.KEY
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_nagasaki_contract_wrap_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_nagasaki_contract_wrap.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_nagasaki_contract_wrap_registered_20261124.md")
CHECKPOINT = "Registered the Daimyo's two-line contract offer after ordinary Nagasaki gameplay."
SHEET, PREVIEW = build.SHEET, build.preflight.ROOT / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, patch, packet, native = map(files.read, (build.STORED, build.PAIRED, PATCH_PROOF,
        build.market.OUT, build.preflight.OUT))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == files.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and files.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"] == packet["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["changed_message"] == KEY and stored["allocation"]["new_null_fields"] == 0
    assert files.reference(build.preflight.OUT) == stored["preflight"] and files.reference(build.STORED) == live["stored"]
    assert live["ordinary_saved_game"] and live["revised"]["frame"] == build.HOLD and len(live["unchanged_frames"]) == 23
    assert files.reference(build.BEFORE) == live["before"] and files.reference(build.REPLAY) == live["after"]
    visuals = [files.reference(SHEET), files.reference(PREVIEW)]
    assert live["sheet"] == visuals[0] and native["sheets"][0]["sha256"] == visuals[1]["sha256"]
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    assert stored["candidate_layout"] == native["native_cases"][1]["layout"]

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    arm, old_common, common = new.read_file(ARM), old.read_file(COMMON), new.read_file(COMMON)
    assert arm == old.read_file(ARM) and files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    before, after = (build.market.common_rows(data, arm) for data in (old_common, common))
    assert [a.message_id for a, b in zip(before, after, strict=True) if a != b] == [KEY]
    new.replace_file(COMMON, old_common)
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_COMMON_contract_question_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    jp = build.market.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    ref = build.panels.text_reference
    assert [stored[f"exact_{kind}"] for kind in ("clean_source", "predecessor", "installed")] == [ref(row[KEY]) for row in (jp, before, after)]
    proposal, = native["manuscript"]["records"]
    records = []
    seen = set()
    for row in packet["observed_dialogue"]:
        key = row["message_ID"]
        if key in seen:
            continue
        seen.add(key)
        original, prior, installed = jp[key], before[key], after[key]
        assert ref(original) == row["clean_reference"] and ref(prior) == row["installed_reference"]
        assert original.text.count(b"%s") == prior.text.count(b"%s") == installed.text.count(b"%s")
        note = proposal["localization_note"] if key == KEY else row["localization_note"]
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_id=key,
            context="The Nagasaki trader refuses trade until Maria signs a contract. The Daimyo quotes the fee, asks for an offer and grants trade on payment.",
            speaker=row["speaker"], source_meaning=proposal["source_meaning"] if key == KEY else note, localization_note=note,
            clean_Japanese=row["clean_Japanese"], previous_English=row["current_English"], english=installed.text.decode("ascii").strip(),
            source_reference=ref(original), current_reference=ref(prior), registered_reference=ref(installed), installed_hex=installed.text.hex(),
            decision="revision" if key == KEY else "retention", review=dict.fromkeys(files.GATES, True)))
    assert len(records) == 5
    previous_review = files.read(parent.REVIEW)
    shared = previous_review["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(before[r["message_ID"]] == after[r["message_ID"]] and ref(after[r["message_ID"]]) == r["installed"]
               for r in shared["records"])
    bounded = files.read(archived.OUT)
    assert bounded["candidate_sha256"] == previous["candidate_sha256"] and bounded["fully_bounded_census_sites"] == 827
    assert all(before[key] == after[key] for key in bounded["archived_ids"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_COMMON_sha256=stored["target_COMMON_sha256"], visual_review=visuals, stored_proof=files.reference(build.STORED),
        gameplay=files.reference(build.PAIRED), source_review=files.reference(build.market.OUT),
        unchanged_archived_message_argument_evidence=files.reference(archived.OUT),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=previous_review["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=previous_review["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
record_update = parent.prepare[parent.prepare.index("        for row in outcome[\"records\"]:"):parent.prepare.index("        update = dict(profile=")]
prepare = checked_text(parent.prepare, {
    "verified_stockholm_recruiting_predecessor=predecessor, tavern_buy_a_round_release=str(REVIEW)":
        "verified_tavern_buy_a_round_predecessor=predecessor, nagasaki_contract_wrap_release=str(REVIEW)",
    "len(batches) == 1120 and len(checks) == 455": "len(batches) == 1121 and len(checks) == 456",
    "set((ARM, HELP)) <= set(paths) and set((ARM, HELP)) <= set(records)": "COMMON in paths and COMMON in records",
    'assert revised == ["TAVERN_MENU_BUY_A_ROUND", "HELP_TOPIC_12", "HELP_TOPIC_14", "HELP_TOPIC_15"]':
        'assert revised == [f"COMMON_MESSAGE_{KEY}"]',
    record_update: '        records[COMMON].extend(ident for ident in revised if ident not in records[COMMON])\n',
    "snapshot_scope=[ARM, HELP]": "snapshot_scope=COMMON",
    "tavern_buy_a_round_release_proof": "nagasaki_contract_wrap_release_proof",
    '"tavern_buy_a_round_pipeline"': '"nagasaki_contract_wrap_pipeline"',
    "played.TAVERN_PROOF, played.HELP_PROOF, PREVIEW, HELP_SHEET":
        "build.PAIRED, PREVIEW, build.market.OUT, build.market.SHEET, build.preflight.OUT",
    "registered_manifest_entries=1121, passing_release_checks=456, changed_components=2, changed_internal_files=[ARM, HELP]":
        "registered_manifest_entries=1122, passing_release_checks=457, changed_components=1, changed_internal_files=[COMMON]",
    'target_ARM9_sha256=outcome["target_ARM9_sha256"], target_HELP_sha256=outcome["target_HELP_sha256"]':
        'target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "reviewed_UI_labels=4, contextual_records_revisited=10, contextual_decisions_reused=6, previously_localized_records=10":
        "reviewed_UI_labels=0, contextual_records_revisited=5, contextual_decisions_reused=4, previously_localized_records=5",
    "prose_revisions=3, justified_retentions=6, text_display_revisions=4, wrap_only_revisions=1":
        "prose_revisions=1, justified_retentions=4, text_display_revisions=1, wrap_only_revisions=0",
    "ordinary_Copenhagen_Tavern=True, revised_gameplay_holds=4, native_help_pages=3, ordinary_help_history_returns=3":
        "ordinary_Nagasaki_Palace_and_Trade=True, revised_gameplay_holds=1, native_pages=1, goods_info_selections=3",
    "prose_revisions=3, wrap_only_revisions=1, texts_retained=6": "prose_revisions=1, wrap_only_revisions=0, texts_retained=4",
    '"tavern_buy_a_round_20261124"': '"nagasaki_contract_wrap_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Nagasaki contract wrap candidate

The Daimyo's payment question stays on one line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Tavern Buy a Round candidate": "Preserve the registered Nagasaki contract wrap candidate",
    "1,121 entries and 456 passing checks": "1,122 entries and 457 passing checks",
    doc: '''    DOC.write_text(f"""# Nagasaki contract and Trade

The Daimyo now says, “Your fee sets your market share. How much will you offer?” The first sentence follows the 1,125-gold quote, and the complete payment question fits on its own line. Four distinct surrounding lines retain their wording. The declined contract outcome remains unvisited here. [Source, exact stored text and five review gates](../{REVIEW.as_posix()})

Ordinary play verified the Trader's refusal, Palace payment, 1% market share, the second Market visit and the return to town. The replay after the edit matched 23 comparison frames pixel for pixel, including the purchase and complete Goods Info masks for Silver, Cotton Cloth and Tortoiseshell. [Ordinary Trade and the contract](../{VERIFY.as_posix()}/{build.market.SHEET.name}) · [Revised question in gameplay](../{VERIFY.as_posix()}/{SHEET.name})

The cumulative candidate passed startup, 457 release checks and 17 focused repository tests. The clean-input patch reconstructs the candidate byte for byte. The five archived shared-message owners, remaining Fleet Info inputs and further practical town or random-scene coverage remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::nagasaki-contract-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
