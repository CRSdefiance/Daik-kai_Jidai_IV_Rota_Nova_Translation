"""Bind all five tutorial review gates to the exact stored and observed records."""
from collections import Counter
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

A = Path('work/analysis')
ROOT = A / 'Rafael_B177_B180_research_final_v1_20261105'
REBUILT = A / 'Rafael_B177_B180_reconstruction_v2_20261105/reconstruction.json'
STORED = A / 'Rafael_B177_B180_storage_inputs_v1_20261105/stored_speeches_and_menus.json'
CATALOGUE = A / 'Rafael_B177_B180_stored_catalogue_v1_20261105/all175_stored_effective_body_bindings.json'
LOADERS = A / 'Rafael_B177_B180_loaders_v1_20261105/verification.json'
NAMES = Path('translations/rafael_B177_B180_scoped_names_review_v1.json')
PLANES = A / 'Rafael_B177_B180_name_planes_v1_20261105/native_name_planes.json'
SHEETS = A / 'Rafael_B177_B180_actual_compact_v1_20261105/receipt.json'
FINAL = Path('translations/rafael_B177_B180_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B177_B180_scoped_names_final_v1.json')


def digest(path):
    return sha(Path(path).read_bytes())


def bind_actual(rebuilt, stored, native, sheet_proof):
    actual_pages, live_menus, actors, proof_paths, menu_sheets = {}, [], set(), [], []
    native_by_id = {r['id']:r for r in native['records']}
    stored_by_id = {r['id']:r for r in stored['records']}
    groups = {g['block']:g for g in rebuilt['groups']}
    total_frames = 0
    for name, menu_version in [('ship',2),('coin',1)]:
        body_path = A / f'Rafael_B177_B180_{name}_body_pixels_v1_20261105/focused_actual_pixels.json'
        menu_path = A / f'Rafael_B177_B180_{name}_menu_pixels_v{menu_version}_20261105/menu_actual_pixels.json'
        body, menu = map(load, [body_path, menu_path])
        fixture, terminal = map(load, [menu['fixture'],menu['terminal']])
        assert digest(menu['fixture']) == menu['fixture_sha256'] and digest(menu['terminal']) == menu['terminal_sha256']
        assert fixture['parent_sha256'] == rebuilt['research_ROM_sha256'] and terminal['terminal']
        assert terminal['frames'] == body['frames'] == menu['frames'] == fixture['frames']
        assert body['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert body['all_selected_pages_observed_in_exact_fixture_order']
        assert not any(body[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        assert all(digest(p) == h for p,h in body['evidence'].items())
        assert sheet_proof['source_proofs'][str(body_path)] == digest(body_path)
        proof_paths.extend([body_path,menu_path,Path(menu['fixture']),Path(menu['terminal'])])
        total_frames += fixture['frames']
        by_offset = {c['fixture_offset']:c for c in fixture['copied_commands']}
        for row in fixture['selected_records']:
            ident = row['id']
            s,n = stored_by_id[ident],native_by_id[ident]
            assert (s['stored_hex'],s['expanded_hex']) == (row['stored_hex'],row['expected_expanded_body_hex'])
            command = next(c for c in groups[s['block']]['all_target_commands'] if c['offset'] == s['new_offset']-5)
            assert command['whole_command_hex'] == by_offset[row['fixture_offset']]['whole_command_hex']
            display = n['complete_native_English_display']
            pages = [display] if row['selector']==254 else display['pages']
            for number,page in enumerate(pages,1):
                key = ident,number
                assert key not in actual_pages
                sample = next(v for v in body['body_pages'] if (v['id'],v['page']) == key)
                assert sample['native_plane_sha256'] == page['native_plane_sha256']
                assert sample['text_hex'] == bytes.fromhex(s['expanded_hex'])[page.get('start',0):].hex()
                assert digest(sample['capture']['path']) == sample['capture']['PNG_sha256']
                actual_pages[key] = dict(id=ident,page=number,proof=str(body_path),capture=sample['capture'],frame=sample['frame'])
        actors.update(h['actor_ID'] for h in body['headers'])
        assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert menu['numeric_modal_return_register_original_story_branches_andcancellation_unvisited']
        controls = load(fixture['inputs'])
        assert digest(fixture['inputs']) == fixture['inputs_sha256']
        for obj in menu['menus']:
            decl = next(m for m in fixture['menus'] if m['stored_command_offset']==obj['source_command_offset'])
            final = next(m for m in stored['typed_objects'] if m['block']==decl['block'])
            assert final['offset']==decl['stored_command_offset'] and final['object_hex']==decl['command_hex']
            assert obj['observed_selected_options']==[0] and obj['count']==2
            sample = next(m for m in menu['menu_samples'] if m['source_command_offset']==final['offset'] and m['visible_selected_option']==0)
            following = next(s for s in fixture['selected_records'] if s['fixture_offset']>decl['fixture_offset'])
            after = next(s for s in body['ordered_selected_source_calls'] if s['id']==following['id'] and s['page']==1)
            assert any('A' in r['buttons'] and sample['frame']<=r['start']<=after['frame'] for r in controls)
            live_menus.append(dict(block=final['block'],offset=final['offset'],labels=final['labels'],visible_cursor=0,
                menu_frame=sample['frame'],ordinary_A_following_fixture_speech=following['id'],following_frame=after['frame'],
                proof=str(menu_path)))
        menu_sheets.append(menu['review_sheet'])
    observed = {key[0] for key in actual_pages}
    assert (total_frames,len(observed),len(actual_pages),len(live_menus),len(actors)) == (38482,104,115,4,9)
    assert {r['block'] for r in live_menus} == {177,178,179,180}
    assert {'DK4_MES_B177_R0114','DK4_MES_B178_R0064','DK4_MES_B178_R0131','DK4_MES_B179_R0122','DK4_MES_B180_R0096'} <= observed
    return observed, actual_pages, live_menus, actors, proof_paths, menu_sheets


def main():
    assert not any(p.exists() for p in (ROOT,FINAL,FINAL_NAMES))
    rebuilt,stored,lookup,loaders,names,name_planes,previews = map(load,[REBUILT,STORED,CATALOGUE,LOADERS,NAMES,PLANES,SHEETS])
    doc_path,plan_path,native_path,menu_path,styles_path = map(Path,
        [rebuilt[k] for k in ('manuscript','plan','native','menu','styles')])
    doc,plan,native,menu,styles = map(load,[doc_path,plan_path,native_path,menu_path,styles_path])
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(REBUILT)
    assert stored['native_sha256']==rebuilt['native_sha256']==digest(native_path)
    assert stored['speech_proof_sha256']==lookup['stored_sha256']==digest(stored['speech_proof'])
    assert native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==name_planes['runtime']
    assert plan['manuscript_sha256']==rebuilt['manuscript_sha256']==digest(doc_path)
    assert native['plan_sha256']==rebuilt['plan_sha256']==digest(plan_path) and not plan['failures']
    assert native['all_final_186_body_pages_directly_viewed'] and native['all_16_reviewed_caption_style_planes_directly_viewed']
    assert native['pages']==stored['complete_stored_pages']==186
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['fresh_relocated_native_relative_cases']==290 and len(stored['relative_cases'])==58
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,8,678)
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert len(lookup['records'])==len(native['records'])==len(stored['records'])==175
    assert stored['typed_labels_checked']==8 and len(stored['typed_objects'])==4 and not styles['objects']
    assert name_planes['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert len(name_planes['planes'])==len(names['records'])==9
    observed,pages,menus,actors,actual_proofs,menu_sheets=bind_actual(rebuilt,stored,native,previews)
    sheets=previews['sheets']+menu_sheets+name_planes['review_sheets']
    assert len(sheets)==13 and sum(s['pages'] for s in previews['sheets'])==115
    assert all(digest(s['path'])==s['sha256'] for s in sheets)
    assert actors=={r['actor_ID'] for r in names['records']}

    archive=Path(rebuilt['target_archive']).read_bytes()
    assert sha(archive)==rebuilt['target_archive_sha256'] and digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    speech={r['id']:r for r in stored['records']}
    captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    layouts={r['id']:r for r in plan['records']}
    assert len(speech)-len(observed)==71 and set(speech)|set(captions)=={r['id'] for r in doc['records']}
    for r in doc['records']:
        assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        ident,b=r['id'],r['block']
        if ident in speech:
            s=speech[ident];at=s['new_offset'];raw=bytes.fromhex(s['stored_hex'])
            assert blocks[b][at-5:at+1].hex()==r['source_complete_preamble_hex']
            ref=dict(offset=at,header_offset=at-5,record_index=s['new_record_index'])
            r['planned_English_markup']=layouts[ident]['formatted_markup']
            r['actual_utterance_observed_in_disclosed_fixture']=ident in observed
        else:
            o,s=captions[ident];at=s['offset'];raw=bytes.fromhex(s['stored_hex'])
            assert o['block']==b and raw.decode('ascii')==r['english']
            ref=dict(offset=at,command_offset=o['offset'],source_index=s['source_index'],record_index=s['record_index'])
            r.update(actual_caption_default_cursor_state_observed=True,other_cursor_and_return_cases_verified_offline=True)
        assert blocks[b][at:at+len(raw)+1]==raw+b'\0'
        r['planned_integrated_reference']=dict(**ref,file_path=r['file_path'],block=b,exact_stored_hex=raw.hex(),
            target_archive_sha256=sha(archive))
        r['review']['formatting']=True
        r['fresh_formatting_binding_pending']=False
        r['registered_release_and_completion_credit_pending']=True
    assert Counter(r['decision'] for r in doc['records'])=={'revision':133,'retention':50}
    for r in names['records']:
        assert not r['review']['formatting']
        r['review']['formatting']=True
        r['actual_header_observed_in_disclosed_fixture']=True
    ROOT.mkdir()
    visual,actual,release_plan = [ROOT/name for name in ('complete_visual_approval.json','actual_review.json','release_plans.json')]
    evidence={str(path):digest(path) for path in [REBUILT,STORED,CATALOGUE,LOADERS,NAMES,PLANES,SHEETS,
        doc_path,plan_path,native_path,menu_path,styles_path,*actual_proofs,Path(__file__)]}
    save(visual,dict(body_pages=186,reviewed_caption_planes=16,scoped_public_names=9,observed_pages=115,
        all_body_caption_andname_planes_approved=True,all_actual_pages_andmenus_directly_viewed=True,
        actual_and_name_sheets=sheets,evidence=evidence,new_credit=0,guide_photos=False))
    save(actual,dict(total_frames=38482,initialized_fixture_runs=2,source_speech_variants_observed=104,
        native_body_pages_observed=115,actual_choice_labels=8,offline_only_speech_variants=71,
        source_IDs_observed=sorted(observed),offline_only_source_IDs=sorted(set(speech)-observed),
        exact_observed_pages=list(pages.values()),observed_public_name_actor_IDs=sorted(actors),menus=menus,
        all_four_menus_default_cursor_andfollowing_fixture_speech_observed=True,
        other_cursor_states_VM_returns_branches_andcancellation_offline_only=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    names.update(all_name_formatting_gates_pending=False,all_individual_five_gates_pass_for_public_nameplanes=True,
        actual_review=str(actual),actual_review_sha256=digest(actual))
    validate_natural_dialogue_batch(names)
    save(FINAL_NAMES,names)
    doc.update(all_fifth_formatting_gates_pending=False,all_individual_five_gates_pass=True,
        native_macro_tokens_still_require_formatter_marking=False,
        no_new_formatting_rendering_gameplay_orregistered_integration_claim=False,only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=186,actual_source_speech_variants=104,actual_body_pages=115,offline_only_source_speech_variants=71,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=digest(FINAL_NAMES),
        parent_manuscript=str(doc_path),parent_manuscript_sha256=digest(doc_path),registered_release_and_completion_credit_pending=True,
        formatting_evidence=dict(native=str(native_path),stored=str(STORED),catalogue=str(CATALOGUE),loaders=str(LOADERS),
            visual=str(visual),actual=str(actual)))
    validate_natural_dialogue_batch(doc)
    save(FINAL,doc)
    plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),exact_all_prose_andcompiled_bytes_unchanged=True)
    save(release_plan,plan)
    save(ROOT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),
        plan=str(release_plan),plan_sha256=digest(release_plan),all_individual_five_gates_pass=True,
        records=183,revisions=133,retentions=50,body_pages=186,typed_labels=8,scoped_public_names=9,
        actual_source_variants=104,actual_pages=115,offline_only_source_variants=71,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in [FINAL,FINAL_NAMES,release_plan,visual,actual]}}))
    print('Sealed all 183 five-gate reviews, 104 observed speeches, 115 observed pages, four menus and nine public headers.')


if __name__ == '__main__':
    main()
