"""Exercise complete B222 policies and distinct unsafe input changes without ROM mutation."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B222_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B222_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_policy_validation_v7051');DOC=Path('translations/lil_B222_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[222]
    deps=[DOC,Path('translations/lil_B222_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B222_profile_v1.py'),Path('dk4tool/dialogue/lil_B222_layout_v1.py'),Path('translations/editorial_review_current_v1.json')];before={str(p):sha(p.read_bytes()) for p in deps};positive=[];negative=[]
    for r in doc['records']:
        p=profile_for(arm,block,r['id']);raw=bytes.fromhex(r['source_hex']);v=encode_relocatable_dialogue(raw,r['english'],p);q=audit_relocatable_dialogue_record(raw,r['english'],p)
        assert v.encoded.hex()==c['record_bindings'][r['id']]['compiled_hex'] and q['native_page_count']==1 and q['base_QA_issues']==r['all_original_base_QA_issues'] and not any(i['severity'] in ['error','warning'] for i in q['issues'])
        positive.append(dict(id=r['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Unsafe input accepted:'+label)
    rows={r['source_record_index']:r for r in doc['records']};r=rows[37];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'])
    for label,bad in [('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),('row-pitch',replace(p,line_height_px=12)),('page-limit',replace(p,max_lines=8)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208}))]:reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad))
    for label,text in [('invented-FI',r['english']+' {MACRO:FI}'),('manual-wrap',r['english']+'{LB}'),('manual-padding',r['english']+'{PAD}'),('wrong-speaker',r['english'].replace('{SPEAKER:10}','{SPEAKER:02}')),('authored-newline',r['english']+'\n'),('cut-armor',r['english'].replace(', gleaming armor and all','')),('one-enemy-instead-of-two',r['english'].replace('under each arm','under one arm')),('invented-named-strait',r['english'].replace('the strait','the Kanmon Strait')),('hearsay-as-certainty',r['english'].replace('They say he','He certainly')),('changed-local-waiver-wording',r['english']+' ' )]:
        assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    for label,index,old,new in [('six-not-seven-ships',33,'seven ships','six ships'),('attempt-as-success',33,'trying to reach','reaching'),('recognition-as-acquaintance',17,"someone I'd know","a friend of mine"),('private-thought-as-spoken',50,'(He looks scary,', 'He looks scary,'),('rumor-as-guaranteed-find',54,'Hmm.','We will find it.'),('invented-rank',20,'military commander','emperor')]:
        other=rows[index];assert old in other['english'];reject(label,lambda other=other,old=old,new=new:encode_relocatable_dialogue(bytes.fromhex(other['source_hex']),other['english'].replace(old,new),profile_for(arm,block,other['id'])))
    reject('changed-complete-source',lambda:encode_relocatable_dialogue(raw[:-1]+bytes([raw[-1]^1]),r['english'],p));reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id']));reject('changed-source-block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id']))
    assert len(positive)==16 and len(negative)==26 and sum(len(v['qa']['exact_reviewed_base_warnings']) for v in positive)==2 and sum(i['code']=='line-break-count' for v in positive for i in v['qa']['issues'])==7
    assert before=={str(p):sha(p.read_bytes()) for p in deps};ROOT.mkdir(parents=True);save(ROOT/'sixteen_positives26_distinct_rejections_seven_row_reasons_two_exact_waivers.json',dict(positive_cases=positive,negative_cases=negative,original_base_diagnostics_retained=True,two_exact_weak_boundary_waivers_no_other_warning_accepted=True,all_rejections_before_ROM_mutation=True,no_input_policy_or_ledger_mutation=True,evidence=before,new_credit=0,new_ROMs=0,full_goal_complete=False));print('16 positive paragraphs/26 distinct rejection risks. All original diagnostics retained;2 exact waivers,7 info reasons. No ROM or credit.')
