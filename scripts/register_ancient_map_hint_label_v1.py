"""Register the verified Ancient Map Hint label over the Sound Setup candidate."""

import argparse
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from scripts import register_arrival_month_labels_v1 as prior
from scripts import run_ancient_map_hint_label_startup_v1 as startup
from scripts import stage_ancient_map_hint_label_v1 as stage
from scripts import verify_ancient_map_hint_label_v2 as live
from scripts.source_locked_derivation_v5118 import checked_text


parent, base = stage.parent, stage.base
ARM, COMMON, CLEAN = stage.ARM, stage.COMMON, stage.CLEAN
PROFILE = 'all-routes-ancient-map-hint-label-v1-20261111'
CHECK = 'registered_ancient_map_hint_label_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_ancient_map_hint_label_candidate')
VERIFICATION = PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_label_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/ancient_map_hint_label_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Ancient_Map_Hint_20261111_candidate.nds'
MANIFEST, PATCH = ROM.with_suffix('.manifest.json'), PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_ancient_map_hint_label_registered_20261111.md')
REGISTRY_PENDING = base.REGISTRY.with_name('release_stack.ancient_map_hint_label.pending.json')
LEDGER_PENDING = base.LEDGER.with_name('editorial_review_current.ancient_map_hint_label.pending.json')
verification = SimpleNamespace(BOOT=startup.BOOT, LIVE=live.OUTPUT,
                               QA=Path('work/ancient_map_hint_label_repo_qa_20261111.xml'))


def register():
    changes = {
        "proof['research_ROM_sha256']": "proof['candidate_sha256']",
        "proof['parent_inverse_exact']": "proof['whole_parent_inverse_exact']",
        "    assert len(live['observed_changes']) == 12 and len(live['whole_frame_equal']) == 28\n"
        "    assert live['calendars_and_other_pixels_unchanged'] and live['repository_tests'] == 34":
            "    assert len(live['observed_hint_frames']) == len(live['return_frames']) == 3\n"
            "    assert live['whole_frame_matches'] == [9900, 11100]\n"
            "    assert live['original_Back_and_Select_masks_exact'] and live['Hint_box_only']\n"
            "    suites = list(ElementTree.parse(verification.QA).iter('testsuite'))\n"
            "    assert sum(int(row.get('tests', 0)) for row in suites) == 34\n"
            "    assert not any(int(row.get(k, 0)) for row in suites for k in ('errors', 'failures', 'skipped'))",
        "== 27597": "== 27696",
        "== 774 and len(manifest['checks']) == 109": "== 777 and len(manifest['checks']) == 112",
        "== 775 and len(manifest['checks']) == 110": "== 778 and len(manifest['checks']) == 113",
        "    arm, records = stage.transform(original, base.NdsImage.open(CLEAN).read_file(ARM))\n"
        "    assert records == proof['records'] and digest(arm) == proof['research_ARM9_sha256']":
            "    arm = stage.transform(original, base.NdsImage.open(CLEAN).read_file(ARM))\n"
            "    records = [proof['record']]\n"
            "    assert digest(original) == proof['parent_ARM9_sha256'] and digest(arm) == proof['target_ARM9_sha256']",
        "proof['research_COMMON_sha256']": "proof['original_COMMON_sha256']",
        "    scope = dict(actual_emulator=True, hardware=False, Trade_holds=11, Golden_Route_Found_holds=1,\n"
        "        other_whole_frames_exact=28, original_calendar_and_Guild_return_exact=True,\n"
        "        fixture_scope='One temporary purchase-cost word to reach the original Golden Route screen.')":
            "    scope = dict(actual_emulator=True, hardware=False, Hint_holds=3, complete_return_label_holds=3,\n"
            "        other_whole_frames_exact=2, stray_footer_pixels_cleared_per_return=2,\n"
            "        fixture_scope='Four temporary clue bits in a copied Syracuse save.')",
        'release_stack_before_arrival_month_labels.json': 'release_stack_before_ancient_map_hint_label.json',
        'verified_golden_route_exchanges_predecessor': 'verified_sound_bgm_titles_predecessor',
        'arrival_month_labels_release': 'ancient_map_hint_label_release',
        'Terminated the original Trade and Golden Route arrival-month labels in their owned slots.':
            'Translated the original Ancient Map Hint button in its exclusive slot.',
        "['arrival_month_labels']": "['ancient_map_hint_label']",
        'arrival_month_labels_registered_successor_pipeline': 'ancient_map_hint_label_registered_successor_pipeline',
        'registered_manifest_entries=775, passing_release_checks=110':
            'registered_manifest_entries=778, passing_release_checks=113',
        'reviewed_UI_labels=2': 'reviewed_UI_labels=1',
        'The two arrival-month label corrections are registered.': 'The Ancient Map Hint label is registered.',
        'arrival_month_labels_20261111': 'ancient_map_hint_label_20261111',
        'Staged the exact cumulative arrival-month release for publication.':
            'Staged the exact cumulative Ancient Map Hint release for publication.',
    }
    source = checked_text(getsource(prior.register), changes)
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::verified-hint-registration', 'exec'), environment)
    environment['register']()


