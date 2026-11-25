"""Six complete current-native pages, distinct FE paper and 24 compiled macro alignments."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B49_registered_route_context_v8478 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B50_pages_v8492')
DOC=Path('translations/hodram_B50_editorial_manuscript_v1.json')
PLAN=Path('work/analysis/Hodram_B50_layout_v8491/automatic_plans.json')
LOGICAL=Path('work/analysis/Hodram_B50_logical_v8490/logical_paragraphs.json')
SOURCE=Path('work/analysis/Hodram_B50_source_display_v8487/source_display.json')
INPUT=Path('work/analysis/current_V8475_Hodram_native_v8478/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,logical,source=map(read,[DOC,PLAN,LOGICAL,SOURCE])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(DOC.read_bytes()) and not plan['failures'] and len(plan['records'])==3
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT');pixels,factory,oracle=bind(image);paint,calibration=factory(image)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};page_adapter=source['source_owned_target_page_adapter'];exec(compile(page_adapter,__file__+'::unchanged-current-complete-pages','exec'),pe)
    prog=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::unchanged-progressive-wrapper','exec'),prog)
    fe=dict(FE_expand.__globals__);exec(compile(logical['source_owned_FE_adapter'],__file__+'::unchanged-nullactor-FE-wrapper','exec'),fe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];pictures=[]
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'];raw=bytes.fromhex(p['encoded_hex']);body=raw[1:];is_FE=row['source_selector']==254
        assert raw[0]==row['source_selector'] and body and not any(v in body for v in [b'\0',b'%']) and not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
        aligned=ctx.execute(fe['expand'] if is_FE else prog['expand'],body,*(() if is_FE else (row['source_selector'],)));ctx.machines.pop()
        expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet');assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
        assert ' '.join(expected.decode('cp932').split())==row['english'].replace('{MACRO:FI}','Hodram')
        if is_FE:
            assert all(c['null_source_actor'] for c in aligned['cases']);target=paint(expected);events=target['events'];logicalplane=target.pop('logical');physical=target.pop('physical')
            plane=ROOT/(row['id']+'_FE_logical.bin');plane.write_bytes(logicalplane);physicalfile=ROOT/(row['id']+'_FE_physical.bin');physicalfile.write_bytes(physical)
            picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in physical]);preview=ROOT/(row['id']+'_FE_complete.png');picture.save(preview)
            rendered=dict(pages=[dict(page=1,start=0,end=len(expected),events=events,native_plane=str(plane),native_plane_sha256=sha(logicalplane),physical_plane=str(physicalfile),physical_plane_sha256=sha(physical),preview=str(preview),preview_sha256=sha(preview.read_bytes()),all_complete_glyphs_original_bounds_andreturn_exact=True)],
                complete_consumed_bytes=len(expected),logical_geometry=[228,48],physical_geometry=[228,64],original_null_actor_consumer=True,independent_logical_andphysical_planes_exact=True,original_native_painter=target)
            pictures.append((row['id']+' original FE',picture))
        else:
            rendered=pe['pages'](arm,font,expected)
            for page in rendered['pages']:
                plane=bytes.fromhex(page.pop('native_plane_hex'));file=ROOT/(row['id']+f'_page{page["page"]}.bin');file.write_bytes(plane)
                segment=expected[page['start']:page['end']];leading=len(segment)-len(segment.lstrip(b' '));assert leading==0 and page['first_visible_origin']==[0,0]
                picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in plane]);preview=file.with_suffix('.png');picture.save(preview)
                page.update(native_plane=str(file),native_plane_sha256=sha(plane),preview=str(preview),preview_sha256=sha(preview.read_bytes()),complete_first_internal_final_codes_bounds_consumption_andindependent_ink_exact=True);pictures.append((row['id']+f' p{page["page"]}',picture))
        assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==p['expected_native_pages']==1
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind=row['kind'],source_reference=row['source_reference'],current_reference=row['current_reference'],compiled_hex=raw.hex(),expanded_native_hex=expected.hex(),logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=aligned,**rendered))
    assert len(rows)==3 and not ctx.machines and len(pictures)==3
    sheet=Image.new('RGB',(1368,320),'#263238');draw=ImageDraw.Draw(sheet)
    for n,(label,picture) in enumerate(pictures):
        x,y=n%3*456,n//3*160;draw.text((x+3,y+3),label+' offline native',fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
    path=ROOT/'three_complete_English_native_pages.png';sheet.save(path)
    save(ROOT/'compiled_native_pages.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),records=rows,
        fresh_compiled_alignment_cases=12,progressive_alignment_cases=8,FE_null_actor_alignment_cases=4,complete_progressive_pages=2,complete_FE_logical_andphysical_pages=1,
        all_complete_leading_internal_final_characters_native_independent_planes_bounds_andconsumption_exact=True,all_three_single_pages_no_blank_orunintended_extra_page=True,all_zero_source_macros_preserved_no_shortening_orprose_manual_wrap=True,
        target_oracle_binding=oracle,FE_factory_calibration=calibration,source_owned_target_page_adapter=page_adapter,source_owned_progressive_adapter=logical['source_owned_progressive_adapter'],source_owned_FE_adapter=logical['source_owned_FE_adapter'],
        review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),direct_view_pending=True,all_three_formatting_gates_still_false=True,
        stored_controls_source_effect_semantics_actual_FE_scene_geometry_palette_transitions_policy_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,LOGICAL,SOURCE,INPUT,Path('scripts/Hodram_FE_font_oracles_v8315.py'),Path(__file__)]}))
    print('B50three complete one-page English displays/12compiled alignments:two progressive+oneoriginalFE;allglyphs/guards/bounds/consumption pass.Directview/stored/actual/release pending.')
