"""Prepare effective-current comparison only after fresh63 source glosses."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    old=Path('scripts/prepare_lil_B122_B127_comparison_v3268.py');new=Path('scripts/compare_lil_B131_B133_effective_v3314b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B122_B127_comparison_v3268':'lil_B131_B133_comparison_v3314b',
      'work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json':'work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json',
      'work/analysis/lil_B122_B127_controls_v3266/all155_source_current_dispatch_FE_null_actor_and14_predicates.json':'work/analysis/lil_B131_B133_controls_v3308b/all61_source_current_dispatch_selector00_FE_and5_predicates.json',
      'work/analysis/lil_B122_B127_clean_context_v3263/all159_complete_clean_exchange_context_notes.json':'work/analysis/lil_B131_B133_clean_context_v3312/all63_complete_clean_context_and_fresh_glosses.json',
      'work/analysis/lil_B122_B127_terms_v3267/clean_current_items_Spirit_static_actors_and_related_terms.json':'work/analysis/lil_B131_B133_terms_v3313/clean_current_items_names_and_share_ratio_reconciliation.json',
      "WAIT=Path('work/analysis/lil_B122_original2000_waits_v3265/original2000_actual_rule_and_current_source_binding.json')\n":'',
      'source,control,context,terms,wait=map(read,[SOURCE,CONTROL,CONTEXT,TERMS,WAIT])':'source,control,context,terms=map(read,[SOURCE,CONTROL,CONTEXT,TERMS])',
      'all159_clean_source_objects_read_before_older_English_comparison':'all63_complete_clean_source_objects_read_before_older_English_comparison',
      "    assert wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']\n":"    assert context['all63_fresh_source_glosses_precede_localized_English']\n",
      'len(rows)==159':'len(rows)==63',
      'Current names, FE null actor, FI, predicates, item/stat terms and original2000 illustration-pause rule bound.':'Current names including static00 Rafael,FE null actor,FI/FO,five predicates,item names andtwo-to-one share terms bound.',
      ';assert replacements==6':'',
      'all159_current_effective_comparison_packet.json':'all63_current_effective_comparison_packet.json',
      'original2000_wait_proof=str(WAIT),original2000_wait_proof_sha256=sha(WAIT.read_bytes()),':'fresh63_glosses_precede_current_English_comparison=True,',
      'all159_current_English_editorial_reading_still_pending':'all63_current_English_editorial_reading_still_pending'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    t=t[:t.rindex('    print(')]+"    print(dict(source_current_comparisons=63,registered_runtime_replacements=replacements,complete_editorial_reading_and_decisions_still_pending=True,credit=0))\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_comparison_tools_v3314');root.mkdir(parents=True);save(root/'clean_first_comparison_successor.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),all63_fresh_source_glosses_written_before_current_English_comparison=True,no_old_producer_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
