"""Complete current six selected Guild font calls; preserve unrelated observation rows."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

folder='guild_transactions_actual_v2237_V2171';ids={1071,1073,1074,1085,1086,1096}
path=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder/'common_observer/requests.json';obs=read(path)
selected=[r for r in obs['rows']if r['source_request']['ID']in ids]
assert {r['source_request']['ID']for r in selected}==ids and len(selected)==6
source=Path('scripts/probe_revised_compact_font_v2147.py').read_text()
for old,new in(('square_revised_continuations_v2147','guild_actual_continuations_v2243'),('promoter_context_live_v2144_V2143',folder),('all_routes_combined_v2143_candidate','all_routes_combined_v2171_candidate'),(" for row in obs['rows']:"," for row in obs['rows']:\n  if row['source_request']['ID'] not in {1071,1073,1074,1085,1086,1096}:continue")):
    assert old in source,old
    source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'selected_call_scope.json',dict(original_observer=str(path),original_observer_sha256=sha(path.read_bytes()),selected_IDs=sorted(ids),selected_calls=6,other3_font_rows_preserved_not_this_batch_or_source_attribution_approval=True,duplicate62_last_request_is_not_assumed_correct_item_description_ID=True,no_original_observer_mutation_or_VRAM_filename_collision=True,effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
