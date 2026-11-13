"""Reuse identical current-ARM9 name pixels and paint only newly scoped public strings."""
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

ROOT=Path('work/analysis/Rafael_B61_B80_progressive_name_planes_20261104')
NAMES=Path('translations/rafael_B61_B80_scoped_names_andterms_v1.json')
BINDINGS=Path('work/analysis/Rafael_B61_B80_clean_20261104/source_identity_event_andterm_checkpoint_v1.json')
QUAL=Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104/dependency_qualification.json')
PRIOR=Path('work/analysis/Rafael_B51_B60_progressive_name_planes_20261104/native_name_planes.json')
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,bound,qual,prior=map(load,[NAMES,BINDINGS,QUAL,PRIOR])
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']
    assert prior['proposed_ARM9_sha256']==sha(ctx.arm)
    assert len(doc['records'])==len(bound['name_bindings'])==22
    getters={r['actor_ID']:r for r in bound['name_bindings']}
    actors=[]
    for row in doc['records']:
        getter=next(c for c in getters[row['actor_ID']]['current_consumers'] if c['consumer']=='progressive-nameplate')
        assert row['english']==getter['text'] and row['english'].encode('ascii').hex()==getter['text_hex']
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        actors.append(dict(actor_ID=row['actor_ID'],text=getter['text'],text_hex=getter['text_hex'],
            source_reference=row['source_reference'],current_reference=row['current_reference'],
            native_getter_binding=getters[row['actor_ID']]))
    cache={r['text']:deepcopy(r) for r in prior['planes']}
    sections=MainCodeFile(ctx.arm,BASE).sections
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=bytes(sections[3].data[:-48]))]
    def machine(arm):
        assert arm==ctx.arm;cpu=proven.paint_machine(arm)
        def exact(u,pc,size,_):
            hits=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(hits)==1
            section=hits[0]
            assert bytes(u.mem_read(pc,size))==bytes(section.data[pc-section.ramAddress:pc-section.ramAddress+size])
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    styleproof=FunctionType(proven.style.style_source_proof.__code__,
        {**proven.style.style_source_proof.__globals__,'ARM9':sha(ctx.arm)})(ctx.arm)
    oracle=dict(proven.expected_pixels.__globals__)
    exec(compile(proven.PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-independent-style11-font-oracle','exec'),oracle)
    env={**proven.raster.__globals__,'machine':machine}
    exec(compile(proven.style.NATIVE_NAME_RASTER_SOURCE,__file__+'::same-original-style11-current-instructions','exec'),env)
    ROOT.mkdir();planes=[];pictures=[];fresh=reused=0
    for text in sorted({r['english'] for r in doc['records']}):
        if text in cache:
            plane=cache[text]
            assert sha(Path(plane['native_plane']).read_bytes())==plane['native_plane_sha256']
            assert sha(Path(plane['preview']).read_bytes())==plane['preview_sha256']
            assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
            plane['exact_previous_plane_reused']=dict(path=str(PRIOR),sha256=sha(PRIOR.read_bytes()),
                complete_target_ARM9_font_native_style_andinput_string_identical=True)
            reused+=1
        else:
            raw=text.encode('ascii');pixels,events,font=env['raster'](ctx.arm,raw)
            assert font==ctx.image.read_file('/GRP/KANJI.FNT') and pixels==oracle['expected_pixels'](ctx.arm,font,events)
            emitted,flushes=proven.original_name_events(events,raw);assert emitted==proven.codes(raw)
            assert all(e['kind']=='ascii' and e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
            assert max(e['x']+6 for e in events)==6*(len(raw)+len(raw)%2)<=216
            path=ROOT/f'name_{len(planes):02d}.bin';path.write_bytes(pixels)
            pic=Image.new('RGB',(216,64));pic.putdata([(65,53,42) if v else (250,245,223) for v in pixels])
            png=path.with_suffix('.png');pic.save(png)
            plane=dict(text=text,native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),
                native_events=events,native_zero_ink_flushes=flushes,
                complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True)
            fresh+=1
        planes.append(plane);pictures.append((text,Image.open(plane['preview']).convert('RGB')))
    assert len(planes)==21 and fresh+reused==21
    sheets=[]
    for start in range(0,len(pictures),12):
        part=pictures[start:start+12]
        sheet=Image.new('RGB',(912,((len(part)+1)//2)*64),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(text,pic) in enumerate(part):
            x,y=i%2*456,i//2*64;draw.text((x+3,y+2),text+' native style11',fill='white')
            sheet.paste(pic.crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST),(x,y+22))
        path=ROOT/f'names_part{start//12+1}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),strings=len(part)))
    save(ROOT/'native_name_planes.json',dict(runtime=ctx.receipt(),actors=actors,scoped_actors=22,distinct_strings=21,
        planes=planes,fresh_name_planes=fresh,exact_reused_name_planes=reused,style_proof=styleproof,review_sheets=sheets,
        current_progressive_names_bound_to_qualified_original_getters=True,
        all_scoped_progressive_names_ASCII_complete_andfit_native216px=True,direct_visual_review_pending=True,
        no_name_data_change_ornew_actual_header_gameplay_claim=True,full_catalogue_UI_andglobal207_review_still_open=True,
        no_new_getter_permutation_execution=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NAMES,BINDINGS,QUAL,PRIOR,RELEASE,Path(__file__)]}))
    print(f'22actors/21strings: {fresh} fresh style11 planes, {reused} exact current-ARM9 reuses. Direct view pending;actual headers still unvisited.',flush=True)
