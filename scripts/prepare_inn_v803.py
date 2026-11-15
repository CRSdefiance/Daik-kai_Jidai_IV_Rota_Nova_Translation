"""Repack Inn23 and verify reviewed outputs through production ARM9 routing."""

from pathlib import Path

from PIL import Image

from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
DRAFT=Path('translations/inn_editorial_manuscript_v2.json')
PROTOTYPE=Path('work/analysis/inn_runtime_v802/layout')
DELTA=Path('work/analysis/inn_runtime_v802/layout_v2_delta')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open('out/all_routes_combined_v799_candidate.nds');rows=read(DRAFT)['records']
    common,arm,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),rows)
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(common);(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(arm)
    save(ROOT/'prospective_common_repack.json',dict(**proof,manuscript_sha256=sha(DRAFT.read_bytes())))
    print('Inn COMMON repacked blocks',proof['repacked_block_range'],flush=True)
    entries=local_entries(proof['directory_sha256'])(common,arm,clean=False)
    rows={r['message_id']:r for r in rows}
    source=(PROTOTYPE/'effective_format_case.py').read_text(encoding='utf-8')
    (ROOT/'effective_format_case.py').write_text(source,encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(ROOT/'effective_format_case.py'),'exec'),env)
    matrix=read(PROTOTYPE/'native_layout_matrix.json');preview=read(PROTOTYPE/'verification.json');delta=read(DELTA/'verification.json')
    assert matrix['count']==1169 and not matrix['findings']
    assert delta['manuscript_sha256']==sha(DRAFT.read_bytes())
    assert read(PROTOTYPE/'visual_review.json')['all95_complete_font_planes_visually_reviewed']
    assert read(DELTA/'visual_review.json')['all_three_duration_fonts_reviewed']
    old=[c for c in matrix['cases'] if c['id']!=1180]
    keys=tuple(matrix['cases'][0]);old.extend({k:c[k] for k in keys} for c in delta['changed_native_cases'])
    assert len(old)==1169 and {c['id'] for c in old}==set(owned.IDS)
    cases=[]
    for i,expected in enumerate(old):
        if i%64==0:cpu=prepared(arm)
        row=rows[expected['id']];assert entries[expected['id']].text==owned.compiled(row)
        result=env['format_case'](cpu,row,tuple(bytes.fromhex(v) for v in expected['source_values_hex']))
        assert result==expected,(expected,result)
        cases.append(result)
    fonts=[p for p in preview['full_font_planes'] if p['id']!=1180]+delta['changed_native_cases']
    assert len(fonts)==96
    kanji=rom.read_file('/GRP/KANJI.FNT')
    for p in fonts:
        path=Path(p['path']);assert sha(path.read_bytes())==p['sha256']
        pixels=raster(arm,bytes.fromhex(p['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(arm,kanji,p['lines'])
        with Image.open(path) as image:assert [bool(v) for v in pixels]==[v<128 for v in image.convert('L').get_flattened_data()]
    save(ROOT/'production_layout.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
        manuscript_sha256=sha(DRAFT.read_bytes()),native_layouts=len(cases),full_font_planes=len(fonts),
        findings=[],cases=cases,font_references=fonts,original_trampoline_and_exact_parent_dispatch_used=True,
        all_outputs_equal_reviewed_research=True,actual_revised_gameplay_pending=True,
        effective_program_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('1169 production layouts and96 complete fonts match reviewed research;COMMON3645 other texts and all opaque spans preserved.',flush=True)


if __name__=='__main__':main()
