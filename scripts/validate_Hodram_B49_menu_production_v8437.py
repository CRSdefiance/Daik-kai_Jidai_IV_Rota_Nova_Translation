"""Run independent B49 provider andactual owned caption/backing/highlight validation."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_menu_evidence_v1 import check_menu_actual
from scripts.validate_Hodram_B49_native_v8433 import require
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_independent_menu_v8437')
PROOFS={
 'menu_provider':'work/analysis/Hodram_B49_menu_v8400/menu_provider_and_planes.json',
 'menu_actual':'work/analysis/Hodram_B49_menu_actual_v8418/four_actual_menus12_full_owned_backing_andhighlight_samples.json',
 'tail_actual':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
}

if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json');data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');result=check_menu_actual(data,doc,parent,clean,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'independent_menu.json',dict(result=result,no_emulator_producer_orROM_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_menu_evidence_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49 menus:6originalproviders/18bridgedreturns plus12actual ownedbackings/24completevisiblelabels,bothhighlights/results match. Later identical sailing captions retained separately.No emulator replay orcredit.')
