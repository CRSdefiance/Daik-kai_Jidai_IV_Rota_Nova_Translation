"""Seal Deck Help30 after all native and actual pages have been directly viewed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.reviewed_help_pages_v10 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T103_T132_formatting_20261104')
FINAL=Path('translations/help_deck30_contextual_final_review_v1.json')

if __name__=='__main__':
    assert not FINAL.exists()and not(ROOT/'production_plan_v1.json').exists()
    plan_path=ROOT/'refined_v3/automatic_plans_v1.json';native_path=ROOT/'native_pages_v1/native_help_pages.json'
    visual_path=ROOT/'preview_qualification_v1/direct_visual_approval.json'
    actual_path=ROOT/'focused_navigation_checked_v1/ordinary_gameplay_verification.json'
    plan,native,visual,actual=map(load,[plan_path,native_path,visual_path,actual_path])
    assert len(plan['pages'])==native['native_pages']==native['complete_articles']==30
    assert native['plan_sha256']==sha(plan_path.read_bytes())and visual['native_proof_sha256']==sha(native_path.read_bytes())
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']and native['all_executed_current_instruction_bytes_exact']
    assert visual['all30_complete_pages_approved']and visual['all_eight_sheets_directly_viewed']
    assert actual['actual_pages']==actual['actual_articles']==30 and actual['offline_only_pages']==0 and not actual['offline_only_article_IDs']
    assert actual['cold_boot_frames']==36601 and len(actual['original_forward_back_andL_R_history_returns'])==25
    assert actual['all_selected_complete_actual_pages_andnative_child_targets_pass']and len(actual['readable_actual_sheets'])==8
    assert actual['actual_ordinary_controls_no_state_injection']and not actual['full_story_playthrough']and not actual['hardware']
    for sheet in actual['readable_actual_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    actual_visual_path=ROOT/'focused_navigation_checked_v1/direct_actual_visual_approval.json';assert not actual_visual_path.exists()
    save(actual_visual_path,dict(actual_proof=str(actual_path),actual_proof_sha256=sha(actual_path.read_bytes()),
        all_eight_actual_sheets_directly_viewed=True,all30_observed_pages_approved=True,sheets=actual['readable_actual_sheets'],
        all30_single_page_articles_sixteen_link_hub_and25_history_returns_observed=True,
        corrected_Y_Crew_instruction_observed_in_Help_andseparately_in_actual_Deck_control_probe=True,
        no_hardware_orfull_story_orordinary_Rafael_progress_claim=True,new_credit=0))
    doc=deepcopy(load(plan['manuscript']));image=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    file=doc['file_path'];resource=Path(plan['research_resource']).read_bytes()
    for row in doc['records']:
        row['review']['formatting']=True;row['offline_only']=False;row['registered_integration_pending']=True
        row['fresh_display_allocation_widgets_andintegration_pending']=False;row['all_fresh_display_gates_pending']=False
        row['planned_stored_pages']=[]
        for page in[p for p in plan['pages']if p['source_article_id']==row['topic_id']]:
            t=page['topic_id'];nr=next(r for r in native['records']if r['topic_id']==t);ar=next(r for r in actual['actual_HELP_cases']if r['topic_id']==t)
            raw=bytes.fromhex(page['encoded_hex']);at=int.from_bytes(resource[8+4*t:12+4*t],'little')
            assert nr['encoded_hex']==page['encoded_hex']and resource[at:at+len(raw)]==raw and ar['all_first_internal_final_glyphs_andblank_gaps_exact']
            row['planned_stored_pages'].append(dict(file_path=file,block=t,archive_offset=at,bytes=len(raw),offset_table_slot=8+4*t,
                exact_stored_hex=raw.hex(),target_archive_sha256=sha(resource),native_preview=nr['preview'],native_preview_sha256=nr['preview_sha256'],
                actual_frame=ar['frame'],actual_capture=ar['capture'],actual_capture_sha256=ar['capture_sha256']))
    assert len(doc['records'])==30 and sum(r['decision']=='revision'for r in doc['records'])==13
    doc.update(format='dk4-deck-help30-contextual-final-review-v1',records_count=30,
        review_gates=['source','context','localization','naturalness','formatting'],all30_individual_five_gates_pass=True,all_fifth_gates_pending=False,
        native_andvisually_approved_pages=30,fresh_native_pages=30,exact_reused_native_pages=0,actual_pages=30,actual_articles=30,offline_only_pages=0,offline_only_articles=0,
        actual_ordinary_coldboot_frames=36601,all25_history_returns_observed=True,registered_parent_still_pending=True,registered_integration_pending=True,
        no_new_pagination_cases=True,all30_single_pages_all_prose_retained_through_wrap_refinements=True,guide_photos=False,new_credit=0,full_goal_complete=False)
    evidence=[plan_path,native_path,visual_path,actual_path,actual_visual_path,Path(__file__),
        Path('work/analysis/Shared_HELP_T103_T132_clean_20261104/native_roles_rooms_andskills_v1.json'),
        Path('work/analysis/HELP103_104_106_current_controls_20261104/control_binding_v1.json')]
    doc['evidence'].update({str(p):sha(p.read_bytes())for p in evidence})
    compiled_resource,compiled=plan_articles(doc,clean.read_file(file),base.read_file(file),image.read_file(file))
    assert compiled_resource==resource and compiled['pages']==plan['pages']
    save(FINAL,doc)
    save(ROOT/'production_plan_v1.json',dict(**compiled,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        research_resource=plan['research_resource'],current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        all_source_native_actual_visual_andindividual_five_gates_bound=True,registered_integration_pending=True,new_credit=0))
    print('Deck Help30 research complete:13 revisions/17 exact-body retentions,all30 native/viewed/observed pages and25 returns. Registered integration pending; no credit.')
