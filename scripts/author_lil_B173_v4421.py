"""Record11 complete-exchange decisions;formatting/native/release gates remain open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B173_prose_v4420 as prose
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B173_author_v4421')
COMPARISON = Path('work/analysis/lil_B173_comparison_v4419/all11_current_effective_comparison_packet.json')
GLOSS = Path('work/analysis/lil_B173_clean_context_v4410/all11_complete_B173_exchange_and_fresh_glosses.json')
OUTPUT = Path('translations/lil_B173_editorial_manuscript_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison, gloss = map(read, [COMPARISON, GLOSS])
    source = read(comparison['source_context'])
    assert gloss['all11_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert len(prose.REVISIONS) == 8 and len(prose.RETAIN_NOTES) == 3 and not set(prose.REVISIONS) & set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS) | set(prose.RETAIN_NOTES) == {row['source_record_index'] for row in source['records']}
    doc = dict(format='dk4-editorial-source-prose-draft-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC2.DK4', current_ROM=source['current_ROM'], current_ROM_sha256=source['current_ROM_sha256'],
        source_ROM_sha256=source['source_ROM_sha256'], required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0, formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending',
        whole_exchange_context=gloss['whole_exchange_context'], clean_first_notes_are_historical_and_precede_current_native_bindings=True)
    dependencies = {
        'source_context': comparison['source_context'], 'control_contract': comparison['control_proof'], 'whole_exchange_context_notes': str(GLOSS),
        'actor_voice_contract': 'work/analysis/lil_B173_voices_v4412/current2_static_names_voices_and207_catalog_rebind.json',
        'branch_proof': 'work/analysis/lil_B173_branches_v4414/original_relative_skip_operand_proof.json',
        'source_entry_proof': 'work/analysis/lil_B173_entry_v4415/source_EV2_B173_action_dependency_and_native_getter_binding.json',
        'source_effect_and_predicate_contract': 'work/analysis/lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end.json',
        'actor_terminology_reconciliation': comparison['terms_binding'],
        'source_nameplate_consumer_proof': 'work/analysis/lil_B173_names_v4416/four_original_name_consumers_and_owned_scratch_paths.json',
        'effective_current_comparison': str(COMPARISON),
    }
    for key, path in dependencies.items():
        doc[key], doc[key + '_sha256'] = path, sha(Path(path).read_bytes())
    speakers = {2:'Lil',202:'Reika'}
    rows = []
    for original in comparison['records']:
        row = deepcopy(original)
        old = row['current_effective_paragraph']
        for macro in ['FI','FA','FO']:
            old = old.replace(macro, '{MACRO:' + macro + '}')
        index = row['source_record_index']
        body, note = prose.REVISIONS[index] if index in prose.REVISIONS else (old, prose.RETAIN_NOTES[index])
        assert body == body.strip() and '\n' not in body and '  ' not in body and all(ord(char) < 128 for char in body)
        assert '%' not in body and not any(tag in body for tag in ['{LB','{PAD','{SPEAKER:'])
        for macro in ['FI','FA','FO']:
            assert bytes.fromhex(row['source_hex']).count(macro.encode()) == body.count('{MACRO:' + macro + '}')
        decision = 'retain-wording' if body == old else 'revise'
        row.update(source_meaning=row['fresh_source_gloss'], english='{SPEAKER:' + format(row['source_selector'], '02X') + '}' + body,
            localization_note=note, editorial_decision=decision, current_stored_English=row['current_raw_storage_English'],
            effective_predecessor_paragraph=old, comparison_basis='Original runtime macro template;NFKC presentation forms and collapsed legacy whitespace;raw/effective replacement provenance remains distinct.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False), context=gloss['whole_exchange_context'],
            speaker=speakers[row['source_selector']], prose_author_module=str(Path(prose.__file__)), status=doc['status'],
            editorial_predecessor_English_comparison_pending=False, full_clean_context_precedes_comparison=True,
            current_macro_dispatch_bound=True, current_complete_native_display_pending=True, current_native_UI_body_explicit_unexecuted_boundary=True,
            current_effective_native_dispatch_proof=comparison['control_proof'], original_native_display_consumer='original_progressive_54020')
        if decision == 'retain-wording':
            row['fresh_retained_wording_justification'] = note
        rows.append(row)
    counts = Counter(row['editorial_decision'] for row in rows)
    assert counts == {'revise':8,'retain-wording':3}
    doc.update(manuscript_kind='speech', prose_companions=[], records=rows, revised=8, retained=3)
    ROOT.mkdir(parents=True)
    save(OUTPUT, doc)
    save(ROOT / 'all11_clean_first_contextual_decisions.json', dict(manuscript=str(OUTPUT), manuscript_sha256=sha(OUTPUT.read_bytes()),
        decision_counts=dict(counts), source_context=comparison['source_context'], source_context_sha256=comparison['source_context_sha256'],
        all11_clean_then_current_whole_exchange_read=True, source_context_localization_naturalness_gates_true_formatting_false=True,
        source_no_FI_FA_FO_macros_preserved=True, all3_retentions_individually_justified=True,
        no_registered_current_replacements_in_this_source_exchange=True,
        native_Lil_Reika_spoken_Julian_current_crown_and_tomb_title_bindings_used=True,
        guarded_recognition_reported_beauty_and_recent_other_question_preserved=True,
        uncertain_name_recollection_smooth_talker_and_apparent_tomb_departure_preserved=True,
        Lil_tentative_inquiry_surprise_named_echo_and_competitive_inference_preserved=True,
        no_established_romance_kinship_rank_precise_location_item_power_or_earned_state_invented=True,
        evidence={str(path): sha(path.read_bytes()) for path in [COMPARISON,GLOSS,Path(prose.__file__),Path(__file__)]},
        new_emulator_runs=0, source_prose_or_completion_credit_added=0, no_ROM_registry_ledger_change=True, full_goal_complete=False))
    print(dict(objects=11, progressive=11, decisions=dict(counts), FI=0, FA=0, FO=0, formatting_pending=True, credit=0))
