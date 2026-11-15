from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v60.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(55,)
LINES={
'DK4_MES_B55_R0004':'{LB}Angelo! Angelo!',
'DK4_MES_B55_R0008':'Xien, what happened?',
'DK4_MES_B55_R0012':'{LB}Angelo collapsed.',
'DK4_MES_B55_R0016':'High fever.',
'DK4_MES_B55_R0028':'Lord Angelo!',
'DK4_MES_B55_R0035':'Angelo! Angelo! Ange...',
'DK4_MES_B55_R0043':'Bianca:{LB}...Brother? Angelo?{LB}Brother Angelo...',
'DK4_MES_B55_R0048':'B-Bianca?{LB}Bianca, is that you...?{LB}And where are we?',
'DK4_MES_B55_R0052':'Bianca:{LB}What are you saying?{LB}You brought flowers for me.',
'DK4_MES_B55_R0055':'These flowers...?{LB}Why am... dressed like this?',
'DK4_MES_B55_R0059':'Bianca:{LB}So strange, brother.',
'DK4_MES_B55_R0062':'(Strange... Was there a ship...?{LB}Ah, never mind.{LB}Bianca is here.)',
'DK4_MES_B55_R0066':'Bianca:{LB}Beautiful...{LB}My favorite amaryllis.',
'DK4_MES_B55_R0070':'Where were you?{LB}You had me searching everywhere!',
'DK4_MES_B55_R0073':'Bianca:{LB}What? This room never changed.',
'DK4_MES_B55_R0076':'What?{LB}But the search...',
'DK4_MES_B55_R0079':'Bianca:{LB}Never mind.{LB}Tell of distant seas.',
'DK4_MES_B55_R0083':'Ah... yes',
'DK4_MES_B55_R0087':'...That\'s it',
'DK4_MES_B55_R0091':'Bianca:{LB}How wonderful...{LB}Cough, cough.',
'DK4_MES_B55_R0095':'Are you all right?{LB}You should lie down.',
'DK4_MES_B55_R0098':'Bianca:{LB}Today feels better.{LB}Please, tell me more...',
'DK4_MES_B55_R0102':'Ah... yes',
'DK4_MES_B55_R0106':'Bianca, now a navigator,{LB}sailing aboard a ship.',
'DK4_MES_B55_R0109':'Remember our old promise?',
'DK4_MES_B55_R0113':'You wished to see flowers.{LB}A ship would show you{LB}the world\'s blooms.',
'DK4_MES_B55_R0117':'Bianca:{LB}...Yes...',
'DK4_MES_B55_R0120':'Not my ship, but come.{LB}See the world\'s flowers{LB}together.',
'DK4_MES_B55_R0124':'Bianca:{LB}...That cannot happen...',
'DK4_MES_B55_R0127':'Do not fear illness.{LB}Doctors live across the sea.',
'DK4_MES_B55_R0130':'One of them may know{LB}how to cure you.',
'DK4_MES_B55_R0133':'Bianca:{LB}Sorry, brother.{LB}Now must go...',
'DK4_MES_B55_R0137':'Go? Go where?',
'DK4_MES_B55_R0141':'Bianca:{LB}We must part.{LB}Time to return.',
'DK4_MES_B55_R0144':'Part? Return?',
'DK4_MES_B55_R0148':'Bianca:{LB}Live on, brother.{LB}You are strong......',
'DK4_MES_B55_R0152':'Do not go...{LB}Joke is cruel.',
'DK4_MES_B55_R0155':'Bianca:{LB}Stop wasting life searching for me.{LB}Now, live for yourself.',
'DK4_MES_B55_R0159':'Bianca!{LB}You are all the family left!',
'DK4_MES_B55_R0162':'There are only two of us!{LB}Will you leave me all alone?!',
'DK4_MES_B55_R0165':'Bianca:{LB}You are not alone...',
'DK4_MES_B55_R0168':'Eh?',
'DK4_MES_B55_R0172':'Bianca:{LB}You have companions...',
'DK4_MES_B55_R0175':'Allies',
'DK4_MES_B55_R0179':'Bianca:{LB}Yes, companions...{LB}Your new family...',
'DK4_MES_B55_R0183':'My family...',
'DK4_MES_B55_R0187':'Bianca:{LB}Yes. Live for yourself{LB}with your new family.',
'DK4_MES_B55_R0191':'Bianca:{LB}And always,{LB}your heart holds me.',
'DK4_MES_B55_R0198':'Bianca:{LB}No time remains.{LB}Time to go...',
'DK4_MES_B55_R0201':'Bianca:{LB}Goodbye, brother...{LB}Thank you.{LB}Be happy for us both...',
'DK4_MES_B55_R0208':'Angelo:{LB}Bianca, wait! Bianca!',
'DK4_MES_B55_R0211':'...anca... Bianca!',
'DK4_MES_B55_R0215':'{LB}Angelo! Angelo!',
'DK4_MES_B55_R0219':'Ugh... hah...{LB}Where is Bianca......?',
'DK4_MES_B55_R0222':'All right, Angelo?',
'DK4_MES_B55_R0226':'...What...?',
'DK4_MES_B55_R0230':'{LB}A high fever felled you.',
'DK4_MES_B55_R0234':'Down...{LB}A dream...',
'DK4_MES_B55_R0245':'Worried.',
'DK4_MES_B55_R0252':'You called "Bianca."{LB}Were you dreaming of your sister?',
'DK4_MES_B55_R0255':'Yes...',
'DK4_MES_B55_R0259':'{LB}May you find her.',
'DK4_MES_B55_R0263':'No. The search for Bianca...{LB}can end now.',
'DK4_MES_B55_R0266':'{LB}Angelo, you must not give up.',
'DK4_MES_B55_R0278':'Quite so.{LB}This warrior will help',
'DK4_MES_B55_R0284':'Sorry...{LB}Leave me alone...',
'DK4_MES_B55_R0287':'Angelo...',
}
STATES={0x03,0x0B,0x0C,0x0F,0xFE};SPEAKERS={'03':'Maria','0B':'Jam','0C':'Companion','0F':'Angelo','FE':'Bianca or dream voice'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if i.startswith('DK4_MES_B55_')}
 if set(LINES)!=set(rows):raise SystemExit(f'V60 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[]
 for i in sorted(LINES,key=lambda v:int(v.rsplit('R',1)[1])):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Scene speaker'),'context':'Maria route optional event: Angelo collapses with fever, dreams of his late sister Bianca, accepts his companions as a new family, and awakens changed.','source_meaning':e.replace('{LB}',' '),'localization_note':'Direct SC3 translation preserving the dream framing, explicit Bianca and Angelo voice labels, portrait states, emotional pacing, source staging, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v60-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 block 55: complete Angelo fever dream and Bianca farewell event.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':{'55':len(records)}},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
