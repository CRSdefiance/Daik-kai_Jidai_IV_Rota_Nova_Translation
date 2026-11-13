"""Prepare final native planes, whole loaders and entry census for nine blocks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B111_B119_reference_tools_v3240')
if __name__=='__main__':
    assert not ROOT.exists();pairs=[]
    def generate(old,new,swaps):
        old,new=Path(old),Path(new);assert not new.exists();t=old.read_text(encoding='utf-8')
        for a,b in swaps.items():assert a in t,a;t=t.replace(a,b)
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes())))
    generate('scripts/prepare_lil_shrines_research_v3194.py','scripts/prepare_lil_B111_B119_research_v3240b.py',{
        'lil_Shrines_Temples_research_v3194':'lil_B111_B119_research_v3240b',
        'lil_Shrines_Temples_V3144_derived_RESEARCH_ONLY.nds':'lil_B111_B119_V3204_derived_RESEARCH_ONLY.nds',
        'all_routes_combined_v3144_candidate.nds':'all_routes_combined_v3204_candidate.nds',
        'lil_Shrines_Temples_relocation_v3193':'lil_B111_B119_relocation_v3239b',
        'lil_Shrines_Temples_font_approval_v3190b/all220_native_macro_font_reconciliation.json':'lil_B111_B119_font_approval_v3236/all150_native_macro_font_reconciliation.json',
        'verify_lil_shrines_fonts_v3183b':'verify_lil_B111_B119_fonts_v3234c',
        'verify_lil_shrines_FE_v3180':'verify_lil_B111_B119_FE_v3231',
        'lil_Shrines_Temples_fonts_v3183b':'lil_B111_B119_fonts_v3234c',
        'all164speech_56aliased_alternatives_15choice_labels_and114_relative_operands_preserved':'all116speech_34aliased_alternatives_no_choices_and64_relative_operands_preserved',
        'all570_relocated_native_skip_cases_match_original_target_mapping':'all320_relocated_native_skip_cases_match_original_target_mapping',
        'range(101,111)':'range(111,120)',
        "stored==compiled[1:] and compiled[0]==208 and row['virtual_D0_excluded_from_stored_body']":"stored==compiled[1:] and compiled[0] in [208,209,214,215,220] and row['actual_virtual_prefix_excluded_from_stored_body']",
        "value=b'\\xd0'+stored":"value=compiled[:1]+stored",
        'value[0] in [2,9,16,20,139,151,160,177,178,191,207,208,254]':'value[0] in [2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220,254]',
        'virtual_actor_style_D0_not_stored':'actual_virtual_actor_style_prefix_not_stored',
        'len(parity)==220 and macro_calls==880':'len(parity)==150 and macro_calls==600',
        'all326_other_SC2_blocks_every_other_file_and_native_component_exact':'all327_other_SC2_blocks_every_other_file_and_native_component_exact',
        'all220_final_targets_complete_native_planes_equal_reviewed_planes':'all150_final_targets_complete_native_planes_equal_reviewed_planes',
        'current_final_padded_macro_alignment_cases=880':'current_final_padded_macro_alignment_cases=600',
        'all56_virtual_D0_prefixes_excluded_from_physical_alternative_body':'all34_actual_virtual_prefixes_excluded_from_physical_alternative_body',
        'all30_FE_final_planes_and120_macro_alignments_bound':'all1_FE_final_plane_and4_macro_alignments_bound',
        'all190_progressive_final_planes_and760_macro_alignments_bound':'all149_progressive_final_planes_and596_macro_alignments_bound',
        'actual_selected_Shrines_Temples_IDs':'actual_selected_B111_B119_IDs',
        'V3144-derived ten-block':'V3204-derived nine-block',
        'Research image:ten selectedSC2blocks only;326otherblocks/allotherfiles/components exact.220final nativeplanes/880macro cases pass;not a release ornewparent.':'Research image:nine selectedSC2blocks only;327otherblocks/allotherfiles/components exact.150final nativeplanes/600macro cases pass;not a release ornewparent.'})
    generate('scripts/verify_lil_shrines_loader_v3195b.py','scripts/verify_lil_B111_B119_loader_v3241.py',{
        'prepare_lil_shrines_research_v3194':'prepare_lil_B111_B119_research_v3240b',
        'lil_Shrines_Temples_research_v3194':'lil_B111_B119_research_v3240b',
        'lil_Shrines_Temples_loader_v3195b':'lil_B111_B119_loader_v3241',
        'ten_selected':'nine_selected',
        'recruitment/Julian resizing':'B111-B119 resizing'})
    generate('scripts/verify_lil_shrines_references_v3196.py','scripts/verify_lil_B111_B119_references_v3242.py',{
        'prepare_lil_shrines_research_v3194':'prepare_lil_B111_B119_research_v3240b',
        'lil_Shrines_Temples_reference_census_v3196':'lil_B111_B119_reference_census_v3242',
        'lil_Shrines_Temples_loader_v3195b':'lil_B111_B119_loader_v3241',
        'ten_selected':'nine_selected',
        'range(101,111)':'range(111,120)',
        '==421':'==305','==114':'==64','==570':'==320',
        'all421_commands114_relative_sites_and_shipped_entry_census':'all305_commands64_relative_sites_and_shipped_entry_census',
        'all421_clean_current_target_commands_and114_relative_sites_reexecuted':'all305_clean_current_target_commands_and64_relative_sites_reexecuted',
        'all326_other_SC2_blocks_preserved':'all327_other_SC2_blocks_preserved',
        'native_commands_each=421,relative_sites=114,target_native_skip_cases=570':'native_commands_each=305,relative_sites=64,target_native_skip_cases=320',
        '268-command/68-span ten-block':'305-command/64-span nine-block'})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_reference_tools_provenance.json',dict(producers=pairs,no_previous_producer_modified=True,actual_variable_virtual_prefixes_bound=True,all_physical_copy_commands_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Nine-block final-plane,336whole-loader/two-mode and three-entry-census successors prepared.')
