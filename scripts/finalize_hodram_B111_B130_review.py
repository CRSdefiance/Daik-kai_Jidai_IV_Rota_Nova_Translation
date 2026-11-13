"""Close individual research gates after stored checks and representative English gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B111_B130_checked_20261102b')
DOC=Path('translations/hodram_B111_B130_editorial_manuscript_v1.json')
FINAL=Path('translations/hodram_B111_B130_contextual_final_review_v1.json')
REBUILT=Path('work/analysis/Hodram_B111_B130_rebuilt_20261102b/reconstruction.json')
STORED=Path('work/analysis/Hodram_B111_B130_stored_20261102/stored_native_verification.json')
LOADERS=Path('work/analysis/Hodram_B111_B130_loaders_20261102/verification.json')
VISUAL=Path('work/analysis/Hodram_B111_B130_editorial_20261101/visual_review.json')
MENU=Path('work/analysis/Hodram_B111_B130_editorial_20261101/menu_v1/menu_provider_and_planes_reviewed.json')
STYLES=Path('work/analysis/Hodram_B111_B130_editorial_20261101/styles_v1/compiled_style_objects.json')
NAME=Path('work/analysis/Hodram_B111_B130_name_native_20261101/native_name_fields_verification_reviewed.json')
NAMES=Path('translations/hodram_B111_B130_speaker_name_review_v1.json')
PIXELS=Path('work/analysis/Hodram_B111_B130_actual_pixels_20261102/focused_actual_pixels.json')
SHEETS=[Path('work/analysis')/f'Hodram_B111_B130_actual_{part}_20261102/capture_sheets.json' for part in ['first','second','third']]
LEDGER=Path('translations/editorial_review_current_v1.json')

def main():
    assert not ROOT.exists() and not FINAL.exists();ROOT.mkdir(parents=True)
    doc,rebuilt,stored,loaders,visual,menu,styles,name,names,pixels=map(load,[DOC,REBUILT,STORED,LOADERS,VISUAL,MENU,STYLES,NAME,NAMES,PIXELS])
    assert (len(doc['records']),doc['revised'],doc['retained'])==(323,239,84)
    assert stored['complete_stored_pages']==visual['pages']==315 and stored['typed_labels_checked']==15
    assert len(stored['records'])==260 and len(stored['style_records'])==48
    assert stored['fresh_relocated_native_relative_cases']==430 and (loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(38,612)
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and visual['all_final_pages_directly_viewed_or_exact_plane_reuse']
    assert len(pixels['name_headers'])==5 and len(pixels['body_pages'])==21 and len(pixels['menu_samples'])==3
    assert {r['selected_option'] for r in pixels['menu_samples']}=={0,1,2}
    assert menu['offline_visual_approved'] and name['offline_visual_approved'] and styles['native_target_slot_cases']==64
    runs=[run for path in SHEETS for run in load(path)['runs']];sheets=[s for r in runs for s in r['review_sheets']]
    assert len(runs)==5 and len(sheets)==25 and sum(r['frames'] for r in runs)==51005
    for run in runs:
        assert run['cold_boot'] and not run['savestate'] and not run['hardware_verification']
        assert sha(Path(run['capture_report']).read_bytes())==run['capture_report_sha256']
        for sheet in run['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    actual_path=ROOT/'actual_review.json'
    actual=dict(runs=runs,total_frames=51005,all_review_sheets_directly_viewed=sheets,
        focused_actual_pixels=str(PIXELS),focused_actual_pixels_sha256=sha(PIXELS.read_bytes()),
        scoped_observations=[
            dict(block=115,frames=[4460,7820,9500,10220,10700],observed='Five Follower headers match the complete corrected native normal-F plane.'),
            dict(block=115,frames=[10940,11420,12380,12860],observed='Capture outcome,refusal of identity andwithdrawal are readable;the scene returns to port.'),
            dict(block=117,frames=[5660,5900,6860],observed='Both lamp pages match native pixels;the complete entrusting sentence starts on page2. Item acquisition andport return follow.'),
            dict(block=118,frames=[4700,4940],observed='The doubling sequence andfour-row bean question match complete native pixels withno unwanted blank row.'),
            dict(block=118,frames=[5300,5320,5360],observed='Allthree expanded captions andeach complete selected/unselected highlight match native planes andrectangles;ordinary Down selects the third option.'),
            dict(block=118,frames=[5520,5760,6000,6240,6720],observed='The59-second correct branch,reward andport return follow ordinary controller input.'),
            dict(block=125,frames=[4460,4940,5660],observed='Both source personality4 alternatives match native pixels under the original unassigned-role Sailor fallback;figurehead acquisition andport return follow.'),
            dict(block=126,frames=[4460,4940,5420,5900,6620],observed='Allfive distinct actor0 Rafael bodies match native pixels;the correct name/portrait andnative FI expansion toHodram are observed.'),
            dict(block=126,frames=[5180,6860,7100,7340],observed='Claudio\'s payment proposal is complete;knife acquisition,closing speech andport return are observed.')],
        representative_progressive_FE_actor0_style_three_choice_name_pagination_andscene_transition_observed=True,
        all_target_sampled_paragraphs_andnormal_F_headers_complete=True,
        source_personality4_observed_other_personalities_offline=True,other_four_menus_offline=True,
        unvisited='B111/B112/B113/B114/B116/B119/B120/B121/B122/B123/B124/B127/B129/B130 are offline-only in this batch. Other personality classes,other menus,wrong-answer paths andconditional B115 crew trap branches were not individually activated. Diogo full-catalogue UI remains unvisited;its original getters andcomplete native style11/1 planes pass offline. No assertion that unbound identical chants identify a particular source occurrence.',
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        no_whole_live_backing_RAM_VRAM_palette_orVM_register_ownership_claim=True,
        repeated_A_after_target_scenes_also_enters_existing_port_tutorial_andmenus=True,
        following_content_limits='Following port/tutorial samples include ordinary intermediate portrait/header transition states;they are not additional target-dialogue approval orproof of original scene location.',
        purpose='Focused editorial/display QA;no guide photo collection.',new_credit=0)
    save(actual_path,actual)
    final=deepcopy(doc);final.update(format='dk4-editorial-final-review-v1',encoder='dialogue-relocatable-v1',all_formatting_gates_false=False,
        all_five_individual_review_gates_passed=True,previous_manuscript=str(DOC),previous_manuscript_sha256=sha(DOC.read_bytes()),
        registered_release_pending=True,new_credit=0,stage_status=dict(prose=True,offline_display=True,stored=True,representative_English_gameplay=True,registered_release=False))
    ordinary={r['id']:r for r in stored['records']};style_rows={r['id']:r for r in stored['style_records']}
    choice_rows={r['id']:(item,r) for item in stored['typed_objects'] for r in item['label_references']}
    target_blocks=IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    clean_blocks=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(doc['file_path'])).blocks
    for row in final['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['review']['formatting']=True;row['registered_release_andcompletion_credit_pending']=True
        row.pop('formatting_names_glyph_stored_actual_andregistered_release_pending',None)
        if row['kind']=='typed-choice-label':
            item,binding=choice_rows[row['id']];at=binding['offset'];raw=bytes.fromhex(binding['stored_hex'])
            row['source_reference']=dict(file_path=row['file_path'],block=row['block'],command_offset=row['source_command_offset'],
                source_index=row['source_index'],offset=row['source_byte_offset'],length=len(bytes.fromhex(row['source_hex'])))
            assert clean_blocks[row['block']][row['source_byte_offset']:row['source_byte_offset']+len(bytes.fromhex(row['source_hex']))].hex()==row['source_hex']
            reference=dict(file_path=row['file_path'],block=row['block'],command_offset=item['offset'],source_index=row['source_index'],
                offset=at,record_index=binding['record_index'],bytes=len(raw),exact_stored_hex=raw.hex(),native_command_word=item['word'])
        else:
            binding=style_rows[row['id']] if row.get('native_object_kind')=='4100-style-alternative' else ordinary[row['id']]
            at=binding['new_offset'];raw=bytes.fromhex(binding['stored_hex'])
            reference=dict(file_path=row['file_path'],block=row['block'],offset=at,record_index=binding['new_record_index'],bytes=len(raw),exact_stored_hex=raw.hex())
            if row.get('native_object_kind')=='4100-style-alternative':
                reference.update(command_offset=binding['final_command_offset'],source_style_indices=row['source_style_indices'],
                    native_command_word=0x4100,virtual_prefix_not_stored=True,final_header_hex=binding['final_header_hex'])
            else:assert target_blocks[row['block']][at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert target_blocks[row['block']][at:at+len(raw)+1]==raw+b'\0'
        reference['target_archive_sha256']=rebuilt['target_archive_sha256'];row['planned_integrated_reference']=reference
        row['formatting_evidence']=dict(stored=str(STORED),visual=str(VISUAL),native_menu=str(MENU) if row['kind']=='typed-choice-label' else None,
            native_styles=str(STYLES) if row.get('native_object_kind')=='4100-style-alternative' else None,actual=str(actual_path),representative_gameplay_not_individual_activation=True)
    plans={r['id']:r for r in load(rebuilt['plan'])['records']}
    for group in rebuilt['groups']:
        for item in group['native_objects']:
            rows=[r for r in final['records'] if r['id'] in {p['id'] for p in item['records']}]
            rows.sort(key=(lambda r:r['source_reference']['offset']) if item['word']==0x4100 else (lambda r:r['source_index']))
            source,current=map(bytes.fromhex,[item['source_hex'],item['current_hex']])
            value=compile_styles(source,current,rows,plans) if item['word']==0x4100 else compile_choices(source,current,rows)
            assert value.hex()==item['compiled_hex']
    final['scoped_speaker_name_review']=dict(manuscript=str(NAMES),sha256=sha(NAMES.read_bytes()),actors=18,
        name_native=str(NAME),name_native_sha256=sha(NAME.read_bytes()),known_six_exact_reuse=doc['known_names'],full_207_review_still_open=True)
    final['formatting_evidence']={str(p):sha(p.read_bytes()) for p in [STORED,LOADERS,VISUAL,MENU,STYLES,NAME,PIXELS,actual_path,REBUILT]}
    validate_natural_dialogue_batch(final);save(FINAL,final)
    name_final=deepcopy(names)
    for row in name_final['records']:
        row['review']['formatting']=True;row['registered_deployment_pending']=True
        row['actual_English_scene_checks_andregistered_deployment_pending']=False
        row['formatting_evidence']=dict(native=str(NAME),actual=str(actual_path),full_catalogue_UI_unvisited=True,exact_unchanged_retained_consumers_not_replayed=True)
    name_final.update(previous=str(NAMES),previous_sha256=sha(NAMES.read_bytes()),all_five_gates_pass_in_scoped_context=True,registered_deployment_pending=True)
    name_out=Path('translations/hodram_B111_B130_speaker_name_review_final_v1.json');assert not name_out.exists();save(name_out,name_final)
    proposal=load(name['proposal']);fields=[]
    for field in proposal['fields']:
        ident=field['actor'];fields.append(dict(id=f'actor{ident}_column{field["column"]}_localized_name_field',english='Follower' if ident==178 else 'Diogo de Escante',
            speaker='Follower' if ident==178 else 'Diogo Escante',context='Source-bound names in the complete B111-B130 exchanges;preserve separate progressive/full consumers.',
            source_meaning='信徒' if ident==178 else 'ディオゴ・エスカンテ / ディオゴ・デ・エスカンテ',localization_note=field['reason'],
            review={g:True for g in ['source','context','localization','naturalness','formatting']},owned_field=field,native=str(NAME),
            actual=str(PIXELS) if ident==178 else None,full_catalogue_UI_unvisited=True,decision='glyph-only-revision' if ident==178 else 'name-component-localization'))
    field_doc=dict(format='dk4-scoped-owned-name-fields-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=fields,owned_field_proposal=name['proposal'],owned_field_proposal_sha256=name['proposal_sha256'],
        native_andrepresentative_gameplay_checked_registered_deployment_pending=True,additional_fields=2,no_new_dialogue_credit=True,new_credit=0,full_207_review_still_open=True)
    validate_natural_dialogue_batch(field_doc);field_out=Path('translations/follower_diogo_owned_name_review_v1.json');assert not field_out.exists();save(field_out,field_doc)
    checkpoint=dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual=str(actual_path),actual_sha256=sha(actual_path.read_bytes()),
        reconstruction=str(REBUILT),stored=str(STORED),loaders=str(LOADERS),name_review=str(name_out),name_fields_review=str(field_out),
        total_reviews=323,revised=239,retained=84,native_pages=315,page_findings_resolved=7,FE_blank_rows_resolved=2,phrase_findings_resolved=2,
        native_relative_cases=430,whole_archive_loads=325,actual_runs=5,actual_frames=51005,directly_viewed_actual_sheets=25,
        all_individual_five_gates_pass_in_research=True,registered_release_andcompletion_credit_pending=True,current_registered_ROM_andmain_unchanged=True,
        terminal_sessions=dict(rebuild=83487,stored=42585,fixtures=81827,game115=89127,game118=97355,game117=54359,game125=86668,game126=52924),
        full_goal_complete=False,new_credit=0)
    save(ROOT/'formatting_checkpoint.json',checkpoint)
    before=LEDGER.read_bytes();ledger=load(LEDGER);backup=ROOT/'ledger_before_research_completion.json';assert not backup.exists();backup.write_bytes(before)
    assert ledger['records_editorially_completed']==8204 and not ledger['full_goal_complete']
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not keys&{(r['file_path'],r['id']) for r in final['records']}
    ledger['Hodram_B111_B130_five_gate_research_20261102']=checkpoint
    ledger['latest_checkpoint']='B111-B130:all323 individual five-gate research reviews pass;239 revisions/84 retentions,315 stored/viewed pages,48 physical style alternatives/64 aliases,15 menu labels/5 menus.430 relocated relative cases/325 archive loads pass.5 initialized English runs/51005frames/25 viewed sheets prove normal F,actor0,FI,style4,three highlights,FE rows,pagination andport returns.2 owned name fields checked. Registered integration/exact clean patch/own startup andonce-only credit pending;8204/current e713/main unchanged. Full goal active;no guide photos.'
    old=load(backup);allowed={'Hodram_B111_B130_five_gate_research_20261102','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in old.items() if k not in allowed}
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    print('323 five-gate research reviews pass;239 revisions/84 retentions,315 stored pages,5 English runs/51005frames,25 viewed actual sheets. Registered integration andcredit pending.')

if __name__=='__main__':main()
