"""All supplied native name combinations and explicit legal editor boundaries."""

import argparse
import struct
from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_barmaid_dialogue_v779 import ROOT, CURRENT
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.review_barmaid_dialogue_v779 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save


def main(manuscript=MANUSCRIPT, out=ROOT/'layouts_v1'):
    manuscript, out = Path(manuscript), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    context, doc = read(ROOT/'native_context.json'), read(manuscript)
    assert read(ROOT/'captain_first_name_bound.json')['capacity'] == 16
    rom = NdsImage.open(CURRENT)
    arm, kanji = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    raw = Path(context['pre_fixture_snapshot']['path']).read_bytes()
    assert sha(raw) == context['pre_fixture_snapshot']['sha256']
    u = machine(arm)
    defaults = []
    for n in range(4):
        p = struct.unpack_from('<I', arm, 0x120B80+n*32)[0]
        value = bytes(u.mem_read(p, 32)).split(b'\0')[0]
        assert 0 < len(value) <= 16
        defaults.append(value)
    names = sorted(set(defaults + [bytes.fromhex(context['original_mutable_captain_first_name']['first_name_hex'])]
                       + [b'A'*n for n in range(1, 17)]
                       + ['ア'.encode('cp932')*n for n in range(1, 9)]
                       + [b'ABCDEFGH IJKLMNO', b'A BCDEFGHIJKLMNO', b'ABCDEFGHIJKLMN A',
                          b'Anna Maria', b'Jean-Luc', b'Joakim', b'Camille']))
    assert all(0 < len(s) <= 16 for s in names)
    cases, findings = [], []
    for row in doc['records']:
        n = row['message_id']
        observed = context['all84_original_city_and_name_provider_cases']
        barmaids = sorted({bytes.fromhex(r['arguments_hex'][0 if n == 989 else 1])
                           for r in observed if r['id'] == n}) if n in (989, 990) else []
        variants = product(barmaids, names) if n == 989 else product(names, barmaids) if n == 990 else ((name,) for name in names) if n == 999 else ((),)
        for i, args in enumerate(variants):
            if i % 64 == 0:
                u = machine(arm)
                u.mem_write(BASE, raw)
            result = format_case(u, row, args)
            result['supplied_editor_boundary_case'] = bool(args) and any(v not in defaults for v in (args[1],) if n == 989) if n == 989 else bool(args) and args[0] not in defaults if n in (990, 999) else False
            cases.append(result)
            if result['findings']:
                findings.append(result)
    save(out/'native_layout_matrix.json', {'cases': cases, 'count': len(cases), 'findings': findings,
                                          'manuscript_sha256': sha(manuscript.read_bytes()),
                                          'name_basis': 'Four real defaults and explicit1..16-byte/CP932/spaced/hyphenated editor-boundary cases;not every arbitrary possible user string.'})
    previews, seen = [], set()
    for case in cases:
        marker = (case['id'], tuple(len(line.encode('cp932')) % 2 for line in case['lines']),
                  any(not bytes.fromhex(v).isascii() for v in case['source_values_hex']))
        if marker in seen:
            continue
        seen.add(marker)
        plane = raster(arm, bytes.fromhex(case['formatted_hex']), 0x01FFCE40-BASE, size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, kanji, case['lines'])
        p = out/f'font_{len(previews):03d}_ID{case["id"]}.png'
        Image.frombytes('L', (228, 64), bytes(0 if v else 255 for v in plane)).save(p)
        previews.append({**case, 'path': str(p), 'sha256': sha(p.read_bytes()), 'complete_independent_font_plane_exact': True})
    sheets = []
    for start in range(0, len(previews), 12):
        sheet = Image.new('RGB', (1428, 720), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(previews[start:start+12]):
            x, y = i % 3 * 476, i // 3 * 180
            draw.text((x+5, y+4), f'RESEARCH ID{row["id"]} / {start+i}', fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x+5, y+24))
        p = out/f'fonts_{start//12:02d}_2x.png'
        sheet.save(p)
        sheets.append({'path': str(p), 'sha256': sha(p.read_bytes())})
    save(out/'verification.json', {'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
                                   'manuscript': str(manuscript), 'manuscript_sha256': sha(manuscript.read_bytes()),
                                   'defaults_hex': [s.hex() for s in defaults], 'supplied_captain_names_hex': [s.hex() for s in names],
                                   'native_layouts': len(cases), 'findings_count': len(findings),
                                   'complete_font_planes': previews, 'sheets': sheets,
                                   'context996_normal_reachability_open': True,
                                   'all_production_dispatch_integration_copy_patch_and_gameplay_gates_pending': True,
                                   'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(len(cases), 'native layouts;', len(findings), 'findings;', len(previews), 'full fonts. Production approval pending.', flush=True)
    for row in findings[:16]:
        print(row['id'], row['lines'], row['findings'], flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--manuscript', type=Path, default=MANUSCRIPT)
    p.add_argument('--out', type=Path, default=ROOT/'layouts_v1')
    a = p.parse_args()
    main(a.manuscript, a.out)
