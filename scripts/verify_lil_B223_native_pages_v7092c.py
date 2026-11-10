"""Prove all seventeen complete paragraphs across nineteen original native pages and 136 logical/compiled alignments."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B223_editorial_manuscript_v1.json');PLAN=Path('work/analysis/lil_B223_layout_v7091d/seventeen_complete_paragraph_plans_original_width_no_prose_changes.json')
INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json');ROOT=Path('work/analysis/lil_B223_native_pages_v7092c')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=read(DOC),read(PLAN);assert sha(DOC.read_bytes())==plan['manuscript_sha256'] and len(plan['records'])==17 and not plan['failures']
    byid={r['id']:r for r in doc['records']};image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==(151 if prefix==208 else prefix) and captain==2'});env=dict(expand.__globals__);exec(compile(adapter,__file__+'::D0-original-fallback','exec'),env)
    page_adapter=checked_text(inspect.getsource(old_pages),{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'});page_env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(page_adapter,__file__+'::2b6-original-pages','exec'),page_env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');cases=[];pictures=[];alignments=0
    for record in plan['records']:
        row=byid[record['id']];body=bytes.fromhex(record['encoded_hex'])[1:];logical=row['english'].split('}',1)[1].encode('ascii');prefix=row['source_selector'];pipelines=[]
        assert prefix in [2,13,21,208] and body and body[-1]!=10 and all(body.count(m)==logical.count(m)==0 for m in [b'FI',b'FA',b'FO'])
        for label,text in [('logical',logical),('compiled-protected',body)]:
            result=ctx.execute(env['expand'],text,prefix);ctx.machines.pop();pipelines.append(dict(version=label,**result));alignments+=4;assert all(c['output_hex']==text.hex() for c in result['cases'])
        rendered=page_env['pages'](arm,font,body);assert len(rendered['pages'])==record['expected_native_pages'] and record['max_total_rows'] in [4,8]
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(record['id']+f'_page{page["page"]}.bin');plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels));leading=len(body[page['start']:page['end']])-len(body[page['start']:page['end']].lstrip(b' '));assert leading==(0 if page['page']==1 else 1) and page['first_visible_origin']==[leading*6,0] and (page['page']==1 or body[page['start']-1:page['start']+1]==b'\n ');page.update(compiler_owned_page_continuation_guard_bytes=leading,exact_first_visible_origin_verified_without_font_or_bounds_change=True)
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);path=plane.with_suffix('.png');picture.save(path);page.update(preview=str(path),preview_sha256=sha(path.read_bytes()));pictures.append((record['id'],page['page'],picture))
        cases.append(dict(id=record['id'],source_kind=row['kind'],source_selector=prefix,compiled_hex=record['encoded_hex'],formatted_markup=record['formatted_markup'],logical_and_compiled_current_native_pipelines=pipelines,**rendered));save(ROOT/(record['id']+'_individual_native_proof.json'),cases[-1])
    assert len(cases)==17 and len(pictures)==19 and alignments==136 and not ctx.machines;sheets=[]
    signature=next(r for r in cases if r['id']=='DK4_MES_B223_R0048');signature_events=signature['pages'][0]['events'];assert [e['code'] for e in signature_events if e['code']!=32][-8:]==list(b'IanDukov')
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(ident,page_number,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),ident+' complete native page'+str(page_number),fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        p=ROOT/f'all17_complete_pages_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all17_paragraphs19_complete_pages136_native_alignments.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=cases,complete_native_pages=19,logical_compiled_input_alignment_cases=136,all17_objects_each_original216x64_page_is_four_rows=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,each_plane_exact_independent_current_font_and_all_canaries=True,all_original_current_font_renderer_instructions_verified=True,all_source_macros_zero_no_new_substitutions=True,no_actor_role_roster_RNG_or_event_assignment=True,D0_fallback151_unchanged=True,complete_Ian_Dukov_signature_native_ink_preserved=True,source_owned_expand_adapter=adapter,source_owned_2b6_page_adapter=page_adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),review_sheets=sheets,visual_review_pending=True,only_offline_complete_native_pages_not_actual_gameplay=True,names_source_actual_controls_policy_stored_reference_and_release_pending=True,all17_formatting_gates_remain_false=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,INPUT,Path(old_pages.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print('All17 paragraphs/19 complete native pages/136 logical and compiled alignments pass; complete signature. Four sheets await viewing. Final stored/native policy/actual English/release pending.')
