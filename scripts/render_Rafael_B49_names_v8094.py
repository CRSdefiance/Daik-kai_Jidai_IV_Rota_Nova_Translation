"""Seven progressive names andtwo disclosed synthetic full-name strings;catalogue UI still untested."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as name_source
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_name_review_assets_v8094')
PROOF=Path('work/analysis/Rafael_B49_source_name_planes_v8093/61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json')
NAMES=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
OLD=Path('work/analysis/Rafael_B48_name_review_assets_v8039/review_sheet_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();proof,names,old=map(read,[PROOF,NAMES,OLD]);assert len(proof['name_planes'])==7
    image=NdsImage.open(proof['candidate']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==proof['ARM9_sha256']
    se={**name_source.__dict__,'CURRENT_ARM9':sha(arm)};exec(compile(proof['source_owned_name_style_adapter'],__file__+'::style11','exec'),se)
    exec(compile(proof['source_owned_header_raster'],__file__+'::original-raster','exec'),se)
    ne=dict(expand.__globals__);exec(compile(proof['source_owned_macro_adapter'],__file__+'::original-literals','exec'),ne)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context');synthetics=[]
    for actor in [8,9]:
        full=next(r for r in names['native_fourteen_progressive_andfull_getters']['rows'] if r['actor_ID']==actor and r['consumer']=='full-catalogue');raw=bytes.fromhex(full['text_hex'])
        assert raw==(b'Arcadius Eirene Eudoxios' if actor==8 else b'Camille Marinus Overijssel')
        pixels,events,font=se['native_name_raster'](arm,raw);assert pixels==expected_pixels(arm,font,events)
        visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
        if actor==8:
            prior=next(e for e in old['entries'] if e.get('synthetic_full_getter_text_in_original_name_style_only'))
            assert prior['text']==full['text'] and prior['input_hex']==raw.hex() and prior['events']==events
            assert pixels==Path(prior['native_plane']).read_bytes() and sha(pixels)==prior['native_plane_sha256']
            synthetic=deepcopy(prior);synthetic.update(reused_exact_full_getter_literal_alignment=True,prior_synthetic_proof=str(OLD),prior_synthetic_proof_sha256=sha(OLD.read_bytes()),current_code_font_literal_text_andactor_controls_bound_by_source_proof=str(PROOF))
        else:
            result=ctx.execute(ne['expand'],raw,actor);ctx.machines.pop();assert len(result['cases'])==4 and all(c['output_hex']==raw.hex() for c in result['cases'])
            p=ROOT/'Camille_full_getter_synthetic_style11.bin';p.write_bytes(pixels)
            synthetic=dict(actor_ID=actor,text=full['text'],input_hex=raw.hex(),native_plane=str(p),native_plane_sha256=sha(pixels),events=events,native_alignment=result,
                original_zero_ink_flushes=flushes,original_pair_flush_width=(len(raw)+1)//2*12,reused_exact_full_getter_literal_alignment=False,
                actual_catalogue_UI_style_geometry_bounds_andscene_NOT_proved=True,synthetic_full_getter_text_in_original_name_style_only=True)
        synthetics.append(synthetic)
    assert not ctx.machines
    entries=[dict(**r,scope='progressive getter / original style11') for r in proof['name_planes']]+[dict(**s,scope='FULL GETTER / synthetic style11, not catalogue UI') for s in synthetics]
    sheet=Image.new('RGB',(1368,480),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(entries):
        pixels=Path(r['native_plane']).read_bytes();assert len(pixels)==216*64 and sha(pixels)==r['native_plane_sha256']
        im=Image.new('RGB',(216,64));im.putdata([(98,97,98) if v else (250,245,223) for v in pixels]);x,y=i%3*456,i//3*160
        draw.text((x+3,y+3),f"Actor{r['actor_ID']} {r['text']}",fill='white');draw.text((x+3,y+16),r['scope'],fill='white');sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x,y+32))
    out=ROOT/'seven_progressive_names_two_synthetic_full_getters.png';sheet.save(out)
    save(ROOT/'review_sheet_receipt.json',dict(source=str(PROOF),source_sha256=sha(PROOF.read_bytes()),native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),entries=entries,
        sheet=str(out),sheet_sha256=sha(out.read_bytes()),seven_progressive_literal_cases_bound=28,synthetic_full_getter_literal_cases_fresh=4,synthetic_full_getter_literal_cases_exact_reused=4,
        all_original_complete_first_internal_final_glyph_masks_andbounds_exact=True,actual_progressive_nameplates_catalogue_UI_custom_names_andfull207_review_still_pending=True,
        visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [PROOF,NAMES,OLD,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Seven progressive names/two synthetic full-getter strings;Camille4fresh/Arcadius4reused literal cases. Actual catalogue UI unclaimed;name sheet needs view.')
