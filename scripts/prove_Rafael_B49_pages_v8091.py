"""Complete original native progressive pages with independent glyph masks andunaltered QA."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_pages_v8091')
PLAN=Path('work/analysis/Rafael_B49_layout_v8090/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json')
LOGICAL=Path('work/analysis/Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json')
MANUSCRIPT=Path('translations/rafael_B49_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
PRIOR=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,logical,doc,names,prior=map(read,[PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and not plan['failures']
    warnings=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert not warnings
    assert not any(i['severity']=='error' for r in plan['records'] for i in r['base_QA']['issues'])
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    page_adapter=prior['source_owned_2b6_page_adapter'];pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(page_adapter,__file__+'::exact-current-progressive-pages','exec'),pe)
    env=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::original-progressive-processing','exec'),env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];pictures=[]
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['kind']=='progressive'
        encoded=bytes.fromhex(p['encoded_hex']);prefix=row['source_selector'];body=encoded[1:]
        assert prefix in [0,2,4,5,6,8,9] and encoded[0]==prefix and body and b'\0' not in body and b'%' not in body
        assert not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
        result=ctx.execute(env['expand'],body,prefix);ctx.machines.pop()
        expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        assert ' '.join(expected.decode('ascii').split())==row['english'].replace('{MACRO:FI}','Rafael')
        assert all(t not in body for t in [b'FA',b'FO']) and body.count(b'FI')==int(row['source_record_index'] in [311,388])
        rendered=pe['pages'](arm,font,expected)
        assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==p['expected_native_pages']
        assert p['expected_native_pages']==1
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
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=49,source_record_index=row['source_record_index'],
            source_selector=prefix,kind='progressive',compiled_hex=encoded.hex(),expanded_native_hex=expected.hex(),
            logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,**rendered))
        print('PAGE_PASS',row['id'],len(rendered['pages']),flush=True)
    assert len(rows)==61 and not ctx.machines and sum(len(r['pages']) for r in rows)==61
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1320,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(label,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*440,n//3*160;draw.text((x+3,y+3),label+' offline native',fill='white')
            sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Rafael_B49_native_pages_sheet{start//6+1:02d}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'61_complete_native_paragraphs61_pages244_compiled_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,fresh_compiled_alignment_cases=244,progressive_alignment_cases=244,FE_null_actor_alignment_cases=0,
        complete_progressive_paragraphs=61,complete_progressive_pages=61,
        all_complete_first_internal_final_characters_native_independent_glyph_planes_bounds_andconsumption_exact=True,
        all61_single_original_four_row_pages_complete=True,
        all_words_punctuation_andtwo_source_FI_macros_preserved_without_shortening=True,
        source00_actor_only_in_complete_preamble_body_NUL_guard_unchanged=True,
        all_original_base_QA_diagnostics_preserved=True,unapproved_exact_ordinary_boundary_warnings=warnings,
        no_warnings_andno_warning_waivers_needed=True,review_sheets=sheets,visual_review_pending=True,
        source_owned_progressive_page_adapter=page_adapter,source_owned_progressive_macro_adapter=logical['source_owned_progressive_adapter'],
        all61_formatting_gates_false=True,native_name_planes_stored_controls_actual_pagination_policy_andregistered_release_pending=True,
        ordinary_captain0_context_no_state_fixture=True,new_emulator_runs=0,new_credit=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('61complete native paragraphs/61pages/244alignments;allglyphs/bounds pass.Zero warnings;eleven sheets need direct viewing,actual/stored/release pending.')
