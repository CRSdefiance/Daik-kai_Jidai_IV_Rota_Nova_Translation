"""Reuse exact style11 planes andrender only newly scoped name strings."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType,SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import check_hodram_B171_B190_scoped_names as proven

ROOT=Path('work/analysis/Rafael_B51_B60_progressive_name_planes_20261104')
NAMES=Path('translations/rafael_B51_B60_scoped_progressive_names_v1.json')
RUNTIME=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
PRIOR=[Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104/native_name_planes.json'),
    Path('work/analysis/Rafael_B36_B41_progressive_names_20261104/native_name_planes.json'),
    Path('work/analysis/Hodram_B171_B190_scoped_name_planes_20261104/native_name_planes.json')]
FERNAN=Path('work/analysis/Rafael_Fernan_name_native_20261104/native_name_fields_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,qual=map(load,[NAMES,RUNTIME/'dependency_qualification.json'])
    ctx=RegisteredRuntime(doc['runtime']['release_proof'],doc['runtime']['startup_proof'],captain=0)
    assert doc['runtime']==ctx.receipt()==qual['runtime']
    arm=Path(RUNTIME/'Fernan_proposed_ARM9_RESEARCH_ONLY.bin').read_bytes()
    proposal=load(RUNTIME/'Fernan_owned_fields_plan.json')
    assert sha(arm)==proposal['target_ARM9_sha256'] and proposal['parent_ARM9_sha256']==sha(ctx.arm)
    inverse=bytearray(arm)
    for f in proposal['fields']:inverse[f['physical_offset']:f['physical_offset']+f['owned_bytes']]=bytes.fromhex(f['old_hex'])
    assert bytes(inverse)==ctx.arm
    cache={}
    for path in PRIOR:
        old=load(path);assert old['runtime']['ARM9_sha256']==qual['previous_runtime']['ARM9_sha256']
        for p in old['planes']:cache[p['text']]=(deepcopy(p),path)
    fernan=load(FERNAN)
    for p in fernan['planes']:
        if p['version']=='proposed' and p['style']==11:
            cache[p['text']]=(dict(text=p['text'],native_plane=p['plane'],native_plane_sha256=p['plane_sha256'],
                preview=p['preview'],preview_sha256=p['preview_sha256'],native_events=p['events'],
                complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=p['complete_glyphs_bounds_andindependent_pixels_pass']),FERNAN)
    sections=MainCodeFile(arm,BASE).sections;owners=[*sections,SimpleNamespace(ramAddress=POOL,data=bytes(sections[3].data[:-48]))]
    def machine(value):
        assert value==arm;cpu=proven.paint_machine(value)
        def exact(u,pc,size,_):
            hits=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)];assert len(hits)==1
            s=hits[0];assert bytes(u.mem_read(pc,size))==bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+size])
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    styleproof=FunctionType(proven.style.style_source_proof.__code__,{**proven.style.style_source_proof.__globals__,'ARM9':sha(arm)})(arm)
    oracle=dict(proven.expected_pixels.__globals__)
    exec(compile(proven.PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-independent-style11-font','exec'),oracle)
    renderer={**proven.raster.__globals__,'machine':machine}
    exec(compile(proven.style.NATIVE_NAME_RASTER_SOURCE,__file__+'::same-complete-current-style11','exec'),renderer)
    ROOT.mkdir();planes=[];pictures=[];reused=fresh=0
    for text in sorted({r['english'] for r in doc['records']}):
        if text in cache:
            plane,path=cache[text];pixels=Path(plane['native_plane']).read_bytes()
            assert sha(pixels)==plane['native_plane_sha256'] and sha(Path(plane['preview']).read_bytes())==plane['preview_sha256']
            assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
            plane['exact_previous_plane_reused']=dict(path=str(path),sha256=sha(path.read_bytes()),
                text_style_font_andall_code_exact_except_disjoint_owned_text_data=True)
            reused+=1
        else:
            raw=text.encode('ascii');pixels,events,font=renderer['raster'](arm,raw)
            assert font==ctx.image.read_file('/GRP/KANJI.FNT') and pixels==oracle['expected_pixels'](arm,font,events)
            emitted,flushes=proven.original_name_events(events,raw);assert emitted==proven.codes(raw)
            assert all(e['kind']=='ascii' and e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
            assert max(e['x']+6 for e in events)==6*(len(raw)+len(raw)%2)<=216
            path=ROOT/f'name_{len(planes)}.bin';path.write_bytes(pixels)
            pic=Image.new('RGB',(216,64));pic.putdata([(65,53,42) if v else (250,245,223) for v in pixels]);png=path.with_suffix('.png');pic.save(png)
            plane=dict(text=text,native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),
                native_events=events,native_zero_ink_flushes=flushes,complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True)
            fresh+=1
        pictures.append((text,Image.open(plane['preview']).convert('RGB')));planes.append(plane)
    assert len(doc['records'])==18 and len(planes)==17
    sheets=[]
    for start in range(0,len(pictures),12):
        part=pictures[start:start+12];sheet=Image.new('RGB',(912,((len(part)+1)//2)*64),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(text,pic) in enumerate(part):
            x,y=i%2*456,i//2*64;draw.text((x+3,y+2),text+' style11',fill='white')
            sheet.paste(pic.crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST),(x,y+22))
        path=ROOT/f'names_part{start//12+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),strings=len(part)))
    save(ROOT/'native_name_planes.json',dict(runtime=ctx.receipt(),proposed_ARM9_sha256=sha(arm),scoped_actors=18,planes=planes,
        fresh_name_planes=fresh,exact_reused_name_planes=reused,style_proof=styleproof,review_sheets=sheets,direct_visual_review_pending=True,
        name_decisions=str(NAMES),name_decisions_sha256=sha(NAMES.read_bytes()),dependency_qualification=str(RUNTIME/'dependency_qualification.json'),
        dependency_qualification_sha256=sha((RUNTIME/'dependency_qualification.json').read_bytes()),
        all_scoped_progressive_names_ASCII_andcomplete_glyphs_fit216px=True,
        no_new_getter_execution_oractual_header_gameplay_claim=True,full_catalogue_UI_not_approved_here=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [*PRIOR,FERNAN,NAMES,RUNTIME/'Fernan_owned_fields_plan.json',Path(__file__)]}))
    print('18actors/17strings:',fresh,'fresh style11 planes,',reused,'exact reuses;direct view pending.')
