"""Five complete native dialogue pages with independent glyph masks and all QA retained."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_pages_v8206')
PLAN=Path('work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json')
LOGICAL=Path('work/analysis/Gerhard_logical_v8204/5_logical_paragraphs20_original_native_alignments.json')
MANUSCRIPT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
NAMES=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')
PRIOR=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')

if __name__=='__main__':
    assert not ROOT.exists();plan,logical,doc,names,prior=map(read,[PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and not plan['failures']
    warnings=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert not any(i['severity']=='error' for r in plan['records'] for i in r['base_QA']['issues'])
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    page_adapter=prior['source_owned_2b6_page_adapter'];pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(page_adapter,__file__+'::exact-current-progressive-pages','exec'),pe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];pictures=[]
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['kind']=='progressive'
        encoded=bytes.fromhex(p['encoded_hex']);prefix=row['source_selector'];body=encoded[1:]
        assert prefix in [1,9,16] and encoded[0]==prefix and body and b'\0' not in body and b'%' not in body
        assert not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
        result=ctx.execute(expand,body,prefix);ctx.machines.pop()
        expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        assert ' '.join(expected.decode('ascii').split())==row['english'].replace('{MACRO:FI}','Lil')
        assert b'FO' not in body and b'FA' not in body and body.count(b'FI')==int(row['block']==74 and row['source_record_index']==185)
        rendered=pe['pages'](arm,font,expected)
        assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==p['expected_native_pages']==1
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'))
            path=ROOT/(row['id']+f'_page{page["page"]}.bin');path.write_bytes(pixels)
            segment=expected[page['start']:page['end']];leading=len(segment)-len(segment.lstrip(b' '))
            assert leading==(0 if page['page']==1 else 1) and page['first_visible_origin']==[6*leading,0]
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
            page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
                first_visible_origin_matches_original_return_andguard=True)
            pictures.append((row['id']+f' p{page["page"]}',picture))
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],
            source_selector=prefix,kind='progressive',compiled_hex=encoded.hex(),expanded_native_hex=expected.hex(),logical_English=row['english'],
            formatted_markup=p['formatted_markup'],native_alignment=result,**rendered))
        print('PAGE_PASS',row['id'],len(rendered['pages']),flush=True)
    assert len(rows)==5 and not ctx.machines and sum(len(r['pages']) for r in rows)==5
    sheet=Image.new('RGB',(1320,320),'#263238');draw=ImageDraw.Draw(sheet)
    for n,(label,picture) in enumerate(pictures):
        x,y=n%3*440,n//3*160;draw.text((x+3,y+3),label+' offline native',fill='white')
        sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    path=ROOT/'Gerhard_five_native_pages.png';sheet.save(path)
    save(ROOT/'5_complete_native_paragraphs5_pages20_compiled_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,fresh_compiled_alignment_cases=20,progressive_alignment_cases=20,FE_null_actor_alignment_cases=0,
        complete_progressive_paragraphs=5,complete_progressive_pages=5,
        all_complete_first_internal_final_characters_native_independent_glyph_planes_bounds_andconsumption_exact=True,
        all5_single_original_four_row_pages_complete=True,all_words_punctuation_source_FI1_preserved_without_shortening=True,
        all_original_base_QA_diagnostics_preserved=True,unapproved_exact_ordinary_boundary_warnings=warnings,
        no_warnings_andno_warning_waivers_needed=not warnings,exact_warning_review_pending=bool(warnings),
        review_sheets=[dict(path=str(path),sha256=sha(path.read_bytes()))],visual_review_pending=True,
        source_owned_progressive_page_adapter=page_adapter,source_owned_progressive_macro_adapter=logical['source_owned_progressive_adapter'],
        all5_formatting_gates_false=True,native_target_name_planes_stored_controls_actual_andregistered_release_pending=True,
        ordinary_captain2_context_no_state_fixture=True,new_emulator_runs=0,new_credit=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('5 complete native paragraphs/5 pages/20 alignments;all glyphs and bounds pass;visual review pending.')
