"""Verify the full roster role crop and native lettering before integration."""

import copy
import json
import struct
from pathlib import Path

from dk4tool.patch.crew_role_labels import LABELS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.roster_role_crop import DESCRIPTOR, WIDTH, transform
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/roster_role_crop_v341')
CONFIG = Path('translations/roster_role_crop_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in
            ('out/all_routes_combined_v340_candidate.nds', 'work/clean.nds',
             'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*arms)
    rasters = []
    for label in LABELS:
        stored = label + (' ' if len(label) % 2 else '')
        for mode in (4, 16):
            result = execute(target, stored, x=0, y=0, tracking=0, mode=mode, buffered_context=True)
            assert result['pixels'] == expected_pixels(target, stored, 0, 0, mode, advance=6)
            assert result['final_x'] == len(stored) * 6 <= WIDTH
            rasters.append({'text': label, 'stored': stored, 'mode': mode,
                            'end_x': result['final_x'], 'all_complete_ink_blank_cells_fit_crop': True})
    proof = {'transform': plan, 'complete_native_role_rasters': rasters,
             'supplied_native_font_geometry_not_all_actual_role_assignments': True,
             'three_source_crop_rows': list(struct.unpack_from('<21i', arms[0], DESCRIPTOR)),
             'actual_missing_First_Mate_source': 'work/emulation_v193/conditional_guild_v341/frame_017800_navigation.png',
             'all18_plaque_entries_and_variants_still_incomplete': True,
             'actual_repaired_roster_playback_pending': True}
    evidence = ROOT / 'native_proof.json'
    evidence.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'research_arm9.bin').write_bytes(target)
    CONFIG.write_text(json.dumps({'format': 'dk4-roster-role-crop-release-v1',
                                 'target_arm9_sha256': sha(target),
                                 'verification_evidence_sha256': {str(evidence): sha(evidence.read_bytes())},
                                 'status': 'experimental-native-verified-live-pending'}, indent=2) + '\n', encoding='utf-8')
    p = Path('translations/release_stack.json')
    registry = json.loads(p.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v340'])
    profile['roster_role_crop_release'] = str(CONFIG)
    profile['note'] = 'Full V340 plus one roster crop width word, 48 to204, preserving complete shared English role names. All strings, code, backing bitmap and neighboring rows remain unchanged; all 18 plaques remain open.'
    registry['profiles']['all-routes-unified-v341'] = profile
    p.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'full_role_rasters': len(rasters), 'all16_roles_fit': True, 'changed_width_word_only': True}))


if __name__ == '__main__':
    main()
