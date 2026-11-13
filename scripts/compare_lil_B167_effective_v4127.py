"""Expose predecessor English after all29 clean glosses,native paths,names and sail terms."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_comparison_v4127')
SOURCE = Path('work/analysis/lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice.json')
GLOSS = Path('work/analysis/lil_B167_clean_context_v4117/all29_complete_B167_exchange_and_fresh_glosses.json')
CONTROL = Path('work/analysis/lil_B167_dispatches_v4121/all27_source_current_dispatches_no_macros_and6_control_leaves.json')
VOICE = Path('work/analysis/lil_B167_voices_v4120/current5_static_names_voices_and207_catalog_rebind.json')
NAMES = Path('work/analysis/lil_B167_names_v4124b/ten_original_names_owned_scratch_and_readonly_paths.json')
ENTRY = Path('work/analysis/lil_B167_entry_v4123/source_EV2_B167_action_dependency_and_native_getter_binding.json')
EFFECT = Path('work/analysis/lil_B167_controls_v4125/two_Cesare_queries_two_resources_four_paths_and6_leaves.json')
BRANCH = Path('work/analysis/lil_B167_branches_v4122/original_relative_skip_operand_proof.json')
TERMS = Path('work/analysis/lil_B167_terms_v4126/six_sail_terms_current_Refit_bodies_and_Spritsail_Jigger_labels.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source,gloss,control,voice,names,entry,effect,branch,terms=map(read,[SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS])
    assert gloss['all29_clean_first_glosses_before_predecessor_English']
    assert source['whole_exchange_context_notes_sha256']==sha(GLOSS.read_bytes())
    assert all(d['source_context_sha256']==sha(SOURCE.read_bytes()) for d in [control,voice,names,entry,effect,branch,terms])
    assert len(control['speech_dispatch_cases'])==54 and len(voice['fresh5_actor_names']['rows'])==5
    assert names['approved_prose_names']=={'2':'Lil','4':'Janus','13':'Cesare','23':'Manuel','109':'Shipwright'}
    assert len(names['native_ten_consumer_cases']['rows'])==10
    assert [(r['event_ID'],r['script_block'],r['action_index']) for r in entry['selected_B167_source_events']]==[(167,167,168)]
    assert effect['option0_accepts_lecture_option1_declines'] and effect['refusal_and_lecture_ends_are_separate']
    assert effect['both_queries_occur_after_menu_and_final_last_result_is_query_result_not_assumed_option']
    assert len(terms['six_sail_terms_bound_to_complete_current_reviewed_copies'])==6 and terms['active_Spritsail_pointer_exact']
    binding=read(control['registered_catalog_binding'])
    catalog={bytes.fromhex(r['key_hex']):r for r in binding['records'] if r['route_mask']&4}
    cases={(r['id'],r['version']):r for r in control['speech_dispatch_cases']}
    rows=[]
    for row in source['records']+source['typed_choice_records']:
        choice=row['kind']=='typed-choice-label'
        stored=bytes.fromhex(row['current_hex'])
        body=stored if choice else stored[1:]
        registered=None if choice else catalog.get(body)
        template=bytes.fromhex(registered['target_hex']) if registered else body
        effective=template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if not choice:
            assert cases[row['id'],'current-English']['boundaries'][1]['text_hex']==effective.hex()
        rows.append({**row,'current_raw_storage_English':body.decode('cp932'),
            'current_effective_runtime_English':effective.decode('cp932'),
            'current_effective_macro_template_hex':template.hex(),'current_effective_macro_template_English':template.decode('cp932'),
            'current_effective_paragraph':' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split()),
            'registered_runtime_catalog_entry':None if registered is None else dict(table_index=binding['records'].index(registered),
                route_mask=registered['route_mask'],requests=registered['requests']),
            'editorial_predecessor_English_comparison_pending':True,'full_clean_context_precedes_comparison':True})
    assert len(rows)==29
    ROOT.mkdir(parents=True)
    transcript=ROOT/'B167_source_and_current_effective.txt'
    lines=['B167 complete source/current comparison. All29 clean-first glosses and source-owned names,voices,paths and current sail terms precede this exposure.']
    for row in sorted(rows,key=lambda r:r['source_reference']['offset']):
        lines.extend(['\n'+row['id']+' '+row['kind']+' actor'+str(row.get('source_selector'))+
            ' ancestors'+str(row.get('ancestor_0100_offsets',[])),'JP: '+row['source_Japanese'],'CURRENT: '+row['current_effective_paragraph']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all29_current_effective_comparison_packet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        clean_first_gloss=str(GLOSS),clean_first_gloss_sha256=sha(GLOSS.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),
        terms_binding=str(TERMS),terms_binding_sha256=sha(TERMS.read_bytes()),records=rows,
        all29_clean_first_meanings_names_control_paths_and_current_terms_bound=True,
        current_registered_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),
        transcript=str(transcript),transcript_sha256=sha(transcript.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS,
            Path('translations/character_name_localization_policy_v1.json'),Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=29,registered_runtime_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),FI=0,credit=0))
