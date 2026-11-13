"""Correct the verifier's field spelling; preserve the failed initial audit."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/verify_editorial_handoff_v4401.py','scripts/verify_editorial_handoff_v4401b.py',{
        'editorial_handoff_verification_v4401':'editorial_handoff_verification_v4401b',
        "r['decision']=='revise'":"r['editorial_decision']=='revise'",
    })
    print('Prepared corrected field binding;no checkpoint mutation or credit change.')
