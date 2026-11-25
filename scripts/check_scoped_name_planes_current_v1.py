"""Render deduplicated current name strings with the qualified native style11 oracle."""
import argparse
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


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['name-review','bindings','out']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    review,bound=map(load,[args.name_review,args.bindings]);receipt=bound['runtime']
    ctx=RegisteredRuntime(receipt['release_proof'],receipt['startup_proof'],captain=receipt['captain'])
    assert ctx.receipt()==receipt
    reviewed={r['actor_ID']:r for r in review['records']}
    assert set(reviewed)=={r['actor_ID'] for r in bound['records']}
    consumers=[]
    for row in bound['records']:
        approved=reviewed[row['actor_ID']]
        assert approved['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert approved['current_reference']['candidate_sha256']==receipt['candidate_sha256']
        assert approved['current_consumers']==row['current_consumers']
        for form in row['current_consumers']:
            assert form['text'].encode('ascii').hex()==form['text_hex']
            consumers.append(dict(actor_ID=row['actor_ID'],consumer=form['consumer'],text=form['text'],text_hex=form['text_hex']))
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
    exec(compile(proven.PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-independent-style11-oracle','exec'),oracle)
    env={**proven.raster.__globals__,'machine':machine}
    exec(compile(proven.style.NATIVE_NAME_RASTER_SOURCE,__file__+'::same-native-style11-current-instructions','exec'),env)
    args.out.mkdir(parents=True);planes=[];pictures=[]
    for text in sorted({r['text'] for r in consumers}):
        raw=text.encode('ascii');pixels,events,font=env['raster'](ctx.arm,raw)
        assert font==ctx.image.read_file('/GRP/KANJI.FNT') and pixels==oracle['expected_pixels'](ctx.arm,font,events)
        emitted,flushes=proven.original_name_events(events,raw);assert emitted==proven.codes(raw)
        assert all(e['kind']=='ascii' and e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        assert max(e['x']+6 for e in events)==6*(len(raw)+len(raw)%2)<=216
        path=args.out/f'name_{len(planes):02d}.bin';path.write_bytes(pixels)
        pic=Image.new('RGB',(216,64));pic.putdata([(65,53,42) if v else (250,245,223) for v in pixels])
        png=path.with_suffix('.png');pic.save(png)
        planes.append(dict(text=text,native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),
            preview_sha256=sha(png.read_bytes()),native_events=events,native_zero_ink_flushes=flushes,
            complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True))
        pictures.append((text,pic))
    sheets=[]
    for start in range(0,len(pictures),16):
        part=pictures[start:start+16]
        sheet=Image.new('RGB',(912,((len(part)+1)//2)*64),'#263238');draw=ImageDraw.Draw(sheet)
        for index,(text,pic) in enumerate(part):
            x,y=index%2*456,index//2*64;draw.text((x+3,y+2),text+' native style11',fill='white')
            sheet.paste(pic.crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST),(x,y+22))
        path=args.out/f'names_part{start//16+1}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),strings=len(part)))
    save(args.out/'native_name_planes.json',dict(runtime=receipt,actors=len(bound['records']),consumer_bindings=consumers,
        distinct_current_strings=len(planes),planes=planes,review_sheets=sheets,style_proof=styleproof,
        original_name_getters_reused_not_replayed=len(consumers),all_name_strings_ASCII_complete_andfit_style11_216px=True,
        full_catalogue_names_are_literal_font_tests_not_catalogue_UI_layout_approval=True,
        direct_visual_review_pending=True,no_new_actual_headers_orconditional_role_assignment=True,
        no_name_data_ROM_orreview_credit_change=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.name_review,args.bindings,Path(__file__)]}))
    print('PASS',len(bound['records']),'actors/',len(consumers),'getters reused/',len(planes),'fresh name strings;direct view pending.')


if __name__=='__main__':main()
