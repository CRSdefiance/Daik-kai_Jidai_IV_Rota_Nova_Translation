"""Correct the approval field name inherited by the first independent audit."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/verify_editorial_handoff_v4442.py','scripts/verify_editorial_handoff_v4442b.py',{
        'editorial_handoff_verification_v4442':'editorial_handoff_verification_v4442b',
        'all27_source_native_reference_and_representative_rules_approved':'all11_source_native_reference_and_representative_rules_approved',
    })
    print('Corrected inherited approval field;failed initial audit retained;no ledger,ROM or prose change.')
