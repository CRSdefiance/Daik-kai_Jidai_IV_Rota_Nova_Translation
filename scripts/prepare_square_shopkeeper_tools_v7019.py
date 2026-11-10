"""Prepare a cold boot and exact-hash helpers for the owned Shopkeeper data target."""
from pathlib import Path
from dk4tool.patch.square_shopkeeper_label_data_v1 import SOURCE
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_tools_v7019')
RECEIPT=Path('work/analysis/square_shopkeeper_data_v7018/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();r=read(RECEIPT);assert r['source_ARM9_sha256']==SOURCE
    assert r['data_plan']['complete_ARM9_inverse'] and len(r['data_plan']['literal_slots'])==2
    target=r['target_ARM9_sha256'];assert target!=SOURCE
    rows=[derive('scripts/run_Al_Ferid_name_v6519.py','scripts/run_square_shopkeeper_v7019.py',{
        'Al_Ferid_name_run_v6519':'square_shopkeeper_run_v7019','Al_Ferid_name_v6519':'square_shopkeeper_v7019',
        'Al_Ferid_name_research_v6518':'square_shopkeeper_data_v7018','lil_B209_runs_v6491':'lil_B221_runs_v7014'})]
    for source,destination in [
        ('scripts/Al_Ferid_exact_native_context_v6520.py','scripts/square_shopkeeper_exact_native_context_v7020.py'),
        ('scripts/Al_Ferid_font_oracles_v6520.py','scripts/square_shopkeeper_font_oracles_v7020.py'),
        ('scripts/Al_Ferid_name_style_v6520.py','scripts/square_shopkeeper_name_style_v7020.py')]:
        rows.append(derive(source,destination,{SOURCE:target}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_target_helpers_and_boot.json',dict(tools=rows,receipt=str(RECEIPT),receipt_sha256=sha(RECEIPT.read_bytes()),
        source_ARM9_sha256=SOURCE,target_ARM9_sha256=target,only_exact_helper_hash_guard_changes=True,
        all_native_addresses_numeric_constants_geometry_COMMON_directory123264_payload_and_executed_instruction_guards_preserved=True,
        target_own_cold_boot_snapshot_required=True,no_historical_RAM_overlay_or_weakening=True,new_review_credit=0,full_goal_complete=False))
    print('Shopkeeper target cold-boot runner and three exact-hash native helpers prepared;own target snapshot required.',flush=True)
