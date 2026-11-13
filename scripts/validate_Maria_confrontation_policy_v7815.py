"""Validate67 exact plans andactual-changing source/prose/geometry/macro/identity rejections."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.maria_B36_profile_v1 import contract,profile_for
from dk4tool.dialogue.maria_B36_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.freeze_Maria_confrontation_policy_v7814 import MANUSCRIPT,CONTRACT,PROFILE,FORMATTER,PLANNER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_policy_validation_v7815')
SEMANTIC=[('readiness-to-completed-travel', 36, 5, 'ready to sail', 'already back from our voyage'), ('recognition-wrong-person', 36, 9, 'Lil Argot', 'Maria Li'), ('invented-rank', 36, 16, 'Admiral', 'Queen'), ('introduction-invented-title', 36, 23, 'My name is', 'My royal title is'), ('direct-arrival-as-invasion', 36, 27, 'came here in person', 'invaded us with your fleet'), ('fear-as-fulfilled-event', 36, 31, 'came to kill me?!', 'already killed me!'), ('tentative-inference-erased', 36, 34, 'It seems', 'I know for certain'), ('metaphor-as-literal-poison', 36, 34, 'really misled you', 'poisoned your food'), ('purpose-inverted', 36, 34, 'tell you the truth', 'attack your fleet'), ('regional-confusion', 36, 37, 'Southeast Asia', 'East Asia'), ('people-as-ships', 36, 37, 'the people', 'the ships'), ('attempt-as-completed-rescue', 36, 37, 'trying to save', 'finished saving'), ('counteraccusation-wider-rule', 36, 41, "China's underworld", "all of China's government"), ('intended-plan-as-past-event', 36, 45, 'He plans to', 'He already managed to'), ('proof-demand-as-proof-owned', 36, 49, 'Do you have any proof', 'I have confirmed proof'), ('proof-challenge-invented-kinship', 36, 49, 'the bad guy', 'my father'), ('life-danger-erased', 36, 52, 'Your life is at stake', 'Your profits are guaranteed'), ('invented-deadline', 36, 52, "It's not too late", 'The deadline is tomorrow'), ('refusal-as-acceptance', 36, 56, "You can't just spring that on me and expect me to believe it", 'I believe everything you said'), ('girl-as-daughter', 36, 60, 'Stubborn girl', 'My stubborn daughter')]
if __name__=='__main__':
    assert not ROOT.exists();c=contract();doc=read(MANUSCRIPT)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    paths=[MANUSCRIPT,Path(doc['current_ROM']),CONTRACT,PROFILE,FORMATTER,PLANNER,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json')]
    before={str(p):sha(p.read_bytes()) for p in paths};positive=[];negative=[]
    records={(r['block'],r['source_record_index']):r for r in doc['records']}
    profiles={}
    for row in doc['records']:
        b=c['record_bindings'][row['id']];p=profile_for(arm,blocks[row['block']],row['id'],row['file_path']);profiles[row['id']]=p
        raw=bytes.fromhex(row['source_hex']);english=b['planning_record']['english']
        v=encode_relocatable_dialogue(raw,english,p);q=audit_relocatable_dialogue_record(raw,english,p)
        assert v.encoded.hex()==b['compiled_hex'] and q['base_QA_issues']==b['base_QA_issues'] and q['native_page_count']==1
        assert not any(i['severity'] in ['error','warning'] for i in q['issues']) and q['all_original_base_QA_issues_preserved']
        positive.append(dict(file_path=row['file_path'],block=row['block'],id=row['id'],compiled_hex=v.encoded.hex(),qa=q))
    def reject(label,fn,message):
        try:fn()
        except ValueError as error:
            assert message in str(error),(label,str(error));negative.append(dict(case=label,rejected=True,error=str(error),expected_guard=message))
        else:raise AssertionError('Unsafe input accepted:'+label)
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);bad=raw[:-1]+bytes([raw[-1]^1]);p=profiles[row['id']]
        english=c['record_bindings'][row['id']]['planning_record']['english'];assert bad!=raw
        reject('changed-source-'+row['id'],lambda bad=bad,p=p,english=english:encode_relocatable_dialogue(bad,english,p),'complete source and reviewed logical paragraph required')
        reject('changed-prose-'+row['id'],lambda raw=raw,p=p,english=english:encode_relocatable_dialogue(raw,english+'!',p),'complete source and reviewed logical paragraph required')
    row=records[36,23];raw=bytes.fromhex(row['source_hex']);p=profiles[row['id']];english=c['record_bindings'][row['id']]['planning_record']['english']
    geometry=[('ASCII-width',replace(p,default_ascii_width=5)),('viewport',replace(p,window_width_px=228)),
        ('row-pitch',replace(p,line_height_px=12)),('page-capacity',replace(p,max_lines=8)),('lost-capacity',replace(p,max_lines=2)),
        ('pair-phase',replace(p,pair_phase_safe_breaks=False)),('guard',replace(p,guard_linebreaks=False)),
        ('selector-scope',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),('literal-policy',replace(p,literal_prefix_policy='forbid')),
        ('FA-stale-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FA':3})),
        ('FA-stale-width',replace(p,macro_widths={**p.macro_widths,'FA':18})),('FO-invented-width',replace(p,macro_widths={**p.macro_widths,'FO':60}))]
    for label,bad in geometry:
        assert bad!=p;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,english,bad),'font/window/page/selector/guard/macro profile changed')
    texts=[('manual-wrap',english+'{LB}'),('positioned-wrap',english+'{LB@3}'),('padding',english+'{PAD}'),
        ('alignment',english+'{ALIGN@3}'),('invented-FI',english+'{MACRO:FI}'),('newline',english+'\n'),
        ('leading-space',english.replace('}','} ',1)),('wrong-speaker',english.replace('{SPEAKER:03}','{SPEAKER:02}'))]
    for label,text in texts:
        assert text!=english;reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p),'complete source and reviewed logical paragraph required')
    for label,block,index,old,new in SEMANTIC:
        row=records[block,index];text=c['record_bindings'][row['id']]['planning_record']['english'];assert old in text
        bad=text.replace(old,new);assert bad!=text
        reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profiles[row['id']]),'complete source and reviewed logical paragraph required')
    macro_cases=0
    for row in doc['records']:
        text=c['record_bindings'][row['id']]['planning_record']['english']
        for token in ['FI','FA','FO']:
            marker='{MACRO:'+token+'}'
            if marker not in text:continue
            bad=text.replace(marker,'a stranger');assert bad!=text;macro_cases+=1
            reject('erased-'+token+'-'+row['id'],lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profiles[row['id']]),'complete source and reviewed logical paragraph required')
    for number in [36]:
        row=next(r for r in doc['records'] if r['block']==number);block=blocks[number]
        reject('changed-tail-B'+str(number),lambda block=block,row=row:profile_for(arm,block[:-1]+bytes([block[-1]^1]),row['id'],row['file_path']),'file-qualified source/current block and2b6 runtime required')
        assert block[2]==1;normalized=block[:2]+b'\0'+block[3:]
        reject('normalized-header-B'+str(number),lambda normalized=normalized,row=row:profile_for(arm,normalized,row['id'],row['file_path']),'file-qualified source/current block and2b6 runtime required')
        other=blocks[next(n for n in [34,108,35] if n!=number)]
        reject('wrong-block-B'+str(number),lambda other=other,row=row:profile_for(arm,other,row['id'],row['file_path']),'file-qualified source/current block and2b6 runtime required')
    row=doc['records'][0];block=blocks[row['block']]
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,row['id'],row['file_path']),'file-qualified source/current block and2b6 runtime required')
    reject('wrong-file',lambda:profile_for(arm,block,row['id'],'/data/SC2.DK4'),'file-qualified source/current block and2b6 runtime required')
    reject('unreviewed-ID',lambda:profile_for(arm,block,'DK4_MES_B999_R9999',row['file_path']),'Unreviewed Maria-B36 paragraph')
    assert len(positive)==16 and macro_cases==3 and len(negative)==32+len(geometry)+len(texts)+len(SEMANTIC)+macro_cases+6
    assert len({r['case'] for r in negative})==len(negative)
    assert sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==9
    assert before=={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(ROOT/'16_positives81_actual_changing_guard_rejections.json',dict(
        positive_cases=positive,positive_count=16,negative_cases=negative,negative_count=len(negative),macro_erasure_cases=macro_cases,
        nine_row_infos_no_warnings_orwaivers=True,all_expected_ValueError_guards_not_arbitrary_failures=True,
        all_inputs_ROM_registry_andledger_hashes_unchanged=True,source_B36_header_normalization_rejected=True,
        frozen_exact_paragraph_checks_not_semantic_oracle_for_unseen_prose=True,
        production_reference_seal_registered_release_andown_startup_pending=True,
        evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('16policy positives /',len(negative),'actual-changing guard rejections;3macro erasures;9row infos/no warnings;all shared inputs unchanged.')
