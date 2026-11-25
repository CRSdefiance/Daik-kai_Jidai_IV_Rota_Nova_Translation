"""Run32 original relative sites in both images with all4MiB and owner/stream guards."""
from pathlib import Path
if __name__=='__main__':
    DRAFT=Path('scripts/prove_lil_B157_branches_v3747.py');t=DRAFT.read_text(encoding='utf-8');assert 'lil_B157_branches_v3747' in t and 'lil_B157_source_v3746/all75_clean_current_complete_context' in t;t=t.replace('lil_B157_branches_v3747','lil_B161_B163_branches_v3916').replace('lil_B157_source_v3746/all75_clean_current_complete_context','lil_B161_B163_source_v3912/all45_clean_current_complete_context');exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=DRAFT))
