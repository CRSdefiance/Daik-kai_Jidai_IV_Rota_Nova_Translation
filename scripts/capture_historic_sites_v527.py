"""Replay all original site fixtures against the registered full-name candidate."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

OUT = Path('work/analysis/historic_sites_v527')
OLD = Path('work/analysis/collection_gallery_v526')
ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v527_candidate.nds')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, default=528)
    args = parser.parse_args()
    version = args.version
    rom = Path(f'out/all_routes_combined_v{version}_candidate.nds')
    out = Path(f'work/analysis/historic_sites_v{version}')
    config_version = 2 if version >= 528 else 1
    config = json.loads(Path(f'translations/historic_site_names_v{config_version}.json').read_text(encoding='utf-8'))
    digest = sha(rom.read_bytes())
    font = GameAsciiFont.from_arm9(NdsImage.open(rom).read_file('/__arm9__.bin'))
    results = []
    for row in config['records']:
        index = row['site_id']
        fixture = json.loads((OLD / f'site_{index:02d}/save_fixture_manifest.json').read_text(encoding='utf-8'))
        fixture['production_ROM'], fixture['production_ROM_sha256'] = str(rom), digest
        target = out / f'site_{index:02d}'
        target.mkdir(parents=True, exist_ok=True)
        manifest = target / 'save_fixture_manifest.json'
        manifest.write_text(json.dumps(fixture, indent=2) + '\n', encoding='utf-8')
        run = ROOT / f'historic_site_{index:02d}_v{version}'
        if not (run / 'capture_report.json').exists():
            with (target / 'capture.log').open('w', encoding='utf-8') as log:
                subprocess.run([
                    sys.executable, 'scripts/headless_desmume_v193.py', '--rom', str(rom), '--out', str(run),
                    '--frames', '2800', '--capture-every', '2800', '--dump-ram', '--touchscreen',
                    '--allow-gallery-fixtures', '--battery-save', fixture['fixture_save'],
                    '--gallery-save-fixture-manifest', str(manifest),
                    '--inputs-json', str(OLD / 'ruins_inputs.json'),
                ], stdout=log, stderr=subprocess.STDOUT, check=True)
        fault = 'Undefined instruction' in (target / 'capture.log').read_text(encoding='utf-8')
        heading_verified = False
        if not fault:
            complete_mask(font, 'Historic Sites', Image.open(run / 'frame_002800_final.png').convert('RGB'),
                          86, 2, (230, 230, 230))
            heading_verified = True
        results.append({'site_id': index, 'English': row['english'], 'run': str(run),
                        'native_CPU_fault_observed': fault, 'display_credit': heading_verified,
                        'fixture_manifest': str(manifest), 'fixture_save_sha256': fixture['fixture_save_sha256']})
        (out / 'site_capture_outcomes.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
        print(f'Site {index:02d}: {"CPU fault; no display credit" if fault else "captured"}', flush=True)


if __name__ == '__main__':
    main()
