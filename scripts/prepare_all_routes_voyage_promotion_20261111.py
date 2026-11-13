"""Reconstruct the cumulative Voyage Reports ROM and audit its editorial coverage."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import prepare_all_routes_combat_promotion_20261111 as combat
from scripts import prepare_all_routes_promotion_20261111 as prior
from scripts import register_oasis_and_whale_reports_v1 as current
from scripts.source_locked_derivation_v5118 import checked_text


NAMES = combat.NAMES + ('pirate_and_retreat_reports', 'battle_commands_and_outcomes',
                        'crew_and_shore_reports', 'oasis_and_whale_reports')
PROMOTION = Path('out/promotion_ready_20261111_voyage_reports')
ROM = PROMOTION / 'Translation_DS_All_Routes_Voyage_Reports_20261111_candidate.nds'
ADJACENT = ROM.with_suffix('.manifest.json')
VERIFICATION = current.VERIFICATION


def add_remaining_groups(audit, clean, candidate, ledger, release):
    scope = audit(clean, candidate, ledger, release)
    shared = scope['shared_native_COMMON']
    pending = set(shared['pending_ids'])
    sailing = set(range(2366, 2425))
    catalogue = set(range(3251, 3668))
    other = pending - sailing - catalogue
    assert sailing | catalogue <= pending and len(other) == 35
    shared['pending_scope_groups'] = dict(
        sailing_exchange_candidates=len(sailing), catalogue_range_keys=len(catalogue),
        other_legacy_menu_and_shared_keys=len(other), other_pending_ids=sorted(other))
    return scope


def main():
    environment = vars(prior) | globals()
    environment['checked_release_chain'] = FunctionType(prior.checked_release_chain.__code__, environment)
    source = checked_text(getsource(prior.audit_remaining), {
        '== 27146': '== 27465',
        '== 2838 and len(pending) == 830': '== 3157 and len(pending) == 511',
        'set(range(2454, 2500)))': 'set(range(2454, 2500)) | set(range(2288, 2359)))',
    })
    exec(compile(source, __file__ + '::audit', 'exec'), environment)
    audit = environment['audit_remaining']
    environment['audit_remaining'] = lambda *args: add_remaining_groups(audit, *args)
    environment['previous_candidate'] = prior.read(combat.VERIFICATION / 'registered_release_verification.json')
    environment['clean_path_for_build'] = current.v1.review.CLEAN
    source = checked_text(getsource(prior.main), {
        'clean_path = current.stage.CLEAN': 'clean_path = clean_path_for_build',
        'prior, release, manifest, registry, packages = checked_release_chain()':
            '_, release, manifest, registry, packages = checked_release_chain()\n    prior = previous_candidate',
        'release_entries=765, release_checks=100': 'release_entries=772, release_checks=107',
        'additional_editorial_records=247': 'additional_editorial_records=204',
        'All Routes Trade and Sailing promotion candidate': 'All Routes Voyage Reports promotion candidate',
        'This build adds 247 reviews since Item Advice, including the last 70 item-advice replies, ':
            'This build adds 204 reviews since Combat and Fleet across pirate and retreat reports, ',
        '124 Price Info descriptions and 53 sailing reactions. It includes Rafael’s tutorials, ':
            'battle commands and outcomes, crew and shore reports, and oasis and whale reports. It includes Rafael’s tutorials, ',
        '27,146 credited reviews and 830 native shared keys': '27,465 credited reviews and 511 native shared keys',
        'Continue from [the registered sailing reactions]': 'Continue from [the registered oasis and whale reports]',
        '830 shared keys pending': '511 shared keys pending',
    })
    exec(compile(source, __file__ + '::reconstruct', 'exec'), environment)
    environment['main']()


if __name__ == '__main__':
    main()
