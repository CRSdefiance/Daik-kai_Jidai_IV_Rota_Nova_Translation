"""Check full original speaker labels and nine Japanese progressive bodies against actual source holds."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.Al_Ferid_name_style_v6520 import native_name_raster,style_source_proof
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_name_catalog_glyphs_v278 import raster as inherited_raster
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_name_source_planes_v6562');INPUT=Path('work/analysis/current_V6541_native_v6549/current_native_input.json');DOC=Path('translations/lil_B211_editorial_manuscript_v1.json');ACTUAL=Path('work/analysis/lil_B211_source_actual_v6561/all12_source_panels_all23_commands_and_observed_return.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);SOURCE=Path(doc['source_context']);NAMES=Path(doc['speaker_name_review']);source,names,actual=map(read,[SOURCE,NAMES,ACTUAL]);assert actual['source_distinct_speech_observations']==12 and names['no_name_asset_change_or_duplicate_dialogue_name_UI_credit'];ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');labels={r['actor_ID']:r['progressive'] for r in names['source_name_fields']};assert labels=={2:'Lil Argot',7:'Cristina Erneco'}
    literals=['Lil Argot','Cristina','Erneco','Cristina Erneco'];alignments=[]
    for ident in [2,7]:
        for text in literals:
            raw=text.encode('ascii');result=ctx.execute(expand,raw,ident);ctx.machines.pop();assert all(r['output_hex']==raw.hex() for r in result['cases']);alignments.append(dict(actor_ID=ident,input_text=text,input_hex=raw.hex(),native=result))
    assert len(alignments)==8 and not ctx.machines;planes=[];sheet=Image.new('RGB',(1024,640),'#263238');draw=ImageDraw.Draw(sheet)
    for index,text in enumerate(literals):
        raw=text.encode('ascii');pixels,events,font=native_name_raster(ctx.arm,raw);assert pixels==expected_pixels(ctx.arm,font,events);emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw) and all(e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        ink={(i%216,i//216) for i,b in enumerate(pixels) if b};width=max(e['x']+6 for e in events);holds=[];differences=[];selected=next((ident for ident,label in labels.items() if label==text),None)
        if selected is not None:
            for panel in actual['speech_observations']:
                if panel['source_selector']!=selected:continue
                for photo in panel['held_captures']:
                    p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');found={(x-4,y) for y in range(13) for x in range(width+8) if im.getpixel((12+x,276+y))==(98,97,98)}
                    if found==ink:holds.append(dict(id=panel['id'],frame=photo['frame'],capture=str(p),sha256=photo['PNG_sha256'],complete_name_and_blank_guards_equal=True))
                    else:differences.append(dict(id=panel['id'],frame=photo['frame'],missing=len(ink-found),extra=len(found-ink)))
            assert holds and not differences
        picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);path=ROOT/f'name_literal{index+1}_complete_style11.png';picture.save(path);y=index*160;draw.text((4,y+3),('actual progressive header' if selected is not None else 'literal name component only')+' '+text,fill='white');sheet.paste(picture.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,y+25));planes.append(dict(text=text,input_hex=raw.hex(),native_events=events,source_owned_zero_ink_flushes=flushes,native_plane_sha256=sha(pixels),preview=str(path),preview_sha256=sha(path.read_bytes()),complete_glyph_sequence_bounds_and_single_row=True,actual_matching_header_holds=holds,actual_header_differences=differences,full_catalogue_UI_unvisited=True))
    sp=ROOT/'two_full_progressive_names_and_two_component_literals.png';sheet.save(sp)
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(inherited_raster.__code__,{**inherited_raster.__globals__,'NdsImage':FontROM},argdefs=inherited_raster.__defaults__);raster.__kwdefaults__=inherited_raster.__kwdefaults__;bodycases=[];consumer=read(doc['current_consumer_proof']);clean_dispatch={r['id']:r for r in consumer['all24_source_current_dispatches'] if r['version']=='clean-Japanese'}
    for row in source['records']:
        if row['source_selector']==254:continue
        body=bytes.fromhex(next(b['text_hex'] for b in clean_dispatch[row['id']]['boundaries'] if b['kind']=='unexecuted-progressive-body'));pixels,events,font=raster(ctx.arm,body);assert pixels==expected_pixels(ctx.arm,font,events);expected={(i%216,i//216) for i,b in enumerate(pixels) if b==1};panel=next(p for p in actual['speech_observations'] if p['id']==row['id']);complete=[];partial=[]
        for photo in panel['held_captures']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');found={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            if found==expected:complete.append(dict(frame=photo['frame'],capture=str(p),sha256=photo['PNG_sha256'],complete_source_native_body_equal=True))
            else:partial.append(dict(frame=photo['frame'],missing=len(expected-found),extra=len(found-expected),incomplete_progressive_frame=True))
        assert complete and panel['selected_capture']['frame'] in [p['frame'] for p in complete];bodycases.append(dict(id=row['id'],source_selector=row['source_selector'],source_template_hex=bytes.fromhex(row['source_hex'])[1:].hex(),expanded_source_hex=body.hex(),native_events=events,native_plane_sha256=sha(pixels),complete_actual_holds=complete,incomplete_progressive_holds=partial))
    assert len(bodycases)==9;fe=[r['source_record_index'] for r in actual['speech_observations'] if r['source_selector']==254];assert fe==[9,17,24]
    save(ROOT/'four_name_planes32_alignments_all_source_headers_nine_Japanese_progressive_body_masks.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),actual_source=str(ACTUAL),actual_source_sha256=sha(ACTUAL.read_bytes()),name_literal_cases=alignments,name_literal_alignment_count=32,original_style11_name_caller=style_source_proof(ctx.arm),name_planes=planes,actual_complete_progressive_name_holds=sum(len(p['actual_matching_header_holds']) for p in planes),source_body_masks=bodycases,all9_selected_Japanese_progressive_bodies_independently_match_native_pixels=True,one_original_source_FI_expansion_included=True,three_actual_FE_source_panels_visually_viewed_indices=fe,independent_Japanese_FE_body_pixel_masks_not_claimed=True,English_FE_all_three_independent_native_planes_bound_separately=True,no_name_asset_change_or_full207_name_approval=True,full_catalogue_UI_unvisited=True,all207_name_role_alias_queue_and_earlier_consumers_open=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,DOC,SOURCE,NAMES,ACTUAL,Path(doc['current_consumer_proof']),Path(__file__),Path('scripts/Al_Ferid_name_style_v6520.py'),Path('scripts/Al_Ferid_font_oracles_v6520.py'),Path('scripts/prove_lil_B208_name_planes_v6405.py')]},full_goal_complete=False));print(dict(name_alignments=32,complete_source_name_holds=sum(len(p['actual_matching_header_holds']) for p in planes),Japanese_progressive_objects=9,complete_Japanese_body_holds=sum(len(p['complete_actual_holds']) for p in bodycases),FE_source_actual_visual_only=fe,no_new_credit=True))
