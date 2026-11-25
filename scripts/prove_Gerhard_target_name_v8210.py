"""Owned12-byte CPU-only name-input probe; original current code, no changed ROM or gameplay."""
import inspect,textwrap
from types import FunctionType
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts import lil_B207_name_style_v6354d as style
from scripts.prove_lil_B208_name_planes_v6405 import original_name_events,codes
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_target_name_v8210')
OWNERSHIP=Path('work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json')
BEFORE=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')

class OwnedNameInputContext(RouteCurrentContext):
    """Original snapshot with one explicitly owned synthetic name-data input; not a new-ROM snapshot."""

MACHINE_ADAPTER=checked_text(textwrap.dedent(inspect.getsource(RouteCurrentContext.machine)),{
    'before=bytes(cpu.mem_read(self.actor_root,0x1A04));executed=set()':
    '''slot=self.name_input['offset'];old=bytes.fromhex(self.name_input['current_hex']);value=bytes.fromhex(self.name_input['target_hex'])
    current=bytes(cpu.mem_read(BASE,len(self.raw)))
    assert current[slot:slot+len(old)]==old and len(old)==len(value)==self.name_input['bytes']==12
    assert current[slot+12:slot+20]==b'Blades\\0\\0'
    cpu.mem_write(BASE+slot,value)
    changed=bytes(cpu.mem_read(BASE,len(self.raw)));expected=bytearray(current);expected[slot:slot+12]=value
    assert changed==bytes(expected) and changed[slot+12:slot+20]==b'Blades\\0\\0'
    restored=bytearray(changed);restored[slot:slot+12]=old;assert bytes(restored)==current
    self.name_input_receipts.append(dict(offset=slot,bytes=12,source_hex=old.hex(),target_hex=value.hex(),
        input_RAM_sha256=sha(current),research_RAM_sha256=sha(changed),all_other_RAM_andBlades_exact=True,
        inverse_recovers_entire_current_machine_RAM=True,synthetic_CPU_data_input_not_actual_gameplay=True))
    before=bytes(cpu.mem_read(self.actor_root,0x1A04));executed=set()''',
})
machine_env=dict(RouteCurrentContext.machine.__globals__)
exec(compile(MACHINE_ADAPTER,__file__+'::owned12byte-name-input','exec'),machine_env)
OwnedNameInputContext.machine=machine_env['machine']

if __name__=='__main__':
    assert not ROOT.exists();ownership,before=map(read,[OWNERSHIP,BEFORE])
    assert ownership['candidate_sha256']==before['candidate_sha256']
    slot=ownership['current_owned_name_span'];assert slot['bytes']==12 and ownership['all_bytes_outside_current12_byte_span_andall_pointer_fields_preserved']
    image=NdsImage.open(before['candidate']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==ownership['ARM9_sha256']
    target=bytearray(arm);target[slot['offset']:slot['offset']+12]=bytes.fromhex(slot['target_hex'])
    assert sha(bytes(target))==ownership['proposed_ARM9_sha256']
    ROOT.mkdir(parents=True);ctx=OwnedNameInputContext(before['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    ctx.name_input=slot;ctx.name_input_receipts=[]
    env={**names.__globals__,'SELECTED_ACTORS':[1,2,9,16]}
    exec(compile(before['source_owned_name_adapter'],__file__+'::unchanged-four-identities','exec'),env)
    getters=ctx.execute(env['names']);ctx.machines.pop()
    previous={(r['actor_ID'],r['consumer']):r['text'] for r in before['native_eight_progressive_andfull_getters']['rows']}
    expected={k:('Gerhard Adernkatz' if k[0]==16 else v) for k,v in previous.items()}
    assert {(r['actor_ID'],r['consumer']):r['text'] for r in getters['rows']}==expected
    assert len(ctx.name_input_receipts)==1 and not ctx.machines
    rebound_style=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(arm)},argdefs=style.style_source_proof.__defaults__)
    raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':rebound_style},argdefs=style.native_name_raster.__defaults__)
    labels=[('before-current-header','Gerhard Ardelknatts'),('proposed-header-and-full-getter','Gerhard Adernkatz'),('proposed-surname-field','Adernkatz'),('retained-given-field','Gerhard')]
    sheet=Image.new('RGB',(1024,400),'#263238');draw=ImageDraw.Draw(sheet);planes=[]
    for n,(label,text) in enumerate(labels):
        raw=text.encode('ascii');pixels,events,font=raster(arm,raw)
        assert font==image.read_file('/GRP/KANJI.FNT') and pixels==expected_pixels(arm,font,events)
        emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw)
        assert all(e['y']==0 and e['style']==11 and 0<=e['x'] and e['x']+6<=216 for e in events)
        width=max(e['x']+6 for e in events);ink={(i%216,i//216) for i,v in enumerate(pixels) if v}
        assert ink and max(y for x,y in ink)<13
        path=ROOT/(label+'.bin');path.write_bytes(pixels)
        preview=Image.new('RGB',(216,64));preview.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);png=path.with_suffix('.png');preview.save(png)
        draw.text((4,n*100+3),label+' offline native input',fill='white');sheet.paste(preview.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,n*100+22))
        planes.append(dict(label=label,text=text,raw_hex=raw.hex(),native_glyph_events=events,source_character_codes=codes(raw),
            only_exact_zero_ink_final_ASCII_flush_allowed=True,source_owned_native_flush_events=flushes,
            native_width_including_flush_space=width,native_plane=str(path),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()),
            all_complete_leading_internal_final_glyphs_one_row_in_bounds=True,independent_current_font_pixels_equal=True))
    sheetpath=ROOT/'Gerhard_current_andproposed_complete_names.png';sheet.save(sheetpath)
    save(ROOT/'owned12byte_input8_getters4_complete_name_planes_Blades_protected.json',dict(
        candidate=before['candidate'],candidate_sha256=before['candidate_sha256'],current_ARM9_sha256=sha(arm),proposed_ARM9_sha256=sha(bytes(target)),
        ownership=str(OWNERSHIP),ownership_sha256=sha(OWNERSHIP.read_bytes()),before_names=str(BEFORE),before_names_sha256=sha(BEFORE.read_bytes()),
        source_owned_current_machine_with12byte_research_data_input=MACHINE_ADAPTER,CPU_input_receipts=ctx.name_input_receipts,
        native_eight_getters=getters,only_Gerhard_two_getter_strings_change=True,all_other_getter_strings_preserved=True,
        protected_Blades_bytes_andall_other_RAM_exact=True,all_original_executed_instruction_bytes_andABI_canaries_unowned4MiB_guards_preserved=True,
        original_style11_caller_proof=rebound_style(arm),planes=planes,
        review_sheet=dict(path=str(sheetpath),sha256=sha(sheetpath.read_bytes())),visual_review_pending=True,
        proposed_Gerhard_progressive_andfull_text_equal_andcomplete=True,actual_catalogue_geometry_andcustom_player_names_not_claimed=True,
        CPU_only_owned_data_input_not_current_ROM_change_actual_scene_ornew_ROM_startup=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_name_scene_fullreference_frozen_policy_atomic_andregistered_release_pending=True,
        new_credit=0,new_emulator_runs=0,new_ROMs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OWNERSHIP,BEFORE,Path(style.__file__),Path(__file__)]}))
    print('Owned12-byte CPU input:8 getters /4 complete native planes;Blades exact;no ROM or gameplay change.')
