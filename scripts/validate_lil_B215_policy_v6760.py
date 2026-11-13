"""Verify every paragraph plus distinct corruption risks before any ROM mutation."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B215_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B215_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B215_policy_validation_v6760');DOC=Path('translations/lil_B215_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[215];positive=[];negative=[]
    for r in doc['records']:
        b=c['record_bindings'][r['id']];p=profile_for(arm,block,r['id']);value=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],p);qa=audit_relocatable_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],p);assert value.encoded.hex()==b['compiled_hex'] and qa['native_page_count']==1 and [i for i in qa['issues'] if i['severity']=='warning']==b['approved_warning_issues'] and qa['all_base_diagnostics_retained'];positive.append(dict(id=r['id'],compiled_hex=value.encoded.hex(),qa=qa))
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Unsafe input accepted:'+label)
    r=next(r for r in doc['records'] if r['source_record_index']==48);raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'])
    for label,bad in [('FA-width',replace(p,macro_widths={**p.macro_widths,'FA':36})),('FA-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FA':6})),('viewport',replace(p,window_width_px=228)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208}))]:reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad))
    for label,text in [('hardcoded-FA',r['english'].replace('{MACRO:FA}','Argot')),('invented-company',r['english'].replace('{MACRO:FA}','{MACRO:FO}')),('lost-qualification',r['english'].replace('might be able to','can')),('manual-wrap',r['english']+'{LB}'),('wrong-speaker',r['english'].replace('{SPEAKER:78}','{SPEAKER:02}'))]:assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    reject('changed-complete-source',lambda:encode_relocatable_dialogue(raw[:-1]+bytes([raw[-1]^1]),r['english'],p));reject('changed-block-tail',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id']));reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id']))
    assert len(positive)==15 and len(negative)==14 and sum(len(p['qa']['approved_warning_issues']) for p in positive)==3;ROOT.mkdir(parents=True);save(ROOT/'fifteen_positives14_distinct_rejections_exact_warning_issues_retained.json',dict(positive_cases=positive,negative_cases=negative,all15_native_profiles_pass=True,all14_distinct_safety_rejections_before_mutation=True,all_base_warning_info_diagnostics_retained=True,three_specific_warning_reasons_no_global_waiver=True,new_credit=0,new_ROMs=0,full_goal_complete=False));print('15 positives/14 distinct safety rejections; exact3 warnings remain visible with individual reasons. No ROM mutation or credit.')
