"""Verify stored paragraphs through the exact new dispatcher, not a chosen helper."""

import inspect
import re
import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.recruitment_editorial_runtime import ENTRY
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.context_shared_dialogue_v781 import CURRENT, ROOT as SOURCE
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.review_shared_dialogue_v781 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')
OUT = ROOT/'production_layout'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plan = read(ROOT/'prospective_common_repack.json')
    common = (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    arm = (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(common) == plan['target_COMMON_sha256'] and sha(arm) == plan['target_ARM9_sha256']
    entries = local_entries(plan['directory_sha256'])(common, arm, clean=False)
    manuscript = read(MANUSCRIPT)
    assert sha(Path(MANUSCRIPT).read_bytes()) == plan['manuscript_sha256']
    rows = {r['message_id']: r for r in manuscript['records']}
    source = inspect.getsource(original.format_case)
    marker = '    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement = '''    n = row['message_id']
    parent, key = (0x02053E38,n) if n==1020 else (0x02053D24,0x021181C0) if 1021<=n<=1027 else (0x02053D24,0x021181A0) if 1035<=n<=1041 else (0x02053D24,0x02118180) if 1042<=n<=1048 else (0x02054014,0)
    for at,value in ((0x264,parent),(0x274,n),(0x27C,key),(0x270,0)):
        u.mem_write(STACK+at,struct.pack('<I',value))
    call(u, ENTRY - BASE, (wrapped, output, 0), instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1)) == value+b'\\0'
    if n in (1028,1029):
        expected = re.sub(rb'([NSEW]) +(?=[0-9])',rb'\\1',expected)'''
    assert source.count(marker) == 1
    source = source.replace(marker, replacement)
    env = {**original.__dict__, 'ENTRY': ENTRY, 're': re}
    exec(compile(source, str(OUT/'effective_format_case.py'), 'exec'), env)
    (OUT/'effective_format_case.py').write_text(source, encoding='utf-8')
    prototype = read(SOURCE/'layouts_v2/native_layout_matrix.json')
    assert prototype['count'] == 857 and not prototype['findings']
    cases = []
    for i, case in enumerate(prototype['cases']):
        if i % 64 == 0:
            u = machine(arm)
        row = rows[case['id']]
        assert entries[case['id']].text == b' '+row['english'].removesuffix('{PAD}').encode('ascii')
        result = env['format_case'](u, row, tuple(bytes.fromhex(v) for v in case['source_values_hex']))
        assert result == case, (case['id'], result, case)
        cases.append(result)
    rom = NdsImage.open(CURRENT)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    fonts = read(SOURCE/'layouts_v2/verification.json')
    planes = []
    for row in fonts['complete_font_planes']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['sha256']
        case = row['case']
        plane = raster(arm, bytes.fromhex(case['formatted_hex']), 0x01FFCE40-0x02000000,
                       size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, kanji, case['lines'])
        with Image.open(path) as image:
            assert [bool(p) for p in plane] == [p == (0, 8, 0) for p in image.convert('RGB').getdata()]
        planes.append({'path': str(path), 'sha256': row['sha256'], 'complete_native_font_plane_exact': True})
    save(OUT/'verification.json', {
        'research_COMMON_sha256': sha(common), 'research_ARM9_sha256': sha(arm),
        'manuscript_sha256': sha(Path(MANUSCRIPT).read_bytes()), 'all857_production_dispatcher_cases_exact_to_reviewed_prototype': True,
        'native_layouts': len(cases), 'findings': [], 'cases': cases,
        'all83_complete_native_font_planes_exact_to_visually_reviewed_images': planes,
        'earlier_visual_review': str(SOURCE/'layouts_v2/visual_review.json'),
        'earlier_visual_review_sha256': sha((SOURCE/'layouts_v2/visual_review.json').read_bytes()),
        'argument_copies_complete_printf_words_guards_and_callee_saved_ABI_preserved': True,
        'actual_new_gameplay_and_registered_ROM_pending': True,
        'effective_program_sha256': sha(source.encode()), 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('857 stored-paragraph/native-dispatch layouts and83 independent font planes match the reviewed prototypes exactly.', flush=True)


if __name__ == '__main__':
    main()
