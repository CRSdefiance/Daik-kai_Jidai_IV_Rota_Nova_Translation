"""Use the original scope-key spelling when applying simultaneous substitutions."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B167_completion_v4164.py');text=p.read_text(encoding='utf-8')
    old="'remaining_B168_B180_physical_speeches=348,remaining_choice_command_leads=1':"
    new="'remaining_B167_B180_physical_speeches=348,remaining_choice_command_leads=1':"
    assert text.count(old)==1
    exec(compile(text.replace(old,new),str(p)+'::source-key-repaired','exec'),dict(globals()))
    save(Path('work/analysis/lil_B167_completion_tools_v4164/derivation_recovery.json'),dict(original_failure='Source-key precondition used the post-substitution B168 spelling; original B167 key is now matched before the simultaneous replacement.',original_producer=str(p),original_producer_sha256=sha(p.read_bytes()),resume_producer_sha256=sha(Path(__file__).read_bytes()),no_ledger_or_document_credit_applied=True))
