"""Expose all36 current paragraphs after clean glosses and current source/name/term binding."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_comparison_v4220')
SOURCE = Path('work/analysis/lil_B169_source_v4211/all36_clean_current_complete_context.json')
GLOSS = Path('work/analysis/lil_B169_clean_context_v4210/all36_complete_B169_exchange_and_fresh_glosses.json')
CONTROL = Path('work/analysis/lil_B169_dispatches_v4214/all36_source_current_dispatches_FI5_FO2_and5_control_leaves.json')
VOICE = Path('work/analysis/lil_B169_voices_v4213/current6_static_names_voices_and207_catalog_rebind.json')
NAMES = Path('work/analysis/lil_B169_names_v4217/twelve_original_name_consumers_and_owned_scratch_paths.json')
ENTRY = Path('work/analysis/lil_B169_entry_v4216/source_EV2_B169_action_dependency_and_native_getter_binding.json')
EFFECT = Path('work/analysis/lil_B169_controls_v4218/three_predicates_five_leaves_and_eight_source_paths.json')
BRANCH = Path('work/analysis/lil_B169_branches_v4215/original_relative_skip_operand_proof.json')
TERMS = Path('work/analysis/lil_B169_terms_v4219/current_Proof_title_Tavern_ruins_names_and_older_variant_refs.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source, gloss, control, voice, names, entry, effect, branch, terms = map(read,[SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS])
    assert gloss['all36_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert source['whole_exchange_context_notes_sha256'] == sha(GLOSS.read_bytes())
    assert all(proof['source_context_sha256'] == sha(SOURCE.read_bytes()) for proof in [control,voice,names,entry,effect,branch,terms])
    assert len(control['speech_dispatch_cases']) == 72 and len(voice['fresh6_actor_names']['rows']) == 6
    assert len(names['native_twelve_consumer_cases']['rows']) == 12
    assert [(row['event_ID'],row['script_block'],row['action_index']) for row in entry['selected_B169_source_events']] == [(169,169,170)]
    assert effect['source_declared_end_offsets'] == [2558] and len(effect['source_predicate_cases']) == 3 and len(branch['cases']) == 120
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
    assert len(rows) == 36
    ROOT.mkdir(parents=True)
    transcript = ROOT / 'B169_source_and_current_effective.txt'
    lines = ['Complete B169 source/current comparison. All36 clean-first glosses and current source/name/term bindings precede this exposure.']
    for row in rows:
        lines.extend(['\n' + row['id'] + ' actor' + str(row['source_selector']) + ' ancestors' + str(row.get('ancestor_0100_offsets',[])),
            'JP: ' + row['source_Japanese'],'CURRENT: ' + row['current_effective_paragraph']])
    transcript.write_text('\n'.join(lines) + '\n',encoding='utf-8')
    save(ROOT / 'all36_current_effective_comparison_packet.json', dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        clean_first_gloss=str(GLOSS),clean_first_gloss_sha256=sha(GLOSS.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),
        terms_binding=str(TERMS),terms_binding_sha256=sha(TERMS.read_bytes()),records=rows,
        all36_clean_first_meanings_names_control_paths_and_current_terms_bound=True,
        current_registered_replacements=sum(row['registered_runtime_catalog_entry'] is not None for row in rows),
        transcript=str(transcript),transcript_sha256=sha(transcript.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        no_ROM_registry_ledger_change=True,evidence={str(path):sha(path.read_bytes()) for path in [SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS,Path('translations/character_name_localization_policy_v1.json'),Path(__file__)]},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=36,progressive=36,FE=0,current_registered_replacements=sum(row['registered_runtime_catalog_entry'] is not None for row in rows),credit=0))
