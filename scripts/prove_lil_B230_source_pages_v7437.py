"""Measure every complete original phoenix-bascinet-callback page and its exact native glyph sequence."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.research_lil_B209_native_pages_v6461 import pages as inherited_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B230_source_pages_v7437')
SOURCE=Path('work/analysis/lil_B230_source_v7428/seventeen_clean_current_phoenix_bascinet_callback_source_references.json')
PRIOR=Path('work/analysis/lil_B222_native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);prior=read(PRIOR);image=NdsImage.open(source['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==source['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    adapter=checked_text(prior['source_owned_2b6_page_adapter'],{"all(0<=e['x']<=210 and e['y'] in [0,16,32,48] for e in visible)":"all(0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 and e['y'] in [0,16,32,48] for e in visible)","[v for v in text if v not in [32,10]]":"[v for v in codes(text) if v not in [32,10]]"})
    env={**inherited_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(adapter,__file__+'::original-complete-CP932-pages','exec'),env)
    ROOT.mkdir(parents=True);rows=[];pictures=[]
    for row in source['records']+source['typed_actor_style_records']:
        raw=bytes.fromhex(row['source_hex']);body=raw[1:] if row['kind']=='progressive' else raw;assert not any(v in body for v in [b'FI',b'FA',b'FO'])
        result=env['pages'](arm,font,body)
        for page in result['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));p=ROOT/(row['id']+'_page'+str(page['page'])+'.bin');p.write_bytes(pixels);im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};im.putdata([colors[v] for v in pixels]);png=p.with_suffix('.png');im.save(png)
            page.update(native_plane=str(p),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()));pictures.append((row['id'],page['page'],im))
        rows.append(dict(id=row['id'],source_kind=row['kind'],source_selector=row['source_selector'],source_reference=row['source_reference'],source_body_hex=body.hex(),complete_CP932_and_ASCII_codes=codes(body),**result))
    assert len(rows)==17 and all(r['pages'] for r in rows)
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1296,308),'#263238');draw=ImageDraw.Draw(sheet)
        for index,(ident,page,im) in enumerate(pictures[start:start+6]):
            x,y=index%3*432,index//3*154;draw.text((x+2,y+2),ident+' source page'+str(page),fill='white');sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        p=ROOT/f'complete_source_pages_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all17_clean_objects_complete_native_CP932_pages_and_exact_consumption.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=rows,complete_objects=17,complete_native_pages=len(pictures),physical_viewport=[216,64],original_four_rows_per_page=True,all_leading_internal_final_CP932_and_ASCII_codes_complete_in_order=True,all_independent_native_font_planes_bounds_canaries_and_consumption_exact=True,source_original_page_counts={r['id']:len(r['pages']) for r in rows},all_original_Japanese_spacing_preserved_as_source_evidence_not_English_authoring=True,source_owned_CP932_page_adapter=adapter,all_native_instruction_constants_and_geometry_unchanged=True,review_sheets=sheets,visual_review_pending=True,offline_source_pages_not_actual_A_button_or_unvisited_conditional_coverage=True,no_ROM_or_font_or_current_English_or_editorial_credit_mutation=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,PRIOR,Path(inherited_pages.__code__.co_filename),Path('scripts/square_shopkeeper_font_oracles_v7020.py'),Path(__file__)]},full_goal_complete=False))
    print(dict(source_objects=17,native_pages=len(pictures),page_counts=[len(r['pages']) for r in rows],credit=0))
