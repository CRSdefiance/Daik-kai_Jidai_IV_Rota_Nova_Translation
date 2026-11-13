"""Compare Windows evidence paths as paths; preserve the pre-mutation failed producer."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/complete_livestock_prayer_context_v2330.py')
if __name__=='__main__':
 source=OLD.read_text();old="scope['current_shared_consumer_control']==str(CONTROL)";assert source.count(old)==1
 source=source.replace(old,"Path(scope['current_shared_consumer_control'])==CONTROL").replace('v2330','v2330b').replace('V2330','V2330b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/livestock_prayer_completion_v2330b/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),initial_failure_before_any_ledger_document_or_evidence_mutation=True,reason='The same Windows path used forward slashes in the scope record and backslashes in str(Path). Compare Path values instead; all evidence and validation assertions are preserved.',producer_sha256=sha(Path(__file__).read_bytes()),effective_source_sha256=sha(source.encode()),full_goal_complete=False))
