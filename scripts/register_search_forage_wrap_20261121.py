"""Register the complete foraging phrase wraps and cumulative patch."""

from inspect import getsource
from json import dumps, loads
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import check_search_forage_wrap_20261121 as display
from scripts import register_search_supply_and_fatigue_digits_20261121 as parent
from scripts import register_victory_reward_wrap_20261121 as registration
from scripts import stage_search_forage_wrap_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow, shared = parent.base, parent.native, parent.workflow, stage.shared
PROFILE = "all-routes-search-forage-wrap-v1-20261121"
ROOT = Path("out/search_forage_wrap_registered_20261121")
ROM = ROOT / "Translation_DS_Search_Forage_Wrap_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_search_forage_wrap_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_search_forage_wrap_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP = EVIDENCE / "own_startup_verification.json"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
QA = EVIDENCE / "qa_passed.xml"
live = SimpleNamespace(PROOF=display.PROOF)
CHECKPOINT = "All five foraging voices keep each barrel count with its resource. Charles’s original gameplay report and sailing return verify the wrap."


def replay_install(draft, before, after):
    arm = before[shared.ARM]
    directory = native.digest(arm[shared.workflow.DIRECTORY_OFFSET:shared.workflow.TABLE_OFFSET])
    records = {r["message_ID"]: r for r in draft["records"]}
    pack = FunctionType(stage.relocate.__code__, stage.relocate.__globals__ | {"DIRECTORY": directory})
    common, metadata, packed, allocation = pack(before[shared.COMMON], arm, records, stage.guarded_storage(records))
    assert loads(dumps(allocation)) == draft["allocation"]
    revised, binding = stage.selector.transform(metadata, native.digest(metadata))
    assert revised == after[shared.ARM] and common == after[shared.COMMON] and binding == draft["runtime"]
    for n, row in records.items():
        assert shared.workflow.reference(packed[n]) == row["staged_reference"] and packed[n].text.hex() == row["staged_hex"]
        row["registered_reference"] = row["staged_reference"] | {"candidate_sha256": draft["candidate_sha256"]}
    return revised


def verify(registry, previous, viewed):
    source = checked_text(getsource(registration.verify), {
        'draft["runtime"]["scoped_message_IDs"] == [301, 305]':
            'draft["allocation"]["changed_visible_templates"] == list(stage.previous.FORAGE_IDS)',
        'assert len(draft["native_display_cases"]) == 44 and len(draft["unchanged_native_controls"]) == 7':
            'assert len(draft["native_display_cases"]) == 35 and draft["source_water_before_food"]',
        'assert actual["original_victory_amounts"] == [109, 103, 6055] and not actual["hardware_verified"]':
            'assert actual["water_and_food"] == [175, 140] and not actual["hardware_verified"]',
        'assert actual["supplies_screen_unchanged"] and len(actual["held_notices"]) == 2':
            'assert actual["exact_live_glyphs"] and actual["changed_dialogue_frames"] == [11173, display.HOLD]',
        'assert len(actual["exact_unchanged_framebuffers"]) == 20':
            'assert actual["actual_return_frame"] in actual["unchanged_frames"]',
        'actual["source_evidence"]': 'actual["evidence"]',
        '{stage.shared.ARM}\n    arm, binding = stage.selector.transform(before[stage.shared.ARM], previous["target_ARM9_sha256"])\n'
        '    assert arm == after[stage.shared.ARM] and binding == draft["runtime"]':
            '{stage.shared.ARM, stage.shared.COMMON}\n    arm = replay_install(draft, before, after)',
        'previous["target_COMMON_sha256"] == draft["target_COMMON_sha256"]':
            'draft["target_COMMON_sha256"]',
        'target.replace_file(stage.shared.ARM, before[stage.shared.ARM])':
            'target.replace_file(stage.shared.ARM, before[stage.shared.ARM])\n'
            '    target.replace_file(stage.shared.COMMON, before[stage.shared.COMMON])',
        '    for row in draft["records"]:\n        row["registered_reference"] = row["current_reference"] | {"candidate_sha256": candidate}\n': '',
        'return draft, draft, {stage.shared.ARM: native.digest(arm)}':
            'return draft, draft, {path: native.digest(after[path]) for path in (stage.shared.ARM, stage.shared.COMMON)}',
    })
    env = vars(registration) | globals()
    exec(compile(source, __file__ + "::register-checks", "exec"), env)
    return env["verify"](registry, previous, viewed)


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 977 and len(manifest["checks"]) == 312':
        'len(manifest["batches"]) == 978 and len(manifest["checks"]) == 313',
    'release_stack_before_search_supply_and_fatigue_digits.json': 'release_stack_before_search_forage_wrap.json',
    'release_stack_with_search_supply_and_fatigue_digits.json': 'release_stack_with_search_forage_wrap.json',
    'live.PROOF, forage_check.PROOF, args.visual_review,': 'live.PROOF, args.visual_review,',
    'verified_power_and_gold_digits_predecessor=predecessor, search_supply_and_fatigue_digits_release=str(REVIEW)':
        'verified_search_supply_and_fatigue_digits_predecessor=predecessor, search_forage_wrap_release=str(REVIEW)',
    'registered_search_supply_and_fatigue_digits_and_complete_parent_inverse':
        'registered_search_forage_wrap_and_complete_parent_inverse',
    'manifest["search_supply_and_fatigue_digits_pipeline"]': 'manifest["search_forage_wrap_pipeline"]',
    'changed_components=1, target_ARM9_sha256=archives[native.ARM],':
        'changed_components=2, target_ARM9_sha256=archives[native.ARM], target_COMMON_sha256=archives[shared.COMMON],',
    'previously_localized_records=7': 'previously_localized_records=5',
    'wrap_only_revisions=0, justified_retentions=7': 'wrap_only_revisions=5, justified_retentions=0',
    'text_display_revisions=7': 'text_display_revisions=0',
    'observed_fatigue_and_foraging=True, alternative_voices_offline=True, native_pages=40':
        'observed_foraging=True, alternative_voices_offline=True, native_pages=35',
    'ledger["search_supply_and_fatigue_digits_20261121"]': 'ledger["search_forage_wrap_20261121"]',
    'prior_records_reviewed=7, actual_Search_notices=3, native_pages=40':
        'prior_records_reviewed=5, actual_Search_notices=1, native_pages=35',
    'Preserve the Search digits candidate and source ROMs': 'Preserve the Search forage-wrap candidate and source ROMs',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Foraging phrase-wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) keeps both foraging amounts with their resources. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Search foraging reports

All five voices now keep the water amount and unit on one row and the food amount and unit on the next. The existing wording, voice choices, and water-before-food substitutions carry forward. The thirty-five native pages cover zero, short, unequal, and maximum source-bound amounts. [Exact source and registered decisions](../{REVIEW.as_posix()})

The paired emulator replay held Charles Rochefort’s report of 175 barrels of water and 140 barrels of food. The full glyph mask, other views, fleet state, and return to sailing passed. The four other voices were checked offline. [Gameplay comparison](../{(VERIFY / display.SHEET.name).as_posix()})

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
environment = parent.environment | globals()
exec(compile(program, __file__ + "::register", "exec"), environment)


if __name__ == "__main__":
    environment["main"]()
