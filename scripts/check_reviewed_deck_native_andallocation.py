"""Check fresh Deck glyphs and disclose the actual current pool's four-byte shortfall."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.deck_explanation_release import format_paragraph
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_arm9_text import components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.execute_scene_caption_raster import execute
from scripts.probe_deck_explanation_layout import geometry
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels

ROOT=Path('work/analysis/Shared_Deck_native_andallocation_20261104')
REVIEW=Path('work/analysis/Shared_Deck_tutorials_contextual_20261104/four_panel_contextual_review_v1.json')
HISTORY=Path('work/analysis/deck_explanations_pool_proof.json')
RELEASE=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0);review,history=map(load,[REVIEW,HISTORY])
    assert review['runtime']==ctx.receipt();start,end=history['source_span'];assert end-start==540
    references=[];fields={r['owner_offset']:r for r in history['references']};assert len(fields)==31
    for name,_,raw in components(ctx.image):
        references.extend((name,at,value-BASE) for at in range(len(raw)-3) if start<=(value:=struct.unpack_from('<I',raw,at)[0])-BASE<end)
    current=[]
    for old in history['moves']:
        ref=fields[old['old_offset']];assert ref['component']=='arm9' and ref['interior_byte_offset']==0
        at=struct.unpack_from('<I',ctx.arm,ref['field_offset'])[0]-BASE
        raw=ctx.arm[at:ctx.arm.index(0,at)];text=raw.decode('cp932')
        current.append(dict(source_owner_offset=old['old_offset'],current_offset=at,reference=ref,text=text,raw_hex=raw.hex(),
            historical_proof_text=old['complete_text'],historical_proof_offset=old['new_offset']))
    expected=[('arm9',r['reference']['field_offset'],r['current_offset']) for r in sorted(current,key=lambda r:r['reference']['field_offset'])]
    assert references==expected
    packed=bytearray();proposed=bytearray();rows={r['offset']:r for r in review['records']}
    for owner in current:
        assert owner['current_offset']==start+len(packed)
        raw=bytes.fromhex(owner['raw_hex'])+b'\0';packed.extend(raw);packed.extend(b'\0'*(-len(packed)%4))
        replacement=format_paragraph(rows[owner['source_owner_offset']]['english'].removesuffix('{PAD}')).encode('cp932')+b'\0' if owner['source_owner_offset'] in rows else raw
        owner['proposed_offset_without_allocation_approval']=start+len(proposed)
        owner['proposed_raw_hex_without_NUL']=replacement[:-1].hex()
        proposed.extend(replacement);proposed.extend(b'\0'*(-len(proposed)%4))
    assert bytes(packed)==ctx.arm[start:end] and len(packed)==540 and len(proposed)==544
    ROOT.mkdir();sheet=Image.new('RGB',(672,656),'white');draw=ImageDraw.Draw(sheet);cases=[]
    dims=geometry(ctx.arm);assert dims['dimensions']==[168,84]
    for index,row in enumerate(review['records']):
        english=row['english'].removesuffix('{PAD}');formatted=format_paragraph(english)
        if row['decision']=='retention':assert formatted==row['current_stored_text']
        for mode in (4,16):
            native=execute(ctx.arm,formatted,tracking=0,x=0,y=0,mode=mode,surface_size=(168,84),deck=True)
            events=[e for e in native['glyph_events'] if e['code']!=32]
            assert [e['code'] for e in events]==[ord(c) for c in english if c!=' ']
            assert all(e['x']>=0 and e['x']+6<=168 and e['y']>=0 and e['y']+12<=36 for e in events)
            assert native['actual_tracking']==0 and native['pixels']==expected_pixels(ctx.arm,b'',native['glyph_events'],mode,background=9)
            cursor=0
            for word in english.split():
                assert len({e['y'] for e in events[cursor:cursor+len(word)]})==1;cursor+=len(word)
            path=ROOT/(row['id']+'_'+str(mode)+'.bin');path.write_bytes(native['pixels'])
            cases.append(dict(id=row['id'],mode=mode,logical_English=english,formatted=formatted,pixels=str(path),pixels_sha256=sha(native['pixels']),
                complete_leading_internal_trailing_glyphs_words_bounds_andindependent_font_pixels_pass=True,
                glyph_events=native['glyph_events'],executed_offsets=native['executed_offsets'],actual_tracking=native['actual_tracking']))
            if mode==16:
                pic=Image.new('RGB',(256,192));pic.putdata([(255,255,255) if c==9 else (128,128,128) if c==14 else (0,0,0) for c in struct.unpack('<49152H',native['pixels'])])
                draw.text((8,index*164+2),row['id'].removeprefix('DECK_EXPLANATION_'),fill='black')
                sheet.paste(pic.crop((0,0,168,36)).resize((672,144),Image.Resampling.NEAREST),(0,index*164+20))
    png=ROOT/'four_current_consumer_native_panels.png';sheet.save(png)
    save(ROOT/'native_andallocation.json',dict(runtime=ctx.receipt(),review=str(REVIEW),review_sha256=sha(REVIEW.read_bytes()),geometry=dims,cases=cases,
        complete_current_source_owned_pool_inventory=current,complete_current_pointer_inventory=references,
        old_historical_pool_is_not_current=True,old_history_full_pool_equality_guard_correctly_rejected=True,
        original_owned_span=[start,end],current_used_bytes=540,proposed_needed_bytes=544,allocation_shortfall_bytes=4,
        accepted_Refit_alignment_andSpritsail_andall27_neighbour_labels_preserved=True,
        current_ARM9_andall_ROM_bytes_not_modified=True,proposed_data_not_written_to_ROM=True,
        all_four_panels_native_glyphs_andwords_bounds_andpixels_pass=True,three_retained_panels_current_wraps_exact=True,
        review_sheet=dict(path=str(png),sha256=sha(png.read_bytes()),panels=4),direct_visual_review_pending=True,
        source_owned_storage_solution_andconnected_target_consumers_andactual_gameplay_pending=True,
        no_ROM_created=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REVIEW,HISTORY,RELEASE,STARTUP,Path(__file__)]}))
    print('Four native Deck panels/eight mode cases pass;current accepted pool540/proposed544:four-byte allocation issue remains,no ROM changed.')
