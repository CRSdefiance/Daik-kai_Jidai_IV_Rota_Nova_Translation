"""Capture each original site in a separate, labeled copied-save fixture."""

import json
import subprocess
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

OUT = Path('work/analysis/collection_gallery_v526')
ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    rows = []
    review = json.loads((OUT / 'historic_site_name_review.json').read_text(encoding='utf-8'))
    for row in review['records']:
        index = row['site_id']
        fixture = OUT / f'site_{index:02d}'
        run = ROOT / f'collection_site_{index:02d}_v526'
        subprocess.run([sys.executable, 'scripts/prepare_collection_gallery_v526.py',
                        '--site-ids', str(index), '--skip-items', '--out', str(fixture)], check=True)
        if not (run / 'capture_report.json').exists():
            with (fixture / 'capture.log').open('w', encoding='utf-8') as log:
                subprocess.run([
                    sys.executable, 'scripts/headless_desmume_v193.py',
                    '--rom', review['current_candidate'], '--out', str(run),
                    '--frames', '2800', '--capture-every', '2800', '--dump-ram',
                    '--touchscreen', '--allow-gallery-fixtures',
                    '--battery-save', str(fixture / 'collection-gallery-test-only.dsv'),
                    '--gallery-save-fixture-manifest', str(fixture / 'save_fixture_manifest.json'),
                    '--inputs-json', str(OUT / 'ruins_inputs.json'),
                ], stdout=log, stderr=subprocess.STDOUT, check=True)
        report_path = run / 'capture_report.json'
        report = json.loads(report_path.read_text(encoding='utf-8'))
        log_text = (fixture / 'capture.log').read_text(encoding='utf-8')
        cpu_fault = 'Undefined instruction' in log_text
        assert report['cold_boot'] and not report['savestate_loaded']
        assert report['ROM_sha256'] == review['current_candidate_sha256']
        assert report['synthetic_gallery_fixtures'] and not report['earned_unlock_verified']
        assert not report['callback_errors'] and report['frames'] == 2800
        ram = (run / 'final_arm9_ram.bin').read_bytes()
        assert ram[row['pointer_field']:row['pointer_field'] + 4] == (0x02000000 + row['source_offset']).to_bytes(4, 'little')
        expected = bytes.fromhex(row['source_hex']) + b'\0'
        assert ram[row['source_offset']:row['source_offset'] + len(expected)] == expected
        image = run / 'frame_002800_final.png'
        rows.append({'site_id': index, 'Japanese': row['japanese'],
                     'reviewed_English_not_yet_applied': row['english'],
                     'image': str(image), 'image_sha256': sha(image.read_bytes()),
                     'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
                     'source_name_pointer_and_bytes_present_in_actual_RAM': True,
                     'native_CPU_fault_observed': cpu_fault,
                     'actual_site_display_credit': not cpu_fault,
                     'synthetic_single_site_fixture': True,
                     'natural_discovery_verified': False, 'complete_English_display_verified': False})
        (OUT / 'single_site_captures.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Site {index:02d}: {"CPU fault; no display credit" if cpu_fault else "native capture"}; original name RAM matches.', flush=True)


if __name__ == '__main__':
    main()
