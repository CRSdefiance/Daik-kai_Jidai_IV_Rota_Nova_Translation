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
ROOT=Path('work/analysis/Rafael_B47_pages_v7985')
PLAN=Path('work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json')
LOGICAL=Path('work/analysis/Rafael_B47_logical_v7983/15_logical_paragraphs60_original_native_progressive_alignments.json')
MANUSCRIPT=Path('translations/rafael_B47_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json')
PRIOR=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,logical,doc,names,prior=map(read,[PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and not plan['failures']
    warnings=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert warnings==[
        dict(id='DK4_MES_B47_R0005',issue=dict(code='weak-line-ending',message="line 2 ends with weak wrap word 'to'",severity='warning')),
        dict(id='DK4_MES_B47_R0063',issue=dict(code='weak-line-ending',message="line 2 ends with weak wrap word 'with'",severity='warning'))]
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
        assert prefix in [0,4,5,6] and encoded[0]==prefix and body and b'\0' not in body and b'%' not in body
        assert not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
        result=ctx.execute(env['expand'],body,prefix);ctx.machines.pop()
        assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
        assert ' '.join(body.decode('ascii').split())==row['english'] and all(t not in body for t in [b'FI',b'FA',b'FO'])
        rendered=pe['pages'](arm,font,body)
        assert rendered['complete_consumed_bytes']==len(body) and len(rendered['pages'])==p['expected_native_pages']
        assert p['expected_native_pages']==(2 if row['source_record_index']==53 else 1)
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'))
            path=ROOT/(row['id']+f'_page{page["page"]}.bin');path.write_bytes(pixels)
            segment=body[page['start']:page['end']];leading=len(segment)-len(segment.lstrip(b' '))
            assert leading==(0 if page['page']==1 else 1) and page['first_visible_origin']==[6*leading,0]
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
            page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
                first_visible_origin_matches_original_return_andguard=True)
            pictures.append((row['id']+f' p{page["page"]}',picture))
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=47,source_record_index=row['source_record_index'],
            source_selector=prefix,kind='progressive',compiled_hex=encoded.hex(),expanded_native_hex=body.hex(),
            logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,**rendered))
        print('PAGE_PASS',row['id'],len(rendered['pages']),flush=True)
    assert len(rows)==15 and not ctx.machines and sum(len(r['pages']) for r in rows)==16
    r53=next(r for r in rows if r['source_record_index']==53)
    assert r53['pages'][0]['consumed_hex'].endswith(b"That's Pasha's territory.\n".hex())
    assert bytes.fromhex(r53['pages'][1]['consumed_hex']).startswith(b' If they target us,')
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1320,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(label,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*440,n//3*160;draw.text((x+3,y+3),label+' offline native',fill='white')
            sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Rafael_B47_native_pages_sheet{start//6+1:02d}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'15_complete_native_paragraphs16_pages60_compiled_alignments.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=rows,fresh_compiled_alignment_cases=60,progressive_alignment_cases=60,FE_null_actor_alignment_cases=0,
        complete_progressive_paragraphs=15,complete_progressive_pages=16,
        all_complete_first_internal_final_characters_native_independent_glyph_planes_bounds_andconsumption_exact=True,
        R53_two_original_four_row_pages_sentence_boundary_then_complete_conditional_clause=True,
        all_words_punctuation_andzero_macros_preserved_without_shortening=True,
        source00_actor_only_in_complete_preamble_body_NUL_guard_unchanged=True,
        all_original_base_QA_diagnostics_preserved=True,unapproved_exact_ordinary_boundary_warnings=warnings,
        warning_waivers_not_yet_authored_orapproved=True,review_sheets=sheets,visual_review_pending=True,
        source_owned_progressive_page_adapter=page_adapter,source_owned_progressive_macro_adapter=logical['source_owned_progressive_adapter'],
        all15_formatting_gates_false=True,native_name_planes_stored_controls_actual_pagination_policy_andregistered_release_pending=True,
        ordinary_captain0_context_no_state_fixture=True,new_emulator_runs=0,new_credit=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOGICAL,MANUSCRIPT,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('15 complete native paragraphs/16 pages/60 alignments;allglyphs/bounds pass.Two exact warnings retained forindividual review;actual R53 page-turn pending.')
