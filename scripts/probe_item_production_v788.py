"""Stored prose through the original trampoline and scoped new dispatcher."""

import inspect
import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.context_item_diplomacy_v784 import CURRENT, TABLES
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_item_common_v788 import ROOT
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.review_item_diplomacy_v784 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

OUT = ROOT/'production_layout'
PROTOTYPE = Path('work/analysis/item_diplomacy_context_v786/provider_layouts')


def native_parent(n):
    for table, values in TABLES.items():
        if n in values:
            return (0x02053D24 if table in (0x02117F60, 0x021180C0, 0x021180A0) else 0x02053DB8), table
    return (0x02053FCC if n in (1073, 1086) else 0x02054014), n


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plan = read(ROOT/'prospective_common_repack.json')
    arm = (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    common = (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    rows = {r['message_id']: r for r in read(MANUSCRIPT)['records']}
    assert sha(MANUSCRIPT.read_bytes()) == plan['manuscript_sha256']
    entries = local_entries(plan['directory_sha256'])(common, arm, clean=False)
    consumers = read(ROOT/'consumer_routing.json')
    assert consumers['research_ARM9_sha256'] == sha(arm)
    source = inspect.getsource(original.format_case)
    marker = '    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement = '''    parent, key = native_parent(row['message_id'])
    for at, value in ((0x264,parent), (0x274,row['message_id']), (0x27C,key), (0x270,0)):
        u.mem_write(STACK+at, struct.pack('<I',value))
    call(u, 0x01FFCF3C - BASE, (wrapped, output, 0), instruction_limit=2000000)
    for p, value in zip(pointers, values):
        assert bytes(u.mem_read(p, len(value)+1)) == value+b'\\0' '''
    assert source.count(marker) == 1
    source = source.replace(marker, replacement)
    (OUT/'effective_format_case.py').write_text(source, encoding='utf-8')
    env = {**original.__dict__, 'native_parent': native_parent}
    exec(compile(source, str(OUT/'effective_format_case.py'), 'exec'), env)
    prototype = read(PROTOTYPE/'native_layout_matrix.json')
    prior = read(PROTOTYPE/'verification.json')
    assert prototype['count'] == 2774 and not prototype['findings']
    assert prior['manuscript_sha256'] == plan['manuscript_sha256'] and prior['complete_native_layouts'] == 2774
    cases = []
    for i, case in enumerate(prototype['cases']):
        if i % 64 == 0: cpu = machine(arm)
        row = rows[case['id']]
        assert entries[case['id']].text == b' '+row['english'].removesuffix('{PAD}').encode('ascii')
        result = env['format_case'](cpu, row, tuple(bytes.fromhex(v) for v in case['source_values_hex']))
        assert result == case, (case['id'], result, case)
        cases.append(result)
    kanji = NdsImage.open(CURRENT).read_file('/GRP/KANJI.FNT')
    planes = []
    for row in prior['complete_font_planes']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['sha256']
        plane = raster(arm, bytes.fromhex(row['formatted_hex']), 0x01FFCE40-0x02000000,
                       size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, kanji, row['lines'])
        with Image.open(path) as image:
            assert [bool(p) for p in plane] == [p < 128 for p in image.convert('L').getdata()]
        planes.append({'ID': row['id'], 'path': str(path), 'sha256': row['sha256'],
                       'complete_native_font_plane_exact': True})
    assert len(planes) == 76
    visual = PROTOTYPE/'visual_review.json'
    assert visual.exists()
    save(OUT/'verification.json', {
        'research_COMMON_sha256': sha(common), 'research_ARM9_sha256': sha(arm),
        'manuscript_sha256': plan['manuscript_sha256'], 'native_original_call_target': 0x01FFCF3C,
        'all2774_stored_paragraph_original_trampoline_and_dispatcher_outputs_exact_to_reviewed_prototypes': True,
        'native_layouts': len(cases), 'findings': [], 'cases': cases,
        'all76_complete_native_font_planes_exact_to_visually_reviewed_images': planes,
        'earlier_visual_review': str(visual), 'earlier_visual_review_sha256': sha(visual.read_bytes()),
        'argument_copies_complete_words_guards_and_callee_saved_ABI_preserved': True,
        'synthetic_boundary_values_do_not_prove_all_faction_pairs_or_prices_eligible': True,
        'registered_ROM_actual_revised_scenes_and_full_branch_eligibility_pending': True,
        'effective_program_sha256': sha(source.encode()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('2774 stored-paragraph layouts through original entry and dispatcher plus 76 complete native font planes match reviewed prototypes.', flush=True)


if __name__ == '__main__':
    main()
