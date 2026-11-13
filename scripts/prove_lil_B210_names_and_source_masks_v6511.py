"""Verify both progressive names, old/proposed full name literals and every actual Japanese body."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.lil_B207_name_style_v6354d import native_name_raster,style_source_proof
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_name_catalog_glyphs_v278 import raster as inherited_raster
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B210_name_source_planes_v6511');INPUT=Path('work/analysis/current_V6488_native_v6497/current_native_input.json');SOURCE=Path('work/analysis/lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json');NAMES=Path('translations/lil_B210_speaker_name_review_pending_v1.json');ACTUAL=Path('work/analysis/lil_B210_source_actual_v6510/all10_source_panels_all21_commands_and_observed_return.json')
if __name__=='__main__':
    assert not ROOT.exists();source,names,actual=map(read,[SOURCE,NAMES,ACTUAL]);assert actual['source_distinct_speech_observations']==10 and names['no_name_asset_revision_applied'];ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');labels={r['actor_ID']:r['progressive'] for r in names['source_name_fields']};assert labels=={2:'Lil Argot',17:'Al Shin'}
    literals=['Lil Argot','Al Shin','Al Ｆerid Shin','Al Ferid Shin'];alignments=[]
    for ident in [2,17]:
        for text in literals:
            raw=text.encode('cp932');result=ctx.execute(expand,raw,ident);ctx.machines.pop();assert all(r['output_hex']==raw.hex() for r in result['cases']);alignments.append(dict(actor_ID=ident,input_text=text,input_hex=raw.hex(),native=result))
    assert len(alignments)==8 and not ctx.machines;planes=[];sheet=Image.new('RGB',(1024,640),'#263238');draw=ImageDraw.Draw(sheet)
    for index,text in enumerate(literals):
        raw=text.encode('cp932');pixels,events,font=native_name_raster(ctx.arm,raw);assert pixels==expected_pixels(ctx.arm,font,events);emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw)
        assert all(e['y']==0 and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events);ink={(i%216,i//216) for i,b in enumerate(pixels) if b};width=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in events);holds=[];differences=[]
        selected=next((ident for ident,label in labels.items() if label==text),None)
        if selected is not None:
            for panel in actual['speech_observations']:
                if panel['source_selector']!=selected:continue
                for photo in panel['held_captures']:
                    p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');found={(x-4,y) for y in range(13) for x in range(width+8) if im.getpixel((12+x,276+y))==(98,97,98)}
                    if found==ink:holds.append(dict(id=panel['id'],frame=photo['frame'],capture=str(p),sha256=photo['PNG_sha256'],complete_name_and_blank_guards_equal=True))
                    else:differences.append(dict(id=panel['id'],frame=photo['frame'],missing=len(ink-found),extra=len(found-ink)))
            assert holds and not differences
        picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);path=ROOT/f'name_literal{index+1}_complete_style11.png';picture.save(path);y=index*160;draw.text((4,y+3),('actual progressive' if selected is not None else 'full-name literal only;catalogue UI unvisited')+' '+text.encode('ascii','backslashreplace').decode(),fill='white');sheet.paste(picture.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,y+25));planes.append(dict(text=text,input_hex=raw.hex(),native_events=events,source_owned_zero_ink_flushes=flushes,native_plane_sha256=sha(pixels),preview=str(path),preview_sha256=sha(path.read_bytes()),complete_glyph_sequence_bounds_and_single_row=True,actual_matching_header_holds=holds,actual_header_differences=differences,full_catalogue_UI_unvisited=selected is None))
    sp=ROOT/'two_progressive_names_and_old_proposed_full_name_literals.png';sheet.save(sp)
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(inherited_raster.__code__,{**inherited_raster.__globals__,'NdsImage':FontROM},argdefs=inherited_raster.__defaults__);raster.__kwdefaults__=inherited_raster.__kwdefaults__;bodycases=[]
    for row in source['records']:
        body=bytes.fromhex(row['source_hex'])[1:];pixels,events,font=raster(ctx.arm,body);assert pixels==expected_pixels(ctx.arm,font,events);expected={(i%216,i//216) for i,b in enumerate(pixels) if b==1};panel=next(p for p in actual['speech_observations'] if p['id']==row['id']);complete=[];partial=[]
        for photo in panel['held_captures']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');found={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            if found==expected:complete.append(dict(frame=photo['frame'],capture=str(p),sha256=photo['PNG_sha256'],complete_source_native_body_equal=True))
            else:partial.append(dict(frame=photo['frame'],missing=len(expected-found),extra=len(found-expected),incomplete_progressive_frame=True))
        assert complete and panel['selected_capture']['frame'] in [p['frame'] for p in complete];bodycases.append(dict(id=row['id'],source_selector=row['source_selector'],source_hex=body.hex(),native_events=events,native_plane_sha256=sha(pixels),complete_actual_holds=complete,incomplete_progressive_holds=partial))
    save(ROOT/'four_name_planes32_literal_alignments_all_source_headers_and_ten_Japanese_body_masks.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),name_finding=str(NAMES),name_finding_sha256=sha(NAMES.read_bytes()),actual_source=str(ACTUAL),actual_source_sha256=sha(ACTUAL.read_bytes()),name_literal_cases=alignments,name_literal_alignment_count=32,original_style11_name_caller=style_source_proof(ctx.arm),name_planes=planes,actual_complete_progressive_name_holds=sum(len(p['actual_matching_header_holds']) for p in planes),source_body_masks=bodycases,all10_selected_Japanese_bodies_independently_match_native_pixels=True,old_fullwidth_F_and_proposed_ASCII_Ferid_literal_glyphs_safe_in_current_renderer=True,proposed_name_asset_and_target_full_catalogue_getter_not_yet_modified_or_executed=True,full_catalogue_UI_unvisited=True,source_English_name_asset_unchanged=True,all207_name_role_alias_queue_and_earlier_consumers_open=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,SOURCE,NAMES,ACTUAL,Path(__file__),Path('scripts/lil_B207_name_style_v6354d.py'),Path('scripts/shady_man_font_oracles_v6263.py'),Path('scripts/prove_lil_B208_name_planes_v6405.py')]},full_goal_complete=False));print('Two progressive names/all actual source headers,old/proposed full-name literals,32 macro alignments andall10 Japanese body masks pass. Name asset and target full-catalogue consumer remain pending;zero credit.')
