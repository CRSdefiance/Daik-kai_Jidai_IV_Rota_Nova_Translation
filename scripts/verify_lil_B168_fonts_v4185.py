"""Fresh native compiled calls for changed wraps; reuse only exact logical inputs and native planes."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.dialogue import lil_B168_layout_v3 as codec
from dk4tool.dialogue.lil_B168_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B156_fonts_v3707 import expand as expand_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_FE
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_fonts_v4185')
DOC=Path('translations/lil_B168_editorial_manuscript_v6.json')
PRIOR=Path('work/analysis/lil_B168_fonts_v4182b/all54_native_planes432_macros_and26_consumer_negatives.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,old=map(read,[DOC,PRIOR]);oldrows={r['id']:r for r in read(old['manuscript'])['records']};oldcases={r['id']:r for r in old['cases']}
    im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks;source=read(doc['source_context'])
    assert sha(arm)==old['ARM9_sha256'] and doc['current_ROM_sha256']==old['candidate_sha256'] and sha(im.read_file('/COMMON/MESFILE.DK4'))==old['COMMON_sha256']
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B168_voices_v4170/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    paint=None;cases=[];reports=[];pictures=[];changed=[]
    for r in doc['records']:
        before=oldrows[r['id']];assert all(r[k]==before[k] for k in ['english','source_hex','current_hex','source_complete_preamble_hex','editorial_decision'])
        fe=r['kind']=='system-FE';raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,blocks[168],'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,r['english'],p);q=codec.audit_relocatable_dialogue_record(raw,r['english'],p)
        assert encoded.encoded.hex()==r['compiled_hex'];bad=[i for i in q['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waiver_reason'))];assert not bad
        reports.append(dict(id=r['id'],qa=q,unwaived_issues=bad,documented_waivers=r.get('qa_waivers',[])))
        previous=oldcases[r['id']];assert sha(Path(previous['preview']).read_bytes())==previous['preview_sha256']
        if encoded.encoded.hex()==previous['encoded_hex']:
            c=deepcopy(previous);c['native_proof_method']='Exact compiled bytes and identical logical words,current runtime,source prefix and complete plane reused.'
        else:
            changed.append(r['id']);body=encoded.encoded[1:];expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            result=ctx.execute(expand_FE,body) if fe else ctx.execute(expand_progressive,body,raw[0]);ctx.machines.pop()
            assert len(result['cases'])==4 and all(v['output_hex']==expected.hex() for v in result['cases'])
            pipelines=[deepcopy(next(v for v in previous['current_native_macro_pipelines'] if v['kind']=='logical')),dict(kind='compiled-protected',**result)]
            if fe:
                if paint is None:paint,_=make_painter(im)
                target=paint(expected);assert target['complete_return_input_object_canaries_and_native_independent_plane_equal'];pixels,events=target['physical'],target['events'];geometry=[228,64];picture=Image.new('RGB',tuple(geometry));picture.putdata([(0,8,0) if v else (239,232,201) for v in pixels]);extra=dict(one_native_page_consumes_complete_target=True,complete_logical228x48_plane_sha256=sha(target['logical']),native_FE_object_rebindings=target['object_rebindings'])
            else:
                pixels,events,font=raster(ctx.arm,expected);assert pixels==expected_pixels(ctx.arm,font,events);geometry=[216,64];picture=Image.new('RGB',tuple(geometry));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);extra=dict(complete_native_independent216x64_plane_equal=True)
            visible=[e for e in events if e['code']!=32];assert [e['code'] for e in visible]==[ord(v) for v in expected.decode('ascii') if v not in ' \n']
            assert len(visible)==len({(e['x'],e['y']) for e in visible}) and all(0<=e['x']<=geometry[0]-6 and 0<=e['y']<=(36 if fe else 48) and e['y']%(12 if fe else 16)==0 for e in visible)
            origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
            path=ROOT/(r['id']+'_complete_native.png');picture.save(path)
            c=dict(id=r['id'],kind=r['kind'],encoded_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,expanded_hex=expected.hex(),current_native_macro_pipelines=pipelines,complete_glyph_events=events,complete_native_independent_plane_equal=True,all_first_final_internal_glyphs_in_order_and_unique_cells=True,first_glyph_code=visible[0]['code'],final_glyph_code=visible[-1]['code'],all_visible_origins_zero_and_native_rows_within4rows=True,logical_row_pitch=12 if fe else 16,physical_row_pitch=16,whole_native_plane_sha256=sha(pixels),visible_origins_by_row=origins,geometry=geometry,preview=str(path),preview_sha256=sha(path.read_bytes()),native_proof_method='Fresh original four compiled alignment calls and complete native plane;exact logical words reuse prior four calls.',**extra)
        cases.append(c);pictures.append((r['id'],r['speaker']+' / '+r['kind'],Image.open(c['preview']).convert('RGB')))
    assert len(cases)==54 and not ctx.machines and set(changed)=={'DK4_MES_B168_R0026','DK4_MES_B168_R0077','DK4_MES_B168_R0112','DK4_MES_B168_R0123','DK4_MES_B168_R0152','DK4_MES_B168_R0194'}
    baseline=Path('scripts/verify_lil_B168_fonts_v4182b.py');text=baseline.read_text(encoding='utf-8');adapter='    negatives=[]'+text.split(';negatives=[]',1)[1].split('    sheets=[]',1)[0]
    env=dict(arm=arm,blocks=blocks,doc=doc,profile_for=profile_for,encode_relocatable_dialogue=codec.encode_relocatable_dialogue)
    exec(compile('if True:\n'+adapter,__file__+'::fresh-source-consumer-negatives','exec'),env);negatives=env['negatives'];assert len(negatives)==26
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,label,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / '+label,fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(path);prior=old['review_sheets'][start//8]
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),byte_identical_to_viewed_predecessor=sha(path.read_bytes())==prior['sha256']))
    assert [i+1 for i,s in enumerate(sheets) if s['byte_identical_to_viewed_predecessor']]==[5,7]
    save(ROOT/'all54_native_planes432_macro_cases_and26_consumer_negatives.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,all54_full_QA_reports=reports,current_original_macro_alignment_calls=432,new_current_original_macro_alignment_calls=len(changed)*4,reused_original_macro_alignment_calls=432-len(changed)*4,new_native_planes=len(changed),exact_reused_native_planes=54-len(changed),changed_records=changed,progressive_planes=51,FE_planes=3,all54_complete_native_independent_planes_pass=True,source_consumer_negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),FE_calibration=old['FE_calibration'],all3_complete_FE_planes_exact_byte_reuse_from_viewed_original=True,prior_native_proof=str(PRIOR),prior_native_proof_sha256=sha(PRIOR.read_bytes()),fresh_source_negative_adapter=adapter,actual_selected_B168_IDs=[],new_emulator_runs=0,formatting_gate_and_editorial_credit_still_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(planes=54,alignment_cases=432,fresh_compiled_cases=len(changed)*4,exact_reused_cases=432-len(changed)*4,fresh_planes=len(changed),source_negatives=26,changed_sheets=[1,2,3,4,6],exact_viewed_sheet_reuses=[5,7],credit=0))
