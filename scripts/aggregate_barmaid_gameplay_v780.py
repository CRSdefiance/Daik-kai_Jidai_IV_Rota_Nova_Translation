"""Combine six original consumer samples and verify actual relationship outcomes."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/barmaid_integration_v780')


def actual_state(arm, raw, town):
    u = machine(arm)
    u.mem_write(0x02000000, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    info = bytes(u.mem_read(get(0x79D8, (town,)), 3))
    assert info[1] == town
    actor = get(0xCB184)+4+info[0]*32
    item = get(0xCB190)+4+info[2]*20
    stage = get(0x7DB0C, (actor,))
    get(0x49DE8, (0x02470020, item))
    descriptor = struct.unpack('<3I', u.mem_read(0x02470020, 12))
    return {'town': town, 'actor_ID': info[0], 'gift_item_ID': info[2],
            'original_relationship_stage': stage, 'original_gift_owner_kind': descriptor[1],
            'original_gift_owner_detail': descriptor[2], 'gift_availability_mask': get(0x4A224, (item,))}


def main():
    inputs = [ROOT/name for name in ('seville_intro_gameplay_verification.json',
                                    'maria_sofala_gameplay_verification.json',
                                    'seoul_gameplay_verification.json')]
    results = [read(p) for p in inputs]
    digest = read(ROOT/'patch_proof.json')['candidate_sha256']
    assert all(r['candidate_sha256'] == digest for r in results)
    holds = [h for r in results for h in r['holds']]
    ids = sorted({r['message_id'] for r in holds})
    assert ids == [989, 990, 991, 999, 1000, 1014] and len(holds) == 12
    assert all(sum(h['message_id'] == n for h in holds) == 2 for n in ids)
    assert all(h['complete_independent_font_and_blank_paper_exact'] and h['all_other_pixels_exact'] for h in holds)
    outcomes = []
    for result, town, stage in zip(results, (13, 34, 57), (1, 2, 2)):
        pair = []
        for report_path in result['capture_reports']:
            report = read(report_path)
            arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
            snapshots = {r['frame']: r for r in report['read_only_pause_RAM_snapshots']}
            before = actual_state(arm, Path(snapshots[3200]['path']).read_bytes(), town)
            after = actual_state(arm, Path(snapshots[result['normal_town_return_frame']]['path']).read_bytes(), town)
            assert before['original_relationship_stage'] == 0
            assert after['original_relationship_stage'] == stage
            assert after['original_gift_owner_kind'] == 6 and after['gift_availability_mask'] == 0
            if town == 57:
                assert before['original_gift_owner_kind'] == 4 and before['original_gift_owner_detail'] == 38
            else:
                assert before['original_gift_owner_kind'] == 6
            pair.append({'report': report_path, 'before': before, 'normal_return': after})
        assert pair[0]['before'] == pair[1]['before'] and pair[0]['normal_return'] == pair[1]['normal_return']
        outcomes.append(pair)
    boot = read(ROOT/'newgame_regression.json')
    assert boot['all_pixels_exact'] and len(boot['whole_screen_frame_pairs']) == 7
    proof = {
        'candidate_sha256': digest, 'scenarios': results,
        'scenario_proofs': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in inputs],
        'actual_IDs': ids, 'actual_complete_holds': 12,
        'consumer_families': {'989': 'barmaid then captain introduction', '990': 'captain then barmaid introduction',
                             '991': 'ordinary chat while requested gift unavailable', '999': 'gift response with captain first name',
                             '1000': 'static gift response', '1014': 'city-specific casual chat after gift'},
        'whole_screen_controls': sum(len(r['whole_screen_controls']) for r in results),
        'paired_state_model_object_task_frames': sum(len(r['paired_state_model_object_task_frames']) for r in results),
        'original_relationship_and_gift_outcomes': outcomes,
        'newgame_regression': str(ROOT/'newgame_regression.json'), 'newgame_whole_frame_pairs': 7,
        'only_declared_location_and_inventory_fixtures': True,
        'no_random_relationship_savestate_or_ROM_scene_injection': True,
        'other25_entries_have_source_native_layout_font_and_family_sampling_not_individual_activation': True,
        'latent996_retained_without_normal_activation_claim': True,
        'normal_travel_earned_gift_acquisition_full_playthrough_hardware_not_claimed': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT/'gameplay_verification.json', proof)
    print('Six original consumer families,12 complete holds,', proof['whole_screen_controls'],
          'whole controls,', proof['paired_state_model_object_task_frames'], 'state/model/task pairs and original outcomes verified.', flush=True)


if __name__ == '__main__':
    main()
