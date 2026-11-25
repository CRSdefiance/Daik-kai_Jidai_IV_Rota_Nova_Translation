"""Freeze exact18 Maria paragraphs, distinct CS0101 inputs and every reviewed QA finding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.draft_Maria_B207_prose_v7687 import MANUSCRIPT,NAMES,CURRENT,CLEAN,CONSUMERS,ENTRY,HEADER,FONTS,CONTROLS,CONTEXT
from scripts.record_Maria_B207_view_v7691 import PLAN,NATIVE,ROOT as VIEW_ROOT
ROOT=Path('work/analysis/maria_B207_policy_v7694')
VIEW=VIEW_ROOT/'Maria18_native_paragraphs_andown_selection_viewed_stored_actual_pending.json'
CONTRACT=Path('translations/maria_B207_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/maria_B207_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/maria_B207_layout_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in [CONTRACT,PROFILE,FORMATTER])
    doc,current,view,plan,native=map(read,[MANUSCRIPT,CURRENT,VIEW,PLAN,NATIVE])
    assert view['all_three_native_page_sheets_individually_viewed'] and native['layout_plan_sha256']==sha(PLAN.read_bytes())
    assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    deps={VIEW,PLAN,NATIVE,MANUSCRIPT,NAMES,CURRENT,CLEAN,CONSUMERS,ENTRY,HEADER,FONTS,CONTROLS,CONTEXT,Path(doc['current_strict_native_input']),Path(__file__),
          Path('scripts/plan_Maria_B207_layout_v7689.py'),Path('scripts/prove_Maria_B207_logical_v7688.py'),Path('scripts/draft_Maria_B207_prose_v7687.py'),
          Path('scripts/plan_lil_B234_layout_v7586d.py'),Path('scripts/plan_lil_B214_layout_v6705b.py'),Path('scripts/maria_unlocked_current_context_v7680.py'),Path('scripts/maria_existing_unlock_contract_v7680.py')}
    bindings={}
    for row,p,n,v in zip(doc['records'],plan['records'],native['records'],view['records'],strict=True):
        assert row['id']==p['id']==n['id']==v['id'] and row['english']==p['English'] and row['source_hex']==p['source_hex']
        assert n['compiled_hex']==v['compiled_hex']==p['encoded_hex'] and len(n['pages'])==p['expected_native_pages']==1 and not row['review']['formatting']
        assert v['qa_waivers']==[] and not any(i['severity'] in ['warning','error'] for i in v['base_QA_issues'])
        planning={k:row[k] for k in ['id','english','kind','source_hex','source_selector','source_record_index']};planning['route']=3
        bindings[row['id']]=dict(file_path=doc['file_path'],route=3,route_identity='Maria',block=207,
            source_block_hashes=[current['clean_block_sha256'],current['current_block_sha256']],source_header_hex=current['source_header_hex'],current_header_hex=current['current_header_hex'],
            route_aware_base_profile=p['route_aware_base_profile'],source_selector=row['source_selector'],source_kind=row['kind'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],planning_record=planning,
            compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason=v['row_count_reason'],
            ordinary_wrap_reasons=[v['row_count_reason']] if row['source_record_index'] in [50,63] else [],
            base_QA_issues=v['base_QA_issues'],exact_reviewed_base_warnings=[],qa_waivers=[],qa_waiver_reason=None)
        for page in n['pages']:deps.update([Path(page['native_plane']),Path(page['preview'])])
    deps.update(Path(s['path']) for s in native['review_sheets'])
    deps.update(Path('dk4tool/dialogue')/s for s in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py'])
    oldprofile=Path('dk4tool/dialogue/papal_trade_profile_v1.py');oldformatter=Path('dk4tool/dialogue/papal_trade_layout_v1.py');deps.update([oldprofile,oldformatter])
    prior=oldprofile.read_text('utf8');oldsha=next(s.split("'")[1] for s in prior.splitlines() if s.startswith('CONTRACT_SHA='))
    oldmetrics="Actual captain0/1 route dispatch/getters andlogical/compiled processor bytes bound;zero source/English FI/FA/FO. Only source-bound R5 original three CP932 ellipses are non-ASCII prose. One exact R33 article continuation perfile keeps Papal States whole."
    profile=checked_text(prior,{
        'Exact SC0B246/SC1B237 source, route, prose and guarded geometry contract.':'Exact Maria SC3B207 source, CS0101 header, prose and guarded geometry contract.',
        'papal_trade_native_contract_v1':'maria_B207_native_contract_v1',oldsha:'CONTRACT_DIGEST',
        'papal-trade':'Maria-B207','!=36':'!=18','Complete36':'Complete18',
        oldmetrics:"Actual Maria captain3/mask8 dispatch/getters andlogical/compiled bytes bound withthe exact disclosed system-only unlock,earned=false;zero source/English FI/FA/FO. Only source-bound R4 three CP932 ellipses are non-ASCII prose. Distinct CS0101 header preserved. Seven row-count infos andno warnings orwaivers.",
    })
    formatter=checked_text(oldformatter.read_text('utf8'),{
        'Frozen papal-trade whole paragraphs with source-bound complete-word boundaries and one exact R33 line1 article-wrap classification andeight informational row-count reasons.':'Frozen Maria18 whole paragraphs with source-bound complete-word boundaries,seven informational row-count reasons andno waived warnings.',
        'papal_trade_profile_v1':'maria_B207_profile_v1','papal-trade':'Maria-B207',
        'plan_papal_trade_layout_v7632b':'plan_Maria_B207_layout_v7689',
    })
    assert len(bindings)==18 and sum(bool(b['row_count_reason']) for b in bindings.values())==7
    compile(profile,str(PROFILE),'exec');compile(formatter,str(FORMATTER),'exec')
    save(CONTRACT,dict(format='Maria-B207-current-native-source-contract-v1',physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=18,record_bindings=bindings,choice_bindings={},dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},all_original_base_QA_issues_preserved=True,base_warning_count=0,individual_row_count_reasons=7,all_source_current_English_zero_FI_FA_FO=True,only_exact_original_R4_three_CP932_ellipses_allowed=True,complete_CS0101_header_preserved=True,existing_system_only_unlock_fixture_earned_false=True,all18_formatting_gates_false_stored_actual_andrelease_pending=True,no_global_runtime_orQA_orname_item_asset_change=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),'utf8');FORMATTER.write_text(formatter,'utf8');ROOT.mkdir(parents=True)
    save(ROOT/'prepared_exact_Maria18_native_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),records=18,seven_row_infos_all_base_QA_preserved_no_waivers=True,source_owned_formatter_native_numeric_constants_unchanged=True,policy_challenges_stored_actual_andrelease_pending=True,new_credit=0,full_goal_complete=False))
    print('Exact Maria18 file-qualified paragraphs frozen;CS0101 preserved,7 row infos/no warnings. Policy challenges/stored/actual/release pending;zero credit.')
