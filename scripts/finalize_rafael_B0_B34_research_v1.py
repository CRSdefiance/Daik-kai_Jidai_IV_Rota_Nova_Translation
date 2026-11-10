"""Seal the complete speech-only batch and its distinct owned-name evidence."""
from collections import Counter
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import FORMATTING as MANUSCRIPT,ROOT
from scripts.qualify_rafael_B0_B34_names_v1 import LABELS,OUT as OWNED
from scripts.verify_rafael_B0_B34_visual_v1 import APPROVAL as VISUAL,FINAL as NATIVE,PLAN

REBUILT=ROOT/'rebuilt_v1/reconstruction.json'
COMBINED=ROOT/'rebuilt_with_names_v1/research_reference.json'
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all283_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
FIXTURE=ROOT/'fixtures_v1/rafael_residual_battles_and_recruitment_fixture.json'
TERMINAL=ROOT/'actual_run_v1/terminal.json'
LIVE=ROOT/'actual_body_v1/focused_actual_pixels.json'
NAMES=ROOT/'retained_name_planes_v2/native_name_planes.json'
MIDDLE=ROOT/'owned_middle_fields_visual_v1.json'
PROPOSAL=OWNED/'proposal.json'
RESEARCH=ROOT/'research_final_v1'
READY=RESEARCH/'research_completion.json'
FINAL=Path('translations/rafael_B0_B34_final_review_v1.json')
FINAL_NAMES=Path('translations/rafael_B0_B34_scoped_names_final_v1.json')
FINAL_FIELDS=Path('translations/rafael_B0_B34_owned_middle_fields_final_v1.json')
GATES=['source','context','localization','naturalness','formatting']


