"""Bind current registered/staged PXL loading evidence to the complete corpus."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

OUT = Path('work/analysis/resource_registry_v509')
ROM = Path('out/all_routes_combined_v508_candidate.nds')


def main():
    current = NdsImage.open(ROM)
    arm = current.read_file('/__arm9__.bin')
    cached = json.loads((OUT/'cache_load_proof.json').read_text(encoding='utf-8'))
    staged_path = Path('work/analysis/image_registry_v385/dynamic_loader_proof.json')
    staged = json.loads(staged_path.read_text(encoding='utf-8'))
    previous = NdsImage.open(staged['candidate'])
    old_arm = previous.read_file('/__arm9__.bin')
    ranges = [(0x28B74,0x28BAC),(0xB7158,0xB7294),(0xD3D30,0xD42AC)]
    assert all(arm[lo:hi] == old_arm[lo:hi]for lo,hi in ranges)
    cache_paths = {r['path']for r in cached['all356_registered_file_loads']}
    stage_paths = set()
    for row in staged['dynamic_event_and_town_files']:
        assert sha(current.read_file(row['path'])) == row['whole_PXL_sha256']
        stage_paths.add(row['path'])
    all_pxl = {p for _,p,_ in current.iter_files()if p.lower().endswith('.pxl')}
    covered = cache_paths|stage_paths
    remaining = sorted(all_pxl-covered)
    assert len(all_pxl) == 660 and len(cache_paths) == 356 and len(stage_paths) == 300
    assert len(covered) == 656
    assert remaining == ['/_pxl/copyright.pxl','/_pxl/logo.pxl','/_pxl/ship_eurL.pxl','/_pxl/startmenu0.pxl']
    proof = {'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
             'current_registered_cache_loads':356,'inherited_staged_loads_bound_to_current_bytes':300,
             'distinct_PXL_files_with_native_file_loading_evidence':656,'total_PXL_files':660,
             'remaining_original_loading_consumers':remaining,
             'cache_proof_sha256':sha((OUT/'cache_load_proof.json').read_bytes()),
             'inherited_staging_proof':str(staged_path),'inherited_staging_proof_sha256':sha(staged_path.read_bytes()),
             'current_staging_code_ranges_exact':ranges,
             'loading_coverage_not_native_scene_crop_alpha_or_gameplay_completion':True,
             'raw_legacy_archives_and_FLS_are_separate_requirements':True,
             'production_ROM_modified':False,'full_goal_complete':False}
    (OUT/'coverage_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Current PXL loading coverage:656/660;four original consumer paths still unresolved.')


if __name__ == '__main__':
    main()
