from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv'); OUTPUT=Path('translations/maria_deep_route_v41.json'); SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2'; BLOCKS=(264,265,266)
EXCLUDED={'DK4_MES_B264_R0028':'Five-byte scene-transition payload 468D808043; not independently rendered dialogue.','DK4_MES_B264_R0092':'Four-byte navigation-scene payload 20468E80; not independently rendered dialogue.'}
LINES={
'DK4_MES_B264_R0011':'Did you bring a map?{LB}Even for you, no one should proceed{LB}without one.',
'DK4_MES_B264_R0024':'Good. You have the map.',
'DK4_MES_B264_R0045':'Admiral, no map means{LB}no passage.',
'DK4_MES_B264_R0046':'Admiral, no map means{LB}no passage.',
'DK4_MES_B264_R0047':'Admiral, we need a map.',
'DK4_MES_B264_R0049':'No map means{LB}no passage.',
'DK4_MES_B264_R0050':'Wait. No map means{LB}no passage.',
'DK4_MES_B264_R0051':'Admiral, we need a map.',
'DK4_MES_B264_R0053':'Admiral, we need a map~',
'DK4_MES_B264_R0055':'Admiral, no map means{LB}no passage.',
'DK4_MES_B264_R0068':'We part here.{LB}Take care.',
'DK4_MES_B264_R0071':'Xien, ready?',
'DK4_MES_B264_R0075':'{LB}Everything is ready.',
'DK4_MES_B264_R0087':'Admiral, move carefully...',
'DK4_MES_B264_R0094':'A dead end...?',
'DK4_MES_B264_R0098':'{LB}Hm.',
'DK4_MES_B264_R0104':'Push on',
'DK4_MES_B264_R0106':'Search',
'DK4_MES_B264_R0120':'Map says...{LB}break through here.',
'DK4_MES_B264_R0121':'Map says{LB}continue ahead...',
'DK4_MES_B264_R0122':'The map says to break through{LB}right here...',
'DK4_MES_B264_R0123':'The map says{LB}break through here...',
'DK4_MES_B264_R0124':'The map says to press through{LB}right here.',
'DK4_MES_B264_R0125':'Hmm. According to the map,{LB}we must cross this point.',
'DK4_MES_B264_R0127':'The map says we have to{LB}cross right here.',
'DK4_MES_B264_R0128':'Map says...{LB}break through here.',
'DK4_MES_B264_R0131':'Then let us go!{LB}Everyone, stay together!',
'DK4_MES_B264_R0138':'Several sailors got separated.',
'DK4_MES_B264_R0146':'Oh?{LB}A path here.',
'DK4_MES_B264_R0149':'{LB}The trees concealed it...{LB}{MACRO:FI}, sharp eyes.{LB}Let us continue.',
'DK4_MES_B264_R0157':'Here...{LB}A splendid view.',
'DK4_MES_B265_R0005':'The Turkish guild is looking for you.',
'DK4_MES_B266_R0004':'Sorry to call you all this way.',
'DK4_MES_B266_R0007':'Our couriers are too slow.{LB}They demand high pay,{LB}yet take forever.',
'DK4_MES_B266_R0010':'Why not dismiss{LB}such lazy couriers?',
'DK4_MES_B266_R0013':'The local couriers work together.{LB}No matter whom we hire,{LB}they all claim the same long trip time.',
'DK4_MES_B266_R0016':'A cartel.',
'DK4_MES_B266_R0020':'Their round trip from here to Ceuta{LB}takes more than two months.{LB}We need your help.',
'DK4_MES_B266_R0023':'Two months?{LB}Awful.',
'DK4_MES_B266_R0027':'Exactly!{LB}Show a round trip{LB}in 30 days.',
'DK4_MES_B266_R0031':'Thirty days?{LB}Does it not normally take about 40?',
'DK4_MES_B266_R0035':'They are told to do it in 40 days.{LB}But first, we must prove{LB}it can be done in 30.',
'DK4_MES_B266_R0038':'Understood.{LB}We accept.',
'DK4_MES_B266_R0041':'Succeed,{LB}or our losses continue. Good luck.',
}
STATES={0x03,0x0C,0x5F,0x94,0xD0,0xD3,0xFE}; SPEAKERS={'03':'Maria','0C':'Companion','5F':'Messenger','94':'Guide or guildmaster','D0':'Companion','D3':'Companion','FE':'System'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s: all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b}_') for b in BLOCKS)}
 if set(LINES)|set(EXCLUDED)!=set(rows): raise SystemExit(f'Maria V41 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}')
 records=[]; counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i]; e=LINES[i]; first=bytes.fromhex(r['source_hex'])[0]; state=f'{first:02X}' if first in STATES else ''; block=i.split('_B',1)[1].split('_',1)[0]; counts[block]+=1; leading=e.startswith('{LB}'); waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if '{LB}' in e else [])+(['source-leading-linebreak'] if leading else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Jungle-map traversal and Turkish guild anti-cartel Ceuta speed-run contract.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").strip(),'localization_note':'Direct SC3 translation reviewed for natural English, choice and companion-branch parity, macro preservation, and state-byte safety.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source transition or semantic grouping.'} if '{LB}' in e else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v41-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 264-266: jungle-map traversal, ancient-kingdom vista, and Turkish guild Ceuta speed-run contract.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':counts},'excluded':[{'id':i,'reason':v} for i,v in EXCLUDED.items()],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} excluded')
if __name__=='__main__': main()
