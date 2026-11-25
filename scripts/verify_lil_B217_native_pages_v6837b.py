"""Check every complete page and both five-byte FA substitutions against current native code."""
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
DOC=Path('translations/lil_B217_editorial_manuscript_v1.json');PLAN=Path('work/analysis/lil_B217_layout_v6836b/four_whole_paragraph_plans_no_macros_no_prose_changes.json');INPUT=Path('work/analysis/current_V6821_native_v6830/current_native_input.json');ROOT=Path('work/analysis/lil_B217_native_pages_v6837')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=read(DOC),read(PLAN);assert sha(DOC.read_bytes())==plan['manuscript_sha256'] and len(plan['records'])==4 and not plan['failures'];byid={r['id']:r for r in doc['records']};image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT');adapter=inspect.getsource(expand);env=dict(expand.__globals__);exec(compile(adapter,__file__+'::original-expand','exec'),env);page_adapter=checked_text(inspect.getsource(old_pages),{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'});page_env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(page_adapter,__file__+'::AA5-original-pages','exec'),page_env);pages=page_env['pages'];ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');cases=[];pictures=[];alignments=0
    for record in plan['records']:
        row=byid[record['id']];body=bytes.fromhex(record['encoded_hex'])[1:];logical=row['english'].split('}',1)[1].replace('{MACRO:FA}','FA').encode('ascii');prefix=row['source_selector'];pipelines=[];assert prefix in [2,92] and body and body[-1]!=10 and body.count(b'FA')==logical.count(b'FA')==bytes.fromhex(row['source_hex'])[1:].count(b'FA')
        for label,text in [('logical',logical),('compiled-protected',body)]:
            result=ctx.execute(env['expand'],text,prefix);ctx.machines.pop();pipelines.append(dict(version=label,**result));alignments+=4;assert all(c['output_hex']==text.replace(b'FA',b'Argot').hex() for c in result['cases'])
        rendered=pages(arm,font,body.replace(b'FA',b'Argot'));assert len(rendered['pages'])==record['expected_native_pages']==1
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(record['id']+f'_page{page["page"]}.bin');plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels));assert page['first_visible_origin']==[0,0];picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);path=plane.with_suffix('.png');picture.save(path);page.update(preview=str(path),preview_sha256=sha(path.read_bytes()));pictures.append((record['id'],page['page'],picture))
        cases.append(dict(id=record['id'],source_kind=row['kind'],source_selector=prefix,compiled_hex=record['encoded_hex'],formatted_markup=record['formatted_markup'],logical_and_compiled_current_native_pipelines=pipelines,**rendered));save(ROOT/(record['id']+'_individual_native_proof.json'),cases[-1])
    assert len(cases)==len(pictures)==4 and alignments==32 and not ctx.machines;sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(ident,page,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),ident+' native page'+str(page),fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        p=ROOT/f'all4_complete_pages_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all4_paragraphs4_complete_native_pages32_alignments.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=cases,complete_native_pages=4,logical_compiled_input_alignment_cases=32,all4_single_pages=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,each216x64_plane_exact_independent_current_font_and_all_canaries=True,all_original_current_font_renderer_instructions_verified=True,zero_source_and_compiled_FI_FA_FO_no_substitutions_added=True,original_pair_phase_and_guards_bound_without_new_substitutions=True,no_actor_role_roster_RNG_or_event_assignment=True,only_original_static_selectors2_92=True,source_owned_expand_adapter=adapter,source_owned_AA5_page_adapter=page_adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),review_sheets=sheets,visual_review_pending=True,only_offline_complete_native_pages_not_actual_button_progression=True,native_name_planes_actual_headers_controls_reference_and_release_pending=True,all4_formatting_gates_remain_false=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,INPUT,Path(old_pages.__code__.co_filename),Path(__file__)]},full_goal_complete=False));print('4 complete single native pages/32 alignments; no original or invented macros. Original pair phase and guards preserved. Actual content, controls, references and release pending.')
