"""Recheck five changed B50 paragraphs;reuse23 exact native proofs andreplace four sheets."""
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
ROOT=Path('work/analysis/Rafael_B50_pages_refined_v8143')
OLD=Path('work/analysis/Rafael_B50_pages_v8141/28_complete_native_paragraphs28_pages112_compiled_alignments.json')
PLAN=Path('work/analysis/Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json')
LOGICAL=Path('work/analysis/Rafael_B50_logical_v8139/28_logical_paragraphs112_original_native_alignments_no_FE.json')
DOC=Path('translations/rafael_B50_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json')
if __name__=='__main__':
    assert not ROOT.exists();old,plan,logical,doc,names=map(read,[OLD,PLAN,LOGICAL,DOC,NAMES]);prior_plan=Path(old['plan']);before=read(prior_plan)
    assert sha(prior_plan.read_bytes())==old['plan_sha256'] and not plan['failures']
    assert plan['manuscript_sha256']==old['manuscript_sha256']==logical['manuscript_sha256']==sha(DOC.read_bytes())
    changed=[p['id'] for p,q in zip(plan['records'],before['records'],strict=True) if p['encoded_hex']!=q['encoded_hex']]
    assert changed==['DK4_MES_B50_R0049','DK4_MES_B50_R0069','DK4_MES_B50_R0103','DK4_MES_B50_R0108','DK4_MES_B50_R0114']
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
        assert prefix==encoded[0] and prefix in [0,2,9] and row['kind']=='progressive' and b'\0' not in body
        assert b'%' not in body
        for token in [b'FI',b'FA',b'FO']:assert body.count(token)==bytes.fromhex(row['source_hex'])[1:].count(token)
        expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        result=ctx.execute(ne['expand'],body,prefix);ctx.machines.pop()
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        assert ' '.join(expected.decode('ascii').split())==row['english'].replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')
        rendered=pe['pages'](arm,font,expected);assert rendered['complete_consumed_bytes']==len(expected) and len(rendered['pages'])==p['expected_native_pages']==1
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(row['id']+'_page1.bin');path.write_bytes(pixels);assert page['first_visible_origin']==[0,0]
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
            page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),first_visible_origin_matches_original_return_andguard=True)
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=50,source_record_index=row['source_record_index'],source_selector=prefix,kind='progressive',compiled_hex=encoded.hex(),expanded_native_hex=expected.hex(),
            logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,reused_exact_native_compiled_record=False,**rendered));fresh.append(row['id'])
    assert not ctx.machines and len(rows)==28 and len(reused)==23 and fresh==changed
    groups=sorted({i//6 for i,r in enumerate(rows) if r['id'] in changed});assert len(groups)==4
    sheets=deepcopy(old['review_sheets']);superseded=[]
    for group in groups:
        sheet=Image.new('RGB',(1320,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,row in enumerate(rows[group*6:group*6+6]):
            page=row['pages'][0];picture=Image.open(page['preview']).convert('RGB');x,y=n%3*440,n//3*160
            draw.text((x+3,y+3),row['id']+' p1 offline native',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Rafael_B50_native_pages_sheet{group+1:02d}_final.png';sheet.save(path);superseded.append(sheets[group]);sheets[group]=dict(path=str(path),sha256=sha(path.read_bytes()))
    warnings=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues'] if i['severity']=='warning']
    assert [r['id'] for r in warnings]==['DK4_MES_B50_R0061','DK4_MES_B50_R0114']
    out=deepcopy(old);out.update(plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),records=rows,prior_native_proof=str(OLD),prior_native_proof_sha256=sha(OLD.read_bytes()),
        fresh_compiled_alignment_cases=20,reused_compiled_alignment_cases=92,total_bound_compiled_alignment_cases=112,fresh_progressive_alignment_cases=20,reused_progressive_alignment_cases=92,
        progressive_alignment_cases=112,exact_reused_compiled_records=reused,fresh_changed_compiled_records=fresh,review_sheets=sheets,prior_superseded_review_sheets=superseded,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),unapproved_exact_ordinary_boundary_warnings=warnings,
        five_phrase_refinements_no_added_rows_pages_orprose_change=True,no_repeated_native_execution_for23_exact_records=True,new_sheets_visual_review_pending=True)
    out['evidence']=dict(out['evidence'])|{str(p):sha(p.read_bytes()) for p in [OLD,PLAN,LOGICAL,DOC,NAMES,Path(__file__)]}
    save(ROOT/'28_final_native_pages20_fresh92_reused_alignments.json',out)
    print('FinalB50:28native pages,20fresh/92exactreused alignments;four updated sheets need direct view.Two original weak-ending diagnostics retained;formatting still pendingactual/release.')
