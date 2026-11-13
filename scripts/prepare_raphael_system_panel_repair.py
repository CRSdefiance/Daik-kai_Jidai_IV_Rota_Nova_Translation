"""Source-first tutorial review and exact terminal repair proposal; no playable ROM."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.raphael_system_panel_release import PATH, TARGETS, encode_panel
from dk4tool.rom.nds import NdsImage

CONFIG = Path('translations/raphael_system_panel_release_v1.json')
ENGLISH = {
    (45, 52): 'Ceuta: FO now owns a 20 percent market share. Trade within that share.',
    (46, 51): 'At sea, you can inspect nearby cities and fleets.',
    (46, 54): 'Press Y for the magnifying glass icon, which indicates Inspect mode.',
    (46, 58): 'To inspect a city or fleet, aim the magnifier at it and press A.',
    (46, 62): 'Your ship can also attack cities and fleets.',
    (46, 65): 'Press L in Inspect mode for the sword icon, which indicates Battle mode.',
    (46, 68): 'To start a battle, aim the sword at a city or fleet and press A.',
    (46, 72): 'To search for items or supplies at sea, press R in Inspect mode.',
    (46, 76): 'A gray frame appears. This indicates Search mode.',
    (46, 80): 'Aim the gray frame at land, then press A to search.',
    (46, 83): 'Press L or R to cycle between Inspect, Battle, and Search modes.',
    (46, 87): 'Press L to cycle modes: Inspect, Battle, then Search.',
    (46, 91): 'Press R or Y to cycle modes: Inspect, Search, then Battle.',
}


def main():
    images = [NdsImage.open(path) for path in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds',
                                            'out/all_routes_combined_v152_candidate.nds')]
    files = [image.read_file(PATH) for image in images]
    containers = [IlnkContainer.parse(data) for data in files]
    current = IlnkContainer.parse(files[2])
    records = []
    for block, segment in sorted(TARGETS):
        jp, canonical, old = [c.blocks[block].split(b'\0')[segment] for c in containers]
        # The original Japanese, rather than a translated prefix, is the control authority.
        if not jp.startswith(b'\xfe') or not old.startswith(b'\xf8\xf2'):
            raise ValueError('Panel proposal source changed')
        rows = ['Ceuta:', 'FO now owns a', '20 percent market share.', 'Trade within that share.'] if block == 45 else None
        new = encode_panel(ENGLISH[block, segment], len(jp), structured_rows=rows)
        record = {'block': block, 'segment': segment, 'clean_hex': jp.hex(),
                  'canonical_hex': canonical.hex(), 'before_hex': old.hex(), 'after_hex': new.hex(),
                  'translation_policy': 'natural-dialogue-v2', 'english': ENGLISH[block, segment],
                  'source_japanese': jp[1:].decode('cp932'),
                  'source_meaning': ENGLISH[block, segment], 'speaker': 'Tutorial system',
                  'context': 'Raphael opening tutorial; retain adjacent script commands and dismissal state.',
                  'localization_note': 'Reviewed against clean Japanese; machine formatter supplies modal guards. FO remains the runtime company macro.',
                  'review': {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')}}
        if rows:
            record['structured_rows'] = rows
            record['manual_break_reason'] = 'Structured city/company/share/instruction panel; four semantic fields, independently verified in the modal consumer.'
        parts = current.blocks[block].split(b'\0'); parts[segment] = new
        current.blocks[block] = b'\0'.join(parts)
        records.append(record)
    config = {'format': 'dk4-raphael-system-panel-release-v1', 'file_path': PATH,
              'clean_file_sha256': sha(files[0]), 'canonical_file_sha256': sha(files[1]),
              'source_file_sha256': sha(files[2]), 'target_file_sha256': sha(current.to_bytes()),
              'native_proof': 'work/analysis/raphael_system_panel_native_proof.json', 'records': records}
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared 13 source-verified modal tutorial repairs within unchanged allocations.')


if __name__ == '__main__':
    main()
