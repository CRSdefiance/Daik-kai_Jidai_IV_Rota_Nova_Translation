"""Freeze complete B222 source/English bytes and exact soft-wrap classifications."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_policy_v7050')
DOC=Path('translations/lil_B222_editorial_manuscript_v3.json')
VIEW=Path('work/analysis/lil_B222_native_review_v7049/all16_native_pages_and_exact_boundary_decisions.json')
CONTRACT=Path('translations/lil_B222_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/lil_B222_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/lil_B222_layout_v1.py')
AUDIT='''def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile)
    original=list(report['issues']);reviewed=r['exact_reviewed_base_warnings']
    if original!=r['base_QA_issues']:raise ValueError('Exact B222 base QA diagnostics changed')
    actual=[i for i in original if i['severity']=='warning']
    if actual!=reviewed or any(i['severity']=='error' for i in original):raise ValueError('Unwaived B222 base QA issue')
    if reviewed and (r['qa_waivers']!=['weak-line-ending'] or not r['qa_waiver_reason']):raise ValueError('Exact B222 record waiver reason required')
    report['issues']=[i for i in original if i not in reviewed]
    report.update(base_QA_issues=original,exact_reviewed_base_warnings=reviewed,
        qa_waivers=r['qa_waivers'],qa_waiver_reason=r['qa_waiver_reason'],
        native_rows_per_page=4,native_page_count=r['native_page_count'],
        row_count_reason=r['row_count_reason'],reviewed_ordinary_boundaries=r['ordinary_wrap_reasons'],
        all_original_base_QA_issues_preserved=True,no_global_weak_boundary_rule_changed=True)
    return report
'''
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER])
    doc,view=map(read,[DOC,VIEW]);fp=Path(view['font_proof']);font=read(fp);pp=Path(view['paragraph_plan']);plan=read(pp);sourcepath=Path(doc['source_context']);source=read(sourcepath)
    assert view['manuscript_sha256']==sha(DOC.read_bytes()) and view['original_warnings']==view['exact_record_local_weak_boundary_waivers']==2 and view['unwaived_warnings']==0
    plans={r['id']:r for r in plan['records']};native={r['id']:r for r in font['records']};bindings={}
    for r in doc['records']:
        p=plans[r['id']];assert r['english']==p['English'] and r['source_hex']==p['source_hex'] and native[r['id']]['compiled_hex']==p['encoded_hex'] and len(native[r['id']]['pages'])==1
        assert not any(v in r['english'] for v in ['{LB','{PAD','{ALIGN','\n','\r']) and not any(x.split()[-1]=='I' for x in p['lines'][:-1])
        bindings[r['id']]=dict(source_selector=r['source_selector'],source_kind='progressive',source_reference=r['source_reference'],current_reference=r['current_reference'],compiler_source_hex=r['source_hex'],planning_record={k:r[k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason=r['row_count_reason'],ordinary_wrap_reasons=r['ordinary_boundary_reasons'],short_complete_sentence_opening_reasons=[],page_boundary_reason=None,base_QA_issues=r['all_original_base_QA_issues'],exact_reviewed_base_warnings=r['exact_reviewed_base_warnings'],qa_waivers=r['qa_waivers'],qa_waiver_reason=r['qa_waiver_reason'])
    deps=[DOC,VIEW,fp,pp,sourcepath,Path(view['base_QA']),Path(view['name_proof']),Path(view['source_visual_review']),Path(doc['speaker_name_review']),Path(doc['current_consumer_proof']),Path(doc['current_strict_native_input']),Path('scripts/plan_lil_B222_layout_v7046b.py'),Path('scripts/plan_lil_B214_layout_v6705b.py'),Path('scripts/review_lil_B222_names_v7041b.py'),Path('scripts/lil_B222_source_span_binding_v7037.py'),Path('scripts/square_shopkeeper_exact_native_context_v7020.py'),Path('scripts/square_shopkeeper_font_oracles_v7020.py'),Path('dk4tool/dialogue/lil_B220_profile_v1.py'),Path('dk4tool/dialogue/lil_B220_layout_v1.py'),Path(__file__),*[Path('dk4tool/dialogue')/n for n in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py']]]
    save(CONTRACT,dict(format='B222-current-native-source-contract-v1',source_block_hashes=[source['blocks'][0]['clean_block_sha256'],source['blocks'][0]['current_block_sha256']],physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=16,record_bindings=bindings,choice_bindings={},dependencies={str(p):sha(p.read_bytes()) for p in deps},all_original_base_QA_diagnostics_preserved=True,two_exact_record_local_weak_boundary_waivers_no_global_change=True,seven_individual_rowcount_reasons=True,unsafe_literal_I_before_LF_rejected=True,no_source_or_invented_FI_FA_FO=True,all16_formatting_actual_reference_and_release_pending=True,original18_commands_A000_and_complete_normal_end_bound_separately=True,new_credit=0,full_goal_complete=False))
    oldhash=sha(Path('translations/lil_B220_native_contract_v1.json').read_bytes())
    profile=checked_text(Path('dk4tool/dialogue/lil_B220_profile_v1.py').read_text('utf8'),{'B220':'B222',oldhash:sha(CONTRACT.read_bytes()),'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':doc['current_ARM9_sha256'],"len(d['record_bindings'])!=17":"len(d['record_bindings'])!=16","d['complete_native_pages']!=17":"d['complete_native_pages']!=16",'seventeen-paragraph/no-menu':'sixteen-paragraph/no-menu','frozenset({26,199})':'frozenset({2,16})','original actors26/199,voices2/0,no source or invented macros;all seventeen complete paragraphs retain one original four-row page.':'original actors2/16,voices3/1,no source or invented macros;all sixteen complete paragraphs retain one original four-row page.','and AA5 runtime required':'and exact2b6 runtime required'})
    original=Path('dk4tool/dialogue/lil_B220_layout_v1.py').read_text('utf8');old_audit=original[original.index('def audit_relocatable_dialogue_record(raw,text,profile):'):]
    formatter=checked_text(original,{'B220':'B222','plan_lil_B220_layout_v6927b':'plan_lil_B222_layout_v7046b','fourteen reviewed ordinary boundaries':'source-bound complete-word boundaries and two exact diagnostic classifications',old_audit:AUDIT})
    for path,code in [(PROFILE,profile),(FORMATTER,formatter)]:compile(code,str(path),'exec');path.write_text(code,'utf8')
    ROOT.mkdir(parents=True);save(ROOT/'prepared_native_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),all16_complete_paragraphs_one_native_page_each=True,original_diagnostics_retained_two_exact_waivers=True,no_global_QA_font_geometry_guard_or_runtime_change=True,new_credit=0,full_goal_complete=False))
    print('B222 frozen:16 whole paragraphs,7 row reasons,2 exact diagnostic waivers; strict2b6. No credit.')
