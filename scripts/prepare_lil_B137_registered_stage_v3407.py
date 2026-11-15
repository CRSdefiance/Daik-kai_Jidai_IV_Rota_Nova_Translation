"""Prepare the one-block48-speech compiler andregistered cumulative stage."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    pairs=[]
    old=Path('dk4tool/patch/lil_B135_B136_editorial_v1.py');new=Path('dk4tool/patch/lil_B137_editorial_v1.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B135_B136_layout_v2':'lil_B137_layout_v3','lil_B135_B136':'lil_B137','B135-B136':'B137','B135/B136':'B137','[135,136]':'[137]',
      'all61_physical_nested_command_boundaries_and4_relative_sites_verified':'all117_physical_nested_command_boundaries_and48_relative_sites_verified','all20_relocated_relative_skip_cases_preserve_original_targets':'all240_relocated_relative_skip_cases_preserve_original_targets','all1_relocated_predicate_pair_preserves_source_operands_results_and_unowned_RAM':'all12_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM','all35_active_speech_targets_preserved':'all48_active_speech_targets_preserved',
      'all35_final_planes140_macros_static_dispatches_and_one_predicate_bound':'all48_final_planes192_macros_static_dispatches_and12_predicates_bound','all35_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all48_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text','all1_predicate_current_relocated_result_and_source_operands_equal':'all12_predicate_current_relocated_results_and_source_operands_equal',
      "len(controls['relocated_predicate_pairs'])==1":"len(controls['relocated_predicate_pairs'])==12","len(native['source_consumer_negative_controls'])==21":"len(native['source_consumer_negative_controls'])==31",
      '{2,9,14,36,47,96}':'{2,9,14,16,17,20,22,23,38,92,198}',
      "len(doc['records'])==len(refs)==35":"len(doc['records'])==len(refs)==48",'len(fonts)==35':'len(fonts)==48',
      'sum(expected_commands.values())==61':'sum(expected_commands.values())==117',"len({r['id'] for r in changes})==35":"len({r['id'] for r in changes})==48",
      'only_SC2_selected_two_blocks_changed':'only_SC2_selected_one_block_changed','all334_other_SC2_blocks_unchanged':'all335_other_SC2_blocks_unchanged','all35_speeches4_relative_operands_verified':'all48_speeches48_relative_operands_verified','all35_progressive_consumers_and_native_planes_verified':'all48_progressive_consumers_and_native_planes_verified',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old=Path('scripts/register_lil_B135_B136_v3371b.py');new=Path('scripts/register_lil_B137_v3408.py');assert not new.exists();t=old.read_text(encoding='utf-8');t=t.replace('all-routes-unified-v3372','__NEW__').replace('all-routes-unified-v3338','all-routes-unified-v3372').replace('__NEW__','all-routes-unified-v3409')
    changes={
      'lil_B135_B136_registration_v3371b':'lil_B137_registration_v3408','all_routes_combined_v3338_candidate':'all_routes_combined_v3372_candidate','lil_B135_B136_editorial_manuscript_v6':'lil_B137_editorial_manuscript_v8','lil_B135_B136_layout_v2':'lil_B137_layout_v3','lil_B135_B136_reference_approval_v3368':'lil_B137_reference_approval_v3406b','lil_B135_B136_loader_v3365b/whole_SC2_and_two_selected_blocks_initial_entry_proof':'lil_B137_loader_v3403/whole_SC2_and_one_selected_block_initial_entry_proof','editorial_handoff_verification_v3362':'editorial_handoff_verification_v3400','lil_B135_B136_relocation_v3363c':'lil_B137_relocation_v3401b',
      "len(proof['changed_records'])==35":"len(proof['changed_records'])==48","if '{MACRO:FO}' in r['english']":"if '{MACRO:FI}' in r['english']",".replace('SPEAKER:60','SPEAKER:02')":".replace('SPEAKER:02','SPEAKER:09')","'missing_source_FO'":"'missing_source_FI'",".replace('{MACRO:FO}','Argot Co.')":".replace('{MACRO:FI}','Lil')","source_complete_preamble_hex='0040ffff0002'":"source_complete_preamble_hex='0040ffff0009'",
      'all1_relocated_predicate_pair_preserves_source_operands_results_and_unowned_RAM':'all12_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM','all35_active_speech_targets_preserved':'all48_active_speech_targets_preserved','release_stack_v3371b_pending':'release_stack_v3408_pending',
      'lil_B135_B136':'lil_B137','B135-B136':'B137','B135/B136':'B137',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    a=t.index("    deps.update(['scripts/research_");z=t.index('    for path in list(deps):',a)
    names=['research_lil_B137_relocation_v3401b','prepare_lil_B137_research_v3402','verify_lil_B137_loader_v3403','verify_lil_B137_references_v3404','prove_lil_B137_relocated_controls_v3405','seal_lil_B137_references_v3406b','verify_lil_B137_fonts_v3397c','approve_lil_B137_native_v3398c','author_lil_B137_v3390b','lil_Nagarpur_money_prose_v3389','read_lil_B137_clean_context_v3386','reconcile_lil_B137_terms_v3387','refine_lil_B137_timing_complaint_v3393c','refine_lil_B137_phrase_flow_v3395','refine_lil_B137_name_prompt_v3397','correct_lil_B137_stale_row_notes_v3398d']
    t=t[:a]+'    deps.update('+repr(['scripts/'+n+'.py' for n in names])+')\n'+t[z:]
    a=t.index('    profile.update(');z=t.index("    registry['profiles'][PROFILE]",a)
    t=t[:a]+"    profile.update(lil_B137_editorial=owned.CONFIG,description='Complete V3372 cumulative stack plus48 contextual Lil B137 reviews.',note='22revisions/26justified retentions;48progressive speeches,11staticactors/FI3/12predicates/117commands/48spans/240targetskips.48nativeplanes/384logical-compiled/192finalmacro cases;sixsheets viewed orhash-exact,18rowcount-only notes. Wordlessshock andprivate-thought markers preserved. Sharedactualdisplayrules inherited byexactcode/assets;no selectednewscene/nameplate/earnedprogress. Registeredbuild/exactpatch/freshstartup pending. Experimental,preserveallROMs/translations,no promotion.')\n"+t[z:]
    t=t.replace('B137 must run once after the complete V3338 stack','B137 must run once after the complete V3372 stack')
    t=t[:t.rindex('    print(')]+"    print('RegisteredV3409 one-manuscript48-object stage;28compiler negatives reject beforemutation. FullV3372/114acceptedlayers/V1492 promotion preserved.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new));root=Path('work/analysis/lil_B137_registered_stage_tools_v3407');root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],globalhelpers_andpreviousprofiles_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
