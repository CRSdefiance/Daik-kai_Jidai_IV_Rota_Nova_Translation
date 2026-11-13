"""Reconstruct the cumulative all-routes candidate through Arrival Month Labels."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import prepare_all_routes_promotion_20261111 as prior
from scripts import prepare_all_routes_voyage_promotion_20261111 as voyage
from scripts import register_arrival_month_labels_v1 as current
from scripts.source_locked_derivation_v5118 import checked_text


NAMES = voyage.NAMES + (
    'sailing_hazards_and_dolphins', 'golden_route_exchanges', 'arrival_month_labels',
)
PROMOTION = Path('out/promotion_ready_20261111_arrival_month_labels')
ROM = PROMOTION / 'Translation_DS_All_Routes_20261111_candidate.nds'
ADJACENT = ROM.with_suffix('.manifest.json')
VERIFICATION = current.VERIFICATION


def add_remaining_groups(scope):
    shared = scope['shared_native_COMMON']
    pending = set(shared['pending_ids'])
    ranges = {
        'music_titles': range(3251, 3289),
        'online_tie_in': range(3289, 3320),
        'scene_and_asset_labels': range(3393, 3607),
        'ancient_map_fields_and_rumors': range(3607, 3668),
    }
    mapped = set().union(*ranges.values())
    other = pending - mapped
    assert mapped <= pending and len(other) == 35
    shared['pending_scope_groups'] = {name: len(ids) for name, ids in ranges.items()} | {
        'other_legacy_menu_and_shared_keys': len(other),
        'other_pending_ids': sorted(other),
    }
    shared['ancient_map_batch_status'] = (
        'All 61 contextual decisions are drafted. A native gameplay word split needs '
        'correction before this batch can be registered or credited.'
    )
    return scope


def main():
    environment = vars(prior) | globals()
    environment['checked_release_chain'] = FunctionType(prior.checked_release_chain.__code__, environment)
    source = checked_text(getsource(prior.audit_remaining), {
        '== 27146': '== 27597',
        '== 2838 and len(pending) == 830': '== 3289 and len(pending) == 379',
        'set(range(2454, 2500)))':
            'set(range(2454, 2500)) | set(range(2288, 2359)) | set(range(2366, 2425)) | set(range(3320, 3393)))',
    })
    exec(compile(source, __file__ + '::audit', 'exec'), environment)
    audit = environment['audit_remaining']
    environment['audit_remaining'] = lambda *args: add_remaining_groups(audit(*args))
    environment['previous_candidate'] = prior.read(voyage.VERIFICATION / 'registered_release_verification.json')
    environment['clean_path_for_build'] = current.CLEAN
    source = checked_text(getsource(prior.main), {
        'clean_path = current.stage.CLEAN': 'clean_path = clean_path_for_build',
        'prior, release, manifest, registry, packages = checked_release_chain()':
            '_, release, manifest, registry, packages = checked_release_chain()\n    prior = previous_candidate',
        "assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']":
            "assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']\n"
            "    assert manifest['checks'][current.CHECK]",
        'release_entries=765, release_checks=100': 'release_entries=775, release_checks=110',
        'additional_editorial_records=247': 'additional_editorial_records=132',
        'All Routes Trade and Sailing promotion candidate': 'All Routes cumulative promotion candidate',
        'This build adds 247 reviews since Item Advice, including the last 70 item-advice replies, ':
            'This build adds 132 reviews since Voyage Reports across sailing hazards, dolphins and Golden Route exchanges. ',
        '124 Price Info descriptions and 53 sailing reactions. It includes Rafael’s tutorials, ':
            'It includes Rafael’s tutorials, both arrival-month label fixes, ',
        '27,146 credited reviews and 830 native shared keys': '27,597 credited reviews and 379 native shared keys',
        'Continue from [the registered sailing reactions]': 'The two arrival-month labels are registered.',
        '830 shared keys pending': '379 shared keys pending',
    })
    exec(compile(source, __file__ + '::reconstruct', 'exec'), environment)
    environment['main']()


if __name__ == '__main__':
    main()
