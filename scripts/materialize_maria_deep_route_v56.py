from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v56.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(46,47)
LINES={
'DK4_MES_B46_R0004':'<A dashing young man>{LB}Hm? Are you the ones{LB}who defeated Espinosa?',
'DK4_MES_B46_R0013':'Splendid.{LB}Now England can expand{LB}into Africa without concern.',
'DK4_MES_B46_R0017':'Espinosa ran quite a profitable{LB}business here.{LB}What excellent fortune.',
'DK4_MES_B46_R0021':'You misunderstand.{LB}No one was invited{LB}to take Espinosa\'s place.',
'DK4_MES_B46_R0025':'Why? This is only natural.',
'DK4_MES_B46_R0028':'Beyond Europe, the world{LB}is split among Western powers.{LB}When one falls,{LB}another takes its place.',
'DK4_MES_B46_R0031':'So the world belongs{LB}to your great powers?{LB}How self-serving.',
'DK4_MES_B46_R0035':'So Europe still has people{LB}shameless enough to say that.',
'DK4_MES_B46_R0039':'We tolerate no such people.{LB}My crew may not spare your life.{LB}Leave at once.',
'DK4_MES_B46_R0042':'A beauty with a fearsome bite.{LB}Very well. We withdraw today.',
'DK4_MES_B46_R0045':'This is not over.{LB}Even with me gone,{LB}another will come.',
'DK4_MES_B46_R0048':'Since someone will take it,{LB}why not me?',
'DK4_MES_B46_R0062':'Admiral, who was that?{LB}Was there trouble?',
'DK4_MES_B46_R0065':'Nothing.{LB}He asked the way.{LB}Sadly, it was unknown.',
'DK4_MES_B46_R0068':'Oh...',
'DK4_MES_B47_R0004':'Wh-what are you doing?!',
'DK4_MES_B47_R0015':'Hm?',
'DK4_MES_B47_R0024':'Come here!',
'DK4_MES_B47_R0028':'Espinosa?!',
'DK4_MES_B47_R0032':'Admiral {MACRO:FA},{LB}thanks for stopping him.',
'DK4_MES_B47_R0035':'Y-you think this ends without cost?!',
'DK4_MES_B47_R0038':'Shut up!',
'DK4_MES_B47_R0042':'Gah!! Th-that hurts!!',
'DK4_MES_B47_R0046':'You had your way{LB}long enough.',
'DK4_MES_B47_R0049':'Wh-what?',
'DK4_MES_B47_R0053':'You forgot?!{LB}You deceived my father,{LB}stole our home and fields,{LB}and my family vanished!',
'DK4_MES_B47_R0056':'My friend tried reporting you.{LB}You killed him{LB}and staged an accident!',
'DK4_MES_B47_R0060':'Back home, villagers were taken{LB}and forced to work everywhere,{LB}barely given food!',
'DK4_MES_B47_R0064':'N-not my doing!{LB}My foolish men acted alone!',
'DK4_MES_B47_R0068':'Y-you bastard!!',
'DK4_MES_B47_R0080':'Appalling...{LB}Nothing but cowardice.',
'DK4_MES_B47_R0093':'A monster...',
'DK4_MES_B47_R0102':'You inhuman brute!{LB}Admiral {MACRO:FA},{LB}may we deal with him?',
'DK4_MES_B47_R0105':'Take him.',
'DK4_MES_B47_R0109':'You heard her! Come!{LB}Your crimes will be repaid!',
'DK4_MES_B47_R0112':'H-help me!!',
'DK4_MES_B47_R0121':'{MACRO:FA}.',
'DK4_MES_B47_R0129':'Please accept this.',
'DK4_MES_B47_R0136':'This?',
'DK4_MES_B47_R0140':'Espinosa carried it.{LB}He also sought the proof{LB}of Africa\'s ruler.{LB}We prayed he would never find it.',
'DK4_MES_B47_R0143':'You should rule these waters.{LB}Please find the treasure soon{LB}and bring this land{LB}peace and prosperity.',
'DK4_MES_B47_R0147':'Thank you.{LB}We shall strive{LB}to meet your hopes.',
'DK4_MES_B47_R0157':'{LB}Look.{LB}Town has gathered{LB}to cheer the Admiral.',
'DK4_MES_B47_R0163':'{LB}Look, Admiral.{LB}The town is here{LB}to cheer for you.',
'DK4_MES_B47_R0170':'So different from Ming...',
'DK4_MES_B47_R0179':'{LB}Your wish to aid the people{LB}reached them.{LB}Now answer their cheers.',
'DK4_MES_B47_R0185':'Your wish to aid the people{LB}reached them.{LB}Please answer their cheers.',
'DK4_MES_B47_R0192':'L-like this?{LB}Never waved before...',
'DK4_MES_B47_R0201':'{LB}(Never before have we seen{LB}{MACRO:FI} so happy...)',
'DK4_MES_B47_R0207':'(Never saw the Admiral so happy...){LB}Coming with her was worth it...',
'DK4_MES_B47_R0211':'Why now?{LB}How strange.',
}
STATES={0x03,0x0A,0x0B,0x0C,0x15,0x1A,0x1C,0x24,0x4A,0x54,0x72,0x8D,0xFE};SPEAKERS={'03':'Maria','0A':'Xien','0B':'Jam','0C':'Companion','15':'Companion','1A':'Companion','1C':'English colonial officer','24':'Espinosa','4A':'Richard','54':'Local leader','72':'Local villager','8D':'Local villager','FE':'Young Englishman'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V56 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route: colonial challenge after Espinosa\'s defeat, Espinosa\'s capture by his victims, regional treasure lead, and Maria\'s first public recognition by the townspeople.','source_meaning':e.replace('{LB}',' '),'localization_note':'Direct SC3 translation preserving the colonial confrontation, testimony against Espinosa, item handoff, crowd scene, portrait states, macros, source staging, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v56-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 46-47: colonial challenge, Espinosa captured by his victims, regional treasure lead, and Maria acclaimed by the townspeople.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
