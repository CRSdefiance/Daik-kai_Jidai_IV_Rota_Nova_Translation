"""Current text/font binding of preserved V997 confirmations and battle transitions."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.battle_declaration_editorial import current_entries as old_entries
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/verify_battle_declaration_gameplay_v1020.py');MODAL=Path('scripts/verify_battle_declaration_modal_v1016.py')
ROOT=Path('work/analysis/battle_declaration_history_v2497');ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v997_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists();rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');old_digest=sha(OLDROM.read_bytes());hpath=Path('work/analysis/battle_declaration_v1020/actual_gameplay_verification.json');hp=read(hpath);assert hp['candidate_sha256']==old_digest
 spans=((0x53CB0,0x55300),(0x6EE90,0x6F7A4),(0x705F8,0x706A4),(0x7B60,0x7C30),(0x7DAF0,0x7E9A0),(0x81F54,0x82E0C),(0x3CB30,0x3CFC8));assert all(arm[a:b]==oldarm[a:b]for a,b in spans);assert rom.read_file('/GRP/KANJI.FNT')==oldrom.read_file('/GRP/KANJI.FNT');doc=read('translations/battle_declaration_contextual_editorial_manuscript_v1.json');current=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);prior=old_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldarm)
 from scripts.battle_declaration_layout_v996 import compiled
 assert all(current[r['message_id']].text==prior[r['message_id']].text==compiled(r)for r in doc['records'])
 msource=MODAL.read_text();changes={'dk4tool.patch.battle_declaration_editorial':'dk4tool.patch.refit_contextual_spritsail_v1',"ROM=Path('out/all_routes_combined_v997_candidate.nds')":"ROM=Path('out/all_routes_combined_v2284_candidate.nds')",'def verify(folder,label,frame):':'def verify(folder,label,frame,raw_override=None,image_override=None):',"raw=rawp.read_bytes();assert":"raw=rawp.read_bytes()if raw_override is None else raw_override;assert","image=Image.open(shot).convert('RGB');assert":"image=Image.open(shot).convert('RGB')if image_override is None else image_override.convert('RGB');assert",'translations/battle_declaration_editorial_manuscript_v3.json':'translations/battle_declaration_contextual_editorial_manuscript_v1.json','work/analysis/battle_declaration_v995b/native_font_proof.json':'work/analysis/battle_declaration_fonts_v2496/native_font_proof.json',"blocks=IlnkContainer.parse(rom.read_file('/COMMON/MESFILE.DK4')).blocks\n    assert raw.count(blocks[entries[n].block])==1":"oldrom=NdsImage.open('out/all_routes_combined_v997_candidate.nds');from dk4tool.patch.battle_declaration_editorial import current_entries as old_entries\n    old=old_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldrom.read_file('/__arm9__.bin'));assert old[n].text==entries[n].text;blocks=IlnkContainer.parse(oldrom.read_file('/COMMON/MESFILE.DK4')).blocks\n    assert raw.count(blocks[old[n].block])==1",'single_complete_current_native_block_resident':'single_complete_historical_block_and_exact_current_payload_resident'}
 for a,b in changes.items():assert a in msource,a;msource=msource.replace(a,b)
 scope={'__name__':'scoped_current_modal','__file__':__file__};exec(compile(msource,__file__,'exec'),scope);modal=scope['verify']
 source=OLD.read_text();changes={"ROM=Path('out/all_routes_combined_v997_candidate.nds')":"ROM=Path('out/all_routes_combined_v2284_candidate.nds')", "ROOT=Path('work/analysis/battle_declaration_v1020')":"ROOT=Path('work/analysis/battle_declaration_history_v2497')",'from scripts.verify_battle_declaration_modal_v1016 import verify as modal':'# Scoped current modal supplied by successor.', 'assert report[\'ROM_sha256\']==digest':'assert report[\'ROM_sha256\']==old_digest','after,proof=dispatch(arm,ram[frame],request)':'after,proof=dispatch(oldarm,ram[frame],request)', "    ROOT.mkdir()\n    save(ROOT/'actual_gameplay_verification.json',":"    finish(ROOT,rom,oldrom,arm,oldarm,holds,cancels,outcomes,ready,data,reports,fixtures,screens)\n    return\n    save(ROOT/'unused_frozen_save_not_executed.json',"}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 def finish(root,rom,oldrom,arm,oldarm,holds,cancels,outcomes,ready,data,reports,fixtures,screens):
  assert len(holds)==7 and len(cancels)==3 and len(outcomes)==2 and len(fixtures)==14
  controls=[];unique={h['label']:h for h in holds}
  def rejects(action):
   try:action()
   except AssertionError:return True
   raise AssertionError('Corrupted historical modal accepted')
  for label,h in unique.items():
   case='known'if label.startswith('Known')else'ready'if label.startswith('Ready')else'unknown';folder=data[case][0];raw=Path(h['RAM']).read_bytes();image=Image.open(h['capture']).convert('RGB');owner=struct.unpack_from('<I',arm,0x552A0)[0];bad=bytearray(raw);bad[owner+0x2030-0x02000000+1]^=1
   controls.append(dict(case=label,negative='corrupt-resident-initial-letter',rejected=rejects(lambda:modal(folder,label,h['frame'],raw_override=bytes(bad)))))
   lines=h['generated_native_lines'];cells=[(0,0,'erase-leading-letter'),(len(lines)-1,len(lines[-1])-1,'erase-final-glyph')]
   if label=='UnknownEmilio':assert lines[0].endswith(' I');cells.append((0,len(lines[0])-1,'erase-literal-I-at-generated-row-end'))
   for line,col,name in cells:
    badimage=image.copy();x,y=22+col*6,296+line*16;badimage.paste('white',(x,y,x+6,y+11));controls.append(dict(case=label,negative=name,rejected=rejects(lambda:modal(folder,label,h['frame'],image_override=badimage))))
   badimage=image.copy();badimage.putpixel((16,296),(0,8,0));controls.append(dict(case=label,negative='stray-native-left-margin-ink',rejected=rejects(lambda:modal(folder,label,h['frame'],image_override=badimage))))
  assert len(controls)==17 and all(c['rejected']for c in controls);root.mkdir(parents=True)
  sheet=Image.new('RGB',(4*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
  for i,h in enumerate(holds):x,y=i%4*256,i//4*410;draw.text((x+3,y+3),h['label']+' ID'+str(h['message_ID']),fill='white');sheet.paste(Image.open(h['capture']),(x,y+24));h.update(message_id=h['message_ID'],historical_capture_candidate_sha256=old_digest,current_payload_binding_only_no_current_emulator_visit=True)
  a=root/'seven_historical_complete_modal_holds.png';sheet.save(a);sheet=Image.new('RGB',(3*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
  points=[('unknown',6260,'Unknown: No'),('known',6360,'Known: No'),('ready',6160,'Ready run: No'),('unknown',7260,'Unknown: Yes battle'),('known',7160,'Known: Yes battle'),('ready',6860,'Readiness: battle')]
  for i,(case,frame,title)in enumerate(points):x,y=i%3*256,i//3*410;draw.text((x+3,y+3),title,fill='white');sheet.paste(Image.open(data[case][2][frame]),(x,y+24))
  b=root/'six_original_cancellation_and_battle_transitions.png';sheet.save(b);transitions=[*cancels,*outcomes,dict(case='ready',original_readiness_dismissal_enters_battle_without_extra_page=True,states=ready)]
  save(root/'historical_battle_declaration_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),historical_candidate=str(OLDROM),historical_candidate_sha256=old_digest,historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),all22_current_compiled_historical_payloads_equal=True,executed_code_spans_current_old_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],historical_holds=holds,historical_IDs=[1895,1897,1904,1909],scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=transitions,seventeen_negative_controls_current_binding_on_offline_clones=controls,no_new_current_battle_emulator_runs_or_family_visits=True,historical_fixture_replay_uses_original_bound_V997_ARM9_no_guard_bypass=True,all14_exact_fixture_replays=fixtures,capture_reports=reports,stable_body_portrait_and_name_controls=screens,all7_complete_current_native_font_and_historical_RGB_ink_planes_equal=True,review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],scope='Preserved V997 fixture-assisted cold boots;current payload,font and source-exact selection binding. Three No paths,two Yes paths and readiness dismissal verify original transitions. No new current visit,earned war,travel,recruitment or battle-result claim.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 env={'__name__':'scoped_historical_rebinding','__file__':__file__,'old_digest':old_digest,'oldarm':oldarm,'finish':finish,'modal':modal};exec(compile(source,__file__,'exec'),env);env['main']()
 save(ROOT/'producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),modal_helper=str(MODAL),modal_helper_sha256=sha(MODAL.read_bytes()),effective_main_sha256=sha(source.encode()),effective_modal_sha256=sha(msource.encode()),frozen_helpers_captures_and_ROMs_preserved=True,full_goal_complete=False))
