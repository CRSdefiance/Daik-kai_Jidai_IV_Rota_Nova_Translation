"""Derive the independent additive-ledger audit for B176's exact source shape."""
import re
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_audit_preparation_v4574')
assert not ROOT.exists()
source=Path('scripts/verify_editorial_handoff_v4520.py')
target=Path('scripts/verify_editorial_handoff_v4574.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
start=text.index("    controls=read(doc['source_effect_and_predicate_contract'])")
end=text.index("    scope=ledger[",start)
text=text[:start]+"""    controls=read(doc['source_effect_and_predicate_contract']);branch=read(doc['branch_proof'])
    assert len(controls['all3_source_current_nonrelative_nonspeech_leaves'])==3
    assert controls['source_declared_end_offsets']==[386] and len(controls['source_C200_pairs'])==1
    assert len(controls['one_A000_structural_cases'])==1
    assert controls['source_A000_hex_by_offset']=={'8':'00a0ffff010a0da1'}
    assert not controls['source_predicate_cases'] and not controls['source_pause_resume_pairs']
    assert controls['no_source_relative_predicate_2000_pause_2100_4100_resources_or_presentation_sites'] and not branch['cases']
    assert len(controls['source_linear_path_command_offsets'])==13 and controls['all10_speeches_on_complete_linear_structural_path']
    names=read(doc['source_nameplate_consumer_proof']);cases=names['native_four_consumer_cases']['rows']
    assert names['approved_prose_names']=={'174':'Owner','175':'Cook'} and len(cases)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['actor_ID'] in [174,175] for r in cases)
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in cases)
    terms=read(doc['actor_terminology_reconciliation'])
    assert terms['chosen_city']=='Seville' and len(terms['exact_city_source_current_pointer_bindings'])==2
    assert terms['chosen_ordinary_commodity_word']=='bananas' and terms['FE_Seville_notice_preserves_prospective_likelihood_not_current_or_guaranteed_boom']
"""+text[end:]
replacements={
    'checkpoint_lil_B175_v4519':'checkpoint_lil_B176_v4573',
    'editorial_handoff_verification_v4520':'editorial_handoff_verification_v4574',
    'unfinished_editorial_scope_v4519':'unfinished_editorial_scope_v4573',
    'unfinished_editorial_scope_v4500':'unfinished_editorial_scope_v4545',
    'lil_B175_scope_reconciliation_v4519':'lil_B176_scope_reconciliation_v4573',
    'lil_B175_v4519':'lil_B176_v4573',
    'remaining_B176_B180':'remaining_B177_B180',
    'all32':'all10','and13_retentions':'and5_retentions',
    'all4_complete_native_sheets_viewed':'all2_complete_native_sheets_viewed',
    'V4519':'V4573','v4519':'v4573','V4496':'V4541','v4496':'v4541','B175':'B176',
}
# Transform template quantities before inserting B176-specific controls above:
# selector175,command13 and name-case4 must remain literal source facts.
prefix=text[:text.index("    controls=read(doc['source_effect_and_predicate_contract'])")]
middle=text[len(prefix):text.index("    scope=ledger[",len(prefix))]
suffix=text[len(prefix)+len(middle):]
numbers={32:10,19:5,13:5,175:176,58:48,5865:5875,5833:5865,5868:5878,
         4012:4022,4266:4276,4234:4266,3709:3728,2124:2137,256:80,23:9,9:1,24:18,4:2,61:49}
def convert(s,counts):
    mapping={**replacements,**({str(k):str(v) for k,v in numbers.items()} if counts else {})}
    pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<!\d)'+k+r'(?!\d)' for k in sorted(mapping,key=len,reverse=True))
    return re.sub(pattern,lambda m:mapping[m.group()],s)
text=convert(prefix,True)+convert(middle,False)+convert(suffix,True)
# Source macros are absent: three invented-macro cases rather than the template's nine.
text=text.replace("('source_macro_preservation_negatives',1)","('source_macro_preservation_negatives',3)")
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8',newline='\n')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),
    target=str(target),target_sha256=sha(target.read_bytes()),full_goal_complete=False))
