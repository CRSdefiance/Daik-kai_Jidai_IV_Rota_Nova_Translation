"""Seal all five gates against the exact stored and observed B181–B200 evidence."""
from collections import Counter
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B181_B187_story_v1 import NAMES, ROOT as SOURCE
from scripts.prepare_rafael_B181_B200_focus_v1 import SELECTION


ROOT = Path('work/analysis/Rafael_B181_B200_research_final_v1_20261106')
REBUILT = SOURCE/'reconstruction_v1/reconstruction.json'
STORED = SOURCE/'stored_native_v1/stored_native_verification.json'
CATALOGUE = SOURCE/'stored_catalogue_v1/all384_stored_effective_body_bindings.json'
LOADERS = SOURCE/'loaders_v1/verification.json'
OFFLINE = SOURCE/'offline_display_package_v1/visual_review.json'
FINAL = Path('translations/rafael_B181_B200_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B181_B200_scoped_names_final_v1.json')
RUNS = ('rafael_yifa_julian_aziza', 'rafael_town_forecasts')
PASSES = dict(source=True,context=True,localization=True,naturalness=True,formatting=False)


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not any(p.exists() for p in (ROOT,FINAL,FINAL_NAMES))
    rebuilt, stored, lookup, loaders, visual, names, selection = map(load,
        (REBUILT,STORED,CATALOGUE,LOADERS,OFFLINE,NAMES,SELECTION))
    paths = [Path(rebuilt[k]) for k in ('manuscript','plan','native','menu','styles')]
    doc,plan,native,menu,styles = map(load,paths)
    doc_path,plan_path,native_path,_,_ = paths
    assert native['manuscript_sha256']==plan['manuscript_sha256']==rebuilt['manuscript_sha256']==digest(doc_path)
    assert native['plan_sha256']==rebuilt['plan_sha256']==digest(plan_path) and not plan['failures']
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(REBUILT)
    assert stored['native_sha256']==rebuilt['native_sha256']==visual['native_sha256']==digest(native_path)
    assert lookup['stored_sha256']==digest(STORED) and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==names['runtime']
    assert len(doc['records'])==len(stored['records'])==len(lookup['records'])==384
    assert native['pages']==stored['complete_stored_pages']==visual['body_pages']==384
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(202,182,210)
    assert len(stored['relative_cases'])==rebuilt['relative_sites']==42
    assert rebuilt['changed_blocks']==list(range(181,201)) and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,40,646)
    assert not menu['menus'] and not styles['objects']
    assert visual['all_body_and_name_sheets_directly_viewed'] and visual['scoped_name_count']==29
    archive=Path(rebuilt['target_archive']).read_bytes()
    assert sha(archive)==rebuilt['target_archive_sha256'] and digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    b0,b1,plans=[{r['id']:r for r in p['records']} for p in (stored,native,plan)]
    groups={g['block']:g for g in rebuilt['groups']}
    actors,samples,fe=set(),{},set()
    review_sheets=list(visual['sheets'])
    actual_paths=[]
    total_frames=body_holds=header_holds=0
    for run,count,frames in zip(RUNS,(72,76),(22241,23201),strict=True):
        fixture_path=SOURCE/'actual_fixtures_v1'/f'{run}_fixture.json'
        terminal_path=SOURCE/f'actual_run_{run}'/'terminal.json'
        pixels_path=SOURCE/f'actual_pixels_{run}'/'focused_actual_pixels.json'
        sheets_path=SOURCE/f'actual_compact_{run}'/'receipt.json'
        actual_paths.extend((fixture_path,terminal_path,pixels_path,sheets_path))
        fixture,terminal,pixels,sheets=map(load,(fixture_path,terminal_path,pixels_path,sheets_path))
        assert not fixture['menus'] and terminal['terminal'] and terminal['frames']==pixels['frames']==fixture['frames']==frames
        assert fixture['parent_sha256']==rebuilt['research_ROM_sha256']
        assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixels['all_selected_pages_observed_in_exact_fixture_order']
        assert not any(pixels[k] for k in ('natural_activation','original_location','earned_chronology','full_route','hardware'))
        assert all(digest(p)==h for p,h in pixels['evidence'].items())
        assert sheets['actual_pixel_proof_sha256']==digest(pixels_path) and sheets['actual_dialogue_pages']==count
        review_sheets.extend(sheets['bottom_screen_sheets']+sheets['full_scene_sheets'])
        actors.update(r['actor_ID'] for r in pixels['headers'])
        body_holds+=pixels['complete_body_planes']
        header_holds+=pixels['complete_header_planes']
        total_frames+=frames
        copied={r['fixture_offset']:r for r in fixture['copied_commands']}
        chosen={r['id']:r for r in fixture['selected_records']}
        assert len(chosen)==count and [r['id'] for r in pixels['ordered_selected_source_calls']]==list(chosen)
        run_samples={}
        for sample in pixels['body_pages']:
            run_samples.setdefault(sample['id'],sample)
        assert set(run_samples)==set(chosen) and not set(run_samples)&set(samples)
        for ident,r in chosen.items():
            s,n=b0[ident],b1[ident]
            assert (s['stored_hex'],s['expanded_hex'])==(r['stored_hex'],r['expected_expanded_body_hex'])
            command=next(c for c in groups[r['block']]['all_target_commands'] if c['offset']==s['new_offset']-5)
            assert copied[r['fixture_offset']]['whole_command_hex']==command['whole_command_hex']
            display=n['complete_native_English_display']
            if r['selector']==254:
                fe.add(ident)
                page=display
            else:
                page,=display['pages']
            sample=run_samples[ident]
            assert sample['page']==1 and sample['native_plane_sha256']==page['native_plane_sha256']
            assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
            assert sample['text_hex']==s['expanded_hex']
        samples.update(run_samples)
    observed=set(samples)
    assert len(observed)==148 and len(set(b0)-observed)==236 and total_frames==45442
    assert (body_holds,header_holds)==(304,250)
    assert fe==set(selection['expected_FE_bodies'])=={r['id'] for r in doc['records'] if r['source_selector']==254}
    assert len(fe)==27 and actors=={r['actor_ID'] for r in names['records']}==set(selection['expected_ordinary_actor_IDs'])
    assert all(digest(s['path'])==s['sha256'] for s in review_sheets)
    for r in doc['records']:
        assert r['review']==PASSES
        ident=r['id'];s=b0[ident];at=s['new_offset'];raw=bytes.fromhex(s['stored_hex']);block=blocks[r['block']]
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and block[at:at+len(raw)+1]==raw+b'\0'
        r.update(planned_English_markup=plans[ident]['formatted_markup'],
            planned_integrated_reference=dict(file_path=r['file_path'],block=r['block'],offset=at,header_offset=at-5,
                record_index=s['new_record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=sha(archive)),
            actual_utterance_observed_in_disclosed_fixture=ident in observed,fresh_formatting_binding_pending=False,
            registered_release_and_completion_credit_pending=True,review={**PASSES,'formatting':True})
        if r.get('native_FE_presentation_binding_pending'):
            assert r['block']==187 and ident in fe
            r['native_FE_presentation_binding_pending']=False
            r['original_event_background_and_portrait_context_unvisited']=True
    assert Counter(r['decision'] for r in doc['records'])=={'revision':317,'retention':67}
    for r in names['records']:
        assert r['review']==PASSES
        r['review']['formatting']=True
        r['actual_header_observed_in_disclosed_fixture']=True
    ROOT.mkdir()
    visual_path,actual_path,release_plan=[ROOT/n for n in ('complete_visual_approval.json','actual_review.json','release_plans.json')]
    evidence={str(p):digest(p) for p in (REBUILT,STORED,CATALOGUE,LOADERS,OFFLINE,NAMES,SELECTION,*actual_paths,*paths,Path(__file__))}
    save(visual_path,dict(body_pages=384,scoped_public_names=29,observed_pages=148,typed_labels=0,
        all_body_and_name_planes_approved=True,all_actual_pages_directly_viewed=True,reviewed_sheets=review_sheets,
        evidence=evidence,new_credit=0,guide_photos=False))
    save(actual_path,dict(total_frames=45442,initialized_fixture_runs=2,source_speech_variants_observed=148,
        native_body_pages_observed=148,actual_choice_labels=0,offline_only_speech_variants=236,
        source_IDs_observed=sorted(observed),offline_only_source_IDs=sorted(set(b0)-observed),
        exact_observed_pages=[dict(id=s['id'],page=s['page'],frame=s['frame'],capture=s['capture']) for s in samples.values()],
        observed_public_name_actor_IDs=sorted(actors),complete_body_holds=body_holds,complete_header_holds=header_holds,
        observed_FE_source_IDs=sorted(fe),all27_FE_bodies_observed=True,all13_town_forecasts_observed=True,
        menus=[],no_typed_menus_in_scope=True,original_story_branches_and_event_outcomes_unvisited=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    names.update(all_name_formatting_gates_pending=False,all_individual_five_gates_pass_for_public_nameplanes=True,
        actual_review=str(actual_path),actual_review_sha256=digest(actual_path))
    validate_natural_dialogue_batch(names)
    save(FINAL_NAMES,names)
    doc.update(all_fifth_formatting_gates_pending=False,all_individual_five_gates_pass=True,
        native_macro_tokens_still_require_formatter_marking=False,only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=384,actual_source_speech_variants=148,actual_body_pages=148,offline_only_source_speech_variants=236,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=digest(FINAL_NAMES),
        parent_manuscript=str(doc_path),parent_manuscript_sha256=digest(doc_path),registered_release_and_completion_credit_pending=True,
        formatting_evidence=dict(native=str(native_path),stored=str(STORED),catalogue=str(CATALOGUE),loaders=str(LOADERS),
            visual=str(visual_path),actual=str(actual_path)))
    validate_natural_dialogue_batch(doc)
    save(FINAL,doc)
    plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),exact_all_prose_and_compiled_bytes_unchanged=True)
    save(release_plan,plan)
    save(ROOT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),plan=str(release_plan),
        plan_sha256=digest(release_plan),all_individual_five_gates_pass=True,records=384,revisions=317,retentions=67,
        body_pages=384,typed_labels=0,scoped_public_names=29,actual_source_variants=148,actual_pages=148,offline_only_source_variants=236,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in (FINAL,FINAL_NAMES,release_plan,visual_path,actual_path)}}))
    print('Sealed all 384 five-gate reviews. Actual 148 pages and 29 labels; 236 speeches remain offline only.')


if __name__=='__main__':
    main()
