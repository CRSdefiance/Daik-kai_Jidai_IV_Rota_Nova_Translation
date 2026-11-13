"""Verify current-font B97 planes and a source72 two-page projection;actual A advance stays open."""
from dataclasses import replace
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.maria_B97_profile import profile_for
from dk4tool.dialogue.maria_B97_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts.prove_maria_B109_macro_profile_v3507 import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.lil_current_font_oracles_v4792 import make_painter,expected_pixels
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_fonts_v5013')
DOC=Path('translations/maria_B97_editorial_manuscript_v3.json')
PROFILE=Path('dk4tool/dialogue/maria_B97_profile.py')
FORMATTER=Path('dk4tool/dialogue/maria_B97_layout_v2.py')

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM'])
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    blocks=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B97_voices_v5000/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
    raster.__kwdefaults__=original_raster.__kwdefaults__
    paint,calibration=make_painter(image);cases=[];pictures=[];macro_calls=0
    colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
    for row in doc['records']:
        isFE=row['kind']=='system-FE';paged=row['source_record_index']==72;raw=bytes.fromhex(row['source_hex'])
        consumer='FE-paper' if isFE else ('progressive-two-page' if paged else 'progressive')
        profile=profile_for(arm,blocks[97],consumer,raw)
        qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))]
        assert not issues,(row['id'],issues)
        encoded=encode_relocatable_dialogue(raw,row['english'],profile);assert encoded.encoded.hex()==row['compiled_hex'] and encoded.encoded[0]==raw[0]
        logical=row['english'].split('}',1)[1]
        for m in ['FI','FA','FO']:logical=logical.replace('{MACRO:'+m+'}',m)
        body=encoded.encoded[1:];assert all(raw.count(m)==body.count(m) for m in [b'FI',b'FA',b'FO'])
        expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan');pipelines=[]
        for label,text in [('logical',logical.encode('ascii')),('compiled-protected',body)]:
            pipelines.append(dict(kind=label,**ctx.execute(FE_expand if isFE else progressive_expand,text,*(() if isFE else (raw[0],)))))
            macro_calls+=4;ctx.machines.pop()
        assert all(c['output_hex']==expected.hex() for c in pipelines[1]['cases'])
        previews=[];plane_paths=[]
        if isFE:
            assert all(c['null_source_actor'] for p in pipelines for c in p['cases'])
            target=paint(expected);events=target['events'];pixels=target['physical'];width=228;maxx=222;pitch=12;maxy=36
            assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
            page=Image.new('RGB',(228,64));page.putdata([(0,8,0) if p else (239,232,201) for p in pixels])
            pages=[page];details=dict(complete_native_independent228x48_plane_equal=True,complete_physical228x64_plane_equal=True,logical_plane_sha256=sha(target['logical']),physical_plane_sha256=sha(pixels),original_null_actor_consumer_preserved=True,object_rebindings=target['object_rebindings'])
        else:
            height=128 if paged else 64
            pixels,events,font=raster(arm,expected,canvas_height=height)
            assert pixels==expected_pixels(arm,font,events,canvas_height=height)
            width=216;maxx=210;pitch=16;maxy=112 if paged else 48
            full=Image.new('RGB',(216,height));full.putdata([colors[v] for v in pixels])
            pages=[full.crop((0,start,216,start+64)) for start in range(0,height,64)]
            details=dict(complete_native_independent_font_matrix_equal=True,font_matrix_width=216,font_matrix_height=height,font_matrix_sha256=sha(pixels),native_font_painter_input_return_and_object_canaries_exact=True,physical_native_viewport_width=216,physical_native_viewport_height=64,physical_rows_per_page=4,original_progressive54020_consumer_preserved=True,pagination_is_offline_projection_not_executed_A_continuation=paged)
        visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[v for v in expected if v not in [32,10]]
        assert len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=maxx and 0<=e['y']<=maxy and e['y']%pitch==0 for e in visible)
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
        if paged:
            assert sorted(origins)==[0,16,32,48,64] and len(pages)==2
            assert qa['visible_lines'][4]=="We're gathering them to stop that."
            assert any(pixels[216*64:]) and not any(pixels[216*80:])
        for number,page in enumerate(pages,1):
            path=ROOT/(row['id']+f'_page{number}_'+('projected' if paged else 'native')+'.png');page.save(path)
            previews.append(dict(page=number,path=str(path),sha256=sha(path.read_bytes()),is_offline_page_projection=paged));pictures.append((row['id']+f' page{number}',row['speaker'],page,paged))
        plane=ROOT/(row['id']+'_whole_font_matrix.bin');plane.write_bytes(pixels)
        cases.append(dict(id=row['id'],kind=row['kind'],encoded_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,expanded_hex=expected.hex(),qa=qa,current_native_macro_pipelines=pipelines,complete_glyph_events=events,all_first_final_internal_glyphs_in_order_and_unique_cells=True,all_visible_origins_zero_and_current_width_bounds_exact=True,visible_origins_by_row=origins,whole_font_plane=str(plane),whole_font_plane_sha256=sha(pixels),previews=previews,one_page_complete_target=not paged,pages_projected=2 if paged else 1,current_actual_page_advance_pending=paged,**details))
        print(row['id']+' complete '+('two-page projection' if paged else ('FE' if isFE else 'progressive')),flush=True)
    assert len(cases)==32 and len(pictures)==33 and macro_calls==256 and not ctx.machines
    assert sum(c['kind']=='system-FE' for c in cases)==1
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,error=str(error),rejected=True))
        else:raise AssertionError(label)
    block=blocks[97];plain=next(r for r in doc['records'] if r['source_record_index']==13);prog=profile_for(arm,block);fe=profile_for(arm,block,'FE-paper')
    r72=next(r for r in doc['records'] if r['source_record_index']==72);paged=profile_for(arm,block,'progressive-two-page',bytes.fromhex(r72['source_hex']))
    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block))
    reject('unrelated-block',lambda:profile_for(arm,blocks[96]))
    reject('mutated-block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1])))
    reject('unknown-consumer',lambda:profile_for(arm,block,'typed-choice'))
    for selector in [3,10,180,254]:
        r=next(r for r in doc['records'] if r['source_selector']==selector and r['source_record_index']!=72);p=fe if selector==254 else prog;tag='{SPEAKER:'+format(selector,'02X')+'}'
        reject('missing-selector-'+str(selector),lambda r=r,p=p,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),p))
        reject('changed-selector-'+str(selector),lambda r=r,p=p,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,'{SPEAKER:55}'),p))
    for macro in ['FI','FA','FO']:reject('invented-macro-'+macro,lambda m=macro:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+' {MACRO:'+m+'}',prog))
    for label,extra in [('manual-layout','{LB}'),('embedded-NUL','{HEX:00}')]:reject(label,lambda extra=extra:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+extra,prog))
    reject('FE-through-progressive',lambda:encode_relocatable_dialogue(b'\xfeJapanese','{SPEAKER:FE}Hello.',prog))
    reject('progressive-through-FE',lambda:encode_relocatable_dialogue(b'\x03Japanese','{SPEAKER:03}Hello.',fe))
    reject('two-page-profile-without-source',lambda:profile_for(arm,block,'progressive-two-page'))
    reject('two-page-profile-unrelated-source',lambda:profile_for(arm,block,'progressive-two-page',bytes.fromhex(plain['source_hex'])))
    reject('two-page-encoder-unrelated-source',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english'],paged))
    reject('single-page-profile-eight-lines',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english'],replace(prog,max_lines=8)))
    reject('two-page-profile-widened',lambda:encode_relocatable_dialogue(bytes.fromhex(r72['source_hex']),r72['english'],replace(paged,window_width_px=228)))
    assert len(negatives)==24
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,picture,paged) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker+(' PROJECTED' if paged else ''),fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'all32_font_matrices_256_alignments_and_source72_page_projection.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,current_original_macro_alignment_calls=256,progressive_alignment_calls=248,FE_null_actor_alignment_calls=8,complete_one_page_progressive_planes=30,complete_FE_logical_and_physical_planes=1,source72_complete_native_font_matrix_and_two_offline_page_projections=True,actual_source72_A_continuation_not_yet_verified=True,all_actor_models_and4MiB_current_Maria_context_exact=True,no_initialized_RAM_or_code_overlay=True,FE_geometry_calibration=calibration,scoped_profile=str(PROFILE),scoped_profile_sha256=sha(PROFILE.read_bytes()),native_formatter_module=str(FORMATTER),native_formatter_module_sha256=sha(FORMATTER.read_bytes()),negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B97_IDs=[],new_emulator_runs=0,new_review_credit=0,not_relocation_actual_or_registered_release_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('32 current-font matrices/256 alignments/24 negatives pass.33 panels on five sheets await visual review;source72 actual A advance remains open.',flush=True)
