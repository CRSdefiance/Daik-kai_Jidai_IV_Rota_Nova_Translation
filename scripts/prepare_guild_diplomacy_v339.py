"""Prepare complete native Guild diplomacy captions without new storage."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.guild_diplomacy_labels import SPECS, transform
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/guild_diplomacy_v339')
CONFIG = Path('translations/guild_diplomacy_labels_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in
            ('out/all_routes_combined_v338_candidate.nds', 'work/clean.nds',
             'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*arms)
    rasters = []
    for _, _, _, japanese, english in SPECS:
        for mode in (4, 16):
            reference = english + (' ' if mode == 4 and len(english) % 2 else '')
            r = execute(target, english, x=84, y=24, tracking=0, mode=mode, buffered_context=True)
            assert r['pixels'] == expected_pixels(target, reference, 84, 24, mode, advance=6)
            assert r['final_x'] == 84 + len(english) * 6 <= 232
            rasters.append({'Japanese': japanese, 'English': english, 'mode': mode,
                            'complete_first_internal_final_glyphs_and_blank_cells': True,
                            'paired_four_bit_terminal_empty_cell_in_reference': len(reference) != len(english)})
    proof = {'transform': plan, 'complete_native_rasters': rasters,
             'supplied_font_geometry_not_actual_menu_parent': True,
             'source_meaning': {'Goodwill': 'Friendly diplomatic exchange; no invented gift expenditure.',
                                'Send Documents': 'Dispatch negotiation documents from the Guild.'},
             'actual_visible_Source_command': 'work/emulation_v193/regional_maps_v339/frame_007200_navigation.png',
             'actual_menu_playback_pending': True}
    (ROOT / 'research_arm9.bin').write_bytes(target)
    evidence = ROOT / 'native_proof.json'
    evidence.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    CONFIG.write_text(json.dumps({'format': 'dk4-guild-diplomacy-labels-release-v1',
                                 'target_arm9_sha256': sha(target),
                                 'verification_evidence_sha256': {str(evidence): sha(evidence.read_bytes())},
                                 'status': 'experimental-native-verified-live-pending'}, indent=2) + '\n', encoding='utf-8')
    p = Path('translations/release_stack.json')
    registry = json.loads(p.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v338'])
    profile['guild_diplomacy_labels_release'] = str(CONFIG)
    profile['note'] = 'Complete V338 plus five source-exact Guild diplomacy captions in existing string slots. All inherited artwork, code, pools and pointers preserved; all 18 plaques remain open.'
    registry['profiles']['all-routes-unified-v339'] = profile
    p.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'complete_native_rasters': len(rasters), 'source_locked_commands': len(SPECS)}))


if __name__ == '__main__':
    main()
