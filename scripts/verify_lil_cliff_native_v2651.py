"""Current fixed/story macro,raw-source guards and complete216x64 native glyphs."""
import struct
from pathlib import Path
from types import FunctionType
from copy import deepcopy
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.script.translation_batch import materialize_translation_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster as old_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_cliff_native_v2651');DOC=Path('translations/lil_cliff_contextual_editorial_manuscript_v1.json');BASE=0x02000000
def expand(arm,common,raw,plan,body):
 cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244);identity=get(0x2434C,0x94);assert 0<=identity<207;actor=root+0x19E4 if identity==captain else root+4+identity*32;before=bytes(cpu.mem_read(BASE,0x400000));cpu.hook_add(UC_HOOK_CODE,lambda u,a,s,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=BASE+0x242CC,end=BASE+0x242CC);cases=[]
 for phase in range(4):
  inp,out=0x02660000+phase,0x02662000;cpu.mem_write(inp-16,b'\xA5'*2080);cpu.mem_write(inp,body+b'\0');input_before=bytes(cpu.mem_read(inp-16,2080));cpu.mem_write(out-16,b'\xA5'*4128);call(cpu,0x242C8,(out,inp,actor),instruction_limit=400000);value=bytes(cpu.mem_read(out,4096)).split(b'\0')[0];assert value==body and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(inp-16,2080))==input_before;assert bytes(cpu.mem_read(out-16,16))==b'\xA5'*16 and bytes(cpu.mem_read(out+len(value)+1,4095-len(value)))==b'\xA5'*(4095-len(value));cases.append(dict(input_alignment=phase,output_hex=value.hex(),complete_input_output_canaries_and4MiB_exact=True))
 return dict(mapped_source_presentation=0x94,original_actor_resolution=identity,actor_object=actor,captain=captain,cases=cases,original_242C8_macro_and_242CC_UI_boundary=True,no_source_model_event_or_RNG_mutation=True)
if __name__=='__main__':
 ctx=CurrentContext(DOC,'out/all_routes_combined_v829_candidate.nds',ROOT);doc=read(DOC);row=doc['records'][0];source=ctx.rom.read_file('/data/SC2.DK4');clean=NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4');profile=get_dialogue_profile(doc['dialogue_profile']);compiled=encode_fixed_dialogue(bytes.fromhex(row['raw_source']['hex']),row['english'],profile);assert compiled.encoded.hex()==row['current_hex']and len(compiled.encoded)==48 and compiled.padding_bytes==4 and not compiled.diagnostics
 logical=row['english'].split('}',1)[1].removesuffix('{PAD}').encode('ascii');wrapped=compiled.encoded[1:];pipelines=[dict(kind=kind,**ctx.execute(expand,body))for kind,body in[('logical',logical),('compiled-protected-and-padded',wrapped)]];assert sum(len(c['cases'])for c in pipelines)==8
 class FontROM:
  @staticmethod
  def open(path):assert str(path)=='work/clean.nds';return ctx.rom
 raster=FunctionType(old_raster.__code__,{**old_raster.__globals__,'NdsImage':FontROM},argdefs=old_raster.__defaults__);pixels,events,font=raster(ctx.arm,wrapped);assert pixels==expected_pixels(ctx.arm,font,events);visible=[e for e in events if e['code']!=32];assert[e['code']for e in visible]==[ord(c)for c in wrapped.decode('ascii')if c not in' \n'];assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in visible);assert len(visible)==len({(e['x'],e['y'])for e in visible});origins={y:min(e['x']for e in visible if e['y']==y)for y in sorted({e['y']for e in visible})};assert origins=={0:0,16:0};assert visible[0]['code']==ord('Y')and visible[-1]['code']==ord('.')and all(not p for p in pixels[216*28:])
 rejected=[]
 for label,kind,value in[('wrong-raw','raw','95'+row['raw_source']['hex'][2:]),('wrong-declared-prefix','prefix','95'),('missing-speaker','english',row['english'].replace('{SPEAKER:94}','')),('wrong-speaker','english',row['english'].replace('94','95')),('missing-PAD','english',row['english'].replace('{PAD}','')),('overflow','english','{SPEAKER:94}'+'A'*100+'{PAD}'),('macro-added','english',"{SPEAKER:94}{MACRO:FI} You're set on it.{PAD}"),('wrong-source-hash','hash','0'*64)]:
  bad=deepcopy(doc)
  if kind=='raw':bad['records'][0]['raw_source']['hex']=value
  elif kind=='prefix':bad['records'][0]['raw_source']['presentation_prefix_hex']=value
  elif kind=='hash':bad['source_file_sha256']=value
  else:bad['records'][0]['english']=value
  try:
   m=materialize_translation_batch(bad,clean)[0];encode_fixed_dialogue(bytes.fromhex(m['source_hex']),m['english'],profile)
  except(ValueError,AssertionError):rejected.append(label)
  else:raise AssertionError(label)
 preview=ROOT/'R73_complete_native_story.png';Image.frombytes('L',(216,64),bytes(0 if p else 255 for p in pixels)).resize((648,192),Image.Resampling.NEAREST).save(preview);save(ROOT/'native_font_proof.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),SC2_sha256=sha(source),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),encoded_hex=compiled.encoded.hex(),formatted_markup=compiled.formatted_markup,padding_bytes=compiled.padding_bytes,complete_native_story_glyphs=events,visible_origins_by_row=origins,native_plane_sha256=sha(pixels),all_complete216x64_native_independent_pixels_and_first_final_glyphs_match=True,all8_current_macro_alignment_cases=pipelines,raw_encoder_negative_inputs_rejected=rejected,review_sheets=[dict(path=str(preview),sha256=sha(preview.read_bytes()))],pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_actor_models_and_main4MiB_unchanged=True,protected_break_and_four_padding_spaces_no_blank_page=True,scope='Current original story parser at8alignment/kind cases and complete native216x64 immediate font plane on mapped94 body;UI construction is a CPU boundary. Historical initialized RAM is used only under bounded immutable overlays. No new current emulator visit,portrait/page transition or hardware claim.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('R73 current8macro alignment cases,complete native216x64 glyphs,raw/fixed negative guards and exact48-byte compilation pass.')
