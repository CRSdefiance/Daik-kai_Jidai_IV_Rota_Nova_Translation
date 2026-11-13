"""Prospective layouts using original printf and existing native format helpers.

The coordinate route is supplied explicitly in this CPU probe. Production routing,
caller eligibility and actual game scenes are separate requirements.
"""

import inspect
import re
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.context_shared_dialogue_v781 import ROOT, CURRENT
from scripts.review_shared_dialogue_v781 import MANUSCRIPT
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

OUT = ROOT/'layouts_v2'


def formatter():
    source = inspect.getsource(original.format_case)
    marker = '    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement = '''    selected_helper = 0x02147A78 if row['message_id'] in (1028,1029) else LITERAL
    call(u, selected_helper - BASE, (wrapped, output, 0), instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1)) == value+b'\\0'
    if row['message_id'] in (1028,1029):
        expected = re.sub(rb'([NSEW]) +(?=[0-9])',rb'\\1',expected)'''
    assert source.count(marker) == 1
    source = source.replace(marker, replacement)
    env = dict(original.__dict__)
    env['re'] = re
    exec(compile(source, str(Path(__file__)), 'exec'), env)
    return env['format_case'], source


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    context, doc = read(ROOT/'native_context.json'), read(MANUSCRIPT)
    rom = NdsImage.open(CURRENT)
    arm, kanji = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    towns = sorted({bytes.fromhex(r['name_hex']) for r in context['all114_native_town_names']})
    coordinates = sorted({bytes.fromhex(r['arguments_hex'][0]) for r in context['all24_village_coordinate_providers_two_modes']})
    amounts = {bytes.fromhex(r['native_hex']) for r in context['native_headcount_strings']}
    # Explicit decimal-width tests; these are not earned crew counts.
    amounts |= {str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９')).encode('cp932')
                for n in (0, 2, 500, 999999, 2147483647)}
    run, source = formatter()
    (OUT/'effective_format_case.py').write_text(source, encoding='utf-8')
    cases, findings = [], []
    for row in doc['records']:
        n = row['message_id']
        variants = coordinates if n in (1028, 1029) else towns if 1030 <= n <= 1034 else sorted(amounts) if 1035 <= n <= 1048 else None
        values = [(v,) for v in variants] if variants is not None else [()]
        for i, args in enumerate(values):
            if i % 64 == 0:
                u = machine(arm)
            result = run(u, row, args)
            cases.append(result)
            if result['findings']:
                findings.append(result)
    save(OUT/'native_layout_matrix.json', {'cases': cases, 'count': len(cases), 'findings': findings,
                                          'manuscript_sha256': sha(Path(MANUSCRIPT).read_bytes()),
                                          'prospective_coordinate_helper_only_not_production_dispatch': True})
    print(len(cases), 'native layouts;', len(findings), 'findings.', flush=True)
    previews, seen = [], set()
    for case in cases:
        marker = (case['id'], len(case['lines']), tuple(len(line.encode('cp932')) % 2 for line in case['lines']))
        if marker in seen:
            continue
        seen.add(marker)
        plane = raster(arm, bytes.fromhex(case['formatted_hex']), 0x01FFCE40-0x02000000,
                       size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, kanji, case['lines'])
        image = Image.new('RGB', (228, 64), '#eee2bd')
        pixels = image.load()
        for i, v in enumerate(plane):
            if v:
                pixels[i % 228, i // 228] = (0, 8, 0)
        path = OUT/f'font_{len(previews):03d}_ID{case["id"]}.png'
        image.save(path)
        previews.append({'path': str(path), 'sha256': sha(path.read_bytes()), 'case': case})
    sheets = []
    for start in range(0, len(previews), 10):
        group = previews[start:start+10]
        sheet = Image.new('RGB', (1020, 146*len(group)+30), '#27343b')
        d = ImageDraw.Draw(sheet)
        for i, row in enumerate(group):
            y = 15+i*146
            d.text((12, y), f'ID {row["case"]["id"]} | lines {len(row["case"]["lines"])} | {row["case"]["findings"]}', fill='white')
            d.text((502, y+35), '\n'.join(row['case']['lines']), fill='#e1e9ed', spacing=8)
            with Image.open(row['path']) as image:
                sheet.paste(image.resize((456, 128), Image.Resampling.NEAREST), (12, y+16))
        path = OUT/f'sheet_{start//10:02d}.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(OUT/'verification.json', {
        'candidate_sha256': sha(CURRENT.read_bytes()), 'manuscript_sha256': sha(Path(MANUSCRIPT).read_bytes()),
        'native_layouts': len(cases), 'findings': findings, 'complete_font_planes': previews, 'sheets': sheets,
        'raw_argument_copies_unchanged': True, 'production_routing_and_gameplay_pending': True,
        'effective_program_sha256': sha(source.encode()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    print(len(previews), 'complete independent font planes;', len(sheets), 'review sheets.', flush=True)


if __name__ == '__main__':
    main()
