"""All82 production compiler positives;changed-input challenges keep every frozen guard active."""
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B54_B60_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue.hodram_B54_B60_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_B54_B60_names_v1 import validate_scoped_names
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_policy_validation_v8831b')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v2.json')
CONTRACT=Path('translations/hodram_B54_B60_native_contract_v1.json')
# Distinct consumers:FE,source punctuation,FI,FA,two-page prose,retention,rough NPC.
CHALLENGED={'DK4_MES_B56_R0010','DK4_MES_B54_R0018','DK4_MES_B57_R0007','DK4_MES_B55_R0006','DK4_MES_B59_R0023','DK4_MES_B54_R0006','DK4_MES_B58_R0039'}

def digest(value):return sha(json.dumps([type(value).__name__,value],ensure_ascii=False,sort_keys=True,default=repr).encode('utf-8'))

if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[DOC,NAMES]);frozen=contract();image=NdsImage.open(doc['current_ROM'])
    validate_runtime(image);validate_approved_batch(doc);validate_scoped_names(names)
    arm=image.read_file('/__arm9__.bin');bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    protected={Path(p) for p in frozen['dependencies']}|{DOC,NAMES,CONTRACT,Path(__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path('work/clean.nds')}
    protected|={Path('dk4tool/dialogue')/f'hodram_B54_B60_{k}_v1.py' for k in ['profile','layout','plan','names']}
    before={str(p):sha(p.read_bytes()) for p in protected}
    partial_path=Path('work/analysis/Hodram_B54_B60_policy_validation_v8831/partial_checked_cases.json')
    assert sha(partial_path.read_bytes())=='7c519f97d304f57ebc6c92390c805e0e5b5dbe536276df5807d7f1fc831caf72'
    previous=read(partial_path)
    assert previous['contract_sha256']==sha(CONTRACT.read_bytes()) and previous['terminal'] is False
    positives=deepcopy(previous['positive_speech_compilers']);negatives=deepcopy(previous['negative_cases'])
    assert len(positives)==80 and len(negatives)==542
    assert [r['id'] for r in positives]==[r['id'] for r in doc['records'][:80]]
    assert CHALLENGED.issubset({r['id'] for r in positives})
    assert len({r['label'] for r in negatives})==542
    for approved,record in zip(doc['records'][:80],positives,strict=True):
        binding=frozen['record_bindings'][approved['id']]
        assert record['compiled_hex']==approved['compiled_hex']==binding['compiled_hex']
        assert record['source_reference']==approved['source_reference'] and record['current_reference']==approved['current_reference'] and record['final_reference']==approved['final_reference']
        assert record['qa']['base_QA_issues']==approved['original_QA_issues']==binding['base_QA_issues']
        assert record['qa']['native_page_count']==approved['expected_native_pages']==binding['native_page_count']
        assert record['qa']['qa_waivers']==[] and not any(i['severity'] in ['warning','error'] for i in record['qa']['issues'])
        cases=[r for r in negatives if r['label'].startswith(approved['id']+':')]
        assert len(cases)==(67 if approved['id'] in CHALLENGED else 1)
        assert any(r['label']==approved['id']+':gate:formatting' for r in cases)
    assert all(r['actual_changed_input'] and r['rejected'] and r['original_sha256']!=r['changed_sha256'] and r['diagnostic'] for r in negatives)
    ROOT.mkdir(parents=True)
    def progress():save(ROOT/'partial_checked_cases.json',dict(positive_speech_compilers=positives,negative_cases=negatives,contract_sha256=sha(CONTRACT.read_bytes()),terminal=False,new_credit=0,full_goal_complete=False))
    def reject(label,original,changed,fn,expected=None):
        assert original!=changed and digest(original)!=digest(changed),label
        try:fn(changed)
        except ValueError as error:
            message=str(error);assert 'Native dependency changed' not in message and 'Frozen Hodram-B54-B60 contract changed' not in message,(label,message)
            if expected:assert expected in message,(label,expected,message)
            negatives.append(dict(label=label,original_sha256=digest(original),changed_sha256=digest(changed),actual_changed_input=True,rejected=True,diagnostic=message))
        else:raise AssertionError('Changed input accepted:'+label)
    for index,row in enumerate(doc['records']):
        if index<80:continue # Exact immutable saved evidence; no completed compiler/challenge replay.
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup'];block=bank[row['block']];consumer='FE-paper' if row['source_selector']==254 else 'progressive'
        p=profile_for(arm,block,ident,'/data/SC1.DK4',consumer);encoded=encode_relocatable_dialogue(raw,text,p);qa=audit_relocatable_dialogue_record(raw,text,p)
        binding=frozen['record_bindings'][ident]
        assert encoded.encoded.hex()==row['compiled_hex']==binding['compiled_hex']
        assert bytes.fromhex(row['stored_hex'])==encoded.encoded+(b' ' if row['compiler_owned_parity_space'] else b'')
        assert qa['native_page_count']==row['expected_native_pages']==binding['native_page_count'] and qa['base_QA_issues']==row['original_QA_issues']==binding['base_QA_issues']
        assert not any(i['severity'] in ['warning','error'] for i in qa['issues']) and qa['qa_waivers']==[]
        positives.append(dict(id=ident,block=row['block'],consumer=consumer,source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=row['final_reference'],compiled_hex=encoded.encoded.hex(),qa=qa))
        # Every individual record must actually participate in the all-five-gate pass.
        changed=deepcopy(doc);changed['records'][index]['review']['formatting']=False;reject(ident+':gate:formatting',doc,changed,validate_approved_batch)
        if ident in CHALLENGED:
            for gate in ['source','context','localization','naturalness']:
                changed=deepcopy(doc);changed['records'][index]['review'][gate]=False;reject(ident+':gate:'+gate,doc,changed,validate_approved_batch)
            fields={'english':row['english']+' Unapproved words.','logical_English':row['logical_English']+' Unapproved words.',
                'context':row['context']+' Invented family relationship.','source_meaning':row['source_meaning']+' Invented rank.',
                'speaker':'Unapproved Captain','localization_note':'','retention_reason':'Unreviewed reason',
                'source_hex':(bytes([raw[0]^1])+raw[1:]).hex(),'current_hex':row['current_hex']+'20','compiled_hex':row['compiled_hex']+'20','stored_hex':row['stored_hex']+'20',
                'source_selector':row['source_selector']^1,'source_complete_preamble_hex':row['source_complete_preamble_hex'][:-2]+'ff',
                'actual_observation_status':'all-conditional-lines-actually-visited','compiler_owned_parity_space':not row['compiler_owned_parity_space'],
                'qa_waivers':['weak-line-ending'],'qa_waiver_scope':dict(unscoped=True),'native_body_review_reason':'','formatting_approval_reason':'',
                'decision':'revision' if row['decision']=='retention' else 'retention','block':60 if row['block']!=60 else 54}
            for field,value in fields.items():
                assert row.get(field)!=value,(ident,field);changed=deepcopy(doc);changed['records'][index][field]=value;reject(ident+':approved-field:'+field,doc,changed,validate_approved_batch)
            for field in ['source_reference','current_reference','final_reference']:
                for part in ['block','offset','bytes','header_offset','record_index']:
                    changed=deepcopy(doc);changed['records'][index][field][part]+=1;reject(ident+':reference:'+field+':'+part,doc,changed,validate_approved_batch)
            for label,value in [('selector',bytes([raw[0]^1])+raw[1:]),('missing-first',raw[:1]+raw[2:]),('missing-final',raw[:-1]),('trailing-NUL',raw+b'\0')]:
                reject(ident+':source:'+label,raw,value,lambda r:encode_relocatable_dialogue(r,text,p),'complete source and reviewed logical paragraph required')
            for label,value in [('manual-break',text+'{LB}'),('raw-LF',text+'\n'),('alignment',text+'{ALIGN@0}'),('padding',text+'{PAD}'),('leading-space',' '+text),('trailing-space',text+' '),('extra-Unicode',text+'“'),('missing-final',text[:-1])]:
                reject(ident+':prose:'+label,text,value,lambda t:encode_relocatable_dialogue(raw,t,p),'complete source and reviewed logical paragraph required')
            for field,value in [('window_width_px',210),('max_lines',5),('default_ascii_width',7),('default_multibyte_width',10),('guard_linebreaks',False),('pair_phase_safe_breaks',False),('leading_speaker_bytes',frozenset({3})),('literal_prefix_policy','forbid'),('macro_ascii_lengths',dict(FI=7,FA=9,FO=15))]:
                bad=replace(p,**{field:value});reject(ident+':profile:'+field,p,bad,lambda q:encode_relocatable_dialogue(raw,text,q),'profile changed')
            reject(ident+':wrong-file','/data/SC1.DK4','/data/SC0.DK4',lambda path:profile_for(arm,block,ident,path,consumer),'file-qualified')
            reject(ident+':wrong-block',block,bytes([block[0]^1])+block[1:],lambda value:profile_for(arm,value,ident,'/data/SC1.DK4',consumer),'file-qualified')
            reject(ident+':other-owned-block',block,bank[60 if row['block']!=60 else 54],lambda value:profile_for(arm,value,ident,'/data/SC1.DK4',consumer),'file-qualified')
            reject(ident+':wrong-runtime',arm,bytes([arm[0]^1])+arm[1:],lambda value:profile_for(value,block,ident,'/data/SC1.DK4',consumer),'file-qualified')
            reject(ident+':wrong-consumer',consumer,'progressive' if consumer=='FE-paper' else 'FE-paper',lambda value:profile_for(arm,block,ident,'/data/SC1.DK4',value),'consumer required')
            progress();print('Distinct consumer challenged',ident,'total negatives',len(negatives),flush=True)
        if (index+1)%8==0:progress();print('Production compilers passed',index+1,'of82;negativecases',len(negatives),flush=True)
    for key,value in [('target_locale','en-GB'),('translation_policy','natural-dialogue-v1'),('file_path','/data/SC0.DK4'),('route',0),('route_identity','Maria'),('blocks',[54]),('encoder','raw'),('registered_predecessor_profile','all-routes-unified-v4701'),('full_goal_complete',True),('new_credit',82),('typed_choice_records',[dict(id='UNAPPROVED_TYPED_CHOICE',english='Yes.')]),('measured_limits',dict(all_conditional_lines_andhardware_verified=True))]:
        changed=deepcopy(doc);changed[key]=value;reject('batch:'+key,doc,changed,validate_approved_batch,'metadata required')
    for label,rows in [('missing-record',doc['records'][:-1]),('reordered-records',list(reversed(doc['records']))),('duplicate-record',[doc['records'][0],*doc['records'][:-1]])]:
        changed=deepcopy(doc);changed['records']=deepcopy(rows);reject('batch:'+label,doc,changed,validate_approved_batch,'complete ordered')
    changed=deepcopy(doc);changed['unapproved_extra_field']='invented';reject('batch:extra-field',doc,changed,validate_approved_batch,'approved batch keys')
    for index,row in enumerate(names['records']):
        for gate in frozen['review_gates']:
            changed=deepcopy(names);changed['records'][index]['review'][gate]=False;reject('names:'+str(row['actor_ID'])+':gate:'+gate,names,changed,validate_scoped_names,'source-qualified review')
        changed=deepcopy(names);changed['records'][index]['current_display']='Unapproved Captain';reject('names:'+str(row['actor_ID'])+':identity',names,changed,validate_scoped_names,'source-qualified review')
    for field,value in [('wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open',False),('full_name_shared_de_ownership_deployment_andconsumers_still_open',False),('actual_progressive_actor_IDs',list(range(207))),('offline_progressive_actor_IDs',[]),('new_credit',10)]:
        changed=deepcopy(names);changed[field]=value;reject('names:'+field,names,changed,validate_scoped_names,'source-qualified review')
    assert len(positives)==82 and len({r['label'] for r in negatives})==len(negatives) and len(negatives)==625
    assert {str(p):sha(p.read_bytes()) for p in protected}==before
    save(ROOT/'policy_validation.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        positive_speech_compilers=positives,resumed_from=str(partial_path),resumed_from_sha256=sha(partial_path.read_bytes()),reused_positive_compilers=80,reused_negative_cases=542,fresh_positive_compilers=2,fresh_negative_cases=83,original_terminal_count_failure_preserved=True,positive_no_typed_menu=True,positive_batch_andten_scoped_names=True,positive_editorial_units=82,
        negative_cases=negatives,negative_count=len(negatives),every_negative_actual_input_changed_andguard_rejected=True,all_frozen_dependency_guards_remained_enabled=True,
        every82individual_formatting_gate_andseven_distinct_consumer_classes_challenged=True,
        complete_batch_keys_source_current_final_refs_prose_gates_actual_scope_names_profiles_andruntime_tested=True,
        all_protected_files_ROMs_registry_ledger_andsource_inputs_hash_exact=True,protected_hashes=before,original24infos_zero_errors_warnings_waivers_preserved=True,
        independent_production_atomic_registered_build_patch_startup_andcredit_still_pending=True,no_ROM_registration_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
    print('82production compilers/10names/'+str(len(negatives))+'genuine changed-input rejections pass;allfrozen guards active;allprotected artifacts exact.No credit.',flush=True)