def publish_prepared():
    changes = {
        'Preserve the arrival-month build.': 'Preserve the Ancient Map Hint build.',
        '# Arrival-month labels candidate': '# All Routes Ancient Map Hint candidate',
        'Trade shows “Arr.” and Golden Route Found shows “Arrival.” Both labels terminate before the following string in ARM9. '
        'The 40-frame Lisbon comparison found 12 label-only differences and 28 exact frames. Both complete glyph masks, the month grids, '
        'the Guild return, cold boot, 24 protected getters, 34 targeted tests and 110 release checks passed.':
            'The original Y button shows “Hint.” Three complete Hint masks and six return-label masks passed. '
            'The original clue screen matches the exact parent. Cold boot, 24 protected getters, '
            '34 targeted tests and 113 release checks passed.',
        '''    document = """# Arrival-month labels registered''': '''    document = """# Ancient Map Hint label registered''',
        'The Trade and Golden Route Found calendars now display complete terminated labels. The eight-byte fields at '
        '\x600215A000\x60 and \x600216AFB0\x60 hold “Arr.” and “Arrival.” The original callers and the strings that follow both slots are byte-exact. '
        'The replay verified the new labels and preserved all other screen pixels in the 40 sampled frames.':
            'The original Ancient Map Y button now displays Hint. Three complete native masks match the focused emulator replay. '
            'The original Back and Select glyphs are intact on both returns. Two stray white pixels above those glyphs now match the footer backing.',
        'releases/all_routes_editorial_20261111_arrival_month_labels_candidate/README.md':
            'releases/all_routes_editorial_20261111_ancient_map_hint_label_candidate/README.md',
        'The dialogue ledger remains at 27,597 reviews, with 379 native shared keys to review or classify. '
        'Continue with the [Ancient Map manuscript](../translations/editorial_checkpoints/SharedText_20261110_v1/treasure_map_documents_context_v1.json). '
        'It records 51 contextual decisions and the 20 original region and direction pairs. '
        'The native document layout and representative replay are pending.':
            'The dialogue ledger remains at 27,696 reviews, with 280 native shared keys to review or classify. '
            'Continue from the [exact Online and scene source comparison](../translations/editorial_checkpoints/SharedText_20261110_v1/online_and_scene_consumer_comparison_v1.json).',
        'The two arrival-month labels are registered.': 'The Ancient Map Hint label is registered.',
        'Registered 775 entries, 114 accepted layers and 110 checks. Dialogue credit remains 27,597.':
            'Registered 778 entries, 114 accepted layers and 113 checks. Dialogue credit remains 27,696.',
    }
    source = checked_text(getsource(prior.publish_prepared), changes)
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::publish-hint-label', 'exec'), environment)
    environment['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--register', action='store_true')
    group.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
