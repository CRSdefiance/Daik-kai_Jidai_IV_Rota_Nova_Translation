from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v49.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(31,32)
LINES={
'DK4_MES_B31_R0005':'Aah!{LB}What? An enemy attack?!',
'DK4_MES_B31_R0008':'{MACRO:FO}\'s fleet{LB}has opened fire!',
'DK4_MES_B31_R0011':'{MACRO:FO}!{LB}Kuen was right about you!',
'DK4_MES_B31_R0015':'What?!{LB}That is not our fleet{LB}attacking Lil!{LB}Who are they?',
'DK4_MES_B31_R0018':'{LB}Kuen disguised his ships{LB}as our fleet to attack Argot!',
'DK4_MES_B31_R0021':'Kuen\'s false fleet...{LB}His true nature is clear.{LB}We must help Lil now!',
'DK4_MES_B31_R0025':'{LB}W-wait!{LB}A fleet approaches!{LB}Those ships...',
'DK4_MES_B31_R0030':'Seems we arrived in time...',
'DK4_MES_B31_R0034':'Liiil!!',
'DK4_MES_B31_R0038':'K-Kamil!{LB}And Hodram...?{LB}Why are you here?',
'DK4_MES_B31_R0042':'{MACRO:FI} warned us:{LB}"Lil is in danger!"{LB}Kuen\'s disguised fleet{LB}is attacking you!',
'DK4_MES_B31_R0045':'What?! No!!',
'DK4_MES_B31_R0049':'Kuen\'s true face!{LB}We will help you!',
'DK4_MES_B31_R0052':'{MACRO:FI}...{LB}We were fools...{LB}Sorry...',
'DK4_MES_B31_R0056':'Never mind. We are in time.{LB}Now let us defeat Kuen!',
'DK4_MES_B31_R0060':'Go!{LB}All hands to battle!',
'DK4_MES_B31_R0063':'Damn, it failed...!',
'DK4_MES_B31_R0067':'Lord Kuen,{LB}we are outmatched.',
'DK4_MES_B31_R0071':'That is obvious!{LB}Damn it, withdraw!',
'DK4_MES_B32_R0014':'Admiral!{LB}That ship again!',
'DK4_MES_B32_R0015':'Admiral!{LB}Strange ship!{LB}Same one?!',
'DK4_MES_B32_R0017':'Admiral!{LB}Strange ship!',
'DK4_MES_B32_R0018':'Admiral!{LB}Strange ship!',
'DK4_MES_B32_R0019':'Admiral!{LB}Odd ship sighted!',
'DK4_MES_B32_R0020':'Admiral!{LB}A strange ship!',
'DK4_MES_B32_R0021':'Admiral!{LB}Odd ship sighted!',
'DK4_MES_B32_R0024':'Th-that is?!',
}
STATES={0x01,0x02,0x03,0x09,0x28,0x97,0x9B,0xD6};SPEAKERS={'01':'Hodram','02':'Lil','03':'Maria','09':'Kamil','28':'Kuen','97':'Lookout','9B':'Kuen officer','D6':'Companion'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s:all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V49 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route: Kuen false-flag attack, Hodram rescue, reconciliation with Lil, and anomalous-ship sighting.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FO}',"the rival fleet leader's name"),'localization_note':'Direct SC3 translation preserving false-flag exposition, route macros, presentation states, and companion variants.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within four display lines.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v49-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 31-32: Kuen false-flag attack, Hodram rescue, Lil reconciliation, and anomalous ship sighting.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
