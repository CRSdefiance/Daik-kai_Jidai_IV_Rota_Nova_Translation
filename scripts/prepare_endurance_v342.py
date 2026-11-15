"""Native complete approximate-day captions and shared-pool safety checks."""

import copy
import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.endurance_approximation import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_common_itcm_arena_reservation import initialize, verify
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/plaque_review_v342')
CONFIG = Path('translations/endurance_approximation_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    roms = [NdsImage.open(p) for p in ('out/all_routes_combined_v341_candidate.nds', 'work/clean.nds',
                                      'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*[r.read_file('/__arm9__.bin') for r in roms])
    rows = []
    for value in [0, 1, 9, 10, 99, 100, 999, 65535, 0x7FFFFFFF, -0x80000000]:
        text = f'~{value} days'
        for mode in (4, 16):
            reference = text + (' ' if mode == 4 and len(text) % 2 else '')
            result = execute(target, text, x=90, y=48, tracking=0, mode=mode, buffered_context=True)
            assert result['pixels'] == expected_pixels(target, reference, 90, 48, mode, advance=6)
            assert result['final_x'] == 90 + len(text) * 6 <= 240
            rows.append({'value': value, 'text': text, 'mode': mode,
                         'tilde_all_letters_digits_and_blank_cells_complete': True})
    payload = bytes(MainCodeFile(target, BASE).sections[3].data[:-48])
    b = boot(target, bytes(roms[0].rom.arm7), roms[0].rom.arm7RamAddress, True, payload)
    assert not b['arm7_source_changed_bytes_after_arm9_autoload']
    assert all(x['matches_original'] for x in b['arm7_native_loaded_sections'])
    assert all(b[k] for k in ['repaired_pool_matches_complete_payload', 'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'])
    assert b['late_copy_cache_model']['worst_case_dirty_data_and_stale_instruction_model_visible']
    assert all(b['SDK_staged_code_cache_line_coverage'][k] for k in ['all_instruction_lines_selected', 'all_data_lines_selected'])
    arena = initialize(target)
    assert arena['low'][0] == POOL + len(payload)
    bounds = verify(target, 0x01FFA000)
    proof = {'transform': plan, 'native_rasters': rows, 'supplied_caption_geometry_not_actual_parent': True,
             'boot': b, 'arena': arena, 'bounds': bounds, 'actual_caption_playback_pending': True}
    evidence = ROOT / 'native_proof.json'
    evidence.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'research_arm9.bin').write_bytes(target)
    CONFIG.write_text(json.dumps({'format': 'dk4-endurance-approximation-release-v1',
                                 'target_arm9_sha256': sha(target),
                                 'verification_evidence_sha256': {str(evidence): sha(evidence.read_bytes())},
                                 'status': 'experimental-native-verified-live-pending'}, indent=2) + '\n', encoding='utf-8')
    p = Path('translations/release_stack.json')
    registry = json.loads(p.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v341'])
    profile['endurance_approximation_release'] = str(CONFIG)
    profile['note'] = 'Full V341 plus source-faithful ~ marker in the Endurance duration caption; original calculation and numeric argument preserved. All 18 plaques remain in audit.'
    registry['profiles']['all-routes-unified-v342'] = profile
    p.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'complete_native_rasters': len(rows), 'source_approximation_restored': True, 'startup_cache_ARM7_arena_pass': True}))


if __name__ == '__main__':
    main()
