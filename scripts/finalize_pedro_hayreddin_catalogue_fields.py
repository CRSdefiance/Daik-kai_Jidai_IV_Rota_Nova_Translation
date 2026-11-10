"""Review the two complete source names and qualify exact reuse on the verified successor."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Pedro_Hayreddin_catalogue_fields_checked_20261104')
FINAL=Path('translations/pedro_hayreddin_catalogue_fields_final_v1.json')
PROPOSAL=Path('work/analysis/Rafael_B36_B41_name_field_proposals_20261104/owned_fields_proposal.json')
NATIVE=Path('work/analysis/Rafael_B36_B41_name_fields_native_20261104/native_name_fields_verification.json')
VISUAL=Path('work/analysis/Rafael_B36_B41_formatting_20261104/speech_display_approved_v3/catalogue_name_proposal_visual_approval.json')
SOURCE=Path('work/analysis/Rafael_B36_B41_new_name_bindings_20261104/names.json')
RELEASE=Path('work/analysis/Rafael_B36_B41_release_verified_20261104/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0);proposal,native,visual,source=map(load,[PROPOSAL,NATIVE,VISUAL,SOURCE])
    assert proposal['runtime']['ARM9_sha256']==sha(ctx.arm) and proposal['runtime']['COMMON_sha256']==sha(ctx.common)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm,proof=plan_arm9_name_fields(ctx.arm,proposal,clean)
    assert proof==native['name_data_plan'] and arm==Path(native['proposed_ARM9']).read_bytes()
    assert native['proposal_sha256']==sha(PROPOSAL.read_bytes()) and visual['native_sha256']==sha(NATIVE.read_bytes())
    assert visual['all12_current_andproposed_name_planes_directly_viewed'] and len(native['negative_cases_rejected'])==8
    assert native['original_progressive_andfull_name_getters_pass'] and not native['actual_gameplay']
    versions={v['version']:{(r['actor_ID'],r['consumer']):r for r in v['names']['rows']} for v in native['versions']}
    clean_full={r['actor_ID']:r for r in source['clean_names']['rows'] if r['consumer']=='full-catalogue'}
    reasons={31:'Render the clean Spanish name particle デ as lowercase de in the complete Pedro de Valdes name. Retain Pedro andValdes andthe unchanged Pedro Valdes progressive form. This corrects the embedded Japanese component without adding a rank,relationship orbiography.',
        34:'Normalize the unintended full-width Latin F in the existing Fazul component to ordinary ASCII F. Retain the complete source identity Barbarossa Fazul Hayreddin andits unchanged Barbarossa Hayreddin progressive form;no new title or historical detail is introduced.'}
    records=[]
    for field in proposal['fields']:
        actor=field['actor'];current=versions['current'][actor,'full-catalogue'];target=versions['proposed'][actor,'full-catalogue']
        assert versions['current'][actor,'progressive-nameplate']['text']==versions['proposed'][actor,'progressive-nameplate']['text']
        assert target['text'] in ['Pedro de Valdes','Barbarossa Fazul Hayreddin'] and field['column']==8
        records.append(dict(id=f'ACTOR{actor}_FULL_CATALOGUE_MIDDLE_FIELD',actor_ID=actor,english=target['text'],speaker=target['text'],
            source_meaning=clean_full[actor]['text'],context='Complete proper name in the full-name catalogue,read with the established progressive identity andthe complete Rafael pirate/Spanish exchanges. The field isnot an independent title orrole.',
            localization_note=reasons[actor],decision='revision',finding='Japanese particle left in Latin name.' if actor==31 else 'Full-width Latin letter in otherwise ASCII full-name component.',
            retained_elements_reason='Keep the established given/epithet andsurname components andthe progressive nameplate exactly.',
            source_reference=dict(native_binding=str(SOURCE),native_binding_sha256=sha(SOURCE.read_bytes()),actor_ID=actor,consumer='full-catalogue',text_hex=clean_full[actor]['text_hex'],middle_component=field['source_clean_component']),
            current_reference=dict(native_binding=str(NATIVE),native_binding_sha256=sha(NATIVE.read_bytes()),actor_ID=actor,consumer='full-catalogue',text=current['text'],field_offset=field['table_field_offset'],physical_offset=field['physical_offset'],component_hex=field['source_hex']),
            reviewed_owned_field=field,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
            progressive_nameplate_unchanged=True,full_catalogue_UI_unvisited=True,formatting_scope='Complete original getters andtwelve native planes/styles1/11 withindependent glyph/bounds proofs. Exact current dependencies permit reuse;no catalogue UI activation claimed.'))
    final=dict(format='dk4-scoped-owned-name-field-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=records,proposed_revisions=2,new_dialogue_completion_credit=0,
        all_five_individual_review_gates_pass_in_scoped_context=True,all_other205_actors_andall_progressive_names_unchanged=True,
        full_catalogue_UI_unvisited=True,global207_name_review_still_open=True,registered_deployment_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PROPOSAL,NATIVE,VISUAL,SOURCE,RELEASE,STARTUP,Path(__file__)]})
    validate_natural_dialogue_batch(final);ROOT.mkdir();save(FINAL,final)
    save(ROOT/'reuse_andeditorial_approval.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),runtime=ctx.receipt(),
        exact_same_current_ARM9_COMMON_andtested_field_plan=True,complete_native_name_data_plan=proof,all12_prior_native_planes_direct_view_reused=True,
        eight_negative_cases_reused=True,no_new_native_calls_claimed=True,no_new_gameplay_orcatalogue_UI_claim=True,
        two_individual_full_name_editorial_reviews_complete=True,registered_deployment_pending=True,new_credit=0,guide_photos=False))
    print('Two full-name field reviews sealed;exact tested ARM9/native plan and12 viewed planes reused;catalogue UI unvisited,zero dialogue credit.')
