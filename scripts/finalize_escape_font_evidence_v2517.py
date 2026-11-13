"""Exact current case counts and162 scoped interjection-boundary decisions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_font_review_v2517')
SOURCE=Path('work/analysis/escape_fonts_v2515/native_font_proof.json')
if __name__=='__main__':
 assert not ROOT.exists()
 proof=deepcopy(read(SOURCE));cases=proof['cases'];assert len(cases)==1423
 unique_text=len({c['formatted_hex']for c in cases});unique_planes=len({c['native_font_sha256']for c in cases})
 assert unique_text==unique_planes==1021
 decisions=[]
 for i,case in enumerate(cases):
  lines=case['lines']
  weak=[j for j,line in enumerate(lines[:-1])if line.split()[-1].strip('.,!?;:').lower()in{'a','an','the','to','of','with','for','from','on','in','as','at','and'}]
  orphan=len(lines)>1 and(len(lines[-1].split())==1 or len(lines[-1].encode('cp932'))<=8)
  assert not orphan
  if weak:
   assert case['message_ID']==1954 and weak==[0]and len(lines)==2 and lines[0].endswith('Come on,')and lines[1]=='lads, cover them!'
   decisions.append(dict(case_index=i,message_ID=1954,variant=case['variant'],lines=lines,native_font_sha256=case['native_font_sha256'],
    disposition='freshly-reviewed-exact-case-retention',reason='Come on is a complete interjection,not on awaiting a prepositional object. The source rallying call is naturally followed by a comma and vocative lads. These exact generated rows preserve that spoken pause,all words and glyphs. No authored alignment,orphan row,missing-letter waiver or general weak-word waiver is introduced.'))
 assert len(decisions)==162 and decisions[-1]['variant']['kind']=='current-immutable-compact-label'
 for item in proof['review_sheets']:assert sha(Path(item['path']).read_bytes())==item['sha256']
 proof.update(unique_native_font_planes=1021,base1417_unique_native_font_planes=1015,current6_ASCII_Faticia_unique_native_font_planes=6,
  all162_exact_current_interjection_boundary_decisions=decisions,all2_font_sheets_and19_record_or_current_name_previews_viewed=True,
  source_combined_font_proof=str(SOURCE),source_combined_font_proof_sha256=sha(SOURCE.read_bytes()),
  combined_unique_count_supersedes_inherited_base1015_counter=True,visual_review_pending=False,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
 ROOT.mkdir(parents=True);save(ROOT/'native_font_proof.json',proof)
 save(ROOT/'visual_formatting_review.json',dict(current_native_expansion_font_cases=1423,unique_complete_font_planes=1021,
  logical_messages=13,current_ASCII_name_supplement_previews=6,all19_previews_on2_sheets_viewed=True,
  all162_exact_current_interjection_boundary_decisions=decisions,blocking_errors=0,unwaived_warnings=0,
  no_global_or_missing_glyph_waiver=True,review_sheets=proof['review_sheets'],
  no_current_emulator_or_gameplay_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('1423 current expansion/font cases,1021 unique planes,19 viewed previews and162 exact Come on decisions pass.')
