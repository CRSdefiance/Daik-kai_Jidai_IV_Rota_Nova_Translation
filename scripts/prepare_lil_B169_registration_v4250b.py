"""Normalize checkpoint file keys before running the preserved registration successor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_registration_tools_v4250b')
if __name__ == '__main__':
    assert not ROOT.exists()
    prior = read('work/analysis/lil_B169_reference_checkpoint_v4247/checkpoint_receipt.json')['preserved_release_files']
    for key,digest in prior.items():
        assert sha(Path(key).read_bytes()) == digest,key
    assert not Path('translations/lil_B169_editorial_release_v1.json').exists()
    tool = derive('scripts/register_lil_B169_v4250.py','scripts/register_lil_B169_v4250b.py',{
        'lil_B169_registration_v4250':'lil_B169_registration_v4250b',
        'prior[str(rp)]':'prior[rp.as_posix()]','prior[str(builder)]':'prior[builder.as_posix()]',
        'v4250.tmp':'v4250b.tmp',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,
        preserved_failure='V4250 stopped before creating its audit root or release config:forward-slash checkpoint keys were indexed with Windows backslash Path strings.',
        all_checkpoint_release_files_verified_unchanged=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('B169 registration successor uses canonical forward-slash checkpoint keys;all preserved inputs unchanged.')
