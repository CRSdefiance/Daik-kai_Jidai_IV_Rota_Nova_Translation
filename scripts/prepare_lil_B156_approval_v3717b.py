"""Preserve the failed derivation and fix its unescaped prose apostrophe."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B156_approval_v3717.py');t=p.read_text(encoding='utf-8');old="question opening Why's he kept together;all reviewed words unchanged.";assert t.count(old)==1;t=t.replace(old,'question opening kept together;all reviewed words unchanged.');exec(compile(t,str(p)+'::unexecuted-output-quote-correction','exec'),dict(__name__='__main__',__file__=__file__));root=Path('work/analysis/lil_B156_approval_tools_v3717');save(root/'failed_derivation_literal_correction.json',dict(previous=str(p),previous_sha256=sha(p.read_bytes()),failure='Compile rejected the unescaped apostrophe in a generated review-note literal before target output or credit mutation.',correction='Use the same review note without the quoted contraction.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
