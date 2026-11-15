"""Recheck the changed compiled page; reuse all exact logical and sixteen unchanged pages."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts import verify_lil_B220_native_pages_v6928 as original
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B220_editorial_manuscript_v1.json');PLAN=Path('work/analysis/lil_B220_layout_v6927b/seventeen_whole_paragraph_plans_no_macros_no_prose_changes.json');PRIOR=Path('work/analysis/lil_B220_native_pages_v6928/all17_paragraphs17_complete_native_pages136_alignments.json');ROOT=Path('work/analysis/lil_B220_native_pages_v6928b');INPUT=Path('work/analysis/current_V6910_native_v6920/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,prior=map(read,[DOC,PLAN,PRIOR]);assert len(plan['records'])==17 and not plan['failures'] and plan['manuscript_sha256']==prior['manuscript_sha256']==sha(DOC.read_bytes());oldplan=read(prior['layout_plan']);assert sha(Path(prior['layout_plan']).read_bytes())==prior['layout_plan_sha256'];byid={r['id']:r for r in doc['records']};oldcases={r['id']:r for r in prior['records']};changed=[r['id'] for r in plan['records'] if r['encoded_hex']!=oldcases[r['id']]['compiled_hex']];assert changed==['DK4_MES_B220_R0035'];assert next(r['line_lengths'] for r in plan['records'] if r['id']==changed[0])==[28,28,29,13]
    env=dict(original.expand.__globals__);exec(compile(prior['source_owned_expand_adapter'],__file__+'::preserved-expand','exec'),env);page_env={**original.old_pages.__globals__,'expected_pixels':original.expected_pixels};exec(compile(prior['source_owned_AA5_page_adapter'],__file__+'::preserved-AA5-pages','exec'),page_env);pages=page_env['pages'];image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT');ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');cases=[];pictures=[];reused=0;fresh=0
    for p in plan['records']:
        row=byid[p['id']];old=oldcases[p['id']];body=bytes.fromhex(p['encoded_hex'])[1:];logical=row['english'].split('}',1)[1].encode('ascii');assert row['source_selector'] in [26,199] and all(v['output_hex']==logical.hex() for v in old['logical_and_compiled_current_native_pipelines'][0]['cases'])
        if p['id'] not in changed:
            assert p['formatted_markup']==old['formatted_markup'];case=deepcopy(old);reused+=8
            for page in case['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] and sha(Path(page['preview']).read_bytes())==page['preview_sha256']
        else:
            result=ctx.execute(env['expand'],body,row['source_selector']);ctx.machines.pop();assert all(v['output_hex']==body.hex() for v in result['cases']);fresh+=4;reused+=4;rendered=pages(arm,font,body);assert len(rendered['pages'])==p['expected_native_pages']==1
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(p['id']+f'_page{page["page"]}.bin');plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels));assert page['first_visible_origin']==[0,0];picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);path=plane.with_suffix('.png');picture.save(path);page.update(preview=str(path),preview_sha256=sha(path.read_bytes()))
            pipelines=[deepcopy(old['logical_and_compiled_current_native_pipelines'][0]),dict(version='compiled-protected',**result)];case=dict(id=p['id'],source_kind=row['kind'],source_selector=row['source_selector'],compiled_hex=p['encoded_hex'],formatted_markup=p['formatted_markup'],logical_and_compiled_current_native_pipelines=pipelines,**rendered)
        case['exact_prior_proof_reuse']=dict(path=str(PRIOR),sha256=sha(PRIOR.read_bytes()),logical_alignments=4,compiled_alignments=0 if p['id'] in changed else 4,complete_page=p['id'] not in changed);cases.append(case);save(ROOT/(p['id']+'_individual_native_proof.json'),case)
        for page in case['pages']:pictures.append((p['id'],page['page'],Image.open(page['preview']).convert('RGB')))
    assert reused==132 and fresh==4 and len(cases)==len(pictures)==17 and not ctx.machines;sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(ident,page,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),ident+' native page'+str(page),fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'all17_complete_pages_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    out=deepcopy(prior);out.update(layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=cases,prior_native_proof=str(PRIOR),prior_native_proof_sha256=sha(PRIOR.read_bytes()),fresh_compiled_alignment_cases=fresh,exact_alignment_cases_reused=reused,complete_pages_reused=16,new_complete_pages=1,only_changed_compiled_record_IDs=changed,all17_paragraphs_and_136_alignment_cases_bound_without_repeating_unchanged_checks=True,review_sheets=sheets,visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={**prior['evidence'],str(PLAN):sha(PLAN.read_bytes()),str(PRIOR):sha(PRIOR.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())});save(ROOT/'all17_paragraphs17_complete_native_pages136_alignments.json',out);print('17 complete pages/136 alignments:132 exact cases reused,4 fresh compiled cases;only R35 wrap changes,unchanged prose/native geometry.')
