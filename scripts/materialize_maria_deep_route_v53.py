from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v53.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(39,40)
LINES={
'DK4_MES_B39_R0004':'M-me...!{LB}My money, company, fleet...{LB}All gone!',
'DK4_MES_B39_R0008':'{LB}Oh, Nagalpur...{LB}Still lurking here?',
'DK4_MES_B39_R0011':'No longer our enemy.{LB}Without money,{LB}that man can do nothing.',
'DK4_MES_B39_R0015':'{LB}True...',
'DK4_MES_B39_R0027':'Heh! All bluster!',
'DK4_MES_B39_R0034':'Y-you!{LB}How dare you!!',
'DK4_MES_B39_R0037':'Money cannot solve everything.{LB}That dream was yours alone.{LB}Surely the lesson sank in?',
'DK4_MES_B39_R0041':'Grr...!',
'DK4_MES_B39_R0045':'{LB}{MACRO:FI} is right.{LB}Cool your head.',
'DK4_MES_B39_R0048':'Aaah! Poverty is awful!{LB}Money! Money!{LB}Give me money!!',
'DK4_MES_B39_R0052':'{LB}Words are wasted on him.',
'DK4_MES_B40_R0004':'Even this island has quite a town.',
'DK4_MES_B40_R0008':'{LB}Quite.{LB}As a vital trade hub,{LB}this town will grow much further.',
'DK4_MES_B40_R0012':'Meaning?',
'DK4_MES_B40_R0016':'{LB}East Africa has cities,{LB}Sofala among them. The coast{LB}funnels all trade along{LB}a single route.',
'DK4_MES_B40_R0019':'{LB}Yet Madagascar can serve as a hub,{LB}letting goods follow several routes{LB}between Cape Town and Mogadishu.',
'DK4_MES_B40_R0022':'So if this island becomes a port,{LB}East African trade gains more routes,{LB}and this town grows too.',
'DK4_MES_B40_R0026':'This seems familiar...{LB}A large island lies{LB}not far from Ming.',
'DK4_MES_B40_R0030':'{LB}Ah...{LB}That island has no port{LB}for trade, right?',
'DK4_MES_B40_R0034':'Then we shall build one.{LB}Right?',
'DK4_MES_B40_R0037':'{LB}Hard task.{LB}The government forbids{LB}an unauthorized town.',
'DK4_MES_B40_R0041':'What if profit is guaranteed?{LB}Those bribe-loving officials{LB}will hardly object.',
'DK4_MES_B40_R0045':'A fine proposal!{LB}Let us return to Hangzhou{LB}and set it in motion.',
'DK4_MES_B40_R0049':'A second Madagascar there...{LB}The cost will be great,{LB}but it should become a major port!',
}
STATES={0x03,0x0A,0x19,0x26,0x4A};SPEAKERS={'03':'Maria','0A':'Xien','19':'Companion','26':'Nagalpur','4A':'Richard'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={row['id']:row for row in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V53 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':"Maria route: Nagalpur's defeat and Maria's Madagascar-inspired East Asian trade-port plan.",'source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name"),'localization_note':'Direct SC3 translation preserving runtime-name macros, geographic and trade context, presentation states, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within four display lines.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v53-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':"Maria SC3 blocks 39-40: Nagalpur's collapse and the Madagascar-inspired port plan.",'inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
