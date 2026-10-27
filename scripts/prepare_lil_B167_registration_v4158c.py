"""Preserve the interrupted negative suite and create a successor with owned test folders."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B167_registration_recovery_v4158c');assert not root.exists()
    tool=derive('scripts/register_lil_B167_v4159.py','scripts/register_lil_B167_v4159b.py',{
        'lil_B167_registration_v4159':'lil_B167_registration_v4159b',
        "path=ROOT/kind/'actual_both_choices_conditional_panels_and_distinct_returns.json';save(path,value)":"path=ROOT/kind/'actual_both_choices_conditional_panels_and_distinct_returns.json';path.parent.mkdir(parents=True);save(path,value)"})
    root.mkdir(parents=True);save(root/'recovery.json',dict(tool=tool,preserved_interrupted_suite='work/analysis/lil_B167_registration_v4159',failure='Nested actual-proof mutation folder was not created; positive reconstruction and earlier negatives had passed,registry/builder/config were not mutated.',same_atomic_compiler_unchanged=True,new_negative_fixture_folder_only=True,producer_sha256=sha(Path(__file__).read_bytes())))
