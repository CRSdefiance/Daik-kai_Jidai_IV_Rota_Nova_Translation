"""Seal all five gates against the stored and observed Rafael B201–B220 evidence."""
from collections import Counter
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT as SOURCE, digest
from scripts.write_rafael_B201_B220_contextual_v1 import LABELS


ROOT=Path('work/analysis/Rafael_B201_B220_research_final_v1_20261106')
REBUILT=SOURCE/'reconstruction_v1/reconstruction.json'
STORED=SOURCE/'stored_native_v1/stored_native_verification.json'
CATALOGUE=SOURCE/'stored_catalogue_v1/all382_stored_effective_body_bindings.json'
LOADERS=SOURCE/'loaders_v1/verification.json'
VISUAL=SOURCE/'offline_display_package_v2/visual_review.json'
SELECTION=SOURCE/'focused_selection_v1.json'
MENUS=SOURCE/'actual_menu_pixels_v1/menu_actual_pixels.json'
FINAL=Path('translations/rafael_B201_B220_final_review_v1.json')
FINAL_NAMES=Path('translations/rafael_B201_B220_scoped_names_final_v1.json')
RUNS={'town':('rafael_town_forecasts',57,57,18641),'letter':('rafael_letter_and_parrot',75,75,22961),
      'menus':('rafael_merchants_and_choices',41,42,16481)}
PASSES=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)


def checksum(path):
    return digest(Path(path))


