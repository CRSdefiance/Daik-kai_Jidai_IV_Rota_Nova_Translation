"""Successor: use preserved V834 KANJI control; retain V2280 failed producer/proof."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/probe_refit_spoken_layouts_v2280.py')
if __name__=='__main__':
 source=OLD.read_text().replace('refit_spoken_layouts_v2280\'','refit_spoken_layouts_v2280b\'')
 anchor=" changes={\n";assert source.count(anchor)==1
 source=source.replace(anchor,anchor+" 'out/all_routes_combined_v255_candidate.nds':'out/all_routes_combined_v834_candidate.nds',\n")
 assert 'work/analysis/refit_dialogue_runtime_v833/native_layout_matrix.json'in source
 source=source.replace('work/analysis/refit_dialogue_runtime_v833/native_layout_matrix.json','work/analysis/refit_dialogue_v833/native_layout_matrix.json')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_spoken_layouts_v2280b/failure_successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),original_failure='All525 layouts passed; font comparison could not open the absent old V255 path. No fonts or completion were approved.',preserved_V834_KANJI_control_used_instead=True,historical_matrix_path_corrected_to_actual_runtime_ROOT=True,all525_cases_freshly_reexecuted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
