"""Use the established historical key resolver; preserve the stopped checkpoint producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_checkpoint_tools_v7692b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/checkpoint_Maria_B207_native_v7692.py','scripts/checkpoint_Maria_B207_native_v7692b.py',{
        'v7692':'v7692b','V7692':'V7692b','v7693':'v7693b',
        'from scripts.complete_B210_Ferid_v6547 import parent_at':'from scripts.complete_B210_Ferid_v6547 import parent_at\nfrom scripts.reconcile_contextual_mood_retentions_v2482 import historical_key',
        "completed={(f['file_path'],r['id']) for f in ledger['completed_editorial_families'] for r in f['records']}":"completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};assert len(completed)==6837",
        "{(r['file_path'],r['id']) for r in prose['records']}":"{historical_key(r) for r in prose['records']}",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_historical_ledger_key_binding.json',dict(derivation=result,old_producer_preserved=True,no_history_orcredit_change=True,full_goal_complete=False))
