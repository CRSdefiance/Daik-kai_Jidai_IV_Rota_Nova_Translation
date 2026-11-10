"""Seal23 individual five-gate research reviews only after all25 native/actual pages areviewed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
FINAL=Path('translations/help_early23_contextual_final_review_v1.json')
if __name__=='__main__':
    assert not FINAL.exists()
    plan_path=ROOT/'automatic_plans_v1.json';plan=load(plan_path);draft_path=Path(plan['manuscript']);draft=load(draft_path)
    native_path=ROOT/'native_pages_v2/native_help_pages.json';native=load(native_path)
    visual_path=ROOT/'preview_qualification_v1/direct_visual_approval.json';visual=load(visual_path)
    actual_path=ROOT/'ordinary_navigation_checked_v2/ordinary_gameplay_verification.json';actual=load(actual_path)
    assert actual['all25_complete_actual_pages_andnative_child_targets_pass'] and len(actual['original_forward_back_andL_R_history_returns'])==3
    assert native['native_pages']==25 and visual['all25_complete_pages_approved']
    assert len(actual['readable_actual_sheets'])==7 and actual['actual_ordinary_controls_no_state_injection']
    # This producer isexecuted only after the seven recorded actual sheets havebeen directly viewed.
    for sheet in actual['readable_actual_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    approval_path=ROOT/'ordinary_navigation_checked_v2/direct_actual_visual_approval.json'
    assert not approval_path.exists()
    save(approval_path,dict(actual_proof=str(actual_path),actual_proof_sha256=sha(actual_path.read_bytes()),
        all_seven_readable_actual_sheets_directly_viewed=True,sheets=actual['readable_actual_sheets'],all25_complete_pages_approved=True,
        findings='All complete text andlinks readable. Full-width Help layout,benefit paragraph continuity,numeric conditions,bottom-row links andboth continuation returns acceptable. No prose shortening ornew manual wrapping.',
        actual_ordinary_cold_boot=True,hardware=False,guide_photos=False,new_credit=0))
    release_path=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/registered_release_verification.json');release=load(release_path)
    image=NdsImage.open(release['candidate']);clean=NdsImage.open('work/clean.nds');baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256'] and not release['own_registered_startup_pending']
    resource=Path(plan['research_resource']).read_bytes();blocks=IlnkContainer.parse(resource).blocks;records=[]
    for old in draft['records']:
        row=deepcopy(old);topic=row['topic_id'];pages=[p for p in plan['pages'] if p['source_article_id']==topic]
        assert len(pages) in [1,2] and all(row['review'][g] is True for g in ['source','context','localization','naturalness'])
        row['review']['formatting']=True;row['fresh_native_font_links_rows_bounds_allocation_pagination_andvisual_checks_pending']=False
        row['metric_UI_Influence_versus_COMMON_Power_binding_pending']=False
        row['actual_gameplay']=True
        row['actual_gameplay_scope']='Ordinary cold-boot title-menu Help navigation;not a story playthrough orhardware test.'
        row['planned_stored_pages']=[]
        for page in pages:
            t=page['topic_id'];raw=bytes.fromhex(page['encoded_hex']);offset=int.from_bytes(resource[8+4*t:12+4*t],'little')
            assert resource[offset:offset+len(raw)]==raw==blocks[t]
            a=next(c for c in actual['actual_HELP_cases'] if c['topic_id']==t)
            n=next(c for c in native['records'] if c['topic_id']==t)
            assert n['encoded_hex']==page['encoded_hex'] and a['source_article_id']==topic
            row['planned_stored_pages'].append(dict(file_path=draft['file_path'],block=t,archive_offset=offset,bytes=len(raw),
                offset_table_slot=8+4*t,exact_stored_hex=raw.hex(),target_archive_sha256=sha(resource),
                native_preview=n['preview'],native_preview_sha256=n['preview_sha256'],actual_capture=a['capture'],
                actual_capture_sha256=a['capture_sha256'],actual_frame=a['frame']))
        row['formatting_note']='Logical paragraphs;compiler-owned41-cell planning/252px native Help width,ten rows,complete ASCII ink at y+1 andnative16px display row pitch. Original binary links,complete first/final glyphs,blank gaps andactual targets pass. Source numbered-benefit paragraphs staytogether with documented continuation ownership.'
        records.append(row)
    final=dict(format='dk4-source-contextual-early-help23-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path=draft['file_path'],formatting_owned_by_compiler=True,not_a_release_batch=True,
        source_clean_HELP_sha256=draft['source_clean_HELP_sha256'],source_canonical_HELP_sha256=draft['source_canonical_HELP_sha256'],
        source_current_HELP_sha256=draft['source_current_HELP_sha256'],current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],
        comparison_ROM=draft['current_ROM'],comparison_ROM_sha256=draft['current_ROM_sha256'],
        current_HELP_exact_to_compared_archive=True,records=records,records_count=23,proposed_revisions=16,justified_retentions=7,
        source_topic_count=202,current_topic_count=211,target_topic_count=212,review_gates=['source','context','localization','naturalness','formatting'],
        all23_individual_five_gates_pass=True,native_andactual_pages=25,actual_ordinary_coldboot_frames=actual['cold_boot_frames'],
        retained_existing_Rafael202_andnew_Hodram211_continuations=True,unowned_topics203_to210_exact=True,
        previous_manuscript=str(draft_path),previous_manuscript_sha256=sha(draft_path.read_bytes()),
        registered_integration_pending=True,new_credit=0,full_goal_complete=False,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [plan_path,draft_path,native_path,visual_path,actual_path,approval_path,release_path,Path(__file__)]})
    encoded,production=plan_articles(final,clean.read_file(final['file_path']),baseline.read_file(final['file_path']),image.read_file(final['file_path']))
    assert encoded==resource and production['formatting_gate_required'] and production['pages']==plan['pages']
    assert len(records)==23 and all(all(r['review'].values()) for r in records)
    save(FINAL,final);save(ROOT/'production_plan_v1.json',dict(**production,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        research_resource=plan['research_resource'],all_native_andactual_page_bytes_unchanged_since_direct_review=True,
        registered_release_pending=True,new_credit=0))
    print('23 five-gate Help research reviews/25 native andactual pages sealed:16 revisions/7 retentions. Production bytes exact toreviewed resource;registered integration remains.')
