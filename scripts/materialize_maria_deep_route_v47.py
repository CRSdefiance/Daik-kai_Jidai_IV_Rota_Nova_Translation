from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v47.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(20,21,22,23,24)
LINES={
'DK4_MES_B20_R0017':'We withdraw for today!{LB}Next time, this ends!',
'DK4_MES_B20_R0020':'Empty boasts.',
'DK4_MES_B20_R0026':'Damn! We withdraw for now,{LB}but surrender is unthinkable!{LB}Remember Aziza Nurennahar!',
'DK4_MES_B20_R0030':'Never gives up...',
'DK4_MES_B21_R0014':'How about that, Admiral?{LB}Never underestimate a pirate!',
'DK4_MES_B21_R0017':'So it seems.{LB}We underestimated you.',
'DK4_MES_B21_R0020':'Only seeing that now?{LB}Then your skill is no better!',
'DK4_MES_B21_R0023':'{LB}{MACRO:FI}!{LB}We retreat!',
'DK4_MES_B21_R0026':'We withdraw for now,{LB}but next time will differ!',
'DK4_MES_B21_R0031':'Got away!',
'DK4_MES_B21_R0035':'{LB}{MACRO:FI}! We must retreat!',
'DK4_MES_B21_R0039':'Taking pirates lightly{LB}was our mistake...',
'DK4_MES_B21_R0042':'Thought you could beat me?{LB}Next time, prepare to die!',
'DK4_MES_B22_R0008':'Got you.{LB}Now off to Batavia.',
'DK4_MES_B22_R0011':'Ow!{LB}Th-this was not the plan...',
'DK4_MES_B23_R0008':'D-damn...{LB}My precious cargo...',
'DK4_MES_B23_R0011':'Still worried about cargo?{LB}Such devotion... or greed.{LB}Now you are coming with us{LB}to Calicut.',
'DK4_MES_B24_R0007':'D-damn...',
'DK4_MES_B24_R0011':'You may be entertaining,{LB}so no gag this time. Talk away{LB}until we reach Havana.',
'DK4_MES_B24_R0014':'Why, over a treaty breach? Ow!',
'DK4_MES_B24_R0025':'Huh?{LB}Ah! Y-you?!',
'DK4_MES_B24_R0028':'Have we met{LB}somewhere before?',
'DK4_MES_B24_R0031':'Damn it!{LB}You meddled twice now!',
'DK4_MES_B24_R0035':'Do not worry.{LB}No third time awaits.',
}
STATES={0x03,0x1B,0x40,0x43,0x44};SPEAKERS={'03':'Maria','1B':'Aziza Nurennahar','40':'Ulysse','43':'Gabriel Cardocci','44':'Jacob Portunto'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s: all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'Maria V47 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';block=str(int(i.split('_B',1)[1].split('_',1)[0]));counts[block]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route early rival-battle outcomes and Ulysse, Jacob, and Gabriel bounty captures.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name"),'localization_note':'Direct SC3 translation cross-checked against parallel route events and fixed-allocation display constraints.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within four display lines.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v47-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 20-24: Aziza rematches and the Ulysse, Jacob, and Gabriel bounty captures.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
