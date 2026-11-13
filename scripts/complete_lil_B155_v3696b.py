"""Keep the historical59-object inventory entry whileadding the current50-object entry."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    source=Path('scripts/complete_lil_B155_v3696.py');t=source.read_text(encoding='utf-8');changes=[('Complete59 integrated reviews','Complete50 integrated reviews'),("inventory['lil_B152_B154_completed_v3654']","inventory['lil_B155_completed_v3696']")]
    for a,b in changes:assert a in t,a;t=t.replace(a,b)
    exec(compile(t,str(source)+'::preserve-historical59-inventory-entry','exec'),dict(__name__='__main__',__file__=__file__));save(Path('work/analysis/lil_B155_completion_v3696/unexecuted_draft_inventory_key_correction.json'),dict(previous_draft=str(source),previous_draft_sha256=sha(source.read_bytes()),executed_successor=__file__,executed_successor_sha256=sha(Path(__file__).read_bytes()),correction_before_any_completion_execution='Use a new B155 completion key andcorrect docstring;preserve historical B152-B15459-object inventory data. No review/prose/ROMchange.',all_predecessors_preserved=True,full_goal_complete=False))
