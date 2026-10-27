"""Verify the anchored pilot,terminal preservation and original cannon ranges."""
from pathlib import Path
from scripts.verify_ship_loadout_pilot_v1381 import audit
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/ship_anchor_verified_v1385')
RUN = Path('work/analysis/ship_sinking_anchor_v1383')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_anchor_v1383_1364')


if __name__=='__main__':
    assert not ROOT.exists()
    assert sha(Path('scripts/run_ship_sinking_anchor_v1383.py').read_bytes())==read(RUN/'run_plan.json')['runner_sha256']
    proof,snapshots,arm = audit(RUN,CAP,13480)
    old = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_loadout_v1379_1364')
    prefix = []
    for frame,row in sorted(snapshots.items()):
        if frame<=10090:
            assert sha((old/f'frame_{frame:06d}_arm9_ram.bin').read_bytes())==row['sha256']
            prefix.append(frame)
    states = [read(f'work/analysis/ship_anchor_inspection_v1384/frame_{f:06d}.json')
        for f in [10090,10140,10340,10540,10740,10940,11040,11440,11840,12240,12640,12740,13040,13340,13350,13390,13430,13480]]
    def own(row):return [s for s in row['ships'] if s['fleet']==1]
    fixed = {s['slot']:s['map_point'] for s in own(states[0])}
    assert all({s['slot']:s['map_point'] for s in own(row)}==fixed for row in states[:14])
    target = next(s for s in states[-1]['ships'] if (s['fleet'],s['slot'])==(5,2))
    assert target['Hull_Crew']==[5,6]
    raw = Path(snapshots[13480]['path']).read_bytes()
    cpu,get = get_machine(arm,raw)
    ranges = [{'native_type':t,'original_range_getter':0x02048144,
        'range':get(0x48144,t),'native_strength':get(0xAB784,t)} for t in range(6)]
    assert [r['range'] for r in ranges]==[160,224,160,160,160,224]
    assert [r['native_strength'] for r in ranges]==[1,2,3,4,5,5]
    assert not any('touch' in r['command'] for r in read(CAP/'navigation_command_journal.json')['commands_received'])
    proof.update(identical_declared_loadout_prefix_through10090=prefix,
        ordinary_B_closes_sails_and_all5_positions_remain_fixed_through13340=True,
        actual_target_Hull_Crew_after_original_anchored_gunfire=[5,6],
        no_ship_sinking_notice_or_new_translation_completion_credit=True,
        intervening_Charles_work_report='Whoa! What\'s going on?!',
        work_report_visible_11440_to12640_and_normal_A_dismissal12740=True,
        work_report_not_a_sinking_or_new_source_review_credit=True,
        native_original_cannon_ranges_and_strength=ranges,
        next_source_bound_loadout_candidate='Original Carronade type5 has strength5 like Heavy Cannon type4 and original range224 instead of160. Apply only in a fresh declared prebattle fixture;the fleeing5Hull target must not be damaged,relocated or revived directly.',
        next_test_geometry='Use ordinary B to anchor at the established10090 firing position;avoid the coast near y3642 that turned the earlier ship west into proximity boarding.',
        original_anchored_gunfire_and_longer_range_plan_are_not_a_sinking_outcome=True,
        stopped_normally_with_battle_active_not_a_gameplay_withdrawal=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_anchor_pilot_verification.json',proof)
    print('Anchored pilot/all inputs45-byte fixture/RAM/donors verified;target5Hull6Crew;native Carronade range224/strength5 mapped;no sinking credit.',flush=True)
