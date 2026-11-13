"""Preserve failed audit and correct its remaining predecessor block literal."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/verify_editorial_handoff_v4358b.py','scripts/verify_editorial_handoff_v4358c.py',{
        'editorial_handoff_verification_v4358b':'editorial_handoff_verification_v4358c',
        "assert row['block']==170":"assert row['block']==171",
        "dict(checkpoint='V4357'":"dict(checkpoint='V4357',preserved_failed_preparer='scripts/prepare_lil_B171_final_audit_v4358.py',preserved_failed_predecessor_audit='scripts/verify_editorial_handoff_v4358b.py',predecessor_block_literal_corrected_without_ROM_prose_or_ledger_change=True",
    })
