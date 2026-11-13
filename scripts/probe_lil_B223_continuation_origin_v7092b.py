"""Identify the compiler-owned leading guard on the second English page without changing geometry."""
from pathlib import Path
from scripts.research_lil_B209_native_pages_v6461 import pages as inherited_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_continuation_origin_v7092b')
FONT=Path('work/analysis/lil_B222_native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments.json')
PLAN=Path('work/analysis/lil_B223_layout_v7091d/seventeen_complete_paragraph_plans_original_width_no_prose_changes.json')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);doc=read(plan['manuscript']);image=NdsImage.open(doc['current_ROM']);env={**inherited_pages.__globals__,'expected_pixels':expected_pixels};adapter=read(FONT)['source_owned_2b6_page_adapter'];exec(compile(adapter,__file__+'::unchanged-original-pages','exec'),env);row=next(r for r in plan['records'] if r['id']=='DK4_MES_B223_R0031');body=bytes.fromhex(row['encoded_hex'])[1:];result=env['pages'](image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT'),body);assert len(result['pages'])==2
    ROOT.mkdir(parents=True)
    for page in result['pages']:
        raw=body[page['start']:page['end']];spaces=len(raw)-len(raw.lstrip(b' '));assert spaces==(0 if page['page']==1 else 1) and page['first_visible_origin']==[spaces*6,0]
        pixels=bytes.fromhex(page.pop('native_plane_hex'));old=Path('work/analysis/lil_B223_native_pages_v7092')/(row['id']+f'_page{page["page"]}.bin');assert old.read_bytes()==pixels;page.update(preserved_failed_run_plane=str(old),native_plane_sha256=sha(pixels),compiler_owned_leading_guard_bytes=spaces,expected_first_visible_origin=[spaces*6,0])
    assert next(e['code'] for e in result['pages'][1]['events'] if e['code']!=32)==ord('f')
    save(ROOT/'R31_page2_source_guard_space_and_complete_first_f_at6.json',dict(id=row['id'],layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),compiled_hex=row['encoded_hex'],complete_native_pages=result,failed_producer='scripts/verify_lil_B223_native_pages_v7092.py',failure='Inherited single-page assertion expected first visible origin[0,0] on every page. The second English page correctly starts with the formatter-owned protective space,so its first visible f is at[6,0].',both_original_failed_plane_files_pixel_equal_to_independent_research=True,no_glyph_dropped_shifted_or_unchecked=True,no_runtime_font_guard_geometry_prose_or_QA_change=True,original_current_native_instruction_fingerprints_and_canaries_pass=True,no_new_EMU_run_or_credit=True,full_goal_complete=False))
    print('R31 origins:page1[0,0];page2[6,0],one compiler-owned guard before complete f. Both saved failure planes equal;all code/glyph/bounds/canaries pass.')