def main():
    assert not any(p.exists() for p in (RESEARCH,FINAL,FINAL_NAMES,FINAL_FIELDS))
    paths=(REBUILT,COMBINED,STORED,LOOKUP,LOADERS,FIXTURE,TERMINAL,LIVE,MANUSCRIPT,PLAN,NATIVE,VISUAL,LABELS,NAMES,MIDDLE,PROPOSAL)
    rebuilt,combined,stored,lookup,loaders,fixture,terminal,live,doc,plan,native,visual,labels,names,middle,proposal=map(load,paths)
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(REBUILT)
    assert rebuilt['native_sha256']==stored['native_sha256']==digest(NATIVE)
    assert native['plan_sha256']==digest(PLAN) and native['manuscript_sha256']==digest(MANUSCRIPT)
    assert lookup['stored_sha256']==digest(STORED)
    assert lookup['all283_ordinary_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert stored['runtime']==lookup['runtime']==native['runtime']==names['runtime']==labels['runtime']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],
        stored['fresh_relocated_native_relative_cases'])==(284,137,147,675)
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,70,616)
    assert rebuilt['changed_blocks']==list(range(35)) and rebuilt['relative_sites']==135 and rebuilt['command_count']==634
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    assert digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    assert digest(combined['research_ROM'])==combined['research_ROM_sha256']
    assert combined['story_reconstruction_sha256']==digest(REBUILT) and combined['name_native_proof_sha256']==digest(MIDDLE)
    assert combined['whole_story_only_parent_inverse_exact']
    assert middle['offline_visual_approved'] and not middle['direct_view_pending']
    assert middle['proposal_sha256']==digest(PROPOSAL) and middle['name_data_plan']==combined['owned_name_metadata_plan']
    assert middle['name_data_plan']['changed_bytes']==9 and middle['name_data_plan']['complete_parent_inverse_exact']
    assert len(proposal['fields'])==3 and {r['actor'] for r in proposal['fields']}=={30,40,59}
    assert visual['all_final_body_caption_and_name_sheets_directly_viewed'] and visual['native_sha256']==digest(NATIVE)
    assert names['scoped_actors']==len(labels['records'])==39 and names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert live['evidence'][str(FIXTURE)]==digest(FIXTURE) and live['evidence'][str(TERMINAL)]==digest(TERMINAL)
    assert live['all_selected_pages_observed_in_exact_fixture_order'] and live['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert not live['complete_scene_commands_retained'] and not live['natural_activation']
    assert (live['frames'],live['selected_utterances'],live['selected_pages'])==(28001,95,96)
    assert live['complete_body_planes']==live['complete_header_planes']==196
    assert set(live['observed_actor_IDs'])=={r['actor_ID'] for r in labels['records']}
    assert fixture['source_personality_tables_copied_complete']==0 and not fixture['menus']
    assert fixture['all_unowned_files_components_andserialized_parent_inverse_exact']
    seen={r['id'] for r in live['body_pages']}
    assert len(seen)==95 and seen=={r['id'] for r in fixture['selected_records']}
    assert {'DK4_MES_B5_R0052','DK4_MES_B26_R0033','DK4_MES_B26_R0124','DK4_MES_B20_R0078'}<=seen
    assert {r['page'] for r in live['body_pages'] if r['id']=='DK4_MES_B25_R0033'}=={1,2}
    sheets=visual['sheets']+live['review_sheets']
    assert len(live['review_sheets'])==16 and all(digest(r['path'])==r['sha256'] for r in sheets)
    capture=Path(terminal['report']); assert digest(capture)==terminal['report_sha256']
    report=load(capture); snapshot=report['read_only_RAM_snapshot']; ram=Path(snapshot['path']).read_bytes()
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert snapshot['read_only_export'] and digest(snapshot['path'])==snapshot['sha256']
    arm=NdsImage.open(fixture['research_ROM']).read_file('/__arm9__.bin')
    payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48])
    assert len(payload)==123264 and ram[POOL-BASE:POOL-BASE+len(payload)]==payload
    blocks=IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    speeches={r['id']:r for r in stored['records']}; layouts={r['id']:r for r in plan['records']}
    assert len(speeches)==len(layouts)==283 and speeches.keys()==layouts.keys()=={r['id'] for r in lookup['records']}
    for row in doc['records']:
        saved=speeches[row['id']]; at=saved['new_offset']; raw=bytes.fromhex(saved['stored_hex'])
        assert blocks[row['block']][at:at+len(raw)+1]==raw+b'\0'
        assert blocks[row['block']][at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert not row['review']['formatting']; row['review']['formatting']=True
        row.update(planned_integrated_reference=dict(offset=at,record_index=saved['new_record_index'],header_offset=at-5,
            file_path=row['file_path'],block=row['block'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256']),
            actual_utterance_observed_in_disclosed_fixture=row['id'] in seen,
            planned_English_markup=layouts[row['id']]['formatted_markup'],fresh_formatting_binding_pending=False,
            source_context_localization_formatting_gates_pending=False,speaker_nameplate_approval_pending=False,
            registered_release_and_completion_credit_pending=True)
    assert Counter(r['decision'] for r in doc['records'])=={'revision':162,'retention':121}
    RESEARCH.mkdir()
    actual_path=RESEARCH/'actual_review.json'; visual_path=RESEARCH/'complete_visual_approval.json'; release_plan=RESEARCH/'release_plans.json'
    evidence={str(p):digest(p) for p in (*paths,capture,Path(__file__))}
    save(actual_path,dict(total_frames=28001,initialized_fixture_runs=1,source_speech_variants_observed=95,
        native_body_pages_observed=96,actual_choice_labels=0,offline_only_speech_variants=188,
        source_IDs_observed=sorted(seen),offline_only_source_IDs=sorted(speeches.keys()-seen),
        observed_public_name_actor_IDs=live['observed_actor_IDs'],all39_progressive_name_headers_observed=True,
        unchanged_ARM9_exact_to_registered_parent=True,owned_middle_field_repairs_have_separate_native_proofs=True,
        all_changed_full_catalogue_UIs_unvisited=True,menus=[],
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    save(visual_path,dict(all_body_caption_andname_planes_approved=True,all_actual_pages_and_menus_directly_viewed=True,
        body_pages=284,observed_pages=96,scoped_public_names=39,typed_labels=0,reviewed_sheets=sheets,
        full_catalogue_UI_unvisited=True,intentional_ellipsis_uses_previously_validated_tiny_native_periods=True,
        evidence=evidence,new_credit=0,guide_photos=False))
    for row in labels['records']:
        row.update(id=f'ACTOR_NAME_{row["actor_ID"]:03d}',english=row['approved_forms']['progressive-nameplate'],
            speaker='Speaker name or role',context='Source-qualified speaker in the complete Rafael residual exchanges.',
            source_meaning=' '.join(next(f['source']['text'] for f in row['source_andcurrent_fields'] if f['column']==c)
                for c in (0,8,4)).strip(),localization_note=row['finding'],
            actual_header_observed_in_disclosed_fixture=True,full_catalogue_UI_unvisited=True)
        row['review']['formatting']=True
    labels.update(encoder='dialogue-relocatable-v1',review_gates=GATES,
        all_individual_five_gates_pass_for_public_nameplanes=True,all_name_formatting_gates_pending=False,
        actual_review=str(actual_path),actual_review_sha256=digest(actual_path),name_changes_registered_integration_pending=True)
    validate_natural_dialogue_batch(labels); save(FINAL_NAMES,labels)
    fields=[]
    for field in proposal['fields']:
        label=next(r for r in labels['records'] if r['actor_ID']==field['actor'])
        fields.append(dict(id=f'ACTOR{field["actor"]}_NAME_COLUMN8_LOCALIZED',english=label['approved_forms']['full-catalogue'],
            speaker='Full-name catalogue',context=label['context'],source_meaning=label['source_meaning'],
            localization_note=label['finding'],review=dict.fromkeys(GATES,True),owned_field=field,
            full_catalogue_UI_unvisited=True,source_reference=label['source_andcurrent_fields'],new_credit=0))
    fields_doc=dict(format='dk4-scoped-owned-name-fields-review-v2',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=GATES,records=fields,new_credit=0)
    validate_natural_dialogue_batch(fields_doc); save(FINAL_FIELDS,fields_doc)
    doc.update(encoder='dialogue-relocatable-v1',review_gates=GATES,all_individual_five_gates_pass=True,
        all_final_display_andname_gates_pending=False,all_fifth_formatting_gates_pending=False,
        native_macro_tokens_still_require_formatter_marking=False,only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=284,actual_source_speech_variants=95,actual_body_pages=96,offline_only_source_speech_variants=188,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=digest(FINAL_NAMES),
        parent_manuscript=str(MANUSCRIPT),parent_manuscript_sha256=digest(MANUSCRIPT),
        registered_release_and_completion_credit_pending=True,formatting_evidence=dict(native=str(NATIVE),stored=str(STORED),
            catalogue=str(LOOKUP),loaders=str(LOADERS),visual=str(visual_path),actual=str(actual_path)))
    validate_natural_dialogue_batch(doc); save(FINAL,doc)
    save(release_plan,{**plan,'manuscript':str(FINAL),'manuscript_sha256':digest(FINAL),'exact_all_prose_and_compiled_bytes_unchanged':True})
    save(READY,dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),plan=str(release_plan),plan_sha256=digest(release_plan),
        all_individual_five_gates_pass=True,records=283,revisions=162,retentions=121,body_pages=284,typed_labels=0,
        scoped_public_names=39,actual_source_variants=95,actual_pages=96,actual_choice_labels=0,actual_menus=0,
        actual_name_headers=39,offline_only_source_variants=188,registered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in (FINAL,FINAL_NAMES,FINAL_FIELDS,release_plan,visual_path,actual_path)}}))
    print('Sealed all 283 five-gate reviews, 284 stored pages and 96 observed emulator pages. Registration pending.')


if __name__=='__main__':main()
