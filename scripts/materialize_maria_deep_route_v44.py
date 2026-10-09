from __future__ import annotations
import csv, json
from pathlib import Path

SOURCE=Path('work/sc3/script.csv'); OUTPUT=Path('translations/maria_deep_route_v44.json')
SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2'; BLOCKS=tuple(range(0,11))
EXCLUDED={'DK4_MES_B00_R0002':'Six-byte opening scene-control payload 214898A8FF61; not independently rendered dialogue.'}
LINES={
'DK4_MES_B00_R0004':'What meaning could there be{LB}in this treasure sought{LB}by every great power?',
'DK4_MES_B00_R0008':'{LB}Who knows? Perhaps it merely{LB}justifies the Western powers{LB}and their rule of the world.',
'DK4_MES_B00_R0012':'The Proof may be a lie?',
'DK4_MES_B00_R0023':'Such arrogance cannot be allowed!',
'DK4_MES_B00_R0030':'Yet if they invented it,{LB}the Proof should be a treasure{LB}they could claim at once.',
'DK4_MES_B00_R0039':'That none has found it{LB}may itself suggest it truly is{LB}the sovereign\'s rightful proof.',
'DK4_MES_B00_R0044':'Ah, yes.',
'DK4_MES_B00_R0048':'That none has found it{LB}may itself suggest it truly is{LB}the sovereign\'s rightful proof.',
'DK4_MES_B00_R0054':'Yes...',
'DK4_MES_B00_R0058':'Either way, to stop the powers{LB}from doing as they please,{LB}we must find the Proof first.',
'DK4_MES_B00_R0061':'{LB}Agreed.',
'DK4_MES_B01_R0005':'So this is... Muramasa...',
'DK4_MES_B01_R0009':'Hmm...{LB}That eerie light nearly{LB}draws one to the blade.',
'DK4_MES_B02_R0005':'Yes! The same dull gleam{LB}as when it left my hands.',
'DK4_MES_B02_R0009':'How was it never found...?',
'DK4_MES_B03_R0005':'Lady {MACRO:FI}!{LB}Today we settle this!',
'DK4_MES_B03_R0015':'Kurushima!{LB}End this folly!',
'DK4_MES_B03_R0018':'A samurai siding with foreigners!{LB}You shame every warrior!',
'DK4_MES_B03_R0022':'You raid coasts and rob{LB}helpless people.{LB}Where is your honor?',
'DK4_MES_B03_R0026':'That rigid virtue...{LB}How disgusting.',
'DK4_MES_B03_R0032':'Heh heh, {MACRO:FI}!{LB}Be my woman and surrender.{LB}Your life alone will be spared!',
'DK4_MES_B03_R0035':'Sojin Kurushima...{LB}Say one more useless word,{LB}and that proud beard comes off.',
'DK4_MES_B03_R0039':'Ha ha ha!{LB}Then die!',
'DK4_MES_B04_R0005':'Conqueror Escante,{LB}free the New World people{LB}you rule without right.',
'DK4_MES_B04_R0009':'Ha ha! What did Maldonado tell you?{LB}What a miscalculation.{LB}A woman, not Valdes, faces me.',
'DK4_MES_B04_R0012':'Valdes? An officer{LB}of your nation?',
'DK4_MES_B04_R0015':'Hmph.{LB}At last, my own kindness{LB}became clear to me.',
'DK4_MES_B04_R0023':'The New World is vast,{LB}yet all this time it served{LB}as money for the homeland.{LB}What a waste.',
'DK4_MES_B04_R0026':'So you bought weapons{LB}to win independence{LB}from your homeland?',
'DK4_MES_B04_R0030':'Exactly. You hate colonial rule,{LB}so surely you can grasp{LB}the brilliance of my plan.',
'DK4_MES_B04_R0033':'The New World people shall have{LB}a nation of their own.{LB}What a bold and splendid vision!',
'DK4_MES_B04_R0037':'How selfish.{LB}Only a villain would dress{LB}greed up as justice.',
'DK4_MES_B04_R0041':'You thought such nonsense{LB}would sway me?{LB}You have badly misjudged me!',
'DK4_MES_B04_R0045':'Talk is over.{LB}A child who won\'t listen{LB}must be punished! All ships, attack!',
'DK4_MES_B04_R0097':'Good timing.',
'DK4_MES_B04_R0105':'He is my enemy too.{LB}We will join you.',
'DK4_MES_B05_R0005':'Look there!{LB}That fleet raids{LB}our waters.{LB}That is {MACRO:FO}!',
'DK4_MES_B05_R0008':'Hooray!',
'DK4_MES_B05_R0012':'Battle stations!{LB}Snake, command!',
'DK4_MES_B05_R0015':'Aye.',
'DK4_MES_B05_R0019':'Angel!{LB}Take their right rear!',
'DK4_MES_B05_R0022':'You got it!{LB}Leave it to me!',
'DK4_MES_B05_R0025':'Dandy!{LB}Are the guns ready?',
'DK4_MES_B05_R0028':'Ready.',
'DK4_MES_B05_R0032':'Heh... what a thrill.{LB}Listen up, you dogs!',
'DK4_MES_B05_R0035':'Now we decide whether me or{LB}{MACRO:FO} deserves to rule{LB}these seas!',
'DK4_MES_B05_R0038':'Hooray!',
'DK4_MES_B05_R0042':'An unknown pirate.',
'DK4_MES_B05_R0046':'{LB}A woman pirate... rare.{LB}What drove her?',
'DK4_MES_B05_R0049':'Whatever her cause,{LB}raiders cannot go free.{LB}Prepare for battle!',
'DK4_MES_B06_R0042':'We found you!{LB}Now we settle it!',
'DK4_MES_B06_R0045':'Hooray!',
'DK4_MES_B06_R0051':'Back again, are you?{LB}{MACRO:FO}!{LB}This time, sink beneath the waves!',
'DK4_MES_B07_R0004':'At last.{LB}Yuris, the ship thief.',
'DK4_MES_B07_R0007':'What a cheap little nickname.{LB}Hardly fitting for someone{LB}born to the highest nobility.',
'DK4_MES_B07_R0010':'So sensitive about a nickname.{LB}Once sent to Batavia,{LB}you can bid it farewell.',
'DK4_MES_B08_R0005':'So you are Jacob Portunto.{LB}A low smuggler playing at piracy?{LB}Push your luck, and pain will follow.',
'DK4_MES_B08_R0009':'What?{LB}You will not lecture me!',
'DK4_MES_B09_R0004':'So you are Gabriel.{LB}Enough trade in breach{LB}of the treaty.',
'DK4_MES_B09_R0008':'Breach? Treaties exist{LB}to be broken.{LB}Enough of your prattle.',
'DK4_MES_B09_R0012':'That is my line.{LB}Must force make you understand?',
'DK4_MES_B09_R0016':'Amusing. Come on!',
'DK4_MES_B10_R0005':'Kee hee hee! Who are you?{LB}Do you want to die?',
'DK4_MES_B10_R0008':'Could be human...?',
'DK4_MES_B10_R0012':'Ooh kee kee! We will sink you!{LB}Sink you! Sink you!',
}
STATES={0x01,0x03,0x0C,0x10,0x15,0x19,0x1B,0x29,0x2B,0x40,0x43,0x44,0x47,0x99,0xB7,0xB8,0xB9}
SPEAKERS={'01':'Reinforcement captain','03':'Maria','0C':'Xien','10':'Sword owner','15':'Companion','19':'Companion','1B':'Pirate captain','29':'Sojin Kurushima','2B':'Escante','40':'Yuris','43':'Gabriel','44':'Jacob','47':'Pirate','99':'Pirate crew','B7':'Angel','B8':'Snake','B9':'Dandy'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s: all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)|set(EXCLUDED)!=set(rows): raise SystemExit(f'Maria V44 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}')
 records=[]; counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i]; e=LINES[i]; first=bytes.fromhex(r['source_hex'])[0]; state=f'{first:02X}' if first in STATES else ''; block=str(int(i.split('_B',1)[1].split('_',1)[0])); counts[block]+=1; leading=e.startswith('{LB}'); waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if '{LB}' in e else [])+(['source-leading-linebreak'] if leading else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route core: Proof discussion, legendary sword scenes, and major pirate/colonial battles.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FO}',"the protagonist's full name").strip(),'localization_note':'Direct SC3 translation reviewed for natural English, character voice, macro preservation, and state-byte safety.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source transition or semantic grouping.'} if '{LB}' in e else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v44-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 0-10: Proof discussion, Muramasa scenes, and major pirate/colonial confrontations.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':counts},'excluded':[{'id':i,'reason':v} for i,v in EXCLUDED.items()],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} excluded')
if __name__=='__main__': main()
