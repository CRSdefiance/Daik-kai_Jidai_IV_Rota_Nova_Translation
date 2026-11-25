"""Carry forward exact proofs for the references that change between the ROMs."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch import fleet_sighting_bearings_v1 as fleet_code
from dk4tool.patch import pirate_report_bearings_v1 as pirate
from dk4tool.patch import special_battle_target_names_v1 as battle
from scripts import checkpoint_pending_shared_native_20261115 as inventory
from scripts import checkpoint_shared_upstream_tails_20261115 as previous
from scripts import register_fleet_sighting_alerts_20261115 as fleet
from scripts import register_square_shop_captions_20261115 as square


base, current, BASE = previous.base, previous.current, previous.BASE
OUTPUT = previous.OUTPUT.with_name('shared_relocated_references_20261115_v1.json')
BATTLE_ALIAS_ENTRY = 0x01FFFCAC
BATTLE_ALIAS_TAIL = 0x01FFFCF8


def branch_target(arm, address, targets):
    at = address - BASE
    (source, target, kind), = inventory.branch_hits(arm[at:at + 4], address, targets)
    assert source == address and kind == 'arm_bl'
    return target


def report_calls(ja, en, earlier):
    before, after = [MainCodeFile(arm, BASE).sections[-1] for arm in (earlier, en)]
    assert before.ramAddress == after.ramAddress and len(before.data) <= len(after.data)
    assert before.data == after.data[:len(before.data)]
    assert inventory.branch_hits(bytes(after.data), after.ramAddress, {pirate.WRAPPER}) == [
        (fleet_code.WRAPPER_TAIL, pirate.WRAPPER, 'arm_b'), (BATTLE_ALIAS_TAIL, pirate.WRAPPER, 'arm_b')]
    tables = {**fleet_code.CALLSITES, pirate.CALL: pirate.TABLES, battle.CALL: (battle.TABLE,)}
    destinations = {**dict.fromkeys(fleet_code.CALLSITES, fleet_code.MAPPER_ENTRY),
                    pirate.CALL: fleet_code.PIRATE_ENTRY, battle.CALL: BATTLE_ALIAS_ENTRY}
    result = {}
    for site, pointers in tables.items():
        assert branch_target(ja, site, {pirate.WRAPPER}) == pirate.WRAPPER
        expected = {destinations[site]}
        assert branch_target(en, site, expected) == branch_target(earlier, site, expected)
        ids = set()
        for pointer in pointers:
            at = pointer - BASE
            assert ja[at:at + 32] == en[at:at + 32] == earlier[at:at + 32]
            ids.update(n for n in unpack_from('<8i', ja, at) if n >= 0)
        assert ids
        result[site] = sorted(ids)
    result[fleet_code.WRAPPER_TAIL] = sorted({n for site in tables if site != battle.CALL for n in result[site]})
    result[BATTLE_ALIAS_TAIL] = result[battle.CALL]
    return result


def lookup_calls(ja, en, earlier, records):
    result = {}
    for row in records['thumb_direct']:
        site = row['call_site']
        at = site - BASE
        assert en[at - 2:at + 4] == earlier[at - 2:at + 4]
        if row['literal']:
            at = row['literal'] - BASE
            assert en[at:at + 4] == earlier[at:at + 4]
        result[site] = [row['message_ID']]
    # The current Thumb entry uses the same ID as the original level-up lookup.
    assert unpack_from('<I', ja, 0x7E3F0) == (0xE3A00061,)
    assert branch_target(ja, 0x0207E404, {0x0205528C}) == 0x0205528C
    result[0x0207E404] = [97]

    first, last = records['source_card_original_supported_ids']
    assert (first, last) == (2815, 3032)
    before, after = [MainCodeFile(arm, BASE).sections[3] for arm in (earlier, en)]
    offset = 0x0238C5C4 - 0x02387A20
    assert before.ramAddress == after.ramAddress and before.data[offset:offset + 48] == after.data[offset:offset + 48]
    for site in records['source_card_origins']:
        assert branch_target(ja, site, {0x0205528C}) == 0x0205528C
        assert branch_target(en, site, {0x0238C5C4}) == branch_target(earlier, site, {0x0238C5C4})
        result[site] = list(range(first, last + 1))
    result[0x0238C5CC] = list(range(first, last + 1))
    return result


def main():
    assert not OUTPUT.exists()
    release, prior, art = map(base.load, (current.RELEASE, previous.OUTPUT, inventory.OUTPUT))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256'] == prior['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256'] == prior['clean_sha256']
    assert base.digest(fleet.ROM) == base.load(fleet.RELEASE)['candidate_sha256']
    assert base.digest(square.ROM) == art['candidate_sha256'] == base.load(square.RELEASE)['candidate_sha256']
    ja, en, fleet_arm, square_arm = (base.NdsImage.open(p).read_file(current.stage.ARM)
                                    for p in (current.stage.CLEAN, current.ROM, fleet.ROM, square.ROM))
    ids = report_calls(ja, en, fleet_arm) | lookup_calls(ja, en, square_arm, art['current_thumb_and_owned_table_routes'])
    paths = (previous.OUTPUT, current.RELEASE, fleet.RELEASE, inventory.OUTPUT, square.RELEASE, Path(__file__))
    clean_only, current_only = (prior[f'retained_other_{side}_reference_candidates'] for side in ('clean', 'current'))
    assert set(ids) == {row[0] for row in clean_only + current_only}
    pending = set(base.load(inventory.LEGACY)['pending_ids'])
    assert all(pending.isdisjoint(values) for values in ids.values())
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        supported_ids_by_changed_reference=ids, clean_only=clean_only, candidate_only=current_only,
        scope='Exact fleet, target alias, level-up and source-card dependencies of previously verified selectors.',
        evidence={str(path): base.digest(path) for path in paths}, new_gameplay_runs=0, new_dialogue_credit=0))
    print(f'Bound all {len(ids)} changed references to already checked message paths.')


if __name__ == '__main__':
    main()
