"""Seal all67 individual reviews after full native/visual and focused actual pagination checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.reviewed_help_pages_v16 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Remaining_HELP67_formatting_20261105')
FINAL=Path('translations/help_remaining67_contextual_final_review_v1.json')

if __name__=='__main__':
    assert not FINAL.exists() and not (ROOT/'production_plan_v1.json').exists()
    paths=[ROOT/'refined_v3/automatic_plans_v1.json',ROOT/'native_pages_v3/native_help_pages.json',
        ROOT/'preview_qualification_v3/direct_visual_approval.json',ROOT/'focused_navigation_checked_v1/ordinary_gameplay_verification.json']
    plan,native,visual,actual=map(load,paths)
    assert native['plan_sha256']==sha(paths[0].read_bytes()) and visual['native_proof_sha256']==sha(paths[1].read_bytes())
    assert visual['all72_pages_approved'] and native['native_pages']==72
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass'] and native['all_executed_current_instruction_bytes_exact']
    assert (actual['actual_pages'],actual['actual_articles'],actual['offline_only_pages'])==(25,20,47)
    assert len(actual['original_forward_back_andL_R_history_returns'])==15 and len(actual['readable_actual_sheets'])==7
    assert actual['all_selected_complete_actual_pages_andnative_child_targets_pass'] and actual['actual_ordinary_controls_no_state_injection']
    assert not actual['full_story_playthrough'] and not actual['hardware'] and actual['cold_boot_frames']==42361
    for sheet in actual['readable_actual_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    approval=ROOT/'focused_navigation_checked_v1/direct_actual_visual_approval.json';assert not approval.exists()
    save(approval,dict(actual_proof=str(paths[3]),actual_proof_sha256=sha(paths[3].read_bytes()),all_seven_actual_sheets_directly_viewed=True,
        all25_observed_pages_approved=True,all_five_continuation_cases_and15_history_returns_observed=True,
        remaining47_articles_pages_offline_only=True,new_credit=0))
    doc=deepcopy(load(plan['manuscript']));resource=Path(plan['research_resource']).read_bytes();cases={r['topic_id']:r for r in actual['actual_HELP_cases']}
    for row in doc['records']:
        row['review']['formatting']=True;row['fresh_display_gates_pending']=False;row['offline_only']=row['topic_id'] in actual['offline_only_article_IDs']
        row['planned_stored_pages']=[]
        for page in [p for p in plan['pages'] if p['source_article_id']==row['topic_id']]:
            t=page['topic_id'];nr=next(r for r in native['records'] if r['topic_id']==t)
            raw=bytes.fromhex(page['encoded_hex']);at=int.from_bytes(resource[8+4*t:12+4*t],'little')
            assert nr['encoded_hex']==raw.hex() and resource[at:at+len(raw)]==raw
            ref=dict(file_path=doc['file_path'],block=t,archive_offset=at,bytes=len(raw),offset_table_slot=8+4*t,
                exact_stored_hex=raw.hex(),target_archive_sha256=sha(resource),native_preview=nr['preview'],native_preview_sha256=nr['preview_sha256'])
            if t in cases:
                ar=cases[t];assert ar['all_first_internal_final_glyphs_andblank_gaps_exact'] and not row['offline_only']
                ref.update(actual_frame=ar['frame'],actual_capture=ar['capture'],actual_capture_sha256=ar['capture_sha256'])
            else:assert row['offline_only']
            row['planned_stored_pages'].append(ref)
    assert len(doc['records'])==67 and sum(r['decision']=='revision' for r in doc['records'])==7 and sum(r['offline_only'] for r in doc['records'])==47
    doc.update(format='dk4-remaining-help67-contextual-final-review-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all67_individual_five_gates_pass=True,all_fifth_gates_pending=False,all67_fresh_formatting_native_visual_andregistered_integration_pending=False,
        native_andvisually_approved_pages=72,initial_fresh_native_pages=72,final_refined_fresh_native_pages=9,final_exact_reused_native_pages=63,
        nine_phrase_tail_refinements_resolved=True,actual_pages=25,actual_articles=20,offline_only_pages=47,offline_only_articles=47,
        actual_ordinary_coldboot_frames=42361,all15_history_returns_observed=True,registered_integration_pending=True,
        new_credit=0,full_goal_complete=False,guide_photos=False)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [*paths,approval,Path(__file__),Path('dk4tool/dialogue/reviewed_help_pages_v16.py')]})
    clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');parent=NdsImage.open(doc['current_ROM']);file=doc['file_path']
    result,compiled=plan_articles(doc,clean.read_file(file),base.read_file(file),parent.read_file(file))
    assert result==resource and compiled['pages']==plan['pages'] and all(all(r['review'].values()) for r in doc['records'])
    save(FINAL,doc);save(ROOT/'production_plan_v1.json',dict(**compiled,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        research_resource=plan['research_resource'],current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        all_source_native_actual_oroffline_visual_andindividual_five_gates_bound=True,registered_integration_pending=True,new_credit=0))
    print('67 five-gate research reviews:7 revisions/60 retentions,72 native/viewed pages,25 actual/47 offline pages and15 returns. Registered integration pending;zero credit.')
