"""Bind the scoped progressive names to the current own context and original pixels."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import check_hodram_B171_B190_scoped_names as proven

ROOT=Path('work/analysis/Rafael_B36_B41_progressive_names_20261104')
NEW=Path('work/analysis/Rafael_B36_B41_new_name_bindings_20261104/names.json')
OLD=Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104/native_name_planes.json')
RELEASE=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0)
    newer,older=map(load,[NEW,OLD]);assert newer['runtime']==older['runtime']
    prior=RegisteredRuntime(newer['runtime']['release_proof'],newer['runtime']['startup_proof'],captain=0)
    assert prior.receipt()==newer['runtime'] and prior.arm==ctx.arm and prior.common==ctx.common and prior.actor_bytes==ctx.actor_bytes
    assert prior.image.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
    consumers=[r for r in [*older['consumer_bindings'],*newer['current_names']['rows']] if r['consumer']=='progressive-nameplate']
    assert len(consumers)==11 and {r['actor_ID'] for r in consumers}=={0,4,5,6,8,31,34,51,75,151,153}
    sections=MainCodeFile(ctx.arm,BASE).sections
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=bytes(sections[3].data[:-48]))]
    def machine(value):
        assert value==ctx.arm
        cpu=proven.paint_machine(value)
        def exact(u,pc,size,_):
            hits=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(hits)==1
            s=hits[0];assert bytes(u.mem_read(pc,size))==bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+size])
        cpu.hook_add(UC_HOOK_CODE,exact)
        return cpu
    styleproof=FunctionType(proven.style.style_source_proof.__code__,{**proven.style.style_source_proof.__globals__,'ARM9':sha(ctx.arm)})(ctx.arm)
    oracle=dict(proven.expected_pixels.__globals__)
    exec(compile(proven.PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-independent-font-oracle','exec'),oracle)
    renderer={**proven.raster.__globals__,'machine':machine}
    exec(compile(proven.style.NATIVE_NAME_RASTER_SOURCE,__file__+'::same-source-proven-style11','exec'),renderer)
    planes=list(older['planes']);assert len(planes)==4
    for p in planes:assert sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256']
    fresh=sorted({r['text'] for r in consumers}-{p['text'] for p in planes});assert len(fresh)==6
    ROOT.mkdir();sheet=Image.new('RGB',(912,192),'#263238');draw=ImageDraw.Draw(sheet)
    for index,text in enumerate(fresh):
        raw=text.encode('ascii');pixels,events,font=renderer['raster'](ctx.arm,raw)
        assert font==ctx.image.read_file('/GRP/KANJI.FNT') and pixels==oracle['expected_pixels'](ctx.arm,font,events)
        emitted,flushes=proven.original_name_events(events,raw);assert emitted==proven.codes(raw)
        assert all(e['kind']=='ascii' and e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        assert max(e['x']+6 for e in events)==6*(len(raw)+len(raw)%2)<=216
        path=ROOT/f'name_{index}.bin';path.write_bytes(pixels)
        pic=Image.new('RGB',(216,64));pic.putdata([(65,53,42) if v else (250,245,223) for v in pixels]);png=path.with_suffix('.png');pic.save(png)
        x,y=index%2*456,index//2*64;draw.text((x+3,y+2),text+' native style11',fill='white')
        sheet.paste(pic.crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST),(x,y+22))
        planes.append(dict(text=text,native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),
            native_events=events,native_zero_ink_flushes=flushes,complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True))
    png=ROOT/'six_additional_progressive_names.png';sheet.save(png)
    assert len(planes)==10
    save(ROOT/'native_name_planes.json',dict(runtime=ctx.receipt(),consumer_bindings=consumers,planes=planes,style_proof=styleproof,
        exact_reused_name_planes=4,fresh_name_planes=6,scoped_actors=11,prior_native_getter_consumers_reused=22,
        complete_ARM9_COMMON_font_andactor_bytes_equal_tested_getter_context=True,
        source_name_bindings=str(NEW),source_name_bindings_sha256=sha(NEW.read_bytes()),prior_names=str(OLD),prior_names_sha256=sha(OLD.read_bytes()),
        review_sheets=[dict(path=str(png),sha256=sha(png.read_bytes()),strings=6)],direct_visual_review_pending=True,
        all_scoped_progressive_names_ASCII_andcomplete_glyphs_fit216px=True,
        full_catalogue_metadata_not_approved_here=True,two_catalogue_field_corrections_remain_pending=True,no_name_data_change=True,
        actual_gameplay=False,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NEW,OLD,RELEASE,STARTUP,Path(proven.__file__),Path(__file__)]}))
    print('11 source-bound progressive names/10 strings:four exact plane reuses,six fresh native/font planes;visual andactual header binding pending.')
