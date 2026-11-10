"""Create exact-hash native helpers for the isolated five-byte name-data successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Al_Ferid_context_tools_v6520')
OLD='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
if __name__=='__main__':
    assert not ROOT.exists();receipt=Path('work/analysis/Al_Ferid_name_research_v6518/research_image_receipt.json');r=read(receipt);assert r['source_ARM9_sha256']==OLD and len(r['changed_ARM9_byte_offsets'])==5;new=r['target_ARM9_sha256'];rows=[]
    for source,target in [('scripts/current_build_native_context_v6261b.py','scripts/Al_Ferid_exact_native_context_v6520.py'),('scripts/shady_man_font_oracles_v6263.py','scripts/Al_Ferid_font_oracles_v6520.py'),('scripts/lil_B207_name_style_v6354d.py','scripts/Al_Ferid_name_style_v6520.py')]:rows.append(derive(source,target,{OLD:new}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_target_helpers.json',dict(tools=rows,source_receipt=str(receipt),source_receipt_sha256=sha(receipt.read_bytes()),source_ARM9_sha256=OLD,exact_target_ARM9_sha256=new,only_exact_expected_hash_changes_no_weaker_runtime_snapshot_or_instruction_guards=True,current_target_own_boot_snapshot_still_required=True,all123264_payload_bytes_and_COMMON_directory_and_each_executed_instruction_checks_preserved=True,no_native_address_or_font_geometry_or_source_instruction_constant_change=True,full_goal_complete=False));print('Three isolated name-target helpers prepared with its exact measured ARM9 hash;all native guards/addresses preserved. Own target snapshot required.')
