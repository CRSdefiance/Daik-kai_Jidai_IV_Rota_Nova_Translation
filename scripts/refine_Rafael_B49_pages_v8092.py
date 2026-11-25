"""Recheck only five changed paragraphs;reuse56 exact native proofs andreplace five sheets."""
from copy import deepcopy
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
ROOT=Path('work/analysis/Rafael_B49_pages_refined_v8092')
OLD=Path('work/analysis/Rafael_B49_pages_v8091/61_complete_native_paragraphs61_pages244_compiled_alignments.json')
PLAN=Path('work/analysis/Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json')
LOGICAL=Path('work/analysis/Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json')
DOC=Path('translations/rafael_B49_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();old,plan,logical,doc,names=map(read,[OLD,PLAN,LOGICAL,DOC,NAMES]);prior_plan=Path(old['plan']);before=read(prior_plan)
    assert sha(prior_plan.read_bytes())==old['plan_sha256'] and not plan['failures']
    assert plan['manuscript_sha256']==old['manuscript_sha256']==logical['manuscript_sha256']==sha(DOC.read_bytes())
    changed=[p['id'] for p,q in zip(plan['records'],before['records'],strict=True) if p['encoded_hex']!=q['encoded_hex']]
    assert changed==['DK4_MES_B49_R0043','DK4_MES_B49_R0142','DK4_MES_B49_R0213','DK4_MES_B49_R0244','DK4_MES_B49_R0405']
    assert all(len(p['lines'])==len(q['lines']) and p['expected_native_pages']==q['expected_native_pages']==1 for p,q in zip(plan['records'],before['records'],strict=True))
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==old['candidate_sha256']==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT');assert sha(arm)==old['ARM9_sha256'] and sha(font)==old['font_sha256']
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(old['source_owned_progressive_page_adapter'],__file__+'::exact-native-pages','exec'),pe)
    ne=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::original-macros','exec'),ne)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context');rows=[];reused=[];fresh=[]
    for row,p,previous in zip(doc['records'],plan['records'],old['records'],strict=True):
        assert row['id']==p['id']==previous['id']
        if row['id'] not in changed:
            assert p['encoded_hex']==previous['compiled_hex'] and p['formatted_markup']==previous['formatted_markup']
            for page in previous['pages']:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] and sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            value=deepcopy(previous);value.update(reused_exact_native_compiled_record=True,prior_native_proof=str(OLD),prior_native_proof_sha256=sha(OLD.read_bytes()));rows.append(value);reused.append(row['id']);continue
        encoded=bytes.fromhex(p['encoded_hex']);body=encoded[1:];prefix=row['source_selector']
        assert prefix==encoded[0] and prefix in [2,8] and row['kind']=='progressive' and b'\0' not in body
        assert all(m not in body for m in [b'FI',b'FA',b'FO',b'%'])
        result=ctx.execute(ne['expand'],body,prefix);ctx.machines.pop()
        assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
        assert ' '.join(body.decode('ascii').split())==row['english']
        rendered=pe['pages'](arm,font,body);assert rendered['complete_consumed_bytes']==len(body) and len(rendered['pages'])==p['expected_native_pages']==1
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(row['id']+'_page1.bin');path.write_bytes(pixels);assert page['first_visible_origin']==[0,0]
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
            page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),first_visible_origin_matches_original_return_andguard=True)
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=49,source_record_index=row['source_record_index'],source_selector=prefix,kind='progressive',compiled_hex=encoded.hex(),expanded_native_hex=body.hex(),
            logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,reused_exact_native_compiled_record=False,**rendered));fresh.append(row['id'])
    assert not ctx.machines and len(rows)==61 and len(reused)==56 and fresh==changed
    groups=sorted({i//6 for i,r in enumerate(rows) if r['id'] in changed});assert len(groups)==5
    sheets=deepcopy(old['review_sheets']);superseded=[]
    for group in groups:
        sheet=Image.new('RGB',(1320,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,row in enumerate(rows[group*6:group*6+6]):
            page=row['pages'][0];picture=Image.open(page['preview']).convert('RGB');x,y=n%3*440,n//3*160
            draw.text((x+3,y+3),row['id']+' p1 offline native',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Rafael_B49_native_pages_sheet{group+1:02d}_final.png';sheet.save(path);superseded.append(sheets[group]);sheets[group]=dict(path=str(path),sha256=sha(path.read_bytes()))
    warnings=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert [r['id'] for r in warnings]==['DK4_MES_B49_R0213','DK4_MES_B49_R0244','DK4_MES_B49_R0405']
    out=deepcopy(old);out.update(plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),records=rows,prior_native_proof=str(OLD),prior_native_proof_sha256=sha(OLD.read_bytes()),
        fresh_compiled_alignment_cases=20,reused_compiled_alignment_cases=224,total_bound_compiled_alignment_cases=244,fresh_progressive_alignment_cases=20,reused_progressive_alignment_cases=224,
        progressive_alignment_cases=244,exact_reused_compiled_records=reused,fresh_changed_compiled_records=fresh,review_sheets=sheets,prior_superseded_review_sheets=superseded,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),unapproved_exact_ordinary_boundary_warnings=warnings,
        five_phrase_refinements_no_added_rows_pages_orprose_change=True,no_repeated_native_execution_for56_exact_records=True,new_sheets_visual_review_pending=True)
    out['evidence']=dict(out['evidence'])|{str(p):sha(p.read_bytes()) for p in [OLD,PLAN,LOGICAL,DOC,NAMES,Path(__file__)]}
    save(ROOT/'61_final_native_pages20_fresh224_reused_alignments.json',out)
    save(ROOT/'rejected_extra_article_phrase_priority_andguard_capacity_note.json',dict(
        final_plan=str(PLAN),final_plan_sha256=sha(PLAN.read_bytes()),preserved_experimental_plan='work/analysis/Rafael_B49_layout_v8090d/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json',
        finding='The d experiment moved the R244 break between Head/west to avoid a weaker article boundary;retain c,which keeps Head west andthe New World intact with a reviewed to/the boundary.',
        unrepresentable_alternative_row='Head west to the New World, or solve',ASCII_cells=36,nonfinal_phase_repair_cells=1,continuation_guard_cells=1,total_cells=38,available_cells=36,
        do_not_drop_words_add_rows_orweaken_native_guard_to_force_the_alternative=True,
        all_prior_plans_andnative_proofs_preserved=True,new_credit=0,full_goal_complete=False))
    print('FinalB49:61native pages,20fresh/224exactreused alignments;five updated sheets need direct view. Three original weak-ending diagnostics retained;formatting still pendingactual/release.')
