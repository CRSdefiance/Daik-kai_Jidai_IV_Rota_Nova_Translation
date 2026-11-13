"""Bind all 67 review gates to exact offline and representative gameplay evidence."""
from collections import Counter
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

A=Path('work/analysis')
ROOT=A/'Rafael_B161_B165_research_final_v1_20261105'
REBUILT=A/'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json'
STORED=A/'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json'
CATALOGUE=A/'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json'
LOADERS=A/'Rafael_B161_B165_loaders_v1_20261105/verification.json'
OFFLINE=A/'Rafael_B161_B165_storage_inputs_v1_20261105/visual_review.json'
FIXTURE=A/'Rafael_B161_B165_actual_fixtures_v1_20261105/mediterranean_story_and_audiences_fixture.json'
TERMINAL=A/'Rafael_B161_B165_actual_run_v1_20261105/terminal.json'
PIXELS=A/'Rafael_B161_B165_actual_pixels_v1_20261105/focused_actual_pixels.json'
SHEETS=A/'Rafael_B161_B165_actual_compact_v1_20261105/receipt.json'
NAMES=Path('translations/rafael_B161_B165_scoped_names_review_v1.json')
FINAL=Path('translations/rafael_B161_B165_final_review_v1.json')
FINAL_NAMES=Path('translations/rafael_B161_B165_scoped_names_final_v1.json')
PASSES=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)


def digest(p):
    return sha(Path(p).read_bytes())


