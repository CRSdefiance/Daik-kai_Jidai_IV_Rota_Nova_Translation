"""Independently validate captured B49 FE objects andevery held bitmap/palette/RGB pixel."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_B49_FE_evidence_v1 import check_FE_geometry
from scripts.validate_Hodram_B49_native_v8433 import PROOFS as native_paths,require
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_independent_FE_v8436')
PROOFS={**native_paths,
 'tail_fixtures':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
 'FE_geometry':'work/analysis/Hodram_B49_FE_binding_v8420/two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json',
}

if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json');data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);native=check_native_models(data,doc['records'],parent,read,require)
    result=check_FE_geometry(data,parent,native,read,require)
    assert result['original_FE_paint_snapshots_recomputed']==2 and result['complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed']==4 and result['focused_actual_frames_bound']==9862
    ROOT.mkdir(parents=True);save(ROOT/'independent_FE.json',dict(result=result,no_emulator_orproducer_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_FE_evidence_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49 FE:two exact originalpaint CPU/WRAM/TCM objects/four held bankD VRAM bitmaps/palettes/RGB reconstruct;9862focusedframes bound.No emulator replay orcredit.')
