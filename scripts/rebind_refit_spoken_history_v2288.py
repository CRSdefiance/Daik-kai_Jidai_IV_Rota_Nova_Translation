"""Historical V834 helper/Rename holds rebound to current reviewed complete text."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_spoken_history_v2288');OLD=Path('work/analysis/refit_dialogue_v834/actual_gameplay_verification.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);history=read(OLD);oldrom=NdsImage.open(history['candidate']);oldarm=oldrom.read_file('/__arm9__.bin');plan=read('work/analysis/refit_spritsail_payload_v2278/payload_plan.json');arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,arm,plan['directory_sha256']);kanji=NdsImage.open('out/all_routes_combined_v2171_candidate.nds').read_file('/GRP/KANJI.FNT');assert kanji==oldrom.read_file('/GRP/KANJI.FNT')
 from dk4tool.dialogue.font_audit import GameAsciiFont
 assert GameAsciiFont.from_arm9(arm).glyphs==GameAsciiFont.from_arm9(oldarm).glyphs
 owner,printed,wrapped=[struct.unpack_from('<I',oldarm,n)[0]for n in(0x552A0,0x5444C,0x54450)];matrix=read('work/analysis/refit_spoken_layouts_v2280c/native_layout_matrix.json')['cases'];cases=[];panels=[]
 for hold in history['actual_complete_dialogue_holds']:
  case,frame,n=hold['case'],hold['frame'],hold['message_id'];receipt=history['receipts'][case];rptpath=Path(receipt['report']);assert sha(rptpath.read_bytes())==receipt['sha256'];rpt=read(rptpath);assert rpt['ROM_sha256']==history['candidate_sha256']and rpt['cold_boot']and not rpt['savestate_loaded']
  snap=next(r for r in rpt['read_only_capture_RAM_snapshots']if r['frame']==frame);raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']and snap['read_only_export']
  cstring=lambda ptr:raw[ptr-0x02000000:ptr-0x02000000+512].split(b'\0')[0]
  assert cstring(owner+0x2030)==entries[n].text
  visible=cstring(wrapped);lines=[r.strip().decode('cp932')for r in visible.split(b'\n')];number=6 if n==1263 else 2 if n==1267 else None
  if n!=1246:
   match=next(r for r in matrix if r['message_id']==n and r['number']==number);assert visible.hex()==match['formatted_hex']
  arg={1263:'６'.encode('cp932'),1267:'２ days'.encode('cp932'),1246:'１８８０'.encode('cp932')}.get(n);expected=entries[n].text%((arg,)if arg is not None else());assert cstring(printed)==expected and b' '.join(visible.split())==b' '.join(expected.split())
  shot=next(r for r in rpt['frames_captured']if r['frame']==frame);p=Path(shot['path']);assert sha(p.read_bytes())==shot['PNG_sha256'];image=Image.open(p).convert('RGB');plane=independent_font(arm,kanji,lines);ink={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1};actual={(x,y)for y in range(294,366)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)};assert actual==ink
  cases.append(dict(case=case,frame=frame,message_ID=n,current_complete_template_and_formatted_bytes_equal_historical_resident_buffers=True,current525_matrix_output_equal=n!=1246,already_fresh_context_only=n==1246,independent_current_font_complete_foreground_and_blank_ink_equal=True,source_report=str(rptpath),source_report_sha256=sha(rptpath.read_bytes()),source_RAM_sha256=sha(raw)))
  panel=Image.new('RGB',(256,412),'#263238');ImageDraw.Draw(panel).text((4,4),f'Historical V834 {case} {frame}',fill='white');panel.paste(image,(0,28));panels.append(panel)
 assert len(cases)==10 and {r['message_ID']for r in cases}=={1246,1256,1263,1264,1265,1266,1267}
 sheet=Image.new('RGB',(1024,1236),'#263238')
 for i,panel in enumerate(panels):sheet.paste(panel,(i%4*256,i//4*412))
 p=ROOT/'historical_refit_spoken_sheet.png';sheet.save(p)
 save(ROOT/'historical_spoken_binding.json',dict(research_ARM9_sha256=sha(arm),research_COMMON_sha256=sha(common),historical_proof=str(OLD),historical_proof_sha256=sha(OLD.read_bytes()),cases=cases,all10_historical_holds_cover6_reviewed_IDs_plus_already_fresh1246=True,qualified_helper_uses_original_disclosed_three_byte_historical_room_role_fixture=True,no_current_helper_discount_rename_visit_or_earned_assignment_claim=True,historical_price1880_and96_calendar_ticks_evidence_inherited_only=True,all12_spoken_have_separate_current_native_layout_coverage=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(historical_holds=10,reviewed_IDs=6,context_only_IDs=[1246],sheet_pending=True))
