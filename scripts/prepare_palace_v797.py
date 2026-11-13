"""Repack full Palace prose and test the original production trampoline."""

import inspect
import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch import palace_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
DRAFT=Path('translations/palace_editorial_manuscript_v2.json')
PROTOTYPE=Path('work/analysis/palace_editorial_v795/prototype_layout')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open('out/all_routes_combined_v792_candidate.nds')
    rows=read(DRAFT)['records']
    common,arm,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),rows)
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(common)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(arm)
    save(ROOT/'prospective_common_repack.json',{**proof,'manuscript_sha256':sha(DRAFT.read_bytes())})
    print('Repacked blocks',proof['repacked_block_range'],flush=True)
    rows={r['message_id']:r for r in rows}
    entries=local_entries(proof['directory_sha256'])(common,arm,clean=False)
    source=inspect.getsource(original.format_case)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    parent = 0x02053FCC if row['message_id']==1166 else 0x02054014
    for at, value in ((0x264,parent),(0x274,row['message_id']),(0x27C,0),(0x270,0)):
        u.mem_write(STACK+at,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1))==value+b'\\0' '''
    assert source.count(marker)==1
    source=source.replace(marker,replacement)
    (ROOT/'effective_format_case.py').write_text(source,encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(ROOT/'effective_format_case.py'),'exec'),env)
    prototype=read(PROTOTYPE/'native_layout_matrix.json');prior=read(PROTOTYPE/'verification.json')
    assert prototype['count']==323 and not prototype['findings'] and len(prior['complete_font_planes'])==40
    assert prior['manuscript_sha256']==sha(DRAFT.read_bytes())
    cases=[]
    for i,case in enumerate(prototype['cases']):
        if i%64==0:cpu=prepared(arm)
        row=rows[case['id']];assert entries[case['id']].text==owned.compiled(row)
        result=env['format_case'](cpu,row,tuple(bytes.fromhex(v) for v in case['source_values_hex']))
        assert result==case,(case,result)
        cases.append(result)
    kanji=rom.read_file('/GRP/KANJI.FNT')
    for p in prior['complete_font_planes']:
        path=Path(p['path']);assert sha(path.read_bytes())==p['sha256']
        pixels=raster(arm,bytes.fromhex(p['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(arm,kanji,p['lines'])
        with Image.open(path) as image:assert [bool(p) for p in pixels]==[p<128 for p in image.convert('L').getdata()]
    visual=read(PROTOTYPE/'visual_review.json');assert visual['all40_complete_font_planes_visually_reviewed']
    save(ROOT/'production_layout.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'manuscript_sha256':sha(DRAFT.read_bytes()),'native_layouts':len(cases),'full_font_planes':40,
        'findings':[],'cases':cases,'original_trampoline_and_exact_parent_dispatch_used':True,
        'all_outputs_equal_reviewed_prototypes':True,'source_context':read('work/analysis/palace_editorial_v795/native_context.json')['producer_sha256'],
        'actual_gameplay_pending':True,'effective_program_sha256':sha(source.encode()),
        'producer_sha256':sha(Path('scripts/prepare_palace_v797.py').read_bytes()),'full_goal_complete':False})
    print('323 production trampoline layouts and40 complete fonts match reviewed prototypes.',flush=True)


if __name__=='__main__':main()
