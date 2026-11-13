"""Reconstruct the latest registered cumulative ROM for acceptance testing."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import prepare_all_routes_promotion_20261111 as prior
from scripts import register_city_combat_notices_v1 as current
from scripts.source_locked_derivation_v5118 import checked_text


NAMES = prior.NAMES + ('crew_item_actions', 'fleet_reports', 'city_combat_notices')
PROMOTION = Path('out/promotion_ready_20261111_combat_and_fleet')
ROM = PROMOTION / 'Translation_DS_All_Routes_Combat_and_Fleet_20261111_candidate.nds'
ADJACENT = ROM.with_suffix('.manifest.json')
VERIFICATION = current.VERIFICATION


def main():
    environment = vars(prior) | globals()
    environment['checked_release_chain'] = FunctionType(prior.checked_release_chain.__code__, environment)
    audit = checked_text(getsource(prior.audit_remaining), {
        '== 27146': '== 27261',
        '== 2838 and len(pending) == 830': '== 2953 and len(pending) == 715',
        'set(range(2454, 2500)))': 'set(range(2454, 2500)) | set(range(2580, 2615)))',
    })
    exec(compile(audit, __file__ + '::audit', 'exec'), environment)
    previous_candidate = prior.read(prior.VERIFICATION / 'registered_release_verification.json')
    environment['previous_candidate'] = previous_candidate
    environment['clean_path_for_build'] = current.stage.first.review.CLEAN
    source = checked_text(getsource(prior.main), {
        'clean_path = current.stage.CLEAN': 'clean_path = clean_path_for_build',
        'prior, release, manifest, registry, packages = checked_release_chain()':
            '_, release, manifest, registry, packages = checked_release_chain()\n    prior = previous_candidate',
        'release_entries=765, release_checks=100': 'release_entries=768, release_checks=103',
        'additional_editorial_records=247': 'additional_editorial_records=115',
        'All Routes Trade and Sailing promotion candidate': 'All Routes Combat and Fleet promotion candidate',
        'This build adds 247 reviews since Item Advice, including the last 70 item-advice replies, ':
            'This build adds 115 reviews since Trade and Sailing, including 33 crew item-action replies, ',
        '124 Price Info descriptions and 53 sailing reactions. It includes Rafael’s tutorials, ':
            '47 fleet reports, and 35 city and combat notices. It includes Rafael’s tutorials, ',
        '27,146 credited reviews and 830 native shared keys': '27,261 credited reviews and 715 native shared keys',
        'Continue from [the registered sailing reactions]': 'Continue from [the registered city and combat notices]',
        '830 shared keys pending': '715 shared keys pending',
    })
    exec(compile(source, __file__ + '::reconstruct', 'exec'), environment)
    environment['main']()


if __name__ == '__main__':
    main()
