"""Prepare the cumulative stage and meaningful source00 compiler negatives."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/register_lil_B122_B127_v3299b.py');new=Path('scripts/register_lil_B131_B133_v3337b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B122_B127_editorial_v2':'lil_B131_B133_editorial_v1',
      'lil_B122_B127_registration_v3299b':'lil_B131_B133_registration_v3337b',
      'all-routes-unified-v3300':'all-routes-unified-v3338','all-routes-unified-v3251':'all-routes-unified-v3300',
      'all_routes_combined_v3251_candidate':'all_routes_combined_v3300_candidate',
      'lil_B122_B127_editorial_manuscript_v6':'lil_B131_B133_editorial_manuscript_v5',
      'lil_B122_B127_choice_manuscript_v5':'lil_B131_B133_choice_manuscript_v6',
      'lil_B122_B127_editorial_relocation_map_v1':'lil_B131_B133_editorial_relocation_map_v1',
      'lil_B122_B127_profile_v2':'lil_B131_B133_profile','lil_B122_B127_layout_v2':'lil_B131_B133_layout_v2',
      'lil_B122_B127_reference_approval_v3295':'lil_B131_B133_reference_approval_v3335b',
      'lil_B122_B127_loader_v3290/whole_SC2_and_six_selected_blocks_initial_entry_proof':'lil_B131_B133_loader_v3331/whole_SC2_and_two_selected_blocks_initial_entry_proof',
      'editorial_handoff_verification_v3297':'editorial_handoff_verification_v3328',
      "'original2000_wait_proof','conditional_return_proof',":"'whole_typed_speech_proof',",
      'lil_B122_B127_relocation_v3288b':'lil_B131_B133_relocation_v3329b',
      'dk4-lil-B122-B127-editorial-release-v1':'dk4-lil-B131-B133-editorial-release-v1',
      "len(proof['changed_records'])==159":"len(proof['changed_records'])==63",
      ".replace('SPEAKER:97','SPEAKER:02')":".replace('SPEAKER:02','SPEAKER:05')",
      'source_complete_preamble_hex=\'0040ffff005c\'':'source_complete_preamble_hex=\'0040ffff0005\'',
      'all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM':'all5_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM',
      'all155_active_speech_targets_preserved':'all61_active_speech_targets_preserved',
      'two2100_objects_four_labels_and_source_indices_0_1_cancel_verified':'one2100_object_two_labels_and_source_indices_0_1_cancel_verified',
      'two_original2000_pause_words_and_mapped_resume_boundaries_verified':'no_source2000_pause_commands',
      'trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified':'all18_source00_prefixes_and_nonempty_bodies_verified',
      'lil_B122_B127_editorial':'lil_B131_B133_editorial',
      'release_stack_v3299b_pending':'release_stack_v3337b_pending',
      'B122-B127 must run once after the complete V3251 stack':'B131/B133 must run once after the complete V3300 stack',
    }
    # Do not cascade the two profile versions.
    t=t.replace('all-routes-unified-v3300','__NEWPROFILE__').replace('all-routes-unified-v3251','all-routes-unified-v3300').replace('__NEWPROFILE__','all-routes-unified-v3338')
    changes.pop('all-routes-unified-v3300');changes.pop('all-routes-unified-v3251')
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    a=t.index('    for p in [\'scripts/research_');z=t.index('    for path in list(deps):',a)
    scripts=['research_lil_B131_B133_relocation_v3329b','prepare_lil_B131_B133_research_v3330b','verify_lil_B131_B133_loader_v3331','verify_lil_B131_B133_references_v3332','prove_lil_B131_B133_relocated_controls_v3333b','reconcile_lil_B131_B133_sampling_v3334','seal_lil_B131_B133_references_v3335b','verify_lil_B131_B133_fonts_v3324b','verify_lil_B131_B133_FE_v3325','prove_lil_B131_B133_choices_v3321c','approve_lil_B131_B133_native_v3326','author_lil_B131_B133_v3316','lil_map_Rafael_share_trade_prose_v3315','prove_lil_source00_typed_speech_v3323','refine_lil_share_acceptance_v3321c','refine_lil_B131_B133_phrase_flow_v3322','lil_kuhn_china_FE_painter_v2909']
    t=t[:a]+'    deps.update('+repr(['scripts/'+p+'.py' for p in scripts])+')\n'+t[z:]
    t='\n'.join(line for line in t.split('\n') if not any(s in line for s in ["def b126(","def pause(","('pause_deleted'","('pause_old_offset_changed'","('pause_new_offset_changed'","('pause_resume_changed'","('pause_source_resume_changed'","('return_mapped_extent_changed'"]))
    anchor='    changes=[\n';assert anchor in t
    zero="""    def zero(d):return next(r for r in d['records'] if r['source_selector']==0)
"""
    t=t.replace(anchor,zero+anchor+"""      ('zero_missing_actor',DOC,'manuscript',lambda d:zero(d).update(english=zero(d)['english'].split('}',1)[1])),
      ('zero_wrong_actor',DOC,'manuscript',lambda d:zero(d).update(english=zero(d)['english'].replace('SPEAKER:00','SPEAKER:02'))),
      ('zero_embedded_NUL',DOC,'manuscript',lambda d:zero(d).update(english=zero(d)['english']+'\\0')),
      ('zero_duplicate_compiled_prefix',DOC,'manuscript',lambda d:zero(d).update(compiled_hex='00'+zero(d)['compiled_hex'])),
      ('zero_wrong_clean_body',DOC,'manuscript',lambda d:zero(d).update(source_hex='0000')),
      ('zero_changed_selector_scope',DOC,'manuscript',lambda d:zero(d).update(source_selector=2)),
""")
    a=t.index("    profile.update(");z=t.index("    registry['profiles'][PROFILE]",a)
    t=t[:a]+"    profile.update(lil_B131_B133_editorial=owned.CONFIG,description='Complete V3300 cumulative stack plus63 contextual Lil B131/B133 reviews.',note='27 revisions/36 justified retentions;61 speech including18 source00 Rafael andone FE,plus2 labels.112 commands/24 spans/120 relocated skips/five predicates. Complete native planes,leading-H menu resolution,source00 full bodies andLil-context macros pass. Shared actual display rules inherited under exact code/data binding;no selected conditional scene or earned progress claimed. Registered build,exact clean patch andfresh startup pending. Experimental;preserve all ROMs andtranslations;no promotion.')\n"+t[z:]
    t=t.replace('Register159 guarded reviews after the complete V3251 cumulative stack.','Register63 guarded reviews after the complete V3300 cumulative stack.')
    t=t[:t.rindex('    print(')]+"    print('RegisteredV3338 cumulative63-object stage;50 compiler negatives reject before mutation. Priorprofiles,114acceptedlayers andV1492 promotion preserved.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_registration_tools_v3337');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
