"""Preserve the precommit failure and explicitly validate pending-to-sealed census metadata."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B46_sealed_guard_v7961')
OLD=Path('dk4tool/patch/rafael_B46_editorial_v1.py')
NEW=Path('dk4tool/patch/rafael_B46_editorial_v2.py')
CONFIG=Path('translations/rafael_B46_editorial_release_v2.json')
POSITIVE=Path('scripts/validate_Rafael_B46_atomic_positive_v7961.py')
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [NEW,CONFIG,POSITIVE])
    first=derive(str(OLD),str(NEW),{
        "CONFIG='translations/rafael_B46_editorial_release_v1.json'":"CONFIG='translations/rafael_B46_editorial_release_v2.json'",
        "require(all(group.get(k)==v for k,v in original.items()),'exact independently reconstructed relocation')":
            "require(original['external_references_complete'] is False and group['external_references_complete'] is True,'pending relocation promoted only after complete census seal')\n    require(all(group.get(k)==v for k,v in original.items() if k!='external_references_complete'),'exact independently reconstructed relocation')",
    })
    second=derive('scripts/validate_Rafael_B46_atomic_positive_v7960.py',str(POSITIVE),{
        'rafael_B46_editorial_v1':'rafael_B46_editorial_v2',
        'Rafael_B46_atomic_positive_v7960':'Rafael_B46_atomic_positive_v7961',
    })
    conf=read('translations/rafael_B46_editorial_release_v1.json')
    conf['dependencies'].update({str(p):sha(p.read_bytes()) for p in [NEW,Path(__file__)]})
    conf.update(prior_config='translations/rafael_B46_editorial_release_v1.json',
        prior_config_sha256=sha(Path('translations/rafael_B46_editorial_release_v1.json').read_bytes()))
    save(CONFIG,conf);ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_successors.json',dict(production=first,positive=second,config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        failure='V7960 rejected exact independently reconstructed relocation before commit because original pending external_references_complete=False became sealed True.',
        correction='Require this exact False-to-True approval transition and equality of every other original relocation field.',
        no_prior_file_orROM_overwritten=True,new_credit=0,full_goal_complete=False))
    print('Preserved V7960 failure;V7961 explicitly checks original pending-to-sealed census flag andevery other relocation field unchanged.')
