"""Exercise reviewed Hodram facts, controls, exact warning allowances and native-profile limits."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_three_blocks_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue.hodram_three_blocks_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_policy_validation_v8288')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v4.json')
SEMANTIC=[
 (137,17,'invented-kinship','to all of you','to my family'),
 (137,39,'unapproved-Camille','Camille','Kamil'),
 (137,47,'invented-rank','I appreciate','As your admiral, I appreciate'),
 (137,54,'reversed-reassurance',"We won't harm",'We will attack'),
 (137,86,'wrong-recruit-object','capable people','warships'),
 (137,89,'guaranteed-recruitment','might find','will certainly find'),
 (137,89,'lost-source-cities','Lisbon and Seville','London'),
 (137,89,'lost-maritime-trade','live by sea trade','are at war'),
 (46,10,'captain-limited-wealth','richest person','richest captain'),
 (46,10,'invented-combat','contest','duel'),
 (46,19,'lost-deciphering-key','key to deciphering','whole treasure from'),
 (46,19,'changed-contest-goal','finds the treasure','wins the battle'),
 (46,23,'invented-completed-defeat',"I'm not losing","I've already lost"),
 (45,7,'invented-sister','boss','sister'),
]
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);binding=contract();validate_approved_batch(doc)
    image=NdsImage.open(doc['current_ROM']);validate_runtime(image);arm=image.read_file('/__arm9__.bin');path=doc['file_path']
    current=IlnkContainer.parse(image.read_file(path)).blocks;clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(path)).blocks
    reloc=read('work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json')
    protected={DOC,Path('translations/hodram_three_blocks_native_contract_v1.json'),Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),
        *[Path('dk4tool/dialogue')/f'hodram_three_blocks_{part}_v1.py' for part in ['profile','layout','plan']]}
    before={str(p):sha(p.read_bytes()) for p in protected};positive=[];negative=[];profiles={}
    def reject(label,fn,expected):
        try:fn()
        except ValueError as error:
            assert expected in str(error),(label,str(error));negative.append(dict(case=label,rejected=True,error=str(error),expected_guard=expected))
        else:raise AssertionError('Changed unsafe input accepted:'+label)
    bodyguard='complete source and reviewed logical paragraph required';profileguard='font/window/page/selector/guard/macro profile changed';batchguard='approved prose/source/context/waiver required'
    for idx,row in enumerate(doc['records']):
        ident=row['id'];p=profile_for(arm,current[row['block']],ident,path,'progressive');profiles[ident]=p
        assert p==profile_for(arm,clean[row['block']],ident,path,'progressive') and p.max_lines==4
        raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup'];encoded=encode_relocatable_dialogue(raw,text,p);qa=audit_relocatable_dialogue_record(raw,text,p)
        assert encoded.encoded.hex()==row['compiled_hex'] and encoded.encoded[0]==row['source_selector'] and b'\0' not in encoded.encoded[1:]
        assert qa['issues']==binding['record_bindings'][ident]['base_QA_issues'] and qa['native_page_count']==1
        positive.append(dict(id=ident,compiled_hex=encoded.encoded.hex(),qa=qa,clean_andcurrent_profiles_equal=True))
        bad=raw[:-1]+bytes([raw[-1]^1]);assert bad!=raw
        reject('changed-source-'+ident,lambda bad=bad,p=p,text=text:encode_relocatable_dialogue(bad,text,p),bodyguard)
        reject('changed-prose-'+ident,lambda raw=raw,p=p,text=text:encode_relocatable_dialogue(raw,text+'!',p),bodyguard)
        for gate in binding['review_gates']:
            changed=deepcopy(doc);changed['records'][idx]['review'][gate]=False;assert changed!=doc
            reject('missing-'+gate+'-'+ident,lambda changed=changed:validate_approved_batch(changed),'v2 requires per-record')
        for field in ['source_meaning','context','localization_note','editorial_finding','retention_reason','decision','speaker','source_complete_preamble_hex']:
            changed=deepcopy(doc);changed['records'][idx][field]=str(row[field])+' changed';assert changed!=doc
            reject('changed-'+field+'-'+ident,lambda changed=changed:validate_approved_batch(changed),batchguard)
        changed=deepcopy(doc);changed['records'][idx]['qa_waivers']=[] if row['qa_waivers'] else ['weak-line-ending'];assert changed!=doc
        reject('changed-warning-allowance-'+ident,lambda changed=changed:validate_approved_batch(changed),batchguard)
        if row['qa_waivers']:
            for field in row['qa_waiver_scope']:
                changed=deepcopy(doc);changed['records'][idx]['qa_waiver_scope'][field]='changed';assert changed!=doc
                reject('changed-warning-scope-'+field+'-'+ident,lambda changed=changed:validate_approved_batch(changed),batchguard)
            changed=deepcopy(doc);changed['records'][idx]['qa_waiver_reason']='Broad waiver.'
            reject('changed-warning-reason-'+ident,lambda changed=changed:validate_approved_batch(changed),batchguard)
    selected=[doc['records'][0],next(r for r in doc['records'] if r['english']=='…'),next(r for r in doc['records'] if r['source_selector']==113)]
    for row in selected:
        p=profiles[row['id']];raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup']
        changes=[('ASCII-width',replace(p,default_ascii_width=5)),('viewport228',replace(p,window_width_px=228)),
            ('row-pitch',replace(p,line_height_px=12)),('page-capacity8',replace(p,max_lines=8)),('page-capacity2',replace(p,max_lines=2)),
            ('pair-phase-disabled',replace(p,pair_phase_safe_breaks=False)),('guard-disabled',replace(p,guard_linebreaks=False)),
            ('balance-policy',replace(p,balanced_wrapping=not p.balanced_wrapping)),('fallback208',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),
            ('literal-policy',replace(p,literal_prefix_policy='forbid')),('FI-length7',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':7})),
            ('FA-length6',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FA':6})),('FO-length10',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),
            ('FA-width36',replace(p,macro_widths={**p.macro_widths,'FA':36})),('FO-width60',replace(p,macro_widths={**p.macro_widths,'FO':60}))]
        for label,bad in changes:
            assert bad!=p;reject(label+'-'+row['id'],lambda raw=raw,text=text,bad=bad:encode_relocatable_dialogue(raw,text,bad),profileguard)
        reject('wrong-consumer-'+row['id'],lambda row=row:profile_for(arm,current[row['block']],row['id'],path,'FE-paper'),'consumer required')
        changedtexts=[text+t for t in ['{LB}','{LB@3}','{ALIGN@3}','{PAD}','\n','\r','\0','{MACRO:FI}','{MACRO:FA}','{MACRO:FO}',' %s']]
        changedtexts += [text.replace('}','} ',1),row['english']]
        for i,bad in enumerate(changedtexts):
            assert bad!=text;reject(f'unsafe-text-{row["id"]}-{i}',lambda raw=raw,bad=bad,p=p:encode_relocatable_dialogue(raw,bad,p),bodyguard)
        reject('removed-selector-'+row['id'],lambda raw=raw,text=text,p=p:encode_relocatable_dialogue(raw[1:],text,p),bodyguard)
    for block,index,label,old,new in SEMANTIC:
        row=next(r for r in doc['records'] if r['block']==block and r['source_record_index']==index);text=row['planned_English_markup']
        assert old in text;bad=text.replace(old,new);assert bad!=text
        reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profiles[row['id']]),bodyguard)
    for row in [r for r in doc['records'] if r['english']=='…']:
        reject('invented-silence-words-'+row['id'],lambda row=row:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['planned_English_markup']+'Well?',profiles[row['id']]),bodyguard)
    changed=deepcopy(doc);changed['records'].reverse();reject('reordered-records',lambda:validate_approved_batch(changed),'Exact complete ordered')
    changed=deepcopy(doc);changed['typed_choice_records']=[dict(english='Yes')];reject('invented-menu',lambda:validate_approved_batch(changed),'typed menu')
    changed=deepcopy(doc);changed['route']=2;reject('wrong-route',lambda:validate_approved_batch(changed),'batch metadata')
    for row in [next(r for r in doc['records'] if r['block']==b) for b in [137,45,46]]:
        block=current[row['block']];badarm=arm[:-1]+bytes([arm[-1]^1]);target=Path(next(g['target_block'] for g in reloc['groups'] if g['block']==row['block'])).read_bytes()
        reject('changed-runtime-'+row['id'],lambda row=row,block=block,badarm=badarm:profile_for(badarm,block,row['id'],path),'Exact file-qualified')
        reject('wrong-file-'+row['id'],lambda row=row,block=block:profile_for(arm,block,row['id'],'/data/SC0.DK4'),'Exact file-qualified')
        reject('target-used-as-source-'+row['id'],lambda row=row,target=target:profile_for(arm,target,row['id'],path),'Exact file-qualified')
    assert {str(p):sha(p.read_bytes()) for p in protected}==before and len(positive)==28
    assert sum(i['severity']=='warning' for r in positive for i in r['qa']['issues'])==2
    assert sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==5
    ROOT.mkdir(parents=True);save(ROOT/'28_single_page_positives_changed_source_prose_gates_profiles_waivers_rejected.json',dict(
        positives=positive,negatives=negative,positive_count=28,negative_count=len(negative),all_changed_inputs_verified_distinct=True,
        all_rejections_checked_against_expected_guard=True,all_original_five_infos_two_exact_warning_exceptions_preserved=True,
        three_silences_six_static_selectors_zero_source_macros_Hodram_defaults6_9_15_preserved=True,
        protected_policy_manuscript_registry_ledger_pins_parent_unchanged=True,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),
        independent_atomic_production_registered_release_pending=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Hodram28 exact positives;',len(negative),'actual-changing expected-guard rejections;source facts/three silences/profiles/QA preserved. Atomic integration pending.')
