"""Replay approved plans and reject actual-changing B46 speech/menu inputs."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.rafael_B46_profile_v1 import contract, profile_for, validate_runtime, validate_approved_batch
from dk4tool.dialogue.rafael_B46_layout_v1 import encode_relocatable_dialogue, audit_relocatable_dialogue_record
from dk4tool.dialogue.rafael_B46_choices_v1 import compile_choices
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Rafael_B46_policy_validation_v7957')
DOC=Path('translations/rafael_B46_editorial_manuscript_v3.json')
SEMANTIC=[
    ('wrong-rescuer',15,'Hayreddin','Hodram'),
    ('invented-certain-attack',23,'may challenge us','will attack us'),
    ('reversed-enemy-initiative',23,'an enemy fleet may challenge us','we may challenge an enemy fleet'),
    ('invented-kinship',27,"I'd better","Grandson, I'd better"),
    ('lost-offer',27,'explain','order'),
    ('guaranteed-discovery',47,'might find','will always find'),
    ('lost-city-target',44,'city or fleet','fleet'),
    ('wrong-inspect-button',54,'Press Y','Press A'),
    ('wrong-battle-button',65,'Press L','Press R'),
    ('wrong-confirm-button',68,'press A','press Y'),
    ('wrong-search-button',72,'press R','press L'),
    ('wrong-search-land',80,'land inside','water outside'),
    ('wrong-mode-icon',65,'sword icon','magnifying glass icon'),
    ('wrong-L-order',87,'Inspect, Battle, then Search','Inspect, Search, then Battle'),
    ('wrong-R-Y-order',91,'Inspect, Search, then Battle','Inspect, Battle, then Search'),
    ('lost-decline-caution',105,"don't let your guard down","take it easy"),
    ('wrong-thanks-name',98,'Julio','Grandpa'),
    ('invented-completed-ambition',117,'(Someday, for sure...)',"(Someday, I'll rule the world.)"),
]

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(DOC);c=contract();validate_approved_batch(doc)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    source=blocks[46]
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(doc['file_path'])).blocks[46]
    target=Path('work/analysis/Rafael_B46_relocation_v7938/SC0_block46_RESEARCH_ONLY.bin').read_bytes()
    paths={DOC,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path('translations/rafael_B46_native_contract_v1.json'),
        *[Path('dk4tool/dialogue')/n for n in ['rafael_B46_profile_v1.py','rafael_B46_layout_v1.py','rafael_B46_plan_v1.py','rafael_B46_choices_v1.py']]}
    before={str(p):sha(p.read_bytes()) for p in paths}
    positive=[];negative=[];profiles={}
    validate_runtime(image)
    for row in doc['records']:
        b=c['record_bindings'][row['id']]
        consumer='FE-paper' if row['source_selector']==254 else 'progressive'
        p=profile_for(arm,source,row['id'],row['file_path'],consumer)
        assert profile_for(arm,clean,row['id'],row['file_path'],consumer)==p
        profiles[row['id']]=p;raw=bytes.fromhex(row['source_hex'])
        encoded=encode_relocatable_dialogue(raw,row['english'],p)
        qa=audit_relocatable_dialogue_record(raw,row['english'],p)
        assert encoded.encoded.hex()==row['compiled_hex']==b['compiled_hex']
        assert encoded.encoded[0]==row['source_selector'] and b'\0' not in encoded.encoded[1:]
        assert qa['base_QA_issues']==b['base_QA_issues'] and qa['native_page_count']==1
        assert qa['all_original_base_QA_issues_preserved'] and not any(i['severity'] in ['warning','error'] for i in qa['issues'])
        positive.append(dict(id=row['id'],consumer=consumer,compiled_hex=encoded.encoded.hex(),qa=qa,clean_andcurrent_profile_equal=True))
    menu=compile_choices(doc['typed_choice_records'])
    assert menu.hex()==c['choice_object_hex'] and len(menu)==30
    def reject(label,fn,expected):
        try:fn()
        except ValueError as error:
            assert expected in str(error),(label,str(error))
            negative.append(dict(case=label,rejected=True,error=str(error),expected_guard=expected))
        else:raise AssertionError('Unsafe input accepted:'+label)
    body_guard='complete source and reviewed logical paragraph required'
    profile_guard='font/window/page/selector/guard/macro profile changed'
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);p=profiles[row['id']];text=row['english']
        bad=raw[:-1]+bytes([raw[-1]^1]);assert bad!=raw
        reject('changed-source-'+row['id'],lambda bad=bad,p=p,text=text:encode_relocatable_dialogue(bad,text,p),body_guard)
        reject('changed-prose-'+row['id'],lambda raw=raw,p=p,text=text:encode_relocatable_dialogue(raw,text+'!',p),body_guard)
    for field in ['records','typed_choice_records']:
        for i,row in enumerate(doc[field]):
            for gate in c['review_gates']:
                altered=deepcopy(doc);altered[field][i]['review'][gate]=False;assert altered!=doc
                reject('missing-'+gate+'-'+row['id'],lambda altered=altered:validate_approved_batch(altered),'v2 requires per-record')
                if field=='typed_choice_records':
                    reject('menu-direct-missing-'+gate+'-'+row['id'],lambda altered=altered:compile_choices(altered['typed_choice_records']),'All five individual B46 choice gates required')
    for row in [doc['records'][0],next(r for r in doc['records'] if r['source_selector']==254)]:
        p=profiles[row['id']];raw=bytes.fromhex(row['source_hex']);text=row['english']
        changes=[
            ('ASCII-width',replace(p,default_ascii_width=5)),('viewport228',replace(p,window_width_px=228)),
            ('row-pitch',replace(p,line_height_px=12)),('extra-page-capacity',replace(p,max_lines=8)),
            ('lost-page-capacity',replace(p,max_lines=2)),('pair-phase-disabled',replace(p,pair_phase_safe_breaks=False)),
            ('guard-disabled',replace(p,guard_linebreaks=False)),('balance-policy',replace(p,balanced_wrapping=not p.balanced_wrapping)),
            ('fallback208',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),
            ('literal-policy',replace(p,literal_prefix_policy='forbid')),
            ('FI-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':7})),
            ('FA-width',replace(p,macro_widths={**p.macro_widths,'FA':42})),
            ('FO-width',replace(p,macro_widths={**p.macro_widths,'FO':66}))]
        for label,bad in changes:
            assert bad!=p
            reject(label+'-'+row['id'],lambda raw=raw,text=text,bad=bad:encode_relocatable_dialogue(raw,text,bad),profile_guard)
        wrong='progressive' if row['source_selector']==254 else 'FE-paper'
        reject('wrong-consumer-'+row['id'],lambda row=row,wrong=wrong:profile_for(arm,source,row['id'],row['file_path'],wrong),'Original Rafael-B46 consumer required')
    zero=next(r for r in doc['records'] if r['source_selector']==0)
    raw=bytes.fromhex(zero['source_hex']);text=zero['english'];p=profiles[zero['id']]
    texts=[('manual-break',text+'{LB}'),('positioned-break',text+'{LB@3}'),('alignment',text+'{ALIGN@3}'),
        ('padding',text+'{PAD}'),('literal-LF',text+'\n'),('literal-CR',text+'\r'),
        ('leading-space',text.replace('}','} ',1)),('embedded-NUL',text+'\0'),
        ('missing-zero-selector',text.removeprefix('{SPEAKER:00}')),
        ('changed-zero-selector',text.replace('{SPEAKER:00}','{SPEAKER:06}')),
        ('invented-FI',text+'{MACRO:FI}'),('invented-FA',text+'{MACRO:FA}'),('invented-FO',text+'{MACRO:FO}')]
    for label,bad in texts:
        assert bad!=text
        reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,bad,p),body_guard)
    reject('missing-source00-byte',lambda:encode_relocatable_dialogue(raw[1:],text,p),body_guard)
    for label,index,old,new in SEMANTIC:
        row=next(r for r in doc['records'] if r['source_record_index']==index)
        assert old in row['english'];bad=row['english'].replace(old,new);assert bad!=row['english']
        reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profiles[row['id']]),body_guard)
    fe=next(r for r in doc['records'] if r['source_selector']==254)
    for label,bad in [('unsafe-printf',fe['english']+' %s'),('converted-FE',fe['english'].replace('{SPEAKER:FE}','{HEX:F8 F2}'))]:
        assert bad!=fe['english']
        reject(label,lambda bad=bad:encode_relocatable_dialogue(bytes.fromhex(fe['source_hex']),bad,profiles[fe['id']]),body_guard)
    block_guard='file-qualified B46 source/current block and2b6 runtime required'
    for label,bad in [('changed-tail',source[:-1]+bytes([source[-1]^1])),
        ('changed-header',bytes([source[0]^1])+source[1:]),('wrong-block',blocks[45]),('already-target-block',target)]:
        assert bad!=source
        reject(label,lambda bad=bad:profile_for(arm,bad,zero['id'],zero['file_path']),block_guard)
    reject('wrong-file',lambda:profile_for(arm,source,zero['id'],'/data/SC2.DK4'),block_guard)
    reject('changed-ARM9',lambda:profile_for(bytes([arm[0]^1])+arm[1:],source,zero['id'],zero['file_path']),block_guard)
    reject('unreviewed-ID',lambda:profile_for(arm,source,'DK4_MES_B46_R9999',zero['file_path']),'Unreviewed Rafael-B46 paragraph')
    for component in c['runtime_component_hashes']:
        original=image.read_file(component);changed=original[:-1]+bytes([original[-1]^1]);assert changed!=original
        class AlteredImage:
            def read_file(self,path):return changed if path==component else image.read_file(path)
        reject('runtime-'+component,lambda:validate_runtime(AlteredImage()),'Exact Rafael-B46 runtime component required:')
    for field,value in [('translation_policy','natural-dialogue-v1'),('target_locale','en-GB'),('encoder','legacy'),('file_path','/data/SC1.DK4'),('route',1)]:
        altered=deepcopy(doc);altered[field]=value;assert altered!=doc
        reject('batch-'+field,lambda altered=altered:validate_approved_batch(altered),'Exact B46 approved batch metadata required:')
    for idx,row in enumerate(doc['typed_choice_records']):
        for key,value in [
            ('english',row['english']+'!'),('source_hex',row['source_hex'][:-2]+'00'),
            ('current_hex',row['current_hex']+'20'),('option_index',1-idx),('command_offset',258),
            ('file_path','/data/SC2.DK4'),('block',45),('kind','progressive'),
            ('source_reference',{**row['source_reference'],'offset':row['source_reference']['offset']+2}),
            ('current_reference',{**row['current_reference'],'offset':row['current_reference']['offset']+2}),
            ('speaker','Julio'),('source_meaning','Unreviewed meaning'),('context','Unreviewed context'),
            ('localization_note','Unreviewed replacement'),('compiled_hex',row['compiled_hex']+'20')]:
            altered=deepcopy(doc['typed_choice_records']);altered[idx][key]=value;assert altered!=doc['typed_choice_records']
            reject('choice-'+str(idx)+'-'+key,lambda altered=altered:compile_choices(altered),'Exact B46 choice source/prose/context required:')
    choices=doc['typed_choice_records']
    for label,bad in [('reversed',list(reversed(choices))),('missing',choices[:1]),('duplicate',[choices[0],choices[0]]),('malformed',[choices[0],None])]:
        assert bad!=choices
        reject('choice-order-'+label,lambda bad=bad:compile_choices(bad),'Exact B46 two-choice source order required')
    assert len(positive)==24 and len({r['case'] for r in negative})==len(negative)
    assert sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==14
    assert before=={str(p):sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True)
    save(ROOT/'24_speech_two_choice_positives_actual_changing_expected_guard_rejections.json',dict(
        positive_cases=positive,positive_speeches=24,positive_menu=menu.hex(),positive_choice_labels=2,
        negative_cases=negative,negative_count=len(negative),original_rowcount_infos=14,
        all_original_QA_infos_preserved_no_warnings_orwaivers=True,
        all_expected_ValueError_guards_not_arbitrary_exceptions=True,
        all_five_record_gates_challenged_for_all26_records_andboth_direct_menu_choices=True,
        exact_source_current_profile_pairs_runtime_components_andtyped_menu_bound=True,
        source00_NUL_guard_andFE_consumer_scope_challenged=True,semantic_challenges=len(SEMANTIC),
        all_ROM_registry_ledger_pins_andpolicy_files_unchanged=True,
        atomic_production_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in sorted(paths)},producer_sha256=sha(Path(__file__).read_bytes()),
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('24 exact speech positives,2 choice labels;',len(negative),'actual-changing expected-guard rejections;14 infos,no waivers.Inputs unchanged.')
