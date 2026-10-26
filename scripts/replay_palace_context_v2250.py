"""Replay all31 source consumers and native providers against current V2171."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/palace_context_v2250')
OLD=Path('scripts/context_palace_v795.py')
if __name__=='__main__':
    assert not ROOT.exists();snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    source=OLD.read_text();changes={'work/analysis/palace_editorial_v795':'work/analysis/palace_context_v2250','out/all_routes_combined_v792_candidate.nds':'out/all_routes_combined_v2171_candidate.nds','E:/Rota Nova translations/Generated/work/emulation_v193/palace_v794_context/frame_004800_arm9_ram.bin':snapshot['path']}
    for old,new in changes.items():assert source.count(old)==1;source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
    save(ROOT/'current_replay_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_genuine_preinteraction_snapshot=snapshot,CPU_letter_flag_and_numeric_inputs_not_earned_or_actual_events=True,all31_original_consumers_and218_monthly_providers_replayed=True,no_new_ROM_or_runtime_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
