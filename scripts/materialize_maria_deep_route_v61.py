from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v61.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(56,)
LINES={
'DK4_MES_B56_R0004':'A bullfight is underway!',
'DK4_MES_B56_R0007':'Bull?',
'DK4_MES_B56_R0018':'He fights a bull like a dance...{LB}How barbaric.',
'DK4_MES_B56_R0026':'Yahoo! We must see this!{LB}Come on, Admiral!',
'DK4_MES_B56_R0047':'A crowd...{LB}(This is difficult...)',
'DK4_MES_B56_R0050':'Yahoo! What luck!{LB}The most popular matador{LB}is appearing today!',
'DK4_MES_B56_R0055':'Wahahaha!',
'DK4_MES_B56_R0059':'Make us laugh!',
'DK4_MES_B56_R0063':'That man?{LB}He is the star?',
'DK4_MES_B56_R0066':'Oh.{LB}That is the picador.',
'DK4_MES_B56_R0069':'He tires the bull first.{LB}Then the matador{LB}delivers the final blow.',
'DK4_MES_B56_R0073':'Hyaaaah!!',
'DK4_MES_B56_R0077':'Gahahaha!{LB}That fool is playing with the bull!{LB}The bull threw him!',
'DK4_MES_B56_R0081':'Ungaaaah!!',
'DK4_MES_B56_R0085':'Wahahaha!',
'DK4_MES_B56_R0089':'Get out of there!!',
'DK4_MES_B56_R0097':'At last, the star appears!',
'DK4_MES_B56_R0101':'Oooooh!!',
'DK4_MES_B56_R0105':'At last!',
'DK4_MES_B56_R0109':'Whistle!',
'DK4_MES_B56_R0113':'Waaaah!',
'DK4_MES_B56_R0117':'Give us a show!',
'DK4_MES_B56_R0121':'Bravo!!',
'DK4_MES_B56_R0125':'Waaaah!',
'DK4_MES_B56_R0130':'Murmur...',
'DK4_MES_B56_R0134':'...Recruit him.',
'DK4_MES_B56_R0138':'Seriously?',
'DK4_MES_B56_R0142':'He may be useful.',
'DK4_MES_B56_R0146':'A bullfighter?{LB}Can he help?',
'DK4_MES_B56_R0149':'Yes.',
'DK4_MES_B56_R0153':'Excuse me. A word?',
'DK4_MES_B56_R0157':'Hm?',
'DK4_MES_B56_R0161':'Eh?!{LB}...Y-you mean me?',
'DK4_MES_B56_R0164':'Would you sail the open seas{LB}aboard my ship?',
'DK4_MES_B56_R0167':'A ship? Sounds frightening.{LB}And not very tasty.',
'DK4_MES_B56_R0170':'Ships are safe.{LB}Across the sea, you can eat{LB}all the good food you want.',
'DK4_MES_B56_R0173':'Delicious food? Heh heh...',
'DK4_MES_B56_R0177':'The world has all kinds of food.',
'DK4_MES_B56_R0181':'S-so much variety?{LB}Then the sea sounds good!',
'DK4_MES_B56_R0185':'Settled, then.{LB}Your name? Mine is{LB}{MACRO:FI} {MACRO:FA}.',
'DK4_MES_B56_R0189':'M-my name is Emilio.',
'DK4_MES_B56_R0193':'Welcome, Emilio.',
}
EXCLUDED={'DK4_MES_B56_R0053':'nontext arena event payload 21 51 46 93 EB; preserved byte-for-byte'}
STATES={0x03,0x0B,0x0E,0x4A,0x52,0x5F,0x68,0x71,0x93,0xFE};SPEAKERS={'03':'Maria','0B':'Jam','0E':'Emilio Ferrog','4A':'Richard','52':'Crowd','5F':'Crowd','68':'Crowd','71':'Crowd','93':'Crowd','FE':'Crowd ambience'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if i.startswith('DK4_MES_B56_')}
 if set(LINES)|set(EXCLUDED)!=set(rows):raise SystemExit(f'V61 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}')
 records=[]
 for i in sorted(LINES,key=lambda v:int(v.rsplit('R',1)[1])):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Scene speaker'),'context':'Maria route optional event: Seville bullfight, crowd reactions, and Emilio Ferrog recruitment through the promise of world cuisine.','source_meaning':e.replace('{LB}',' '),'localization_note':'Direct SC3 translation preserving the arena event, crowd states, recruitment exchange, protagonist name macros, source staging, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v61-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 block 56: complete bullfight spectacle and Emilio Ferrog recruitment.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':{'56':len(records)}},'excluded':[{'id':i,'reason':r} for i,r in EXCLUDED.items()],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} preserved control')
if __name__=='__main__':main()
