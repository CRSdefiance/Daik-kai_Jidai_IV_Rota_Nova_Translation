"""Audit every FE system notice in all routes through the real modal glyph pipeline."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.raphael_system_panel_release import (
    PATH,
    apply_release,
    reject_corrupt_panel_selectors,
)
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def main():
    rom = NdsImage.open('out/all_routes_combined_v152_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    files = {f'/data/SC{i}.DK4': rom.read_file(f'/data/SC{i}.DK4') for i in range(4)}
    files[PATH], _ = apply_release(files[PATH], canonical.read_file(PATH), clean.read_file(PATH),
                                  'translations/raphael_system_panel_release_v1.json', require_proof=False)
    reject_corrupt_panel_selectors(files)
    cases, failures, excluded = [], [], []
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        for block, data in enumerate(IlnkContainer.parse(files[path]).blocks):
            for segment, raw in enumerate(data.split(b'\0')):
                if not raw.startswith(b'\xfe'):
                    continue
                identifier = f'SC{route}_B{block}_R{segment}'
                if raw == b'\xfe':
                    original = IlnkContainer.parse(clean.read_file(path)).blocks[block].split(b'\0')[segment]
                    if original != raw:
                        raise ValueError('Empty system state replaces original text')
                    excluded.append({'id': identifier, 'hex': raw.hex(), 'reason': 'Source-identical empty system state; no text removed.'})
                    continue
                if (route, block, segment) == (2, 328, 13):
                    original = IlnkContainer.parse(clean.read_file(path)).blocks[block].split(b'\0')[segment]
                    if raw != original or raw != b'\xfe\x0f\xb1':
                        raise ValueError('Excluded nontext event payload changed')
                    excluded.append({'id': identifier, 'hex': raw.hex(), 'reason': 'Source-identical nontext event-control payload; no printable text.'})
                    continue
                body = raw[1:].rstrip(b' ').replace(b'FI', ('Raphael', 'Hodram', 'Lil', 'Maria')[route].encode('ascii')).replace(b'FO', b'Castor Co.')
                text = body.decode('cp932')
                try:
                    native = execute(source, text, modal=True, modal_guarded=True,
                                     audit_modal_legacy_guards=True, mode=16,
                                     kanji_font=font if not body.isascii() else None)
                    events = [e for e in native['glyph_events'] if e['code'] != 32]
                    expected = [int.from_bytes(c.encode('cp932'), 'big') for c in text if c not in (' ', '\n')]
                    actual = [e['code'] for e in events]
                    if actual != expected:
                        raise ValueError('Leading/interior/final glyph order differs')
                    if any(e['x'] < 0 or e['y'] < 0 or e['x'] + (12 if e['kind'] == 'cp932' else 6) > 256
                           or e['y'] + 12 > 96 for e in events):
                        raise ValueError('Glyph escapes modal bounds')
                    if native['pixels'] != expected_pixels(source, font, native['glyph_events'], 16, background=9):
                        raise ValueError('Independently decoded full pixels differ')
                    cases.append({'id': identifier, 'text': text, 'pixels_sha256': sha(native['pixels']),
                                  'row_origins': sorted({e['y'] for e in events}),
                                  'complete_glyph_order_and_pixels': True})
                except (ValueError, UnicodeError) as error:
                    failures.append({'id': identifier, 'text': text, 'error': str(error)})
                if (len(cases) + len(failures)) % 100 == 0:
                    print(f'{len(cases)} panels passed; {len(failures)} failures', flush=True)
    result = {'source_arm9_sha256': sha(source), 'cases': cases, 'failures': failures, 'excluded': excluded,
              'source_files_sha256': {path: sha(data) for path, data in files.items()},
              'all_readable_system_notices_pass': not failures,
              'all_four_routes_audited': True, 'corrupt_F8F2_selectors_remaining': 0,
              'limitations': 'Default protagonist/company macro expansion and initialized mode-zero modal bitmap are explicit contracts. Actual ASCII/CP932 glyph requests and font pixels execute. Physical frame composition, customized names and dismissal require runtime testing.'}
    output = Path('work/analysis/all_route_system_panel_native_audit.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native system panels passed; {len(failures)} failures; {len(excluded)} nontext exclusions.')
    if failures:
        print(json.dumps(failures, ensure_ascii=True, indent=2))
        raise SystemExit(1)
    config_path = Path('translations/raphael_system_panel_release_v1.json')
    config = json.loads(config_path.read_text(encoding='utf-8'))
    config.update({'all_route_native_audit': str(output), 'all_route_native_audit_sha256': sha(output.read_bytes())})
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
