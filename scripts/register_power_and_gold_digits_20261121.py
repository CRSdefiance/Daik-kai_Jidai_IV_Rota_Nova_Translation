"""Register regular digits for all established Power and Search gold call sites."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_search_gold_digits_20261121 as display
from scripts import register_victory_reward_wrap_20261121 as parent
from scripts import stage_power_and_gold_digits_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
shared = stage.rewards.shared
PROFILE = "all-routes-power-and-gold-digits-v1-20261121"
ROOT = Path("out/power_and_gold_digits_registered_20261121")
ROM = ROOT / "Translation_DS_Power_And_Gold_Digits_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_power_and_gold_digits_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_power_and_gold_digits_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "Power and shore Search gold now use regular digits at all established callers. The original Search replay awards 370 gold on both builds."


def verify(registry, previous, viewed):
    source = checked_text(getsource(parent.verify), {
        'assert draft["exact_parent_inverse"] and draft["runtime"]["scoped_message_IDs"] == [301, 305]':
            'assert draft["exact_parent_inverse"] and len(draft["original_call_bindings"]) == 4',
        'assert len(draft["native_display_cases"]) == 44 and len(draft["unchanged_native_controls"]) == 7':
            'assert len(draft["native_display_cases"]) == 16 and len(draft["native_number_checks"]) == 1792',
        'assert actual["original_victory_amounts"] == [109, 103, 6055] and not actual["hardware_verified"]':
            'assert actual["amount"] == 370 and not actual["hardware_verified"]',
        'assert actual["supplies_screen_unchanged"] and len(actual["held_notices"]) == 2':
            'assert actual["original_outcome_selection"] and len(actual["corrected_holds"]) == 2',
        'assert len(actual["exact_unchanged_framebuffers"]) == 20':
            'assert 5350 in actual["unchanged_frames"] and actual["power_alternates_offline_only"]',
        'stage.shared': 'shared',
        'arm, binding = stage.selector.transform(before[stage.shared.ARM], previous["target_ARM9_sha256"])':
            'arm, binding = stage.patch(before[shared.ARM], original[shared.ARM])',
        'binding == draft["runtime"]': 'binding == draft["original_call_bindings"]',
    })
    env = vars(parent) | globals()
    exec(compile(source, __file__ + "::register-checks", "exec"), env)
    return env["verify"](registry, previous, viewed)


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 975 and len(manifest["checks"]) == 310':
        'len(manifest["batches"]) == 976 and len(manifest["checks"]) == 311',
    'release_stack_before_victory_reward_wrap.json': 'release_stack_before_power_and_gold_digits.json',
    'release_stack_with_victory_reward_wrap.json': 'release_stack_with_power_and_gold_digits.json',
    'verified_victory_reward_digits_predecessor=predecessor, victory_reward_wrap_release=str(REVIEW)':
        'verified_victory_reward_wrap_predecessor=predecessor, power_and_gold_digits_release=str(REVIEW)',
    'registered_victory_reward_wrap_and_complete_parent_inverse':
        'registered_power_and_gold_digits_and_complete_parent_inverse',
    'manifest["victory_reward_wrap_pipeline"]': 'manifest["power_and_gold_digits_pipeline"]',
    'original_victory_reward_arithmetic_and_modal_calls=True': 'original_Power_and_Search_reward_amounts=True',
    'wrap_only_revisions=2, justified_retentions=0': 'wrap_only_revisions=0, justified_retentions=2',
    'text_display_revisions=0': 'text_display_revisions=2',
    'original_fleet_victory=True, observed_captured_gold=True, national_reward_offline=True, native_pages=44, position_fixture_bytes=40':
        'original_Search_outcome=True, observed_received_gold=True, alternate_Power_calls_offline=True, native_pages=16, position_fixture_bytes=48',
    'ledger["victory_reward_wrap_20261121"]': 'ledger["power_and_gold_digits_20261121"]',
    'prior_records_reviewed=2, actual_reward_notices=1, native_pages=44':
        'prior_records_reviewed=2, actual_reward_notices=1, native_pages=16',
    'Preserve the victory wrap candidate and source ROMs': 'Preserve the Power and gold candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Power and Search gold testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses the regular English digits in all established Power and Search gold notices. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Power and shore Search gold

Normalized the digits at the three remaining Power call sites and the shore Search gold call. The existing ruins Power correction carries forward. Both notices preserve their English wording, one original substitution, and the original calculation. Native checks cover 1,792 ring-slot cases and 16 complete displays. [Exact source and release decisions](../{REVIEW.as_posix()})

In the paired emulator runs, Gerhard reports that the expedition seems to have found something, then the original Search awards 370 gold. The gold total and final wallet agree across both runs. The revised notice matches the complete English glyph mask. The copied save used a 48-byte adjustment to the fleet’s position. The result was held on screen for verification. The alternate Power paths were checked offline. [Gameplay comparison](../{(VERIFY / display.SHEET.name).as_posix()})

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
