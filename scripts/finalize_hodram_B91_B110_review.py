"""Close the211 source-bound reviews after offline/storage and representative gameplay."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B91_B110_editorial_20261101')
DOC=Path('translations/hodram_B91_B110_editorial_manuscript_v2.json')
FINAL=Path('translations/hodram_B91_B110_contextual_final_review_v1.json')
REBUILT=Path('work/analysis/Hodram_B91_B110_rebuilt_20261101/reconstruction.json')
STORED=Path('work/analysis/Hodram_B91_B110_stored_20261101/stored_native_verification.json')
LOADERS=Path('work/analysis/Hodram_B91_B110_loaders_20261101/verification.json')
VISUAL=Path('work/analysis/Hodram_B91_B110_visual_20261101/visual_review.json')
MENU=Path('work/analysis/Hodram_B91_B110_menu_20261101/menu_provider_and_planes_reviewed.json')
NAME=Path('work/analysis/Hodram_B91_B110_name_native_20261101/native_name_fields_verification_reviewed.json')
PIXELS=Path('work/analysis/Hodram_B91_B110_actual_pixels_20261101d/focused_actual_pixels.json')
SHEETS=[Path('work/analysis/Hodram_B91_B110_actual_20261101/capture_sheets.json'),Path('work/analysis/Hodram_B91_B110_decline_actual_20261101/capture_sheets.json')]
LEDGER=Path('translations/editorial_review_current_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists();ROOT.mkdir(parents=True)
    doc,rebuilt,stored,loaders,visual,menu,name,pixels=map(load,[DOC,REBUILT,STORED,LOADERS,VISUAL,MENU,NAME,PIXELS])
    assert len(doc['records'])==211 and (doc['revised'],doc['retained'])==(129,82)
    assert stored['complete_stored_pages']==visual['pages']==215 and stored['typed_labels_checked']==2
    assert stored['fresh_relocated_native_relative_cases']==40
    assert (loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(28,622)
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and visual['all_final_pages_directly_viewed_or_exact_plane_reuse']
    assert len(pixels['name_headers'])==6 and len(pixels['body_pages'])==6 and len(pixels['menu_samples'])==3
    assert menu['offline_visual_approved'] and name['offline_visual_approved']
    runs=[run for path in SHEETS for run in load(path)['runs']];sheets=[s for r in runs for s in r['review_sheets']]
    assert len(runs)==3 and len(sheets)==13 and sum(r['frames'] for r in runs)==28003
    for run in runs:
        assert run['cold_boot'] and not run['savestate'] and not run['hardware_verification']
        assert sha(Path(run['capture_report']).read_bytes())==run['capture_report_sha256']
        for sheet in run['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    actual_path=ROOT/'actual_review.json'
    actual=dict(runs=runs,total_frames=28003,all_review_sheets_directly_viewed=sheets,
        focused_actual_pixels=str(PIXELS),focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        scoped_observations=[
            dict(block=91,frame=4320,observed='The Sailor asks about miracles;the original question,portrait andSailor label display correctly.'),
            dict(block=91,frame=4560,observed='Both complete belief captions fit the native popup;initial option0 highlight is partial in this captured frame.'),
            dict(block=91,run='decline',frames=[4560,4680,4800],observed='Ordinary DOWN moves to option1 witha complete highlight;ordinary A reaches the distinct refusal response.'),
            dict(block=91,frames=[5040,5520,6000,6480,7200],observed='Normal-F Fernando Dias headers match complete native style11 pixels.'),
            dict(block=91,run='decline',frame=4800,observed='A sixth complete Fernando Dias header matches native pixels.'),
            dict(block=91,frames=[8400,8640],ids=['DK4_MES_B91_R0084','DK4_MES_B91_R0087'],observed='Both one-point Luck notices display completely;the first expands FI natively to Hodram.'),
            dict(block=91,run='decline',frames=[5280,5520],ids=['DK4_MES_B91_R0103','DK4_MES_B91_R0106'],observed='Both one-point Spirit notices display completely;the first expands FI natively to Hodram.'),
            dict(block=91,frame=9120,observed='Agreement completes item acquisition andreturns to port UI.'),
            dict(block=91,run='decline',frame=5760,observed='Refusal returns to port UI.'),
            dict(block=104,frames=[4320,4560],id='DK4_MES_B104_R0013',observed='Both complete telescope pages match native pixels;the attributed second sentence starts on page2.'),
            dict(block=104,frame=6720,observed='The exchange returns to port UI.')],
        representative_progressive_FE_macros_pagination_menu_name_andscene_transition_observed=True,
        all_four_conditional_B91_notices_observed_across_two_unforced_selection_paths=True,
        unvisited='B92/B93/B95/B97/B100/B101/B102/B103/B105/B108/B109/B110 andthree monkey FE bodies are offline-only in this batch. B91 R61 has no complete sampled body. Samwell full-catalogue UI is unvisited;both getters andcomplete native style1/11 planes are checked offline. Other unsampled text andconditional participation remain unproved individually.',
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        no_whole_live_backing_RAM_VRAM_palette_orVM_register_ownership_claim=True,
        repeated_A_after_scene_also_enters_following_port_tutorial_content=True,
        failed_pixel_comparison_producers_preserved='Earlier comparisons assumed another scene\'s body palette/origin andfull initial highlight. The passing successor uses measured RGB/origin andexplicit partial-highlight limits;no ROM defect is inferred from those checker failures.',
        purpose='Focused editorial/display QA;no guide photo collection.',new_credit=0)
    save(actual_path,actual)
    final=deepcopy(doc);final.update(format='dk4-editorial-final-review-v1',all_formatting_gates_false=False,
        all_five_individual_review_gates_passed=True,previous_manuscript=str(DOC),previous_manuscript_sha256=sha(DOC.read_bytes()),registered_release_pending=True,new_credit=0)
    text={r['id']:r for g in rebuilt['groups'] for r in g['text_records']}
    choice=next(c for g in rebuilt['groups'] for c in g['typed_objects']);raw=bytes.fromhex(choice['compiled_hex']);offsets=struct.unpack_from('<2H',raw,2)
    for row in final['records']:
        assert all(row['review'][g] for g in ['source','context','localization','naturalness']);row['review']['formatting']=True
        row['registered_release_andcompletion_credit_pending']=True
        if row['kind']=='typed-choice-label':
            i=row['source_index'];start=6+offsets[i];end=raw.index(0,start);assert raw[start:end].decode('ascii')==row['english']
            row['planned_integrated_reference']=dict(file_path=row['file_path'],block=row['block'],command_offset=choice['new_offset'],source_index=i,offset=choice['new_offset']+start,bytes=end-start,exact_stored_hex=raw[start:end].hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            row['typed_native_caption_provider_layout_andcontroller_verification_pending']=False
        else:
            binding=text[row['id']]
            row['planned_integrated_reference']=dict(file_path=row['file_path'],block=row['block'],offset=binding['new_offset'],record_index=binding['new_record_index'],bytes=len(bytes.fromhex(binding['stored_hex'])),exact_stored_hex=binding['stored_hex'],target_archive_sha256=rebuilt['target_archive_sha256'])
        row['formatting_evidence']=dict(stored=str(STORED),visual=str(VISUAL),menu=str(MENU) if row['kind']=='typed-choice-label' else None,actual=str(actual_path),representative_gameplay_not_individual_activation=True)
    names_path=Path('work/analysis/Hodram_B91_B110_new_names_20261101/names.json');names=load(names_path)
    retentions={
        15:'Angelo Puccini matches the clean identity;retain the established spelling andItalian-flavored humor without an invented title.',
        108:'Trader naturally identifies the trade-house speaker. Familiar親父 does not make him the captain\'s father.',
        114:'Port Worker identifies the departure-office speaker. Familiar兄貴 does not establish brotherhood,age orrank.',
        139:'Priest is the natural English role for神父 in this exchange;no new church rank is implied.',
        152:'Retain the distinct source consumers:水夫 is Sailor on the progressive nameplate;配下 is Retainer in the full catalogue. Do not normalize one into the other.',
        188:'Margrete matchesマルグレーテ. Retain the existing spelling;separate Hamburg metadata supplies no surname orguaranteed scene location.',
    }
    final['scoped_speaker_name_review']=dict(native_source_current=str(names_path),native_source_current_sha256=sha(names_path.read_bytes()),
        justified_retentions=[dict(actor=k,reason=v,clean_getters=[r for r in names['clean_names']['rows'] if r['actor_ID']==k],current_getters=[r for r in names['current_names']['rows'] if r['actor_ID']==k],unchanged_native_consumers=True,no_new_global_207_name_credit=True) for k,v in retentions.items()],
        corrected_fields_native=str(NAME),known_six_exact_name_reuse=doc['known_name_reuse'],full_207_review_still_open=True)
    final['formatting_evidence']={str(p):sha(p.read_bytes()) for p in [STORED,LOADERS,VISUAL,MENU,NAME,PIXELS,actual_path,REBUILT]}
    validate_natural_dialogue_batch(final)
    assert compile_choices(bytes.fromhex(choice['source_hex']),bytes.fromhex(choice['current_hex']),[r for r in final['records'] if r['kind']=='typed-choice-label']).hex()==choice['compiled_hex']
    save(FINAL,final)
    proposal=load(name['proposal']);name_rows=[]
    for field in proposal['fields']:
        ident=field['actor'];name_rows.append(dict(id=f'actor{ident}_column{field["column"]}_localized_name_field',english='Fernando Dias' if ident==20 else 'Samwell da Khan',speaker='Fernando' if ident==20 else 'Samwell',
            context='Preserve the source character identity anddistinct progressive/full name consumers in the complete Hodram exchanges.',
            source_meaning='フェルナンド・ディアス' if ident==20 else 'サムウェル・カーン / サムウェル・ダ・カーン',localization_note=field['reason'],
            decision='glyph-only-revision' if ident==20 else 'name-component-localization',review={g:True for g in ['source','context','localization','naturalness','formatting']},
            owned_field=field,exact_clean_getters=[r for r in names['clean_names']['rows'] if r['actor_ID']==ident],exact_current_getters=[r for r in names['current_names']['rows'] if r['actor_ID']==ident],
            native=str(NAME),actual=str(PIXELS) if ident==20 else None,full_catalogue_UI_unvisited=True))
    name_doc=dict(format='dk4-scoped-owned-name-fields-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=name_rows,owned_field_proposal=name['proposal'],owned_field_proposal_sha256=name['proposal_sha256'],
        native_andrepresentative_gameplay_checked_registered_deployment_pending=True,additional_fields=2,no_new_dialogue_credit=True,new_credit=0,full_207_review_still_open=True)
    validate_natural_dialogue_batch(name_doc);name_out=Path('translations/fernando_samwell_owned_name_review_v1.json');assert not name_out.exists();save(name_out,name_doc)
    before=LEDGER.read_bytes();ledger=load(LEDGER);assert ledger['records_editorially_completed']==7993
    (ROOT/'ledger_before_formatting_checkpoint.json').write_bytes(before)
    checkpoint=dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),objects=211,revisions=129,retentions=82,physical_speeches=209,typed_choices=2,
        all_five_individual_review_gates_passed=True,stored_pages=215,typed_labels=2,native_relative_cases=40,archive_loads=325,fresh_parent_cases=28,reused_parent_cases=622,
        actual_runs=3,actual_frames=28003,actual_sheets=13,actual_review=str(actual_path),actual_review_sha256=sha(actual_path.read_bytes()),
        page_coherence_findings_resolved=5,additional_name_fields=2,name_review=str(name_out),name_review_sha256=sha(name_out.read_bytes()),
        research_reference='work/analysis/Hodram_B91_B110_name_research_20261101/research_reference.json',
        source_terms='work/analysis/Hodram_B91_B110_clean_20261101/source_bound_item_terminology_v2.json',Spirit_term='work/analysis/Hodram_B91_B110_clean_20261101/Spirit_source_term_binding.json',
        main_unchanged=True,registered_release_andcompletion_credit_pending=True,no_guide_photo_collection=True,new_credit=0,full_goal_complete=False,
        next='Qualify the registered scene extension andseparate final owned-name-fields successor after the unchanged runtime-bounds/Emilio stages;then atomic guards,cumulative reconstruction,exact clean-input patch andown final startup.')
    key='Hodram_B91_B110_five_gate_research_20261101';assert key not in ledger;ledger[key]=checkpoint
    ledger['Hodram_B91_B110_clean_next_20261101'].update(earlier_English_unconsulted=False,earlier_English_dialogue_andchoice_labels_unconsulted=False,current_English_contextual_editorial_native_formatting_stored_gameplay_andrelease_pending=False,registered_release_only_pending=True,continued_checkpoint=str(ROOT/'formatting_checkpoint.json'))
    ledger['latest_checkpoint']='B91-B110 research:211 five-gate reviews,129 revisions/82 retentions;215 stored/visually reviewed pages,5 page findings resolved,2 additional name fields,3 focused coldboots/28003frames. Registered release pending;7993 completed/main unchanged. No guide photos;full scope active.'
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger);save(ROOT/'formatting_checkpoint.json',checkpoint)
    pins=Path('translations/rom_retention_pins.json');pin_before=pins.read_bytes();values=load(pins);known={str(Path(p['path']).resolve()).lower() for p in values}
    reference=load(checkpoint['research_reference']);fixtures=load('work/analysis/Hodram_B91_B110_fixtures_20261101/fixtures.json')
    paths=[Path(rebuilt['research_ROM']),Path(reference['research_ROM']),*[Path(r['research_ROM']) for r in fixtures['fixtures']]]
    additions=[]
    for path in paths:
        absolute=str(path.resolve())
        if absolute.lower() not in known:additions.append(dict(path=absolute,reason='Preserve B91-B110 editorial/menu/name research andfocused QA fixtures. Not a registered release. SHA256 '+sha(path.read_bytes())))
    (ROOT/'pins_before_research.json').write_bytes(pin_before);assert pins.read_bytes()==pin_before;save(pins,values+additions)
    save(ROOT/'new_research_pins.json',dict(added=additions,no_deletions=True,previous_pins_sha256=sha(pin_before)))
    print(dict(objects=211,revisions=129,retentions=82,five_gates=211,pages=215,actual_frames=28003,actual_sheets=13,pinned_ROMs=len(additions),registered_release_pending=True,new_credit=0))
