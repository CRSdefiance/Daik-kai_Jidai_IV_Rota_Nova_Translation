"""Exercise the reviewed B221 paragraphs, typed responses and distinct fidelity/display risks."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B221_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B221_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_B221_choices_v1 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B221_policy_validation_v6993b')
DOC=Path('translations/lil_B221_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_B221_choice_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,choices=map(read,[DOC,CHOICES]);c=contract();image=NdsImage.open(doc['current_ROM'])
    arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[221]
    positives=[];negatives=[]
    for row in doc['records']:
        binding=c['record_bindings'][row['id']];profile=profile_for(arm,block,row['id'])
        encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        assert encoded.encoded.hex()==binding['compiled_hex'] and qa['native_page_count']==binding['native_page_count']
        assert qa['native_rows_per_page']==4 and qa['no_base_QA_issue_removed']
        assert not [i for i in qa['issues'] if i['severity'] in ['error','warning']]
        positives.append(dict(id=row['id'],compiled_hex=encoded.encoded.hex(),qa=qa))
    target=compile_choices(choices['records'])
    assert target.hex()==c['choice_object_hex'] and len(target)==14
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as exc:negatives.append(dict(case=label,rejected=True,error=str(exc)))
        else:raise AssertionError('Unsafe/unreviewed B221 input accepted:'+label)
    rows={r['source_record_index']:r for r in doc['records']}
    row=rows[27];raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,block,row['id'])
    for label,bad in [
        ('ASCII-width',replace(profile,default_ascii_width=5)),
        ('viewport',replace(profile,window_width_px=228)),
        ('row-pitch',replace(profile,line_height_px=12)),
        ('ordinary-paragraph-eight-row-limit',replace(profile,max_lines=8)),
        ('pair-phase',replace(profile,pair_phase_safe_breaks=False)),
        ('guard',replace(profile,guard_linebreaks=False)),
        ('unreviewed-selector',replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{208}))]:
        reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,row['english'],bad))
    for index in [46,60]:
        long=rows[index];p=profile_for(arm,block,long['id'])
        assert p.max_lines==8 and c['record_bindings'][long['id']]['native_page_count']==2
        reject('erase-reviewed-pagination-R'+str(index),lambda long=long,p=p:encode_relocatable_dialogue(bytes.fromhex(long['source_hex']),long['english'],replace(p,max_lines=4)))
    for label,text in [
        ('invented-FI',row['english']+' {MACRO:FI}'),
        ('manual-wrap',row['english']+'{LB}'),
        ('manual-alignment',row['english']+'{ALIGN@2}'),
        ('wrong-speaker',row['english'].replace('{SPEAKER:55}','{SPEAKER:11}'))]:
        assert text!=row['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,profile))
    changes=[
        ('army-recast-as-knight-rank',27,'A chivalrous army','Chivalrous knights'),
        ('European-report-made-certain',33,'apparently','certainly'),
        ('wealth-objective-replaced',46,"this region's wealth",'military glory'),
        ('new-religious-office',49,'Our true hero','Our high priest'),
        ('peace-terms-lost',60,'peace terms','peace talks'),
        ('remembered-armor-report-made-possession',67,"I once heard that Saladin's armor had gone missing","I now own Saladin's armor")]
    for label,index,old,new in changes:
        r=rows[index];assert old in r['english'] and old!=new
        reject(label,lambda r=r,old=old,new=new:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(old,new),profile_for(arm,block,r['id'])))
    reject('changed-complete-source',lambda:encode_relocatable_dialogue(raw[:-1]+bytes([raw[-1]^1]),row['english'],profile))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,row['id']))
    reject('changed-source-block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),row['id']))
    reject('unreviewed-record-ID',lambda:profile_for(arm,block,'DK4_MES_B221_R9999'))
    reject('reversed-choice-source-order',lambda:compile_choices(list(reversed(choices['records']))))
    for label,key,value in [
        ('wrong-original-choice-index','option_index',1),
        ('wrong-choice-source','source_hex','00'),
        ('wrong-predecessor-choice','current_hex','00'),
        ('wrong-original-choice-command','command_offset',152),
        ('wrong-choice-block','block',220),
        ('choice-answer-swapped','english','No'),
        ('choice-alignment-authored','english','Yes '),
        ('choice-break-authored','english','Yes\n'),
        ('choice-identity-changed','id','DK4_CHOICE_B221_C150_O2')]:
        bad=deepcopy(choices['records']);assert bad[0][key]!=value;bad[0][key]=value
        reject(label,lambda bad=bad:compile_choices(bad))
    bad=deepcopy(choices['records']);bad[0]['current_reference']['offset']+=2
    reject('misbound-choice-current-pointer',lambda:compile_choices(bad))
    bad=deepcopy(choices['records']);bad[0]['review']['source']=False
    reject('unreviewed-choice-source',lambda:compile_choices(bad))
    bad=deepcopy(choices['records']);bad[0]['source_meaning']=''
    reject('lost-choice-source-meaning',lambda:compile_choices(bad))
    assert len(positives)==14 and len(negatives)==36
    assert sum(p['qa']['native_page_count'] for p in positives)==16
    assert sum(i['code']=='line-break-count' for p in positives for i in p['qa']['issues'])==7
    ROOT.mkdir(parents=True)
    save(ROOT/'fourteen_paragraphs_one_typed_menu36_distinct_rejections_seven_row_reasons.json',dict(
        positive_paragraphs=positives,typed_menu_object_hex=target.hex(),typed_menu_labels=['Yes','No'],negative_cases=negatives,
        all14_profiles_and_original_four_row_pages_two_scoped_continuations_pass=True,
        all_two_response_source_current_bindings_and_indices_pass=True,
        all36_distinct_safety_and_fidelity_rejections_before_ROM_mutation=True,
        all_original_QA_diagnostics_preserved_seven_info_reasons_no_warning_error=True,
        frozen_wording_rejects_changes_without_substituting_automatic_semantic_review=True,
        source_0_1_normal_value_words_and_actual_page_buttons_require_final_reference_checks=True,
        new_credit=0,new_ROMs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,CHOICES,Path('translations/lil_B221_native_contract_v1.json'),
            Path('dk4tool/dialogue/lil_B221_profile_v1.py'),Path('dk4tool/dialogue/lil_B221_layout_v1.py'),
            Path('dk4tool/dialogue/lil_B221_choices_v1.py'),Path(__file__)]}))
    print('14 paragraphs/16 native pages + one typed menu pass;36 distinct rejections,7 info reasons,zero QA warning/error. No ROM/credit.')