def main():
    assert not any(p.exists() for p in (ROOT,FINAL,FINAL_NAMES))
    rebuilt,stored,lookup,loaders,visual,selection,menus,names=map(load,
        (REBUILT,STORED,CATALOGUE,LOADERS,VISUAL,SELECTION,MENUS,LABELS))
    paths=[Path(rebuilt[k]) for k in ('manuscript','plan','native','menu','styles')]
    manuscript,plan,native,menu,styles=map(load,paths)
    doc_path,plan_path,native_path,_,_=paths
    assert rebuilt['manuscript_sha256']==plan['manuscript_sha256']==native['manuscript_sha256']==checksum(doc_path)
    assert rebuilt['plan_sha256']==native['plan_sha256']==checksum(plan_path)
    assert not plan['failures'] and all(q['severity']=='info' for r in plan['records'] for q in r['base_QA']['issues'])
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==checksum(REBUILT)
    assert stored['native_sha256']==rebuilt['native_sha256']==visual['native_sha256']==checksum(native_path)
    assert lookup['stored_sha256']==checksum(STORED) and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==names['runtime']
    assert len(manuscript['records'])==403 and len(stored['records'])==len(lookup['records'])==382
    assert native['pages']==stored['complete_stored_pages']==visual['body_pages']==383
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(188,195,520)
    assert len(stored['relative_cases'])==rebuilt['relative_sites']==104
    assert rebuilt['changed_blocks']==list(range(201,221)) and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,40,646)
    assert len(menu['menus'])==10 and not styles['objects'] and stored['typed_labels_checked']==21
    assert visual['all_final_body_caption_and_name_sheets_directly_viewed'] and visual['scoped_name_count']==41
    archive=Path(rebuilt['target_archive']).read_bytes()
    assert checksum(rebuilt['target_archive'])==rebuilt['target_archive_sha256'] and checksum(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    speech={r['id']:r for r in stored['records']}
    captions={r['id']:(item,r) for item in stored['typed_objects'] for r in item['label_references']}
    layouts={r['id']:r for r in plan['records']}
    native_by_id={r['id']:r for r in native['records']}
    groups={g['block']:g for g in rebuilt['groups']}
    sheets=list(visual['sheets'])
    observed_pages,actors,actual_paths={},set(),[]
    total_frames=0
    for tag,(name,utterances,page_count,frames) in RUNS.items():
        fixture_path=SOURCE/'actual_fixtures_v1'/f'{name}_fixture.json'
        terminal_path=SOURCE/f'actual_run_{tag}/terminal.json'
        pixels_path=SOURCE/f'actual_pixels_{tag}_v1/focused_actual_pixels.json'
        actual_paths.extend((fixture_path,terminal_path,pixels_path))
        fixture,terminal,pixels=map(load,(fixture_path,terminal_path,pixels_path))
        assert terminal['terminal'] and terminal['frames']==fixture['frames']==pixels['frames']==frames
        assert fixture['parent_sha256']==rebuilt['research_ROM_sha256']
        assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixels['all_selected_pages_observed_in_exact_fixture_order']
        assert not any(pixels[k] for k in ('natural_activation','original_location','earned_chronology','full_route','hardware'))
        assert all(checksum(p)==h for p,h in pixels['evidence'].items())
        actors.update(pixels['observed_actor_IDs'])
        total_frames+=frames
        sheets.extend(pixels['review_sheets'])
        copied={c['fixture_offset']:c for c in fixture['copied_commands']}
        selected={r['id']:r for r in fixture['selected_records']}
        by_page={}
        for sample in pixels['body_pages']:
            by_page.setdefault((sample['id'],sample['page']),sample)
        assert len(selected)==utterances and len(by_page)==page_count
        assert not observed_pages.keys()&by_page.keys()
        assert [r['id'] for r in pixels['ordered_selected_source_calls']]==[
            ident for ident in selected for _ in range(layouts[ident]['expected_native_pages'])]
        for ident,row in selected.items():
            s,n=speech[ident],native_by_id[ident]
            assert (s['stored_hex'],s['expanded_hex'])==(row['stored_hex'],row['expected_expanded_body_hex'])
            command=next(c for c in groups[s['block']]['all_target_commands'] if c['offset']==s['new_offset']-5)
            assert command['whole_command_hex']==copied[row['fixture_offset']]['whole_command_hex']
            display=n['complete_native_English_display']
            pages=[display] if row['selector']==254 else display['pages']
            for number,page in enumerate(pages,1):
                sample=by_page[ident,number]
                assert sample['native_plane_sha256']==page['native_plane_sha256']
                assert checksum(sample['capture']['path'])==sample['capture']['PNG_sha256']
                assert sample['text_hex']==bytes.fromhex(s['expanded_hex'])[page.get('start',0):].hex()
        observed_pages.update(by_page)
    observed={ident for ident,_ in observed_pages}
    assert len(observed)==173 and len(observed_pages)==174 and total_frames==58083
    assert observed==set(selection['source_variant_IDs'])
    assert actors==set(selection['ordinary_actor_IDs'])
    assert len(speech)-len(observed)==209
    assert menus['ordinary_A_return_to_next_fixture_speech_observed']
    assert menus['observed_each_menu_between_its_own_exact_preceding_and_following_speech']
    assert len(menus['menus'])==6 and menus['complete_live_caption_samples']==12
    assert all(m['observed_selected_options']==[0] for m in menus['menus'])
    seen_menus={(m['block'],m['clean_source_command_offset']) for m in menus['menus']}
    assert seen_menus=={(m['block'],m['source_command_offset']) for m in selection['menus']}
    viewed_labels={ident for m in menu['menus'] if (m['block'],m['source_command_offset']) in seen_menus for ident in m['record_IDs']}
    assert len(viewed_labels)==13 and len(captions)-len(viewed_labels)==8
    sheets.append(menus['review_sheet'])
    assert len(sheets)==35 and all(checksum(s['path'])==s['sha256'] for s in sheets)
    for row in manuscript['records']:
        assert row['review']==PASSES
        ident,block=row['id'],row['block']
        if ident in speech:
            s=speech[ident]
            offset=s['new_offset']
            assert blocks[block][offset-5:offset+1].hex()==row['source_complete_preamble_hex']
            ref=dict(offset=offset,header_offset=offset-5,record_index=s['new_record_index'])
            row.update(planned_English_markup=layouts[ident]['formatted_markup'],
                actual_utterance_observed_in_disclosed_fixture=ident in observed)
            if row['kind']=='system-FE':
                row.update(native_FE_presentation_binding_pending=False,original_event_background_unvisited=True)
        else:
            menu_object,s=captions[ident]
            offset=s['offset']
            assert menu_object['block']==block and bytes.fromhex(s['stored_hex']).decode('ascii')==row['english']
            ref=dict(offset=offset,command_offset=menu_object['offset'],source_index=s['source_index'],record_index=s['record_index'])
            row.update(actual_caption_default_cursor_state_observed=ident in viewed_labels,
                other_cursor_and_return_cases_verified_offline=True,complete_native_menu_binding_andformatting_pending=False)
        raw=bytes.fromhex(s['stored_hex'])
        assert blocks[block][offset:offset+len(raw)+1]==raw+b'\0'
        row.update(planned_integrated_reference=dict(**ref,file_path=row['file_path'],block=block,
            exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256']),
            review={**PASSES,'formatting':True},fresh_formatting_binding_pending=False,
            registered_release_and_completion_credit_pending=True)
    assert Counter(r['decision'] for r in manuscript['records'])=={'revision':299,'retention':104}
    assert len(names['records'])==41
    for row in names['records']:
        assert row['review']==PASSES
        row.update(review={**PASSES,'formatting':True},actual_header_observed_in_disclosed_fixture=row['actor_ID'] in actors)

    ROOT.mkdir()
    vis,actual,release_plan=[ROOT/name for name in ('complete_visual_approval.json','actual_review.json','release_plans.json')]
    evidence={str(p):checksum(p) for p in (REBUILT,STORED,CATALOGUE,LOADERS,VISUAL,LABELS,SELECTION,MENUS,*paths,*actual_paths,Path(__file__))}
    save(vis,dict(body_pages=383,reviewed_caption_planes=42,scoped_public_names=41,observed_pages=174,typed_labels=21,
        all_body_and_name_planes_approved=True,all_body_caption_andname_planes_approved=True,
        all_actual_pages_directly_viewed=True,all_actual_pages_and_menus_directly_viewed=True,
        reviewed_sheets=sheets,evidence=evidence,new_credit=0,guide_photos=False))
    seen_fe={r['id'] for r in manuscript['records'] if r['kind']=='system-FE'} & observed
    save(actual,dict(total_frames=total_frames,initialized_fixture_runs=3,source_speech_variants_observed=173,
        native_body_pages_observed=174,actual_choice_labels=13,offline_only_speech_variants=209,offline_only_caption_count=8,
        source_IDs_observed=sorted(observed),offline_only_source_IDs=sorted(set(speech)-observed),
        exact_observed_pages=[dict(id=s['id'],page=s['page'],frame=s['frame'],capture=s['capture']) for s in observed_pages.values()],
        observed_public_name_actor_IDs=sorted(actors),observed_FE_source_IDs=sorted(seen_fe),all_seven_town_forecasts_observed=True,
        menus=menus['menus'],all_six_menu_instances_default_cursor_and_following_fixture_speech_observed=True,
        other_cursor_states_VM_returns_branches_andcancellation_offline_only=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    names.update(all_name_formatting_gates_pending=False,all_individual_five_gates_pass_for_public_nameplanes=True,
        actual_review=str(actual),actual_review_sha256=checksum(actual))
    validate_natural_dialogue_batch(names)
    save(FINAL_NAMES,names)
    manuscript.update(all_fifth_formatting_gates_pending=False,all_individual_five_gates_pass=True,
        native_macro_tokens_still_require_formatter_marking=False,only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=383,actual_source_speech_variants=173,actual_body_pages=174,offline_only_source_speech_variants=209,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=checksum(FINAL_NAMES),
        parent_manuscript=str(doc_path),parent_manuscript_sha256=checksum(doc_path),registered_release_and_completion_credit_pending=True,
        formatting_evidence=dict(native=str(native_path),stored=str(STORED),catalogue=str(CATALOGUE),loaders=str(LOADERS),
            visual=str(vis),actual=str(actual)))
    validate_natural_dialogue_batch(manuscript)
    save(FINAL,manuscript)
    save(release_plan,{**plan,'manuscript':str(FINAL),'manuscript_sha256':checksum(FINAL),
        'exact_all_prose_and_compiled_bytes_unchanged':True})
    save(ROOT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=checksum(FINAL),plan=str(release_plan),
        plan_sha256=checksum(release_plan),all_individual_five_gates_pass=True,records=403,revisions=299,retentions=104,
        body_pages=383,typed_labels=21,scoped_public_names=41,actual_source_variants=173,actual_pages=174,
        actual_choice_labels=13,actual_menus=6,actual_name_headers=len(actors),offline_only_source_variants=209,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):checksum(p) for p in (FINAL,FINAL_NAMES,release_plan,vis,actual)}}))
    print('Sealed all 403 five-gate reviews, 174 observed pages, 6 live menus, and',len(actors),'observed name headers.')


if __name__=='__main__':
    main()

