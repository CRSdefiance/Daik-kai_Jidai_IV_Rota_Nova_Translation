"""Close330 source editorial gates with explicit virtual-page and actual/offline provenance."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES,validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import labels,count_and_base
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael330_checked_20261105')
FINAL=Path('translations/rafael_B81_B84_contextual_final_review_v1.json')
NAMES_FINAL=Path('translations/rafael_B81_B84_scoped_names_actual_final_v1.json')
INPUTS=Path('work/analysis/Rafael330_stored_consumer_inputs_v3_20261105')

def main():
    assert not ROOT.exists() and not FINAL.exists() and not NAMES_FINAL.exists()
    rebuilt_path=Path('work/analysis/Rafael_B81_B84_rebuilt_v3_20261105/reconstruction.json')
    rebuilt=load(rebuilt_path);manuscript=Path(rebuilt['manuscript']);doc=load(manuscript)
    native_path=INPUTS/'native_consumer_planes.json';native=load(native_path)
    stored_path=Path('work/analysis/Rafael330_stored_native_v3_20261105/stored_native_verification.json')
    stored=load(stored_path)
    lookup_path=Path('work/analysis/Rafael330_stored_catalogue_v3_20261105/all327_stored_effective_body_bindings.json')
    loaders_path=Path('work/analysis/Rafael330_loaders_v3_20261105/verification.json')
    lookup,loaders=map(load,[lookup_path,loaders_path])
    flat=load(INPUTS/'native_consumer_manuscript.json');consumer=load(INPUTS/'native_consumer_reconstruction.json')
    assert len(doc['records'])==330 and sum(r['kind']!='typed-choice-label' for r in doc['records'])==325
    assert len(native['records'])==len(stored['records'])==len(lookup['records'])==327
    assert native['pages']==stored['complete_stored_pages']==336
    assert stored['native_sha256']==sha(native_path.read_bytes())
    assert stored['reconstruction_sha256']==sha((INPUTS/'native_consumer_reconstruction.json').read_bytes())
    assert stored['fresh_relocated_native_relative_cases']==140
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,2,684)
    assert loaders['prior_executed_parent_instructions_match_current_runtime']
    assert native['runtime']==stored['runtime'] and stored['runtime']['captain']==0
    image=NdsImage.open(rebuilt['research_ROM']);assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    bank=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    assert sha(image.read_file(doc['file_path']))==rebuilt['target_archive_sha256']
    current_n={r['id']:r for r in native['records']};current_s={r['id']:r for r in stored['records']}
    flat_rows={r['id']:r for r in flat['records']}
    assert set(current_n)==set(current_s)==set(flat_rows)
    bysource={}
    for group in consumer['groups']:
        for text in group['text_records']:
            owner=text['source_editorial_ID'];bysource.setdefault(owner,[]).append(text)
            raw=bytes.fromhex(text['stored_hex']);at=text['new_offset'];block=bank[group['block']]
            assert block[at:at+len(raw)+1]==raw+b'\0'
            assert block[at-5:at+1].hex()==text['complete_source_preamble_hex']
            assert text['stored_hex']==current_s[text['id']]['stored_hex']
            assert text['compiled_hex']==current_n[text['id']]['compiled_hex']
    assert len(bysource)==325 and sum(len(v)==2 for v in bysource.values())==2
    historical_approval=Path('work/analysis/Rafael330_actual_progress_20261105/actual_visual_andscope_approval_v1.json')
    previous_actual=load(historical_approval)
    assert previous_actual['all16_scoped_names_actual_complete']
    assert previous_actual['all_four_FE_continuation_panels_andthree_FI_notice_texts_observed']
    native_visual=Path('work/analysis/Rafael_B84_choices_20261105/complete_native_visual_approval_v1.json')
    assert load(native_visual)['all20_menu_style_planes_andfour_FE_pages_approved']
    composite_path=Path('work/analysis/Rafael330_food_composite_v3_20261105/native323.json')
    composite=load(composite_path)
    assert composite['all323_subset_body_layouts_approved'] and not composite['direct_visual_review_pending']
    for ident in ['DK4_MES_B81_R0216','DK4_MES_B81_R0220']:
        origin=composite['origins'][ident]
        assert sha(Path(origin['native_proof']).read_bytes())==origin['native_proof_sha256']
    actual_paths=[Path(p) for p in [
        'work/analysis/Rafael_B81_complete_scene_pixels_v2_20261105/focused_actual_pixels.json',
        'work/analysis/Rafael330_names_pages_FE_pixels_v1_20261105/focused_actual_pixels.json',
        'work/analysis/Rafael330_menu_cursor_body_pixels_v3_20261105/focused_actual_pixels.json',
        'work/analysis/Rafael_food_actual_pixels_v3_20261105/focused_actual_pixels.json']]
    actual_proofs=list(map(load,actual_paths));observed_native=set();pages=set();observed_actors=set();compatible_samples=[]
    changed={'DK4_MES_B81_R0216','DK4_MES_B81_R0220'}
    for index,proof in enumerate(actual_proofs):
        assert proof['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert proof['all_selected_pages_observed_in_exact_fixture_order']
        assert not any(proof[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        for sample in proof['body_pages']:
            if index<3 and sample['id'] in changed:continue
            row=current_n[sample['id']];display=row['complete_native_English_display']
            page=display if row['kind']=='system-FE' else display['pages'][sample['page']-1]
            assert sample['native_plane_sha256']==page['native_plane_sha256']
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            observed_native.add(sample['id']);pages.add((sample['id'],sample['page']))
            compatible_samples.append(dict(id=sample['id'],page=sample['page'],proof=str(actual_paths[index]),
                frame=sample['frame'],capture=sample['capture']))
        observed_actors.update(h['actor_ID'] for h in proof['headers'])
    assert (actual_proofs[-1]['selected_utterances'],actual_proofs[-1]['selected_pages'])==(9,9)
    observed_source={flat_rows[k].get('source_editorial_ID',k) for k in observed_native}
    assert (len(observed_source),len(observed_native),len(pages),len(observed_actors))==(75,77,86,16)
    assert actual_proofs[0]['complete_scene_commands_retained']
    menu_paths=[Path(f'work/analysis/{name}/menu_actual_pixels.json') for name in
        ['Rafael330_menu_actual_pixels_v2_20261105','Rafael330_menu_cursor_actual_pixels_v2_20261105']]
    options={3114:set(),5298:set()}
    for path in menu_paths:
        proof=load(path);assert proof['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert proof['numeric_modal_return_register_original_story_branches_andcancellation_unvisited']
        for menu in proof['menus']:options[menu['source_command_offset']].update(menu['observed_selected_options'])
    assert options=={3114:{0,1},5298:{0,1,2}}
    sheet_path=Path('work/analysis/Rafael_food_actual_sheets_v3_20261105/receipt.json')
    fresh_sheets=load(sheet_path);assert fresh_sheets['actual_dialogue_pages']==9 and len(fresh_sheets['bottom_screen_sheets'])==1
    for sheet in fresh_sheets['bottom_screen_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir()
    visual_path=ROOT/'complete_visual_approval.json'
    save(visual_path,dict(body_pages=336,all336_final_pages_directly_viewed_or_exact_native_plane_reuse=True,
        all20_caption_style_planes_andfive_labels_viewed=True,all16_scoped_nameplanes_viewed=True,
        all_nine_final_food_exchange_actual_pages_directly_viewed=True,fresh_actual_sheets=fresh_sheets['bottom_screen_sheets'],
        historical_visual_approval=str(historical_approval),native_menu_FE_visual_approval=str(native_visual),
        one_fresh_Rafael_assurance_native_sheet_viewed=True,prior_Emilio_native_andactual_views_preserved=True,new_credit=0))
    actual_path=ROOT/'actual_review.json'
    save(actual_path,dict(total_frames=72406,initialized_fixture_runs=6,qualifying_current_runs=5,qualifying_current_frames=65205,
        earlier_food_v2_run_preserved_not_relabelled_for_changed_R216=True,
        source_speeches_observed=75,native_commands_observed=77,native_body_pages_observed=86,
        actual_choice_labels=5,source_editorial_objects_observed=80,offline_only_source_speeches=250,
        sampled_source_IDs=sorted(observed_source),sampled_native_IDs=sorted(observed_native),compatible_page_samples=compatible_samples,
        all16_actual_nameplates=True,all_nine_two_page_cases_andseven_page_turn_fixes_observed=True,
        four_FE_panels_andthree_FI_notice_texts_observed=True,all_native_menu_cursor_positions_andA_returns_observed=True,
        actual_training_stat_effects_numeric_choice_returns_original_story_branches_andcancellation_unvisited=True,
        original_B81_all101_commands_retained_49of51_speeches_inone_branch=True,
        both_conditional_asides_seen_separately_infocused_fixture=True,static_CG_does_not_resolve_throw_agent_orobject=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        body_proofs=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in actual_paths],
        menu_proofs=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in menu_paths],new_credit=0,guide_photos=False))
    names_path=Path('translations/rafael_B81_B84_scoped_names_androles_v1.json');names=deepcopy(load(names_path))
    assert {r['actor_ID'] for r in names['records']}==observed_actors
    names.update(encoder='dialogue-relocatable-v1',review_gates=sorted(REQUIRED_REVIEW_GATES),
        scoped_progressive_planes_pending=False,actual_headers_andfull_catalogue_UI_unvisited=False,
        actual_headers_observed=True,full_catalogue_UI_unvisited=True,no_new_dialogue_credit=True)
    for row in names['records']:
        row['review']['formatting']=True
        row.update(speaker=row['english'],context='Scoped speaker identity/role within the four reviewed Rafael recruitment/training exchanges.',
            source_meaning=' / '.join(s for s in row['clean_components'] if s),localization_note=row['finding'],
            actual_header_proof=str(actual_paths[1]),actual_header_proof_sha256=sha(actual_paths[1].read_bytes()))
    validate_natural_dialogue_batch(names);save(NAMES_FINAL,names)
    final=deepcopy(doc);plans=load(Path(rebuilt['research_ROM']).parent/'complete_two_source_FE_page_plan.json')
    plan_byid={r['id']:r for r in plans['records']};assert len(plan_byid)==325
    group_byblock={g['block']:g for g in rebuilt['groups']}
    for row in final['records']:
        assert all(row['review'][g] for g in REQUIRED_REVIEW_GATES-{'formatting'})
        row['review']['formatting']=True
        if row['kind']=='typed-choice-label':
            obj=next(o for o in group_byblock[row['block']]['first_page_reconstruction']['native_objects']
                if o['old_offset']==row['source_command_offset'])
            mapped=next(o for o in next(g for g in consumer['groups'] if g['block']==row['block'])['typed_objects'] if o['id']==obj['id'])
            raw=bytes.fromhex(obj['compiled_hex']);count,base=count_and_base(raw);index=row['source_index']
            at=mapped['new_offset']+base+struct.unpack_from('<H',raw,2+index*2)[0]
            caption=labels(raw)[index];assert caption==row['english'].encode('ascii')
            row['planned_integrated_reference']=dict(file_path=doc['file_path'],block=row['block'],offset=at,
                exact_stored_hex=caption.hex(),source_index=index,command_offset=mapped['new_offset'],
                complete_choice_object_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            assert bank[row['block']][at:at+len(caption)+1]==caption+b'\0'
            row['native_caption_geometry_selection_anddisplay_pending']=False
            row['actual_utterance_observed_in_disclosed_fixture']=True
        else:
            entries=bysource[row['id']];first=entries[0]
            row['planned_integrated_reference']=dict(file_path=doc['file_path'],block=row['block'],offset=first['new_offset'],
                header_offset=first['new_offset']-5,record_index=first['new_record_index'],exact_stored_hex=first['stored_hex'],
                target_archive_sha256=rebuilt['target_archive_sha256'])
            row['planned_English_markup']=plan_byid[row['id']]['formatted_markup']
            if len(entries)==2:
                row['planned_integrated_native_pages']=[dict(id=e['id'],offset=e['new_offset'],record_index=e['new_record_index'],
                    exact_stored_hex=e['stored_hex'],complete_source_preamble_hex=e['complete_source_preamble_hex']) for e in entries]
                paragraphs=[flat_rows[e['id']]['english'] for e in entries]
                assert ' '.join(paragraphs)==row['english']
            else:assert current_n[first['id']]['logical_English']==row['english']
            row['actual_utterance_observed_in_disclosed_fixture']=row['id'] in observed_source
        row.update(registered_release_andcompletion_credit_pending=True,all_fresh_display_andintegration_pending=False,
            source_context_localization_formatting_gates_pending=False,complete_native_preamble_andfresh_formatting_pending=False,
            formatting_evidence=dict(native=str(native_path),stored=str(stored_path),actual=str(actual_path),visual=str(visual_path),
                native_vs_source_commands='325 source speeches become327 native commands via two source-owned FE continuations;five captions remain separate.'))
    evidence=[manuscript,native_path,stored_path,lookup_path,loaders_path,rebuilt_path,historical_approval,native_visual,
        composite_path,visual_path,actual_path,sheet_path,NAMES_FINAL,*actual_paths,*menu_paths,Path(__file__)]
    final.update(format='dk4-editorial-final-review-v1',all_five_individual_review_gates_passed=True,
        all_formatting_gates_false=False,all_fifth_gates_false_until_stored_actual_andrelease=False,
        B81_original_action_andtransition_sample_pending=False,registered_release_andcompletion_credit_pending=True,
        source_editorial_objects=330,source_speeches=325,native_commands=327,native_body_pages=336,typed_choice_labels=5,
        actual_source_speeches=75,actual_body_pages=86,offline_only_source_speeches=250,
        scoped_name_review=str(NAMES_FINAL),scoped_name_review_sha256=sha(NAMES_FINAL.read_bytes()),
        formatting_evidence={str(p):sha(p.read_bytes()) for p in evidence},new_credit=0,full_goal_complete=False)
    validate_natural_dialogue_batch(final);save(FINAL,final)
    save(ROOT/'release_plans.json',{**plans,'failures':[], 'manuscript':str(FINAL),'manuscript_sha256':sha(FINAL.read_bytes())})
    save(ROOT/'formatting_checkpoint.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        revised=174,retained=156,source_editorial_objects=330,source_speeches=325,native_commands=327,body_pages=336,
        captions=5,names_retained=16,actual_source_speeches=75,actual_body_pages=86,offline_only_source_speeches=250,
        layout_only_refinements=18,page_turn_fixes=7,phrase_wrap_fixes=11,fullwidth_Latin_fixes=4,
        all_five_individual_gates_pass_in_research=True,registered_integration_andcredit_pending=True,new_credit=0,guide_photos=False))
    print('330 five-gate research decisions(174 revisions/156 retentions);336 pages/five captions/16 names.75 speeches observed/250 offline-only;integration pending.')

if __name__=='__main__':main()
