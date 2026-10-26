"""Successor with scoped current-font helper; no historical helper/global edits."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/probe_refit_spoken_layouts_v2280.py')
if __name__=='__main__':
 source=OLD.read_text().replace("refit_spoken_layouts_v2280'","refit_spoken_layouts_v2280c'")
 source=source.replace('work/analysis/refit_dialogue_runtime_v833/native_layout_matrix.json','work/analysis/refit_dialogue_v833/native_layout_matrix.json')
 anchor=' changes={\n';assert source.count(anchor)==1
 extra={
 'out/all_routes_combined_v255_candidate.nds':'out/all_routes_combined_v834_candidate.nds',
 'from scripts.verify_common_alignment_native_v257 import raster':"from scripts.primary_town_native_font_v2102 import font_tools\nraster,_,_=font_tools(NdsImage.open('out/all_routes_combined_v2171_candidate.nds'))"
 }
 source=source.replace(anchor,anchor+''.join(' '+repr(k)+':'+repr(v)+',\n'for k,v in extra.items()))
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_spoken_layouts_v2280c/failure_successor_provenance.json',dict(failed_producers=['scripts/probe_refit_spoken_layouts_v2280.py','scripts/probe_refit_spoken_layouts_v2280b.py'],failure='All525 layouts passed twice; an absent V255 path existed in both the top-level font comparison and the historical raster helper. Those runs approve no fonts.',current_font_scoped_helper='scripts/primary_town_native_font_v2102.py',helper_frozen_and_globals_unchanged=True,all525_cases_freshly_reexecuted=True,physical16pitch_font_oracle_separate_from_logical_capacity=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
