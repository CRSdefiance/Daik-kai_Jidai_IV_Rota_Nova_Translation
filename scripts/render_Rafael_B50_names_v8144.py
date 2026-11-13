"""Review three B50 progressive names and a disclosed synthetic Camille full getter using exact prior literal cases."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as name_source
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_name_review_assets_v8144')
PROOF=Path('work/analysis/Rafael_B50_source_name_planes_v8142/28_complete_source_pages3_names0_fresh12_reused_literal_alignments.json')
NAMES=Path('work/analysis/Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json')
OLD=Path('work/analysis/Rafael_B49_name_review_assets_v8094b/review_sheet_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();proof,names,old=map(read,[PROOF,NAMES,OLD]);assert len(proof['name_planes'])==3
    image=NdsImage.open(proof['candidate']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==proof['ARM9_sha256']
    se={**name_source.__dict__,'CURRENT_ARM9':sha(arm)};exec(compile(proof['source_owned_name_style_adapter'],__file__+'::style11','exec'),se)
    exec(compile(proof['source_owned_header_raster'],__file__+'::current-native-raster','exec'),se)
    fields=next(r for r in names['complete_clean_andcurrent_name_fields'] if r['actor_ID']==9)
    full=next(r for r in fields['original_getters'] if r['consumer']=='full-catalogue');raw=bytes.fromhex(full['text_hex']);assert raw==b'Camille Marinus Overijssel'
    prior=next(e for e in old['entries'] if e['actor_ID']==9 and e.get('synthetic_full_getter_text_in_original_name_style_only'))
    pixels,events,font=se['native_name_raster'](arm,raw);assert pixels==expected_pixels(arm,font,events)
    visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
    assert prior['text']==full['text'] and prior['input_hex']==raw.hex() and prior['events']==events and prior['original_zero_ink_flushes']==flushes
    assert pixels==Path(prior['native_plane']).read_bytes() and sha(pixels)==prior['native_plane_sha256']
    assert len(prior['native_alignment']['cases'])==4 and all(c['output_hex']==raw.hex() for c in prior['native_alignment']['cases'])
    synthetic=deepcopy(prior);synthetic.update(reused_exact_full_getter_literal_alignment=True,prior_synthetic_proof=str(OLD),prior_synthetic_proof_sha256=sha(OLD.read_bytes()),
        current_code_font_literal_text_fields_andwhole_actor_controls_bound_by_source_proof=str(PROOF))
    entries=[dict(r,scope='progressive getter / original style11') for r in proof['name_planes']]+[dict(synthetic,scope='FULL GETTER / synthetic style11, not catalogue UI')]
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(912,320),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(entries):
        data=Path(r['native_plane']).read_bytes();assert len(data)==216*64 and sha(data)==r['native_plane_sha256']
        im=Image.new('RGB',(216,64));im.putdata([(98,97,98) if v else (250,245,223) for v in data]);x,y=i%2*456,i//2*160
        draw.text((x+3,y+3),f"Actor{r['actor_ID']} {r['text']}",fill='white');draw.text((x+3,y+16),r['scope'],fill='white');sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x,y+32))
    path=ROOT/'three_progressive_names_one_synthetic_full_getter.png';sheet.save(path)
    save(ROOT/'review_sheet_receipt.json',dict(source=str(PROOF),source_sha256=sha(PROOF.read_bytes()),native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),entries=entries,
        sheet=str(path),sheet_sha256=sha(path.read_bytes()),three_progressive_literal_cases_bound=12,synthetic_full_getter_literal_cases_fresh=0,synthetic_full_getter_literal_cases_exact_reused=4,
        current_full_getter_raster_executed_andmatches_exact_prior_independent_glyph_masks=True,
        no_repeated_literal_alignment_execution_for_known_unchanged_names=True,
        all_original_complete_first_internal_final_glyph_masks_andbounds_exact=True,
        actual_progressive_nameplates_catalogue_UI_custom_names_andfull207_review_still_pending=True,visual_review_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PROOF,NAMES,OLD,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Three complete progressive names/one synthetic Camille full getter;12+4exact literal cases reused. Actual B50 nameplates/catalogue/custom names unclaimed;sheet needs direct view.')
