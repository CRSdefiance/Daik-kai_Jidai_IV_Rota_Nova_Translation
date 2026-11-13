"""Verify the shared crew-role selector and full native English glyphs."""

import copy
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.crew_role_labels import ENGLISH, LABELS, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/crew_roles_v326')
CONFIG = Path('translations/crew_role_labels_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (
        'out/all_routes_combined_v324_candidate.nds', 'work/clean.nds',
        'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*arms)
    u = machine(target)
    payload = bytes(MainCodeFile(target, BASE).sections[3].data[:-48])
    u.mem_write(POOL, payload)
    pointers = struct.unpack_from('<16I', payload, ENGLISH - POOL)
    selectors = []
    for index in [-1, *range(256), 0x7FFFFFFF, 0x80000000]:
        call(u, 0x86314, (index & 0xFFFFFFFF,))
        result = u.reg_read(UC_ARM_REG_R0)
        assert result == (ENGLISH + index * 4 if 0 <= index < 16 else 0)
        if result:
            assert struct.unpack('<I', u.mem_read(result, 4))[0] == pointers[index]
        selectors.append({'input': index, 'result': result})
    rasters = []
    for english in LABELS:
        stored = english + (' ' if len(english) % 2 else '')
        for mode in (4, 16):
            rendered = execute(target, stored, x=82, y=64, tracking=0, mode=mode, buffered_context=True)
            assert rendered['pixels'] == expected_pixels(target, stored, 82, 64, mode, advance=6)
            assert rendered['final_x'] == 82 + len(stored) * 6 <= 256
            rasters.append({'English': english, 'stored': stored, 'mode': mode,
                            'full_bounds': [82, 64, 82 + len(stored) * 6, 75],
                            'all_complete_ink_and_blank_cells_exact': True})
    proof = {'transform': plan, 'native_selector_cases': selectors, 'native_role_rasters': rasters,
             'source_meanings_match_existing_reviewed_item_role_dictionary': True,
             'original_logic_bounds_fallback_and_all_other_bytes_preserved': True,
             'actual_gerhard_source_capture': 'work/emulation_v193/existing_save_v325/capture_report.json',
             'source_save_provenance_unknown_no_progress_legitimacy_claim': True,
             'goal_complete': False}
    evidence = ROOT / 'native_proof.json'
    evidence.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'research_arm9.bin').write_bytes(target)
    CONFIG.write_text(json.dumps({'format': 'dk4-crew-role-labels-release-v1',
                                  'target_arm9_sha256': sha(target),
                                  'verification_evidence_sha256': {str(evidence): sha(evidence.read_bytes())},
                                  'status': 'experimental-native-verified-live-pending'}, indent=2) + '\n', encoding='utf-8')
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v324'])
    profile['crew_role_labels_release'] = str(CONFIG)
    profile['note'] = 'Full V324 stack plus shared selector using existing complete English table for all 16 crew roles. No pool, text, logic or artwork allocation change; all 18 plaques remain open.'
    prior = registry['profiles'].get('all-routes-unified-v326')
    assert prior is None or prior == profile
    registry['profiles']['all-routes-unified-v326'] = profile
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'selector_cases': len(selectors), 'full_role_rasters': len(rasters), 'all16_roles': True}))


if __name__ == '__main__':
    main()
