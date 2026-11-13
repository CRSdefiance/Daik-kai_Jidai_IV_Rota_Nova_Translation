"""Challenge all36 exact reviewed records; count only expected guard rejections."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.papal_trade_profile_v1 import contract,profile_for
from dk4tool.dialogue.papal_trade_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B234_policy_validation_v7591 import SEMANTIC
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_policy_validation_v7639')
if __name__=='__main__':
    assert not ROOT.exists();c=contract();first=read(MANUSCRIPTS[0]);image=NdsImage.open(first['current_ROM']);arm=image.read_file('/__arm9__.bin')
    paths=[*MANUSCRIPTS.values(),Path(first['current_ROM']),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/papal_trade_native_contract_v1.json'),Path('dk4tool/dialogue/papal_trade_profile_v1.py'),Path('dk4tool/dialogue/papal_trade_layout_v1.py')]
    before={str(p):sha(p.read_bytes()) for p in paths};positive=[];negative=[];blocks={}
    for route,path in MANUSCRIPTS.items():
        d=read(path);block=IlnkContainer.parse(image.read_file(d['file_path'])).blocks[d['records'][0]['block']];blocks[route]=block
        for r in d['records']:
            p=profile_for(arm,block,r['id'],d['file_path']);raw=bytes.fromhex(r['source_hex']);v=encode_relocatable_dialogue(raw,r['english'],p);q=audit_relocatable_dialogue_record(raw,r['english'],p);binding=c['record_bindings'][r['id']]
            assert v.encoded.hex()==binding['compiled_hex'] and q['base_QA_issues']==binding['base_QA_issues'] and q['native_page_count']==1
            assert not any(i['severity'] in ['error','warning'] for i in q['issues']) and q['all_original_base_QA_issues_preserved']
            positive.append(dict(route=route,file_path=d['file_path'],id=r['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(route,label,fn,message):
        try:fn()
        except ValueError as e:
            assert message in str(e),(label,str(e))
            negative.append(dict(route=route,case=label,rejected=True,error=str(e),expected_guard=message))
        else:raise AssertionError('Unsafe input accepted:'+label)
    semantic=[(label,index,'fell away' if label=='decline-as-total-extinction' else 'Divine aid...' if label=='reflection-as-reward' else old,new) for label,index,old,new in SEMANTIC]
    for route,path in MANUSCRIPTS.items():
        d=read(path);block=blocks[route];rows={r['source_record_index']:r for r in d['records']}
        for r in d['records']:
            raw=bytes.fromhex(r['source_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);p=profile_for(arm,block,r['id'],d['file_path']);assert bad!=raw
            reject(route,'changed-complete-source-'+r['id'],lambda r=r,bad=bad,p=p:encode_relocatable_dialogue(bad,r['english'],p),'complete source and reviewed logical paragraph required')
            reject(route,'changed-prose-'+r['id'],lambda r=r,raw=raw,p=p:encode_relocatable_dialogue(raw,r['english']+'!',p),'complete source and reviewed logical paragraph required')
        r=rows[12];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'],d['file_path'])
        geometry=[('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),('row-pitch',replace(p,line_height_px=12)),('invented-page-capacity',replace(p,max_lines=8)),('lost-original-capacity',replace(p,max_lines=2)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),('literal-policy',replace(p,literal_prefix_policy='forbid')),('macro-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':99}))]
        for label,bad in geometry:
            assert bad!=p;reject(route,label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad),'font/window/page/selector/guard/macro profile changed')
        for label,text in [('manual-wrap',r['english']+'{LB}'),('positioned-wrap',r['english']+'{LB@3}'),('manual-padding',r['english']+'{PAD}'),('alignment',r['english']+'{ALIGN@3}'),('invented-FI',r['english']+'{MACRO:FI}'),('authored-newline',r['english']+'\n'),('leading-space',r['english'].replace('}','} ',1)),('wrong-speaker',r['english'].replace('{SPEAKER:68}','{SPEAKER:02}'))]:
            assert text!=r['english'];reject(route,label,lambda text=text:encode_relocatable_dialogue(raw,text,p),'complete source and reviewed logical paragraph required')
        for label,index,old,new in semantic:
            row=rows[index];assert old in row['english'];bad=row['english'].replace(old,new);assert bad!=row['english']
            reject(route,label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profile_for(arm,block,row['id'],d['file_path'])),'complete source and reviewed logical paragraph required')
        reject(route,'changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id'],d['file_path']),'file-qualified source/current block and2b6 runtime required')
        reject(route,'changed-complete-block-tail',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id'],d['file_path']),'file-qualified source/current block and2b6 runtime required')
        reject(route,'unreviewed-record-ID',lambda:profile_for(arm,block,'DK4_MES_B999_R9999',d['file_path']),'Unreviewed papal-trade paragraph')
        other=read(MANUSCRIPTS[1-route])
        reject(route,'wrong-file-qualification',lambda:profile_for(arm,block,r['id'],other['file_path']),'file-qualified source/current block and2b6 runtime required')
        assert blocks[1-route]!=block
        reject(route,'other-route-current-block',lambda:profile_for(arm,blocks[1-route],r['id'],d['file_path']),'file-qualified source/current block and2b6 runtime required')
    assert len(positive)==36 and len(negative)==174 and len({(r['route'],r['case']) for r in negative})==174
    assert sum(len(r['qa']['exact_reviewed_base_warnings']) for r in positive)==2 and sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==16
    assert before=={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(ROOT/'36_positives174_expected_actual_changing_rejections_before_mutation.json',dict(positive_cases=positive,positive_count=36,negative_cases=negative,negative_count=174,two_exact_R33_warnings16_infos_preserved=True,all_rejections_expected_ValueError_guards_not_arbitrary_exceptions=True,no_unchanged_mutation_schema_failure_orstartup_failure_counted_asnegative=True,all_input_ROM_registry_ledger_hashes_unchanged=True,frozen_paragraph_guards_not_semantic_oracle_for_unseen_prose=True,stored_actual_reference_andrelease_pending=True,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('36 positive paragraphs /174 actual-changing expected guard rejections; all ROM/registry/ledger inputs unchanged. Two exact R33 warnings and16 infos preserved;stored/actual/release pending.')
