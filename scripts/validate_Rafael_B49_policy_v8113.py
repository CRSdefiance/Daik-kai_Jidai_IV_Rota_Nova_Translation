"""Exercise actual-changing B49 source/prose/waiver/profile inputs against frozen guards."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.rafael_B49_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue.rafael_B49_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Rafael_B49_policy_validation_v8113')
DOC=Path('translations/rafael_B49_editorial_manuscript_v3.json')
SEMANTIC=[('wrong-trade-house', 5, 'trade house', 'Guild'), ('reversed-Camille-rebuke', 20, 'Camille, stay out of it.', 'Camille, you make a good point.'), ('invented-final-warning', 74, "I'm only going to say this once.", 'This is your final warning.'), ('invented-established-trust', 122, 'you seem decent', 'you are our most trusted friend'), ('lost-unfinished-name-joke', 142, 'Hodram Ber... something', 'Hodram Bergstrom'), ('invented-given-name', 158, 'Clifford', 'James Clifford'), ('invented-Hanseatic-rank', 175, 'Martin Speyer', 'Admiral Martin Speyer'), ('lost-prospective-claim', 183, "we're hoping to claim", 'we already own'), ('wrong-contract-mechanic', 187, 'sign a contract with a city', 'conquer a city'), ('invented-permanent-trade-ban', 192, 'for a while', 'forever'), ('wrong-African-destination', 238, 'Africa', 'India'), ('wrong-western-New-World', 244, 'Head west to the New World', 'Head east to the New World'), ('invented-guaranteed-attack', 259, "We've got plans of our own", 'We will certainly attack you'), ('invented-completed-alliance', 266, "You're asking us to form a pact", "We've already signed a formal alliance"), ('reversed-pride', 271, "we're asking you for a favor", 'you owe us your obedience'), ('invented-romance', 275, 'You really hate to lose', "You're obviously in love with me"), ('changed-first-FI', 311, '{MACRO:FI}', '{MACRO:FA}'), ('wrong-Valdes-country', 328, 'Valdes of Spain', 'Valdes of Portugal'), ('lost-prospective-Spanish-threat', 331, 'has its eye on', 'has already conquered'), ('invented-common-enemy-assent-on-all-paths', 343, 'Uh...', 'Yes, Valdes is our common enemy.'), ('invented-kinship', 367, 'Lil, wait!', 'My sister Lil, wait!'), ('literalized-storm-joke', 381, "The storm's passed...", 'The weather forecast is clear.'), ('reversed-grudging-loyalty', 388, "I don't like it", 'I approve completely'), ('changed-second-FI', 388, '{MACRO:FI}', '{MACRO:FO}'), ('lost-qualified-impression', 392, "I bet she's scary", "I know she's always violent"), ('lost-North-Sea-condition', 405, "as long as the North Sea isn't all we have left", 'because we already rule the North Sea'), ('lost-temporary-decision', 409, 'for now', 'forever')]

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(DOC);c=contract();validate_approved_batch(doc)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    source=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks[49]
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(doc['file_path'])).blocks[49]
    target=Path('work/analysis/Rafael_B49_relocation_v8096/SC0_block49_RESEARCH_ONLY.bin').read_bytes()
    paths={DOC,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path('translations/rafael_B49_native_contract_v1.json'),
        *[Path('dk4tool/dialogue')/n for n in ['rafael_B49_profile_v1.py','rafael_B49_layout_v1.py','rafael_B49_plan_v1.py']]}
    before={str(p):sha(p.read_bytes()) for p in paths}
    positive=[];negative=[];profiles={}
    validate_runtime(image)
    def reject(label,fn,expected):
        try:fn()
        except ValueError as error:
            assert expected in str(error),(label,str(error))
            negative.append(dict(case=label,rejected=True,error=str(error),expected_guard=expected))
        else:raise AssertionError('Unsafe changed input accepted:'+label)
    body_guard='complete source and reviewed logical paragraph required'
    profile_guard='font/window/page/selector/guard/macro profile changed'
    approved_guard='Exact B49 approved prose/source/context/waiver required'
    for row in doc['records']:
        ident=row['id'];b=c['record_bindings'][ident];p=profile_for(arm,source,ident,row['file_path'],'FE-paper' if row['source_selector']==254 else 'progressive')
        assert profile_for(arm,clean,ident,row['file_path'],'FE-paper' if row['source_selector']==254 else 'progressive')==p
        profiles[ident]=p;raw=bytes.fromhex(row['source_hex'])
        encoded=encode_relocatable_dialogue(raw,row['english'],p)
        qa=audit_relocatable_dialogue_record(raw,row['english'],p)
        assert encoded.encoded.hex()==row['compiled_hex']==b['compiled_hex']
        assert encoded.encoded[0]==row['source_selector'] and b'\0' not in encoded.encoded[1:]
        assert qa['base_QA_issues']==b['base_QA_issues'] and qa['native_page_count']==b['native_page_count']
        assert qa['all_original_base_QA_issues_preserved'] and qa['qa_waiver_scope']==row['qa_waiver_scope']
        assert p.max_lines==4
        positive.append(dict(id=ident,compiled_hex=encoded.encoded.hex(),qa=qa,clean_andcurrent_profile_equal=True))
        bad=raw[:-1]+bytes([raw[-1]^1]);assert bad!=raw
        reject('changed-source-'+ident,lambda bad=bad,p=p,row=row:encode_relocatable_dialogue(bad,row['english'],p),body_guard)
        reject('changed-prose-'+ident,lambda raw=raw,p=p,row=row:encode_relocatable_dialogue(raw,row['english']+'!',p),body_guard)
        for gate in c['review_gates']:
            altered=deepcopy(doc);altered['records'][len(positive)-1]['review'][gate]=False;assert altered!=doc
            reject('missing-'+gate+'-'+ident,lambda altered=altered:validate_approved_batch(altered),'v2 requires per-record')
    for row in [doc['records'][0],next(r for r in doc['records'] if r['source_record_index']==15)]:
        p=profiles[row['id']];raw=bytes.fromhex(row['source_hex']);text=row['english']
        changes=[
            ('ASCII-width',replace(p,default_ascii_width=5)),('viewport228',replace(p,window_width_px=228)),
            ('row-pitch',replace(p,line_height_px=12)),('changed-page-capacity',replace(p,max_lines=4 if p.max_lines==8 else 8)),
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
        reject('wrong-consumer-'+row['id'],lambda row=row:profile_for(arm,source,row['id'],row['file_path'],'FE-paper'),'Original Rafael-B49 consumer required')
    zero=next(r for r in doc['records'] if r['source_selector']==0)
    raw=bytes.fromhex(zero['source_hex']);text=zero['english'];p=profiles[zero['id']]
    texts=[('manual-break',text+'{LB}'),('positioned-break',text+'{LB@3}'),('alignment',text+'{ALIGN@3}'),
        ('padding',text+'{PAD}'),('literal-LF',text+'\n'),('literal-CR',text+'\r'),
        ('leading-space',text.replace('}','} ',1)),('embedded-NUL',text+'\0'),
        ('missing-zero-selector',text.removeprefix('{SPEAKER:00}')),
        ('changed-zero-selector',text.replace('{SPEAKER:00}','{SPEAKER:06}')),
        ('invented-FI',text+'{MACRO:FI}'),('invented-FA',text+'{MACRO:FA}'),('invented-FO',text+'{MACRO:FO}'),
        ('unsafe-printf',text+' %s')]
    for label,bad in texts:
        assert bad!=text
        reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,bad,p),body_guard)
    reject('missing-source00-byte',lambda:encode_relocatable_dialogue(raw[1:],text,p),body_guard)
    for label,index,old,new in SEMANTIC:
        row=next(r for r in doc['records'] if r['source_record_index']==index)
        assert old in row['english'];bad=row['english'].replace(old,new);assert bad!=row['english']
        reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profiles[row['id']]),body_guard)
    for idx,row in enumerate(doc['records']):
        for field in ['source_meaning','context','localization_note','editorial_finding','retention_reason','decision','speaker']:
            altered=deepcopy(doc);altered['records'][idx][field]=str(row[field])+' changed';assert altered!=doc
            reject('changed-'+field+'-'+row['id'],lambda altered=altered:validate_approved_batch(altered),approved_guard)
        # Warning allowances may neither be removed nor copied to another record.
        altered=deepcopy(doc)
        altered['records'][idx]['qa_waivers']=[] if row['qa_waivers'] else ['weak-line-ending']
        assert altered!=doc
        reject('changed-warning-allowance-'+row['id'],lambda altered=altered:validate_approved_batch(altered),approved_guard)
        if row['qa_waivers']:
            for field in ['id','source_hex','compiled_hex','line','last_word','next_word','exact_issue']:
                altered=deepcopy(doc);scope=altered['records'][idx]['qa_waiver_scope']
                scope[field]=3 if field=='line' else ('changed' if field!='exact_issue' else dict(code='weak-line-ending',message='changed',severity='warning'))
                assert altered!=doc
                reject('changed-warning-scope-'+field+'-'+row['id'],lambda altered=altered:validate_approved_batch(altered),approved_guard)
            altered=deepcopy(doc);altered['records'][idx]['qa_waiver_reason']='Changed broad exception.'
            reject('changed-warning-reason-'+row['id'],lambda altered=altered:validate_approved_batch(altered),approved_guard)
    altered=deepcopy(doc);altered['records'].reverse()
    reject('reordered-records',lambda:validate_approved_batch(altered),'Exact complete ordered')
    altered=deepcopy(doc);altered['typed_choice_records']=[dict(english='Yes')]
    reject('invented-menu',lambda:validate_approved_batch(altered),'No B49 typed menu')
    badarm=arm[:-1]+bytes([arm[-1]^1]);assert badarm!=arm
    reject('changed-runtime',lambda:profile_for(badarm,source,zero['id'],zero['file_path']),'Exact file-qualified')
    reject('wrong-file',lambda:profile_for(arm,source,zero['id'],'/data/SC1.DK4'),'Exact file-qualified')
    reject('target-used-as-source',lambda:profile_for(arm,target,zero['id'],zero['file_path']),'Exact file-qualified')
    assert {str(p):sha(p.read_bytes()) for p in paths}==before
    assert len(positive)==61 and sum(x['qa']['native_page_count'] for x in positive)==61
    assert sum(i['severity']=='warning' for x in positive for i in x['qa']['issues'])==3
    assert sum(i['code']=='line-break-count' for x in positive for i in x['qa']['issues'])==22
    ROOT.mkdir(parents=True)
    save(ROOT/'61_speech61_page_positives_actual_changing_expected_guard_rejections.json',dict(
        positives=positive,negatives=negative,positive_count=len(positive),negative_count=len(negative),
        all_changed_inputs_verified_distinct=True,all_rejections_checked_against_expected_guard=True,
        all_original_QA_diagnostics_preserved_22_infos_three_exact_warning_exceptions=True,
        all61_single_pages_andallseven_source_selectors_source00_body_guard_preserved=True,
        eleven_native_only_speeches_andall_actual_measured_limits_retained=True,
        registry_ledger_pins_parent_andpolicy_files_unchanged=True,
        evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),
        atomic_production_andregistered_release_pending=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('B49:61 exact speech positives/61 pages;',len(negative),'actual-changing expected-guard rejections;22 infos/3 narrow warning exceptions unchanged. Atomic integration pending.')
