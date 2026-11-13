"""Bind all253 final body pages andfour menu captions to exact viewed native evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')

if __name__=='__main__':
    out=ROOT/'body_display_approval_v4.json';combined=ROOT/'combined_native_v4.json'
    assert not out.exists() and not combined.exists()
    base_path=ROOT/'combined_native_v3.json';fresh_path=ROOT/'speech_native_delta_v4/compiled_native_pages.json'
    plans_path=ROOT/'automatic_v4/automatic_plans.json';initial_path=ROOT/'speech_native_v1/compiled_native_pages.json'
    first_delta_path=ROOT/'speech_native_delta_v3/compiled_native_pages.json';choices_path=ROOT/'two_choices_native_v1/complete_choice_objects.json'
    base,fresh,plans,initial,delta,choices=map(load,[base_path,fresh_path,plans_path,initial_path,first_delta_path,choices_path])
    assert base['runtime']==fresh['runtime']==initial['runtime']==delta['runtime']
    rows={r['id']:deepcopy(r) for r in base['records']};rows.update({r['id']:r for r in fresh['records']})
    assert len(rows)==245 and len(fresh['records'])==2 and fresh['pages']==4
    assert all(rows[r['id']]['compiled_hex']==r['encoded_hex'] and rows[r['id']]['logical_English']==r['logical_English'] for r in plans['records'])
    assert not plans['failures'] and not any(i['severity'] in ['error','warning'] for r in plans['records'] for i in r['base_QA']['issues'])
    assert sum(r['expected_native_pages'] for r in plans['records'])==253
    reviewed=[*initial['review_sheets'],*delta['review_sheets'],*fresh['review_sheets'],*[o['review_sheet'] for o in choices['objects']]]
    assert len(initial['review_sheets'])==25 and len(delta['review_sheets'])==9 and len(fresh['review_sheets'])==1
    for sheet in reviewed:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    result=deepcopy(base);result.update(records=[rows[r['id']] for r in plans['records']],
        plan=str(plans_path),plan_sha256=sha(plans_path.read_bytes()),pages=253,
        direct_visual_review_pending=False,two_new_page_boundary_findings_pending=False,
        final_exact_native_record_sources=dict(original=207,first_refresh=36,last_refresh=2),
        source_native_receipts={str(p):sha(p.read_bytes()) for p in [base_path,fresh_path,plans_path,initial_path,first_delta_path,Path(__file__)]})
    save(combined,result)
    name_path=Path('work/analysis/Rafael_Fernan_name_native_20261104/native_name_fields_verification.json');name=load(name_path)
    assert len(name['planes'])==4 and len(name['negative_cases_rejected'])==8 and name['original_progressive_andfull_name_getters_pass']
    assert sha(Path(name['review_sheet']['path']).read_bytes())==name['review_sheet']['sha256']
    save(out,dict(final_native=str(combined),final_native_sha256=sha(combined.read_bytes()),final_plan=str(plans_path),
        final_plan_sha256=sha(plans_path.read_bytes()),body_records=245,body_pages=253,
        all_initial253_andall42_first_refresh_andall4_last_refresh_pages_directly_viewed=True,
        final_253_pages_have_exact_native_glyphs_bounds_controls_substitutions_consumption_pagination_andvisual_approval=True,
        all_reviewed_sheets=reviewed,logical_prose_unchanged_across_layout_revisions=True,
        changed_layout_records=38,final_refresh_only_records=2,unchanged_native_record_reuses=207,
        ordinary_width216_andFE_width228_andfour_rows_andaccepted_runtime_andfont_unchanged=True,
        phrasal_verb_boundary_retention=dict(id='DK4_MES_B56_R0077',line='The whole town chipped in,',
            reason='Chipped in is a complete phrasal verb;the reviewed line isnot an unattached-preposition error.Original QA warning remains archived andonly this exact bound line isretained.'),
        menus=dict(receipt=str(choices_path),receipt_sha256=sha(choices_path.read_bytes()),objects=2,captions=4,
            complete_style_planes=16,native_provider_alignments=12,bridged_modal_returns=36,negative_compiler_cases=14,
            both_caption_sheets_directly_viewed=True,actual_controller=False),
        Fernan_field=dict(native=str(name_path),native_sha256=sha(name_path.read_bytes()),all4_current_andproposed_planes_directly_viewed=True,
            all8_negative_cases_pass=True,spelling_unchanged_only_fullwidth_F_corrected=True,
            registered_deployment_pending=True,latest_4b10fd67_parent_rebase_pending=True),
        actual_gameplay=False,all249_records_live_unvisited=True,
        source_header_localization_fields_storage_transitions_representative_gameplay_andregistered_release_still_pending=True,
        all_individual_fifth_gates_remain_false_until_remaining_scope_passes=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Approved253 final native body pages/4 menu captions;38 layout fixes/3 I fixes and4 viewed Fernan glyph planes;stored/headers/gameplay remain.')
