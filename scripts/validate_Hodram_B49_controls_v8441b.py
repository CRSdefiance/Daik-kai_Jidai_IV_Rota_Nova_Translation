"""Run independent control checks against whole current input and freshly rebuilt B49 bytes."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_controls_v3 import check_controls
from dk4tool.patch.hodram_B49_reconstruction_v2 import reconstruct
from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices
from dk4tool.patch.hodram_B49_native_evidence_v1 import check_native_models
from scripts.validate_Hodram_B49_native_v8433 import PROOFS as native_paths,require
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_independent_controls_v8441b')
PROOFS={**native_paths,
 'relocation':'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json',
 'current':'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json',
 'source_controls':'work/analysis/Hodram_B49_source_controls_v8384/source_controls.json',
 'controls':'work/analysis/Hodram_B49_controls_v8401d/stored_controls.json',
}
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json');data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);reference=NdsImage.open(doc['reference_ROM']);clean=NdsImage.open('work/clean.nds')
    packet=data['current']['groups'][0];group=data['relocation']['groups'][0]
    old=IlnkContainer.parse(parent.read_file(doc['file_path'])).blocks[49];original=IlnkContainer.parse(clean.read_file(doc['file_path'])).blocks[49]
    target=reconstruct(old,original,group,packet,doc['records'],data['source_controls']['operands_requiring_adjustment_when_resizing'],doc['typed_choice_records'],compile_choices(doc['typed_choice_records']))
    rebuilt=dict(target_block=target);native=check_native_models(data,doc['records'],parent,read,require)
    result=check_controls(data,doc['records'],parent,reference,rebuilt,native,read,require);ROOT.mkdir(parents=True)
    save(ROOT/'independent_controls.json',dict(result=result,no_emulator_producer_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_controls_v3.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49 controls:14dispatches/nullFE/8branches40cases/1rawquery/4picture-hide/25normalends/2EV1getters/7pairedopaque decodes;no emulator replay orcredit.')
