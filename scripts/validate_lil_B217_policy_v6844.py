"""Check each complete paragraph and distinct geometry, source and wording-lock risks."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B217_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B217_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B217_policy_validation_v6844');DOC=Path('translations/lil_B217_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[217];positive=[];negative=[]
    for r in doc['records']:
        b=c['record_bindings'][r['id']];p=profile_for(arm,block,r['id']);v=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],p);q=audit_relocatable_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],p);assert v.encoded.hex()==b['compiled_hex'] and q['native_page_count']==1 and not [i for i in q['issues'] if i['severity'] in ['error','warning']] and q['no_base_QA_issue_removed'];positive.append(dict(id=r['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Unsafe or unreviewed input accepted:'+label)
    rows={r['source_record_index']:r for r in doc['records']};r=rows[8];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'])
    for label,bad in [('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),('row-pitch',replace(p,line_height_px=12)),('page-limit',replace(p,max_lines=8)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208}))]:reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad))
    for label,text in [('invented-FI',r['english']+' {MACRO:FI}'),('asserted-witch-identity',r['english'].replace('who calls herself a witch','who is a witch')),('manual-wrap',r['english']+'{LB}'),('wrong-speaker',r['english'].replace('{SPEAKER:5C}','{SPEAKER:02}'))]:assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    for label,index,old,new in [('invented-uncle',5,'Say','Uncle'),('removed-hearsay',12,'supposedly','certainly'),('universal-instead-of-personal-knowledge',16,"I've never heard of anyone finding it",'nobody has ever found it')]:
        other=rows[index];assert old in other['english'];reject(label,lambda other=other,old=old,new=new:encode_relocatable_dialogue(bytes.fromhex(other['source_hex']),other['english'].replace(old,new),profile_for(arm,block,other['id'])))
    reject('changed-complete-source',lambda:encode_relocatable_dialogue(raw[:-1]+bytes([raw[-1]^1]),r['english'],p));reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id']));reject('changed-source-block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id']));assert len(positive)==4 and len(negative)==17 and sum(i['code']=='line-break-count' for p in positive for i in p['qa']['issues'])==3;ROOT.mkdir(parents=True);save(ROOT/'four_positives17_distinct_rejections_three_row_reasons.json',dict(positive_cases=positive,negative_cases=negative,all4_native_profiles_pass=True,all17_distinct_safety_rejections_before_mutation=True,no_base_QA_issue_removed_or_warning_waiver=True,new_wording_requires_its_own_editorial_review_not_automatic_semantic_approval=True,new_credit=0,new_ROMs=0,full_goal_complete=False));print('Four positives/17 distinct rejection risks,three individual row reasons,zero warnings/errors. No ROM mutation or credit.')
