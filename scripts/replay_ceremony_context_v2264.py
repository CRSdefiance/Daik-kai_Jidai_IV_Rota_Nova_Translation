"""Fresh current source-bound ceremony choices, participants, sites and branch exchanges."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/ceremony_context_v2264');OLD=Path('scripts/context_ceremony_v806.py')
if __name__=='__main__':
    assert not ROOT.exists();snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256'];source=OLD.read_text()
    changes={'work/analysis/ceremony_context_v806':'work/analysis/ceremony_context_v2264','out/all_routes_combined_v803_candidate.nds':'out/all_routes_combined_v2171_candidate.nds','from dk4tool.patch.inn_editorial import current_entries':'from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries','E:/Rota Nova translations/Generated/work/emulation_v193/inn_v803_stays/frame_003200_arm9_ram.bin':Path(snapshot['path']).as_posix(),'7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad':'4df01b870562dc04d623fb5c0011d38100bc4062371d32ad2be12f352292260a'}
    for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
    save(ROOT/'current_replay_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_genuine_preinteraction_snapshot=snapshot,CPU_hero_facility_day_site_yesno_and_boundary_inputs_not_earned_states_or_actual_visits=True,all_source_code_spans_exact_to_clean=True,all52_source_records_and_complete_consumer_exchanges_replayed=True,no_ROM_runtime_or_emulator_fixture_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
