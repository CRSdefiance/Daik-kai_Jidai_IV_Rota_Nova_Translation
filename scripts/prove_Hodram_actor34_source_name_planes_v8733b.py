"""Paint both actual clean-getter strings using unchanged native name style/font."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B207_name_style_v6354d as style
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_actor34_source_name_planes_v8733b')
SOURCE=Path('work/analysis/Hodram_actor34_clean_name_composition_v8732/clean_source_full_andprogressive_name_composition.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);current=read(source['current_two_getters_andtwo_nameplanes_reused_from'])
    image=NdsImage.open(current['candidate']);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');digest=sha(arm)
    assert sha(Path(current['candidate']).read_bytes())==source['current_candidate_sha256']==current['candidate_sha256']
    assert image.read_file('/GRP/KANJI.FNT')==clean.read_file('/GRP/KANJI.FNT')
    caller=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':digest},argdefs=style.style_source_proof.__defaults__)
    raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':caller},argdefs=style.native_name_raster.__defaults__)
    pixels,unused_factory,oracle=bind(image);ROOT.mkdir(parents=True);rows=[];pictures=[]
    for r in source['source_native_getters']:
        raw=bytes.fromhex(r['text_hex']);plane,events,font=raster(arm,raw)
        assert font==image.read_file('/GRP/KANJI.FNT') and plane==pixels(arm,font,events)
        assert [e['code'] for e in events]==codes(raw)
        assert all(e['kind']=='cp932' and e['style']==11 and (e['x'],e['y'])==((i%18)*12,(i//18)*16) and e['x']+12<=216 and e['y']+13<=64 for i,e in enumerate(events))
        assert len(events)==len(raw)//2 and len(events)==(13 if r['consumer']=='progressive-nameplate' else 19)
        assert max(e['x']+12 for e in events)==min(216,12*len(events))
        path=ROOT/(r['consumer']+'.bin');path.write_bytes(plane)
        pic=Image.new('RGB',(216,64));pic.putdata([(98,97,98) if v else (250,245,223) for v in plane]);preview=path.with_suffix('.png');pic.save(preview)
        rows.append(dict(consumer=r['consumer'],text=r['text'],input_hex=raw.hex(),native_glyph_events=events,width_px=min(216,12*len(events)),literal_advance_px=12*len(events),rows=1+(len(events)-1)//18,native_plane=str(path),native_plane_sha256=sha(plane),
            preview=str(preview),preview_sha256=sha(preview.read_bytes()),all_complete_first_internal_final_glyphs_native_andindependent_pixels_in_bounds=True))
        pictures.append((r['consumer']+' clean literal',pic))
    for r in current['fresh_actor34_name_planes']:
        assert sha(Path(r['native_plane']).read_bytes())==r['native_plane_sha256'] and sha(Path(r['preview']).read_bytes())==r['preview_sha256']
        pictures.append((r['text']+' exact prior current literal',Image.open(r['preview']).convert('RGB')))
    sheet=Image.new('RGB',(912,320),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,pic) in enumerate(pictures):
        x,y=i%2*456,i//2*160;draw.text((x+3,y+3),label+' offline native',fill='white');sheet.paste(pic.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    sheetfile=ROOT/'clean_andcurrent_two_name_consumers.png';sheet.save(sheetfile)
    save(ROOT/'source_complete_names_andcurrent_reuse.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),candidate=current['candidate'],candidate_sha256=current['candidate_sha256'],ARM9_sha256=digest,
        source_name_planes=rows,reused_current_name_planes=current['fresh_actor34_name_planes'],whole_clean_current_font_exact=True,original_style11_caller=caller(arm),font_oracle_binding=oracle,
        review_sheet=dict(path=str(sheetfile),sha256=sha(sheetfile.read_bytes())),direct_view_pending=True,
        full_getter_literal_native_plane_not_actual_catalogue_UI_orline_width_measurement=True,
        source_full_literal_19th_character_wraps_to_row2_under_this216px_test_consumer=True,
        preserved_stopped_one_row_assumption='scripts/prove_Hodram_actor34_source_name_planes_v8733.py',
        original_metrics_font_guard_andcomplete_glyph_requirements_unchanged=True,no_actual_gameplay_orall207_name_claim=True,
        no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(source['current_two_getters_andtwo_nameplanes_reused_from']),Path(__file__)]}))
    print('Both clean-getter literals:',[(r['text'],r['width_px']) for r in rows],flush=True)
    print('Complete native/independent source glyphs pass;prior current planes reused exactly. Direct view andeditorial name decision pending.',flush=True)
