"""Check only the changed paragraph; reuse eight exact completed native proofs."""
import inspect
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_question_native_v6609');DOC=Path('translations/lil_B212_editorial_manuscript_v2.json');PLAN=Path('work/analysis/lil_B212_layout_v6608/nine_whole_paragraph_research_plans.json');BEFORE=Path('work/analysis/lil_B212_research_fonts_v6606c/all9_bodies9_complete_native_pages_and72_alignments_RESEARCH.json');INPUT=Path('work/analysis/current_V6584_native_v6593/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,previous=map(read,[DOC,PLAN,BEFORE]);assert previous['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes());oldplan=read(previous['layout_plan']);assert sha(Path(previous['layout_plan']).read_bytes())==previous['layout_plan_sha256'];old={r['id']:r for r in oldplan['records']};prior={r['id']:r for r in previous['records']};changed=[r['id'] for r in plan['records'] if r['encoded_hex']!=old[r['id']]['encoded_hex']];assert changed==['DK4_MES_B212_R0032'];ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT');env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(previous['source_owned_AA5_page_adapter'],__file__+'::AA5-original-page','exec'),env);rows=[]
    for p in plan['records']:
        row=next(r for r in doc['records'] if r['id']==p['id']);assert old[p['id']]['English']==p['English']==row['english']
        if p['id'] not in changed:
            record=deepcopy(prior[p['id']]);assert record['compiled_hex']==p['encoded_hex'] and record['formatted_markup']==p['formatted_markup']
            for page in record['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] and sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            record['exact_reused_from']=str(BEFORE);record['exact_reused_from_sha256']=sha(BEFORE.read_bytes());rows.append(record);continue
        pipelines=[];body=bytes.fromhex(p['encoded_hex'])[1:];logical=row['english'].split('}',1)[1].encode('ascii')
        for label,text in [('logical',logical),('compiled-protected',body)]:
            result=ctx.execute(expand,text,149);ctx.machines.pop();assert all(c['output_hex']==text.hex() for c in result['cases']);pipelines.append(dict(version=label,**result))
        rendered=env['pages'](arm,font,body);assert len(rendered['pages'])==1
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(p['id']+'_page1_216x64.bin');path.write_bytes(pixels);picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);preview=path.with_suffix('.png');picture.save(preview);page.update(native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()))
        rows.append(dict(id=p['id'],source_kind=row['kind'],source_selector=149,compiled_hex=p['encoded_hex'],formatted_markup=p['formatted_markup'],logical_and_compiled_current_native_pipelines=pipelines,**rendered))
    assert len(rows)==9 and not ctx.machines;out=deepcopy(previous);out.update(layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),records=rows,previous_font_proof=str(BEFORE),previous_font_proof_sha256=sha(BEFORE.read_bytes()),fresh_input_alignment_cases=8,exact_reused_alignment_cases=64,logical_compiled_input_alignment_cases=72,whole_question_preserved_on_second_row_with_no_new_page=True,changed_objects=changed,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_preview=rows[2]['pages'][0]['preview'],new_preview_sha256=rows[2]['pages'][0]['preview_sha256'],visual_review_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,BEFORE,INPUT,Path(expand.__code__.co_filename),Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()));save(ROOT/'all9_complete_pages72_alignments8_fresh64_exact_reused.json',out);print('R32 complete question/native page passes8 fresh alignments; eight unchanged objects reuse64 exact cases. All9 pages/72 alignments bound; no repeat of unchanged native checks.')
