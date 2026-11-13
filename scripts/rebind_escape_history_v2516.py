"""Current paragraph/font binding of two V1189 defeat notices and the historical title return."""
from pathlib import Path
import inspect,struct,textwrap
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.escape_direct_entries import current_entries as old_entries
from dk4tool.rom.nds import NdsImage
from scripts import verify_escape_actual_holds_v1193 as original
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROOT=Path('work/analysis/escape_history_v2516')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
OLDROM=Path('out/all_routes_combined_v1189_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin')
 common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);prior=old_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldarm)
 ids=[*range(1951,1957),*range(1973,1980)]
 assert all(entries[n].text==prior[n].text for n in ids)
 hpath=Path('work/analysis/escape_terminal_v1194/terminal_gameplay_verification.json');historical=read(hpath)
 reportpath=Path(historical['terminal_capture_report']);report=read(reportpath)
 assert sha(OLDROM.read_bytes())==historical['candidate_sha256']==report['ROM_sha256']
 assert sha(reportpath.read_bytes())==historical['terminal_capture_report_sha256']and report['frames']==7802
 assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert historical['source_and_disposable_saves_unchanged']and historical['last_fixture_frame5770_before_duel5772']and len(historical['all31_fixture_replays'])==31
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
 screenshots={r['frame']:r for r in report['frames_captured']}
 spans=[tuple(r)for r in historical['all_source_outcome_selection_RNG_equipment_and_combat_functions_exact']]
 assert all(arm[a:b]==oldarm[a:b]for a,b in spans)
 ref=read('work/analysis/escape_fonts_v2515/native_font_proof.json')
 case=next(r for r in ref['cases']if r['message_ID']==1973)
 assert ref['ARM9_sha256']==sha(arm)
 historical_block=IlnkContainer.parse(oldrom.read_file('/COMMON/MESFILE.DK4')).blocks[prior[1973].block]
 class CurrentFont:
  @staticmethod
  def open(path):return rom
 raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
 code=inspect.getsource(original.main)
 start=code.index('        ram_path=');end=code.index('    a,b=[Image.open',start)
 body=textwrap.dedent(code[start:end])
 body=body.replace('raw=ram_path.read_bytes();assert','raw=ram_path.read_bytes()if raw_override is None else raw_override;assert')
 body=body.replace("image=Image.open(image_path).convert('RGB')","image=Image.open(image_path).convert('RGB')if image_override is None else image_override.convert('RGB')")
 body=body.replace("block=IlnkContainer.parse(common).blocks[entries[1973].block]","block=historical_block")
 body=body.replace('unique_whole_resident_COMMON_block_exact','unique_whole_historical_block_and_current_notice_payload_exact')
 function='def verify(frame,raw_override=None,image_override=None):\n    holds=[]\n'+textwrap.indent(body,'    ')+'\n    return holds[0]\n'
 env={**original.__dict__,'rom':rom,'arm':arm,'common':common,'entries':entries,'case':case,'raster':raster,'historical_block':historical_block}
 exec(compile(function,__file__,'exec'),env);verify=env['verify']
 holds=[verify(frame)for frame in(6912,6922)]
 for hold in holds:
  frame=hold['frame'];assert hold['RAM_sha256']==snapshots[frame]['sha256']and hold['capture_sha256']==screenshots[frame]['PNG_sha256']
  hold.update(message_id=1973,historical_capture_candidate_sha256=historical['candidate_sha256'],current_payload_font_binding_only_no_current_emulator_visit=True)
 controls=[]
 def rejected(action):
  try:action()
  except AssertionError:return True
  raise AssertionError('Corrupted escape notice accepted')
 first=holds[0];raw=Path(first['RAM']).read_bytes();image=Image.open(first['capture']).convert('RGB')
 owner,wrapped=[struct.unpack_from('<I',arm,at)[0]for at in(0x552A0,0x54450)]
 for address,label in((owner+0x2030,'corrupt-resident-source-Admiral'),(wrapped,'corrupt-wrapped-initial-Admiral')):
  bad=bytearray(raw);bad[address-BASE+1]^=1
  controls.append(dict(negative=label,rejected=rejected(lambda:verify(6912,raw_override=bytes(bad)))))
 lines=case['lines'];assert lines[1].startswith('Everyone,')
 for line,column,label in((0,0,'erase-initial-Admiral-A'),(1,0,'erase-Everyone-E'),(len(lines)-1,len(lines[-1])-1,'erase-final-exclamation')):
  bad=image.copy();x,y=22+column*6,296+line*16;bad.paste('white',(x,y,x+6,y+11))
  controls.append(dict(negative=label,rejected=rejected(lambda:verify(6912,image_override=bad))))
 bad=image.copy();bad.putpixel((16,296),(0,8,0))
 controls.append(dict(negative='stray-ink-in-uniform-left-margin',rejected=rejected(lambda:verify(6912,image_override=bad))))
 assert len(controls)==6 and all(r['rejected']for r in controls)
 transitions=[]
 for item in historical['ordinary_A_defeat_to_GameOver_to_title']:
  frame=item['frame'];ram=Path(snapshots[frame]['path']).read_bytes()
  assert sha(ram)==snapshots[frame]['sha256']==item['RAM_sha256']
  assert sha(Path(item['capture']).read_bytes())==item['capture_sha256']==screenshots[frame]['PNG_sha256']
  transitions.append(dict(item,historical_only_not_current_aftermath_translation_or_title_regression=True))
 assert [r['frame']for r in transitions]==[7042,7162,7382,7802]
 for state in historical['natural_duel_HP_evolution']:
  data=Path(snapshots[state['frame']]['path']).read_bytes();assert sha(data)==state['RAM_sha256']
  cpu,get=get_machine(arm,data);actors=get(0xCB184)
  assert[get(0x7E19C,p)for p in(actors+0x19E4,actors+4+32*32)]==state['own_enemy_captain_HP']
 ROOT.mkdir(parents=True)
 sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,hold in enumerate(holds):draw.text((i*256+4,3),'Historical V1189 ID1973',fill='white');sheet.paste(Image.open(hold['capture']),(i*256,24))
 a=ROOT/'two_historical_complete_escape_holds.png';sheet.save(a)
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,item in enumerate(transitions):draw.text((i*256+4,3),str(item['frame'])+' '+item['visually_reviewed_state'],fill='white');sheet.paste(Image.open(item['capture']),(i*256,24))
 b=ROOT/'four_historical_defeat_to_title_transitions.png';sheet.save(b)
 save(ROOT/'historical_escape_current_binding.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  historical_candidate=str(OLDROM),historical_candidate_sha256=sha(OLDROM.read_bytes()),historical_proof=str(hpath),historical_proof_sha256=sha(hpath.read_bytes()),
  historical_capture_report=str(reportpath),historical_capture_report_sha256=sha(reportpath.read_bytes()),historical_holds=holds,historical_IDs=[1973],
  scoped_historical_cancellation_and_battle_transitions_freshly_rechecked=transitions,six_negative_controls_current_binding_on_offline_clones=controls,
  all13_current_and_historical_notice_payloads_equal=True,no_new_current_battle_emulator_runs_or_family_visits=True,
  original_First_Mate_actor18_and_actual_captain1_unchanged=True,natural_historical_own_enemy_HP=[0,45],
  original31_pre_duel_fixture_audits_hash_bound_not_needlessly_repeated=True,one_original_shield_transfer_to_inventory_hash_bound=historical['one_original_shield_inventory_transfer'],
  source_selector_combat_equipment_RNG_and_consequence_code_current_old_equal=[dict(start=x,end=y,sha256=sha(arm[x:y]))for x,y in spans],
  complete_current228x64_font_and_historical_RGB_ink_blank_masks_equal=True,
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in(a,b)],effective_native_hold_helper_sha256=sha(function.encode()),
  scope='Preserved V1189 isolated defeat sample.31 disclosed positive-starting-HP/contact fixtures and one native shield transfer precede combat;none during or after the original duel. Two actual1973 holds bind current complete notice/fonts. Natural defeat then ordinary A advances abandon-ship/loss,Game Over and title;these four transition captures are historical,not current translation/startup approvals or earned progression.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Two historical complete notice holds,6 corruption controls and4 historical defeat/title transitions pass;no current emulator runs.')
