"""Bind seven name literals, four progressive planes and the source's actually selected style4 bodies."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.lil_B207_name_style_v6354d import native_name_raster,style_source_proof
from scripts.prove_lil_B208_name_planes_v6405 import original_name_events
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_name_planes_v6464')
INPUT=Path('work/analysis/current_V6439_native_v6449/current_native_input.json')
NAMES=Path('work/analysis/lil_B209_names_v6455b/four_source_or_fallback_names_eight_getters_full_signature_and_exact_fields.json')
SOURCE=Path('work/analysis/lil_B209_source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json')
ACTUAL=Path('work/analysis/lil_B209_source_actual_v6456/six_actual_panels24_visited_of27_stored_commands_and_honest_conditional_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();names,source,actual=map(read,[NAMES,SOURCE,ACTUAL]);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    labels={r['actor_ID']:r['progressive'] for r in names['source_name_fields']};assert labels=={2:'Lil Argot',11:'Jam Ludwyan',12:'Yukihisa Shiraki',151:'Sailor'}
    literals=sorted({r[k] for r in names['source_name_fields'] for k in ['progressive','catalogue']});assert len(literals)==7
    assert ctx.rom.read_file('/GRP/KANJI.FNT')==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    cases=[]
    for ident in labels:
        for value in literals:
            result=ctx.execute(expand,value.encode('ascii'),ident);ctx.machines.pop();assert all(bytes.fromhex(c['output_hex'])==value.encode('ascii') for c in result['cases']);cases.append(dict(actor_ID=ident,literal=value,native=result))
    assert len(cases)==28 and not ctx.machines
    planes=[];sheet=Image.new('RGB',(1024,640),'#263238');draw=ImageDraw.Draw(sheet)
    for index,(ident,label) in enumerate(labels.items()):
        raw=label.encode('ascii');pixels,events,font=native_name_raster(ctx.arm,raw);assert pixels==expected_pixels(ctx.arm,font,events);codes,flushes=original_name_events(events,raw);assert codes==list(raw)
        assert all(e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        ink={(i%216,i//216) for i,b in enumerate(pixels) if b};width=max(e['x']+6 for e in events);holds=[];differences=[];samples=[]
        for panel in actual['actual_panel_observations']:
            selected=151 if panel['source_selector']==208 else panel['source_selector']
            if selected!=ident:continue
            for photo in panel['held_captures']:
                p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');found={(x-4,y) for y in range(13) for x in range(width+8) if im.getpixel((12+x,276+y))==(98,97,98)}
                if found==ink:holds.append(dict(id=panel['id'],frame=photo['frame'],capture=str(p),sha256=photo['PNG_sha256'],complete_label_and_blank_guards_equal=True))
                else:differences.append(dict(id=panel['id'],frame=photo['frame'],missing=len(ink-found),extra=len(found-ink)))
            samples.append(panel['selected_capture'])
        assert not differences
        path=ROOT/f'actor{ident}_complete_style11_native_name.png';picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);picture.save(path)
        y=index*160;draw.text((3,y+3),f'Actor{ident} {label}; '+('source header observed' if samples else 'Jam branch unvisited: native plane only'),fill='white');sheet.paste(picture.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(3,y+24))
        if samples:
            image=Image.open(samples[0]['path']).convert('RGB').crop((8,272,160,291));sheet.paste(image.resize((608,76),Image.Resampling.NEAREST),(3,y+90))
        planes.append(dict(actor_ID=ident,label=label,native_glyph_events=events,only_owned_zero_ink_flush_spaces=flushes,complete_native_plane_sha256=sha(pixels),preview=str(path),preview_sha256=sha(path.read_bytes()),actual_matching_header_holds=holds,actual_header_mask_differences=differences,unvisited_actual_header=not samples,complete_leading_internal_final_glyphs_and_bounds=True))
    sp=ROOT/'all_four_native_names_and_three_actual_source_headers.png';sheet.save(sp)
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    styles=[]
    for at in [8,702]:
        row=next(r for r in source['typed_actor_style_records'] if r['command_offset']==at and r['style_indices']==[4]);body=bytes.fromhex(row['source_hex']);pixels,events,font=raster(ctx.arm,body);assert pixels==expected_pixels(ctx.arm,font,events)
        expected={(i%216,i//216) for i,b in enumerate(pixels) if b==1};panel=next(p for p in actual['actual_panel_observations'] if p['interval']['source_offset']==at);complete=[];partial=[]
        for photo in panel['held_captures']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');found={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            if found==expected:complete.append(dict(frame=photo['frame'],capture=str(p),sha256=photo['PNG_sha256'],whole_native_style4_body_equal=True))
            else:partial.append(dict(frame=photo['frame'],missing=len(expected-found),extra=len(found-expected),progressive_not_yet_complete=True))
        assert complete and panel['selected_capture']['frame'] in [p['frame'] for p in complete]
        styles.append(dict(id=row['id'],source_command_offset=at,source_style_index=4,source_hex=body.hex(),native_glyph_events=events,native_plane_sha256=sha(pixels),complete_actual_body_holds=complete,incomplete_progressive_holds=partial,unvisited_other_source_styles_not_claimed=True))
    save(ROOT/'four_name_planes112_alignments_actual_headers_and_two_source_style4_masks.json',dict(candidate=str(ctx.rompath),candidate_sha256=ctx.doc['current_ROM_sha256'],source_name_proof=str(NAMES),source_name_proof_sha256=sha(NAMES.read_bytes()),literal_macro_cases=cases,native_name_literal_alignment_cases=112,source_current_style11_caller=style_source_proof(ctx.arm),planes=planes,actual_source_style4_complete_body_masks=styles,all_other_13_stored_style_bodies_not_actual_gameplay=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,all_original_name_characters_complete_in_bounds_and_all_headers_match=True,Jam_R65_actual_header_not_visited=True,proper_names_contextually_retained_no_asset_change=True,actor151_progressive_Sailor_catalogue_Retainer_consumer_difference_not_global_editorial_approval=True,full_catalogue_UI_unvisited_and_full_name_getters_bound_separately=True,all207_names_aliases_and_older_consumers_still_open=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,NAMES,SOURCE,ACTUAL,Path(__file__)]},full_goal_complete=False))
    print('Four complete native name planes,112 literal alignments,all actual source headers and two independently identified source style4 bodies pass;Jam branch remains unvisited.')
