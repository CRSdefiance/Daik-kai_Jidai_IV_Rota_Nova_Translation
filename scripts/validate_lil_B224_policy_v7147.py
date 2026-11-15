"""Challenge source, prose, geometry and explicit semantic risks without ROM mutation."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B224_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B224_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_policy_validation_v7147');DOC=Path('translations/lil_B224_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[224]
    deps=[DOC,Path('translations/lil_B224_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B224_profile_v1.py'),Path('dk4tool/dialogue/lil_B224_layout_v1.py'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path(doc['current_ROM'])];before={str(p):sha(p.read_bytes()) for p in deps};positive=[];negative=[];rows={r['source_record_index']:r for r in doc['records']}
    for r in doc['records']:
        p=profile_for(arm,block,r['id']);raw=bytes.fromhex(r['source_hex']);v=encode_relocatable_dialogue(raw,r['english'],p);q=audit_relocatable_dialogue_record(raw,r['english'],p)
        assert v.encoded.hex()==c['record_bindings'][r['id']]['compiled_hex'] and q['native_page_count']==1 and q['base_QA_issues']==r['all_original_base_QA_issues'] and q['all_original_base_QA_issues_preserved'] and not any(i['severity'] in ['error','warning'] for i in q['issues'])
        positive.append(dict(id=r['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Unsafe input accepted:'+label)
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);p=profile_for(arm,block,r['id'])
        reject('changed-complete-source-'+r['id'],lambda r=r,bad=bad,p=p:encode_relocatable_dialogue(bad,r['english'],p))
        reject('changed-prose-'+r['id'],lambda r=r,raw=raw,p=p:encode_relocatable_dialogue(raw,r['english']+'!',p))
    r=rows[26];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'])
    for label,bad in [('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),('row-pitch',replace(p,line_height_px=12)),('page-limit',replace(p,max_lines=8)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208}))]:reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad))
    for label,text in [('manual-wrap',r['english']+'{LB}'),('positioned-wrap',r['english']+'{LB@3}'),('manual-padding',r['english']+'{PAD}'),('alignment',r['english']+'{ALIGN@3}'),('invented-FI',r['english']+'{MACRO:FI}'),('authored-newline',r['english']+'\n'),('leading-space',r['english'].replace('}', '} ',1)),('wrong-speaker',r['english'].replace('{SPEAKER:1A}','{SPEAKER:C5}'))]:
        assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    for label,index,old,new in [('hearsay-as-certainty',26,"They say it's","It is certainly"),('invented-sea',26,'Tasman Sea','Aegean Sea'),('wrong-item',26,'Medusa Shield','Medusa Sword'),('invented-religious-garment',32,'uncovering your hair','removing your hijab'),('invented-magic-touch',32,'those beautiful eyes alone','your magic touch'),('hypothesis-as-established-event',39,'If you turned me','When you turned me'),('invented-husband',43,'take care of you','take care of my husband'),('lost-little-qualification',54,' a little',''),('changed-monster',29,'snake-haired','red-haired'),('lost-wondering-question',18,'feels like?','feels like.'),('lost-as-ever',5,'as mysterious as ever','mysterious'),('invented-rank',8,'Julian','Captain Julian'),('changed-retained-ellipsis',11,'…','...'),('invented-heart-symbol',54,'a little.','a little. ♡')]:
        row=rows[index];assert old in row['english'];bad=row['english'].replace(old,new);assert bad!=row['english'];reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profile_for(arm,block,row['id'])))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id']));reject('changed-source-block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id']));reject('unreviewed-record-ID',lambda:profile_for(arm,block,'DK4_MES_B224_R9999'))
    assert len(positive)==15 and len(negative)==len({r['case'] for r in negative})==62
    assert sum(len(r['qa']['exact_reviewed_base_warnings']) for r in positive)==3 and sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==5
    silence=next(r for r in positive if r['id']=='DK4_MES_B224_R0011');assert silence['compiled_hex']=='1a8163' and silence['qa']['line_widths_px']==[12]
    assert before=={str(p):sha(p.read_bytes()) for p in deps};ROOT.mkdir(parents=True)
    save(ROOT/'fifteen_positives62_rejections_five_row_reasons_three_exact_waivers.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_paragraph_cases=positive,positive_paragraph_count=15,negative_cases=negative,negative_count=62,complete_native_pages=15,row_count_reasons={r['id']:r['row_count_reason'] for r in doc['records'] if r['row_count_reason']},three_exact_record_local_weak_waivers_all_base_diagnostics_preserved=True,original_R11_ellipsis_compiled_hex='1a8163',original_R11_native_width_px=12,all_rejections_before_ROM_archive_registry_or_ledger_mutation=True,all_input_policy_registry_ledger_and_current_ROM_hashes_unchanged=True,exact_reviewed_paragraph_guards_not_automatic_semantic_approval_of_unseen_text=True,stored_English_actual_reference_and_release_pending=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('15 positive paragraphs/62 actual-changing rejection risks;3 exact warnings and5 row reasons retained. Original ellipsis remains1a8163/12px. No ROM orcredit change.')