def main():
    assert not any(p.exists() for p in (ROOT,FINAL,FINAL_NAMES))
    rebuilt,stored,lookup,loaders,visual,fixture,terminal,pixels,sheets,names=map(load,
        [REBUILT,STORED,CATALOGUE,LOADERS,OFFLINE,FIXTURE,TERMINAL,PIXELS,SHEETS,NAMES])
    doc_path,plan_path,native_path,menu_path,styles_path=map(Path,
        [rebuilt[k] for k in ('manuscript','plan','native','menu','styles')])
    doc,plan,native,menu,styles=map(load,[doc_path,plan_path,native_path,menu_path,styles_path])
    assert native['manuscript_sha256']==plan['manuscript_sha256']==rebuilt['manuscript_sha256']==digest(doc_path)
    assert native['plan_sha256']==rebuilt['plan_sha256']==digest(plan_path) and not plan['failures']
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(REBUILT)
    assert stored['native_sha256']==rebuilt['native_sha256']==visual['native_sha256']==digest(native_path)
    assert lookup['stored_sha256']==digest(STORED)
    assert native['runtime']==stored['runtime']==lookup['runtime']==menu['runtime']==styles['runtime']==names['runtime']
    assert len(doc['records'])==len(stored['records'])==len(lookup['records'])==67
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert native['pages']==stored['complete_stored_pages']==visual['body_pages']==68
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(36,32,100)
    assert len(stored['relative_cases'])==20 and rebuilt['relative_sites']==20
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,10,676)
    assert not menu['menus'] and not styles['objects'] and not fixture['menus']
    assert visual['all_body_and_name_sheets_directly_viewed'] and visual['scoped_name_count']==8
    assert terminal['terminal'] and terminal['frames']==pixels['frames']==fixture['frames']==18401
    assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert pixels['all_selected_pages_observed_in_exact_fixture_order']
    assert not any(pixels[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    assert all(digest(p)==h for p,h in pixels['evidence'].items())
    assert sheets['actual_pixel_proof_sha256']==digest(PIXELS) and sheets['actual_dialogue_pages']==56
    review_sheets=visual['sheets']+sheets['bottom_screen_sheets']+sheets['full_scene_sheets']
    assert len(visual['sheets'])==9 and all(digest(s['path'])==s['sha256'] for s in review_sheets)
    actors={r['actor_ID'] for r in pixels['headers']}
    assert actors=={r['actor_ID'] for r in names['records']}=={0,4,5,8,120,125,132,163}

    archive=Path(rebuilt['target_archive']).read_bytes()
    assert sha(archive)==rebuilt['target_archive_sha256'] and digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']==fixture['parent_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    b0={r['id']:r for r in stored['records']}
    b1={r['id']:r for r in native['records']}
    plans={r['id']:r for r in plan['records']}
    groups={g['block']:g for g in rebuilt['groups']}
    copied={r['fixture_offset']:r for r in fixture['copied_commands']}
    samples={}
    for s in pixels['body_pages']:
        samples.setdefault((s['id'],s['page']),s)
    observed={r['id'] for r in fixture['selected_records']}
    assert len(observed)==55 and len(samples)==56 and len(set(b0)-observed)==12
    for r in fixture['selected_records']:
        key=r['id'];s,n=b0[key],b1[key]
        assert (s['stored_hex'],s['expanded_hex'])==(r['stored_hex'],r['expected_expanded_body_hex'])
        command=next(c for c in groups[r['block']]['all_target_commands'] if c['offset']==s['new_offset']-5)
        assert copied[r['fixture_offset']]['whole_command_hex']==command['whole_command_hex']
        display=n['complete_native_English_display']
        for i,page in enumerate([display] if r['selector']==254 else display['pages'],1):
            match=samples[(key,i)]
            assert digest(match['capture']['path'])==match['capture']['PNG_sha256']
            assert match['native_plane_sha256']==page['native_plane_sha256']
            assert match['text_hex']==bytes.fromhex(s['expanded_hex'])[page.get('start',0):].hex()
    assert b'Castor Co., I see.' in bytes.fromhex(b0['DK4_MES_B162_R0006']['expanded_hex'])
    assert ('DK4_MES_B165_R0016',2) in samples
    for r in doc['records']:
        assert r['review']==PASSES
        k=r['id'];s=b0[k];at=s['new_offset'];raw=bytes.fromhex(s['stored_hex']);block=blocks[r['block']]
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert block[at:at+len(raw)+1]==raw+b'\0'
        r.update(planned_English_markup=plans[k]['formatted_markup'],
            planned_integrated_reference=dict(file_path=r['file_path'],block=r['block'],offset=at,header_offset=at-5,
                record_index=s['new_record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=sha(archive)),
            actual_utterance_observed_in_disclosed_fixture=k in observed,
            fresh_formatting_binding_pending=False,registered_release_and_completion_credit_pending=True,
            review={**PASSES,'formatting':True})
    assert Counter(r['decision'] for r in doc['records'])=={'revision':51,'retention':16}
    for r in names['records']:
        assert r['review']==PASSES
        r['review']['formatting']=True
        r['actual_header_observed_in_disclosed_fixture']=True

    ROOT.mkdir()
    visual_path,actual_path,release_plan=[ROOT/n for n in ('complete_visual_approval.json','actual_review.json','release_plans.json')]
    evidence={str(p):digest(p) for p in [REBUILT,STORED,CATALOGUE,LOADERS,OFFLINE,FIXTURE,TERMINAL,PIXELS,SHEETS,NAMES,
        doc_path,plan_path,native_path,menu_path,styles_path,Path(__file__)]}
    save(visual_path,dict(body_pages=68,scoped_public_names=8,observed_pages=56,typed_labels=0,
        all_body_and_name_planes_approved=True,all_actual_pages_directly_viewed=True,reviewed_sheets=review_sheets,
        evidence=evidence,new_credit=0,guide_photos=False))
    save(actual_path,dict(total_frames=18401,initialized_fixture_runs=1,source_speech_variants_observed=55,
        native_body_pages_observed=56,actual_choice_labels=0,offline_only_speech_variants=12,
        source_IDs_observed=sorted(observed),offline_only_source_IDs=sorted(set(b0)-observed),
        exact_observed_pages=[dict(id=r['id'],page=r['page'],frame=r['frame'],capture=r['capture']) for r in samples.values()],
        observed_public_name_actor_IDs=sorted(actors),menus=[],all_four_menus_default_cursor_andfollowing_fixture_speech_observed=False,
        no_typed_menus_in_scope=True,original_story_branches_and_event_outcomes_unvisited=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    names.update(all_name_formatting_gates_pending=False,all_individual_five_gates_pass_for_public_nameplanes=True,
        actual_review=str(actual_path),actual_review_sha256=digest(actual_path))
    validate_natural_dialogue_batch(names)
    save(FINAL_NAMES,names)
    doc.update(all_fifth_formatting_gates_pending=False,all_individual_five_gates_pass=True,
        native_macro_tokens_still_require_formatter_marking=False,
        no_new_formatting_rendering_gameplay_orregistered_integration_claim=False,only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=68,actual_source_speech_variants=55,actual_body_pages=56,offline_only_source_speech_variants=12,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=digest(FINAL_NAMES),
        parent_manuscript=str(doc_path),parent_manuscript_sha256=digest(doc_path),registered_release_and_completion_credit_pending=True,
        formatting_evidence=dict(native=str(native_path),stored=str(STORED),catalogue=str(CATALOGUE),loaders=str(LOADERS),
            visual=str(visual_path),actual=str(actual_path)))
    validate_natural_dialogue_batch(doc)
    save(FINAL,doc)
    plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),exact_all_prose_and_compiled_bytes_unchanged=True)
    save(release_plan,plan)
    save(ROOT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),plan=str(release_plan),
        plan_sha256=digest(release_plan),all_individual_five_gates_pass=True,records=67,revisions=51,retentions=16,
        body_pages=68,typed_labels=0,scoped_public_names=8,actual_source_variants=55,actual_pages=56,offline_only_source_variants=12,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in [FINAL,FINAL_NAMES,release_plan,visual_path,actual_path]}}))
    print('Sealed all 67 five-gate reviews, 55 observed speeches, 56 observed pages and eight public headers.')


if __name__=='__main__':
    main()
