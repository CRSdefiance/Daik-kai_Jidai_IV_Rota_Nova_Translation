"""Preserve failed preparer and explicitly relocate all source block-index literals."""
from scripts.prepare_lil_B156_layout_v3705 import derive
import runpy

if __name__=='__main__':
    derive('scripts/prepare_lil_B171_final_audit_v4358.py','scripts/prepare_lil_B171_final_audit_v4358b_impl.py',{
        'lil_B171_final_audit_tools_v4358':'lil_B171_final_audit_tools_v4358b',
        "NEW=Path('scripts/verify_editorial_handoff_v4358.py')":"NEW=Path('scripts/verify_editorial_handoff_v4358b.py')",
        "'editorial_handoff_verification_v4358'":"'editorial_handoff_verification_v4358b'",
        "'B170':'B171','lil_B170':'lil_B171',":"'B170':'B171','lil_B170':'lil_B171','[170]':'[171]',",
    })
    runpy.run_path('scripts/prepare_lil_B171_final_audit_v4358b_impl.py',run_name='__main__')
