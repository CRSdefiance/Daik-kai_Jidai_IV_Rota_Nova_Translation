"""Freeze the complete B221 source-bound paragraphs, typed menu and scoped pagination."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_policy_v6992')
DOC=Path('translations/lil_B221_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_B221_choice_manuscript_v1.json')
CONTRACT=Path('translations/lil_B221_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/lil_B221_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/lil_B221_layout_v1.py')
TYPED=Path('dk4tool/dialogue/lil_B221_choices_v1.py')
VIEW=Path('work/analysis/lil_B221_native_source_view_v6989/all_native_pages_names_menu_both_source_choices_and_exact_wrap_reasons_viewed.json')
FONT=Path('work/analysis/lil_B221_native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments.json')
QA=Path('work/analysis/lil_B221_base_QA_v6982b/all14_base_QA_diagnostics_before_any_scoped_classification.json')
NAMES=Path('work/analysis/lil_B221_name_planes_v6981/three_actors_six_getters_nine_name_component_planes36_alignments.json')
MENU=Path('work/analysis/lil_B221_choices_v6977/three_original_choice_decoders_nine_modal_cases_twelve_complete_label_planes.json')

TYPED_SOURCE='''"""Compile only the exact two reviewed B221 response labels as one native object."""
import struct
from dk4tool.dialogue.lil_B221_profile_v1 import contract

def compile_choices(rows):
    d=contract();bindings=d['choice_bindings']
    expected=sorted(bindings,key=lambda ident:bindings[ident]['option_index'])
    if not isinstance(rows,list) or len(rows)!=2 or [r.get('id') for r in rows]!=expected:
        raise ValueError('Exact B221 two-choice source order required')
    chunks=[];offsets=[];cursor=0
    for row in rows:
        binding=bindings[row['id']]
        for key in ['english','source_hex','current_hex','source_reference','current_reference','option_index','command_offset','block','kind']:
            if row.get(key)!=binding[key]:raise ValueError('B221 reviewed choice differs:'+key)
        if not all(row.get('review',{}).get(k) is True for k in ['source','context','localization','naturalness']):
            raise ValueError('Four individual B221 choice prose gates required before native compilation')
        if any(not row.get(k) for k in ['speaker','source_meaning','context','localization_note']):
            raise ValueError('Complete B221 choice meaning/context required')
        value=row['english'].encode('ascii');offsets.append(cursor)
        chunk=value+b'\\0';chunk+=bytes(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    result=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
    if offsets!=[0,4] or result.hex()!=d['choice_object_hex']:
        raise ValueError('Exact original-count/source-index B221 native choice object required')
    return result
'''

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,TYPED])
    doc,choices,view,font,qa,menu=map(read,[DOC,CHOICES,VIEW,FONT,QA,MENU])
    assert not view['visual_review_pending'] and view['all16_final_native_body_pages_nine_name_planes_and_menu_sheet_viewed']
    assert font['manuscript_sha256']==sha(DOC.read_bytes()) and font['complete_native_pages']==16
    assert not [i for r in qa['records'] for i in r['base_QA']['issues'] if i['severity'] in ['warning','error']]
    planpath=Path(font['layout_plan']);plan=read(planpath)
    sourcepath=Path(doc['source_context']);source=read(sourcepath)
    native={r['id']:r for r in font['records']};plans={r['id']:r for r in plan['records']}
    viewed={r['id']:r for r in view['records']};bindings={};different=[]
    for row in doc['records']:
        ident=row['id'];p=plans[ident];v=viewed[ident];raw=bytes.fromhex(row['source_hex'])
        two=ident in ['DK4_MES_B221_R0046','DK4_MES_B221_R0060']
        assert p['encoded_hex']==native[ident]['compiled_hex'] and len(native[ident]['pages'])==(2 if two else 1)
        assert p['max_total_rows']==(8 if two else 4) and len(p['lines'])==(6 if two else len(p['lines']))
        diff=raw.count(b'\n')!=len(p['lines'])-1
        assert diff==bool(v['row_count_reason'])
        if diff:different.append(row['source_record_index'])
        page_reason=plan['page_boundary_reasons'].get(ident)
        assert bool(page_reason)==two
        bindings[ident]=dict(source_selector=row['source_selector'],source_kind='progressive',
            source_reference=row['source_reference'],current_reference=row['current_reference'],compiler_source_hex=row['source_hex'],
            planning_record={k:row[k] for k in ['id','english','kind','source_hex','source_selector']},
            compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=p['max_total_rows'],native_page_count=len(native[ident]['pages']),
            row_count_reason=v['row_count_reason'],ordinary_wrap_reasons=v['ordinary_boundary_reasons'],
            short_complete_sentence_opening_reasons=[],page_boundary_reason=page_reason)
    assert len(bindings)==14 and different==[8,27,33,39,46,60,63]
    choice_bindings={}
    for row in choices['records']:
        assert row['option_index'] in [0,1] and row['command_offset']==150 and row['block']==221
        choice_bindings[row['id']]={k:row[k] for k in ['english','source_hex','current_hex','source_reference','current_reference','option_index','command_offset','block','kind']}
    assert len(choice_bindings)==2 and menu['typed_target_object_hex']=='002100000400596573004e6f0000'
    dependencies=[DOC,CHOICES,VIEW,FONT,QA,NAMES,MENU,planpath,sourcepath,
        Path(doc['speaker_name_review']),Path(doc['current_consumer_proof']),Path(doc['current_strict_native_input']),
        Path('work/analysis/lil_B221_controls_v6971/two_A000_structural_cases50_normal_seeded_ends_choice_and_relatives_separate.json'),
        Path('work/analysis/lil_B221_branches_v6970/original_relative_skip_operand_proof.json'),
        Path('work/analysis/lil_B221_entry_v6969/source_EV2_B221_action_dependency_and_native_getter_binding.json'),
        Path('work/analysis/lil_B221_source_actual_v6988/two_source_choices_all14_speeches_all30_commands_complete_bodies_names_and_returns.json'),
        Path('scripts/plan_lil_B221_layout_v6976c.py'),Path('scripts/plan_lil_B214_layout_v6705b.py'),
        Path('work/analysis/lil_B221_wrap_tools_v6985/one_source_bound_auxiliary_boundary_no_prose_or_page_change.json'),
        Path('dk4tool/dialogue/lil_B220_profile_v1.py'),Path('dk4tool/dialogue/lil_B220_layout_v1.py'),Path(__file__),
        *[Path('dk4tool/dialogue')/n for n in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py']]]
    save(CONTRACT,dict(format='B221-current-native-source-contract-v1',
        source_block_hashes=[source['blocks'][0]['clean_block_sha256'],source['blocks'][0]['current_block_sha256']],
        physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=16,
        record_bindings=bindings,choice_bindings=choice_bindings,choice_object_hex=menu['typed_target_object_hex'],
        scoped_two_page_record_IDs=['DK4_MES_B221_R0046','DK4_MES_B221_R0060'],
        dependencies={str(p):sha(p.read_bytes()) for p in dependencies},
        no_base_QA_issue_removed_or_warning_waiver=True,
        seven_individual_rowcount_reasons_and25_exact_ordinary_boundaries=True,
        only_R67_had_gone_auxiliary_boundary_distinguished_no_global_waiver=True,
        unsafe_literal_I_before_LF_rejected_without_changing_prose=True,
        no_source_or_invented_FI_FA_FO=True,original_four_relatives_one2100_A000_and_normal_end_bound_separately=True,
        original_indices0_1_Yes_No_and_normal_value_words0_1_observed=True,
        source_name_assets_unchanged_Shopkeeper_separate_layer_pending=True,
        English_actual_pagination_final_stored_reference_and_registered_release_pending=True,new_credit=0,full_goal_complete=False))
    prototype=Path('dk4tool/dialogue/lil_B220_profile_v1.py').read_text('utf-8')
    oldhash=sha(Path('translations/lil_B220_native_contract_v1.json').read_bytes())
    profile=checked_text(prototype,{'B220':'B221',oldhash:sha(CONTRACT.read_bytes()),
        "len(d['record_bindings'])!=17":"len(d['record_bindings'])!=14",
        "len(d['choice_bindings'])!=0":"len(d['choice_bindings'])!=2",
        "d['complete_native_pages']!=17":"d['complete_native_pages']!=16",
        'seventeen-paragraph/no-menu':'fourteen-paragraph/two-choice/two-continuation',
        'frozenset({26,199})':'frozenset({2,17,85})',
        'original actors26/199,voices2/0,no source or invented macros;all seventeen complete paragraphs retain one original four-row page.':
        'original actors2/17/85,voices3/4/0,no source or invented macros;only R46/R60 retain six reviewed generated rows across two original four-row pages. Other twelve paragraphs remain one page. Two original response labels use their separate typed consumer.'})
    formatter=checked_text(Path('dk4tool/dialogue/lil_B220_layout_v1.py').read_text('utf-8'),{
        'B220':'B221','plan_lil_B220_layout_v6927b':'plan_lil_B221_layout_v6976c',
        'fourteen reviewed ordinary boundaries':'twenty-five reviewed ordinary boundaries'})
    for path,code in [(PROFILE,profile),(FORMATTER,formatter),(TYPED,TYPED_SOURCE)]:
        compile(code,str(path),'exec');path.write_text(code,encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_native_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),
        typed_compiler=str(TYPED),typed_compiler_sha256=sha(TYPED.read_bytes()),
        fourteen_paragraphs_two_choice_labels_two_scoped_two_page_paragraphs=True,
        all_original_QA_diagnostics_and_individual_boundary_reasons_preserved=True,
        no_new_ROM_credit_or_dialogue_formatting_gate=True,full_goal_complete=False))
    print('B221 policy frozen:14 paragraphs,2 typed labels,2 scoped continuations;7 row reasons/25 boundaries. No ROM or credit.')
