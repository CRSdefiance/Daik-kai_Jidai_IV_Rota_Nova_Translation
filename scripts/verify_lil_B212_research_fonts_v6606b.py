"""Verify all9 compiled native bodies, one original page each and72 current input alignments."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B212_editorial_manuscript_v2.json')
PLAN=Path('work/analysis/lil_B212_layout_v6605b/nine_whole_paragraph_research_plans.json')
INPUT=Path('work/analysis/current_V6584_native_v6593/current_native_input.json')
ROOT=Path('work/analysis/lil_B212_research_fonts_v6606b')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=read(DOC),read(PLAN);assert sha(DOC.read_bytes())==plan['manuscript_sha256'] and len(plan['records'])==9 and not plan['failures']
    byid={r['id']:r for r in doc['records']};image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    adapter=inspect.getsource(expand)
    env=dict(expand.__globals__);exec(compile(adapter,__file__+'::original-D0-fallback-no-assignment','exec'),env)
    page_adapter=checked_text(inspect.getsource(old_pages),{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'});page_env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(page_adapter,__file__+'::AA5-native-pages','exec'),page_env);pages=page_env['pages']
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');cases=[];pictures=[];alignments=0
    for record in plan['records']:
        row=byid[record['id']];body=bytes.fromhex(record['encoded_hex'])[1:];logical=row['english'].split('}',1)[1].encode('ascii');prefix=row['source_selector'];pipelines=[]
        assert body and body[-1]!=10 and all(body.count(m)==logical.count(m)==0 for m in [b'FI',b'FA',b'FO'])
        for label,text in [('logical',logical),('compiled-protected',body)]:
            result=ctx.execute(env['expand'],text,prefix);ctx.machines.pop();pipelines.append(dict(version=label,**result));alignments+=4
            assert all(c['output_hex']==text.hex() for c in result['cases'])
        rendered=pages(arm,font,body);expected_pages=1
        assert len(rendered['pages'])==expected_pages
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(record['id']+f'_page{page["page"]}.bin');plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels))
            assert page['first_visible_origin']==([0,0] if page['page']==1 else [6,0])
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);path=plane.with_suffix('.png');picture.save(path);page.update(preview=str(path),preview_sha256=sha(path.read_bytes()));pictures.append((record['id'],page['page'],picture))
        cases.append(dict(id=record['id'],source_kind=row['kind'],source_selector=prefix,compiled_hex=record['encoded_hex'],formatted_markup=record['formatted_markup'],logical_and_compiled_current_native_pipelines=pipelines,**rendered))
    assert len(cases)==9 and len(pictures)==9 and alignments==72 and not ctx.machines
    sheets=[]
    for start in range(0,len(pictures),6):
        subset=pictures[start:start+6];sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(ident,page,picture) in enumerate(subset):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),ident+' native page'+str(page),fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        p=ROOT/f'all9_complete_pages_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all9_bodies9_complete_native_pages_and72_alignments_RESEARCH.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=cases,complete_native_pages=9,logical_compiled_input_alignment_cases=72,all9_objects_one_original_four_row_native_page=True,no_B209_page_footer_or_typed_style_exception_inherited=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,each216x64_plane_exact_independent_current_font_and_all_canaries=True,continuation_first_row_retains_original6px_guard_indent=True,all_original_current_font_renderer_instructions_verified=True,all_source_macros_zero_no_new_substitutions=True,no_actor_role_roster_RNG_or_event_assignment=True,only_original_static_selector149_no_dynamic_role=True,source_owned_expand_adapter=adapter,source_owned_AA5_page_adapter=page_adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),review_sheets=sheets,visual_review_pending=True,only_offline_complete_native_pages_not_actual_button_progression=True,native_name_planes_actual_style_header_masks_reference_and_release_pending=True,all14_formatting_gates_remain_false=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,INPUT,Path(pages.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print('All9 bodies/9 complete current native pages/72 alignments pass. Two sheets await viewing;actual source/English,names and release remain pending.')
