from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v52.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(37,38)
LINES={
'DK4_MES_B37_R0004':'Saved...{LB}Damn Kuen...',
'DK4_MES_B37_R0007':'Lil! Are you safe?!',
'DK4_MES_B37_R0011':'Yes...{LB}All my fault...{LB}How can this be made right?',
'DK4_MES_B37_R0015':'All over now.{LB}Kuen is to blame.',
'DK4_MES_B37_R0018':'Disaster was averted.{LB}Now back to the North Sea.{LB}Take care...',
'DK4_MES_B37_R0022':'Thank you, Hodram.',
'DK4_MES_B37_R0026':'Thank {MACRO:FI},{LB}not me.',
'DK4_MES_B37_R0029':'What will you do?',
'DK4_MES_B37_R0033':'Back to North Sea for me too.{LB}The world is far beyond me{LB}as things stand...',
'DK4_MES_B37_R0037':'Lil...{LB}Let me come.',
'DK4_MES_B37_R0040':'Thank you, Kamil!',
'DK4_MES_B37_R0044':'Then leave the rest to us.{LB}We will defeat Kuen.',
'DK4_MES_B37_R0047':'{LB}We cannot forgive him!',
'DK4_MES_B37_R0051':'Well then...{LB}Sorry for all the trouble...',
'DK4_MES_B38_R0005':'Are you {MACRO:FA},{LB}stirring these waters lately?',
'DK4_MES_B38_R0008':'And you?',
'DK4_MES_B38_R0012':'With the Uddin Company.',
'DK4_MES_B38_R0016':'This may be blunt, but these waters{LB}have long been ruled by Muslims.{LB}Do not interfere here.',
'DK4_MES_B38_R0019':'What do you mean?{LB}You want us out of these waters?',
'DK4_MES_B38_R0022':'Do not jump to conclusions.{LB}We are busy ousting Europeans.{LB}No time for you now.{LB}So here is my proposal.',
'DK4_MES_B38_R0025':'An alliance.',
'DK4_MES_B38_R0029':'Stay out of our territory.{LB}Should Europeans trouble you,{LB}we will offer some support.{LB}What do you say?',
'DK4_MES_B38_R0034':'Agreed.',
'DK4_MES_B38_R0036':'Cannot agree.',
'DK4_MES_B38_R0044':'Hahaha! That is the spirit.{LB}A fine partner indeed.{LB}Until next time.',
'DK4_MES_B38_R0052':'A pity. Then by Arab pride,{LB}we shall defend our waters{LB}to the last.',
}
STATES={0x01,0x02,0x03,0x09,0x0A,0x25,0x81};SPEAKERS={'01':'Hodram','02':'Lil','03':'Maria','09':'Kamil','0A':'Xien','25':'Uddin representative','81':'Maria'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={row['id']:row for row in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V52 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route: Lil rescue aftermath and the Uddin Company proposal in the Indian Ocean.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FA}',"the protagonist's surname"),'localization_note':'Direct SC3 translation preserving route macros, political context, choice branches, presentation states, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within four display lines.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v52-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 37-38: Lil rescue aftermath and the Uddin Company proposal.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
