"""Bind approved addresses,source thought markers andthe exact wage ratio."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B137_terms_v3387')
SOURCE=Path('work/analysis/lil_remaining_B137_B140_source_v3380b/next48_B137_clean_current_context.json')
VOICE=Path('work/analysis/lil_B137_voices_v3383b/current_eleven_static_names_voices_and207_catalog_rebind.json')
CONTEXT=Path('work/analysis/lil_B137_clean_context_v3386/all48_complete_clean_context_and_fresh_glosses.json')
if __name__=='__main__':
    assert not ROOT.exists();source,voice,context=map(read,[SOURCE,VOICE,CONTEXT]);assert context['all48_complete_clean_source_objects_read_before_older_English_comparison'] and context['all48_fresh_source_glosses_precede_localized_English']
    names={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh_eleven_actor_names']['rows']};assert set(names)=={2,9,14,16,17,20,22,23,38,92,198} and names[38]=='Zamorin Ahmad Nagarpur' and names[198]=='Benazir'
    rows={r['source_record_index']:r for r in source['records']};assert '５倍' in rows[258]['source_Japanese'] and rows[276]['source_Japanese']=='！' and rows[231]['source_Japanese'].startswith('（FI') and rows[231]['source_Japanese'].endswith('）')
    refs=[{k:rows[i][k] for k in ['id','source_reference','source_hex','source_Japanese']} for i in [6,89,92,137,145,156,168,175,192,198,208,231,245,258,276,302]]
    ROOT.mkdir(parents=True);terms=ROOT/'clean_current_names_addresses_thought_and_fivefold_wages.json'
    save(terms,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_clean_context=str(CONTEXT),complete_clean_context_sha256=sha(CONTEXT.read_bytes()),voice_proof=str(VOICE),voice_proof_sha256=sha(VOICE.read_bytes()),exact_current_actor_names=names,approved_dialogue_names=dict(Lil='Lil',Camille='Camille',Emilio='Emilio',Gerhard='Gerhard',Al='Al',Fernando='Fernando',Samwell='Samwell',Manuel='Manuel',Nagarpur='Nagarpur',Benazir='Benazir',barkeep='unnamed barkeep;not Lil\'s uncle'),exact_source_references=refs,Nagarpur_sama_uses_ordinary_respectful_Mr_Nagarpur_without_invented_noble_rank=True,Nagarpur_current_catalogue_Zamorin_title_not_newly_inserted_into_unrelated_addresses=True,admiral_only_where_explicit_in_Gerhard_and_Manuel_source=True,tavern_worker_is_Nagarpur_mistaken_assumption_not_Lil_actual_job=True,leering_touch_does_not_authorize_invented_body_parts_or_romance=True,lower_middle_rating_is_backhanded_praise_not_new_physical_measurement=True,parenthesized_Camille_private_thought_preserves_FI=True,FI3_uses_Lil_captain2_context=True,navigators_and_sailors_five_times_wages_are_hypothetical=True,bare_exclamation_is_source_wordless_shock_not_placeholder=True,poetry_notes_are_Manuel_existing_notes_not_new_item=True,paradise_boast_and_Fernando_echo_reviewed_together=True,no_items_or_Proof_term_in_this_exchange=True,whole_goal_Proof_consistency_reconciliation_remains_open_separate_from_technical_reaudit=True,no_old_completed_record_reopened_recounted_or_silently_renamed=True,no_ROM_registry_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    old=Path('scripts/compare_lil_B135_B136_effective_v3353c.py');new=Path('scripts/compare_lil_B137_effective_v3388.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B135_B136_comparison_v3353':'lil_B137_comparison_v3388',
      'work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json':str(SOURCE).replace('\\','/'),
      'work/analysis/lil_B135_B136_controls_v3347/all35_source_current_dispatches_and1_predicate.json':'work/analysis/lil_B137_controls_v3384/all48_source_current_dispatches_and12_predicates.json',
      'work/analysis/lil_B135_B136_clean_context_v3349/all35_complete_clean_context_and_fresh_glosses.json':str(CONTEXT).replace('\\','/'),
      'work/analysis/lil_B135_B136_terms_v3352/clean_current_tablets_narcotic_names_and_wordplay_reconciliation.json':str(terms).replace('\\','/'),
      'all35_complete_clean_source_objects_read_before_older_English_comparison':'all48_complete_clean_source_objects_read_before_older_English_comparison',
      'all35_fresh_source_glosses_precede_localized_English':'all48_fresh_source_glosses_precede_localized_English',
      'len(rows)==35':'len(rows)==48','all35_current_effective_comparison_packet':'all48_current_effective_comparison_packet','fresh35_glosses':'fresh48_glosses','all35_current_English':'all48_current_English','source_current_comparisons=35':'source_current_comparisons=48',
      'Six static names,FO1,one predicate,tablet item names andthe existing narcotic name bound.':'Eleven static names,FI3,twelve predicates,thought/wordless-shock markers andfivefold hypothetical wages bound.',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');save(ROOT/'comparison_tool_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes())))
    print('Nagarpur/Benazir andnineotherstatic names,ordinary addresses,source thought/emote andhypotheticalfivefold wages bound. OldEnglish comparison prepared;zero credit.')
