"""Bind final tag-aware plan using90 exact native reuses andfour fresh R140 alignment cases."""
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
ROOT=Path('work/analysis/Rafael_B48_pages_refined_v8038')
OLD=Path('work/analysis/Rafael_B48_pages_v8036/91_complete_native_paragraphs92_pages364_compiled_alignments4_FE.json')
PLAN=Path('work/analysis/Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json')
LOGICAL=Path('work/analysis/Rafael_B48_logical_v8032/91_logical_paragraphs364_original_native_alignments4_FE.json')
DOC=Path('translations/rafael_B48_editorial_manuscript_v2.json')
NAMES=Path('work/analysis/Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists()
    old,plan,logical,doc,names=map(read,[OLD,PLAN,LOGICAL,DOC,NAMES])
    prior_plan=Path(old['plan']);before=read(prior_plan)
    assert sha(prior_plan.read_bytes())==old['plan_sha256'] and not plan['failures']
    assert plan['manuscript_sha256']==old['manuscript_sha256']==logical['manuscript_sha256']==sha(DOC.read_bytes())
    changed=[p['id'] for p,q in zip(plan['records'],before['records'],strict=True) if p['encoded_hex']!=q['encoded_hex']]
    assert changed==['DK4_MES_B48_R0140']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==old['candidate_sha256']==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==old['ARM9_sha256'] and sha(font)==old['font_sha256']
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(old['source_owned_progressive_page_adapter'],__file__+'::exact-current-native-pages','exec'),pe)
    ne=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::original-macros','exec'),ne)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];reused=[];fresh=[]
    for row,p,previous in zip(doc['records'],plan['records'],old['records'],strict=True):
        assert row['id']==p['id']==previous['id']
        if row['id'] not in changed:
            assert p['encoded_hex']==previous['compiled_hex'] and p['formatted_markup']==previous['formatted_markup']
            for page in previous['pages']:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            value=deepcopy(previous);value.update(reused_exact_native_compiled_record=True,prior_native_proof=str(OLD),prior_native_proof_sha256=sha(OLD.read_bytes()))
            rows.append(value);reused.append(row['id']);continue
        encoded=bytes.fromhex(p['encoded_hex']);body=encoded[1:]
        assert row['source_selector']==encoded[0]==75 and row['kind']=='progressive' and b'\0' not in body
        result=ctx.execute(ne['expand'],body,75);ctx.machines.pop()
        assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
        assert ' '.join(body.decode('ascii').split())==row['english']
        rendered=pe['pages'](arm,font,body)
        assert rendered['complete_consumed_bytes']==len(body) and len(rendered['pages'])==p['expected_native_pages']==1
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(row['id']+f'_page{page["page"]}.bin');path.write_bytes(pixels)
            assert page['first_visible_origin']==[0,0]
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview)
            page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
                first_visible_origin_matches_original_return_andguard=True)
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=48,source_record_index=row['source_record_index'],
            source_selector=75,kind='progressive',compiled_hex=encoded.hex(),expanded_native_hex=body.hex(),
            logical_English=row['english'],formatted_markup=p['formatted_markup'],native_alignment=result,
            reused_exact_native_compiled_record=False,**rendered))
        fresh.append(row['id'])
    assert not ctx.machines and len(rows)==91 and len(reused)==90 and fresh==changed
    pictures=[(r['id']+(' FE original paper' if r['kind']=='system-FE' else f' p{p["page"]}'),p) for r in rows for p in r['pages']]
    assert len(pictures)==92
    index=next(i for i,(label,p) in enumerate(pictures) if label.startswith(changed[0]));group=index//6
    assert group==3
    sheet=Image.new('RGB',(1368,320),'#263238');draw=ImageDraw.Draw(sheet)
    for n,(label,page) in enumerate(pictures[group*6:group*6+6]):
        picture=Image.open(page['preview']).convert('RGB');x,y=n%3*456,n//3*160
        draw.text((x+3,y+3),label+' offline native',fill='white')
        sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
    path=ROOT/'Rafael_B48_native_pages_sheet04_final.png';sheet.save(path)
    sheets=deepcopy(old['review_sheets']);superseded=deepcopy(sheets[group])
    sheets[group]=dict(path=str(path),sha256=sha(path.read_bytes()))
    out=deepcopy(old)
    out.update(plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),records=rows,
        prior_native_proof=str(OLD),prior_native_proof_sha256=sha(OLD.read_bytes()),
        fresh_compiled_alignment_cases=4,reused_compiled_alignment_cases=360,total_bound_compiled_alignment_cases=364,
        fresh_progressive_alignment_cases=4,reused_progressive_alignment_cases=344,reused_FE_null_actor_alignment_cases=16,
        progressive_alignment_cases=348,FE_null_actor_alignment_cases=16,
        exact_reused_compiled_records=reused,fresh_changed_compiled_records=fresh,
        source_tag_question_kept_together_no_added_row_orprose_change=True,review_sheets=sheets,
        prior_superseded_review_sheet=superseded,new_sheet_visual_review_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_repeated_native_execution_for90_exact_records=True)
    out['evidence']=dict(out['evidence'])|{str(p):sha(Path(p).read_bytes()) for p in [OLD,PLAN,LOGICAL,DOC,NAMES,Path(__file__)]}
    save(ROOT/'91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json',out)
    print('Final B48 native binding:91paragraphs/92pages,4fresh/360exactreused alignments.Tag together;one updated sheet requires view.All other native checks reused.')
