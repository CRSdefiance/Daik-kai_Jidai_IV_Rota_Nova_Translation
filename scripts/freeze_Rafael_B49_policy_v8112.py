"""Freeze all61 approved B49 single-page paragraphs, exact source controls and three narrow warnings."""
from pathlib import Path
from scripts import freeze_Rafael_B48_policy_v8058 as previous
from scripts.freeze_Rafael_B46_policy_v7956 import BOUND_FIELDS,GATES
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.rafael_B48_profile_v1 import contract as prior_contract
from scripts.approve_Rafael_B49_actual_v8111 import OUT as DOC,NAMES,PLAN,CALLERS,REVIEW
ROOT=Path('work/analysis/Rafael_B49_policy_v8112')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
NATIVE=Path('work/analysis/Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json')
APPROVAL=Path('work/analysis/Rafael_B49_actual_approval_v8111/61_source_context_native_representative_actual_approved_policy_release_pending.json')
CONTRACT=Path('translations/rafael_B49_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/rafael_B49_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/rafael_B49_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/rafael_B49_plan_v1.py')
metrics=previous.PROFILE_SOURCE.split('metrics_source="',1)[1].split('")',1)[0]
PROFILE_SOURCE=checked_text(previous.PROFILE_SOURCE,{
    'B48':'B49','!=91 or d["choice_bindings"]':'!=61 or d["choice_bindings"]',
    'd["complete_native_pages"]!=92':'d["complete_native_pages"]!=61',
    'ninety-one-paragraph/ninety-two-page':'sixty-one-paragraph/sixty-one-page',
    '{"FI":1,"FA":0,"FO":0}':'{"FI":2,"FA":0,"FO":0}',
    'else {0,4,5,6,7,8,13,75,113}':'else {0,2,4,5,6,8,9}',
    metrics:'Exact B49/current2b6:216px usable text/four physical rows; all61 progressive paragraphs use one216x64 page. Source00/02/09 and all seven selectors remain original preambles; body NUL guard unchanged. Native FI6/FA6/FO10,twoFI,complete compiled/stored planes andpaired actual masks verified. Coherent phrase preferences preserve all words androw counts. Three exact source/text/compiled/line-bound weak endings retain all original warnings and22infos. Four actual complete names,three native-only headers,50actual speeches per language and11native-only conditionals remain scoped. Timing,RNG andlater RGB differences retained despite equal sampled final components/actor. No full simulation equivalence or global font/profile/guard/weak-rule change.',
})
FORMATTER_SOURCE=checked_text(previous.FORMATTER_SOURCE,{'B48':'B49'})
PLANNER_SOURCE=checked_text(previous.PLANNER_SOURCE,{
    'B48':'B49','plan_Rafael_B48_layout_v8035d':'plan_Rafael_B49_layout_v8090c',
    'environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}':'environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}\nenvironment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["source_coherent_phrase_pairs"]}',
})
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,names,plan,current,native,approval=map(read,[DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and not plan['failures']
    assert approval['all61_individual_source_context_prose_andformat_gates_true']
    assert approval['actual_complete_holds']==318 and approval['actual_speech_occurrences']==100
    assert approval['eleven_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage']
    assert approval['actual_later_five_components_andwhole_actor_equal_RNG_andRGB_differences_preserved']
    assert approval['C281_original_effect_body_andtransition_complete_Lil_Camille_headers_andnormal_return_verified']
    assert approval['disclosed_opening_ROM_entry_fixture_not_natural_B49_activation_original_location_fullroute_orhardware']
    assert len(approval['directly_viewed_sheets'])==22 and all(s['directly_viewed'] for s in approval['directly_viewed_sheets'])
    image=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256']
    group=current['groups'][0]
    deps={Path(p) for p in prior_contract()['dependencies']}|{DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL,REVIEW,Path(__file__),Path(previous.__file__)}
    for key in ['actual_proof','comparison','RNG_measurement','focused_C281_transition']:
        path=Path(approval[key]);assert sha(path.read_bytes())==approval[key+'_sha256'];deps.add(path)
    for s in approval['directly_viewed_sheets']:
        path=Path(s['path']);assert sha(path.read_bytes())==s['sha256'];deps.add(path)
    for path,digest in doc['evidence'].items():
        p=Path(path);assert sha(p.read_bytes())==digest;deps.add(p)
    for path in [
        'scripts/plan_Rafael_B49_layout_v8090c.py','scripts/approve_Rafael_B49_actual_v8111.py',
        'work/analysis/Rafael_B49_loaders_v8103/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        str(CALLERS),'work/analysis/Rafael_B49_reference_v8102/research_image_receipt.json',
        'work/analysis/Rafael_B49_C281_structural_v8080/exact_C281_source_original_structural_boundary.json',
    ]:deps.add(Path(path))
    bindings={}
    waiver_lines={'DK4_MES_B49_R0213':1,'DK4_MES_B49_R0244':2,'DK4_MES_B49_R0405':1}
    for row,p,n,c in zip(doc['records'],plan['records'],native['records'],current['records'],strict=True):
        ident=row['id'];assert ident==p['id']==n['id']==c['id']
        assert row['english']==p['planning_record']['english']
        assert row['source_hex']==p['source_hex']==c['source_hex'] and row['current_hex']==c['current_hex']
        assert row['compiled_hex']==p['encoded_hex']==n['compiled_hex'] and all(row['review'][g] is True for g in GATES)
        assert len(n['pages'])==p['expected_native_pages']==1 and p['max_total_rows']==4
        warnings=[i for i in p['base_QA']['issues'] if i['severity']=='warning']
        assert not any(i['severity']=='error' for i in p['base_QA']['issues'])
        if row['qa_waivers']:
            scope=row['qa_waiver_scope'];assert ident in waiver_lines
            assert row['qa_waivers']==['weak-line-ending'] and row['qa_waiver_reason']
            assert scope['id']==ident and scope['source_hex']==row['source_hex'] and scope['compiled_hex']==row['compiled_hex']
            assert scope['logical_English']==row['logical_English'] and warnings==[scope['exact_issue']]
            line=scope['line'];assert line==waiver_lines[ident]
            assert p['lines'][line-1].split()[-1].strip('.,;:!?')==scope['last_word'] and p['lines'][line].split()[0]==scope['next_word']
        else:assert not warnings and not row['qa_waiver_scope']
        row_info=any(i['code']=='line-break-count' for i in p['base_QA']['issues'])
        fields=BOUND_FIELDS+['source_complete_preamble_hex','source_selector','compiled_hex','logical_English','qa_waivers','qa_waiver_reason','qa_waiver_scope','row_count_reason','actual_record_observed','native_only_unvisited_conditional']
        bindings[ident]=dict(file_path=row['file_path'],route=0,route_identity='Rafael',block=49,
            source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],source_header_hex=group['source_header_hex'],current_header_hex=group['current_header_hex'],
            source_reference=row['source_reference'],current_reference=row['current_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],
            predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],consumer='progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,
            row_count_reason=row['row_count_reason'] if row_info else None,ordinary_wrap_reasons=[row['row_count_reason']],base_QA_issues=p['base_QA']['issues'],
            qa_waivers=row['qa_waivers'],qa_waiver_reason=row['qa_waiver_reason'],qa_waiver_scope=row['qa_waiver_scope'],approved_fields={k:row[k] for k in fields})
        for pg in n['pages']:
            for pk,hk in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:
                path=Path(pg[pk]);assert sha(path.read_bytes())==pg[hk];deps.add(path)
    assert len(bindings)==61 and sum(b['source_selector']==0 for b in bindings.values())==16
    assert {b['source_selector'] for b in bindings.values()}=={0,2,4,5,6,8,9}
    infos=sum(bool(b['row_count_reason']) for b in bindings.values());assert infos==22
    assert sum(bool(b['qa_waivers']) for b in bindings.values())==3
    planner=PLANNER_SOURCE.replace('PLAN_PATH',PLAN.as_posix()).replace('PLAN_DIGEST',sha(PLAN.read_bytes()))
    profile=PROFILE_SOURCE.replace('CONTRACT_PATH',CONTRACT.as_posix())
    for path,text in [(PLANNER,planner),(FORMATTER,FORMATTER_SOURCE),(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64))]:compile(text,str(path),'exec')
    for path,text in [(PLANNER,planner),(FORMATTER,FORMATTER_SOURCE)]:path.write_text(text,encoding='utf8');deps.add(path)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV0.DK4']}
    save(CONTRACT,dict(format='Rafael-B49-source-native-contract-v1',record_bindings=bindings,choice_bindings={},review_gates=GATES,
        batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','block']},
        source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],runtime_component_hashes=runtime,
        measured_macro_ascii_lengths=dict(FI=6,FA=6,FO=10),source_macro_counts=dict(FI=2,FA=0,FO=0),physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],usable_text_width_px=216,complete_native_pages=61,
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},all61_source_context_native_stored_andrepresentative_actual_checks_bound=True,
        individual_row_count_infos=infos,exact_warning_exception_count=3,all_original_base_QA_issues_preserved_three_exact_narrow_exceptions=True,
        all61_single_original_four_row_pages_no_FE_or_typed_menus=True,exact_original_source00_02_09_allseven_preambles_andbody_NUL_rejection_preserved=True,
        actual_eleven_conditional_speeches_andthree_headers_not_visited=True,actual_C281_effect_andLil_Camille_names_return_bound=True,
        measured_timing_RNG_components_calendar_RGB_limits_retained=True,frozen_policy_validation_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8')
    ROOT.mkdir(parents=True);save(ROOT/'prepared61_speeches61_pages_no_FE_three_exact_warning_exceptions.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        files={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER]},source_locked_template=str(previous.__file__),source_locked_template_sha256=sha(Path(previous.__file__).read_bytes()),
        records=61,pages=61,choices=0,FE_consumers=0,row_count_infos=infos,exact_warning_exceptions=3,all_five_per_record_gates_true_representative_actual_andmeasured_limits_bound=True,
        policy_challenges_atomic_production_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Frozen B49:61 single-page paragraphs/noFE;22 infos/three exact warnings. Policy challenges and integration pending;zero credit.')
