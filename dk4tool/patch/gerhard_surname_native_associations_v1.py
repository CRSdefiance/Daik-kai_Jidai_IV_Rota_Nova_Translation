"""Bind every final dispatch, query and terminal to its independent complete source/current/target map."""
from dk4tool.patch.gerhard_surname_evidence_v1 import expanded
NAMES='work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json'

def check_final_native_associations(data,result,sourcegroups,load,require):
    controls=data['native_controls'];names=load(NAMES)
    voices={r['source_selector']:r for r in names['native_static_selector_andvoice_resolution']['rows']}
    require(set(voices)=={1,9,16} and names['measured_default_macro_lengths']==dict(FI=3,FA=5,FO=9),'three source-bound static voices/Lil macros')
    texts={r['id']:(g,r) for g in result['groups'] for r in g['text_records']}
    require([d['id'] for d in controls['final_dispatches']]==list(texts),'five final dispatch source IDs in order')
    for d in controls['final_dispatches']:
        group,ref=texts[d['id']];raw=bytes.fromhex(ref['target_hex']);actor=voices[raw[0]]
        require(d['block']==group['block'] and d['final_offset']==ref['new_offset'] and d['final_stored_hex']==ref['target_hex'],'final stored dispatch physical reference')
        require(d['source_selector']==d['resolved_actor_ID']==actor['resolved_actor_ID']==raw[0] and d['source_voice_class']==actor['original_voice_class'],'original final dispatch actor andvoice')
        require(d['registered_catalog_match'] is None and not d['FE_original_null_actor_calls'] and d['all4MiB_actor_role_RNG_input_and_ABI_guards_exact'],'unmapped catalogue/FE paths not invented')
        require(d['boundaries']==[dict(boundary=0x020940B0,kind='unexecuted-UI-preparation'),dict(boundary=0x02054020,kind='unexecuted-progressive-body',actor_object=actor['actor_object'],FE_incidental_r1=None,text_hex=expanded(raw[1:]).hex())],'all original final dispatch boundaries/body/macro/actor references')
    queries=[];terminals={}
    for group in result['groups']:
        number=group['block'];source=sourcegroups[number]['all_source_commands'];current=group['all_current_commands'];target=group['all_target_commands']
        terminals.update({(number,'clean'):source[-1],(number,'current'):current[-1],(number,'target'):target[-1]})
        for a,b,c in zip(source,current,target,strict=True):
            if a['word']==0x8000:queries.append((number,a,b,c))
    require(len(queries)==len(controls['raw_predicates_andqueries'])==10,'all ten original query memberships')
    for proof,(number,*commands) in zip(controls['raw_predicates_andqueries'],queries,strict=True):
        require(proof['block']==number and proof['source_offset']==commands[0]['offset'] and proof['target_offset']==commands[2]['offset'],'original raw source/current/target membership')
        for case,command in zip(proof['cases'],commands,strict=True):require(case['offset']==command['offset'] and case['source_command_hex']==command['whole_command_hex'],'each exact original raw operand association')
    require([(e['block'],e['version']) for e in controls['normal_seeded_ends']]==list(terminals),'all six unique original terminal phases')
    for e in controls['normal_seeded_ends']:
        require(e['terminal']==terminals[e['block'],e['version']] and e['normal_value_carry_not_zero_assumption'],'complete terminal binds exact independent command map')
        require(all(not c['flagged_terminal'] and c['parser_end_contract_not_actual_branch_selection_or_full_VM_execution'] for c in e['cases']),'ordinary terminal scope not broadened into VM/gameplay claim')
    return dict(all_five_final_dispatches_ten_queries_six_terminals_sourcequalified=True)
