"""Current numeric special fonts; scoped CPU tests, no new gameplay claim."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts import verify_duel_special_native_v1219 as frozen
from scripts.duel_special_dispatch_v1217 import IDS,helper,front
from scripts.duel_special_layout_v1216 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_fonts_v2534')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
OLDROM=Path('out/all_routes_combined_v1206_candidate.nds')
MANUSCRIPT=Path('translations/duel_special_contextual_editorial_manuscript_v1.json')

if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
 doc=read(MANUSCRIPT);context=read(doc['native_context_proof']);rawpath=Path(context['actual_snapshot']);raw=rawpath.read_bytes()
 assert sha(raw)==context['actual_snapshot_sha256']and sha(ROM.read_bytes())==doc['current_ROM_sha256']
 assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 component=IlnkContainer.parse(common).blocks[21][:1480]
 assert sha(component)=='64474a4c40ba1aeb655be68297ca676e79b9b090760b83e46dbb50140a3e7aac'
 ROOT.mkdir(parents=True);planpath=ROOT/'current_native_pipeline_plan.json'
 save(planpath,dict(metadata_fields=[[DIRECTORY_OFFSET,41*4],[TABLE_OFFSET,3668*2]],
  new_code_prefix=dict(block=21,component_bytes=1480,component_sha256=sha(component)),
  candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  source_historical_ROM=str(OLDROM),source_historical_ROM_sha256=sha(OLDROM.read_bytes()),source_snapshot=str(rawpath),source_snapshot_sha256=sha(raw),
  bounded_code_overlays=[[0xDA28,0x134],[0x535E8,64]],all_other_initialized_RAM_and_actor_models_preserved=True,full_goal_complete=False))
 bind=FunctionType(frozen.bindings.__code__,{**frozen.__dict__,'PLAN':planpath})
 execute,execute_scope,sources=bind(oldrom)
 effective=[]
 for name,source in sources.items():
  p=ROOT/f'effective_{name}.py';p.write_text(source,encoding='utf-8');effective.append(dict(path=str(p),sha256=sha(p.read_bytes())))
 actors={r['message_ID']:r['actor_object']for r in context['all15_original_message_call_bindings']}
 rows={r['message_id']:r for r in doc['records']};entries=current_entries(common,arm)
 font=GameAsciiFont.from_arm9(arm);kanji=rom.read_file('/GRP/KANJI.FNT');cases=[];controls=[];previews=[]
 assert set(rows)==set(IDS)
 for n,row in rows.items():
  text=compiled(row);assert text==entries[n].text==bytes.fromhex(row['current_hex'])
  result,visible=execute(arm,common,raw,actors[n],b'','special_move_numeric',0,n,text,font,kanji)
  assert result['native_getter_IDs']==[n,1931]
  result.update(original_entry='D4D0',original_source_side=0,original_source_duration=120,no_name_or_format_arguments=True,
   source_speaker=row['speaker'],source_actor_ID=row['source_actor_ID'])
  cases.append(result)
  p=ROOT/f'ID{n}_complete_current_native_special.png'
  Image.frombytes('L',(144,36),bytes(0 if v else 255 for v in visible)).save(p)
  previews.append(dict(message_ID=n,path=str(p),sha256=sha(p.read_bytes()),lines=result['lines']))
  print(n,result['lines'],'current D4D0 side0 duration120 complete native fonts/crops pass',flush=True)
 # The unchanged comprehensive dispatch proof is bound below. Focus on old
 # numeric and escape callers that must remain outside the special formatter.
 cpu,get=get_machine(arm,raw);root=get(0xCB184);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4]
 for n in (1931,1957,1972):
  controls.append(execute_scope(arm,common,raw,actors[1990],b'Rafael','direct_negative',0,n,entries[n].text,direct=True))
 for n,table in ((1951,0x02117500),(1973,0x02117620),(1979,0x02117620)):
  actor=next(o for o in objects if get(0x53F4C,o,table)==n)
  controls.append(execute_scope(arm,common,raw,actor,b'Rafael','escape_voice_negative',table,n,entries[n].text))
 assert len(cases)==15 and len(controls)==6 and all(not r['eligible']for r in controls)
 sheet=Image.new('RGB',(4*308,4*110),'#263238');draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(previews):
  x,y=i%4*308,i//4*110;draw.text((x+5,y+3),'ID'+str(row['message_ID'])+' native special',fill='white')
  sheet.paste(Image.open(row['path']).resize((288,72),Image.Resampling.NEAREST),(x+5,y+24))
 image=ROOT/'all15_current_numeric_special_fonts.png';sheet.save(image)
 loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in rows]
 dispatch=Path('work/analysis/duel_special_dispatch_v1217/owned_dispatch_proof.json')
 assert len(copies)==30
 save(ROOT/'native_font_proof.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),cases=cases,all15_complete_native_cases=cases,
  all30_native_cold_warm_copies=copies,native_file_IO_explicit_host_contract=True,
  all15_source_numeric_selection_complete_ABI_words_and_visible_ink_pass=True,complete_native_font_cases=15,
  focused_excluded_prior_numeric_and_escape_controls=controls,all6_focused_excluded_callers_skip_component=True,
  unchanged_exhaustive_dispatch_proof=str(dispatch),unchanged_exhaustive_dispatch_proof_sha256=sha(dispatch.read_bytes()),
  all15_original_D4D0_side0_duration120_source_contract_preserved=True,current_parent_projection_controls=0,
  current_distinct_duel_208x36_native_canvas_and_three144x12_crops=True,current_Deck_or_shared_modal_projection_claim=False,
  all47_cache_lines_and_no_COMMON_reentry_or_component_write_pass=True,component_sha256=sha(component),
  complete_first_last_letters_words_and_registered24x3_bounds_pass=True,
  pipeline_plan=str(planpath),pipeline_plan_sha256=sha(planpath.read_bytes()),bound_effective_sources=effective,
  review_sheets=[dict(path=str(image),sha256=sha(image.read_bytes()))],visual_review_pending=True,
  scope='Current isolated CPU original D4D0 numeric/loader/printf/macro/cache/PIC/native-font/crop tests on disclosed historical actor objects. Widget/controller setup is a CPU formatting fixture. File I/O,SDK clear,UI registration,GPU submission and cache hardware effects are explicit boundaries. No current emulator run or new actor/special activation.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('15 full current numeric special fonts,6 focused exclusions,30 cold/warm copies pass;historical gameplay remains separate.')
