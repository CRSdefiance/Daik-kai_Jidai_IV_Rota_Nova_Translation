"""Complete native English pages and four compiled alignments for all82 utterances."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as original_FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.prove_Hodram_B54_B60_logical_v8801 import expanded_body
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_pages_v8803b')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
PLAN=Path('work/analysis/Hodram_B54_B60_layout_v8802c/automatic_plans.json')
LOGICAL=Path('work/analysis/Hodram_B54_B60_logical_v8801/logical_paragraphs.json')
SOURCE=Path('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,plan,logical,source=map(read,[DOC,PLAN,LOGICAL,SOURCE])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(DOC.read_bytes()) and len(plan['records'])==82 and not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    pixels,factory,oracle=bind(image);FE,calibration=factory(image)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes}
    exec(compile(source['source_owned_target_page_adapter'],__file__+'::complete-original-pages','exec'),pe)
    prog=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::progressive-macros','exec'),prog)
    fe=dict(original_FE_expand.__globals__);exec(compile(logical['source_owned_FE_adapter'],__file__+'::null-actor-FE-macros','exec'),fe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    reuse_path=Path('work/analysis/Hodram_B54_B60_pages_preparation_v8803b/65_complete_rows_andnine_sheets_exact.json');reuse=read(reuse_path)
    assert reuse['manuscript_sha256']==sha(DOC.read_bytes()) and reuse['plan_sha256']==sha(PLAN.read_bytes())
    for path,digest in reuse['files'].items():assert sha(Path(path).read_bytes())==digest
    rows=list(reuse['records']);sheets=list(reuse['sheets']);page_count=reuse['pages']
    for block in doc['blocks']:
        if block in reuse['blocks']:continue
        pictures=[]
        for row in [r for r in doc['records'] if r['block']==block]:
            p=next(r for r in plan['records'] if r['id']==row['id']);raw=bytes.fromhex(p['encoded_hex']);prefix,body=raw[0],raw[1:];is_FE=prefix==254
            assert prefix==row['source_selector'] and body and not any(v in body for v in [b'\0',b'%'])
            assert not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
            expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            assert ' '.join(expected.decode('cp932').split())==expanded_body(row['english']).decode('cp932')
            aligned=ctx.execute(fe['expand'] if is_FE else prog['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
            assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
            if is_FE:
                assert p['expected_native_pages']==1
                rendered=FE(expected);plane=rendered.pop('physical');logical_plane=rendered.pop('logical')
                file=ROOT/(row['id']+'_FE_physical.bin');file.write_bytes(plane);logical_file=file.with_name(row['id']+'_FE_logical.bin');logical_file.write_bytes(logical_plane)
                rendered.update(native_physical_plane=str(file),native_physical_plane_sha256=sha(plane),native_logical_plane=str(logical_file),native_logical_plane_sha256=sha(logical_plane),pages=1)
                picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in plane])
                preview=file.with_suffix('.png');picture.save(preview);rendered.update(preview=str(preview),preview_sha256=sha(preview.read_bytes()))
                pictures.append((row['id']+' FE null-actor',picture));page_count+=1
            else:
                rendered=pe['pages'](arm,font,expected)
                assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==p['expected_native_pages']
                for page in rendered['pages']:
                    plane=bytes.fromhex(page.pop('native_plane_hex'));file=ROOT/(row['id']+f'_page{page["page"]}.bin');file.write_bytes(plane)
                    segment=expected[page['start']:page['end']]
                    guarded=page['page']>1 and segment.startswith(b' ') and not segment.startswith(b'  ')
                    assert page['first_visible_origin']==([6,0] if guarded else [0,0])
                    if guarded:assert page['events'][0]==dict(kind='ascii',code=32,style=1,x=0,y=0)
                    page['native_continuation_guard_at_zero_andfirst_visible_at_six']=guarded
                    picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                    picture.putdata([colors[v] for v in plane]);preview=file.with_suffix('.png');picture.save(preview)
                    page.update(native_plane=str(file),native_plane_sha256=sha(plane),preview=str(preview),preview_sha256=sha(preview.read_bytes()),complete_first_internal_final_codes_bounds_consumption_andindependent_ink_exact=True)
                    pictures.append((row['id']+f' p{page["page"]}',picture));page_count+=1
            rows.append(dict(id=row['id'],file_path=row['file_path'],block=block,source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=prefix,
                source_record_index=row['source_record_index'],kind=row['kind'],compiled_hex=raw.hex(),expanded_native_hex=expected.hex(),logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=aligned,complete_native_English_display=rendered))
        for start in range(0,len(pictures),12):
            part=pictures[start:start+12];sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
            for index,(label,picture) in enumerate(part):
                x,y=index%2*456,index//2*160;draw.text((x+3,y+3),label+' offline English',fill='white')
                sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
            path=ROOT/f'B{block}_English_part{start//12+1}.png';sheet.save(path);sheets.append(dict(block=block,path=str(path),sha256=sha(path.read_bytes()),pages=len(part)))
        save(ROOT/f'B{block}_completed_English_rows.json',dict(records=[r for r in rows if r['block']==block],new_credit=0,actual_gameplay=False))
        print('Complete English native block',block,'utterances',len([r for r in rows if r['block']==block]),'pages',len(pictures),flush=True)
    assert len(rows)==82 and page_count==85 and not ctx.machines
    save(ROOT/'compiled_native_pages.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),records=rows,
        fresh_compiled_alignment_cases=68,reused_compiled_alignment_cases=260,total_bound_compiled_alignment_cases=328,progressive_alignment_cases=324,FE_null_actor_alignment_cases=4,complete_native_English_pages=85,
        progressive_pages=84,FE_panels=1,two_page_record_IDs=[r['id'] for r in plan['records'] if r['expected_native_pages']==2],
        all_complete_leading_internal_final_characters_native_independent_planes_bounds_andconsumption_exact=True,
        no_blank_overlap_orunintended_extra_pages=True,FI3_FA4_FO0_preserved_no_shortening_orprose_manual_wrap=True,
        target_oracle_binding=oracle,FE_factory_calibration=calibration,source_owned_target_page_adapter=source['source_owned_target_page_adapter'],
        source_owned_progressive_adapter=logical['source_owned_progressive_adapter'],source_owned_FE_adapter=logical['source_owned_FE_adapter'],
        review_sheets=sheets,completed65_reuse=str(reuse_path),completed65_reuse_sha256=sha(reuse_path.read_bytes()),native_guard_is_not_a_dropped_leading_glyph=True,direct_view_pending=True,all82_formatting_gates_still_false=True,
        native_offline_checks_not_gameplay_ornew_source_activation=True,stored_controls_actual_headers_transitions_policy_andregistered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,LOGICAL,SOURCE,INPUT,Path('scripts/Hodram_FE_font_oracles_v8315.py'),Path(__file__)]}))
    print('82 records /85 complete native English pages /328 compiled alignments pass; direct view and stored/actual/release pending.',flush=True)
