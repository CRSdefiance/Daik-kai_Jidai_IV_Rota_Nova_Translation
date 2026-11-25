"""Seal the 557 research gates with exact current storage and representative capture bindings."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

A=Path('work/analysis')
ROOT=A/'Rafael557_research_final_v1_20261105'
REBUILT=A/'Rafael557_reconstruction_v2_20261105/reconstruction.json'
STORED=A/'Rafael557_stored_native_v3_20261105/stored_native_verification.json'
CATALOGUE=A/'Rafael557_stored_catalogue_v2_20261105/all_stored_effective_body_bindings.json'
LOADERS=A/'Rafael557_loaders_v2_20261105/verification.json'
INPUT=A/'Rafael557_storage_inputs_v2_20261105'
BODY=A/'Rafael557_body_visual_review_v2_20261105/body_visual_review.json'
INITIAL=A/'Rafael557_company_punctuation_v1_20261105/direct_actual_visual_review_before_delta.json'
NAME_DOC=Path('translations/rafael_B141_B160_scoped_names_review_v1.json')
FINAL=Path('translations/rafael_B141_B160_final_review_v1.json')
FINAL_NAMES=Path('translations/rafael_B141_B160_scoped_names_final_v1.json')
PIXELS=[A/f'{r}/focused_actual_pixels.json' for r in ['Rafael557_tutorials_actual_pixels_v2_20261105','Rafael557_story_actual_pixels_v1_20261105','Rafael557_punctuation_actual_pixels_v1_20261105']]
MENUS=[A/f'Rafael557_{r}_menu_pixels_v1_20261105/menu_actual_pixels.json' for r in ['tutorial','story','punctuation']]
REPLAY_SHEETS=A/'Rafael557_punctuation_actual_sheets_v1_20261105/receipt.json'

def hashes(paths):return {str(p):sha(Path(p).read_bytes()) for p in paths}

def one(mapping,predicate):return next(x for x in mapping if predicate(x))

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,FINAL,FINAL_NAMES])
    rebuilt,stored,cat,loaders,body,initial,replay,names=map(load,[REBUILT,STORED,CATALOGUE,LOADERS,BODY,INITIAL,REPLAY_SHEETS,NAME_DOC])
    docpath,planpath,nativepath,menupath,stylespath=map(Path,[rebuilt['manuscript'],rebuilt['plan'],rebuilt['native'],rebuilt['menu'],rebuilt['styles']])
    doc,plan,native,menu,styles=map(load,[docpath,planpath,nativepath,menupath,stylespath])
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==sha(REBUILT.read_bytes())
    assert stored['native_sha256']==rebuilt['native_sha256']==sha(nativepath.read_bytes())
    assert plan['manuscript_sha256']==rebuilt['manuscript_sha256']==sha(docpath.read_bytes())
    assert native['plan_sha256']==rebuilt['plan_sha256']==sha(planpath.read_bytes()) and not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert body['all558_final_body_pages_directly_viewed'] and body['fresh_punctuation_pages_viewed']==2
    assert native['all558_complete_pages_directly_viewed'] and native['pages']==stored['complete_stored_pages']==558
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['total_relocated_native_relative_cases']==1190 and len(stored['relative_cases'])==238
    assert cat['stored_sha256']==sha(STORED.read_bytes()) and cat['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (cat['fresh_native_lookups'],cat['exact_previous_lookups_reused'])==(2,547)
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,2,684)
    assert len(doc['records'])==557 and len(native['records'])==len(stored['records'])==len(cat['records'])==549
    assert stored['typed_labels_checked']==8 and len(stored['typed_objects'])==4 and not stored['style_records'] and not styles['objects']
    assert menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus'])==4
    nameproof=INPUT/'qualified_public_names.json';np=load(nameproof)
    assert np['offline_visual_approved'] and len(np['planes'])==len(names['records'])==20
    assert np['runtime']==native['runtime']==stored['runtime']==cat['runtime']==menu['runtime']==styles['runtime']
    archive=Path(rebuilt['target_archive']).read_bytes();assert sha(archive)==rebuilt['target_archive_sha256']
    blocks=IlnkContainer.parse(archive).blocks;assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    bystored={r['id']:r for r in stored['records']};bycompiled={r['id']:r for r in native['records']}
    byl={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    byplan={r['id']:r for r in plan['records']};docrows={r['id']:r for r in doc['records']}
    groups={g['block']:g for g in rebuilt['groups']}
    for g in groups.values():assert sha(blocks[g['block']])==g['target_sha256']
    accepted={};actorids=set();live_menus=[];proof_files=[];frames=0
    for i,(pixelpath,menuproofpath) in enumerate(zip(PIXELS,MENUS,strict=True)):
        pixels,live=map(load,[pixelpath,menuproofpath]);fixturepath=Path(live['fixture']);terminalpath=Path(live['terminal'])
        fixture,terminal=map(load,[fixturepath,terminalpath]);proof_files.extend([fixturepath,terminalpath])
        assert live['fixture_sha256']==sha(fixturepath.read_bytes()) and live['terminal_sha256']==sha(terminalpath.read_bytes())
        assert terminal['terminal'] and terminal['frames']==pixels['frames']==fixture['frames']
        assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match'] and pixels['all_selected_pages_observed_in_exact_fixture_order']
        assert not any(pixels[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        for ref,digest in pixels['evidence'].items():assert sha(Path(ref).read_bytes())==digest
        frames+=fixture['frames'];copied={c['fixture_offset']:c for c in fixture['copied_commands']}
        holdframes=set()
        for item in fixture['selected_records']:
            if i==1 and item['block']==154:continue  # Superseded by the focused replay below.
            ident=item['id'];s=bystored[ident];n=bycompiled[ident];assert s['block']==item['block']
            assert (s['stored_hex'],s['expanded_hex'])==(item['stored_hex'],item['expected_expanded_body_hex'])
            c=one(groups[s['block']]['all_target_commands'],lambda c:c['offset']==s['new_offset']-5)
            assert copied[item['fixture_offset']]['whole_command_hex']==c['whole_command_hex']
            display=n['complete_native_English_display'];pages=[display] if item['selector']==254 else display['pages']
            for idx,p in enumerate(pages,1):
                samples=[r for r in pixels['body_pages'] if r['id']==ident and r['page']==idx]
                assert samples and (ident,idx) not in accepted
                for sample in samples:
                    assert sample['native_plane_sha256']==p['native_plane_sha256']
                    assert sample['text_hex']==bytes.fromhex(s['expanded_hex'])[p.get('start',0):].hex()
                    holdframes.add(sample['frame'])
                accepted[(ident,idx)]=dict(id=ident,page=idx,proof=str(pixelpath),capture=samples[0]['capture'],frame=samples[0]['frame'])
        actorids.update(h['actor_ID'] for h in pixels['headers'] if h['frame'] in holdframes)
        assert live['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert live['numeric_modal_return_register_original_story_branches_andcancellation_unvisited']
        controls=load(fixture['inputs']);assert sha(Path(fixture['inputs']).read_bytes())==fixture['inputs_sha256']
        for m in live['menus']:
            declared=one(fixture['menus'],lambda v:v['stored_command_offset']==m['source_command_offset'])
            if i==1 and declared['block']==154:continue
            final=one(stored['typed_objects'],lambda v:v['block']==declared['block'])
            assert declared['stored_command_offset']==final['offset'] and declared['command_hex']==final['object_hex']
            assert m['observed_selected_options']==[0] and m['count']==2
            sample=one(live['menu_samples'],lambda r:r['source_command_offset']==final['offset'] and r['visible_selected_option']==0)
            subsequent=one(fixture['selected_records'],lambda r:r['fixture_offset']>declared['fixture_offset'])
            follow=one(pixels['ordered_selected_source_calls'],lambda r:r['id']==subsequent['id'] and r['page']==1)
            assert any('A' in r['buttons'] and sample['frame']<=r['start']<=follow['frame'] for r in controls)
            live_menus.append(dict(block=final['block'],offset=final['offset'],labels=final['labels'],visible_cursor=0,
                menu_frame=sample['frame'],ordinary_A_following_fixture_speech=subsequent['id'],following_frame=follow['frame'],proof=str(menuproofpath)))
    ids={k[0] for k in accepted};allids=set(bystored)
    assert (len(ids),len(accepted),frames,len(live_menus))==(188,193,65763,4)
    assert {r['block'] for r in live_menus}=={143,146,148,154}
    assert {'DK4_MES_B143_R0067','DK4_MES_B146_R0006','DK4_MES_B148_R0121','DK4_MES_B154_R0084','DK4_MES_B154_R0114'}<=ids
    assert sum(docrows[i]['kind']=='system-FE' for i in ids)==6 and not any(b'Castor Co..' in bytes.fromhex(r['expanded_hex']) for r in bystored.values())
    assert replay['actual_dialogue_pages']==14 and replay['actual_pixel_proof_sha256']==sha(PIXELS[-1].read_bytes())
    sheets=initial['directly_opened_readable_sheets']+replay['bottom_screen_sheets']+replay['full_scene_sheets']+[load(MENUS[-1])['review_sheet']]
    assert len(sheets)==25 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    ROOT.mkdir(parents=True)
    evidence=hashes([REBUILT,STORED,CATALOGUE,LOADERS,BODY,INITIAL,REPLAY_SHEETS,NAME_DOC,nameproof,docpath,planpath,nativepath,menupath,stylespath,
        INPUT/'complete_offline_visual_andinventory_review.json',*PIXELS,*MENUS,*proof_files,Path(__file__)])
    visual=ROOT/'complete_visual_approval.json';actual=ROOT/'actual_review.json'
    save(visual,dict(all558_body_pages_8_captions_20_public_names_approved=True,all193_final_observed_pages_andfour_menus_directly_viewed=True,
        reviewed_sheets=sheets,retired_initial_B154_captures_preserved=True,all_other_pages_reused_only_after_exact_body_command_andplane_match=True,
        whole_exchange_retention_notes=initial['whole_exchange_retention_notes'],evidence=evidence,new_credit=0,guide_photos=False))
    save(actual,dict(total_frames=frames,initialized_fixture_runs=3,source_speech_variants_observed=len(ids),native_body_pages_observed=len(accepted),
        actual_choice_labels=8,offline_only_speech_variants=len(allids-ids),source_IDs_observed=sorted(ids),offline_only_source_IDs=sorted(allids-ids),
        exact_observed_pages=list(accepted.values()),observed_public_name_actor_IDs=sorted(actorids),menus=live_menus,
        all_four_menus_default_cursor_andfollowing_fixture_speech_observed=True,other_cursor_states_VM_returns_branches_andcancellation_offline_only=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        updated_B154_replay_replaces_same_source_IDs_without_double_credit=True,evidence=evidence,new_credit=0,guide_photos=False))
    for r in names['records']:
        assert r['kind']=='progressive-nameplate' and not r['review']['formatting']
        r['review']['formatting']=True;r['actual_header_observed_in_disclosed_fixture']=r['actor_ID'] in actorids
    names.update(all_name_formatting_gates_pending=False,all20_individual_five_gates_pass_for_public_nameplanes=True,
        actor_IDs_unvisited_in_current_fixtures=sorted({r['actor_ID'] for r in names['records']}-actorids),actual_review=str(actual),actual_review_sha256=sha(actual.read_bytes()))
    validate_natural_dialogue_batch(names);save(FINAL_NAMES,names)
    waivers=[]
    for r in doc['records']:
        ident=r['id'];b=r['block'];assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if ident in bystored:
            s=bystored[ident];at=s['new_offset'];raw=bytes.fromhex(s['stored_hex']);assert blocks[b][at-5:at+1].hex()==r['source_complete_preamble_hex']
            ref=dict(offset=at,header_offset=at-5,record_index=s['new_record_index']);r['planned_English_markup']=byplan[ident]['formatted_markup']
            r['actual_utterance_observed_in_disclosed_fixture']=ident in ids
            for issue in byplan[ident]['base_QA']['issues']:
                if 'reviewed_retention_reason' in issue:
                    assert issue['code']=='weak-line-ending';r.setdefault('qa_waivers',[]).append(issue['code'])
                    r['qa_waiver_reason']=issue['reviewed_retention_reason'];waivers.append(ident)
        else:
            obj,s=byl[ident];at=s['offset'];raw=bytes.fromhex(s['stored_hex']);assert raw.decode('ascii')==r['english'] and obj['block']==b
            ref=dict(offset=at,command_offset=obj['offset'],source_index=s['source_index'],record_index=s['record_index'])
            r.update(actual_caption_default_cursor_state_observed=True,other_cursor_andreturn_cases_verified_offline=True)
        assert blocks[b][at:at+len(raw)+1]==raw+b'\0'
        r['planned_integrated_reference']=dict(**ref,file_path=r['file_path'],block=b,exact_stored_hex=raw.hex(),target_archive_sha256=sha(archive))
        for key in ['fresh_formatting_binding_pending','all_five_review_gates_pending','source_context_localization_formatting_gates_pending',
            'complete_native_menu_binding_andformatting_pending','approved_names_terms_titles_andruntime_substitutions_pending',
            'current_English_comparison_pending','source_preamble_andname_consumer_approval_not_inferred']:
            if key in r:r[key]=False
        r['review']['formatting']=True;r['registered_release_andcompletion_credit_pending']=True
    assert set(waivers)=={'DK4_MES_B142_R0005','DK4_MES_B143_R0372'}
    assert Counter(r['decision'] for r in doc['records'])=={'revision':235,'retention':322}
    doc.update(all_fifth_formatting_gates_pending=False,all_individual_five_gates_pass=True,all557_individual_five_gates_pass=True,
        fresh_formatting_stored_andfocused_checks_pending_for_two_changed_rows=False,current_FU_native_display_still_pending=False,
        current_FU_expansion_parity_width_anddisplay_proof_pending=False,native_macro_tokens_still_require_formatter_marking=False,
        no_new_formatting_rendering_gameplay_orregistered_integration_claim=False,only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=558,actual_source_speech_variants=188,actual_body_pages=193,offline_only_source_speech_variants=361,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=sha(FINAL_NAMES.read_bytes()),
        parent_manuscript=str(docpath),parent_manuscript_sha256=sha(docpath.read_bytes()),registered_release_andcompletion_credit_pending=True,
        formatting_evidence=dict(native=str(nativepath),stored=str(STORED),catalogue=str(CATALOGUE),loaders=str(LOADERS),visual=str(visual),actual=str(actual)))
    validate_natural_dialogue_batch(doc);save(FINAL,doc)
    plan.update(manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),exact_all_prose_andcompiled_bytes_unchanged=True)
    final_plan=ROOT/'release_plans.json';save(final_plan,plan)
    save(ROOT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),plan=str(final_plan),plan_sha256=sha(final_plan.read_bytes()),
        all_individual_five_gates_pass=True,records=557,revisions=235,retentions=322,body_pages=558,typed_labels=8,scoped_public_names=20,
        actual_source_variants=188,actual_pages=193,offline_only_source_variants=361,actual_public_names=len(actorids),
        two_full_catalogue_particle_fixes_pending=True,registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**hashes([FINAL,FINAL_NAMES,final_plan,visual,actual])}))
    print(dict(five_gate_records=557,observed_variants=188,observed_pages=193,public_names_observed=len(actorids),offline_only_speeches=361,registered_integration_pending=True))
