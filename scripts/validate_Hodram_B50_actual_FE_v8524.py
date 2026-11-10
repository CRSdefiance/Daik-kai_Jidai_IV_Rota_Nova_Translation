"""Independently bind complete fixture traces and FE captures using one native recomputation."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B50_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_B50_actual_evidence_v1 import check_actual
from dk4tool.patch.hodram_B50_FE_evidence_v1 import check_FE_geometry
from scripts.validate_Hodram_B50_native_v8520 import PROOFS as native_paths,require
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_independent_actual_FE_v8524')
DOC=Path('translations/hodram_B50_editorial_manuscript_v5.json')
MAP=Path('work/analysis/Hodram_B50_references_v8503/source_current_final_map.json')
PROOFS={**native_paths,
 'fixtures':'work/analysis/Hodram_B50_fixtures_v8504/two_whole_scripts.json',
 'actual':'work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json',
 'FE_geometry':'work/analysis/Hodram_B50_FE_binding_v8508/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
}
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');mapping=read(MAP)
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==mapping['candidate_sha256']
    rebuilt=dict(target_archive=Path(mapping['target_archive']).read_bytes());assert sha(rebuilt['target_archive'])==mapping['target_archive_sha256']
    native=check_native_models(data,doc['records'],parent,read,require)
    actual=check_actual(data,doc['records'],parent,clean,rebuilt,native,read,require)
    print('Independent complete B50 fixtures/traces/body/name/FE-header masks pass.',flush=True)
    FE=check_FE_geometry(data,parent,native,read,require)
    assert actual['summary']['complete_actual_page_occurrences']==6 and actual['summary']['complete_actual_holds']==50 and actual['summary']['unique_speech_IDs']==3
    assert FE['original_FE_paint_snapshots_recomputed']==2 and FE['complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed']==6 and FE['actual_frames_bound']==20002
    modules=[Path('dk4tool/patch')/f'hodram_B50_{stem}_v1.py' for stem in ['native_guards','native_evidence','actual_evidence','FE_evidence']]
    ROOT.mkdir(parents=True);save(ROOT/'independent_actual_FE.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_summary=native['summary'],actual_summary=actual['summary'],FE_summary=FE,one_native_recomputation_shared_across_actual_andFE_checks=True,no_emulator_orproducer_replay=True,comparison_controls_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),DOC,MAP,*modules,*map(Path,PROOFS.values())]}))
    print('Independent B50:two wholefixtureROMs reconstruct/invert;6pageoccurrences/50completeholds/3speeches/normalreturns,twoFEpaint CPUobjects/sixheldVRAMpaletteRGB pass.No emulator replay orcredit.')
