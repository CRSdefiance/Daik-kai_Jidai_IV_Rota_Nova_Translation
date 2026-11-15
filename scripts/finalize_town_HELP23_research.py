"""Seal23 five-gate town-help research reviews with15 observed/13 offline-only pages explicit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v3 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')
FINAL=Path('translations/help_town23_contextual_final_review_v1.json')
if __name__=='__main__':
    assert not FINAL.exists()
    plan_path=ROOT/'refined_v2/automatic_plans_v1.json';plan=load(plan_path);input_path=Path(plan['manuscript']);doc=load(input_path)
    native_path=ROOT/'refined_native_v2/native_help_pages.json';native=load(native_path)
    visual_path=ROOT/'preview_qualification_v2/direct_visual_approval.json';visual=load(visual_path)
    actual_path=ROOT/'focused_navigation_checked_v1/ordinary_gameplay_verification.json';actual=load(actual_path)
    assert native['native_pages']==28 and (native['fresh_pages'],native['exact_reused_pages'])==(10,18)
    assert visual['all28_complete_pages_approved'] and actual['all_selected_complete_actual_pages_andnative_child_targets_pass']
    assert (actual['actual_pages'],actual['actual_articles'],actual['offline_only_pages'])==(15,10,13)
    assert len(actual['original_forward_back_andL_R_history_returns'])==6 and len(actual['readable_actual_sheets'])==4
    assert all(r['complete_title_andbody_RGB_equal'] for r in actual['original_forward_back_andL_R_history_returns'])
    for sheet in actual['readable_actual_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    approval_path=ROOT/'focused_navigation_checked_v1/direct_actual_visual_approval.json';assert not approval_path.exists()
    save(approval_path,dict(actual_proof=str(actual_path),actual_proof_sha256=sha(actual_path.read_bytes()),
        all_four_actual_sheets_directly_viewed=True,all15_observed_pages_approved=True,sheets=actual['readable_actual_sheets'],
        all_five_two_page_cases_two_row_heading_bottom_links_andoriginal_returns_observed=True,
        Inn_B_phrase_andSquare_Trends_wording_observed_in_Help_not_new_town_command_activation=True,
        full_story_playthrough=False,hardware=False,guide_photos=False,new_credit=0))
    resource=Path(plan['research_resource']).read_bytes();blocks=IlnkContainer.parse(resource).blocks
    native_rows={r['topic_id']:r for r in native['records']};actual_rows={r['topic_id']:r for r in actual['actual_HELP_cases']};records=[]
    for old in doc['records']:
        row=deepcopy(old);assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        row['review']['formatting']=True;row['fresh_display_allocation_widgets_andintegration_pending']=False
        row['registered_integration_pending']=True;row['planned_stored_pages']=[];samples=[]
        for page in [p for p in plan['pages'] if p['source_article_id']==row['topic_id']]:
            t=page['topic_id'];raw=bytes.fromhex(page['encoded_hex']);at=int.from_bytes(resource[8+4*t:12+4*t],'little')
            assert resource[at:at+len(raw)]==raw==blocks[t] and native_rows[t]['encoded_hex']==raw.hex()
            ref=dict(file_path=doc['file_path'],block=t,archive_offset=at,bytes=len(raw),offset_table_slot=8+4*t,
                exact_stored_hex=raw.hex(),target_archive_sha256=sha(resource),native_preview=native_rows[t]['preview'],native_preview_sha256=native_rows[t]['preview_sha256'])
            if t in actual_rows:
                case=actual_rows[t];assert case['all_first_internal_final_glyphs_andblank_gaps_exact'];samples.append(case)
                ref.update(actual_frame=case['frame'],actual_capture=case['capture'],actual_capture_sha256=case['capture_sha256'])
            row['planned_stored_pages'].append(ref)
        row['actual_source_bound_samples']=samples;row['actual_gameplay']=bool(samples);row['offline_only']=not bool(samples)
        row['formatting_note']='Complete41-cell logical wrapping/252px Help width,ten rows,current y+1 ASCII ink. Semantic paragraphs keep tips,letter instructions and100-percent exceptions whole. Continuation headings omit repeated caller context while first-page headings retain it. No shortened body prose ormanual line breaks. Exact-byte/runtime proof reuse isexplicit;all28 pages directly viewed.'
        records.append(row)
    assert len(records)==23 and sum(r['offline_only'] for r in records)==13
    final={k:v for k,v in doc.items() if k!='records'}
    final.update(format='dk4-town-help23-contextual-final-review-v1',records=records,records_count=23,
        review_gates=['source','context','localization','naturalness','formatting'],all23_individual_five_gates_pass=True,
        all_fifth_gates_pending=False,proposed_revisions=19,justified_retentions=4,
        native_andvisually_approved_pages=28,initial_pages29_preserved_after_six_display_refinements=True,
        fresh_native_pages=10,exact_reused_native_pages=18,actual_pages=15,actual_articles=10,offline_only_pages=13,offline_only_articles=13,
        actual_ordinary_coldboot_frames=31641,all_five_continuation_cases_andL_R_returns_observed=True,
        registered_parent_still_pending=True,registered_integration_pending=True,new_credit=0,full_goal_complete=False,guide_photos=False,
        previous_manuscript=str(input_path),previous_manuscript_sha256=sha(input_path.read_bytes()))
    for p in [plan_path,input_path,native_path,visual_path,actual_path,approval_path,Path(__file__)]:final['evidence'][str(p)]=sha(p.read_bytes())
    image=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    encoded,production=plan_articles(final,clean.read_file(file),base.read_file(file),image.read_file(file))
    assert encoded==resource and production['pages']==plan['pages'] and production['formatting_gate_required']
    save(FINAL,final);save(ROOT/'production_plan_v1.json',dict(**production,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        research_resource=plan['research_resource'],all_native_visual_andactual_bytes_unchanged=True,registered_parent_andintegration_pending=True,new_credit=0))
    print('23 town Help reviews sealed:19 revisions/4 retentions,28 native/viewed pages,15 observed/13 offline-only. All five gates pass;parent release/integration andcredit remain pending.')
