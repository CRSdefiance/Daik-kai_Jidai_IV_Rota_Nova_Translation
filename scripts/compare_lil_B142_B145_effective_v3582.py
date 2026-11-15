"""Expose old wording only after the fresh complete Japanese gloss and term binding."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
CONTROL=Path('work/analysis/lil_B142_B145_dispatches_v3574/all38_source_current_progressive_FE_dispatches_and_FI2.json')
CONTEXT=Path('work/analysis/lil_B142_B145_clean_context_v3573/all38_complete_clean_exchanges_and_fresh_glosses.json')
TERMS=Path('work/analysis/lil_B142_B145_terms_v3581/three_native_item_names_and_Mediterranean_Proof_context.json')
if __name__=='__main__':
    a=Path('scripts/compare_lil_B139_B140_effective_v3467.py');b=Path('scripts/compare_lil_B142_B145_effective_v3582b.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[('lil_B139_B140_comparison_v3467','lil_B142_B145_comparison_v3582'),('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json',SOURCE.as_posix()),('work/analysis/lil_B139_B140_controls_v3464/all67_dispatches12_predicates1_query_and_C200_contract.json',CONTROL.as_posix()),('work/analysis/lil_B139_B140_clean_context_v3465/all67_complete_clean_context_and_fresh_glosses.json',CONTEXT.as_posix()),('work/analysis/lil_B139_B140_terms_v3466/clean_current_items_polder_names_entries_and_copy_census.json',TERMS.as_posix()),('all67','all38'),('fresh67','fresh38'),('len(rows)==67','len(rows)==38'),('source_current_comparisons=67','source_current_comparisons=38'),('Seven static names including Janus4 andStudent171,FI7,twelve predicates,query129,C200 source-owned UI request,three items,polder terms andseparate B139/B140 entries bound. C200 resource bodies/actual transition remain unexecuted.','Nine static actors including Cesare0D andShipwright6D,one FE null-actor panel,FI2,six unforced predicates,25 relative sites,distinct900000/300000 payments,three native items andfour separate entries bound. Event143 leads through silent42 to144. C200/resource bodies and actual scene activation remain unexecuted.')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B142_B145_comparison_tool_v3582');assert not root.exists();root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
