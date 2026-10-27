"""Current COMMON->native scoped cache->PIC->full font/crop tests;no live injection."""
from pathlib import Path
from types import FunctionType
import inspect
from PIL import Image,ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from scripts import probe_duel_cache_scope_v1150 as scope
from scripts import probe_duel_resident_fonts_v1151 as fonts
from scripts.duel_bark_front_v1201 import TABLES
from scripts.duel_editorial_layout_v1155 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/static_duel_fonts_v2504');PLAN=Path('work/analysis/static_duel_context_v2502/current_native_pipeline_plan.json');MANUSCRIPT=Path('translations/static_duel_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 assert not ROOT.exists();plan=read(PLAN);arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes();assert sha(arm)==plan['target_ARM9_sha256']and sha(common)==plan['target_COMMON_sha256'];rom=NdsImage.open(plan['current_ROM']);assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256'];raw=Path(plan['source_snapshot']).read_bytes();assert sha(raw)==plan['source_snapshot_sha256'];doc=read(MANUSCRIPT);records={r['message_id']:r for r in doc['records']};entries=current_entries(common,arm);assert all(compiled(r)==entries[n].text==bytes.fromhex(r['current_hex'])for n,r in records.items())
 code=inspect.getsource(scope.pipeline);a="spans=[*plan['metadata_fields'],[0xDA28,0x134]]";assert code.count(a)==1;code=code.replace(a,"spans=[*plan['metadata_fields'],*plan['owned_ARM9_fields']]");env={**scope.__dict__,'PLAN_PATH':PLAN,'TABLES':TABLES};exec(compile(code,__file__,'exec'),env);pipeline=env['pipeline'];execute=FunctionType(fonts.execute.__code__,{**fonts.execute.__globals__,'pipeline':pipeline,'PLAN_PATH':PLAN},argdefs=fonts.execute.__defaults__);execute_scope=FunctionType(scope.execute.__code__,{**scope.execute.__globals__,'pipeline':pipeline,'PLAN_PATH':PLAN,'TABLES':TABLES},argdefs=scope.execute.__defaults__);execute_scope.__kwdefaults__=scope.execute.__kwdefaults__
 c=read(doc['native_context_proof']);actors={}
 for r in c['all624_current_original_actor_voice_selections']:actors.setdefault(r['message_ID'],r['actor_object'])
 font=GameAsciiFont.from_arm9(arm);kanji=rom.read_file('/GRP/KANJI.FNT');cases=[];scope_cases=[];representative=[];previews=[];ROOT.mkdir(parents=True)
 for n,row in records.items():
  table=row['source_table'];actor=actors[n];family='challenge'if n<1939 else'acceptance'if n<1945 else'threat';scope_cases.append(execute_scope(arm,common,raw,actor,b'Clifford',family,table,n,compiled(row)))
  for i,name in enumerate((b'Clifford',b'ABCDEFGHIJKLMNOP',b'\x82\x65ernando')if row['native_argument_count']else(b'Clifford',)):
   text=compiled(row).replace(b'%s',name);result,visible=execute(arm,common,raw,actor,name,family,table,n,text,font,kanji);assert result['native_getter_IDs']==[n,1931];result.update(message_ID=n,name_case='ordinary-layout-label'if i==0 else'16_ASCII_cell_layout_stress'if i==1 else'mixed_CP932_ASCII_layout_stress',layout_name_is_CPU_argument_only_no_live_name_replacement=True);cases.append(result)
   p=ROOT/f'ID{n}_variant{i}_complete_native.png';Image.frombytes('L',(144,36),bytes(0 if v else255 for v in visible)).save(p);previews.append(dict(message_ID=n,path=str(p),sha256=sha(p.read_bytes()),lines=result['lines']))
   if i==0:representative.append(dict(message_ID=n,**{k:v for k,v in result.items()if k!='message_ID'}))
  print(n,'current native loader,PIC,painters and all three crops pass',flush=True)
 # Keep both portrait escape tables and direct static IDs excluded by the current extended front.
 registered={r['message_id']:r for r in read(c['registered_manuscript'])['records']};cpu,get=get_machine(arm,raw);root=get(0xCB184);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4];excluded={}
 for table in(0x02117500,0x02117620):
  for obj in objects:n=get(0x53F4C,obj,table);excluded.setdefault(n,(obj,table))
 assert len(excluded)==13
 for n,(actor,table)in sorted(excluded.items()):scope_cases.append(execute_scope(arm,common,raw,actor,b'Clifford','escape_negative',table,n,compiled(registered[n])))
 for n,row in records.items():scope_cases.append(execute_scope(arm,common,raw,actors[1931],b'Clifford','direct_negative',0,n,compiled(row),direct=True))
 assert len(cases)==36 and len(representative)==20 and len(scope_cases)==53 and sum(r['eligible']for r in scope_cases)==20
 priorpath=Path('work/analysis/duel_resident_fonts_v1151/cache_resident_complete_fonts.json');prior=read(priorpath);assert len(prior['cases'])==1356;priorplan=read('work/analysis/duel_cache_payload_v1144/cache_prefix_research_plan.json');oldarm=Path(priorplan['target_ARM9']).read_bytes();assert sha(oldarm)==prior['ARM9_sha256'];assert all(arm[a:b]==oldarm[a:b]for a,b in((0xD458,0xD538),(0xD5404,0xD56E0),(0xD16B4,0xD19C0)));assert kanji==NdsImage.open(priorplan['source_ROM']).read_file('/GRP/KANJI.FNT');assert sha(__import__('dk4tool.formats.ilnk',fromlist=['IlnkContainer']).IlnkContainer.parse(common).blocks[21][:1480])==priorplan['new_code_prefix']['component_sha256']
 from scripts.duel_postmacro_layout_v1134 import layout
 for case in prior['cases']:
  n=case['message_ID'];template=compiled(records[n]);text=bytes.fromhex(case['expanded_hex']);name=bytes.fromhex(case['name_hex']);assert template.replace(b'%s',name)==text;output,lines=layout(text);assert output.hex()==case['formatted_hex']and lines==case['lines']
 sheets=[]
 for page in range(2):
  sheet=Image.new('RGB',(3*298,6*104),'#263238');draw=ImageDraw.Draw(sheet)
  for i,r in enumerate(previews[page*18:(page+1)*18]):x,y=i%3*298,i//3*104;draw.text((x+4,y+3),'ID'+str(r['message_ID'])+' native static duel',fill='white');sheet.paste(Image.open(r['path']).resize((288,72),Image.Resampling.NEAREST),(x+4,y+25))
  p=ROOT/f'all36_current_native_page{page+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
 loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in records];assert len(copies)==40
 save(ROOT/'native_font_proof.json',dict(candidate=plan['current_ROM'],candidate_sha256=plan['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),all20_complete_native_cases=representative,all40_native_cold_warm_copies=copies,native_file_IO_explicit_host_contract=True,all20_source_numeric_selection_complete_ABI_words_and_visible_ink_pass=True,complete_native_font_cases=36,cases=cases,all53_current_scope_cases=scope_cases,all20_static_selected_and13_portrait_escape_plus20_direct_excluded=True,current_parent_projection_controls=0,current_distinct_duel_208x36_native_canvas_and_three144x12_crops=True,current_Deck_or_shared_modal_projection_claim=False,all1480_component_bytes_exact_to_prior1356_full_font_matrix=True,prior1356_font_proof=str(priorpath),prior1356_font_proof_sha256=sha(priorpath.read_bytes()),all1356_name_template_generated_layout_bindings_rechecked_without_repeating_unchanged_rasters=True,whole24x3_complete_words_leading_trailing_ASCII_CP932_glyphs_bounds_canaries_ABI_and47_cache_lines_pass=True,scope='Current CPU-only selector/loader/printf/macro/cache/PIC/painter/crop executions. File I/O,SDK clear,UI registration,GPU submission and hardware cache effects are explicit boundaries. Existing actor models remain unchanged;display widget and name arguments are declared CPU layout fixtures. No new emulator run or live message/name injection.',current_pipeline_source_sha256=sha(code.encode()),current_pipeline_plan=str(PLAN),current_pipeline_plan_sha256=sha(PLAN.read_bytes()),review_sheets=sheets,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('36 current full native fonts;53 selected/excluded controls;40 cold/warm copies;1356 unchanged prior font/layout bindings pass.',flush=True)
