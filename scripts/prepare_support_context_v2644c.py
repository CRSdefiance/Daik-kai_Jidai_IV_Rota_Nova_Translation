"""Bind actual58-fleet context;extra original fleet57 Manuel is already in matrix."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/prepare_support_context_v2644.py').read_text().replace("for row in old['original_source_fragments']:","for row in read(old['original_source_fragments']):").replace("row['address']-BASE","row['start']-BASE")
 old="assert[(r['fleet_ID'],r['name_hex'])for r in fleet_names]==[(r['fleet_ID'],r['name_hex'])for r in old['all_nonnull63_fleet_commander_labels']]"
 new="current_fleet_names={r['fleet_ID']:r['name_hex']for r in fleet_names};previous_fleet_names={r['fleet_ID']:r['name_hex']for r in old['all_nonnull63_fleet_commander_labels']};assert len(fleet_names)==58 and all(current_fleet_names[i]==v for i,v in previous_fleet_names.items())and set(current_fleet_names)-set(previous_fleet_names)=={57}and current_fleet_names[57]==b'Manuel'.hex()"
 assert source.count(old)==1;source=source.replace(old,new).replace('all57_current_nonnull_fleet_commander_labels','all58_current_nonnull_fleet_commander_labels').replace('outside the57fleet/28regular matrix','outside the58fleet/28regular matrix').replace('all20_factions57fleet_names28regular_names_current_exact','all20_factions58fleet_names28regular_names_current_exact').replace('20factions,57fleets','20factions,58fleets').replace('support_context_v2644','support_context_v2644c')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
