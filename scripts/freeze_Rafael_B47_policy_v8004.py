"""Freeze fifteen approved B47 paragraphs, one scoped second page and two exact warnings."""
from pathlib import Path
from scripts import freeze_Rafael_B45_policy_v7901 as previous
from scripts.freeze_Rafael_B46_policy_v7956 import BOUND_FIELDS, GATES
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.rafael_B46_profile_v1 import contract as prior_contract

ROOT=Path('work/analysis/Rafael_B47_policy_v8004')
DOC=Path('translations/rafael_B47_editorial_manuscript_v3.json')
NAMES=Path('translations/rafael_B47_speaker_name_review_v3.json')
PLAN=Path('work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
NATIVE=Path('work/analysis/Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json')
APPROVAL=Path('work/analysis/Rafael_B47_actual_approval_v8003/15_source_context_native_representative_actual_approved_policy_release_pending.json')
CONTRACT=Path('translations/rafael_B47_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/rafael_B47_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/rafael_B47_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/rafael_B47_plan_v1.py')

PROFILE_SOURCE=checked_text(previous.PROFILE_SOURCE,{'B45':'B47'})
PROFILE_SOURCE=checked_text(PROFILE_SOURCE,{
    '!=12 or d["choice_bindings"]':'!=15 or d["choice_bindings"]',
    'd["complete_native_pages"]!=12':'d["complete_native_pages"]!=16',
    'Complete twelve-paragraph/no-menu contract required':'Complete fifteen-paragraph/sixteen-page/no-menu contract required',
    '{"FI":0,"FA":0,"FO":1}':'{"FI":0,"FA":0,"FO":0}',
    'max_lines=4,':'max_lines=r["maximum_total_rows"],',
    'else {0,6}':'else {0,4,5,6}',
    'One-step RNG timing difference retained;future random outcomes not proved equal.':
        'R53 alone may use two original four-row pages. Two exact source/text/compiled/line-bound weak-ending exceptions retain original warnings. Measured extra-page timing and later RNG/component/calendar/RGB differences retained; no full simulation equivalence.',
})
PROFILE_SOURCE+='''

def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact B47 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered B47 approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact B47 approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual B47 gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No B47 typed menu records authorized")
    return d
'''
FORMATTER_SOURCE=checked_text(previous.FORMATTER_SOURCE,{'B45':'B47'})
FORMATTER_SOURCE=checked_text(FORMATTER_SOURCE,{
    'issues!=r["base_QA_issues"] or any(i["severity"] in ["warning","error"] for i in issues)':
        'issues!=r["base_QA_issues"] or any(i["severity"]=="error" for i in issues) or [i for i in issues if i["severity"]=="warning"]!=([r["qa_waiver_scope"]["exact_issue"]] if r["qa_waivers"] else [])',
    'base QA diagnostics required without waivers':'base QA diagnostics and exact source-bound warning exception required',
    'native_page_count=1':'native_page_count=r["native_page_count"]',
    'no_warning_removal_orwaivers=True':'no_warning_removal=True,qa_waivers=r["qa_waivers"],qa_waiver_reason=r["qa_waiver_reason"],qa_waiver_scope=r["qa_waiver_scope"]',
})
PLANNER_SOURCE=checked_text(previous.PLANNER_SOURCE,{
    'B45':'B47','plan_Rafael_B45_layout_v7881b':'plan_Rafael_B47_layout_v7984e',
})

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,names,plan,current,native,approval=map(read,[DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and not plan['failures']
    assert approval['all15_individual_source_context_prose_andformat_gates_true']
    assert approval['actual_complete_holds']==88 and approval['actual_speech_occurrences']==22
    assert approval['four_conditional_speeches_andJanus_header_not_claimed_as_actual_coverage']
    assert approval['actual_later_models_persistent_objects_actors_calendar_andRGB_differences_preserved']
    assert approval['R53_two_pages_complete_ordinary_A4720_same_command_andfollowing_R70_return_verified']
    assert approval['disclosed_opening_ROM_entry_fixture_not_natural_B47_activation_original_location_fullroute_orhardware']
    assert len(approval['directly_viewed_sheets'])==8 and all(s['directly_viewed'] for s in approval['directly_viewed_sheets'])
    image=NdsImage.open(current['current_ROM'])
    assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256']
    group=current['groups'][0]
    deps={Path(p) for p in prior_contract()['dependencies']}|{DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL,Path(__file__),Path(previous.__file__),Path('scripts/freeze_Rafael_B46_policy_v7956.py')}
    for key in ['actual_proof','comparison','RNG_measurement','focused_page_turn']:
        path=Path(approval[key]);assert sha(path.read_bytes())==approval[key+'_sha256'];deps.add(path)
    for s in approval['directly_viewed_sheets']:
        path=Path(s['path']);assert sha(path.read_bytes())==s['sha256'];deps.add(path)
    # Bind existing exact research, stored, control and source evidence without re-running it.
    for path,digest in doc['evidence'].items():
        p=Path(path);assert sha(p.read_bytes())==digest;deps.add(p)
    for path in [
        'scripts/plan_Rafael_B47_layout_v7984e.py','scripts/approve_Rafael_B47_actual_v8003b.py',
        'work/analysis/Rafael_B47_loaders_v7995/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'work/analysis/Rafael_B47_reference_census_v7996/all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json',
        'work/analysis/Rafael_B47_reference_v7994/research_image_receipt.json',
    ]:deps.add(Path(path))
    bindings={}
    for row,p,n,c in zip(doc['records'],plan['records'],native['records'],current['records'],strict=True):
        ident=row['id'];assert ident==p['id']==n['id']==c['id']
        assert row['english']==p['planning_record']['english']
        assert row['source_hex']==p['source_hex']==c['source_hex'] and row['current_hex']==c['current_hex']
        assert row['compiled_hex']==p['encoded_hex']==n['compiled_hex'] and all(row['review'][g] is True for g in GATES)
        pages=2 if ident=='DK4_MES_B47_R0053' else 1
        assert len(n['pages'])==p['expected_native_pages']==pages and p['max_total_rows']==pages*4
        warnings=[i for i in p['base_QA']['issues'] if i['severity']=='warning']
        assert not any(i['severity']=='error' for i in p['base_QA']['issues'])
        if row['qa_waivers']:
            scope=row['qa_waiver_scope']
            assert ident in ['DK4_MES_B47_R0005','DK4_MES_B47_R0063']
            assert row['qa_waivers']==['weak-line-ending'] and row['qa_waiver_reason']
            assert scope['id']==ident and scope['source_hex']==row['source_hex'] and scope['compiled_hex']==row['compiled_hex']
            assert scope['line']==2 and warnings==[scope['exact_issue']]
            assert p['lines'][1].split()[-1].strip('.,;:!?')==scope['last_word']
            assert p['lines'][2].split()[0]==scope['next_word']
        else:assert not warnings and not row['qa_waiver_scope']
        row_info=any(i['code']=='line-break-count' for i in p['base_QA']['issues'])
        fields=BOUND_FIELDS+['source_complete_preamble_hex','source_selector','compiled_hex',
            'logical_English','qa_waivers','qa_waiver_reason','qa_waiver_scope','row_count_reason',
            'actual_record_observed','native_only_unvisited_conditional']
        bindings[ident]=dict(file_path=row['file_path'],route=0,route_identity='Rafael',block=47,
            source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],
            source_header_hex=group['source_header_hex'],current_header_hex=group['current_header_hex'],
            source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],
            predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],
            consumer='progressive',planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},
            compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=pages*4,native_page_count=pages,
            row_count_reason=row['row_count_reason'] if row_info else None,
            ordinary_wrap_reasons=[row['row_count_reason']],base_QA_issues=p['base_QA']['issues'],
            qa_waivers=row['qa_waivers'],qa_waiver_reason=row['qa_waiver_reason'],qa_waiver_scope=row['qa_waiver_scope'],
            approved_fields={k:row[k] for k in fields})
        for pg in n['pages']:
            for pk,hk in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:
                path=Path(pg[pk]);assert sha(path.read_bytes())==pg[hk];deps.add(path)
    assert len(bindings)==15 and sum(b['source_selector']==0 for b in bindings.values())==5
    assert {b['source_selector'] for b in bindings.values()}=={0,4,5,6}
    infos=sum(bool(b['row_count_reason']) for b in bindings.values());assert infos==6
    assert sum(bool(b['qa_waivers']) for b in bindings.values())==2 and sum(b['native_page_count'] for b in bindings.values())==16
    planner=PLANNER_SOURCE.replace('PLAN_PATH',PLAN.as_posix()).replace('PLAN_DIGEST',sha(PLAN.read_bytes()))
    profile=PROFILE_SOURCE.replace('CONTRACT_PATH',CONTRACT.as_posix())
    sources=[(PLANNER,planner),(FORMATTER,FORMATTER_SOURCE)]
    for path,text in sources+[(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64))]:compile(text,str(path),'exec')
    for path,text in sources:path.write_text(text,encoding='utf8');deps.add(path)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV0.DK4']}
    save(CONTRACT,dict(format='Rafael-B47-source-native-contract-v1',record_bindings=bindings,choice_bindings={},
        review_gates=GATES,batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','block']},
        source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],
        runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=6,FO=10),source_macro_counts=dict(FI=0,FA=0,FO=0),
        physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],usable_text_width_px=216,complete_native_pages=16,
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},
        all15_source_context_native_stored_andrepresentative_actual_checks_bound=True,
        individual_row_count_infos=infos,exact_warning_exception_count=2,
        all_original_base_QA_issues_preserved_two_exact_narrow_exceptions=True,
        R53_only_two_pages_original_four_physical_rows_allothers_one=True,
        exact_original_source00_preambles_andbody_NUL_rejection_preserved=True,
        actual_four_conditional_speeches_andJanus_header_not_visited=True,
        measured_timing_RNG_components_calendar_RGB_limits_retained=True,
        frozen_policy_validation_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8')
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared15_speeches16_pages_two_exact_warning_exceptions.json',dict(
        contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        files={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER]},
        source_locked_template=str(previous.__file__),source_locked_template_sha256=sha(Path(previous.__file__).read_bytes()),
        records=15,pages=16,choices=0,row_count_infos=infos,exact_warning_exceptions=2,
        all_five_per_record_gates_true_representative_actual_andmeasured_limits_bound=True,
        policy_challenges_atomic_production_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Frozen B47:15 speeches,16 pages,R53-only second page,six unchanged infos,two exact warnings/exceptions;policy challenges andatomic integration pending.')
