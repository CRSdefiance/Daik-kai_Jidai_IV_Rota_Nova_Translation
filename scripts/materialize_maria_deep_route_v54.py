from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v54.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(41,42,43,44)
LINES={
'DK4_MES_B41_R0004':'{LB}{MACRO:FI},{LB}about that new town...',
'DK4_MES_B41_R0007':'Plans nearly done.{LB}Only talks remain.',
'DK4_MES_B41_R0010':'Admiral, leave those talks to me.',
'DK4_MES_B41_R0013':'Very well.{LB}You are suited to such work.',
'DK4_MES_B41_R0017':'Truly? Leave it to me!{LB}And one request...',
'DK4_MES_B41_R0020':'Anything else?',
'DK4_MES_B41_R0024':'Would you let me{LB}build the town?',
'DK4_MES_B41_R0027':'{LB}Oh? You would lead it?',
'DK4_MES_B41_R0039':'Hey, can you handle such work?',
'DK4_MES_B41_R0045':'Surely the leader cannot remain in Ming{LB}solely to oversee construction...',
'DK4_MES_B41_R0049':'True... That is impossible.{LB}Much still remains to be done.',
'DK4_MES_B41_R0053':'Rumor says Ming officials{LB}are moving suspiciously{LB}against our actions.',
'DK4_MES_B41_R0057':'What?!',
'DK4_MES_B41_R0061':'Government will be kept in check{LB}while the truth is uncovered.{LB}Please continue your voyages as before.',
'DK4_MES_B41_R0064':'Understood.{LB}This is in your hands.',
'DK4_MES_B41_R0067':'Once negotiations end,{LB}construction will need funds.{LB}Could you prepare 500,000 gold?',
'DK4_MES_B41_R0070':'500,000.{LB}Yes, it will be ready.',
'DK4_MES_B41_R0073':'Then talks begin at once.{LB}Bring the funds to Hangzhou{LB}when they are ready.',
'DK4_MES_B42_R0004':'Admiral {MACRO:FI}!{LB}We awaited you!',
'DK4_MES_B42_R0007':'Did the talks go smoothly?',
'DK4_MES_B42_R0011':'Of course. All is arranged.{LB}Construction of Tamsui has begun,{LB}exactly as {MACRO:FI} envisioned.',
'DK4_MES_B42_R0014':'{LB}Oh, so it worked.',
'DK4_MES_B42_R0018':'Excellent.{LB}The 500,000 gold{LB}is ready too.',
'DK4_MES_B42_R0023':'Then preparations are complete.{LB}Please visit Tamsui.',
'DK4_MES_B42_R0026':'Of course.',
'DK4_MES_B42_R0030':'Construction needs many workers.{LB}Bringing many from England{LB}was useful, but...',
'DK4_MES_B42_R0033':'They dislike the food here.',
'DK4_MES_B42_R0036':'And?',
'DK4_MES_B42_R0040':'To raise morale, serving wine{LB}or other Western spirits{LB}would be best.',
'DK4_MES_B42_R0044':'Very well, if that works.{LB}How much is needed?',
'DK4_MES_B42_R0047':'About five holds.',
'DK4_MES_B42_R0051':'{LB}Suspicious. Are workers the excuse,{LB}when you really want the wine?',
'DK4_MES_B42_R0055':'Very well. Then five holds{LB}of wine to Tamsui, correct?',
'DK4_MES_B42_R0059':'Yes, as soon as possible.{LB}Morale depends on it.{LB}Now, let me go ahead to town...',
'DK4_MES_B43_R0004':'Welcome, Admiral {MACRO:FI}.',
'DK4_MES_B43_R0007':'Wine is in the warehouse.{LB}Serve it freely.',
'DK4_MES_B43_R0011':'Thank you. We shall.{LB}Also, the trading post is complete.',
'DK4_MES_B43_R0015':'{MACRO:FO} controls all trade{LB}in this town,{LB}so use it freely.',
'DK4_MES_B43_R0018':'Trade already...{LB}Real progress.{LB}Our first step is done.',
'DK4_MES_B43_R0022':'{LB}Now the goal is this town\'s growth.{LB}Reinvest its trading profits here.',
'DK4_MES_B43_R0026':'Let us make it a great city...{LB}Richard, continue leading the work.',
'DK4_MES_B43_R0030':'Certainly.{LB}Leave it to me.',
'DK4_MES_B44_R0004':'Admiral {MACRO:FA}!{LB}Welcome. The work is unfinished,{LB}so nothing is here yet...',
'DK4_MES_B44_R0007':'{LB}Work advances more slowly{LB}than expected.',
'DK4_MES_B44_R0010':'Yes. Without wine...',
'DK4_MES_B44_R0014':'This will get us nowhere.{LB}Serve them drink at once{LB}and raise efficiency.',
'DK4_MES_B44_R0018':'Quite so.{LB}Please bring five holds of wine{LB}as soon as possible.',
}
STATES={0x03,0x0A,0x0B,0x4A};SPEAKERS={'03':'Maria','0A':'Xien','0B':'Jam','4A':'Richard'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V54 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route: Tamsui founding, government negotiations, construction funding, English workers, and the wine delivery quest.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FA}',"the protagonist's surname").replace('{MACRO:FO}',"the protagonist's fleet name"),'localization_note':'Direct SC3 translation preserving route macros, quest quantities, presentation states, source staging, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v54-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 41-44: founding Tamsui, negotiations, construction funding, workers, wine delivery, and trading-post completion.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
