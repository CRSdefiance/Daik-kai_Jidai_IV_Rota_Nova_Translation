"""Prepare final source00 planes,complete menu andwhole-loader/reference proofs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B131_B133_reference_tools_v3330');assert not root.exists();pairs=[]
    def generate(old,new,changes):
        old,new=Path(old),Path(new);assert not new.exists();t=old.read_text(encoding='utf-8')
        for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
        return old,new,t
    old,new,t=generate('scripts/prepare_lil_B122_B127_research_v3289b.py','scripts/prepare_lil_B131_B133_research_v3330b.py',{
      'lil_B122_B127_research_v3289b':'lil_B131_B133_research_v3330b',
      'lil_B122_B127_V3251_derived_RESEARCH_ONLY.nds':'lil_B131_B133_V3300_derived_RESEARCH_ONLY.nds',
      'all_routes_combined_v3251_candidate.nds':'all_routes_combined_v3300_candidate.nds',
      'lil_B122_B127_relocation_v3288b':'lil_B131_B133_relocation_v3329b',
      'lil_B122_B127_native_approval_v3285/all159_native_macro_font_choice_reconciliation.json':'lil_B131_B133_native_approval_v3326/all63_native_macro_font_choice_and_source00_reconciliation.json',
      'verify_lil_B122_B127_fonts_v3283':'verify_lil_B131_B133_fonts_v3324b',
      'verify_lil_B122_B127_FE_v3284':'verify_lil_B131_B133_FE_v3325',
      'lil_B122_B127_fonts_v3283':'lil_B131_B133_fonts_v3324b',
      'all155speech_four_choice_labels_and64_relative_operands_preserved':'all61speech_two_choice_labels_and24_relative_operands_preserved',
      'all320_relocated_native_skip_cases_match_original_target_mapping':'all120_relocated_native_skip_cases_match_original_target_mapping',
      'range(122,128)':'[131,133]',
      'value[0] in [2,6,9,20,26,92,95,151,254]':'value[0] in [0,2,5,9,20,254]',
      'len(parity)==155 and macro_calls==620':'len(parity)==61 and macro_calls==244',
      'all330_other_SC2_blocks_every_other_file_and_native_component_exact':'all334_other_SC2_blocks_every_other_file_and_native_component_exact',
      'all155_final_targets_complete_native_planes_equal_reviewed_planes':'all61_final_targets_complete_native_planes_equal_reviewed_planes',
      'current_final_padded_macro_alignment_cases=620':'current_final_padded_macro_alignment_cases=244',
      'all155_complete_source_static_or_FE_prefixes_preserved':'all61_complete_source_static_or_FE_prefixes_preserved',
      'all10_FE_final_planes_and40_macro_alignments_bound':'all1_FE_final_plane_and4_macro_alignments_bound',
      'all145_progressive_final_planes_and580_macro_alignments_bound':'all60_progressive_final_planes_and240_macro_alignments_bound',
      'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs',
      'len(menus)==2 and len(pauses)==2':'len(menus)==1 and len(pauses)==0',
      'all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound':'all1_final2100_object_two_labels_and3_selection_cancel_cases_bound',
      'both_original_pause_resume_words_and20_decoder_cases_bound=True':'no_source2000_pause_commands=True,all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved=True',
      'V3251-derived six-block':'V3300-derived two-block'})
    a=t.index("        for c in block['original2000_pause_and_resume_maps']:");z=t.index('        container.blocks[n]=target',a);t=t[:a]+"        assert not block['original2000_pause_and_resume_maps']\n"+t[z:]
    t=t[:t.rindex('    print(')]+"    print('Research image:two selectedSC2blocks only;334otherblocks/allotherfiles/components exact.61final nativeplanes/244macro cases,one complete menu and18source00 targets pass;not a release ornewparent.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    for a,b,changes in [
      ('scripts/verify_lil_B122_B127_loader_v3290.py','scripts/verify_lil_B131_B133_loader_v3331.py',{'prepare_lil_B122_B127_research_v3289b':'prepare_lil_B131_B133_research_v3330b','lil_B122_B127_research_v3289b':'lil_B131_B133_research_v3330b','lil_B122_B127_loader_v3290':'lil_B131_B133_loader_v3331','six_selected':'two_selected','B122-B127':'B131/B133'}),
      ('scripts/verify_lil_B122_B127_references_v3291.py','scripts/verify_lil_B131_B133_references_v3332.py',{'prepare_lil_B122_B127_research_v3289b':'prepare_lil_B131_B133_research_v3330b','lil_B122_B127_reference_census_v3291':'lil_B131_B133_reference_census_v3332','lil_B122_B127_loader_v3290':'lil_B131_B133_loader_v3331','six_selected':'two_selected','range(122,128)':'[131,133]','==312':'==112','==64':'==24','==320':'==120','all312_':'all112_','64_relative_sites':'24_relative_sites','all334_':'all334_','all330_other_SC2_blocks_preserved':'all334_other_SC2_blocks_preserved','native_commands_each=312,relative_sites=64,target_native_skip_cases=320':'native_commands_each=112,relative_sites=24,target_native_skip_cases=120','312-command/64-span six-block':'112-command/24-span two-block'})]:
        if 'all334_' in changes:changes.pop('all334_')
        old,new,t=generate(a,b,changes);compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    root.mkdir(parents=True);save(root/'source00_reference_successors.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],no_previous_producer_orROM_modified=True,preserve_all_generated_ROMs_and_earlier_translations=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
