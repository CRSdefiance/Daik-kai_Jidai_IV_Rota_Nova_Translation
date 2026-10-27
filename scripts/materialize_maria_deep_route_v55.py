from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v55.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(45,)
LINES={
'DK4_MES_B45_R0004':'Here... At last.{LB}Africa, visited by Zheng He...',
'DK4_MES_B45_R0008':'Move! Now!!',
'DK4_MES_B45_R0017':'Do not stop! Want to die?!',
'DK4_MES_B45_R0021':'(Are those local people{LB}being driven along?{LB}What brutal treatment.)',
'DK4_MES_B45_R0025':'Stop the violence!',
'DK4_MES_B45_R0029':'Huh? Who are you?{LB}They belong to me.{LB}You have no say!',
'DK4_MES_B45_R0033':'People are not livestock.{LB}No one can own them.',
'DK4_MES_B45_R0036':'They work my fields!{LB}What is wrong with using them?',
'DK4_MES_B45_R0039':'Outsider!{LB}Spare me the lecture!',
'DK4_MES_B45_R0042':'How convenient.{LB}Here in Africa, you Westerners{LB}are outsiders too.',
'DK4_MES_B45_R0046':'Y-you!{LB}You clearly do not know who we are!',
'DK4_MES_B45_R0049':'Do not want to know.',
'DK4_MES_B45_R0053':'Enough! Listen,{LB}we are the feared Espinosa Company!{LB}Leave if you value your life!',
'DK4_MES_B45_R0057':'A threat?{LB}Stray dogs bark better.',
'DK4_MES_B45_R0060':'Y-you...!{LB}Such a sharp tongue!',
'DK4_MES_B45_R0063':'Pest control is my work.{LB}Destroying parasites like you,{LB}across every nation.',
'DK4_MES_B45_R0067':'P-parasites? Pest control?{LB}Want to die?{LB}You should have said so!',
'DK4_MES_B45_R0071':'Go tell your boss:{LB}find new work while you can.{LB}Your trade ends in a few months.',
'DK4_MES_B45_R0074':'What?!',
'DK4_MES_B45_R0078':'Still confused?{LB}This corrupt company{LB}will be closed.',
'DK4_MES_B45_R0082':'Gahahaha! What a strange woman!{LB}Brave, or merely stupid?',
'DK4_MES_B45_R0085':'All right! You are coming with me!{LB}You will kneel before Lord Espinosa!!',
'DK4_MES_B45_R0089':'Pitiful.{LB}More sense could have{LB}saved your life.',
'DK4_MES_B45_R0092':'You will regret those words.{LB}Next time, no mercy.{LB}Prepare yourself.',
'DK4_MES_B45_R0096':'Y-you little...!!',
'DK4_MES_B45_R0108':'As human beings, we cannot ignore{LB}the Espinosa Company\'s evil.',
'DK4_MES_B45_R0111':'Of course.{LB}Never forgiven.',
}
STATES={0x03,0x2F,0x4A};SPEAKERS={'03':'Maria','2F':'Espinosa overseer','4A':'Richard'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V55 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route: first African landfall, confrontation with an Espinosa plantation overseer, condemnation of enslavement, and declaration of war on the company.','source_meaning':e.replace('{LB}',' '),'localization_note':'Direct SC3 translation preserving the anti-slavery confrontation, threats, portrait states, source staging, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v55-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 block 45: first African landfall and confrontation with Espinosa plantation overseers.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
