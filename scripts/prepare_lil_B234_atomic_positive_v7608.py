"""Bind fresh production-support data and freeze the one-write positive reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.lil_B234_final_paths_v7602 import ITEM,NAMEPROOF,NAMES,SEAL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B234_atomic_support_tools_v7608')
if __name__=='__main__':
    assert not ROOT.exists();item,names,np,seal=map(read,[ITEM,NAMES,NAMEPROOF,SEAL]);r=item['actor104_regional_secondary_storage_contract']
    assert (r['pointer_field'],r['current_pointer'],r['current_deployed_payload_offset'],r['current_physical_ARM9_storage_offset'])==(1185924,37256672,960,1518924)
    assert (np['name_literal_alignment_count'],np['fresh_native_name_font_alignment_cases'],np['exact_reused_native_name_font_alignment_cases'])==(20,8,12)
    ROOT.mkdir(parents=True);module=Path('dk4tool/patch/lil_B234_atomic_support_v1.py')
    save(ROOT/'source_bound_role_alias_item_palette_andoffset_scope.json',dict(support_module=str(module),support_module_sha256=sha(module.read_bytes()),fresh_source_owned_guard_not_legacy_helper_weakening=True,regional_absolute_ARM9_1518924_anddeployed_relative960_independently_bound=True,item106_static_current1435852_not_payload_relative=True,exact_R5_original_CP932_palette_andone_scoped_R33_warning_bound=True,five_name_planes20_alignments8_fresh12_reused=True,source234_no_prerequisite_or_exclusion_andmeasured_late_scope_bound=True,evidence={str(p):sha(p.read_bytes()) for p in [ITEM,NAMES,NAMEPROOF,SEAL,Path(__file__)]},new_credit=0,full_goal_complete=False))
    changes={'B233':'B234','atomic_v7560':'atomic_v7608','final_paths_v7554':'final_paths_v7602','lil_B233_atomic_support_tools_v7559/source_locked_chisel_scope':'lil_B234_atomic_support_tools_v7608/source_bound_role_alias_item_palette_andoffset_scope','prepare_lil_B233_atomic_support_v7559':'prepare_lil_B234_atomic_positive_v7608','seal_lil_B233_references_v7556':'seal_lil_B234_references_v7604','lil_B233_atomic_tools_v7559':'lil_B234_atomic_tools_v7605','prepare_lil_B233_atomic_v7559':'prepare_lil_B234_atomic_v7605',"len(proof['changed_records'])==11":"len(proof['changed_records'])==18",'positive_records=11':'positive_records=18','source964_bytes_inverse_source_tail2_target_tail2_recovered':'source1468_bytes_inverse_source_tail0_target_tail0_recovered','all11_actual11_pages43_body43_headers_bound':'all18_actual18_pages71_body71_headers_bound','11 speeches/11 pages,complete964-byte':'18 speeches/18 pages,complete1468-byte'}
    derive('scripts/validate_lil_B233_atomic_v7560.py','scripts/validate_lil_B234_atomic_v7608.py',changes)
