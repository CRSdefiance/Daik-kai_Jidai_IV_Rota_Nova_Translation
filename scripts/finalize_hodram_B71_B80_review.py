"""Bind completed editorial/display review; completion credit still waits for release."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B71_B80_editorial_20261101')
DOC=Path('translations/hodram_B71_B80_editorial_manuscript_v1.json')
FINAL=Path('translations/hodram_B71_B80_contextual_final_review_v1.json')
ACTUAL=Path('work/analysis/Hodram_B71_B80_actual_20261101/capture_sheets.json')
STORED=Path('work/analysis/Hodram_B71_B80_stored_20261101/stored_native_verification.json')
LOADERS=Path('work/analysis/Hodram_B71_B80_loaders_20261101/verification.json')
VISUAL=ROOT/'visual_review.json'
REBUILT=Path('work/analysis/Hodram_B71_B80_rebuilt_20261101/reconstruction.json')

if __name__=='__main__':
    assert not FINAL.exists()
    doc,actual,stored,loaders,visual,rebuilt=map(load,[DOC,ACTUAL,STORED,LOADERS,VISUAL,REBUILT])
    assert len(doc['records'])==144 and doc['revised']==100 and doc['retained']==44
    assert stored['complete_stored_pages']==visual['final_pages']==154
    assert stored['fresh_relocated_native_relative_cases']==420
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert loaders['fresh_whole_archive_loads_andcache_hits']==325
    assert loaders['fresh_parent_cases']==20 and loaders['exact_reused_parent_cases']==630
    for run in actual['runs']:
        assert run['cold_boot'] and not run['savestate'] and not run['hardware_verification']
        assert sha(Path(run['capture_report']).read_bytes())==run['capture_report_sha256']
        for sheet in run['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    sheets=[sheet for run in actual['runs'] for sheet in run['review_sheets']]
    assert len(sheets)==10
    report=dict(fixtures='work/analysis/Hodram_B71_B80_fixtures_20261101/fixtures.json',
        fixtures_sha256=sha(Path('work/analysis/Hodram_B71_B80_fixtures_20261101/fixtures.json').read_bytes()),
        runs=actual['runs'],total_frames=sum(run['frames'] for run in actual['runs']),
        all_review_sheets_directly_viewed=sheets,
        scoped_observations=[
            dict(block=72,frame=3360,observed='Complete Xien Yan greeting, portrait, nameplate and default FA surname.'),
            dict(block=72,frame=7200,id='DK4_MES_B72_R0055',observed='Second page begins with the complete mainland-coast continuation, and ends with the Wako name.'),
            dict(block=72,frame=9600,id='DK4_MES_B72_R0091',observed='Four-row first page keeps the for-now clause complete. Its second page is not in this capture schedule.'),
            dict(block=72,frame=11520,observed='Maria Li portrait/nameplate and sarcasm response.'),
            dict(block=72,frame=12000,observed='Returned to town UI after the scene.'),
            dict(block=72,frame=18000,observed='Later departure/tutorial dialogue has completed and sailing UI is visible; those lines receive no new editorial credit.'),
            dict(block=76,frame=4000,id='DK4_MES_B76_R0006',observed='Complete letter notice in FE consumer with no speaker nameplate.'),
            dict(block=76,frame=4080,id='DK4_MES_B76_R0009',observed='Complete declaration-of-war notice; no speaker nameplate.'),
            dict(block=76,frame=4320,observed='Returned to town UI. The seven conditional progressive speeches were not observed in this fixture.'),
            dict(block=76,frame=7000,observed='Later Port Worker resupply prompt is intact; no new credit for it.')],
        representative_progressive_FE_pagination_andscene_transition_observed=True,
        full_two_page_pair_for_one_speech_not_claimed=True,
        no_new_blank_box_lost_glyph_orportrait_issue_seen_in_reviewed_samples=True,
        actual_pixel_backing_comparison_not_performed=True,
        unvisited='Other eight batch scenes, skipped B76 progressive branch, unsampled B72 speeches/pages and natural optional-event activation remain offline-only.',
        no_natural_event_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        repeated_A_after_scene_also_activates_following_town_tutorial_sailing_content=True,
        purpose='Focused editorial/display QA only. Guide photo collection discontinued.',new_credit=0)
    assert report['total_frames']==25002
    actual_review=ACTUAL.with_name('actual_review.json');save(actual_review,report)
    final=deepcopy(doc)
    final.update(format='dk4-editorial-final-review-v1',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'])
    bindings={r['id']:r for g in rebuilt['groups'] for r in g['text_records']}
    for row in final['records']:
        assert all(row['review'][gate] for gate in ['source','context','localization','naturalness'])
        row['review']['formatting']=True
        row['formatting_native_stored_actual_andregistered_release_pending']=False
        row['registered_release_andcompletion_credit_pending']=True
        stored_row=bindings[row['id']]
        row['planned_integrated_reference']=dict(file_path=row['file_path'],block=row['block'],
            offset=stored_row['new_offset'],record_index=stored_row['new_record_index'],
            bytes=len(bytes.fromhex(stored_row['stored_hex'])),
            exact_stored_hex=stored_row['stored_hex'],target_archive_sha256=rebuilt['target_archive_sha256'])
        row['formatting_evidence']=dict(stored=str(STORED),visual=str(VISUAL),actual=str(actual_review),
            gameplay_is_representative_not_individual_activation=True)
    final['all_individual_four_prose_gates_true_formatting_false']=False
    final['all_five_individual_review_gates_passed']=True
    final['previous_manuscript']=str(DOC);final['previous_manuscript_sha256']=sha(DOC.read_bytes())
    final['formatting_evidence']={str(p):sha(p.read_bytes()) for p in [STORED,LOADERS,VISUAL,actual_review,REBUILT]}
    final['new_credit']=0;final['registered_release_pending']=True
    validate_natural_dialogue_batch(final)
    save(FINAL,final)
    print('144 individual five-gate reviews complete;25002 representative fixture frames reviewed. Registered integration and completion credit pending.')
