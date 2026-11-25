"""Prove the changed compiled R16 input;reuse100 exact unchanged alignment cases by bytes/hashes."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_native_pages_v7207');DOC=Path('translations/lil_B225_editorial_manuscript_v1.json');OLDPLAN=Path('work/analysis/lil_B225_layout_v7191b/thirteen_whole_paragraph_plans_no_macros_no_prose_changes.json');PLAN=Path('work/analysis/lil_B225_layout_v7191c/thirteen_whole_paragraph_plans_no_macros_no_prose_changes.json');PRIOR=Path('work/analysis/lil_B225_native_pages_v7192/all13_paragraphs14_complete_native_pages104_alignments.json');INPUT=Path('work/analysis/current_V7168_native_v7173/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,oldplan,plan,prior=map(read,[DOC,OLDPLAN,PLAN,PRIOR]);assert oldplan['manuscript_sha256']==plan['manuscript_sha256']==prior['manuscript_sha256']==sha(DOC.read_bytes()) and prior['layout_plan_sha256']==sha(OLDPLAN.read_bytes());oldrows={r['id']:r for r in oldplan['records']};models={r['id']:r for r in prior['records']};ident='DK4_MES_B225_R0016';changed=[r['id'] for r in plan['records'] if r['encoded_hex']!=oldrows[r['id']]['encoded_hex']];assert changed==[ident] and not plan['failures']
    for r in plan['records']:assert r['English']==oldrows[r['id']]['English'] and r['source_hex']==oldrows[r['id']]['source_hex'] and r['expected_native_pages']==oldrows[r['id']]['expected_native_pages']
    r=next(r for r in plan['records'] if r['id']==ident);assert oldrows[ident]['line_lengths']==[24,28,18] and r['line_lengths']==[35,17,18]
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');env={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(prior['source_owned_2b6_page_adapter'],__file__+'::exact-pages','exec'),env)
    from scripts.verify_lil_B174_fonts_v4470 import expand as original_expand
    expandenv=dict(original_expand.__globals__);exec(compile(prior['source_owned_expand_adapter'],__file__+'::original-expand','exec'),expandenv);cases=[];pictures=[]
    for p in plan['records']:
        base=deepcopy(models[p['id']]);assert all(sha(Path(pg['native_plane']).read_bytes())==pg['native_plane_sha256'] for pg in base['pages'])
        if p['id']==ident:
            body=bytes.fromhex(p['encoded_hex'])[1:];compiled=ctx.execute(expandenv['expand'],body,16);ctx.machines.pop();assert len(compiled['cases'])==4 and all(v['output_hex']==body.hex() for v in compiled['cases']);rendered=env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body);assert len(rendered['pages'])==1
            for pg in rendered['pages']:
                pixels=bytes.fromhex(pg.pop('native_plane_hex'));assert pg['first_visible_origin']==[0,0];path=ROOT/(ident+'_page1.bin');path.write_bytes(pixels);im=Image.new('RGB',(216,64));im.putdata([{0:(239,232,201),1:(0,8,0),15:(98,97,98)}[v] for v in pixels]);png=path.with_suffix('.png');im.save(png);pg.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),compiler_owned_page_continuation_guard_bytes=0,exact_first_visible_origin_verified_without_font_or_bounds_change=True)
            logical=deepcopy(next(v for v in base['logical_and_compiled_current_native_pipelines'] if v['version']=='logical'));base.update(compiled_hex=p['encoded_hex'],formatted_markup=p['formatted_markup'],logical_and_compiled_current_native_pipelines=[logical,dict(version='compiled-protected',**compiled)],**rendered)
        else:assert base['compiled_hex']==p['encoded_hex'] and base['formatted_markup']==p['formatted_markup']
        cases.append(base)
        for pg in base['pages']:
            assert sha(Path(pg['preview']).read_bytes())==pg['preview_sha256'];pictures.append((base['id'],pg['page'],Image.open(pg['preview']).convert('RGB')))
    assert len(cases)==13 and len(pictures)==14 and not ctx.machines;sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(key,page,im) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),key+' native page'+str(page),fill='white');sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'all14_complete_pages_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    out=deepcopy(prior);out.update(layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=cases,review_sheets=sheets,prior_native_proof=str(PRIOR),prior_native_proof_sha256=sha(PRIOR.read_bytes()),new_alignment_cases=4,exact_reused_alignment_cases=100,logical_compiled_input_alignment_cases=104,R16_opening35_cells_predecessor24_without_prose_change=True,only_R16_compiled_bytes_changed_all_other12_exact=True,visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),stored_actual_references_andrelease_require_successors=True);out['evidence'].update({str(p):sha(p.read_bytes()) for p in [DOC,OLDPLAN,PLAN,PRIOR,INPUT,Path(__file__)]});save(ROOT/'all13_paragraphs14_complete_native_pages104_alignments.json',out);print('R16 first row24->35 cells,unchanged prose,4 fresh compiled alignments/100 exact reused cases. All13 paragraphs/14 complete native pages remain. New stored/actual/reference/release successors pending;zero credit.')
