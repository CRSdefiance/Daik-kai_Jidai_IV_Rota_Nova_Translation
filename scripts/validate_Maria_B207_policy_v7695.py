"""Exercise all18 frozen positives andactual-changing source/text/geometry/header rejections."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.maria_B207_profile_v1 import contract,profile_for
from dk4tool.dialogue.maria_B207_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_policy_validation_v7695')
MANUSCRIPT=Path('translations/maria_B207_editorial_manuscript_v1.json')
SEMANTIC=[
('source-silence-erased',4,'………','Hello!'),('personal-alias-erased',8,'Filippo','my brother'),
('recognition-wrong-person',11,'Carlo','Manuel'),('business-as-homecoming',15,'stopped by on business','returned home forever'),
('recovery-cause-invented',18,'doing better','cured of your disease'),('tentative-as-certainty',18,"it looks like you're","I know for certain you are"),
('active-return-as-rank',22,"I'm finally back in action","I've finally been promoted to admiral"),
('aboard-as-convoy',22,"I'm aboard their ship now","I'm only sailing beside their ship now"),
('ancestor-kinship-changed',25,'great-grandfather','father'),('story-as-map',28,'story','precise treasure map'),
('territory-as-current-city',32,'Papal States','city we are visiting'),('direct-rule-erased',32,'ruled directly over','never ruled'),
('Venice-approximation-erased',32,'almost to Venice','over Venice itself'),('hearsay-as-proof',36,'They say','I guarantee'),
('trade-as-guaranteed-profit',36,'trade flourished','every trader always became rich'),('donations-as-tax',39,'donate','pay in taxes'),
('donation-kinds-erased',39,'what to donate','whether to fight'),('shared-ancestry-invented',42,'My ancestors','Our shared ancestors'),
('invented-shipping-route',42,'passing goods along','shipping goods from one lord to another'),
('decline-as-total-extinction',46,'fell away','vanished completely'),('greatgrandfather-as-stranger',50,'My great-grandfather','Some unrelated old man'),
('reported-finds-as-certainty',53,"I've heard",'I know for certain'),('occasional-as-guaranteed',53,'sometimes','always'),
('used-report-as-authenticity',56,'a pope was said to have used','we know a pope really used'),
('blessing-as-guarantee',56,'might carry a blessing','guarantees huge trade profits'),
('reflection-as-reward',59,'Divine aid...','Treasure obtained!'),('invented-rank',63,'Admiral','Your Majesty'),
('if-found-condition-erased',63,'If we found','Now that we own'),('favored-object-as-specific-title',63,'something a pope treasured',"Gregory's Crown, which we already own"),
]
if __name__=='__main__':
    assert not ROOT.exists();c=contract();doc=read(MANUSCRIPT);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks[207]
    paths=[MANUSCRIPT,Path(doc['current_ROM']),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/maria_B207_native_contract_v1.json'),Path('dk4tool/dialogue/maria_B207_profile_v1.py'),Path('dk4tool/dialogue/maria_B207_layout_v1.py')]
    before={str(p):sha(p.read_bytes()) for p in paths};positive=[];negative=[]
    for r in doc['records']:
        p=profile_for(arm,block,r['id'],doc['file_path']);raw=bytes.fromhex(r['source_hex']);v=encode_relocatable_dialogue(raw,r['english'],p);q=audit_relocatable_dialogue_record(raw,r['english'],p);binding=c['record_bindings'][r['id']]
        assert v.encoded.hex()==binding['compiled_hex'] and q['base_QA_issues']==binding['base_QA_issues'] and q['native_page_count']==1
        assert not any(i['severity'] in ['error','warning'] for i in q['issues']) and q['all_original_base_QA_issues_preserved']
        positive.append(dict(file_path=doc['file_path'],id=r['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(label,fn,message):
        try:fn()
        except ValueError as e:
            assert message in str(e),(label,str(e));negative.append(dict(case=label,rejected=True,error=str(e),expected_guard=message))
        else:raise AssertionError('Unsafe input accepted:'+label)
    rows={r['source_record_index']:r for r in doc['records']}
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);p=profile_for(arm,block,r['id'],doc['file_path']);assert bad!=raw
        reject('changed-complete-source-'+r['id'],lambda r=r,bad=bad,p=p:encode_relocatable_dialogue(bad,r['english'],p),'complete source and reviewed logical paragraph required')
        reject('changed-prose-'+r['id'],lambda r=r,raw=raw,p=p:encode_relocatable_dialogue(raw,r['english']+'!',p),'complete source and reviewed logical paragraph required')
    r=rows[11];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'],doc['file_path'])
    geometry=[('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),('row-pitch',replace(p,line_height_px=12)),('invented-page-capacity',replace(p,max_lines=8)),('lost-original-capacity',replace(p,max_lines=2)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),('literal-policy',replace(p,literal_prefix_policy='forbid')),('macro-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':99}))]
    for label,bad in geometry:
        assert bad!=p;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad),'font/window/page/selector/guard/macro profile changed')
    for label,text in [('manual-wrap',r['english']+'{LB}'),('positioned-wrap',r['english']+'{LB@3}'),('manual-padding',r['english']+'{PAD}'),('alignment',r['english']+'{ALIGN@3}'),('invented-FI',r['english']+'{MACRO:FI}'),('authored-newline',r['english']+'\n'),('leading-space',r['english'].replace('}','} ',1)),('wrong-speaker',r['english'].replace('{SPEAKER:68}','{SPEAKER:02}'))]:
        assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p),'complete source and reviewed logical paragraph required')
    for label,index,old,new in SEMANTIC:
        row=rows[index];assert old in row['english'];bad=row['english'].replace(old,new);assert bad!=row['english']
        reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profile_for(arm,block,row['id'],doc['file_path'])),'complete source and reviewed logical paragraph required')
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id'],doc['file_path']),'file-qualified source/current block and2b6 runtime required')
    reject('changed-complete-block-tail',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id'],doc['file_path']),'file-qualified source/current block and2b6 runtime required')
    assert block[2]==1;normalized=block[:2]+b'\0'+block[3:];assert normalized!=block
    reject('illegally-normalized-CS0101-header',lambda:profile_for(arm,normalized,r['id'],doc['file_path']),'file-qualified source/current block and2b6 runtime required')
    reject('unreviewed-record-ID',lambda:profile_for(arm,block,'DK4_MES_B999_R9999',doc['file_path']),'Unreviewed Maria-B207 paragraph')
    reject('wrong-file-qualification',lambda:profile_for(arm,block,r['id'],'/data/SC2.DK4'),'file-qualified source/current block and2b6 runtime required')
    other=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks[246];assert other!=block
    reject('other-route-current-block',lambda:profile_for(arm,other,r['id'],doc['file_path']),'file-qualified source/current block and2b6 runtime required')
    expected=18*2+len(geometry)+8+len(SEMANTIC)+6
    assert len(positive)==18 and len(negative)==expected==89 and len({r['case'] for r in negative})==89
    assert sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==7 and not any(r['qa']['exact_reviewed_base_warnings'] for r in positive)
    assert before=={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(ROOT/'18_positives89_expected_actual_changing_rejections_before_mutation.json',dict(positive_cases=positive,positive_count=18,negative_cases=negative,negative_count=89,seven_row_infos_no_warnings_preserved=True,all_rejections_expected_ValueError_guards_not_arbitrary_exceptions=True,no_unchanged_mutation_schema_failure_orstartup_failure_counted_asnegative=True,distinct_CS0101_normalization_rejected=True,all_input_ROM_registry_ledger_hashes_unchanged=True,frozen_paragraph_guards_not_semantic_oracle_for_unseen_prose=True,stored_actual_reference_andrelease_pending=True,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('18 positive Maria paragraphs /89 actual-changing expected guard rejections;all ROM/registry/ledger inputs unchanged.CS0101 normalization rejected;stored/actual/release pending.')
