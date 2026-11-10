"""Add the exact completed native page adapter without repeating or changing the binary reconstruction."""
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'reconstruction_v2';assert not out.exists()
    original=ROOT/'reconstruction_v1/reconstruction.json';rebuilt=load(original)
    nativepath=Path(rebuilt['native']);native=load(nativepath);assert digest(nativepath)==rebuilt['native_sha256']
    calibrationpath=ROOT/'native_B116_fix_v1/compiled_native_pages.json';calibration=load(calibrationpath)
    assert calibration['runtime']==native['runtime'] and calibration['font_sha256']==native['font_sha256']
    adapter=calibration['source_owned_target_page_adapter'];assert adapter and 'source_owned_target_page_adapter' not in native
    selectionpath=ROOT/'native_final_selection_v2/resume_selection.json';selection=load(selectionpath);seen=set()
    for row in selection['reused_native_records']:
        proof=load(row['receipt']);assert digest(row['receipt'])==row['receipt_sha256']
        path=Path(proof['native_run_inputs']);assert digest(path)==proof['native_run_inputs_sha256']
        if str(path) in seen:continue
        seen.add(str(path));run=load(path)
        assert run['runtime']==native['runtime'] and run['font_sha256']==native['font_sha256']
        assert run['source_owned_target_page_adapter']==adapter and run['source_owned_progressive_macro_adapter']==native['source_owned_progressive_macro_adapter']
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256'] and digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    out.mkdir();complete=deepcopy(native);complete.update(source_owned_target_page_adapter=adapter,
        metadata_only_target_page_adapter_bridge=True,original_native_proof=str(nativepath),original_native_proof_sha256=digest(nativepath),
        adapter_origin=str(calibrationpath),adapter_origin_sha256=digest(calibrationpath),all_selected_native_run_adapters_exact=True)
    newnative=out/'native_pages.json';save(newnative,complete)
    result=deepcopy(rebuilt);result.update(native=str(newnative),native_sha256=digest(newnative),binary_reconstruction_proof=str(original),
        binary_reconstruction_proof_sha256=digest(original),metadata_only_native_adapter_completion=True,
        metadata_completion_evidence={str(p):digest(p) for p in [original,nativepath,calibrationpath,selectionpath,Path(__file__)]})
    assert all(result[k]==v for k,v in rebuilt.items() if k not in ['native','native_sha256'])
    save(out/'reconstruction.json',result)
    print('Completed exact native-adapter metadata; reconstructed ROM/archive/groups and every page unchanged; no rebuild repeated.')

if __name__=='__main__':main()
