"""Expose B166 predecessor English only after44 clean glosses and native/term/control bindings."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_comparison_v4063')
SOURCE=Path('work/analysis/lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice.json')
GLOSS=Path('work/analysis/lil_B166_clean_context_v4053/all44_complete_B166_exchange_and_fresh_glosses.json')
CONTROL=Path('work/analysis/lil_B166_dispatches_v4057/all42_source_current_dispatches_FI3_and11_control_leaves.json')
VOICE=Path('work/analysis/lil_B166_voices_v4056/current4_static_names_voices_and207_catalog_rebind.json')
NAMES=Path('work/analysis/lil_B166_names_v4060/six_original_Manuel_Fernando_Camille_name_consumers.json')
ENTRY=Path('work/analysis/lil_B166_entry_v4059/source_EV2_B166_action_dependency_and_native_getter_binding.json')
EFFECT=Path('work/analysis/lil_B166_controls_v4061/Fernando_predicate_two_resources_advice_paths_and11_leaves.json')
BRANCH=Path('work/analysis/lil_B166_branches_v4058/original_relative_skip_operand_proof.json')
TERMS=Path('work/analysis/lil_B166_terms_v4062/nine_rooms_active_Speech_Shipwright_Surgeon_and_source_distinctions.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,control,voice,names,entry,effect,branch,terms=map(read,[SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS])
    assert gloss['all44_clean_first_glosses_before_predecessor_English'] and source['whole_exchange_context_notes_sha256']==sha(GLOSS.read_bytes())
    assert all(d['source_context_sha256']==sha(SOURCE.read_bytes()) for d in [control,voice,names,entry,effect,branch,terms])
    assert len(control['speech_dispatch_cases'])==84 and len(voice['fresh4_actor_names']['rows'])==4
    assert names['approved_prose_names']=={'23':'Manuel Almeida','20':'Fernando Dias','9':'Camille'}
    assert [(r['event_ID'],r['script_block'],r['action_index']) for r in entry['selected_B166_source_events']]==[(166,166,167)]
    assert [r['spoken_source_record_indices'] for r in effect['advice_choice_paths']]==[[149,153,157,161,165,169,172,175],[181]]
    assert terms['entire_HELP_exact_to_reviewed_skill_release'] and len(terms['nine_room_terms_bound_to_complete_current_topics'])==9
    binding=read(control['registered_catalog_binding']);catalog={bytes.fromhex(r['key_hex']):r for r in binding['records'] if r['route_mask']&4};cases={(r['id'],r['version']):r for r in control['speech_dispatch_cases']};rows=[]
    for r in source['records']+source['typed_choice_records']:
        choice=r['kind']=='typed-choice-label';stored=bytes.fromhex(r['current_hex']);body=stored if choice else stored[1:];entry=None if choice else catalog.get(body);template=bytes.fromhex(entry['target_hex']) if entry else body
        effective=template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if not choice:assert cases[r['id'],'current-English']['boundaries'][1]['text_hex']==effective.hex()
        rows.append({**r,'current_raw_storage_English':body.decode('cp932'),'current_effective_runtime_English':effective.decode('cp932'),'current_effective_macro_template_hex':template.hex(),'current_effective_macro_template_English':template.decode('cp932'),'current_effective_paragraph':' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split()),'registered_runtime_catalog_entry':None if entry is None else dict(table_index=binding['records'].index(entry),route_mask=entry['route_mask'],requests=entry['requests']),'editorial_predecessor_English_comparison_pending':True,'full_clean_context_precedes_comparison':True})
    assert len(rows)==44;ROOT.mkdir(parents=True);lines=['B166 complete source/current comparison;all44 clean-first glosses,original names/voices,branch/getter bindings andcurrent Help terms precede exposure. Advice choices do not decide hiring.']
    for r in sorted(rows,key=lambda r:r['source_reference']['offset']):lines.extend(['\n'+r['id']+' '+r['kind']+' actor'+str(r.get('source_selector'))+' ancestors'+str(r.get('ancestor_0100_offsets',[])),'JP: '+r['source_Japanese'],'CURRENT: '+r['current_effective_paragraph']])
    transcript=ROOT/'B166_source_and_current_effective.txt';transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all44_current_effective_comparison_packet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_first_gloss=str(GLOSS),clean_first_gloss_sha256=sha(GLOSS.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),terms_binding=str(TERMS),terms_binding_sha256=sha(TERMS.read_bytes()),records=rows,all44_clean_first_meanings_names_control_paths_and_current_terms_bound=True,current_registered_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),transcript=str(transcript),transcript_sha256=sha(transcript.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS,Path('translations/character_name_localization_policy_v1.json'),Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=44,registered_runtime_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),FI=3,credit=0))
