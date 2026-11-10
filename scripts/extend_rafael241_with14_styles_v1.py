"""Add fourteen individually reviewed source style variants without repeating241 completed reviews."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

OLD=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v4.json')
OBJECTS=Path('work/analysis/Rafael14_style_current678_20261105/current_objects.json')
ROLES=OBJECTS.with_name('roles0_1.json')
IDENTITY=Path('work/analysis/Rafael241_names_terms_20261105/names_terms_roles_andconsumer_dependency_qualification_v1.json')
OUT=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v5.json')
QUAL=Path('work/analysis/Rafael255_extended_identity_20261105.json')
REVISE={
 'SC0_B113_STYLE_10_126':'Replace portentous behold with a natural deferential request to look; preserve the admiral address andthe object reference without inventing ceremonial importance.',
 'SC0_B119_STYLE_16_0':'Make the polite report a complete conversational statement. The clipped dead end alert is too abrupt for this source variant.',
 'SC0_B119_STYLE_16_70':'Preserve the conversational dead-end report as a natural sentence; do not manufacture a gendered English address.'
}
RETAIN={
 'SC0_B113_STYLE_10_0':'The polite look request is natural; the nearby temple object supplies the source deictic referent. Preserve the shared0/1 alias.',
 'SC0_B113_STYLE_10_28':'The direct attention call naturally fits the casual source; retain its shared2/3 alias without an invented relationship.',
 'SC0_B113_STYLE_10_48':'The energetic Admiral,look atthis already suits the informal request; no new slang isneeded.',
 'SC0_B113_STYLE_10_74':'Look here is a natural rough attention call inthe object-discovery exchange. It doesnot establish kinship orbiography.',
 'SC0_B113_STYLE_10_100':'The two short exclamations preserve the youthful calling tone in readable American English without an artificial stretched Admiral spelling.',
 'SC0_B119_STYLE_16_24':'The restrained elliptical observation is natural inthis brief dead-end report; preserve the admiral address.',
 'SC0_B119_STYLE_16_46':'The puzzled Huh andnoun-phrase realization naturally express the casual surprise; there isno admiral address toadd.',
 'SC0_B119_STYLE_16_92':'The clipped Oops/Dead end reaction is natural for the rough informal voice andpreserves its lack ofadmiral address.',
 'SC0_B119_STYLE_16_116':'The concise observation suits the measured older register without imposing an English old-man caricature ornew family label.',
 'SC0_B119_STYLE_16_142':'The youthful two-part alert already sounds natural andkeeps the energetic admiral call.',
 'SC0_B119_STYLE_16_170':'Oh my conveys the mild source surprise,andthe concise dead-end observation suits the measured register.'
}

if __name__=='__main__':
    assert not OUT.exists() and not QUAL.exists()
    old,objects,roles,identity=map(load,[OLD,OBJECTS,ROLES,IDENTITY])
    assert objects['runtime']==roles['runtime']==identity['runtime']
    assert len(objects['style_records'])==14 and len(objects['style_objects'])==2 and objects['native_style_getter_cases']==16
    assert {r['source_selector'] for r in objects['style_records']}=={208}
    assert len(roles['source_records'])==26 and {r['source_selector'] for r in roles['native_roles']['rows']}=={207,208}
    selected=next(r for r in roles['native_roles']['rows'] if r['source_selector']==208)
    assert (selected['role_index'],selected['strict_assignment'],selected['resolved_actor_ID'],selected['source_voice_class'])==(1,208,151,4)
    doc=deepcopy(old);added=[]
    for original in objects['style_records']:
        row=deepcopy(original);key=row['id'];prior=row['current_comparison_paragraph'];retained=key in RETAIN
        assert retained != (key in REVISE)
        reason=RETAIN[key] if retained else REVISE[key]
        english=prior if retained else row['independent_English_draft']
        row.update(kind='progressive',native_object_kind='4100-style-alternative',english=english,
            decision='retention' if retained else 'revision',finding=reason,localization_note=reason,retention_reason=reason if retained else None,
            speaker='Runtime role1 companion; Sailor fallback inverified own context; identity not fixed bytranslation',
            current_English=row['current_effective_text'],current_normalized_logical_English=prior,
            prior_macro_normalized_comparison=prior,source_record_index=row['source_reference']['physical_record_index'],
            source_native_extent=row['source_native_extent'],planned_English_markup='{SPEAKER:D0}'+english,
            virtual_formatter_prefix_is_not_part_of_stored_alternative_text=True,
            native_role_voice_alias_controls_andformatting_pending=False,source_dynamic_speaker_binding_pending=False,
            native_dynamic_identity_proof=str(ROLES),native_dynamic_identity_proof_sha256=sha(ROLES.read_bytes()),
            no_fixed_identity_inferred_for_dynamic_selector=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            source_name_term_control_binding_pending=False,fresh_formatting_binding_pending=True,
            all_fresh_display_andregistered_integration_pending=True,new_credit=0)
        assert english.isascii() and not any(c in english for c in '\r\n\t')
        added.append(row)
    assert (sum(r['decision']=='revision' for r in added),sum(r['decision']=='retention' for r in added))==(3,11)
    doc['records']+=added
    doc.update(physical_speech_objects=243,ordinary_speech_objects=229,style_physical_speech_objects=14,style_command_objects=2,
        source_speeches=243,source_choice_labels=12,contextual_comparisons=255,proposed_revisions=135,justified_retentions=120,
        four_gate_passes=255,all255_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        all_previous241_records_exact_unchanged=True,new14_style_comparisons=14,new14_style_revisions=3,new14_style_retentions=11,
        style_current_objects=str(OBJECTS),style_current_objects_sha256=sha(OBJECTS.read_bytes()),
        scoped_identity_proof=str(QUAL),source_style_intake_earlier_command_hex_exposure_disclosed=True,
        ordinary_speeches_andmenus_had_previously_received_current_English_review=True,
        all_style_drafts_preceded_current_style_English_decoding_not_blanket_prior_exposure_claim=True)
    updated=deepcopy(identity)
    updated.update(dynamic_selectors=[207,208],dynamic_binding=str(ROLES),dynamic_binding_sha256=sha(ROLES.read_bytes()),
        dynamic_roles=roles['native_roles'],source_style_objects=str(OBJECTS),source_style_objects_sha256=sha(OBJECTS.read_bytes()),
        original18_names_andmacro_dependencies_exact_unchanged=True,source_4100_alias_bindings_complete=True,
        prior_ordinary_identity=str(IDENTITY),prior_ordinary_identity_sha256=sha(IDENTITY.read_bytes()),new_credit=0)
    save(QUAL,updated);doc['scoped_identity_proof_sha256']=sha(QUAL.read_bytes())
    assert doc['records'][:241]==old['records']
    assert len({r['id'] for r in doc['records']})==255 and all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    save(OUT,doc);print('255 four-gate comparisons:135 revisions/120 retentions;14 new style variants,241 exact reviewed records retained. No completion credit.')
