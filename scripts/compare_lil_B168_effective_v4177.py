"""Expose current English only after all54 clean-first glosses and exact native/term binding."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_comparison_v4177')
SOURCE=Path('work/analysis/lil_B168_source_v4168/all54_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B168_clean_context_v4167/all54_complete_B168_exchange_and_fresh_glosses.json')
CONTROL=Path('work/analysis/lil_B168_dispatches_v4171/all54_source_current_dispatches_macros_FE_and16_control_leaves.json')
VOICE=Path('work/analysis/lil_B168_voices_v4170/current8_static_names_voices_and207_catalog_rebind.json')
NAMES=Path('work/analysis/lil_B168_names_v4174/sixteen_original_name_consumers_and_owned_or_readonly_paths.json')
ENTRY=Path('work/analysis/lil_B168_entry_v4173/source_EV2_B168_action_dependency_and_native_getter_binding.json')
EFFECT=Path('work/analysis/lil_B168_controls_v4175/three_predicates_four_resources_six_presentations_and16_leaves.json')
BRANCH=Path('work/analysis/lil_B168_branches_v4172/original_relative_skip_operand_proof.json')
TERMS=Path('work/analysis/lil_B168_terms_v4176/current_Deck_officers_items_X_Brunei_and_naturalist_wording.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,control,voice,names,entry,effect,branch,terms=map(read,[SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS])
    assert gloss['all54_clean_first_glosses_before_predecessor_English'] and source['whole_exchange_context_notes_sha256']==sha(GLOSS.read_bytes())
    assert all(d['source_context_sha256']==sha(SOURCE.read_bytes()) for d in [control,voice,names,entry,effect,branch,terms])
    assert len(control['speech_dispatch_cases'])==108 and len(voice['fresh8_actor_names']['rows'])==8 and len(names['native_sixteen_consumer_cases']['rows'])==16
    assert [(r['event_ID'],r['script_block'],r['action_index']) for r in entry['selected_B168_source_events']]==[(168,168,169)]
    assert effect['source_declared_end_offsets']==[2906,2910] and len(effect['source_predicate_cases'])==3 and len(branch['cases'])==120
    binding=read(control['registered_catalog_binding']);catalog={bytes.fromhex(r['key_hex']):r for r in binding['records'] if r['route_mask']&4}
    cases={(r['id'],r['version']):r for r in control['speech_dispatch_cases']};rows=[]
    for r in source['records']:
        stored=bytes.fromhex(r['current_hex']);body=stored[1:];registered=catalog.get(body)
        template=bytes.fromhex(registered['target_hex']) if registered else body
        effective=template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert cases[r['id'],'current-English']['boundaries'][1]['text_hex']==effective.hex()
        rows.append({**r,'current_raw_storage_English':body.decode('cp932'),'current_effective_runtime_English':effective.decode('cp932'),'current_effective_macro_template_hex':template.hex(),'current_effective_macro_template_English':template.decode('cp932'),'current_effective_paragraph':' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split()),'registered_runtime_catalog_entry':None if registered is None else dict(table_index=binding['records'].index(registered),route_mask=registered['route_mask'],requests=registered['requests']),'editorial_predecessor_English_comparison_pending':True,'full_clean_context_precedes_comparison':True})
    assert len(rows)==54
    ROOT.mkdir(parents=True);transcript=ROOT/'B168_source_and_current_effective.txt'
    lines=['B168 complete source/current comparison. All54 clean-first glosses,source-owned identities,control paths and UI terms precede this exposure.']
    for r in rows:lines.extend(['\n'+r['id']+' '+r['kind']+' actor'+str(r['source_selector'])+' ancestors'+str(r.get('ancestor_0100_offsets',[])),'JP: '+r['source_Japanese'],'CURRENT: '+r['current_effective_paragraph']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all54_current_effective_comparison_packet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_first_gloss=str(GLOSS),clean_first_gloss_sha256=sha(GLOSS.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),terms_binding=str(TERMS),terms_binding_sha256=sha(TERMS.read_bytes()),records=rows,all54_clean_first_meanings_names_control_paths_and_current_terms_bound=True,current_registered_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),transcript=str(transcript),transcript_sha256=sha(transcript.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,CONTROL,VOICE,NAMES,ENTRY,EFFECT,BRANCH,TERMS,Path('translations/character_name_localization_policy_v1.json'),Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=54,progressive=51,FE=3,current_registered_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),credit=0))
