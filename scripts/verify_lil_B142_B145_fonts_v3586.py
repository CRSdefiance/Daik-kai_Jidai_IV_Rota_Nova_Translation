"""37 progressive planes,one FE plane,304 macro cases and source consumer negatives."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B142_B145_profile import profile_for
from dk4tool.dialogue.lil_B142_B145_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B141_fonts_v3549 import expand as expand_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_FE
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_fonts_v3586')
DOC=Path('translations/lil_B142_B145_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');paint,calibration=make_painter(image)
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__;cases=[];reports=[];pictures=[];macros=0
    for row in doc['records']:
        fe=row['kind']=='system-FE';raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],'FE-paper' if fe else 'progressive');compiled=encode_relocatable_dialogue(raw,row['english'],profile);assert compiled.encoded.hex()==row['compiled_hex'];qa=audit_relocatable_dialogue_record(raw,row['english'],profile);bad=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))];assert not bad,(row['id'],bad);reports.append(dict(id=row['id'],qa=qa,unwaived_issues=bad,documented_waivers=row.get('qa_waivers',[])))
        logical=row['english'].split('}',1)[1]
        for k in ['FI','FA','FO']:logical=logical.replace('{MACRO:'+k+'}',k)
        logical=logical.encode('ascii');body=compiled.encoded[1:];assert compiled.encoded[0]==raw[0];pipelines=[]
        for kind,value in [('logical',logical),('compiled-protected',body)]:
            result=ctx.execute(expand_FE,value) if fe else ctx.execute(expand_progressive,value,raw[0]);ctx.machines.pop();pipelines.append(dict(kind=kind,**result));macros+=4
        expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert all(c['output_hex']==expected.hex() for c in pipelines[1]['cases'])
        if fe:
            assert all(c['null_source_actor'] for p in pipelines for c in p['cases']);target=paint(expected);assert target['complete_return_input_object_canaries_and_native_independent_plane_equal'];events=target['events'];pixels=target['physical'];geometry=[228,64];picture=Image.new('RGB',tuple(geometry));picture.putdata([(0,8,0) if v else (239,232,201) for v in pixels]);extra=dict(one_native_page_consumes_complete_target=True,complete_logical228x48_plane_sha256=sha(target['logical']),native_FE_object_rebindings=target['object_rebindings'])
        else:
            pixels,events,font=raster(ctx.arm,expected);assert pixels==expected_pixels(ctx.arm,font,events);geometry=[216,64];picture=Image.new('RGB',tuple(geometry));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);extra=dict(complete_native_independent216x64_plane_equal=True)
        visible=[e for e in events if e['code']!=32];wanted=[ord(c) for c in expected.decode('ascii') if c not in ' \n'];assert [e['code'] for e in visible]==wanted and len(visible)==len({(e['x'],e['y']) for e in visible});assert all(0<=e['x']<=geometry[0]-6 and 0<=e['y']<=48 and e['y']%16==0 for e in visible);origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values());assert body and not body.startswith((b' ',b'\n'))
        path=ROOT/(row['id']+'_complete_native.png');picture.save(path);pictures.append((row['id'],row['speaker']+' / '+row['kind'],picture));cases.append(dict(id=row['id'],kind=row['kind'],encoded_hex=compiled.encoded.hex(),formatted_markup=compiled.formatted_markup,expanded_hex=expected.hex(),current_native_macro_pipelines=pipelines,complete_glyph_events=events,complete_native_independent_plane_equal=True,all_first_final_internal_glyphs_in_order_and_unique_cells=True,first_glyph_code=visible[0]['code'],final_glyph_code=visible[-1]['code'],all_visible_origins_zero_and16px_rows_within4rows=True,whole_native_plane_sha256=sha(pixels),visible_origins_by_row=origins,geometry=geometry,preview=str(path),preview_sha256=sha(path.read_bytes()),**extra))
    assert len(cases)==38 and len(reports)==38 and macros==304 and not ctx.machines;negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,error=str(error),rejected=True))
        else:raise AssertionError(label)
    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[142]));reject('unrelated-block',lambda:profile_for(arm,blocks[141]));reject('mutated-source-block',lambda:profile_for(arm,blocks[142][:-1]+bytes([blocks[142][-1]^1])))
    progressive=profile_for(arm,blocks[142]);feprofile=profile_for(arm,blocks[144],'FE-paper')
    for selector in [2,4,9,13,16,20,23,109,171]:
        row=next(r for r in doc['records'] if r['source_selector']==selector);tag='{SPEAKER:'+format(selector,'02X')+'}';other='{SPEAKER:'+format(4 if selector==2 else 2,'02X')+'}'
        reject('missing-'+format(selector,'02X'),lambda r=row,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),progressive));reject('wrong-legal-'+format(selector,'02X'),lambda r=row,t=tag,o=other:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,o),progressive))
    plain=next(r for r in doc['records'] if r['kind']=='progressive' and '{MACRO:' not in r['english']);modal=next(r for r in doc['records'] if r['kind']=='system-FE')
    reject('FE-as-ordinary',lambda:encode_relocatable_dialogue(bytes.fromhex(modal['source_hex']),modal['english'],progressive));reject('ordinary-as-FE',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english'],feprofile));reject('missing-FE',lambda:encode_relocatable_dialogue(bytes.fromhex(modal['source_hex']),modal['english'].replace('{SPEAKER:FE}',''),feprofile));reject('wrong-FE',lambda:encode_relocatable_dialogue(bytes.fromhex(modal['source_hex']),modal['english'].replace('{SPEAKER:FE}','{SPEAKER:02}'),feprofile))
    reject('invented-native-macro',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+' {MACRO:FI}',progressive));reject('manual-layout',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+'{LB}',progressive));reject('embedded-NUL',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+'{HEX:00}',progressive));assert len(negatives)==28
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,label,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / '+label,fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x+5,y+24))
        p=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all38_native_planes304_macros_and28_consumer_negatives.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,all38_full_QA_reports=reports,current_original_macro_alignment_calls=macros,progressive_planes=37,FE_planes=1,all38_complete_native_independent_planes_pass=True,source_consumer_negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),FE_calibration=calibration,source0D6D_do_not_enter_visible_prose=True,actual_selected_B142_B145_IDs=[],new_emulator_runs=0,formatting_gate_and_editorial_credit_still_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('38 complete native planes,304 macro alignments,28 consumer negatives pass. Five sheets need visual review. No gameplay or credit.')
