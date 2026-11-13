"""Record directly viewed B52 speech and English menu planes without premature formatting approval."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_native_review_v8637')
OLD=Path('translations/hodram_B52_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B52_editorial_manuscript_v2.json')
PAGES=Path('work/analysis/Hodram_B52_pages_v8635/compiled_native_pages.json')
MENU=Path('work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json')
REASONS={
    6:'Two automatically generated rows use the full216px native width. Are you planning to make an enemy / of Hayreddin\'s outfit? is a readable ordinary word boundary joining the noun enemy to its of phrase across rows. The next word of does not fit the current first row with the following phrase under the unchanged automatic planner. All words, the apostrophe and final question mark are complete; no shortened prose, authored break, padding or viewport narrowing is used.',
    21:'The retained complete sentence occupies one35-cell row inside the original216px width. Every first/internal/final glyph and final period is complete. Its source two-row to English one-row difference remains the original line-count info; there is no blank or extra page and no word was removed for fit.',
    33:'The revised complete comment fits one native row, including the leading Y, contraction apostrophe, comma and final question mark. Its casual commenting cadence remains intact; the glyph proof does not assert an actual branch visit.',
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,pages,menu=map(read,[OLD,PAGES,MENU]);planpath=Path(pages['plan']);plan=read(planpath)
    assert pages['manuscript_sha256']==menu['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes()) and pages['plan_sha256']==sha(planpath.read_bytes())
    assert len(pages['records'])==3 and len(menu['records'])==8 and menu['current_width_px']==84 and menu['reviewed_width_px']==72
    assert menu['current_rectangle']==[70,64,186,128] and menu['reviewed_rectangle']==[76,64,180,128]
    for proof in [pages,menu]:
        sheet=proof['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rows=[];infos=[]
    for original,p,n in zip(old['records'],plan['records'],pages['records'],strict=True):
        assert original['id']==p['id']==n['id'] and original['english']==n['logical_English']==' '.join(p['lines']) and len(n['pages'])==1
        assert not original['review']['formatting']
        for page in n['pages']:
            for key in ['native_plane','preview']:assert sha(Path(page[key]).read_bytes())==page[key+'_sha256']
        for issue in p['base_QA']['issues']:
            assert issue['severity']=='info' and issue['code']=='line-break-count';infos.append(dict(id=original['id'],issue=issue))
        row=deepcopy(original);row.update(compiled_hex=p['encoded_hex'],compiled_bytes=len(bytes.fromhex(p['encoded_hex'])),formatted_markup=p['formatted_markup'],planned_English_markup=p['planning_record']['english'],generated_lines=p['lines'],expected_native_pages=1,qa_waivers=[],qa_waiver_scope=[],native_body_review_reason=REASONS[row['source_record_index']],native_body_review_proof=str(PAGES),native_body_review_proof_sha256=sha(PAGES.read_bytes()),compiled_native_body_review=deepcopy(n),all_stored_controls_actual_branch_context_headers_policy_andregistered_release_pending=True)
        assert all(row[k]==original[k] for k in ['english','source_hex','current_hex','source_reference','current_reference','review','decision','retention_reason','localization_note']);rows.append(row)
    assert len(infos)==1 and infos[0]['id']=='DK4_MES_B52_R0021'
    choices=[]
    for original in old['typed_choice_records']:
        row=deepcopy(original);index=row['option_index'];planes=[r for r in menu['records'] if r['version']=='reviewed-stored-English' and r['option_index']==index]
        assert len(planes)==2 and {r['style'] for r in planes}=={1,15}
        assert all(r['text']==row['english'] and r['visible_cell_center_twice']==r['logical_width_px']==72 and sha(Path(r['native_plane']).read_bytes())==r['native_plane_sha256'] for r in planes)
        row.update(compiled_choice_label_hex=row['english'].encode('ascii').hex(),compiled_choice_object=menu['compiled_choice_object'],compiled_choice_object_sha256=menu['compiled_choice_object_sha256'],native_choice_style_planes=deepcopy(planes),native_choice_review_proof=str(MENU),native_choice_review_proof_sha256=sha(MENU.read_bytes()),native_choice_review_reason='Retained words and punctuation are complete and centered in both style1/style15 planes at the measured72px menu width. The old84px menu included three storage-only spaces in option0; removing those changes geometry without changing either editorial label. Actual backing/highlight/controller choices andnormal/flagged end transitions remain required.',all_stored_choice_references_branch_extents_actual_backing_controller_policy_andregistered_release_pending=True)
        assert all(row[k]==original[k] for k in ['english','source_hex','current_hex','source_reference','current_reference','review','decision','retention_reason','localization_note']);choices.append(row)
    doc=deepcopy(old);doc.update(records=rows,typed_choice_records=choices,predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),compiled_plan=str(planpath),compiled_plan_sha256=sha(planpath.read_bytes()),native_body_pages=str(PAGES),native_body_pages_sha256=sha(PAGES.read_bytes()),native_choice_proof=str(MENU),native_choice_proof_sha256=sha(MENU.read_bytes()),all_three_complete_native_body_pages_andfour_current_target_menu_caption_examples_directly_viewed=True,all_five_formatting_gates_still_false=True,one_original_line_count_info_zero_warnings_waivers=True,menu_geometry_risk=dict(current_width_px=84,reviewed_width_px=72,current_rectangle=menu['current_rectangle'],reviewed_rectangle=menu['reviewed_rectangle'],source_of_change='three unspoken option0 storage spaces removed; both choice words retained',actual_geometry_highlight_controller_andboth_distinct_end_paths_still_pending=True),status='contextual-prose-compiled-native-bodies-English-choice-planes-reviewed-relocation-stored-actual-policy-release-pending')
    save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'native_body_andchoice_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),directly_viewed_speech_sheet=pages['review_sheet'],directly_viewed_menu_sheet=menu['review_sheet'],reviewed_body_pages=3,fresh_logical_alignment_cases=12,fresh_compiled_alignment_cases=12,reviewed_current_target_English_menu_styleplanes=8,individual_body_reviews=[dict(id=r['id'],reason=r['native_body_review_reason'],generated_lines=r['generated_lines'],compiled_hex=r['compiled_hex']) for r in rows],individual_choice_reviews=[dict(id=r['id'],reason=r['native_choice_review_reason']) for r in choices],original_infos=infos,original_warnings=[],original_QA_not_suppressed=True,no_qa_waivers=True,all_approved_words_source_current_refs_individual_reasons_andreview_gates_preserved=True,full216px_width_font_metrics_pagination_andguard_rules_unchanged=True,measured_menu_width84_to72_actual_geometry_risk_preserved=True,body_menu_preview_not_actual_nameplates_controller_branch_transitions_ornatural_activation=True,all_five_formatting_gates_false=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,DOC,PAGES,MENU,planpath,Path(__file__)]}))
    print('B52 native review:3complete speech pages/8English menu styleplanes directly viewed; one original info,zero warnings/waivers. Manuscriptv2 keeps all prose/refs/gates; changed-menu actual tests andremaining release work pending.')
