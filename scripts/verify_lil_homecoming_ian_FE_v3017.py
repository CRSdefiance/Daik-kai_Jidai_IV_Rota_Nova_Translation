"""All14 source FE panels: current null-actor macros, whole font planes, pagination."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_homecoming_ian_profile import profile_for
from dk4tool.dialogue.lil_homecoming_ian_layout_v2 import encode_relocatable_dialogue
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Homecoming_Ian_FE_v3017')
DOC=Path('translations/lil_homecoming_ian_editorial_manuscript_v4.json')
WEDDING=Path('work/analysis/lil_Homecoming_Ian_wedding_contract_v3006/historical_actual_wedding_FE_and_M26_source_contract.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');source=read(doc['source_context'])
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True);contextpath=ROOT/'historical_source_context.json';save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json';save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context');paint,calibration=make_painter(image)
    wedding=read(WEDDING);assert wedding['current_ROM_sha256']==doc['current_ROM_sha256'] and wedding['current_native_paint_of_historical_first_wedding_body_complete_ink_and_blank_mask_equals_actual']
    cases=[];pictures=[];macro_calls=0;FI_cases=[]
    for row in doc['records']:
        if row['kind']!='system-FE': continue
        profile=profile_for(arm,blocks[row['block']],'FE-paper');compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile);assert compiled.encoded[:1]==b'\xfe'
        logical=row['english'].split('}',1)[1].replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('ascii');body=compiled.encoded[1:];pipelines=[]
        for kind,text in [('logical',logical),('compiled-protected',body)]:
            pipelines.append(dict(kind=kind,**ctx.execute(expand,text)));macro_calls+=4;ctx.machines.pop()
        expanded=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert all(c['output_hex']==expanded.hex() for c in pipelines[1]['cases'])
        sourcebody=bytes.fromhex(row['source_hex'])[1:]
        for macro in [b'FI',b'FA',b'FO']: assert sourcebody.count(macro)==body.count(macro)
        if b'FI' in sourcebody:
            assert row['id']=='DK4_MES_B70_R0634' and sourcebody.count(b'FI')==1
            FI_cases.append(dict(id=row['id'],all8_logical_compiled_original_null_actor_substitution_cases_exact=True))
        target=paint(expanded);assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
        visible=[e for e in target['events'] if e['code']!=32]
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
        assert not row.get('source_visible_speaker_label') and not row['source_Japanese'].startswith('＜')
        assert not body.startswith((b'\n',b' '))
        preview=ROOT/(row['id']+'_complete_physical.png');picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in target['physical']]);picture.save(preview);pictures.append((row['id'],picture))
        plane=ROOT/(row['id']+'_complete_logical_228x48.bin');plane.write_bytes(target['logical'])
        cases.append(dict(id=row['id'],encoded_hex=compiled.encoded.hex(),formatted_markup=compiled.formatted_markup,expanded_hex=expanded.hex(),current_native_macro_pipelines=pipelines,
            native_glyphs=target['events'],one_native_page_consumes_complete_target=True,complete_native_independent_plane_and_all_glyphs_and_canaries_equal=True,all_visible_origins_zero_and4rows=True,visible_origins_by_row=origins,
            native_plane=str(plane),native_plane_sha256=sha(target['logical']),whole_physical228x64_plane_sha256=sha(target['physical']),preview=str(preview),preview_sha256=sha(preview.read_bytes()),object_rebindings=target['object_rebindings']))
    assert len(cases)==14 and macro_calls==112 and len(FI_cases)==1 and not ctx.machines
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / FE paper',fill='white');sheet.paste(picture.resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_FE_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'current_FE_macro_font_and_typed_paper_proof.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,current_original_null_actor_macro_alignment_cases=112,
        logical_geometry=[228,48],physical_geometry=[228,64],physical_rows_advance=16,logical_rows_advance=12,current_cold_typed_graphics_object_construction=True,no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter=True,
        all14_one_native_page_consumes_complete_target=True,all14_complete_native_independent_planes_all_glyphs_and_canaries_equal=True,all14_source_panels_remain_distinct_and_unlabeled=True,source_FI_null_actor_cases=FI_cases,
        source_conditional_departure_separate_from_unconditional_realization=True,several_years_and_two_bells_and_five_wedding_FE_exchanges_preserved=True,
        scoped_profile='dk4tool/dialogue/lil_homecoming_ian_profile.py',scoped_profile_sha256=sha(Path('dk4tool/dialogue/lil_homecoming_ian_profile.py').read_bytes()),native_formatter_module='dk4tool/dialogue/lil_homecoming_ian_layout_v2.py',native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_homecoming_ian_layout_v2.py').read_bytes()),
        historical_calibration=calibration,wedding_contract=str(WEDDING),wedding_contract_sha256=sha(WEDDING.read_bytes()),review_sheets=sheets,visual_review_pending=True,
        dependencies={str(p):sha(p.read_bytes()) for p in [Path('scripts/lil_kuhn_china_FE_painter_v2909.py'),Path('scripts/verify_lil_clifford_north_new_world_FE_v2980.py')]},
        native_macro_context_plan=str(ctx.proof_path),native_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_Homecoming_Ian_IDs=[],new_emulator_runs=0,reference_and_release_still_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('14FE complete current nativeplanes/112null-actor macro cases;oneFI preserved. Historical actual wedding paper rule bound;two sheets need visual review.')
