"""Current16 side0 reactions:loader/cache/PIC/fonts/crops and numeric exclusions."""
from pathlib import Path
from types import FunctionType
import inspect
from PIL import Image,ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts import probe_duel_cache_scope_v1150 as scope
from scripts import probe_duel_resident_fonts_v1151 as fonts
from scripts.duel_special_dispatch_v1217 import TABLES,helper,front
from scripts.duel_bark_layout_v1200 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_reaction_fonts_v2525')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
OLDROM=Path('out/all_routes_combined_v1189_candidate.nds')
MANUSCRIPT=Path('translations/duel_reaction_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
 doc=read(MANUSCRIPT);context=read(doc['native_context_proof']);rawpath=Path(context['actual_snapshot']);raw=rawpath.read_bytes()
 assert sha(raw)==context['actual_snapshot_sha256']and sha(ROM.read_bytes())==doc['current_ROM_sha256']
 assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 component=IlnkContainer.parse(common).blocks[21][:1480]
 assert sha(component)=='64474a4c40ba1aeb655be68297ca676e79b9b090760b83e46dbb50140a3e7aac'
 ROOT.mkdir(parents=True);planpath=ROOT/'current_native_pipeline_plan.json'
 save(planpath,dict(metadata_fields=[[DIRECTORY_OFFSET,41*4],[TABLE_OFFSET,3668*2]],owned_ARM9_fields=[[0xDA28,0x134],[0x535E8,64]],
  new_code_prefix=dict(block=21,component_bytes=1480,component_sha256=sha(component)),
  candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  source_historical_ROM=str(OLDROM),source_historical_ROM_sha256=sha(OLDROM.read_bytes()),source_snapshot=str(rawpath),source_snapshot_sha256=sha(raw),
  all_other_initialized_RAM_and_actor_models_preserved=True,full_goal_complete=False))
 class HistoricalSource:
  @staticmethod
  def open(path):
   assert str(path)=='out/all_routes_combined_v1105_candidate.nds'
   return oldrom
 pipeline_source=inspect.getsource(scope.pipeline)
 old="spans=[*plan['metadata_fields'],[0xDA28,0x134]]"
 assert pipeline_source.count(old)==1
 pipeline_source=pipeline_source.replace(old,"spans=[*plan['metadata_fields'],*plan['owned_ARM9_fields']]")
 env={**scope.__dict__,'NdsImage':HistoricalSource,'PLAN_PATH':planpath,'TABLES':TABLES}
 exec(compile(pipeline_source,__file__,'exec'),env);pipeline=env['pipeline']
 font_source=inspect.getsource(fonts.execute)
 old="0 if family == 'challenge' else 1"
 assert font_source.count(old)==1
 font_source=font_source.replace(old,"0 if family in ('positive_action_reaction','negative_action_reaction') else 1")
 env={**fonts.__dict__,'pipeline':pipeline,'PLAN_PATH':planpath}
 exec(compile(font_source,__file__,'exec'),env);execute=env['execute']
 scope_source=inspect.getsource(scope.execute)
 old="side=0 if family=='challenge' else 1"
 assert scope_source.count(old)==1
 scope_source=scope_source.replace(old,"side=0 if family in ('positive_action_reaction','negative_action_reaction') else 1")
 env={**scope.__dict__,'pipeline':pipeline,'PLAN_PATH':planpath,'TABLES':TABLES}
 exec(compile(scope_source,__file__,'exec'),env);execute_scope=env['execute']
 choices={}
 for r in context['all416_unchanged_native_voice_selections']:choices.setdefault(r['message_ID'],r['actor_object'])
 rows={r['message_id']:r for r in doc['records']};entries=current_entries(common,arm)
 font=GameAsciiFont.from_arm9(arm);kanji=rom.read_file('/GRP/KANJI.FNT');cases=[];controls=[];previews=[]
 for n,row in rows.items():
  text=compiled(row);assert text==entries[n].text==bytes.fromhex(row['current_hex'])
  family,table,actor=row['source_family'],row['source_table'],choices[n]
  result,visible=execute(arm,common,raw,actor,b'',family,table,n,text,font,kanji)
  assert result['native_getter_IDs']==[n,1931]
  result.update(original_source_side=0,original_source_duration=60,no_name_or_format_arguments=True)
  cases.append(result)
  controls.append(execute_scope(arm,common,raw,actor,b'',family,table,n,text))
  controls.append(execute_scope(arm,common,raw,actor,b'','direct_negative',0,n,text,direct=True))
  p=ROOT/f'ID{n}_complete_current_native_reaction.png'
  Image.frombytes('L',(144,36),bytes(0 if v else 255 for v in visible)).save(p)
  previews.append(dict(message_ID=n,path=str(p),sha256=sha(p.read_bytes()),lines=result['lines']))
  print(n,result['lines'],'current side0 complete native fonts and all three crops pass',flush=True)
 assert len(cases)==16 and len(controls)==32 and sum(r['eligible']for r in controls)==16
 sheet=Image.new('RGB',(4*308,4*110),'#263238');draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(previews):
  x,y=i%4*308,i//4*110;draw.text((x+5,y+3),'ID'+str(row['message_ID'])+' native side0',fill='white')
  sheet.paste(Image.open(row['path']).resize((288,72),Image.Resampling.NEAREST),(x+5,y+24))
 image=ROOT/'all16_current_side0_timed_reaction_fonts.png';sheet.save(image)
 loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in rows]
 assert len(copies)==32
 save(ROOT/'native_font_proof.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),cases=cases,all16_complete_native_cases=cases,
  all32_native_cold_warm_copies=copies,native_file_IO_explicit_host_contract=True,
  all16_source_numeric_selection_complete_ABI_words_and_visible_ink_pass=True,complete_native_font_cases=16,
  all32_current_selected_and_direct_exclusion_scope_cases=controls,all16_original_side0_selections_enter_and16_numeric_calls_skip_component=True,
  all16_original_side0_duration60_source_contract_preserved=True,current_parent_projection_controls=0,
  current_distinct_duel_208x36_native_canvas_and_three144x12_crops=True,current_Deck_or_shared_modal_projection_claim=False,
  all47_cache_lines_and_no_COMMON_reentry_or_component_write_pass=True,component_sha256=sha(component),
  complete_first_last_letters_words_ASCII_I_ellipses_and_registered24x3_bounds_pass=True,
  pipeline_plan=str(planpath),pipeline_plan_sha256=sha(planpath.read_bytes()),effective_pipeline_source_sha256=sha(pipeline_source.encode()),
  effective_font_source_sha256=sha(font_source.encode()),effective_scope_source_sha256=sha(scope_source.encode()),
  review_sheets=[dict(path=str(image),sha256=sha(image.read_bytes()))],visual_review_pending=True,
  scope='Current isolated CPU side0 table/loader/printf/macro/cache/PIC/native-font/crop tests on a disclosed historical actor model. Widget/controller setup is a CPU formatting fixture. File I/O,SDK clear,UI registration,GPU submission and cache hardware effects are explicit boundaries. No live actor,HP,input,RNG,message or outcome changes and no current emulator run.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('16 full current side0 fonts,32 selected/excluded controls and32 cold/warm copies pass;historical timing/gameplay binding remains separate.')
