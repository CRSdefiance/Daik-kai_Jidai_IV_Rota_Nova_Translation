"""Register the verified Search fatigue and supply digit correction."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_search_forage_digits_20261121 as forage_check
from scripts import register_power_and_gold_digits_20261121 as parent
from scripts import replay_search_supply_and_fatigue_digits_20261121 as display
from scripts import stage_search_supply_and_fatigue_digits_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow, shared = parent.base, parent.native, parent.workflow, stage.shared
PROFILE = "all-routes-search-supply-and-fatigue-digits-v1-20261121"
ROOT = Path("out/search_supply_and_fatigue_digits_registered_20261121")
ROM = ROOT / "Translation_DS_Search_Supply_And_Fatigue_Digits_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_search_supply_and_fatigue_digits_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_search_supply_and_fatigue_digits_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "Shore Search uses regular digits for fatigue and foraging. Gameplay verified both fatigue notices and the water-before-food portrait."


def verify(registry, previous, viewed):
    source = checked_text(getsource(parent.parent.verify), {
        'assert draft["exact_parent_inverse"] and draft["runtime"]["scoped_message_IDs"] == [301, 305]':
            'assert draft["exact_parent_inverse"] and len(draft["original_call_bindings"]) == 5',
        'assert len(draft["native_display_cases"]) == 44 and len(draft["unchanged_native_controls"]) == 7':
            'assert len(draft["native_display_cases"]) == 40 and len(draft["native_number_checks"]) == 1920',
        'assert actual["original_victory_amounts"] == [109, 103, 6055] and not actual["hardware_verified"]':
            'assert actual["original_search_outcomes"] and not actual["hardware_verified"]',
        'assert actual["supplies_screen_unchanged"] and len(actual["held_notices"]) == 2':
            'assert [r["message_ID"] for r in actual["held_results"]] == [309, 308]',
        'assert len(actual["exact_unchanged_framebuffers"]) == 20':
            'assert actual["exact_same_return_frame"] and draft["water_then_food"]',
        'assert viewed == {r["path"]: r["sha256"] for r in (*draft["sheets"], actual["sheet"])}':
            'forage = base.load(forage_check.PROOF)\n'
            '    assert forage["candidate_sha256"] == candidate and forage["parent_sha256"] == previous["candidate_sha256"]\n'
            '    assert forage["source_water_and_food"] == [175, 140] and forage["full_foreground_glyph_masks"]\n'
            '    assert viewed == {r["path"]: r["sha256"] for r in (*draft["sheets"], actual["sheet"], forage["sheet"])}',
        'actual["source_evidence"]': 'actual["evidence"] | forage["evidence"]',
        'native_and_replay_evidence=str(display.PROOF), checked_story_format_guard=controls,':
            'native_and_replay_evidence=str(display.PROOF), foraging_gameplay_evidence=str(forage_check.PROOF), checked_story_format_guard=controls,',
        'arm, binding = stage.selector.transform(before[stage.shared.ARM], previous["target_ARM9_sha256"])':
            'arm, binding = stage.patch(before[stage.shared.ARM], original[stage.shared.ARM])',
        'binding == draft["runtime"]': 'binding == draft["original_call_bindings"]',
    })
    env = vars(parent.parent) | globals()
    exec(compile(source, __file__ + "::register-checks", "exec"), env)
    return env["verify"](registry, previous, viewed)


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 976 and len(manifest["checks"]) == 311':
        'len(manifest["batches"]) == 977 and len(manifest["checks"]) == 312',
    'release_stack_before_power_and_gold_digits.json': 'release_stack_before_search_supply_and_fatigue_digits.json',
    'release_stack_with_power_and_gold_digits.json': 'release_stack_with_search_supply_and_fatigue_digits.json',
    'live.PROOF, args.visual_review,': 'live.PROOF, forage_check.PROOF, args.visual_review,',
    'verified_victory_reward_wrap_predecessor=predecessor, power_and_gold_digits_release=str(REVIEW)':
        'verified_power_and_gold_digits_predecessor=predecessor, search_supply_and_fatigue_digits_release=str(REVIEW)',
    'registered_power_and_gold_digits_and_complete_parent_inverse':
        'registered_search_supply_and_fatigue_digits_and_complete_parent_inverse',
    'manifest["power_and_gold_digits_pipeline"]': 'manifest["search_supply_and_fatigue_digits_pipeline"]',
    'original_Power_and_Search_reward_amounts=True': 'original_Search_supplies_and_fatigue_changes=True',
    'previously_localized_records=2': 'previously_localized_records=7',
    'justified_retentions=2': 'justified_retentions=7',
    'text_display_revisions=2': 'text_display_revisions=7',
    'observed_received_gold=True, alternate_Power_calls_offline=True, native_pages=16, position_fixture_bytes=48':
        'observed_fatigue_and_foraging=True, alternative_voices_offline=True, native_pages=40, position_fixture_bytes=48',
    'ledger["power_and_gold_digits_20261121"]': 'ledger["search_supply_and_fatigue_digits_20261121"]',
    'prior_records_reviewed=2, actual_reward_notices=1, native_pages=16':
        'prior_records_reviewed=7, actual_Search_notices=3, native_pages=40',
    'Preserve the Power and gold candidate and source ROMs': 'Preserve the Search digits candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Search supply and fatigue font testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses regular English digits for shore Search supply and fatigue notices. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Shore Search counts and fatigue

Regular-width digits now appear in both fatigue notices and all five foraging voices. The original signed fatigue logic, capped stored fatigue, and reported adjustment carry forward. The foraging report and supply update both receive water first and food second. The original unit is barrels for both. The battle capture notice uses the reverse order. [Exact source and release decisions](../{REVIEW.as_posix()})

The same copied save and original Search inputs showed a requested fatigue reduction of 15 at a hot spring and an increase of 3 after a failed search. Continued Search produced Charles Rochefort’s report of 175 barrels of water and 140 of food. The paired runs matched the relevant fleet state and return to sailing. The replay used fleet-position setups at the original shoreline. Forty native pages and 1,920 formatter checks passed. [Fatigue comparison](../{(VERIFY / display.SHEET.name).as_posix()}) · [Foraging comparison](../{(VERIFY / forage_check.SHEET.name).as_posix()})

The foraging paragraph still splits the water quantity from “of water” on some lines. Follow up with whole resource phrases, retaining both substituted amounts. [Native previews](../{(VERIFY / 'portrait_sheet_01.png').as_posix()})

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
