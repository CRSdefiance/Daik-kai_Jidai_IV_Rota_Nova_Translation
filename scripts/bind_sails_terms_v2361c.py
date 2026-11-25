"""Use the repository ILNK parse entry;preserve the pre-output failed producer."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/bind_sails_terms_v2361b.py')
if __name__=='__main__':
 source=OLD.read_text();assert source.count('IlnkContainer.from_bytes')==1;source=source.replace('IlnkContainer.from_bytes','IlnkContainer.parse').replace('sails_terms_v2361b','sails_terms_v2361c');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/sails_terms_v2361c/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),initial_failure_before_any_proof_or_ledger_mutation=True,reason='The ILNK API is parse,not from_bytes. This changes the local container-reader entry only; all source/native/HELP assertions remain intact.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
