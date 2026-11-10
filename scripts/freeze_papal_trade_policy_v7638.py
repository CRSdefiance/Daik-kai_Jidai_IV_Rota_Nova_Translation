"""Freeze36 reviewed paragraphs and route-specific policy without changing shared defaults."""
from pathlib import Path
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS,NAMES,CURRENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/papal_trade_policy_v7638')
VIEW=Path('work/analysis/papal_trade_native_review_v7635/all36_native_paragraphs_viewed_two_exact_R33_boundaries16_row_infos_stored_actual_pending.json')
PLAN=Path('work/analysis/papal_trade_layout_v7632b/two_routes36_automatic_full_width_plans_all_base_QA_preserved.json')
NATIVE=Path('work/analysis/papal_trade_native_pages_v7634/two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json')
CONTRACT=Path('translations/papal_trade_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/papal_trade_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/papal_trade_layout_v1.py')
PROFILE_TEXT='''"""Exact SC0B246/SC1B237 source, route, prose and guarded geometry contract."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/papal_trade_native_contract_v1.json')
CONTRACT_SHA='CONTRACT_DIGEST'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('Frozen papal-trade contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Native dependency changed:'+p)
    if len(d['record_bindings'])!=36 or d['choice_bindings'] or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=36:raise ValueError('Complete36-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed papal-trade paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile(r['route_aware_base_profile'])
    return replace(base,name='papal-trade-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({19,104}),literal_prefix_policy='native-guard-v255',metrics_source=base.metrics_source+'; exact route-bound '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase andguards. Actual captain0/1 route dispatch/getters andlogical/compiled processor bytes bound;zero source/English FI/FA/FO. Only source-bound R5 original three CP932 ellipses are non-ASCII prose. One exact R33 article continuation perfile keeps Papal States whole. Every base QA issue androw reason preserved. No global font,width,literal I/F,macro orweak-ending change. Stored,actual andrelease approval remains separate.')
def profile_for(arm,block,ident,file_path):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed papal-trade paragraph')
    r=d['record_bindings'][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r['file_path'] or sha(block) not in r['source_block_hashes']:raise ValueError('Exact file-qualified source/current block and2b6 runtime required')
    return expected_profile(ident)
'''
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in [CONTRACT,PROFILE,FORMATTER])
    view,plan,native,current=map(read,[VIEW,PLAN,NATIVE,CURRENT]);bindings={}
    assert view['all_three_distinct_native_page_sheets_individually_viewed'] and native['layout_plan_sha256']==sha(PLAN.read_bytes())
    deps={VIEW,PLAN,NATIVE,CURRENT,NAMES,*MANUSCRIPTS.values(),Path(__file__),Path('scripts/plan_papal_trade_layout_v7632b.py'),Path('scripts/plan_papal_trade_layout_v7632.py'),Path('scripts/plan_lil_B234_layout_v7586d.py'),Path('scripts/plan_lil_B214_layout_v6705b.py'),Path('scripts/draft_papal_trade_prose_v7631.py'),Path('scripts/papal_trade_route_native_context_v7626.py')}
    for route,path in MANUSCRIPTS.items():
        doc=read(path);pg=plan['groups'][route];ng=native['groups'][route];vg=view['groups'][route];cg=current['groups'][route]
        assert pg['manuscript_sha256']==sha(path.read_bytes()) and cg['route']==route
        deps.add(Path(doc['current_strict_native_input']))
        for dkey in ['source_context','whole_clean_source_packet','current_consumer_proof','source_entry_proof','name_font_proof','controls_proof']:deps.add(Path(doc[dkey]))
        for row,p,n,v in zip(doc['records'],pg['records'],ng['records'],vg['records'],strict=True):
            assert row['id']==p['id']==n['id']==v['id'] and row['english']==p['English'] and row['source_hex']==p['source_hex']
            assert n['compiled_hex']==v['compiled_hex']==p['encoded_hex'] and len(n['pages'])==p['expected_native_pages']==1 and not row['review']['formatting']
            bindings[row['id']]=dict(file_path=doc['file_path'],route=route,route_identity=doc['route_identity'],block=row['block'],source_block_hashes=[cg['clean_block_sha256'],cg['current_block_sha256']],route_aware_base_profile=p['route_aware_base_profile'],source_selector=row['source_selector'],source_kind=row['kind'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],planning_record={k:row[k] for k in ['id','english','kind','source_hex','source_selector','source_record_index','route']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason=v['row_count_reason'],ordinary_wrap_reasons=([v['qa_waiver_reason']] if v['qa_waiver_reason'] else [v['row_count_reason']] if row['source_record_index']==64 else []),base_QA_issues=v['base_QA_issues'],exact_reviewed_base_warnings=v['exact_reviewed_base_warnings'],qa_waivers=v['qa_waivers'],qa_waiver_reason=v['qa_waiver_reason'])
            for page in n['pages']:deps.update([Path(page['native_plane']),Path(page['preview'])])
    deps.update(Path(s['path']) for s in native['review_sheets'])
    deps.update(Path('dk4tool/dialogue')/s for s in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py'])
    assert len(bindings)==36 and sum(bool(b['row_count_reason']) for b in bindings.values())==16 and sum(len(b['exact_reviewed_base_warnings']) for b in bindings.values())==2
    prior=Path('dk4tool/dialogue/lil_B234_layout_v1.py');deps.add(prior)
    formatter=checked_text(prior.read_text('utf8'),{'B234':'papal-trade','lil_B234_profile_v1':'papal_trade_profile_v1','lil-B234-source-bound-v1':'papal-trade-source-bound-v1','plan_lil_B234_layout_v7586d':'plan_papal_trade_layout_v7632b'})
    # checked_text uses simultaneous substitutions, so the more specific import/prefix
    # keys above retain valid Python identifiers while prose messages become route-neutral.
    compile(PROFILE_TEXT,str(PROFILE),'exec');compile(formatter,str(FORMATTER),'exec')
    save(CONTRACT,dict(format='papal-trade-current-native-source-contract-v1',physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=36,record_bindings=bindings,choice_bindings={},dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},all_original_base_QA_issues_preserved=True,exact_file_qualified_R33_warning_count=2,individual_row_count_reasons=16,all_source_current_English_zero_FI_FA_FO=True,only_exact_original_R5_three_CP932_ellipses_allowed=True,all36_formatting_gates_false_stored_actual_andrelease_pending=True,no_global_runtime_orQA_orname_item_asset_change=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(PROFILE_TEXT.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),'utf8');FORMATTER.write_text(formatter,'utf8');ROOT.mkdir(parents=True)
    save(ROOT/'prepared_two_route_native_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),records=36,two_exact_R33_boundaries16_row_infos_all_base_QA_preserved=True,source_owned_formatter_native_numeric_constants_unchanged=True,policy_challenges_stored_actual_andrelease_pending=True,new_credit=0,full_goal_complete=False))
    print('Exact36 file-qualified paragraphs frozen with actual route profiles;two scoped R33 warnings/16 row reasons. Policy challenges, stored/actual/release pending;zero credit.')
