"""Actual-changing source/prose/profile/name/neighbor challenges against the frozen six-record policy."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch,validate_name_transition
from dk4tool.dialogue.gerhard_surname_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_policy_validation_v8237')
DOC=Path('translations/gerhard_surname_consistency_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();validate_approved_batch(doc)
    parent,target=NdsImage.open(c['parent_ROM']),NdsImage.open(c['target_ROM']);clean=NdsImage.open('work/clean.nds')
    arm,newarm=parent.read_file('/__arm9__.bin'),target.read_file('/__arm9__.bin')
    validate_runtime(parent);validate_runtime(target,'target');name_positive=validate_name_transition(arm,newarm)
    paths={DOC,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        Path(c['parent_ROM']),Path(c['target_ROM']),Path('out/raphael_natural_v2_accepted_base.nds'),Path('translations/gerhard_surname_native_contract_v1.json'),
        *[Path('dk4tool/dialogue')/n for n in ['gerhard_surname_profile_v1.py','gerhard_surname_layout_v1.py','gerhard_surname_plan_v1.py']]}
    before={str(p):sha(p.read_bytes()) for p in paths};positive=[];negative=[];profiles={}
    def reject(label,fn,expected):
        try:fn()
        except ValueError as error:
            assert expected in str(error),(label,str(error),expected)
            negative.append(dict(case=label,rejected=True,error=str(error),expected_guard=expected,actual_input_change_asserted=True))
        else:raise AssertionError('Changed unsafe input accepted:'+label)
    body_guard='complete source and reviewed logical paragraph required';profile_guard='font/window/page/selector/guard/macro profile changed'
    approved_guard='approved prose/source/context/waiver required';name_guard='Exact approved surname source/context/owned12-byte span required'
    for index,row in enumerate(doc['records']):
        ident=row['id'];p=profile_for(arm,IlnkContainer.parse(parent.read_file(row['file_path'])).blocks[row['block']],ident,row['file_path'],'progressive');profiles[ident]=p
        assert profile_for(arm,IlnkContainer.parse(clean.read_file(row['file_path'])).blocks[row['block']],ident,row['file_path'],'progressive')==p
        assert profile_for(newarm,IlnkContainer.parse(target.read_file(row['file_path'])).blocks[row['block']],ident,row['file_path'],'progressive')==p
        raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup'];encoded=encode_relocatable_dialogue(raw,text,p);qa=audit_relocatable_dialogue_record(raw,text,p)
        assert encoded.encoded.hex()==row['compiled_hex']==c['record_bindings'][ident]['compiled_hex']
        assert encoded.encoded[0]==row['source_selector'] and b'\0' not in encoded.encoded[1:] and qa['base_QA_issues']==row['all_original_QA_issues']
        assert qa['native_page_count']==1 and qa['all_original_base_QA_issues_preserved'] and qa['qa_waivers']==[]
        positive.append(dict(id=ident,compiled_hex=encoded.encoded.hex(),qa=qa,clean_current_target_profile_equal=True))
        bad=raw[:-1]+bytes([raw[-1]^1]);assert bad!=raw
        reject('source-byte-'+ident,lambda bad=bad,p=p,text=text:encode_relocatable_dialogue(bad,text,p),body_guard)
        reject('prose-byte-'+ident,lambda raw=raw,p=p,text=text:encode_relocatable_dialogue(raw,text+'!',p),body_guard)
        for gate in c['review_gates']:
            changed=deepcopy(doc);changed['records'][index]['review'][gate]=False;assert changed!=doc
            reject('missing-'+gate+'-'+ident,lambda changed=changed:validate_approved_batch(changed),'v2 requires per-record')
        fields={
            'english':row['english']+'!', 'logical_English':row['logical_English']+'!', 'source_meaning':row['source_meaning']+' Unreviewed claim.',
            'context':row['context']+' Unreviewed context.', 'localization_note':row['localization_note']+' Unreviewed adaptation.',
            'speaker':row['speaker']+' X', 'source_selector':254, 'source_hex':bad.hex(), 'current_hex':row['current_hex']+'20',
            'source_complete_preamble_hex':'ff'+row['source_complete_preamble_hex'][2:], 'block':row['block']+1,
            'kind':'system-FE', 'compiled_hex':row['compiled_hex']+'20', 'final_stored_hex':row['final_stored_hex']+'20',
            'source_reference':{**row['source_reference'],'offset':row['source_reference']['offset']+2},
            'current_reference':{**row['current_reference'],'offset':row['current_reference']['offset']+2},
            'final_reference':{**row['final_reference'],'offset':row['final_reference']['offset']+2},
            'retention_reason':row['retention_reason']+' Unreviewed reason.',
        }
        for key,value in fields.items():
            changed=deepcopy(doc);changed['records'][index][key]=value;assert changed!=doc
            reject('bound-'+key+'-'+ident,lambda changed=changed:validate_approved_batch(changed),approved_guard)
    semantic=[(0,"I've heard of you.","We've served together."),(1,'pirate hunter','pirate king'),(2,'Admiral','Uncle'),
        (3,'{MACRO:FI}','{MACRO:FO}'),(4,'Please keep teaching me!',"I'll be your apprentice forever!")]
    for index,old,new in semantic:
        changed=deepcopy(doc);r=changed['records'][index];assert old in r['english'];r['english']=r['english'].replace(old,new);r['logical_English']=r['english'];assert changed!=doc
        reject('source-fact-intent-'+r['id'],lambda changed=changed:validate_approved_batch(changed),approved_guard)
    for row in [doc['records'][0],doc['records'][3]]:
        p=profiles[row['id']];raw=bytes.fromhex(row['source_hex']);text=row['planned_English_markup']
        variants=[('ASCII5',replace(p,default_ascii_width=5)),('ASCII7',replace(p,default_ascii_width=7)),('CP93211',replace(p,default_multibyte_width=11)),
            ('width210',replace(p,window_width_px=210)),('width228',replace(p,window_width_px=228)),('rows8',replace(p,max_lines=8)),('pitch12',replace(p,line_height_px=12)),
            ('no-guard',replace(p,guard_linebreaks=False)),('no-pair-phase',replace(p,pair_phase_safe_breaks=False)),
            ('FI4',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4})),('FA6',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FA':6})),
            ('FO10',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('FI24px',replace(p,macro_widths={**p.macro_widths,'FI':24})),
            ('FA36px',replace(p,macro_widths={**p.macro_widths,'FA':36})),('FO60px',replace(p,macro_widths={**p.macro_widths,'FO':60})),
            ('I6px',replace(p,macro_widths={**p.macro_widths,'I':6})),('glyphA7',replace(p,glyph_widths={65:7})),
            ('extra-selector02',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{2})),('extra-selectorFE',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{254})),
            ('empty-selectors',replace(p,leading_speaker_bytes=frozenset())),('prefix-forbid',replace(p,literal_prefix_policy='forbid'))]
        for label,wrong in variants:
            assert wrong!=p;reject('profile-'+label+'-'+row['id'],lambda wrong=wrong,raw=raw,text=text:encode_relocatable_dialogue(raw,text,wrong),profile_guard)
        for label,badtext in [('authored-LB',text+'{LB}'),('positioned-LB',text+'{LB@24}'),('padding',text+'{PAD}'),('literal-LF',text+'\n'),('literal-NUL',text+'\0'),('authored-leading-space',' '+text)]:
            assert badtext!=text;reject(label+'-'+row['id'],lambda badtext=badtext,p=p,raw=raw:encode_relocatable_dialogue(raw,badtext,p),body_guard)
    for key,value in [('target_locale','en-GB'),('translation_policy','natural-dialogue-v1'),('encoder','raw'),('route',0),('file_path','/testdata/SC2.DK4')]:
        changed=deepcopy(doc);changed[key]=value;assert changed!=doc;reject('batch-'+key,lambda changed=changed:validate_approved_batch(changed),'approved batch metadata required')
    for label,rows in [('missing',doc['records'][:-1]),('duplicate',doc['records']+[deepcopy(doc['records'][0])]),('reordered',list(reversed(doc['records'])))]:
        changed=deepcopy(doc);changed['records']=rows;assert changed!=doc;reject('record-set-'+label,lambda changed=changed:validate_approved_batch(changed),'complete ordered')
    changed=deepcopy(doc);changed['typed_choice_records']=[dict(english='New menu')];assert changed!=doc
    reject('unreviewed-choice',lambda:validate_approved_batch(changed),'No new surname-revisit typed menu')
    for gate in c['review_gates']:
        changed=deepcopy(doc);changed['name_records'][0]['review'][gate]=False;assert changed!=doc
        reject('name-missing-'+gate,lambda changed=changed:validate_approved_batch(changed),'All five individual Gerhard name gates')
    name=doc['name_records'][0];name_fields={'actor_ID':18,'file_path':'/data/SC2.DK4','offset':name['offset']+1,'bytes':20,
        'current_hex':name['current_hex']+'00','target_hex':name['target_hex']+'00','source_Japanese':name['source_Japanese']+'ト',
        'english':'Lord Adernkatz','reason':name['reason']+' Official historical identity claimed.',
        'protected_Blades_neighbor':{**name['protected_Blades_neighbor'],'current_hex':'00'*8}}
    for key,value in name_fields.items():
        changed=deepcopy(doc);changed['name_records'][0][key]=value;assert changed!=doc
        reject('name-bound-'+key,lambda changed=changed:validate_approved_batch(changed),name_guard)
    for label,names in [('missing',[]),('duplicate',[deepcopy(name),deepcopy(name)])]:
        changed=deepcopy(doc);changed['name_records']=names;assert changed!=doc
        reject('name-set-'+label,lambda changed=changed:validate_approved_batch(changed),'Exactly one owned Gerhard surname')
    at=c['owned_name_span']['offset']
    for i in range(12):
        bad=bytearray(newarm);bad[at+i]^=1;assert bytes(bad)!=newarm
        reject('target-owned-byte-'+str(i),lambda bad=bytes(bad):validate_name_transition(arm,bad),'Exact terminated owned12-byte')
        bad=bytearray(arm);bad[at+i]^=1;assert bytes(bad)!=arm
        reject('source-owned-byte-'+str(i),lambda bad=bytes(bad):validate_name_transition(bad,newarm),'Exact terminated owned12-byte')
    for label,offset in [('before-name',at-1),('Blades-leading',at+12),('Blades-trailing',at+17),('Blades-NUL',at+18),('after-Blades',at+20)]:
        bad=bytearray(newarm);bad[offset]^=1;assert bytes(bad)!=newarm
        reject('unowned-'+label,lambda bad=bytes(bad):validate_name_transition(arm,bad),'Unowned ARM9 bytes or protected Blades')
    for index,ref in enumerate(c['name_andneighbor_pointer_references']):
        a,b=bytearray(arm),bytearray(newarm);a[ref['pointer_field_offset']]^=1;b[ref['pointer_field_offset']]^=1
        assert bytes(a)!=arm and bytes(b)!=newarm
        reject('same-corrupted-pointer-'+str(index),lambda a=bytes(a),b=bytes(b):validate_name_transition(a,b),'Protected name/item pointer field')
    for relative in range(1,12):
        a,b=bytearray(arm),bytearray(newarm);value=(c['owned_name_address']+relative).to_bytes(4,'little');a[at+20:at+24]=value;b[at+20:at+24]=value
        assert bytes(a)!=arm and bytes(b)!=newarm
        reject('interior-alias-'+str(relative),lambda a=bytes(a),b=bytes(b):validate_name_transition(a,b),'Interior surname literal pointer alias')
    for path in c['runtime_component_hashes']:
        changed=deepcopy(parent);raw=changed.read_file(path);bad=raw[:-1]+bytes([raw[-1]^1]);assert bad!=raw;changed.replace_file(path,bad)
        reject('runtime-component-'+path,lambda changed=changed:validate_runtime(changed),'runtime component required')
    mixed=deepcopy(parent);mixed.replace_file('/__arm9__.bin',newarm)
    reject('partial-name-with-old-archive-parent',lambda:validate_runtime(mixed),'runtime component required')
    reject('partial-name-with-old-archive-target',lambda:validate_runtime(mixed,'target'),'runtime component required')
    reject('unapproved-runtime-phase',lambda:validate_runtime(parent,'accepted'),'Exact parent ortarget runtime phase')
    after={str(p):sha(p.read_bytes()) for p in paths};assert after==before;contract();validate_approved_batch(doc)
    ROOT.mkdir(parents=True);negative_path=ROOT/'actual_changing_expected_guard_rejections.json';save(negative_path,negative)
    save(ROOT/'five_body_one_name_policy_positives_andexpected_guard_rejections.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_body_records=positive,positive_owned_name=name_positive,
        clean_current_target_profiles_equal_forall5=True,parent_andtarget_runtime_components_exact=True,
        negative_cases=str(negative_path),negative_cases_sha256=sha(negative_path.read_bytes()),negative_count=len(negative),
        all_mutations_change_actual_reviewed_source_prose_profile_orowned_neighbor_input=True,
        source_fact_rank_relationship_macro_source_preamble_layout_glyph_name_NUL_padding_Blades_alias_pointer_andpartial_runtime_guards_exercised=True,
        all_rejections_match_expected_semantic_guard=True,all_input_code_registry_ledger_ROM_pins_andfrozen_files_unchanged=True,
        trusted_frozen_contract_revalidated_before_andafter=True,no_dependency_bypass_inthis_policy_suite=True,
        later_independent_atomic_proof_corruption_andcommit_trap_suite_still_required=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,Path('translations/gerhard_surname_native_contract_v1.json'),Path(__file__)]}))
    print('Policy:5positivebody records/onepositiveowned name;expectedguardrejections',len(negative),';allinputs unchanged;atomic suite pending.')
