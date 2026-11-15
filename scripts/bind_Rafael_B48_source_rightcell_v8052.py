"""Bind one original Japanese nineteenth-cell question mark; do not widen English rules."""
from copy import deepcopy
from types import FunctionType
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts import square_shopkeeper_font_oracles_v7020 as oracle
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_source_rightcell_v8052')
PRIOR=Path('work/analysis/Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json')
ACTUAL=Path('work/analysis/Rafael_B48_actual_v8051b/paired_source_English_observed_path_complete_pages_names_andR347_transition.json')
TERMINAL=Path('work/analysis/Rafael_B48_scene_runs_v8050/route0_clean_Japanese/terminal.json')
ID='DK4_MES_B48_R0129'
if __name__=='__main__':
    assert not ROOT.exists();prior,audit,terminal=map(read,[PRIOR,ACTUAL,TERMINAL]);assert len(audit['unresolved'])==1 and audit['unresolved'][0]['id']==ID
    report=read(terminal['report']);photo=next(p for p in report['frames_captured'] if p['frame']==7330);assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
    im=Image.open(photo['path']).convert('RGB');source=next(r for r in prior['source_records'] if r['id']==ID);assert len(source['pages'])==1
    oldplane=Path(source['pages'][0]['native_plane']).read_bytes();assert sha(oldplane)==source['pages'][0]['native_plane_sha256']
    expected216={(i%216,i//216) for i,b in enumerate(oldplane) if b==1}
    actual216={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
    missing=expected216-actual216;extra=actual216-expected216;assert len(missing)==14 and not extra
    observed_right={(x-16,y-296) for y in range(296,360) for x in range(232,244) if im.getpixel((x,y))==(0,8,0)}
    assert observed_right=={(x+216,y-16) for x,y in missing}
    armim=NdsImage.open(prior['candidate']);arm,font=armim.read_file('/__arm9__.bin'),armim.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==prior['ARM9_sha256'] and sha(font)==prior['font_sha256']
    # Only this original-source oracle uses the measured nineteen complete12px cells.
    # Both executable functions are unchanged; WIDTH is an isolated scratch-canvas input.
    independent=FunctionType(oracle._expected.__code__,{**oracle._expected.__globals__,'WIDTH':228},argdefs=oracle._expected.__defaults__)
    independent.__kwdefaults__=oracle._expected.__kwdefaults__
    def expected_wide(arm,font,events):
        assert sha(arm)==prior['ARM9_sha256']
        return independent(arm,font,events)
    adapter=checked_text(prior['source_owned_page_adapter'],{"e['x']+(6 if e['kind']=='ascii' else 12)<=216":"e['x']+(6 if e['kind']=='ascii' else 12)<=228"})
    ns={**old_pages.__globals__,'WIDTH':228,'expected_pixels':expected_wide,'codes':codes}
    exec(compile(adapter,__file__+'::single-clean-source-nineteenth-cell-plane','exec'),ns)
    body=bytes.fromhex(source['original_current_expanded_source_hex']);rendered=ns['pages'](arm,font,body);assert len(rendered['pages'])==1
    page=rendered['pages'][0];pixels=bytes.fromhex(page.pop('native_plane_hex'));assert len(pixels)==228*64
    black={(i%228,i//228) for i,b in enumerate(pixels) if b==1};gray={(i%228,i//228) for i,b in enumerate(pixels) if b==15}
    actualblack={(x-16,y-296) for y in range(296,360) for x in range(16,244) if im.getpixel((x,y))==(0,8,0)}
    actualgray={(x-16,y-296) for y in range(296,360) for x in range(16,244) if im.getpixel((x,y))==(197,198,197)}
    assert black==actualblack and gray==actualgray
    oldevents=source['pages'][0]['events'];events=page['events'];assert len(events)==len(oldevents)
    changes=[dict(index=i,before=a,actual_matched_after=b) for i,(a,b) in enumerate(zip(oldevents,events,strict=True)) if a!=b]
    assert len(changes)==1 and changes[0]['before']['kind']=='cp932' and changes[0]['before']['code']==changes[0]['actual_matched_after']['code']==0x8148
    assert (changes[0]['before']['x'],changes[0]['before']['y'])==(0,32) and (changes[0]['actual_matched_after']['x'],changes[0]['actual_matched_after']['y'])==(216,16)
    ROOT.mkdir(parents=True);path=ROOT/'B48_R129_complete_original_source_228_cellspan.bin';path.write_bytes(pixels)
    preview=Image.new('RGB',(228,64));colors={0:(239,232,201),1:(0,8,0),15:(197,198,197)};preview.putdata([colors[b] for b in pixels]);png=path.with_suffix('.png');preview.save(png)
    page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),native_viewport_width=228,
        measured_source_glyph_cellspan_not_global_English_geometry=True)
    doc=deepcopy(prior);r=next(r for r in doc['source_records'] if r['id']==ID)
    for key,value in rendered.items():r[key]=deepcopy(value)
    r.update(original216_page_model_reference=source,source_only_actual_nineteenth_cell_bound=True)
    doc.update(previous_source_font_proof=str(PRIOR),previous_source_font_proof_sha256=sha(PRIOR.read_bytes()),
        source_only_original_CP932_R129_nineteenth_cell_actual_position_proved=True,
        no_English_font_geometry_profile_compiled_prose_guard_orROM_change=True,
        specific_source_position_difference=changes,source_only_page_adapter=adapter,source_only_canvas_width=228,
        actual_black_andCP932_gray_full_masks_exact_for_frame7330=True,
        source_glyph_cellspan_not_claimed_whole_engine_constructor_width=True,
        original_failed_source216_audit_andall_capture_proofs_preserved=True)
    out=ROOT/'91_source_native_pages9_name_planes_R129_actual_rightcell_bound.json';save(out,doc)
    save(ROOT/'source_question_mark_actual_position_binding.json',dict(
        source_font=str(PRIOR),source_font_sha256=sha(PRIOR.read_bytes()),corrected_source_font=str(out),corrected_source_font_sha256=sha(out.read_bytes()),
        original_audit=str(ACTUAL),original_audit_sha256=sha(ACTUAL.read_bytes()),actual_capture=photo,
        missing_in216_model=sorted(missing),actual_visible_nineteenth_cell_black_pixels=sorted(observed_right),
        final_source_CP932_question_mark_code=0x8148,source_original_actual_cell_origin=[216,16],old216_oracle_origin=[0,32],
        all_other_glyph_positions_codes_andshapes_unchanged=True,
        independent_andoriginal_native_source_raster_black_gray_bounds_codes_canaries_andconsumption_pass=True,
        complete_source_glyph_was_visible_not_missing_ortruncated=True,
        only_this_clean_source_paragraph_uses_measured228px_glyph_cellspan=True,
        English216px_safe_geometry_all91_compiled_stored_bytes_andall48_parity_tails_unchanged=True,
        source_only_geometry_finding_retained_for_later_older_record_technical_reaudit=True,
        no_new_ROM_capture_orcredit=True,evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,ACTUAL,TERMINAL,Path(__file__)]},full_goal_complete=False))
    print('R129original question mark iscomplete atsource cell19(216,16);single-source native228-cellspan plane matches actual black andgray exactly.Allother glyphs andEnglish216geometry unchanged.')
