"""Prepare one-block48-speech relocation andcomplete final-reference proofs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B137_reference_tools_v3401');assert not root.exists();pairs=[]
    def make(a,b,changes):
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        for x,y in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert x in t,x;t=t.replace(x,y)
        return old,new,t
    old,new,t=make('scripts/research_lil_B135_B136_relocation_v3363c.py','scripts/research_lil_B137_relocation_v3401b.py',{
      'lil_B135_B136_relocation_v3363c':'lil_B137_relocation_v3401b','lil_B135_B136_editorial_manuscript_v5':'lil_B137_editorial_manuscript_v7','all_routes_combined_v3338_candidate':'all_routes_combined_v3372_candidate',
      "len(results)==2 and sum(len(r['text_records']) for r in results)==35":"len(results)==1 and sum(len(r['text_records']) for r in results)==48",
      "sum(len(r['relative_skip_fixups']) for r in results)==4":"sum(len(r['relative_skip_fixups']) for r in results)==48",
      "sum(len(r['target_native_skip_cases']) for r in results)==20":"sum(len(r['target_native_skip_cases']) for r in results)==240",
      "sum(len(r['command_map']) for r in results)==61":"sum(len(r['command_map']) for r in results)==117",
      '[135,136]':'[137]','all35speech_and4_relative_operands_preserved':'all48speech_and48_relative_operands_preserved','all20_relocated_native_skip_cases_match_original_target_mapping':'all240_relocated_native_skip_cases_match_original_target_mapping','all334_other_SC2_blocks_exact':'all335_other_SC2_blocks_exact'})
    t=t[:t.rindex("    print('")]+"    print('117commands/48speech/48spans/240targetskipcases,inversebytes and335otherblocks exact. Researchonly.')\n";compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=make('scripts/prepare_lil_B135_B136_research_v3364b.py','scripts/prepare_lil_B137_research_v3402.py',{
      'lil_B135_B136_research_v3364b':'lil_B137_research_v3402','all_routes_combined_v3338_candidate':'all_routes_combined_v3372_candidate','lil_B135_B136_V3338_derived_RESEARCH_ONLY':'lil_B137_V3372_derived_RESEARCH_ONLY','lil_B135_B136_relocation_v3363c':'lil_B137_relocation_v3401b',
      'lil_B135_B136_native_approval_v3360/all35_native_macro_font_and_source_reconciliation':'lil_B137_native_approval_v3398b/all48_native_macro_font_and_source_reconciliation',
      'verify_lil_B135_B136_fonts_v3359b':'verify_lil_B137_fonts_v3397c','lil_B135_B136_fonts_v3359':'lil_B137_fonts_v3397c',
      'all35speech_and4_relative_operands_preserved':'all48speech_and48_relative_operands_preserved','all20_relocated_native_skip_cases_match_original_target_mapping':'all240_relocated_native_skip_cases_match_original_target_mapping',
      '[135,136]':'[137]','value[0] in [2,9,14,36,47,96]':'value[0] in [2,9,14,16,17,20,22,23,38,92,198]',
      'len(parity)==35 and macro_calls==140':'len(parity)==48 and macro_calls==192','all334_other_SC2_blocks_every_other_file_and_native_component_exact':'all335_other_SC2_blocks_every_other_file_and_native_component_exact',
      'all35_final_targets_complete_native_planes_equal_reviewed_planes':'all48_final_targets_complete_native_planes_equal_reviewed_planes','current_final_padded_macro_alignment_cases=140':'current_final_padded_macro_alignment_cases=192',
      'all35_final_speech_prefixes_and_nonempty_bodies_preserved':'all48_final_speech_prefixes_and_nonempty_bodies_preserved','all35_complete_source_static_prefixes_preserved':'all48_complete_source_static_prefixes_preserved','all35_progressive_final_planes_and140_macro_alignments_bound':'all48_progressive_final_planes_and192_macro_alignments_bound',
      'actual_selected_B135_B136_IDs':'actual_selected_B137_IDs','V3338-derived two-block':'V3372-derived one-block'})
    t=t[:t.rindex('    print(')]+"    print('Researchimage changesB137only;48final nativeplanes/192macro cases and335otherblocks/allotherfiles/components exact. Not arelease ornewparent.')\n";compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=make('scripts/verify_lil_B135_B136_loader_v3365c.py','scripts/verify_lil_B137_loader_v3403.py',{
      'prepare_lil_B135_B136_research_v3364b':'prepare_lil_B137_research_v3402','lil_B135_B136_loader_v3365b':'lil_B137_loader_v3403','lil_B135_B136_research_v3364b':'lil_B137_research_v3402','two_selected_blocks':'one_selected_block','B135/B136':'B137'})
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=make('scripts/verify_lil_B135_B136_references_v3366b.py','scripts/verify_lil_B137_references_v3404.py',{
      'prepare_lil_B135_B136_research_v3364b':'prepare_lil_B137_research_v3402','lil_B135_B136_reference_census_v3366b':'lil_B137_reference_census_v3404','lil_B135_B136_loader_v3365b':'lil_B137_loader_v3403','two_selected_blocks':'one_selected_block','[135,136]':'[137]',
      "sum(len(r['mapped_commands'])for r in result)==61":"sum(len(r['mapped_commands'])for r in result)==117","sum(r['typed_relative_span_count']for r in result)==4":"sum(r['typed_relative_span_count']for r in result)==48","sum(r['target_native_skip_cases']for r in result)==20":"sum(r['target_native_skip_cases']for r in result)==240",
      'all61_commands4_relative_sites':'all117_commands48_relative_sites','all61_clean_current_target_commands_and4_relative_sites_reexecuted':'all117_clean_current_target_commands_and48_relative_sites_reexecuted','all334_other_SC2_blocks_preserved':'all335_other_SC2_blocks_preserved','native_commands_each=61,relative_sites=4,target_native_skip_cases=20':'native_commands_each=117,relative_sites=48,target_native_skip_cases=240'})
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=make('scripts/prove_lil_B135_B136_relocated_controls_v3367b.py','scripts/prove_lil_B137_relocated_controls_v3405.py',{
      'prepare_lil_B135_B136_research_v3364b':'prepare_lil_B137_research_v3402','lil_B135_B136_relocated_controls_v3367b':'lil_B137_relocated_controls_v3405','lil_B135_B136_editorial_manuscript_v5':'lil_B137_editorial_manuscript_v7','lil_B135_B136_reference_census_v3366b/all61_commands4_relative_sites':'lil_B137_reference_census_v3404/all117_commands48_relative_sites','lil_B135_B136_fonts_v3359':'lil_B137_fonts_v3397c','len(dispatches)==35':'len(dispatches)==48','len(predicates)==1':'len(predicates)==12',
      'all35_relocated_dispatches_and1_predicate_pair':'all48_relocated_dispatches_and12_predicate_pairs','all35_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all48_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text','all1_predicate_current_relocated_result_and_source_operands_equal':'all12_predicate_current_relocated_results_and_source_operands_equal','all_six_static_speaker_selectors_preserved_without_role_assignment':'all_eleven_static_speaker_selectors_preserved_without_role_assignment','actual_selected_B135_B136_IDs':'actual_selected_B137_IDs'})
    t=t[:t.rindex('    print(')]+"    print('48relocated staticdispatches/12predicatepairs pass;source operands/results/unownedRAM exact. No selectedgameplay orrelease claim.')\n";compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new));root.mkdir(parents=True)
    save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],allprevious_ROMs_producers_andproofs_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
