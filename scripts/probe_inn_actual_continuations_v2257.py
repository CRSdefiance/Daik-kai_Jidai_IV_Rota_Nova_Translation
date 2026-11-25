"""Complete current five Inn font calls; retain greeting63 as outside-batch context."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
folder='inn_actual_v2253_V2171';ids={1177,1178,1179,1180,1181}
path=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder/'common_observer/requests.json';obs=read(path);selected=[r for r in obs['rows']if r['source_request']['ID']in ids];assert len(selected)==5 and {r['source_request']['ID']for r in selected}==ids
source=Path('scripts/probe_revised_compact_font_v2147.py').read_text()
for old,new in(('square_revised_continuations_v2147','inn_actual_continuations_v2257'),('promoter_context_live_v2144_V2143',folder),('all_routes_combined_v2143_candidate','all_routes_combined_v2171_candidate'),(" for row in obs['rows']:"," for row in obs['rows']:\n  if row['source_request']['ID'] not in {1177,1178,1179,1180,1181}:continue")):
    assert old in source;source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'selected_call_scope.json',dict(original_observer=str(path),original_observer_sha256=sha(path.read_bytes()),selected_IDs=sorted(ids),selected_calls=5,greeting63_context_not_extra_editorial_credit=True,no_observer_mutation_or_VRAM_filename_collision=True,effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
