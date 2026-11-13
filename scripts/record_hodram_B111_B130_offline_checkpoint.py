"""Record completed prose/native views while leaving storage, English gameplay and release open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B111_B130_editorial_20261101')
DOC=Path('translations/hodram_B111_B130_editorial_manuscript_v1.json')
PLAN=ROOT/'plans_v5/automatic_plans.json'
NATIVE=ROOT/'native_v3/compiled_native_pages.json'
MENU=ROOT/'menu_v1/menu_provider_and_planes.json'
STYLE=ROOT/'styles_v1/compiled_style_objects.json'
LEDGER=Path('translations/editorial_review_current_v1.json')

def main():
    target=ROOT/'offline_checkpoint.json';assert not target.exists()
    doc,plan,native,menu,style=map(load,[DOC,PLAN,NATIVE,MENU,STYLE])
    assert (doc['total_editorial_objects'],doc['revised'],doc['retained'])==(323,239,84)
    assert native['manuscript_sha256']==menu['manuscript_sha256']==style['manuscript_sha256']==sha(DOC.read_bytes())
    assert native['plan_sha256']==style['plan_sha256']==sha(PLAN.read_bytes())
    assert not plan['failures'] and not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert len(doc['records'])==323 and len(native['records'])==len(plan['records'])==308
    assert len({r['id'] for r in doc['records']})==323
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    initial=ROOT/'native_v1/compiled_native_pages.json'
    changed=[ROOT/'native_v2/fresh/compiled_native_pages.json',ROOT/'native_v3/fresh/compiled_native_pages.json']
    viewed={};sheets=[]
    for path in [initial,*changed]:
        report=load(path)
        for sheet in report['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];sheets.append(sheet)
        for row in report['records']:
            rendered=row['complete_native_English_display']
            for page in rendered['pages'] if row['kind']=='progressive' else [rendered]:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
                viewed[page['native_plane_sha256']]=dict(native_report=str(path),id=row['id'],page=page.get('page',1))
    coverage=[]
    for row in native['records']:
        rendered=row['complete_native_English_display']
        for page in rendered['pages'] if row['kind']=='progressive' else [rendered]:
            key=page['native_plane_sha256'];assert key in viewed
            coverage.append(dict(id=row['id'],page=page.get('page',1),native_plane=page['native_plane'],native_plane_sha256=key,visual_binding=viewed[key]))
    assert len(coverage)==315 and len(sheets)==44
    FE=load(ROOT/'FE_final_layout_check.json');assert FE['FE_records']==35 and not FE['findings'] and FE['unexpected_blank_rows_orwraps_absent']
    findings={
        'DK4_MES_B117_R0031':"Keep We'll entrust it to you together on page2, with ancient times intact on page1.",
        'DK4_MES_B120_R0036':'Keep Japan barely escaped disaster as a complete subject/predicate on page2.',
        'DK4_MES_B121_R0118':"Begin page2 with the complete It's no use sentence rather than here with me alone.",
        'DK4_MES_B123_R0089':'Keep the complete second coordinated group, and the brutal soldiers who plunder it, on page2.',
        'DK4_MES_B123_R0118':'Keep to stop them together as the purpose clause on page2, with the following explanation.',
        'DK4_MES_B123_R0124':'Keep the full we can meet them complement together on page2, including equal terms.',
        'DK4_MES_B129_R0077':'Begin page2 with the complete trade-permission prohibition instead of without its permission alone.',
        'DK4_MES_B118_R0022':'Remove native extra blank row with a source-scoped formatter budget; preserve the final if I started with two condition as one line.',
        'DK4_MES_B127_R0053':'Remove native extra blank row without changing the L/left and R/right instructions.',
        'DK4_MES_B114_R0133':'Keep Let me ask you another together on its line.',
        'DK4_MES_B129_R0048':'Keep let me explain together on its line.',
    }
    save(ROOT/'visual_review.json',dict(native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),records=coverage,pages=315,
        directly_viewed_sheets=sheets,all_final_pages_directly_viewed_or_exact_plane_reuse=True,
        resolved_findings=findings,page_boundary_findings=7,extra_blank_row_findings=2,additional_phrase_findings=2,
        no_wording_shortened_for_layout=True,no_authored_ordinary_breaks=True,
        page_retention_reason='The seven long speeches retain every word and use the original four-row pagination. Some first-page rows are shorter to preserve the complete final sentence or coordinated clause. No isolated word, severed subject/predicate or blank filler row remains.',
        original_FE_physical_width_228_unchanged=True,two_FE_records_use_36_cell_formatter_budget_for_observed_guard_flush_wrap=True,
        FE_row_layout_check=str(ROOT/'FE_final_layout_check.json'),FE_row_layout_check_sha256=sha((ROOT/'FE_final_layout_check.json').read_bytes()),
        actual_gameplay=False,stored_script_andactual_English_andregistered_release_pending=True,new_credit=0))
    for path in [MENU]:
        reviewed=deepcopy(load(path));assert reviewed['direct_view_pending']
        for sheet in reviewed['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        assert len(reviewed['review_sheets'])==3 and reviewed['complete_English_caption_style_planes']==60
        reviewed.update(direct_view_pending=False,offline_visual_approved=True,original_pending_report=str(path),original_pending_report_sha256=sha(path.read_bytes()),
            visual_review_note='All current/reviewed captions directly viewed on the three readable sheets. Both native style masks are complete; actual English highlight/controller scenes remain pending.')
        save(path.with_name(path.stem+'_reviewed.json'),reviewed)
    fixture_root=Path('work/analysis/Hodram_B111_B130_source_fixtures_20261101')
    fixture=load(fixture_root/'fixtures.json');runs=[]
    for block,folder,frames in [(126,'Hodram_B111_B130_B126_source_20261101',8501),(118,'Hodram_B111_B130_B118_source_third_20261101',8001)]:
        reportpath=Path('work/emulation_v193')/folder/'capture_report.json';report=load(reportpath)
        binding=next(r for r in fixture['fixtures'] if r['block']==block)
        assert report['ROM_sha256']==binding['ROM_sha256'] and report['frames']==frames
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['hardware_device_verification'] and not report['callback_errors']
        runs.append(dict(block=block,capture_report=str(reportpath),capture_report_sha256=sha(reportpath.read_bytes()),ROM_sha256=report['ROM_sha256'],frames=frames,
            actual_scripted_input_schedule=report['scripted_input_schedule']))
    source_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in sorted((fixture_root/'QA').glob('*.png'))];assert len(source_sheets)==4
    source_actual=dict(fixture_definition=str(fixture_root/'fixtures.json'),fixture_definition_sha256=sha((fixture_root/'fixtures.json').read_bytes()),
        runs=runs,total_completed_frames=16502,directly_viewed_source_sheets=source_sheets,
        Rafael_source_preamble='0040ffff0000',Rafael_source_body_ID_andobserved_frame={
            'DK4_MES_B126_R0013':4320,'DK4_MES_B126_R0021':4800,'DK4_MES_B126_R0029':5280,'DK4_MES_B126_R0038':5760,'DK4_MES_B126_R0049':6480},
        source_Rafael_portrait_complete_nameplate_andFI_Hodram_observed=True,
        source_three_choice_observations=dict(first_highlight=5300,second_highlight=5320,third_highlight=5360,third_held=5400,correct_branch_Hodram=5520,Gerhard_reply=5760,answer59=6000,reward=6240,Stockholm_return=6720),
        source_B126_knife_widget_acquisition_andStockholm_return_observed=True,
        uncompleted_earlier_probe=dict(session=82371,exit_code=1,reason='Interactive checker stdin reached EOF at5300; no final capture report. Preserve partial images; not counted as a completed run or ROM defect.'),
        no_savestate_RNG_roster_role_eventflag_orconditional_override=True,
        initialized_source_script_fixtures_not_natural_event_activation=True,
        original_catalogue_may_select_earlier_English=True,new_editorial_English_not_yet_played=True,
        no_all_personality_paths_conditional_participation_full_route_orhardware_claim=True,new_credit=0)
    save(fixture_root/'source_actual_review.json',source_actual)
    checkpoint=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),visual_review=str(ROOT/'visual_review.json'),visual_review_sha256=sha((ROOT/'visual_review.json').read_bytes()),
        menu=str(MENU.with_name(MENU.stem+'_reviewed.json')),styles=str(STYLE),source_actual=str(fixture_root/'source_actual_review.json'),
        ordinary_speeches=260,personality_physical_alternatives=48,personality_alias_slots=64,menu_labels=15,total_prose_decisions=323,
        revised=239,retained=84,all_four_individual_prose_gates=True,formatting_gates_false_until_remaining_checks=True,
        final_speech_pages=315,initial_fresh_macro_alignment_cases=1232,refresh_alignment_cases=52,
        exact_native_reuse_without_repeating_initial_checks=True,directly_viewed_native_sheets=44,menu_review_sheets=3,
        native_style_target_slots=64,menu_provider_alignments=30,bridged_menu_returns=120,complete_menu_style_planes=60,
        page_findings_resolved=7,FE_extra_blank_rows_resolved=2,additional_phrase_findings_resolved=2,
        source_fixture_runs=2,source_fixture_frames=16502,
        pending=['Source-owned Follower178 F and Diogo43 de display fields and scoped name consistency.','Relocated complete 4100/2200/ordinary objects, original commands/relative branches, stored native planes and archive loaders.','Representative new-English gameplay for styles, three-choice menus, actor0, FE rows, pagination and transitions.','Registered cumulative release, exact clean-input patch, own startup and once-only completion credit.'],
        registered_current_candidate=doc['current_ROM'],registered_current_sha256=doc['current_ROM_sha256'],new_registered_ROM=False,new_credit=0,
        full_goal_complete=False,guide_photo_collection_discontinued=True,all_ROMs_andearlier_translations_preserved=True)
    save(target,checkpoint)
    before=LEDGER.read_bytes();ledger=load(LEDGER);assert ledger['records_editorially_completed']==8204 and not ledger['full_goal_complete']
    backup=ROOT/'ledger_before_offline_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    ledger['Hodram_B111_B130_clean_next_20261101'].update(earlier_English_unconsulted=False,earlier_English_dialogue_andchoice_labels_unconsulted=False,current_English_all323_compared=True,
        offline_checkpoint=str(target),offline_checkpoint_sha256=sha(target.read_bytes()),new_credit=0)
    ledger['Hodram_B111_B130_prose_native_research_20261101']=checkpoint
    ledger['latest_checkpoint']='B111-B130:323 contextual prose decisions (239 revisions/84 retentions),315 viewed native pages,15 menu labels and48 physical personality alternatives checked offline. Seven page boundaries,two FE blank rows andtwo phrase boundaries corrected without changing prose. Source-only actor0/three-choice fixtures observed;new English/stored/name fixes/release still pending.8204 completed;current e713/main unchanged. Full goal active;no guide photos.'
    prior=load(backup)
    for key in ['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed','current_integrated_candidate','current_native_relocation_reference','full_goal_complete']:
        assert ledger[key]==prior[key]
    allowed={'Hodram_B111_B130_clean_next_20261101','Hodram_B111_B130_prose_native_research_20261101','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    print('Saved323 prose decisions/315 directly reviewed final pages,typed objects,scoped source gameplay and pending work. Completion8204/current e713/main unchanged.')

if __name__=='__main__':main()
