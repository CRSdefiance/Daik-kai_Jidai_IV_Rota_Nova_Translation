"""Exercise approved mixed-consumer positives and meaningful changed-input source/prose/profile rejections."""
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue.hodram_outcomes_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_outcomes_names_v1 import validate_scoped_names
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_policy_validation_v8346')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v2.json')

def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,default=repr).encode('utf8'))

if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[DOC,NAMES]);frozen=contract();image=NdsImage.open(doc['current_ROM']);validate_runtime(image);validate_approved_batch(doc);validate_scoped_names(names)
    bank=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks;arm=image.read_file('/__arm9__.bin');positives=[];negatives=[]
    protected={Path(p) for p in frozen['dependencies']}|{DOC,NAMES,Path('translations/hodram_outcomes_native_contract_v1.json'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path('work/clean.nds'),Path(__file__),Path('dk4tool/dialogue/hodram_outcomes_profile_v1.py'),Path('dk4tool/dialogue/hodram_outcomes_names_v1.py')}
    before={str(p):sha(p.read_bytes()) for p in protected}
    def reject(label,original,changed,fn,expected):
        assert original!=changed and digest(original)!=digest(changed),label
        try:fn(changed)
        except ValueError as error:
            message=str(error);assert expected in message,(label,expected,message);negatives.append(dict(label=label,original_sha256=digest(original),changed_sha256=digest(changed),actual_changed_input=True,rejected=True,expected_guard=expected,diagnostic=message))
        else:raise AssertionError('Changed input was accepted:'+label)
    for index,row in enumerate(doc['records']):
        ident=row['id'];kind='FE-paper' if row['source_selector']==254 else 'progressive';p=profile_for(arm,bank[row['block']],ident,doc['file_path'],kind);raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup']
        encoded=encode_relocatable_dialogue(raw,text,p);qa=audit_relocatable_dialogue_record(raw,text,p)
        assert encoded.encoded.hex()==row['compiled_hex']==frozen['record_bindings'][ident]['compiled_hex'] and qa['native_page_count']==1 and qa['issues']==frozen['record_bindings'][ident]['base_QA_issues']
        assert all(i['severity']=='info' for i in qa['issues']) and qa['qa_waivers']==[]
        positives.append(dict(id=ident,consumer=kind,source_reference=row['source_reference'],current_reference=row['current_reference'],compiled_hex=encoded.encoded.hex(),qa=qa))
        for gate in frozen['review_gates']:
            changed=deepcopy(doc);changed['records'][index]['review'][gate]=False
            reject(ident+':gate:'+gate,doc,changed,validate_approved_batch,'per-record source, context, localization, naturalness, and formatting review')
        changes={
            'english':row['english']+' Unapproved words.',
            'logical_English':row['english']+' Unapproved words.',
            'context':row['context']+' Invented relationship.',
            'source_meaning':row['source_meaning']+' Invented fact.',
            'speaker':'Captain Lil' if row['source_selector']==2 else 'Lil Argot',
            'localization_note':'',
            'retention_reason':'Unreviewed retention reason',
            'source_hex':(bytes([raw[0]^1])+raw[1:]).hex(),
            'current_hex':row['current_hex']+'20',
            'compiled_hex':row['compiled_hex']+'20',
            'source_selector':2 if row['source_selector']==254 else 254,
            'qa_waivers':['weak-line-ending'],
            'qa_waiver_scope':dict(unscoped=True),
            'native_body_review_reason':'',
        }
        for field,value in changes.items():
            changed=deepcopy(doc);changed['records'][index][field]=value
            reject(ident+':approved-field:'+field,doc,changed,validate_approved_batch,'localization_note' if field=='localization_note' else 'required')
        for field in ['source_reference','current_reference','integrated_reference_pending']:
            for part in ['offset','bytes','header_offset','record_index']:
                changed=deepcopy(doc);changed['records'][index][field][part]+=1
                reject(ident+':reference:'+field+':'+part,doc,changed,validate_approved_batch,'required')
        for label,changed in [('leading-byte',(bytes([raw[0]^1])+raw[1:])),('missing-first',raw[:1]+raw[2:]),('missing-final',raw[:-1]),('trailing-control',raw+b'\0')]:
            reject(ident+':compiler-source:'+label,raw,changed,lambda value:encode_relocatable_dialogue(value,text,p),'complete source and reviewed logical paragraph required')
        for changed in [text+'{LB}',text+'\n',text+'{ALIGN@0}',text+'{PAD}',text+' ',text.replace('{SPEAKER:','{SPEAKER:FF')]:
            reject(ident+':compiler-text:'+str(len(negatives)),text,changed,lambda value:encode_relocatable_dialogue(raw,value,p),'complete source and reviewed logical paragraph required')
        profile_changes=[dict(window_width_px=228),dict(max_lines=8),dict(guard_linebreaks=False),dict(pair_phase_safe_breaks=False),dict(literal_prefix_policy='forbid'),dict(default_ascii_width=5),dict(default_multibyte_width=10),dict(leading_speaker_bytes=frozenset({2,254})),dict(macro_ascii_lengths={'FI':5,'FA':9,'FO':15}),dict(macro_widths={'FI':30,'FA':54,'FO':90,'I':12})]
        for change in profile_changes:
            bad=replace(p,**change)
            reject(ident+':profile:'+next(iter(change)),repr(p),repr(bad),lambda unused,bad=bad:encode_relocatable_dialogue(raw,text,bad),'font/window/page/selector/guard/macro profile changed')
        reject(ident+':wrong-file',doc['file_path'],'/data/SC0.DK4',lambda value:profile_for(arm,bank[row['block']],ident,value,kind),'Exact file-qualified')
        block=bank[row['block']]
        reject(ident+':wrong-block',block,block+b'\0',lambda value:profile_for(arm,value,ident,doc['file_path'],kind),'Exact file-qualified')
        reject(ident+':wrong-consumer',kind,'progressive' if kind=='FE-paper' else 'FE-paper',lambda value:profile_for(arm,block,ident,doc['file_path'],value),'consumer required')
    semantics=[
        (47,6,'unsupported-unfairness','Argh!',"That's not fair!"),
        (47,10,'invented-romance','Oh well.',"Let's get married."),
        (47,13,'invented-conquest','the best in the world','ruler of the conquered world'),
        (47,13,'present-supremacy',"I won't settle for less!",'You already rule the world!'),
        (48,6,'lost-qualification','appears to have found','definitely owns'),
        (48,6,'wrong-discoverer','Lil Argot','Hodram'),
        (48,6,'wrong-established-artifact',"Ullr's Bow","Ullr's Shield"),
        (48,11,'lost-runtime-name','{MACRO:FI}','Hodram'),
        (48,11,'invented-rank','Too bad,','Too bad, Admiral'),
        (48,14,'reversed-wait-direction','Then wait in Amsterdam.',"I'm already waiting in Amsterdam."),
        (48,14,'wrong-destination','Amsterdam','London'),
        (48,14,'invented-handover','Want it?',"It's yours now!"),
    ]
    for block,record,label,a,b in semantics:
        index=next(i for i,r in enumerate(doc['records']) if (r['block'],r['source_record_index'])==(block,record));changed=deepcopy(doc);original=changed['records'][index]['english'];assert a in original;changed['records'][index]['english']=original.replace(a,b)
        reject('source-fact:'+label,doc,changed,validate_approved_batch,'required')
    for field,value in [('translation_policy','natural-dialogue-v1'),('target_locale','en-GB'),('route',2),('file_path','/data/SC2.DK4'),('blocks',[48,47]),('encoder','dialogue-fixed-v1')]:
        changed=deepcopy(doc);changed[field]=value;reject('batch:'+field,doc,changed,validate_approved_batch,'batch metadata required')
    for field,value in [('current_name','Lil Admiral'),('actor_ID',1),('source_given','女性'),('localization_reason','')]:
        changed=deepcopy(names);changed['records'][0][field]=value;reject('scoped-name:'+field,names,changed,validate_scoped_names,'exact source-qualified')
    for gate in ['source','context','localization','naturalness','formatting']:
        changed=deepcopy(names);changed['records'][0]['review'][gate]=False;reject('scoped-name:gate:'+gate,names,changed,validate_scoped_names,'exact source-qualified')
    for field,value in [('FE_is_not_actor254_orpersonal_name',False),('system_FE_record_IDs',[])]:
        changed=deepcopy(names);changed[field]=value;reject('system-name:'+field,names,changed,validate_scoped_names,'exact source-qualified')
    class DifferentRuntime:
        def __init__(self,path):self.path=path
        def read_file(self,path):
            value=image.read_file(path);return value+b'X' if path==self.path else value
    for path in frozen['runtime_component_hashes']:
        reject('runtime:'+path,False,True,lambda unused,path=path:validate_runtime(DifferentRuntime(path)),'runtime component required')
    assert len(positives)==6 and all(n['actual_changed_input'] and n['rejected'] for n in negatives)
    after={str(p):sha(p.read_bytes()) for p in protected};assert before==after
    ROOT.mkdir(parents=True);save(ROOT/'six_positives_source_facts_FE_FI_five_gates_profiles_andscope_rejections.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),positive_count=len(positives),positives=positives,negative_count=len(negatives),negatives=negatives,
        all_changed_inputs_verified_distinct=True,all_rejections_match_expected_guard=True,all_protected_files_ROMs_registry_ledger_pins_anddependencies_byte_exact=True,protected_before=before,protected_after=after,
        no_new_native_oractual_scene_replays=True,independent_actual_atomic_semantic_challenges_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Policy6 positivecompilations/QA and',len(negatives),'meaningful expectedguardrejections pass;protectedfiles exact.No ROM orcredit change.')
