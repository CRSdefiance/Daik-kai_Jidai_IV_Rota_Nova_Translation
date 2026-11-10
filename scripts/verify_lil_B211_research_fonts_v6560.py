"""Measure all B211 research layouts on the exact current progressive/FE native consumers."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels,make_painter
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_lil_B174_fonts_v4470 import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B211_editorial_manuscript_v1.json');PLAN=Path('work/analysis/lil_B211_layout_v6559c/twelve_whole_paragraph_research_plans.json');INPUT=Path('work/analysis/current_V6541_native_v6549/current_native_input.json');ROOT=Path('work/analysis/lil_B211_research_fonts_v6560')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=read(DOC),read(PLAN);assert sha(DOC.read_bytes())==plan['manuscript_sha256'] and len(plan['records'])==12 and not plan['failures'];byid={r['id']:r for r in doc['records']};image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    adapter=checked_text(inspect.getsource(old_pages),{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'});env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(adapter,__file__+'::exact-current-four-row-pages','exec'),env);pages=env['pages'];paint,cal=make_painter(image)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');cases=[];pictures=[];alignments=0
    for record in plan['records']:
        row=byid[record['id']];fe=row['kind']=='system-FE';body=bytes.fromhex(record['encoded_hex'])[1:];logical=row['english'].split('}',1)[1].replace('{MACRO:FI}','FI').encode('ascii');prefix=row['source_selector'];pipelines=[]
        assert body and body[-1]!=10 and body.count(b'FI')==logical.count(b'FI')==bytes.fromhex(row['source_hex'])[1:].count(b'FI') and all(body.count(m)==logical.count(m)==0 for m in [b'FA',b'FO'])
        for label,text in [('logical',logical),('compiled-protected',body)]:
            result=ctx.execute(FE_expand if fe else progressive_expand,text,*(() if fe else (prefix,)));ctx.machines.pop();pipelines.append(dict(version=label,**result));alignments+=4;expected=text.replace(b'FI',b'Lil');assert all(c['output_hex']==expected.hex() for c in result['cases'])
            if fe:assert all(c['null_source_actor'] for c in result['cases'])
        expanded=body.replace(b'FI',b'Lil')
        if fe:
            native=paint(expanded);events=native['events'];assert native['complete_return_input_object_canaries_and_native_independent_plane_equal'];pixels=native['physical'];plane=ROOT/(record['id']+'_physical_228x64.bin');plane.write_bytes(pixels);logical_path=ROOT/(record['id']+'_logical_storage288x48.bin');logical_path.write_bytes(native['logical']);picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if p else (239,232,201) for p in pixels]);visible=[e for e in events if e['code']!=32]
            assert [e['code'] for e in visible]==[v for v in expanded if v not in [32,10]] and len(visible)==len({(e['x'],e['y']) for e in visible}) and all(0<=e['x']<=210 and e['y'] in [0,12,24,36] for e in visible)
            rendered=dict(pages=[dict(page=1,native_plane=str(plane),native_plane_sha256=sha(pixels),logical_native_plane=str(logical_path),logical_native_plane_sha256=sha(native['logical']),events=events,all_first_internal_final_glyphs_in_order_unique_and_bounded=True)],total_bytes=len(expanded),complete_consumed_bytes=len(expanded),all_visible_first_internal_final_characters_in_order=True,no_blank_or_overlap_page=True,original_null_actor_typed_FE228x48_logical228x64_physical=True,object_rebindings=native['object_rebindings'])
        else:
            rendered=pages(arm,font,expanded);assert len(rendered['pages'])==1
            page=rendered['pages'][0];pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(record['id']+'_page1_216x64.bin');plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels));picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels])
        preview=ROOT/(record['id']+'_complete_native.png');picture.save(preview);pictures.append((record['id'],fe,picture));cases.append(dict(id=record['id'],source_kind=row['kind'],source_selector=prefix,compiled_hex=record['encoded_hex'],expanded_hex=expanded.hex(),formatted_markup=record['formatted_markup'],preview=str(preview),preview_sha256=sha(preview.read_bytes()),logical_and_compiled_current_native_pipelines=pipelines,**rendered));print(record['id']+' complete '+('FE' if fe else 'progressive'),flush=True)
    assert len(cases)==12 and len(pictures)==12 and alignments==96 and not ctx.machines and sum(c['source_kind']=='system-FE' for c in cases)==3
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1368,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(ident,fe,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*456,n//3*160;draw.text((x+3,y+3),ident+(' FE null actor' if fe else ' progressive'),fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
        p=ROOT/f'all12_complete_pages_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all12_bodies12_complete_native_pages_and96_alignments_RESEARCH.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=cases,complete_native_pages=12,progressive_pages=9,FE_pages=3,logical_compiled_input_alignment_cases=96,progressive_alignment_cases=72,FE_null_actor_alignment_cases=24,all12_objects_one_original_four_row_native_page=True,all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds=True,progressive216x64_and_FE_original_descriptor_independent_planes_and_canaries_exact=True,original_FI_macro_preserved_and_expands_to_Lil_in_all_alignments=True,FE_no_assigned_speaker_or_fallback_actor=True,no_native_font_viewport_guard_pair_phase_or_prose_change=True,source_owned_progressive_page_adapter=adapter,FE_geometry_calibration=cal,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),review_sheets=sheets,visual_review_pending=True,only_offline_complete_native_pages_not_actual_button_progression=True,source_actual_native_masks_names_and_references_release_pending=True,all12_formatting_gates_remain_false=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,INPUT,Path(old_pages.__code__.co_filename),Path(progressive_expand.__code__.co_filename),Path(FE_expand.__code__.co_filename),Path('scripts/Al_Ferid_font_oracles_v6520.py'),Path(__file__)]},full_goal_complete=False));print('All twelve native pages and96 alignment cases pass;FE/current source capture and visual review remain separately required.')
