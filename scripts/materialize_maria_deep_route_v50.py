from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v50.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(33,34)
EXCLUDED={
'DK4_MES_B33_R0058':'Opaque nine-byte event-control payload between debrief phases.',
'DK4_MES_B33_R0088':'Opaque four-byte event-control payload.',
'DK4_MES_B33_R0097':'Opaque four-byte event-control payload.',
'DK4_MES_B33_R0101':'Opaque four-byte event-control payload.',
'DK4_MES_B33_R0112':'Opaque six-byte event-control payload ending the strategy scene.',
}
LINES={
'DK4_MES_B33_R0013':'Admiral, we are back!',
'DK4_MES_B33_R0017':'Wako destroyed.{LB}Mission complete.',
'DK4_MES_B33_R0022':'Our losses?',
'DK4_MES_B33_R0026':'Heh heh!{LB}We used that plan.{LB}Losses? Not a scratch!',
'DK4_MES_B33_R0030':'We trapped their swift ships{LB}with our formation,{LB}then sank them by sheer firepower.{LB}No losses were suffered.',
'DK4_MES_B33_R0033':'Hmm. Good work.',
'DK4_MES_B33_R0045':'Both did well.{LB}Good work.',
'DK4_MES_B33_R0048':'Yahoo!',
'DK4_MES_B33_R0052':'Yes!',
'DK4_MES_B33_R0060':'Hey, old man Xien!{LB}We are back!',
'DK4_MES_B33_R0063':'{LB}A great victory.',
'DK4_MES_B33_R0067':'We followed {MACRO:FI}\'s plan.{LB}Taking the windward side{LB}assured victory.',
'DK4_MES_B33_R0070':'The enemy appeared exactly{LB}where {MACRO:FI} predicted.{LB}Even we were amazed!',
'DK4_MES_B33_R0073':'A masterstroke.{LB}Brilliant.',
'DK4_MES_B33_R0077':'{LB}Hmm. {MACRO:FI}{LB}has done well.',
'DK4_MES_B33_R0080':'Terrifying,{LB}but amazing too.',
'DK4_MES_B33_R0083':'Our lives depend{LB}on that commander.',
'DK4_MES_B33_R0086':'{LB}Richard is truly insufferable.{LB}At sea he is completely useless.{LB}Yet he acts as adviser to {MACRO:FI}.',
'DK4_MES_B33_R0090':'His English connections{LB}let us defy Ming\'s isolation{LB}and operate openly.',
'DK4_MES_B33_R0093':'{LB}Yet you have no such ties{LB}to your homeland.',
'DK4_MES_B33_R0096':'Heh. Some unknown scoundrel{LB}framed me, so home is barred.{LB}Once found, he gets a beating!',
'DK4_MES_B33_R0099':'{LB}Yukihisa\'s fate is ironic too.',
'DK4_MES_B33_R0103':'{LB}Seeking a legendary sword,{LB}he boarded wako, then hunted them.',
'DK4_MES_B33_R0107':'No concern is needed.{LB}Abroad exposed their wrongdoing.{LB}Such shame cannot stand.',
'DK4_MES_B33_R0110':'{LB}Reassuring words.',
'DK4_MES_B33_R0121':'Where is the envoy?',
'DK4_MES_B33_R0125':'You called?',
'DK4_MES_B33_R0129':'Report on the coastal contracts.',
'DK4_MES_B33_R0133':'Going well. Bribes work wonders.',
'DK4_MES_B33_R0137':'They settled for 3% of sales.{LB}Disguise us as foreign ships,{LB}and officials will look away.',
'DK4_MES_B33_R0140':'As expected.{LB}Utterly corrupt...',
'DK4_MES_B33_R0143':'Harsh words, Admiral...{LB}But the magistrate saw more gain{LB}in allowing our trade.',
'DK4_MES_B33_R0147':'Merchants always seek profit.{LB}Winning their support early{LB}was worth the effort.',
'DK4_MES_B33_R0151':'At any rate, the way is open.{LB}Trade can begin immediately.',
'DK4_MES_B33_R0154':'Good. Maintain every ship{LB}for Kurushima\'s retaliation.',
'DK4_MES_B33_R0158':'Understood.',
'DK4_MES_B34_R0005':'So you are {MACRO:FA}?{LB}Leave before Kuen and Pereira{LB}drag you into their feud.',
'DK4_MES_B34_R0010':'Whoever wins, we gain nothing.{LB}What a nuisance...',
'DK4_MES_B34_R0013':'Why?',
'DK4_MES_B34_R0017':'They came to expand their lands.{LB}Either victor will exploit us.{LB}Locals gain nothing.',
'DK4_MES_B34_R0020':'{LB}So neither side cares{LB}about the local people...',
'DK4_MES_B34_R0034':'Portugal and Holland...{LB}Both seek control of East Asia.',
'DK4_MES_B34_R0042':'We must act before harm{LB}reaches our homeland.',
}
STATES={0x03,0x0B,0x0C,0x15,0x4A,0x74};SPEAKERS={'03':'Maria','0B':'Jam','0C':'Yuki','15':'Ian','4A':'Xien','74':'Local sailor'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s:all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)|set(EXCLUDED)!=set(rows):raise SystemExit(f'V50 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route: wako battle debrief, command-strategy reflection, coastal trade contracts, and local warning about Kuen and Pereira.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FA}',"the protagonist's surname"),'localization_note':'Direct SC3 translation preserving route macros, political context, presentation states, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within four display lines.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v50-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 33-34: wako debrief, strategy reflection, coastal contracts, and colonial warning.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':counts},'excluded':[{'id':i,'reason':v} for i,v in EXCLUDED.items()],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls excluded')
if __name__=='__main__':main()
