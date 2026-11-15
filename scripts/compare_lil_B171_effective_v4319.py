"""Expose all37 current paragraphs after clean glosses and current source/name/term binding."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_comparison_v4319')
SOURCE = Path('work/analysis/lil_B171_source_v4311/all37_clean_current_complete_context.json')
GLOSS = Path('work/analysis/lil_B171_clean_context_v4309/all37_complete_B171_exchange_and_fresh_glosses.json')
CONTROL = Path('work/analysis/lil_B171_dispatches_v4313/all37_source_current_dispatches_FI1_FO0_and8_control_leaves.json')
VOICE = Path('work/analysis/lil_B171_voices_v4312/current3_static_names_voices_and207_catalog_rebind.json')
NAMES = Path('work/analysis/lil_B171_names_v4316/six_original_name_consumers_and_owned_scratch_paths.json')
ENTRY = Path('work/analysis/lil_B171_entry_v4315/source_EV2_B171_action_dependency_and_native_getter_binding.json')
EFFECT = Path('work/analysis/lil_B171_controls_v4317/one_resource_C200_four_presentations_two_ends_and8_source_leaves.json')
BRANCH = Path('work/analysis/lil_B171_branches_v4314/original_relative_skip_operand_proof.json')
TERMS = Path('work/analysis/lil_B171_terms_v4318b/current_Taoist_arts_Sanghyeon_training_bond_and_new_facts_reconciliation.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source, gloss, control, voice, names, entry, effect, branch, terms = map(read,[SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS])
    assert gloss['all37_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert source['whole_exchange_context_notes_sha256'] == sha(GLOSS.read_bytes())
    assert all(proof['source_context_sha256'] == sha(SOURCE.read_bytes()) for proof in [control,voice,names,entry,effect,branch,terms])
    assert len(control['speech_dispatch_cases']) == 74 and len(voice['fresh3_actor_names']['rows']) == 3
    assert len(names['native_six_consumer_cases']['rows']) == 6
    assert [(row['event_ID'],row['script_block'],row['action_index']) for row in entry['selected_B171_source_events']] == [(171,171,172)]
    assert effect['source_declared_end_offsets'] == [2112,2116] and len(effect['source_predicate_cases']) == 0 and len(branch['cases']) == 0
    binding = read(control['registered_catalog_binding'])
    catalog = {bytes.fromhex(row['key_hex']):row for row in binding['records'] if row['route_mask'] & 4}
    cases = {(row['id'],row['version']):row for row in control['speech_dispatch_cases']}
    rows = []
    for row in source['records']:
        stored = bytes.fromhex(row['current_hex'])
        body = stored[1:]
        registered = catalog.get(body)
        template = bytes.fromhex(registered['target_hex']) if registered else body
        effective = template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert cases[row['id'],'current-English']['boundaries'][1]['text_hex'] == effective.hex()
        rows.append({**row,'current_raw_storage_English':body.decode('cp932'),'current_effective_runtime_English':effective.decode('cp932'),
            'current_effective_macro_template_hex':template.hex(),'current_effective_macro_template_English':template.decode('cp932'),
            'current_effective_paragraph':' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split()),
            'registered_runtime_catalog_entry':None if registered is None else dict(table_index=binding['records'].index(registered),route_mask=registered['route_mask'],requests=registered['requests']),
            'editorial_predecessor_English_comparison_pending':True,'full_clean_context_precedes_comparison':True})
    assert len(rows) == 37
    ROOT.mkdir(parents=True)
    transcript = ROOT / 'B171_source_and_current_effective.txt'
    lines = ['Complete B171 source/current comparison. All37 clean-first glosses and current source/name/term bindings precede this exposure.']
    for row in rows:
        lines.extend(['\n' + row['id'] + ' actor' + str(row['source_selector']) + ' ancestors' + str(row.get('ancestor_0100_offsets',[])),
            'JP: ' + row['source_Japanese'],'CURRENT: ' + row['current_effective_paragraph']])
    transcript.write_text('\n'.join(lines) + '\n',encoding='utf-8')
    save(ROOT / 'all37_current_effective_comparison_packet.json', dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        clean_first_gloss=str(GLOSS),clean_first_gloss_sha256=sha(GLOSS.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),
        terms_binding=str(TERMS),terms_binding_sha256=sha(TERMS.read_bytes()),records=rows,
        all37_clean_first_meanings_names_control_paths_and_current_terms_bound=True,
        current_registered_replacements=sum(row['registered_runtime_catalog_entry'] is not None for row in rows),
        transcript=str(transcript),transcript_sha256=sha(transcript.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        no_ROM_registry_ledger_change=True,evidence={str(path):sha(path.read_bytes()) for path in [SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS,Path('translations/character_name_localization_policy_v1.json'),Path(__file__)]},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=37,progressive=37,FE=0,current_registered_replacements=sum(row['registered_runtime_catalog_entry'] is not None for row in rows),credit=0))
