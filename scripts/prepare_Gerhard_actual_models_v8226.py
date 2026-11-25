"""Exact native models for five old bodies, five reviewed revised bodies and three relevant headers."""
from copy import deepcopy
from types import FunctionType
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as style
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_actual_models_v8226')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
NATIVE=Path('work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json')
EFFECTIVE=Path('work/analysis/Gerhard_surname_effective_v8201/all5_effective_English_templates10_original_dispatches_no_FE.json')
STORED=Path('work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json')
NAMES=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')
OWN_NAMES=Path('work/analysis/Gerhard_research_startup_view_v8219/own_research_startup6_RGBpairs_actor_equal8_fresh_getters_direct_view.json')
NAME_PLANES=Path('work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json')
if __name__=='__main__':
    assert not ROOT.exists();reference,native,effective,stored,names,own,prior_planes=map(read,[REFERENCE,NATIVE,EFFECTIVE,STORED,NAMES,OWN_NAMES,NAME_PLANES])
    assert stored['native_viewed_proof_sha256']==sha(NATIVE.read_bytes()) and reference['full_ROM_inverse_recovers_every_parent_byte']
    image,target=NdsImage.open(reference['parent']),NdsImage.open(reference['research_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==native['ARM9_sha256'] and font==target.read_file('/GRP/KANJI.FNT')
    field=reference['only_changed_name_span'];targetarm=target.read_file('/__arm9__.bin');inverse=bytearray(targetarm);inverse[field['offset']:field['offset']+12]=bytes.fromhex(field['current_hex']);assert bytes(inverse)==arm
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::unchanged-current-painter','exec'),pe)
    ROOT.mkdir(parents=True);pictures=[];parent_rows=[]
    for row in effective['effective_current_records']:
        raw=bytes.fromhex(row['current_actual_default_expanded_hex']);rendered=pe['pages'](arm,font,raw)
        assert rendered['complete_consumed_bytes']==len(raw) and len(rendered['pages'])==1
        for page in rendered['pages']:
            plane=bytes.fromhex(page.pop('native_plane_hex'));p=ROOT/(row['id']+'_parent_page1.bin');p.write_bytes(plane)
            preview=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};preview.putdata([colors[v] for v in plane]);png=p.with_suffix('.png');preview.save(png)
            page.update(native_plane=str(p),native_plane_sha256=sha(plane),preview=str(png),preview_sha256=sha(png.read_bytes()));pictures.append((row['id']+' previous English',preview))
        parent_rows.append(dict(id=row['id'],block=row['block'],source_selector=row['source_selector'],expanded_native_hex=raw.hex(),**rendered))
    revised_rows=deepcopy(native['records'])
    for row in revised_rows:
        s=next(r for r in stored['records'] if r['id']==row['id']);row['expanded_stored_hex']=s['expanded_stored_hex']
        for page in row['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
    style_proof=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(arm)},argdefs=style.style_source_proof.__defaults__)
    raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':style_proof},argdefs=style.native_name_raster.__defaults__)
    old_values={r['actor_ID']:r['text'] for r in names['native_eight_progressive_andfull_getters']['rows'] if r['consumer']=='progressive-nameplate'}
    new_values={r['actor_ID']:r['text'] for r in own['native_eight_getters_from_actual_own_research_snapshot']['rows'] if r['consumer']=='progressive-nameplate'}
    headers={v:[] for v in ['parent_English','revised_English']};fresh_headers=[]
    for actor in [1,9,16]:
        for version,values in [('parent_English',old_values),('revised_English',new_values)]:
            text=values[actor];raw=text.encode('ascii')
            if actor==16:
                label='before-current-header' if version=='parent_English' else 'proposed-header-and-full-getter'
                p=next(r for r in prior_planes['planes'] if r['label']==label);assert p['text']==text
                plane=Path(p['native_plane']).read_bytes();assert sha(plane)==p['native_plane_sha256']
                result=dict(actor_ID=actor,text=text,native_plane=p['native_plane'],native_plane_sha256=p['native_plane_sha256'],
                    original_pair_flush_width=p['native_width_including_flush_space'],exact_reused_name_plane=True,reuse_proof=str(NAME_PLANES))
            elif version=='revised_English':
                old=next(h for h in headers['parent_English'] if h['actor_ID']==actor);assert old['text']==text;result=deepcopy(old);result['exact_reused_name_plane']=True
            else:
                plane,events,actualfont=raster(arm,raw);assert actualfont==font and plane==expected_pixels(arm,font,events)
                emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw)
                assert all(e['y']==0 and e['style']==11 and 0<=e['x'] and e['x']+6<=216 for e in events)
                p=ROOT/f'actor{actor}_unchanged_header.bin';p.write_bytes(plane)
                picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if v else (250,245,223) for v in plane]);png=p.with_suffix('.png');picture.save(png);pictures.append((text+' unchanged header',picture))
                result=dict(actor_ID=actor,text=text,native_plane=str(p),native_plane_sha256=sha(plane),native_glyph_events=events,source_owned_final_zero_ink_flushes=flushes,
                    original_pair_flush_width=max(e['x']+6 for e in events),exact_reused_name_plane=False,preview=str(png),preview_sha256=sha(png.read_bytes()))
                fresh_headers.append(actor)
            headers[version].append(result)
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1320,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(label,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*440,n//3*160;draw.text((x+3,y+3),label+' offline native',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        p=ROOT/f'previous_bodies_andunchanged_headers_sheet{start//6+1:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'five_previous_body_planes_revised_exact_reuses_three_header_consumers.json',dict(
        parent=reference['parent'],parent_sha256=reference['parent_sha256'],research_ROM=reference['research_ROM'],research_ROM_sha256=reference['research_ROM_sha256'],
        oracle_ARM9=reference['current_ARM9_sha256'],target_same_complete_code_font_outside_owned12_byte_name_byinverse=True,
        native_models=dict(parent_English=parent_rows,revised_English=revised_rows),name_planes=headers,
        fresh_previous_body_native_pages=5,revised_complete_native_page_reuses=5,fresh_header_actors=fresh_headers,reused_Gerhard_before_after_planes=2,
        current_body_expansions_bound_to_original_dispatch_not_assumed_Lil_macro_width=True,
        all_complete_first_internal_final_glyph_planes_bounds_consumption_andname_flushes_pass=True,
        no_extra_native_macro_alignment_cases_ornew_prose_approvals_claimed=True,source_owned_page_adapter=native['source_owned_progressive_page_adapter'],
        original_style11_caller_proof=style_proof(arm),review_sheets=sheets,visual_review_pending=True,
        actual_header_body_selection_pagination_andtransitions_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,NATIVE,EFFECTIVE,STORED,NAMES,OWN_NAMES,NAME_PLANES,Path(__file__)]}))
    print('5previous body pages/5exact revised page reuses/3header consumers prepared;2new unchangedheader planes,2Gerhard exactreuses;actual comparison pending.')
