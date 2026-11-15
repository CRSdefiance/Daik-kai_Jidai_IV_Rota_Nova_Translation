"""Correct audit timing count accidentally caught by the decision-count remap."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/verify_editorial_handoff_v4409.py','scripts/verify_editorial_handoff_v4409b.py',{
        'editorial_handoff_verification_v4409':'editorial_handoff_verification_v4409b',
        'dict(total=30,speech=19,control_or_end=6)':'dict(total=30,speech=24,control_or_end=6)',
    })
    print('Corrected timing24 separate from revision19;original failed audit retained;no ROM/prose/ledger change.')
