"""Terminal Carronade pilot audit;no sinking or new editorial completion credit."""
import inspect
from pathlib import Path
from types import FunctionType
from scripts import verify_ship_loadout_pilot_v1381 as previous
from scripts.native_carronade_fixture_v1387 import apply_fixture
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha


if __name__=='__main__':
    root = Path('work/analysis/carronade_verified_v1390')
    assert not root.exists()
    source = inspect.getsource(previous.audit)
    old = "assert [r['after'] for r in fixture['cannon_equipment']]==[4,7,7,7,7]"
    assert source.count(old)==1
    source = source.replace(old,"assert [r['after'] for r in fixture['cannon_equipment']]==[5,7,7,7,7]")
    env = {**previous.__dict__,'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env)
    run = Path('work/analysis/carronade_sinking_v1388')
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/carronade_sinking_v1388_1364')
    assert sha(Path('scripts/run_carronade_sinking_v1388.py').read_bytes())==read(run/'run_plan.json')['runner_sha256']
    proof,snapshots,arm = env['audit'](run,cap,11880)
    assert proof['sole_fixture']['original_Carronade_range']==224
    last = read('work/analysis/carronade_inspection_v1389/frame_011880.json')
    assert all(s['Hull_Crew'][0]>0 for s in last['ships'])
    proof.update(final_native_ships=last['ships'],
        no_sinking_notice_or_new_translation_completion_credit=True,
        stopped_at_ordinary_battle_without_health_crew_RNG_result_or_during_duel_changes=True,
        original_closed_sails_new_fire_versus_in_flight_projectile_question_unresolved=True,
        no_original_engine_defect_inferred_from_pilot_firing_geometry=True,
        defer16_sinking_scene_gate_while_proceeding_with_other_unreviewed_editorial_families=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    root.mkdir(parents=True)
    save(root/'terminal_carronade_verification.json',proof)
    print('Original Carronade pilot45-byte fixture/input/RAM/PNGs/saves audited;no sinking or completion credit.',flush=True)
