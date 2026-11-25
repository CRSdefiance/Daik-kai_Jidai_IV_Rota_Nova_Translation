"""Reuse81 exact compiled records; rerender only the improved two-page explanation."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from scripts import prove_Hodram_B54_B60_pages_v8803 as native
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B54_B60_pages_v8804')
PRIOR=Path('work/analysis/Hodram_B54_B60_pages_v8803b/compiled_native_pages.json')
PLAN=Path('work/analysis/Hodram_B54_B60_layout_v8802d/automatic_plans.json')

if __name__=='__main__':
    assert not ROOT.exists();old,new,doc,source=map(read,[PRIOR,PLAN,native.DOC,native.SOURCE]);previous=read(old['plan'])
    assert old['manuscript_sha256']==new['manuscript_sha256']==sha(native.DOC.read_bytes()) and not new['failures']
    assert not any(i['severity'] in ['warning','error'] for r in new['records'] for i in r['base_QA']['issues'])
    changed=[a['id'] for a,b in zip(new['records'],previous['records'],strict=True) if a['encoded_hex']!=b['encoded_hex']]
    assert changed==['DK4_MES_B59_R0023']
    for a,b in zip(new['records'],previous['records'],strict=True):
        assert a['id']==b['id'] and a['logical_English']==b['logical_English']
        if a['id'] not in changed:assert a['encoded_hex']==b['encoded_hex'] and a['formatted_markup']==b['formatted_markup'] and a['base_QA']==b['base_QA']
    image=native.NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT');pixels,_,oracle=native.bind(image)
    pe={**native.original_pages.__globals__,'expected_pixels':pixels,'codes':native.codes}
    exec(compile(source['source_owned_target_page_adapter'],__file__+'::unchanged-native-pages','exec'),pe)
    logical=read(native.LOGICAL);prog=dict(native.progressive_expand.__globals__)
    exec(compile(logical['source_owned_progressive_adapter'],__file__+'::unchanged-native-macros','exec'),prog)
    ROOT.mkdir(parents=True);ctx=native.RouteCurrentContext(native.INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=deepcopy(old['records']);row=next(r for r in rows if r['id']==changed[0]);p=next(r for r in new['records'] if r['id']==changed[0]);raw=bytes.fromhex(p['encoded_hex'])
    prefix,body=raw[0],raw[1:];assert prefix==84 and not any(t in body for t in [b'FI',b'FA',b'FO',b'\0',b'%'])
    aligned=ctx.execute(prog['expand'],body,prefix);ctx.machines.pop()
    assert len(aligned['cases'])==4 and all(c['output_hex']==body.hex() for c in aligned['cases']) and not ctx.machines
    rendered=pe['pages'](arm,font,body);assert rendered['complete_consumed_bytes']==len(body) and len(rendered['pages'])==p['expected_native_pages']==2
    for page in rendered['pages']:
        plane=bytes.fromhex(page.pop('native_plane_hex'));file=ROOT/(row['id']+f'_page{page["page"]}.bin');file.write_bytes(plane)
        segment=body[page['start']:page['end']];guarded=page['page']>1 and segment.startswith(b' ') and not segment.startswith(b'  ')
        assert page['first_visible_origin']==([6,0] if guarded else [0,0])
        if guarded:assert page['events'][0]==dict(kind='ascii',code=32,style=1,x=0,y=0)
        pic=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};pic.putdata([colors[v] for v in plane]);preview=file.with_suffix('.png');pic.save(preview)
        page.update(native_plane=str(file),native_plane_sha256=sha(plane),preview=str(preview),preview_sha256=sha(preview.read_bytes()),
            native_continuation_guard_at_zero_andfirst_visible_at_six=guarded,complete_first_internal_final_codes_bounds_consumption_andindependent_ink_exact=True)
    row.update(compiled_hex=raw.hex(),expanded_native_hex=body.hex(),formatted_markup=p['formatted_markup'],native_alignment=aligned,complete_native_English_display=rendered)
    pictures=[]
    for r in [r for r in rows if r['block']==59]:
        for page in r['complete_native_English_display']['pages']:
            path=Path(page['preview']);assert sha(path.read_bytes())==page['preview_sha256'];pictures.append((r['id']+f' p{page["page"]}',Image.open(path).convert('RGB')))
    sheet=Image.new('RGB',(912,((len(pictures)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
    for index,(label,pic) in enumerate(pictures):
        x,y=index%2*456,index//2*160;draw.text((x+3,y+3),label+' offline English',fill='white');sheet.paste(pic.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    path=ROOT/'B59_English_part1.png';sheet.save(path)
    sheets=[dict(block=59,path=str(path),sha256=sha(path.read_bytes()),pages=len(pictures)) if s['block']==59 else s for s in old['review_sheets']]
    reused_files={}
    for r in rows:
        d=r['complete_native_English_display']
        if r['kind']=='system-FE':parts=[d];keys=['native_physical_plane','native_logical_plane','preview']
        else:parts=d['pages'];keys=['native_plane','preview']
        for part in parts:
            for key in keys:
                digest=part[key+'_sha256'];assert sha(Path(part[key]).read_bytes())==digest
                if r['id'] not in changed:reused_files[part[key]]=digest
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    result=deepcopy(old);result.update(records=rows,plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),review_sheets=sheets,
        fresh_compiled_alignment_cases=4,reused_compiled_alignment_cases=324,total_bound_compiled_alignment_cases=328,
        prior_native_pages=str(PRIOR),prior_native_pages_sha256=sha(PRIOR.read_bytes()),only_changed_record_IDs=changed,reused81_record_planes_andpreviews=reused_files,
        improved_auxiliary_page_boundary_prose_unchanged=True,direct_view_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={**old['evidence'],str(PRIOR):sha(PRIOR.read_bytes()),str(PLAN):sha(PLAN.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())})
    save(ROOT/'compiled_native_pages.json',result)
    print('One changed record: two fresh complete native pages /four alignments;81 records and83 pages reused exactly. Total82/85; direct view pending.')
