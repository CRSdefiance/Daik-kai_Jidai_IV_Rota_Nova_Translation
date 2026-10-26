"""Seven FE stat/monkey panels: current null-actor macros,whole planes,pagination."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_crew_items_profile import profile_for
from dk4tool.dialogue.lil_crew_items_layout_v2 import encode_relocatable_dialogue
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Crew_Items_FE_v3129')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v4.json')
TERMS=Path('work/analysis/lil_Crew_Items_terms_v3116/clean_current_ten_items_stat_UI_and_native_actor_terms.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');source=read(doc['source_context'])
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True);contextpath=ROOT/'historical_source_context.json';save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json';save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context');paint,calibration=make_painter(image)
    terms=read(TERMS);assert terms['all10_clean_current_pointer_strings_equal_registered_names']
    cases=[];pictures=[];macro_calls=0;FI_cases=[]
    expected_source_and_targets={'DK4_MES_B82_R0083': ('FIの運勢が\n１上がりました！', "FI's Luck rose by 1!", "Lil's Luck rose by 1!"), 'DK4_MES_B82_R0086': ('フェルナンドの運勢が\n１上がりました！', "Fernando's Luck rose by 1!", "Fernando's Luck rose by 1!"), 'DK4_MES_B82_R0102': ('FIの精神が\n１上がりました！', "FI's Spirit rose by 1!", "Lil's Spirit rose by 1!"), 'DK4_MES_B82_R0105': ('フェルナンドの精神が\n１上がりました！', "Fernando's Spirit rose by 1!", "Fernando's Spirit rose by 1!"), 'DK4_MES_B84_R0005': ('ウッキッキーーー！', 'Ook ook ook!', 'Ook ook ook!'), 'DK4_MES_B84_R0013': ('ウッキッキーーー！', 'Ook ook ook!', 'Ook ook ook!'), 'DK4_MES_B84_R0021': ('ウッキッキーーー！', 'Ook ook ook!', 'Ook ook ook!')}
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
        Japanese,logical_expected,expanded_expected=expected_source_and_targets[row['id']]
        assert row['source_Japanese']==Japanese and logical==logical_expected.encode('ascii') and expanded==expanded_expected.encode('ascii')
        assert not Japanese.startswith('＜')
        assert all(c['null_source_actor'] for pipeline in pipelines for c in pipeline['cases'])
        if b'FI' in sourcebody:
            assert sourcebody.count(b'FI')==1 and expanded.startswith(b"Lil's ")
            FI_cases.append(dict(id=row['id'],source_Japanese=Japanese,original_24310_null_actor=True,complete_current_macro_pipelines=pipelines,expanded_hex=expanded.hex(),all8_alignment_cases_Lil_possessive_stat_identity_exact=True))
        target=paint(expanded);assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
        visible=[e for e in target['events'] if e['code']!=32]
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
        assert b':' not in logical and not expanded.startswith(b'\n')
        assert not body.startswith((b'\n',b' '))
        preview=ROOT/(row['id']+'_complete_physical.png');picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in target['physical']]);picture.save(preview);pictures.append((row['id'],picture))
        plane=ROOT/(row['id']+'_complete_logical_228x48.bin');plane.write_bytes(target['logical'])
        cases.append(dict(id=row['id'],encoded_hex=compiled.encoded.hex(),formatted_markup=compiled.formatted_markup,expanded_hex=expanded.hex(),current_native_macro_pipelines=pipelines,
            native_glyphs=target['events'],one_native_page_consumes_complete_target=True,complete_native_independent_plane_and_all_glyphs_and_canaries_equal=True,all_visible_origins_zero_and4rows=True,visible_origins_by_row=origins,
            native_plane=str(plane),native_plane_sha256=sha(target['logical']),whole_physical228x64_plane_sha256=sha(target['physical']),preview=str(preview),preview_sha256=sha(preview.read_bytes()),object_rebindings=target['object_rebindings']))
    assert len(cases)==7 and macro_calls==56 and len(FI_cases)==2 and not ctx.machines
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / FE paper',fill='white');sheet.paste(picture.resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_FE_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'current_FE_macro_font_and_typed_paper_proof.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,current_original_null_actor_macro_alignment_cases=56,
        logical_geometry=[228,48],physical_geometry=[228,64],physical_rows_advance=16,logical_rows_advance=12,current_cold_typed_graphics_object_construction=True,no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter=True,
        all7_one_native_page_consumes_complete_target=True,all7_complete_native_independent_planes_all_glyphs_and_canaries_equal=True,all7_source_unlabeled_stat_notices_and_monkey_calls_preserved=True,source_FI_null_actor_cases=FI_cases,
        four_distinct_source_Luck_Spirit_notices_and_three_monkey_calls_preserved=True,only2_source_FI_macros_preserved_no_invented_labels_or_kinship=True,
        scoped_profile='dk4tool/dialogue/lil_crew_items_profile.py',scoped_profile_sha256=sha(Path('dk4tool/dialogue/lil_crew_items_profile.py').read_bytes()),native_formatter_module='dk4tool/dialogue/lil_crew_items_layout_v2.py',native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_crew_items_layout_v2.py').read_bytes()),
        historical_calibration=calibration,terminology_contract=str(TERMS),terminology_contract_sha256=sha(TERMS.read_bytes()),review_sheets=sheets,visual_review_pending=True,
        dependencies={str(p):sha(p.read_bytes()) for p in [Path('scripts/lil_kuhn_china_FE_painter_v2909.py'),Path('scripts/verify_lil_clifford_north_new_world_FE_v2980.py')]},
        native_macro_context_plan=str(ctx.proof_path),native_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_Crew_Items_IDs=[],new_emulator_runs=0,reference_and_release_still_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Seven FE complete current nativeplanes/56null-actor macro cases;twoFI names/fourstat identities/threeunlabeledmonkey calls preserved. One sheet needs visual review.')
