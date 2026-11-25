"""Prepare an independent lossless-history and once-only B183 completion audit."""
from pathlib import Path
from scripts.prepare_lil_B181_compiler_v4865 import alter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

INVENTORY="""    assert scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open'] and scope['completed_B183_previously_uncredited_objects']==25
    assert scope['next_earlier_wrap_revisit_leads']==[682,764,774,775]
    inventory,oldinv=read(scope['path']),read(before['unfinished_editorial_scope_v4919']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    same_except(oldinv,inventory,{'next_focus','broader_coverage_units','historical_B183_lead_before_v4971','remaining_B183_unreviewed_uncredited','lil_B183_completed_v4971'})
    assert inventory['historical_B183_lead_before_v4971']==oldinv['next_B183_clean_context_v4923']
    assert inventory['remaining_B183_unreviewed_uncredited']['physical_speeches']==0
    for a,b in zip(oldinv['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']=='all-route-scenes':same_except(a,b,{'reviewed_route_records','completed_route_records','next'})
        else:assert a==b
    lead=read(SOURCE);assert len(lead['records'])==25 and lead['new_review_credit']==0 and lead['read_no_predecessor_English']
    assert {('/data/SC2.DK4','DK4_MES_B183_R'+str(r['source_record_index']).zfill(4)) for r in lead['records']}<=set(keys)
"""

if __name__=='__main__':
    root=Path('work/analysis/lil_B183_audit_tools_v4972');out=Path('scripts/audit_lil_B183_completion_v4972.py');assert not root.exists() and not out.exists()
    text=Path('scripts/audit_lil_B182_completion_v4920.py').read_text(encoding='utf-8')
    a=text.index("    assert scope['canonical_Maria32_pending_uncredited']");b=text.index('    release,start,view,actual,transitions,reg=',a)
    text=text[:a]+INVENTORY+text[b:]
    text=alter(text,{
        'B182':'B183','complete_lil_B182_v4919':'complete_lil_B183_v4971b','PRIOR,B183':'PRIOR,SOURCE',
        'unfinished_editorial_scope_v4919\',\'lil_B182_completion_v4919':'unfinished_editorial_scope_v4971\',\'lil_B183_completion_v4971',
        "scope=ledger['unfinished_editorial_scope_v4919']":"scope=ledger['unfinished_editorial_scope_v4971']",
        "{'lil_B182_v4919'}":"{'lil_B183_v4971'}",'5941':'5966','5944':'5969','3764':'3780','2177':'2186','4088':'4113','4342':'4367',
        'len(rows)==8':'len(rows)==25','==(6,2,6,2)':'==(16,9,16,9)','source_prose_and_completion_credit_added_once\']==8':"source_prose_and_completion_credit_added_once']==25",
        "new_completed_records']==8":"new_completed_records']==25",'dict(revised=6,retained=2)':'dict(revised=16,retained=9)',
        "completion_credit_added']==8":"completion_credit_added']==25",
        'all564_manifest_batches':'all565_manifest_batches','equal_V4867':'equal_V4914',"reg['negative_count']==58":"reg['negative_count']==57",'==58 and all':'==57 and all',
        'release_tools_v4914':'release_tools_v4966',"tests['output']":"tests['stdout']",'reference_v4898':'reference_v4950',"len(manifest['batches'])==564":"len(manifest['batches'])==565",
        'blocks[182]':'blocks[183]','actual_source_event182':'actual_source_event183',"{'progressive':7,'system-FE':1}":"{'progressive':23,'system-FE':2}",
        "actual['complete_matching_observations']==8":"actual['complete_matching_observations']==25",'==[23,23]':'==[37,37]','==[4776,4775]':'==[8855,8854]',
        "transitions['nontext_equal_samples']==115":"transitions['nontext_equal_samples']==149",'dict(total=13,speech=7,control_or_end=6)':'dict(total=11,speech=9,control_or_end=2)',
        "len(transitions['actual_timing_differences'])==13":"len(transitions['actual_timing_differences'])==11",
        "assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==18":"assert not transitions['sampled_postscene_whole_RGB_differences_unmasked'] and transitions['all_sampled_postscene_whole_RGB_equal']",
        'postscene9001':'postscene11001','[3723009301,403514907]':'[1228390232,713326998]',
        'lil_B182_contextual_reference_v4910':'lil_B183_contextual_native_reference_v4955',
        'from scripts.verify_editorial_handoff_v4911 import audit_scene':'from scripts.verify_editorial_handoff_v4956 import audit as audit_scene',
        'source_prose_and_completion_adds8_once':'source_prose_and_completion_adds25_once',
        'Staged B182 completion audited:8 source/prose+8 completions once;5941 unique completed keys':'Staged B183 completion audited:25 source/prose+25 completions once;5966 unique completed keys',
    })
    # The inserted inventory section reads the previous inventory; preserve that historical key.
    compile(text,str(out),'exec');out.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('scripts/apply_lil_B182_completion_v4919.py','scripts/apply_lil_B183_completion_v4971.py',{'B182':'B183','completion_v4919':'completion_v4971'})]
    tools.append(derive('scripts/verify_editorial_handoff_v4921.py','scripts/verify_editorial_handoff_v4973.py',{
        'B182':'B183','audit_lil_B182_completion_v4920':'audit_lil_B183_completion_v4972','complete_lil_B182_v4919':'complete_lil_B183_v4971b',
        'editorial_handoff_verification_v4921':'editorial_handoff_verification_v4973','V4919':'V4971','V4914':'V4966',
        '5941':'5966','5944':'5969','3764':'3780','2177':'2186','new_source_prose_and_completion_credit=8':'new_source_prose_and_completion_credit=25',
        'all564_manifest_entries':'all565_manifest_entries','all8_actual_scene_panels_and_conditional_controls':'all25_actual_scene_panels_and_linear_controls',
        'native_state_equality_and_unequal_final_PRNG_timings_indicator_differences_disclosed':'native_state_and_sampled_RGB_equality_with_unequal_final_PRNG_and11_timings_disclosed',
        'next_B183_clean_only_uncredited_objects=25':'completed_B183_previously_uncredited_objects=25',
        'B18325 uncredited;full goal active.':'B18325 integrated once;earlier wrapping and full goal remain active.',
    }))
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(audit=str(out),tools=tools,no_ledger_or_document_mutation_yet=True,full_goal_complete=False))
