"""Measure full-width-F compatibility and complete current names;never normalize name bytes."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_name_planes_v6354b')
INPUT=Path('work/analysis/current_V6327_native_v6337/current_native_input.json')
NAMES=Path('work/analysis/lil_B207_source_names_v6341/two_exact_source_name_fields_voices_and_distinct_name_consumers.json')
ACTUAL=Path('work/analysis/lil_B207_source_actual_v6347/all13_source_speeches_all24_commands_and_complete_return.json')
def codes(raw):
    result=[];i=0
    while i<len(raw):
        if raw[i]<128:result.append(raw[i]);i+=1
        else:result.append(int.from_bytes(raw[i:i+2],'little'));i+=2
    return result
if __name__=='__main__':
    assert not ROOT.exists();names,actual=map(read,[NAMES,ACTUAL]);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');cases=[]
    for ident in [2,14]:
        for text in ['Ｆerog','Emilio Ｆerog','Ferog','Emilio Ferog']:
            value=ctx.execute(expand,text.encode('cp932'),ident);ctx.machines.pop();cases.append(dict(source_selector=ident,input_text=text,input_hex=text.encode('cp932').hex(),native=value,all_four_outputs=[bytes.fromhex(r['output_hex']).decode('cp932') for r in value['cases']]))
    assert not ctx.machines and all(c['all_four_outputs']==[c['input_text']]*4 for c in cases if 'Ｆ' in c['input_text'])
    labels={r['actor_ID']:r['progressive'] for r in names['source_name_fields']};assert labels=={2:'Lil Argot',14:'Emilio Ｆerog'};planes=[];sheet=Image.new('RGB',(1024,320),'#263238');draw=ImageDraw.Draw(sheet);evidence={str(p):sha(p.read_bytes()) for p in [INPUT,NAMES,ACTUAL,Path(__file__),Path('scripts/shady_man_font_oracles_v6263.py'),Path('scripts/generic_name_macro_owned_v5886b.py')]}
    for row,ident in enumerate([2,14]):
        raw=labels[ident].encode('cp932');pixels,events,font=raster(ctx.arm,raw);expected=expected_pixels(ctx.arm,font,events);assert pixels==expected
        emitted=[e['code'] for e in events];original=codes(raw);assert emitted in [original,original+[32]]
        assert len({e['y'] for e in events})==1 and all(0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 and e['y']==0 for e in events)
        width=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in events);ink={(i%216,i//216) for i,b in enumerate(pixels) if b};assert ink and max(y for x,y in ink)<13
        holds=[];differences=[]
        for speech in actual['speech_observations']:
            if speech['source_selector']!=ident:continue
            for photo in speech['held_captures']:
                p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');found={(x-4,y) for y in range(13) for x in range(width+8) if pic.getpixel((12+x,276+y))==(98,97,98)}
                if found==ink:holds.append(dict(id=speech['id'],frame=photo['frame'],capture=str(p),capture_sha256=photo['PNG_sha256'],all_complete_native_name_glyphs_and_blank_guards_equal=True))
                else:differences.append(dict(id=speech['id'],frame=photo['frame'],missing_pixels=len(ink-found),extra_pixels=len(found-ink)))
        preview=Image.new('RGB',(216,64),'#faf5df');preview.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);p=ROOT/f'actor{ident}_complete_name_native_plane.png';preview.save(p)
        sample=next(s['selected_capture'] for s in actual['speech_observations'] if s['source_selector']==ident);pic=Image.open(sample['path']).convert('RGB');actual_strip=pic.crop((8,272,120,291));draw.text((4,row*152+3),f'Actor{ident}: native complete label; actual caption below',fill='white');sheet.paste(preview.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,row*152+22));sheet.paste(actual_strip.resize((448,76),Image.Resampling.NEAREST),(4,row*152+90))
        planes.append(dict(actor_ID=ident,label=labels[ident],raw_hex=raw.hex(),native_glyph_events=events,source_character_codes=original,only_original_implicit_trailing_space_allowed=True,complete_native_plane_sha256=sha(pixels),preview=str(p),preview_sha256=sha(p.read_bytes()),native_width_including_flush_space=width,complete_leading_internal_final_glyphs_and_one_row_in_bounds=True,independent_current_ASCII_and_CP932_pixels_equal=True,actual_matching_header_holds=holds,actual_header_mask_differences=differences))
    p=ROOT/'both_complete_native_names_and_actual_headers.png';sheet.save(p)
    save(ROOT/'two_complete_native_names32_literal_macro_alignments_and_actual_headers.json',dict(candidate=str(ctx.rompath),candidate_sha256=ctx.doc['current_ROM_sha256'],native_input=str(INPUT),native_input_sha256=sha(INPUT.read_bytes()),literal_macro_cases=cases,native_macro_alignment_cases=32,current_fullwidth_F_literal_outputs_exact=True,plain_ASCII_F_literal_output_comparisons_measured_not_assumed=True,planes=planes,review_sheet=dict(path=str(p),sha256=sha(p.read_bytes())),complete_current_native_planes_equal_independent_font_models=True,source_current_name_fields_and_four_consumers_unchanged=True,no_name_item_or_ROM_bytes_changed=True,actual_name_pixel_review_pending=any(r['actual_header_mask_differences'] for r in planes),proper_name_retention_and_visual_approval_pending=True,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all_original_macro_canaries_actor_RNG_and_unowned4MiB_exact=True,all207_name_role_alias_queue_and_full_editorial_goal_open=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence=evidence,full_goal_complete=False))
    print(dict(macro_alignment_cases=32,literal_outputs=[(c['source_selector'],c['input_text'],c['all_four_outputs']) for c in cases],headers=[(r['actor_ID'],len(r['actual_matching_header_holds']),len(r['actual_header_mask_differences'])) for r in planes]))
