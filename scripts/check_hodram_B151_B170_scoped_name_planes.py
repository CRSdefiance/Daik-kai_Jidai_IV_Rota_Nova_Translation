"""Reuse bound names/getters and the proven style ABI; check distinct current glyph strings."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
import math
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.probe_button_prompt_native import machine as paint_machine
from scripts import lil_B207_name_style_v6354d as style
from scripts.shady_man_font_oracles_v6263 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels,raster
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events

ROOT=Path('work/analysis/Hodram_B151_B170_scoped_name_planes_20261102')
BINDINGS=Path('work/analysis/Hodram_B151_B170_clean_20261102/native_identity_and_item_checkpoint_v1.json')
NAMES=Path('translations/hodram_B151_B170_scoped_names_andterms_v1.json')
RELEASE=Path('work/analysis/Hodram_B131_B150_release_verified_20261102/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists() or not any(ROOT.iterdir());bound,names=load(BINDINGS),load(NAMES)
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'));assert bound['runtime']==ctx.receipt()
    assert bound['whole_actual_actor_model_COMMON_font_exact'] and bound['complete_ARM9_inverse']['complete_parent_inverse_exact']
    for r in bound['records']:assert sha(Path(r['prior_native_proof']).read_bytes())==r['prior_native_proof_sha256']
    consumers=[dict(actor_ID=r['actor_ID'],consumer=c['consumer'],text=c['text'],text_hex=c['text_hex'],binding_record=i)
        for i,r in enumerate(bound['records']) for c in r['current_consumers']]
    assert len(consumers)==72 and len(bound['records'])==36
    mention=bound['mentioned_name'];given=next(r['current'] for r in mention['fields'] if r['column']==0)
    consumers.append(dict(actor_ID=79,consumer='mentioned-given-name-only',text=given['text'],text_hex=given['hex'],binding_record='mentioned_name.fields[column0]'))
    assert given['text']=='Mivor'
    literals=sorted({r['text'] for r in consumers});assert all(t.encode('ascii').hex()==r['text_hex'] for r in consumers for t in [r['text']])
    sections=MainCodeFile(ctx.arm,BASE).sections;payload=bytes(sections[3].data[:-48]);owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    def machine(value):
        assert value==ctx.arm;cpu=paint_machine(value)
        def exact(u,pc,size,_):
            hits=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)];assert len(hits)==1
            s=hits[0];assert bytes(u.mem_read(pc,size))==bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+size])
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    styleproof=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(ctx.arm)})(ctx.arm)
    oracle=dict(expected_pixels.__globals__);exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-font-oracle','exec'),oracle)
    env={**raster.__globals__,'machine':machine};exec(compile(style.NATIVE_NAME_RASTER_SOURCE,__file__+'::same-name-style11','exec'),env)
    ROOT.mkdir(parents=True,exist_ok=True);rows=[];pictures=[]
    for index,text in enumerate(literals):
        raw=text.encode('ascii');pixels,events,font=env['raster'](ctx.arm,raw)
        assert font==ctx.image.read_file('/GRP/KANJI.FNT') and pixels==oracle['expected_pixels'](ctx.arm,font,events)
        emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw)
        assert all(e['kind']=='ascii' and e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        # An odd ASCII name has the already-proven final zero-ink flush cell.
        # original_name_events binds every real glyph separately above.
        assert max(e['x']+6 for e in events)==6*(len(raw)+len(raw)%2)<=216
        path=ROOT/f'name_{index:02d}.bin';path.write_bytes(pixels)
        picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if v else (250,245,223) for v in pixels]);png=path.with_suffix('.png');picture.save(png)
        rows.append(dict(text=text,native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),
            native_events=events,native_zero_ink_flushes=flushes,complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass=True,
            style11_proven_progressive_name_consumer=True,full_name_literal_font_test_not_actual_catalogue_UI_layout_approval=True))
        pictures.append((text,picture))
    sheets=[]
    for start in range(0,len(pictures),16):
        part=pictures[start:start+16];sheet=Image.new('RGB',(912,math.ceil(len(part)/2)*64),'#263238');draw=ImageDraw.Draw(sheet)
        for j,(text,picture) in enumerate(part):
            x=j%2*456;y=j//2*64;draw.text((x+3,y+2),text+' native style11',fill='white');sheet.paste(picture.crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST),(x,y+22))
        path=ROOT/f'names_{start//16+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),strings=len(part)))
    save(ROOT/'native_name_planes.json',dict(runtime=ctx.receipt(),bindings=str(BINDINGS),bindings_sha256=sha(BINDINGS.read_bytes()),
        individual_localization_decisions=str(NAMES),individual_localization_decisions_sha256=sha(NAMES.read_bytes()),actors=36,
        exact_existing_native_getters_reused_not_replayed=72,mentioned_given_name=79,consumer_bindings=consumers,
        distinct_current_strings=len(literals),planes=rows,review_sheets=sheets,style_proof=styleproof,
        all_current_names_ASCII_andfull_characters_fit_original216px=True,native_style11_full_name_literals_not_catalogue_UI_observation=True,
        direct_visual_review_pending=True,representative_B168_headers_andEnglish_gameplay_pending=True,new_credit=0,new_ROM=False,
        evidence={str(p):sha(p.read_bytes()) for p in [BINDINGS,NAMES,Path(style.__file__),Path('scripts/verify_name_catalog_glyphs_v278.py'),Path(__file__)]}))
    print(dict(actors=36,reused_getter_values=72,mentioned_names=1,distinct_native_planes=len(rows),sheets=len(sheets),visual_pending=True,new_credit=0))
