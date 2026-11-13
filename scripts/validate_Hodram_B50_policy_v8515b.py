"""Exercise every approved B50 compiler andmeaningful changed-input policy rejections;never edit frozen inputs."""
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B50_profile_v2 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue.hodram_B50_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_B50_names_v2 import validate_scoped_names
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_policy_validation_v8515b')
DOC=Path('translations/hodram_B50_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B50_speaker_name_review_v2.json')

def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,default=repr).encode('utf8'))

if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[DOC,NAMES]);frozen=contract();image=NdsImage.open(doc['current_ROM'])
    validate_runtime(image);validate_approved_batch(doc);validate_scoped_names(names)
    arm=image.read_file('/__arm9__.bin');bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    protected={Path(p) for p in frozen['dependencies']}|{DOC,NAMES,Path('translations/hodram_B50_native_contract_v2.json'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path('work/clean.nds'),Path(__file__)}
    protected|={Path('dk4tool/dialogue')/('hodram_B50_'+suffix+'_v2.py') for suffix in ['profile','layout','plan','names']}
    before={str(p):sha(p.read_bytes()) for p in protected};positives=[];negatives=[];ROOT.mkdir(parents=True)
    def reject(label,original,changed,fn,expected=None):
        assert original!=changed and digest(original)!=digest(changed),label
        try:fn(changed)
        except ValueError as error:
            message=str(error)
            assert 'Native dependency changed' not in message and 'Frozen Hodram-B50 contract changed' not in message,(label,message)
            if expected is not None:assert expected in message,(label,expected,message)
            negatives.append(dict(label=label,original_sha256=digest(original),changed_sha256=digest(changed),actual_changed_input=True,rejected=True,diagnostic=message,expected_guard=expected or 'approved source/context/prose/reference/review or exact source-order policy'))
        else:raise AssertionError('Changed input accepted:'+label)
    for index,row in enumerate(doc['records']):
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup'];block=bank[50]
        kind='FE-paper' if row['source_selector']==254 else 'progressive';p=profile_for(arm,block,ident,'/data/SC1.DK4',kind)
        encoded=encode_relocatable_dialogue(raw,text,p);qa=audit_relocatable_dialogue_record(raw,text,p)
        assert encoded.encoded.hex()==row['compiled_hex']==frozen['record_bindings'][ident]['compiled_hex']
        assert qa['native_page_count']==1 and qa['issues']==frozen['record_bindings'][ident]['base_QA_issues'] and qa['qa_waivers']==[]
        assert all(i['severity']=='info' and i['code']=='line-break-count' for i in qa['issues'])
        positives.append(dict(id=ident,consumer=kind,source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=row['final_reference'],compiled_hex=encoded.encoded.hex(),qa=qa))
        for gate in frozen['review_gates']:
            changed=deepcopy(doc);changed['records'][index]['review'][gate]=False
            reject(ident+':gate:'+gate,doc,changed,validate_approved_batch)
        for field,value in {
            'english':row['english']+' Unapproved words.','logical_English':row['logical_English']+' Unapproved words.',
            'context':row['context']+' Invented family relationship.','source_meaning':row['source_meaning']+' Invented rank.',
            'speaker':'Unapproved Captain','localization_note':'','retention_reason':'Unreviewed reason',
            'source_hex':(bytes([raw[0]^1])+raw[1:]).hex(),'current_hex':row['current_hex']+'20',
            'compiled_hex':row['compiled_hex']+'20','source_selector':254 if row['source_selector']!=254 else 1,
            'qa_waivers':['weak-line-ending'],'qa_waiver_scope':dict(unscoped=True),'native_body_review_reason':'',
        }.items():
            assert row.get(field)!=value,(ident,field)
            changed=deepcopy(doc);changed['records'][index][field]=value
            reject(ident+':approved-field:'+field,doc,changed,validate_approved_batch)
        for field in ['source_reference','current_reference','final_reference']:
            for part in ['offset','bytes','header_offset','record_index']:
                changed=deepcopy(doc);changed['records'][index][field][part]+=1
                reject(ident+':reference:'+field+':'+part,doc,changed,validate_approved_batch)
        for label,value in [('selector',bytes([raw[0]^1])+raw[1:]),('missing-first',raw[:1]+raw[2:]),('missing-final',raw[:-1]),('trailing-NUL',raw+b'\0')]:
            reject(ident+':source:'+label,raw,value,lambda r:encode_relocatable_dialogue(r,text,p),'complete source and reviewed logical paragraph required')
        for label,value in [('manual-break',text+'{LB}'),('raw-LF',text+'\n'),('alignment',text+'{ALIGN@0}'),('padding',text+'{PAD}'),('leading-space',' '+text),('trailing-space',text+' '),('Unicode-punctuation',text+'“'),('missing-final',text[:-1])]:
            reject(ident+':prose:'+label,text,value,lambda t:encode_relocatable_dialogue(raw,t,p),'complete source and reviewed logical paragraph required')
        for field,value in [('window_width_px',210),('max_lines',5),('default_ascii_width',7),('default_multibyte_width',10),('guard_linebreaks',False),('pair_phase_safe_breaks',False),('leading_speaker_bytes',frozenset({3})),('literal_prefix_policy','forbid'),('macro_ascii_lengths',dict(FI=7,FA=9,FO=15))]:
            bad=replace(p,**{field:value});assert bad!=p
            reject(ident+':profile:'+field,p,bad,lambda q:encode_relocatable_dialogue(raw,text,q),'profile changed')
        reject(ident+':wrong-file','/data/SC1.DK4','/data/SC0.DK4',lambda path:profile_for(arm,block,ident,path,kind),'file-qualified')
        reject(ident+':wrong-block',block,bytes([block[0]^1])+block[1:],lambda value:profile_for(arm,value,ident,'/data/SC1.DK4',kind),'file-qualified')
        reject(ident+':wrong-runtime',arm,bytes([arm[0]^1])+arm[1:],lambda value:profile_for(value,block,ident,'/data/SC1.DK4',kind),'file-qualified')
        reject(ident+':wrong-consumer',kind,'progressive' if kind=='FE-paper' else 'FE-paper',lambda value:profile_for(arm,block,ident,'/data/SC1.DK4',value),'consumer required')
        print('POLICY_PASS',ident,'negatives',len(negatives),flush=True)
    assert not frozen['choice_bindings'] and not doc.get('typed_choice_records')
    changed=deepcopy(doc);changed['typed_choice_records']=[dict(id='UNAPPROVED_TYPED_CHOICE',english='Yes.')]
    reject('no-typed-menu-authorized',doc,changed,validate_approved_batch,'typed menu records authorized')
    for key,value in [('target_locale','en-GB'),('translation_policy','natural-dialogue-v1'),('file_path','/data/SC0.DK4'),('route',0),('blocks',[48]),('encoder','raw')]:
        changed=deepcopy(doc);changed[key]=value;reject('batch:'+key,doc,changed,validate_approved_batch,'metadata required')
    for index,row in enumerate(names['records']):
        for gate in frozen['review_gates']:
            changed=deepcopy(names);changed['records'][index]['review'][gate]=False
            reject('names:'+str(row['actor_ID'])+':gate:'+gate,names,changed,validate_scoped_names,'source-qualified review')
        changed=deepcopy(names);changed['records'][index]['current']='Unapproved Name'
        reject('names:'+str(row['actor_ID'])+':identity',names,changed,validate_scoped_names,'source-qualified review')
    changed=deepcopy(names);changed['no_FE_personal_actor_name']=False
    reject('names:FE-membership',names,changed,validate_scoped_names,'source-qualified review')
    assert len(positives)==3 and sum(len(p['qa']['issues']) for p in positives)==3
    assert {str(p):sha(p.read_bytes()) for p in protected}==before
    save(ROOT/'policy_validation.json',dict(contract='translations/hodram_B50_native_contract_v2.json',contract_sha256=sha(Path('translations/hodram_B50_native_contract_v2.json').read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_speech_compilers=positives,positive_no_typed_menu=True,positive_batch_andone_scoped_name=True,positive_editorial_units=3,negative_cases=negatives,negative_count=len(negatives),every_negative_actual_input_changed_andguard_rejected=True,all_frozen_dependency_guards_remained_enabled=True,all_protected_files_ROMs_registry_ledger_andsource_inputs_hash_exact=True,protected_hashes=before,three_original_infos_zero_warnings_waivers_preserved=True,complete_original_B50_prose_controls_andcoherent_gift_phrase_boundary_frozen=True,independent_native_actual_evidence_atomic_stage_registered_build_andstartup_still_pending=True,no_ROM_registration_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
    print('B50 policy:3 speech compiler positives/no typedmenu/allfivegates/one scopedname pass;',len(negatives),'actualchanged-input rejections. Frozen files/ROMs/source/registry/ledger exact;zero credit.',flush=True)
