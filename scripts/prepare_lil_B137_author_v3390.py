"""Prepare the48-record contextual manuscript from source-first glosses."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/author_lil_B135_B136_v3355.py');new=Path('scripts/author_lil_B137_v3390b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'scripts.lil_Espinosa_tablet_prose_v3354':'scripts.lil_Nagarpur_money_prose_v3389',
      'lil_B135_B136_author_v3355':'lil_B137_author_v3390b',
      'work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json':'work/analysis/lil_remaining_B137_B140_source_v3380b/next48_B137_clean_current_context.json',
      'lil_B135_B136_comparison_v3353/all35_current_effective_comparison_packet':'lil_B137_comparison_v3388/all48_current_effective_comparison_packet',
      'lil_B135_B136_clean_context_v3349/all35_complete_clean_context_and_fresh_glosses':'lil_B137_clean_context_v3386/all48_complete_clean_context_and_fresh_glosses',
      'lil_B135_B136_controls_v3347/all35_source_current_dispatches_and1_predicate':'lil_B137_controls_v3384/all48_source_current_dispatches_and12_predicates',
      'lil_B135_B136_voices_v3346b/current_six_static_names_voices_and207_catalog_rebind':'lil_B137_voices_v3383b/current_eleven_static_names_voices_and207_catalog_rebind',
      'lil_B135_B136_terms_v3352/clean_current_tablets_narcotic_names_and_wordplay_reconciliation':'lil_B137_terms_v3387/clean_current_names_addresses_thought_and_fivefold_wages',
      'lil_B135_B136_branches_v3348b':'lil_B137_branches_v3385b',
      'scripts/lil_Espinosa_tablet_prose_v3354.py':'scripts/lil_Nagarpur_money_prose_v3389.py',
      'lil_B135_B136_editorial_manuscript_v1':'lil_B137_editorial_manuscript_v1',
      'all35_complete_clean_source_objects_read_before_older_English_comparison':'all48_complete_clean_source_objects_read_before_older_English_comparison',
      'all35_fresh_source_glosses_precede_localized_English':'all48_fresh_source_glosses_precede_localized_English',
      "len(comparison['records'])==35 and comparison['registered_runtime_catalog_replacement_count']==1":"len(comparison['records'])==48 and comparison['registered_runtime_catalog_replacement_count']==0",
      "len(control['speech_dispatch_cases'])==70 and len(control['current_original_predicate_cases'])==1":"len(control['speech_dispatch_cases'])==96 and len(control['current_original_predicate_cases'])==12",
      "speakers={2:'Lil Argot',9:'Camille',14:'Emilio',36:'Espinosa',47:'Gilberto',96:'Customer;unnamed distressed man'}":"speakers={2:'Lil Argot',9:'Camille',14:'Emilio',16:'Gerhard',17:'Al',20:'Fernando',22:'Samwell',23:'Manuel',38:'Nagarpur',92:'Barkeep;unnamed',198:'Benazir'}",
      'Allsix static actors andLil-context FO are bound':'Alleleven static actors andLil-context FI are bound',
      "len(rows)==35 and counts['revise']+counts['retain-wording']==35":"len(rows)==48 and counts['revise']+counts['retain-wording']==48",
      'all35_contextual_prose_or_retention_receipt':'all48_contextual_prose_or_retention_receipt',
      'all35_clean_then_current_complete_exchanges_read':'all48_clean_then_current_complete_exchanges_read',
      'all35_fresh_glosses_precede_localized_English':'all48_fresh_glosses_precede_localized_English',
      'all35_individual_revision_or_retention_notes':'all48_individual_revision_or_retention_notes',
      'one_registered_Camille_replacement_preserved_as_effective_current_provenance=True':'zero_registered_catalogue_replacements_raw_and_effective_provenance_separate=True',
      'chart_cheese_tart_wordplay_adaptation_documented_without_new_item_orplot=True':'rating_joke_Fernando_Camille_conditions_and_wordless_shock_fivefold_wages_reviewed=True',
      'objects=35':'objects=48',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B137_author_tools_v3390');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
