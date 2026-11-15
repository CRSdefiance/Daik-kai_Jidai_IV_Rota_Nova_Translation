"""Fresh compiled alignments and native independent full-page glyph proofs for67 speeches."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_pages_v7794')
PLAN=Path('work/analysis/maria_confrontation_layout_v7793/16_automatic_full_width_plans_all_base_QA_preserved.json')
MANUSCRIPT=Path('translations/maria_B36_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json')
PRIOR=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,doc,names,prior=map(read,[PLAN,MANUSCRIPT,NAMES,PRIOR])
    assert plan['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and not plan['failures'] and not any(i['severity'] in ['warning','error'] for p in plan['records'] for i in p['base_QA']['issues'])
    im=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=im.read_file('/__arm9__.bin'),im.read_file('/GRP/KANJI.FNT')
    page_adapter=prior['source_owned_2b6_page_adapter'];pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(page_adapter,__file__+'::exact-current-native-page-renderer','exec'),pe)
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==3'})
    env=dict(expand.__globals__);exec(compile(adapter,__file__+'::Maria-compiled-alignments','exec'),env)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];pictures=[]
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'];encoded=bytes.fromhex(p['encoded_hex']);body=encoded[1:];prefix=row['source_selector']
        assert encoded[0]==prefix and prefix in names['exact_static_source_selectors'] and body and not body.endswith(b'\n') and b'\0' not in body
        result=ctx.execute(env['expand'],body,prefix);ctx.machines.pop()
        expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        prose=row['english'].replace('FI','Maria').replace('FA','Li').replace('FO','Li Clan')
        assert ' '.join(expected.decode('cp932').split())==prose
        rendered=pe['pages'](arm,font,expected)
        assert len(rendered['pages'])==p['expected_native_pages'] and rendered['complete_consumed_bytes']==len(expected)
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(row['id']+f'_page{page["page"]}.bin');path.write_bytes(pixels)
            segment=expected[page['start']:page['end']];leading=len(segment)-len(segment.lstrip(b' '))
            assert leading==(0 if page['page']==1 else 1) and page['first_visible_origin']==[6*leading,0]
            if page['page']>1:assert expected[page['start']-1:page['start']]==b'\n'
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
            page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
                compiler_owned_continuation_guard_bytes=leading,first_visible_origin_matches_original_return_andguard=True,
                native_preview_shade_not_actual_CP932_scene_palette_claim=True)
            pictures.append((row['id']+f' p{page["page"]}',picture))
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=prefix,
            compiled_hex=p['encoded_hex'],expanded_native_hex=expected.hex(),logical_English=row['english'],formatted_markup=p['formatted_markup'],
            native_alignment=result,**rendered))
        print('PAGE_PASS',row['id'],len(rendered['pages']),flush=True)
    assert len(rows)==16 and not ctx.machines and sum(len(r['pages']) for r in rows)==sum(p['expected_native_pages'] for p in plan['records'])
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(label,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),label+' native offline',fill='white')
            sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Maria_story_native_pages_sheet{start//6+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'16_compiled64_alignments_complete_native_pages.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,fresh_compiled_alignment_cases=64,fresh_complete_native_page_renders=sum(len(r['pages']) for r in rows),
        all_first_internal_final_visible_codes_in_order=True,all_independent_glyph_planes_bounds_input_bitmap_headers_canaries_andconsumption_exact=True,
        compiler_owned_page2_guard_preserved_not_prose_padding=True,native_four_row_pagination_not_actual_button_orwhole_scene=True,
        review_sheets=sheets,visual_review_pending=True,source_owned_compiled_macro_adapter=adapter,source_owned_native_page_adapter=page_adapter,
        all16_formatting_gates_false=True,stored_wholecontrols_sourcebranches_actual_policy_production_andregistered_release_pending=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,new_emulator_runs=0,new_credit=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,MANUSCRIPT,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('PASS:16compiled paragraphs/64fresh alignments/all planned native complete pages. Visual,stored,wholecontrols,actual andintegration stillpending.')
