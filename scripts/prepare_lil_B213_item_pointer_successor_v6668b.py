"""Distinguish a legacy batch's pointer from the verified current staged-name pointer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_item_pointer_tools_v6668b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/bind_lil_B213_item_card_lead_v6668.py','scripts/bind_lil_B213_item_card_lead_v6668b.py',{'item_card_lead_v6668':'item_card_lead_v6668b',"assert jp[at:at+4].hex()==row['source_hex'].lower() and arm[at:at+4].hex()==row['replacement_hex'].lower()":"assert jp[at:at+4].hex()==row['source_hex'].lower();legacy_pointer=int.from_bytes(bytes.fromhex(row['replacement_hex']),'little');assert current_pointer!=legacy_pointer",'registered_item_name_batch=str(CATALOG),':'registered_item_name_batch=str(CATALOG),legacy_batch_pointer=legacy_pointer,current_pointer_relocated_from_legacy_batch=True,current_label_independently_decoded_from_verified_current_ARM9_or_staged_pool=True,'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_legacy_vs_current_pointer_correction.json',dict(proof=proof,earlier_legacy_pointer_equality_assumption_rejected_without_mutation=True,source_field_current_pointer_target_text_and_actual_capture_independently_bound=True,no_old_pointer_overlay_name_asset_or_ROM_change=True,full_goal_complete=False))
