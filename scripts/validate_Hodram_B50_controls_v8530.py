"""Run independent control checks against whole current input and freshly rebuilt B50 bytes."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B50_controls_v1 import check_controls
from dk4tool.patch.hodram_B50_reconstruction_v1 import reconstruct
from dk4tool.patch.hodram_B50_native_evidence_v1 import check_native_models
from scripts.validate_Hodram_B50_native_v8520 import PROOFS as native_paths,require
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B50_independent_controls_v8530')
PROOFS={**native_paths,
 'relocation':'work/analysis/Hodram_B50_references_v8503/source_current_final_map.json',
 'current':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
 'source_controls':'work/analysis/Hodram_B50_source_controls_v8486/source_controls.json',
 'controls':'work/analysis/Hodram_B50_controls_v8497/stored_controls.json',
}
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B50_editorial_manuscript_v5.json');data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);reference=NdsImage.open(doc['reference_ROM']);clean=NdsImage.open('work/clean.nds')
    packet=data['current']['groups'][0];group=data['relocation']['groups'][0]
    old=IlnkContainer.parse(parent.read_file(doc['file_path'])).blocks[50];original=IlnkContainer.parse(clean.read_file(doc['file_path'])).blocks[50]
    target=reconstruct(old,original,group,packet,doc['records'],[])
    rebuilt=dict(target_block=target);native=check_native_models(data,doc['records'],parent,read,require)
    result=check_controls(data,doc['records'],parent,reference,rebuilt,native,read,require);ROOT.mkdir(parents=True)
    save(ROOT/'independent_controls.json',dict(result=result,no_emulator_producer_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B50_controls_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B50 controls:3dispatches/nullFE/no branch-query-menu/2picture-hide/25normalends/1EV1getter/6pairedopaque decodes;no emulator replay orcredit.')
