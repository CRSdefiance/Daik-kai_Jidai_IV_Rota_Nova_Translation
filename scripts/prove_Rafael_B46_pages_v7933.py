"""Current-code complete native progressive pages and distinct FE logical/physical planes."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels,make_painter
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_pages_v7933')
PLAN=Path('work/analysis/Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json')
LOGICAL=Path('work/analysis/Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json')
PRIOR=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,logical,doc,names,prior=map(read,[PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    page_adapter=prior['source_owned_2b6_page_adapter'];pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(page_adapter,__file__+'::exact-current-progressive-pages','exec'),pe)
    prog_env=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::original-progressive-macros','exec'),prog_env)
    fe_env=dict(FE_expand.__globals__);exec(compile(logical['source_owned_FE_adapter'],__file__+'::original-null-actor-FE-macros','exec'),fe_env)
    paint,calibration=make_painter(image)
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    executable_sections=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    cold_original=paint.__globals__['cold_machine'];FE_executed=set()
    def guarded_cold(current_arm):
        assert current_arm==arm
        cpu=cold_original(current_arm)
        def exact(u,pc,size,unused):
            owners=[s for s in executable_sections if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(owners)==1,hex(pc)
            s=owners[0];at=pc-s.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(s.data[at:at+size]),hex(pc)
            FE_executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact)
        return cpu
    paint=FunctionType(paint.__code__,{**paint.__globals__,'cold_machine':guarded_cold},
        argdefs=paint.__defaults__,closure=paint.__closure__)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];pictures=[]
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'];encoded=bytes.fromhex(p['encoded_hex']);prefix=row['source_selector'];body=encoded[1:];is_FE=prefix==254
        assert encoded[0]==prefix and b'\0' not in body and b'%' not in body and body and not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
        result=ctx.execute(fe_env['expand'] if is_FE else prog_env['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
        expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        assert ' '.join(expected.decode('ascii').split())==row['english'].replace('FI','Rafael').replace('FA','Castor').replace('FO','Castor Co.')
        if is_FE:
            assert all(c['null_source_actor'] for c in result['cases'])
            assert all(token not in expected for token in [b'FI',b'FA',b'FO',b'%'])
            target=paint(expected);assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
            events=target['events'];visible=[e for e in events if e['code']!=32]
            assert [e['code'] for e in visible]==[v for v in expected if v not in [32,10]]
            assert len(visible)==len({(e['x'],e['y']) for e in visible})
            assert all(0<=e['x']<=222 and e['y'] in [0,12,24,36] for e in visible)
            plane=ROOT/(row['id']+'_FE228x48.bin');plane.write_bytes(target['logical'])
            picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in target['physical']])
            path=ROOT/(row['id']+'_FE_complete.png');picture.save(path);pictures.append((row['id']+' FE original paper',picture))
            rendered=dict(pages=[dict(page=1,start=0,end=len(expected),events=events,
                native_plane=str(plane),native_plane_sha256=sha(target['logical']),physical_plane_sha256=sha(target['physical']),
                preview=str(path),preview_sha256=sha(path.read_bytes()),all_complete_glyphs_andoriginal_bounds_exact=True)],
                complete_consumed_bytes=len(expected),logical_geometry=[228,48],physical_geometry=[228,64],
                independent_logical_andphysical_planes_exact=True,original_null_actor_consumer=True,
                no_new_actual_FE_gameplay_claim=True,object_rebindings=target['object_rebindings'])
        else:
            rendered=pe['pages'](arm,font,expected)
            assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==p['expected_native_pages']
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(row['id']+f'_page{page["page"]}.bin');path.write_bytes(pixels)
                segment=expected[page['start']:page['end']];leading=len(segment)-len(segment.lstrip(b' '))
                assert leading==(0 if page['page']==1 else 1) and page['first_visible_origin']==[6*leading,0]
                picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
                page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
                    first_visible_origin_matches_original_return_andguard=True)
                pictures.append((row['id']+f' p{page["page"]}',picture))
        assert len(rendered['pages'])==p['expected_native_pages']
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],
            source_selector=prefix,kind=row['kind'],compiled_hex=encoded.hex(),expanded_native_hex=expected.hex(),
            logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,**rendered))
        print('PAGE_PASS',row['id'],row['kind'],len(rendered['pages']),flush=True)
    assert len(rows)==24 and not ctx.machines and sum(len(r['pages']) for r in rows)==24
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1368,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(label,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*456,n//3*160;draw.text((x+3,y+3),label+' offline native',fill='white')
            sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Rafael_B46_native_pages_sheet{start//6+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'24_complete_native_pages96_compiled_alignments12_FE.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,fresh_compiled_alignment_cases=96,progressive_alignment_cases=48,FE_null_actor_alignment_cases=48,
        complete_progressive_pages=12,complete_FE_logical_andphysical_pages=12,
        all_complete_first_internal_final_characters_native_independent_glyph_planes_bounds_andconsumption_exact=True,
        FE_original228x48_logical_228x64_physical_6x12_metrics=True,
        FE_source_zero_macros_buttons_mode_orders_andno_printf_conversion_preserved=True,
        FE_current_executed_instruction_addresses=len(FE_executed),all_FE_executed_instructions_exact_current_sections_andpayload=True,
        historical_FE_geometry_current_font_calibration=calibration,review_sheets=sheets,visual_review_pending=True,
        source_owned_progressive_page_adapter=page_adapter,
        source_owned_progressive_macro_adapter=logical['source_owned_progressive_adapter'],source_owned_FE_macro_adapter=logical['source_owned_FE_adapter'],
        all26_formatting_gates_false=True,wholecontrols_relocation_actual_andregistered_release_pending=True,
        ordinary_captain0_context_no_state_fixture=True,new_emulator_runs=0,new_credit=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('24 complete native pages/96 fresh compiled alignments pass. Four sheets need viewing;choice fonts,actual scenes,relocation andregistered release pending.')
