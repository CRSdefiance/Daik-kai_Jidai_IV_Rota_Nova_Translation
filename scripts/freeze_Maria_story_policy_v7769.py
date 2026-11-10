"""Freeze67 exact file-qualified decisions with measured Maria macros andoriginal safe geometry."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_policy_v7769')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v3.json')
PLAN=Path('work/analysis/maria_story_final_prose_v7756b/67_final_v3_plans_two_refinements65_exact_compiled_retentions.json')
CURRENT=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
NATIVE=Path('work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json')
STORED=Path('work/analysis/maria_story_final_stored_v7759/67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json')
VIEW=Path('work/analysis/maria_story_final_view_v7768/130_final_actual_panes11_new_sheets93_prior_panes_exact.json')
NAMES=Path('translations/maria_B34_B108_B35_speaker_name_review_v3.json')
CONTRACT=Path('translations/maria_story_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/maria_story_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/maria_story_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/maria_story_plan_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,plan,current,native,stored,view=map(read,[MANUSCRIPT,PLAN,CURRENT,NATIVE,STORED,VIEW])
    assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and stored['font_proof_sha256']==sha(NATIVE.read_bytes())
    assert view['all130_final_actual_panes_viewed_with_exact_reuse'] and stored['all67_final_stored_targets_equal_reviewed_complete_native_ink']
    bindings={};deps={MANUSCRIPT,PLAN,CURRENT,NATIVE,STORED,VIEW,NAMES,Path(__file__)}
    for row,p,n in zip(doc['records'],plan['records'],native['records'],strict=True):
        assert row['id']==p['id']==n['id'] and row['english']==p['logical_English'] and row['source_hex']==p['source_hex']
        assert p['encoded_hex']==n['compiled_hex'] and len(n['pages'])==p['expected_native_pages']==1
        assert not row['review']['formatting'] and not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        group=next(g for g in current['groups'] if g['block']==row['block'])
        bindings[row['id']]=dict(file_path=row['file_path'],route=3,route_identity='Maria',block=row['block'],
            source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],source_header_hex=group['source_header_hex'],current_header_hex=group['current_header_hex'],
            route_aware_base_profile='maria-story-shared-events-live',source_selector=row['source_selector'],source_kind=row['kind'],
            source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],
            planning_record=p['planning_record'],logical_English=row['english'],compiled_hex=p['encoded_hex'],lines=p['lines'],
            maximum_total_rows=4,native_page_count=1,row_count_reason=p.get('row_count_reason'),
            ordinary_wrap_reasons=[],base_QA_issues=p['base_QA']['issues'],exact_reviewed_base_warnings=[],qa_waivers=[],qa_waiver_reason=None)
        deps.update(Path(pg['native_plane']) for pg in n['pages'])
    assert len(bindings)==67 and sum(bool(b['row_count_reason']) for b in bindings.values())==22
    deps.update(Path('dk4tool/dialogue')/s for s in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py','maria_B207_profile_v1.py','maria_B207_layout_v1.py'])
    deps.update(Path(p) for p in ['scripts/plan_Maria_story_layout_v7733.py','scripts/plan_lil_B234_layout_v7586d.py',
        'scripts/plan_lil_B214_layout_v6705b.py','scripts/source_locked_derivation_v5118.py','scripts/refine_Maria_story_final_prose_v7756b.py'])
    oldprofile=Path('dk4tool/dialogue/maria_B207_profile_v1.py').read_text('utf8')
    digest=next(s.split("'")[1] for s in oldprofile.splitlines() if s.startswith('CONTRACT_SHA='))
    oldmetrics="Actual Maria captain3/mask8 dispatch/getters andlogical/compiled bytes bound withthe exact disclosed system-only unlock,earned=false;zero source/English FI/FA/FO. Only source-bound R4 three CP932 ellipses are non-ASCII prose. Distinct CS0101 header preserved. Seven row-count infos andno warnings orwaivers."
    profile=checked_text(oldprofile,{
        'maria_B207_native_contract_v1':'maria_story_native_contract_v1',digest:'CONTRACT_DIGEST',
        'Maria-B207':'Maria-story','Maria SC3B207':'Maria SC3B34/B108/B35','!=18':'!=67','Complete18':'Complete67',
        "max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({19,104})":
        "max_lines=r['maximum_total_rows'],macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7},leading_speaker_bytes=frozenset({1,3,9,10,26,74,116,155})",
        oldmetrics:"Own Maria captain3/mask8 native macro/literal paths andfinal67 one-page paragraphs bound;scoped FI5/FA2/FO7 measurements replace no global defaults. Preserve eight original selectors,all12 real substitutions,source-supported ellipses andCS0101. Twenty-two individual row-count infos;no warnings orwaivers. Existing exact system-only unlock isdisclosed,earned=false. Shared155 label semantics andfull207 names remainopen.",
    })
    formatter=checked_text(Path('dk4tool/dialogue/maria_B207_layout_v1.py').read_text('utf8'),{
        'Maria18':'Maria67','seven informational row-count reasons':'22 informational row-count reasons',
        'maria_B207_profile_v1':'maria_story_profile_v1','Maria-B207':'Maria-story',
        'from scripts.plan_Maria_B207_layout_v7689 import plan as frozen_plan':'from dk4tool.dialogue.maria_story_plan_v1 import plan as frozen_plan',
    })
    planner="""\"\"\"The exact final-v3 source-owned automatic Maria planner; no authored layout.\"\"\"
from pathlib import Path
from scripts.plan_Maria_story_layout_v7733 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path('PLAN_PATH')
PLAN_SHA='PLAN_DIGEST'
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
exec(compile(read(PLAN)['source_owned_automatic_plan_adapter'],str(PLAN)+'::frozen','exec'),environment)
plan=environment['plan']
""".replace('PLAN_PATH',PLAN.as_posix()).replace('PLAN_DIGEST',sha(PLAN.read_bytes()))
    for p,text in [(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64)),(FORMATTER,formatter),(PLANNER,planner)]:compile(text,str(p),'exec')
    save(CONTRACT,dict(format='Maria-story-current-native-source-contract-v1',physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=67,
        record_bindings=bindings,choice_bindings={},dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},
        all_original_base_QA_issues_preserved=True,base_warning_count=0,individual_row_count_reasons=22,
        scoped_actual_FI5_FA2_FO7_not_global_profile_change=True,all_complete_sixbyte_preambles_andoriginal_macros_preserved=True,
        source_original_CS0101_headers_preserved=True,existing_system_only_unlock_fixture_earned_false=True,
        all67_formatting_false_policy_challenges_andrelease_pending=True,no_global_runtime_QA_name_asset_change=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),'utf8')
    FORMATTER.write_text(formatter,'utf8');PLANNER.write_text(planner,'utf8');ROOT.mkdir(parents=True)
    save(ROOT/'prepared67_exact_native_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),
        planner=str(PLANNER),planner_sha256=sha(PLANNER.read_bytes()),records=67,row_count_infos=22,
        immutable_original_profile_formatter_derived_with_native_high_constants_preserved=True,
        exact_final_automatic_adapter_andmeasured_scoped_macros=True,policy_challenges_production_release_pending=True,new_credit=0,full_goal_complete=False))
    print('67 exact native policy bindings;22 row-count infos,no warnings/waivers;FI5/FA2/FO7 scoped.No global label/font/runtime changes.')
