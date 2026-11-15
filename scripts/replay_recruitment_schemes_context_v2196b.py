"""Successor: create new output folders required by the frozen context writers."""
from pathlib import Path
import sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
assert sys.argv[1] in ('recruitment','schemes')
original=Path('scripts/replay_recruitment_schemes_context_v2196.py')
source=original.read_text().replace('tavern_recruitment_context_v2196','tavern_recruitment_context_v2196b').replace('tavern_schemes_context_v2197','tavern_schemes_context_v2197b')
assert source.count('assert not root.exists()')==1
source=source.replace('assert not root.exists()','assert not root.exists()\nroot.mkdir(parents=True)')
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
save(env['root']/'output_folder_correction.json',dict(prior_wrapper=str(original),prior_wrapper_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),prior_runs_passed_native_assertions_but_failed_saving_to_absent_folders=True,no_ROM_or_context_contract_changes=True))
