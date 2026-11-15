"""Normalize Windows evidence keys without changing staged checkpoint content."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_checkpoint_tools_v4807b')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/verify_lil_B180_checkpoint_v4807.py','scripts/verify_lil_B180_checkpoint_v4807b.py',{
        "entry['evidence'][p]":"entry['evidence'][str(Path(p))]"})]
    tools.append(derive('scripts/verify_editorial_handoff_v4807.py','scripts/verify_editorial_handoff_v4807b.py',{
        'editorial_handoff_verification_v4807':'editorial_handoff_verification_v4807b',
        'from scripts.verify_lil_B180_checkpoint_v4807 import':'from scripts.verify_lil_B180_checkpoint_v4807b import'}))
    ROOT.mkdir(parents=True);save(ROOT/'windows_key_correction.json',dict(tools=tools,
        reason='Staged evidence keys are str(Path),which uses Windows separators; normalize the verifier lookup identically.',
        failed4807_and_all_staged_bytes_preserved=True,full_goal_complete=False))
