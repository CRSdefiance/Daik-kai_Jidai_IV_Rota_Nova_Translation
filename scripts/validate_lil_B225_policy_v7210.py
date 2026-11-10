"""Challenge the exact reviewed B225 source/prose/native contract without ROM mutation."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B225_profile_v2 import contract,profile_for
from dk4tool.dialogue.lil_B225_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_policy_validation_v7210');DOC=Path('translations/lil_B225_editorial_manuscript_v2b.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[225]
    deps=[DOC,Path('translations/lil_B225_native_contract_v2.json'),Path('dk4tool/dialogue/lil_B225_profile_v2.py'),Path('dk4tool/dialogue/lil_B225_layout_v2.py'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path(doc['current_ROM'])];before={str(p):sha(p.read_bytes()) for p in deps};positive=[];negative=[];rows={r['source_record_index']:r for r in doc['records']}
    for r in doc['records']:
        p=profile_for(arm,block,r['id']);raw=bytes.fromhex(r['source_hex']);v=encode_relocatable_dialogue(raw,r['english'],p);q=audit_relocatable_dialogue_record(raw,r['english'],p)
        assert v.encoded.hex()==c['record_bindings'][r['id']]['compiled_hex'] and q['native_page_count']==r['native_page_count']==(2 if r['source_record_index']==26 else 1) and q['base_QA_issues']==r['all_original_base_QA_issues'] and q['all_original_base_QA_issues_preserved'] and not any(i['severity'] in ['error','warning'] for i in q['issues'])
        positive.append(dict(id=r['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Unsafe input accepted:'+label)
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);p=profile_for(arm,block,r['id']);assert bad!=raw
        reject('changed-complete-source-'+r['id'],lambda r=r,bad=bad,p=p:encode_relocatable_dialogue(bad,r['english'],p))
        reject('changed-prose-'+r['id'],lambda r=r,raw=raw,p=p:encode_relocatable_dialogue(raw,r['english']+'!',p))
    r=rows[26];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'])
    for label,bad in [('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),('row-pitch',replace(p,line_height_px=12)),('invented-third-page-capacity',replace(p,max_lines=12)),('lost-required-second-page-capacity',replace(p,max_lines=4)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208}))]:
        assert bad!=p;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad))
    for label,text in [('manual-wrap',r['english']+'{LB}'),('positioned-wrap',r['english']+'{LB@3}'),('manual-padding',r['english']+'{PAD}'),('alignment',r['english']+'{ALIGN@3}'),('invented-FI',r['english']+'{MACRO:FI}'),('authored-newline',r['english']+'\n'),('leading-space',r['english'].replace('}', '} ',1)),('wrong-speaker',r['english'].replace('{SPEAKER:10}','{SPEAKER:02}'))]:
        assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    semantic=[('lost-theatrical-great',5,'The great Charles Martel','Charles Martel'),('invented-historical-rank',5,'The great Charles Martel','Emperor Charles Martel'),('lost-explicit-surrender',9,'I give up!','Mercy!'),('invented-parent',9,'I give up!','Daddy, help!'),('unsupported-modern-date',23,'over 800 years ago','in 732'),('invented-geography',26,'Iberian Peninsula','French coast'),('lost-invasion',26,'had invaded','had left'),('reversed-advance',26,'advancing north','retreating south'),('invented-crusade',26,'splendid victory','holy crusade'),('lost-military-viewpoint-objection',29,"That's a soldier's way of thinking.",''),('counterfactual-as-authorial-fact',36,'Had he lost,','Historical fact:'),('invented-individual-conversions',36,'all of Europe would have become Islamic','every European would have converted to Islam'),('lost-qualified-concession',40,"I guess it's",'It is certainly'),('invented-new-conquests',44,'achievements','conquests'),('guaranteed-religious-fame',48,'will remember you','will worship you')]
    for label,index,old,new in semantic:
        row=rows[index];assert old in row['english'];bad=row['english'].replace(old,new);assert bad!=row['english'];reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profile_for(arm,block,row['id'])))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id']));reject('changed-complete-source-tail',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id']));reject('unreviewed-record-ID',lambda:profile_for(arm,block,'DK4_MES_B225_R9999'))
    assert len(positive)==13 and len(negative)==len({r['case'] for r in negative})==60 and sum(r['qa']['native_page_count'] for r in positive)==14
    assert sum(len(r['qa']['exact_reviewed_base_warnings']) for r in positive)==0 and sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==2
    assert before=={str(p):sha(p.read_bytes()) for p in deps};ROOT.mkdir(parents=True)
    save(ROOT/'thirteen_positives60_rejections_two_row_reasons_zero_waivers.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_paragraph_cases=positive,positive_paragraph_count=13,negative_cases=negative,negative_count=60,complete_native_pages=14,row_count_reasons={r['id']:r['row_count_reason'] for r in doc['records'] if r['row_count_reason']},all_base_QA_diagnostics_preserved_zero_warning_waivers=True,source_R26_required_second_original_page_with_guard_not_taller_geometry=True,source_Sailor_cast_not_relabelled_from_children_phrase=True,all_rejections_before_ROM_archive_registry_or_ledger_mutation=True,all_input_policy_registry_ledger_andcurrent_ROM_hashes_unchanged=True,exact_reviewed_paragraph_guards_not_automatic_semantic_approval_of_unseen_text=True,stored_English_actual_reference_andrelease_pending=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('B22513 positives/60 actual-changing rejects,14 original pages,two row reasons,zero warning waivers. All inputs/ROM/ledger unchanged;stored/actual/release pending;zero credit.')
