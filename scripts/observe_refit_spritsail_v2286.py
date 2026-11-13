"""Read-only exact revised help and auxiliary Spritsail label font observation."""
from pathlib import Path
source=Path('scripts/observe_refit_current_v2275.py').read_text()
source=source.replace('town_trade_port_contextual_reference_v1','refit_contextual_spritsail_v1').replace('refit_actual_v2276','refit_spritsail_actual_v2287').replace('all_routes_combined_v2171_candidate.nds','all_routes_combined_v2284_candidate.nds')
old="    if direct_help:\n";new="    direct_aux=candidate_text==b'Spritsail'\n    if direct_aux:\n     source_request=dict(frame=frame,ID='ARM9_REFIT_SPRITSAIL_LABEL',source='exact-revised-label-text',original_last_request=self.last)\n     modal=False;body=v[5];text=candidate_text\n    elif direct_help:\n";assert source.count(old)==1;source=source.replace(old,new)
old="source_request=source_request,direct_help_payload_match=direct_help,PC=pc";new="source_request=source_request,direct_help_payload_match=direct_help,direct_aux_label=direct_aux,PC=pc";assert source.count(old)==1;source=source.replace(old,new)
exec(compile(source,__file__,'exec'),globals())
