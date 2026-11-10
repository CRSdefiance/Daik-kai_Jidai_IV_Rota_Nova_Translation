"""Close individual formatting gates after offline/stored/focused actual checks; release pending."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B81_B89_editorial_20261101')
DOC=Path('translations/hodram_B81_B89_editorial_manuscript_v2.json')
FINAL=Path('translations/hodram_B81_B89_contextual_final_review_v1.json')
REBUILT=Path('work/analysis/Hodram_B81_B89_rebuild_20261101/reconstruction.json')
STORED=Path('work/analysis/Hodram_B81_B89_stored_20261101/stored_native_verification.json')
LOADERS=Path('work/analysis/Hodram_B81_B89_loaders_20261101/verification.json')
VISUAL=ROOT/'visual_review.json'
MENU=Path('work/analysis/Hodram_B87_menu_20261101/menu_provider_and_planes_reviewed.json')
NAME=Path('work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification_reviewed.json')
PIXELS=Path('work/analysis/Hodram_B81_B89_actual_pixels_20261101d/focused_actual_pixels.json')
SHEETS=[Path('work/analysis/Hodram_B81_B89_actual_20261101/capture_sheets.json'),Path('work/analysis/Hodram_B87_decline_actual_20261101/capture_sheets.json')]
LEDGER=Path('translations/editorial_review_current_v1.json')

if __name__=='__main__':
    assert not FINAL.exists()
    doc,rebuilt,stored,loaders,visual,menu,name,pixels=map(load,[DOC,REBUILT,STORED,LOADERS,VISUAL,MENU,NAME,PIXELS])
    assert len(doc['records'])==306 and doc['revised']==222 and doc['retained']==84
    assert stored['complete_stored_pages']==visual['pages']==306
    assert stored['fresh_relocated_native_relative_cases']==140 and stored['typed_labels_checked']==2
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert loaders['fresh_whole_archive_loads_andcache_hits']==325 and loaders['fresh_parent_cases']==18 and loaders['exact_reused_parent_cases']==632
    assert menu['offline_visual_approved'] and name['offline_visual_approved']
    assert len(pixels['name_headers'])==7 and len(pixels['menu_samples'])==7 and len(pixels['rejection_pages'])==2
    runs=[run for path in SHEETS for run in load(path)['runs']]
    sheets=[s for run in runs for s in run['review_sheets']]
    assert len(runs)==4 and len(sheets)==20 and sum(r['frames'] for r in runs)==41004
    for run in runs:
        assert run['cold_boot'] and not run['savestate'] and not run['hardware_verification']
        assert sha(Path(run['capture_report']).read_bytes())==run['capture_report_sha256']
        for sheet in run['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    # Every sheet was directly opened. Repeated holds are reused only through
    # the source-bound same-run lower-RGB maps, not inferred textual similarity.
    actual_path=ROOT/'actual_review.json'
    prior_FE=Path('work/analysis/Hodram_B71_B80_actual_20261101/actual_review.json')
    assert load(prior_FE)['representative_progressive_FE_pagination_andscene_transition_observed']
    actual=dict(fixtures='work/analysis/Hodram_B81_B89_fixtures_20261101/fixtures.json',runs=runs,total_frames=41004,
        all_review_sheets_directly_viewed=sheets,focused_actual_pixels=str(PIXELS),focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        scoped_observations=[
            dict(block=84,frame=4320,observed='Revised opportunity/invitation is two complete natural rows.'),
            dict(block=84,frames=[6720,7200,11520,12240,12720,13200,13680],observed='Seven complete corrected Emilio Ferog headers match native font masks, including normal F and final g.'),
            dict(block=84,frame=14160,observed='Emilio Ferog joined notice uses the corrected name; visually checked, no separate notice pixel-mask claim.'),
            dict(block=84,frame=14400,observed='Returned to port/town UI.'),
            dict(block=85,frames=[4800,5040],id='DK4_MES_B85_R0018',observed='Both complete rejection pages match native glyph planes; final statement begins coherently on page2.'),
            dict(block=87,frame=5520,observed='Both complete translated menu captions fit the constructor-sized popup.'),
            dict(block=87,frames=[5760,6960,8880,9120,9360],observed='Agreement leads to repair thanks, later full introduction/join notice/Refit advice, then port UI.'),
            dict(block=87,run='decline',frames=[5500,5620],observed='Original highlight moves from agreement to refusal using ordinary DOWN; all14 sampled caption masks/backgrounds pass.'),
            dict(block=87,run='decline',frames=[5720,6240],observed='Ordinary A selects refusal; Janus says he will try someone else, then returns to port UI.')],
        representative_progressive_pagination_menu_name_andscene_transition_observed=True,
        FE_new_batch_bodies_not_observed_in_gameplay=True,
        FE_distinct_behavior_reference=str(prior_FE),FE_distinct_behavior_reference_sha256=sha(prior_FE.read_bytes()),
        FE_reuse_basis='The registered right-bound renderer, font, consumer ABI andgeometry are unchanged. The research ARM9 differs only by the exclusively owned eight-byte actor14 name slot; complete inverse is in the name proof. Five new FE bodies have fresh native/stored checks.',
        no_new_blank_box_lost_glyph_orportrait_issue_seen_in_reviewed_samples=True,
        actual_pixel_checks_scope='Seven name headers,fourteen menu captions andboth rejection pages only; no whole live backing/RAM/VRAM/palette ownership claim.',
        unvisited='B81/B82/B83/B86/B88/B89, later B85 dialogue after the7001-frame stop, unsampled/skipped lines/pages andall five new FE bodies remain offline-only. Original conditional activation,location andearned chronology are not established.',
        no_natural_event_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        repeated_A_after_scene_also_activates_following_town_tutorial_sailing_content=True,
        purpose='Focused editorial/display QA. No guide photo collection.',new_credit=0)
    save(actual_path,actual)
    final=deepcopy(doc);final.update(format='dk4-editorial-final-review-v1',all_formatting_gates_false=False,
        all_five_individual_review_gates_passed=True,previous_manuscript=str(DOC),previous_manuscript_sha256=sha(DOC.read_bytes()),
        registered_release_pending=True,new_credit=0)
    speech_bindings={r['id']:r for group in rebuilt['groups'] for r in group['text_records']}
    choice=next(c for g in rebuilt['groups'] for c in g['typed_objects']);raw=bytes.fromhex(choice['compiled_hex'])
    offsets=struct.unpack_from('<2H',raw,2)
    for row in final['records']:
        assert all(row['review'][gate] for gate in ['source','context','localization','naturalness'])
        row['review']['formatting']=True;row['registered_release_andcompletion_credit_pending']=True
        if row['kind']=='typed-choice-label':
            i=row['source_index'];start=6+offsets[i];end=raw.index(0,start)
            assert raw[start:end].decode('ascii')==row['english']
            row['planned_integrated_reference']=dict(file_path=row['file_path'],block=row['block'],command_offset=choice['new_offset'],
                source_index=i,offset=choice['new_offset']+start,bytes=end-start,exact_stored_hex=raw[start:end].hex(),
                target_archive_sha256=rebuilt['target_archive_sha256'])
            row['typed_native_caption_provider_layout_andcontroller_verification_pending']=False
        else:
            binding=speech_bindings[row['id']]
            row['planned_integrated_reference']=dict(file_path=row['file_path'],block=row['block'],offset=binding['new_offset'],
                record_index=binding['new_record_index'],bytes=len(bytes.fromhex(binding['stored_hex'])),
                exact_stored_hex=binding['stored_hex'],target_archive_sha256=rebuilt['target_archive_sha256'])
        row['formatting_evidence']=dict(stored=str(STORED),visual=str(VISUAL),menu=str(MENU) if row['kind']=='typed-choice-label' else None,
            actual=str(actual_path),gameplay_is_representative_not_individual_activation=True)
    final['scoped_names_review']['Emilio_name_glyph']='Corrected in research only. Both original getters andcomplete native font planes,seven actual name headers andjoined notice pass. Registered deployment andown final startup remain pending.'
    final['formatting_evidence']={str(p):sha(p.read_bytes()) for p in [STORED,LOADERS,VISUAL,MENU,NAME,PIXELS,actual_path,REBUILT]}
    validate_natural_dialogue_batch(final)
    typed=[r for r in final['records'] if r['kind']=='typed-choice-label']
    assert compile_choices(bytes.fromhex(choice['source_hex']),bytes.fromhex(choice['current_hex']),typed).hex()==choice['compiled_hex']
    save(FINAL,final)
    # Name glyphs are an additional display correction, not another306 record
    # completions and not blanket approval for the207-entry catalogue.
    name_rows=load('work/analysis/Hodram_B81_B90_new_names_20261101/names.json')
    name_doc=dict(format='dk4-scoped-name-glyph-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=[dict(id='actor14_surname_normal_F',english='Emilio Ferog',speaker='Emilio',
            context='B84 complete recruitment exchange; preserve the existing proper-name spelling across progressive/full native getters andthe joined notice.',
            source_meaning='エミリオ・フェローグ: character identity; no invented title,rank orrelationship.',
            localization_note='Retain Emilio Ferog; normalize only an unintended full-width F. All other name fields,pointers,allocations andadjacent Ferid bytes remain exact.',
            decision='glyph-only-revision',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
            exact_clean_getters=[r for r in name_rows['clean_names']['rows'] if r['actor_ID']==14],
            exact_current_getters=[r for r in name_rows['current_names']['rows'] if r['actor_ID']==14],
            proposed_native=str(NAME),actual=str(PIXELS))],
        owned_field_proposal=name['proposal'],owned_field_proposal_sha256=name['proposal_sha256'],
        native_andactual_passed_registered_deployment_pending=True,no_new_dialogue_credit=True,new_credit=0,full_207_review_still_open=True)
    validate_natural_dialogue_batch(name_doc);name_out=Path('translations/emilio_name_glyph_review_v1.json');assert not name_out.exists();save(name_out,name_doc)
    before=LEDGER.read_bytes();ledger=load(LEDGER);backup=ROOT/'ledger_before_formatting_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    key='Hodram_B81_B89_five_gate_research_20261101';assert key not in ledger
    checkpoint=dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),objects=306,revisions=222,retentions=84,
        all_five_individual_review_gates_passed=True,stored_pages=306,typed_labels=2,native_relative_cases=140,
        archive_loads=325,fresh_parent_cases=18,reused_parent_cases=632,actual_runs=4,actual_frames=41004,actual_sheets=20,
        actual_review=str(actual_path),actual_review_sha256=sha(actual_path.read_bytes()),
        name_glyph_review=str(name_out),name_glyph_review_sha256=sha(name_out.read_bytes()),
        research_reference='work/analysis/Hodram_B81_B89_name_research_20261101/research_reference.json',
        preserved_new_ROMs=5,main_unchanged=True,registered_release_andcompletion_credit_pending=True,
        next='Source-qualified typed-menu production adapter,registered story extension plus final owned-name metadata stage after unchanged right-bound pipeline,atomic/negative guards,exact clean-input patch andown final startup.',
        no_guide_photo_collection=True,new_credit=0,full_goal_complete=False)
    ledger[key]=checkpoint
    assert ledger['records_editorially_completed']==7687 and ledger['records_revised_and_integrated']==4770 and ledger['retained_wordings_editorially_completed']==2917
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger);save(ROOT/'formatting_checkpoint.json',checkpoint)
    print(dict(objects=306,revisions=222,retentions=84,five_gates=306,pages=306,actual_frames=41004,actual_sheets=20,registered_release_pending=True,new_credit=0))
