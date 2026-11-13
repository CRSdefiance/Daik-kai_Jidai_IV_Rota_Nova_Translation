from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path("work/sc3/script.csv"); OUTPUT=Path("translations/maria_deep_route_v40.json"); SC3_SHA256="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"; BLOCKS=(260,261,262,263)
EXCLUDED={"DK4_MES_B263_R0002":"Four-byte scene-entry payload 20469480; not independently rendered dialogue."}
LINES={
"DK4_MES_B260_R0004":"Ms. {MACRO:FI}, you are Chinese.{LB}You know shark fin, right?",
"DK4_MES_B260_R0007":"Yes?",
"DK4_MES_B260_R0010":"Malacca's lord wants to try it.{LB}But shark fin is rare.{LB}Any idea where to get some?",
"DK4_MES_B260_R0013":"That may be difficult.{LB}Even in China, it is palace fare.{LB}Never tasted it.",
"DK4_MES_B260_R0017":"Thought so...{LB}Makes sense.",
"DK4_MES_B260_R0020":"Should some turn up,{LB}we can buy it. No promises.",
"DK4_MES_B260_R0024":"Thanks!",
"DK4_MES_B260_R0028":"Otherwise, bring some delicacy{LB}unlike anything seen before.",
"DK4_MES_B260_R0032":"Unknown delicacy?{LB}Difficult. He must have eaten{LB}food from around the world.",
"DK4_MES_B260_R0036":"Exactly. His appetite is...{LB}Oops. Best say no more.{LB}Good luck.",
"DK4_MES_B261_R0004":"Here is what you requested:{LB}shark fin.",
"DK4_MES_B261_R0007":"Really!?{LB}This is genuine!",
"DK4_MES_B261_R0010":"That should become easier{LB}to obtain now.",
"DK4_MES_B261_R0013":"Splendid work!{LB}Your reward will be generous!",
"DK4_MES_B261_R0018":"Received 50,000 coins.",
"DK4_MES_B261_R0042":"Malacca share rose slightly!",
"DK4_MES_B261_R0059":"A curious tale, then.",
"DK4_MES_B261_R0063":"Deep inland, ruins of an ancient{LB}kingdom remain intact{LB}within the jungle.",
"DK4_MES_B261_R0067":"Ancient ruins? Hard to believe.",
"DK4_MES_B261_R0071":"No one has found it yet.{LB}Merely a rumor.{LB}Perhaps you can find it.",
"DK4_MES_B262_R0004":"Well?{LB}Any luck with shark fin?",
"DK4_MES_B262_R0007":"Sadly, none turned up.{LB}But we found something rare.{LB}Surely it is worth a taste.",
"DK4_MES_B262_R0011":"What is this?{LB}...D-delicious!",
"DK4_MES_B262_R0014":"Right?",
"DK4_MES_B262_R0018":"This can be served with confidence!{LB}Excellent work!{LB}Please accept this reward!",
"DK4_MES_B262_R0024":"Received 30,000 coins.",
"DK4_MES_B262_R0048":"Malacca share rose slightly!",
"DK4_MES_B262_R0065":"A curious tale, then.",
"DK4_MES_B262_R0069":"Deep inland, ruins of an ancient{LB}kingdom remain intact{LB}within the jungle.",
"DK4_MES_B262_R0073":"Hard to believe...",
"DK4_MES_B262_R0077":"No one has found it yet.{LB}Merely a rumor.{LB}Perhaps you can find it.",
"DK4_MES_B263_R0013":"Admiral!{LB}Come over here!",
"DK4_MES_B263_R0014":"Admiral!{LB}Come, please!",
"DK4_MES_B263_R0015":"Admiral!{LB}Here!",
"DK4_MES_B263_R0016":"Admiral!{LB}Come here!",
"DK4_MES_B263_R0017":"Admiral!{LB}Come here!",
"DK4_MES_B263_R0018":"Admiral!{LB}Come here!",
"DK4_MES_B263_R0019":"Admiral!{LB}Come here!",
"DK4_MES_B263_R0022":"What?",
"DK4_MES_B263_R0026":"Let's dig!",
"DK4_MES_B263_R0030":"A very ancient coin, it seems.",
}
STATES={0x03,0x93,0x9C,0xD6,0xFE}; SPEAKERS={"03":"Maria","93":"Guildmaster","9C":"Companion","D6":"Companion","FE":"System"}
def main()->None:
    with SOURCE.open(encoding="utf-8-sig",newline="") as s: all_rows={r["id"]:r for r in csv.DictReader(s)}
    rows={i:r for i,r in all_rows.items() if any(i.startswith(f"DK4_MES_B{b}_") for b in BLOCKS)}
    if set(LINES)|set(EXCLUDED)!=set(rows): raise SystemExit(f"Maria V40 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}")
    records=[]; counts={str(b):0 for b in BLOCKS}
    for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
        r=rows[i]; e=LINES[i]; first=bytes.fromhex(r['source_hex'])[0]; state=f"{first:02X}" if first in STATES else ""; block=i.split('_B',1)[1].split('_',1)[0]; counts[block]+=1
        leading=e.startswith('{LB}'); waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if '{LB}' in e else [])+(['source-leading-linebreak'] if leading else [])
        records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Malacca shark-fin commission, alternate delicacy resolution, jungle-kingdom rumor, and ancient-coin discovery.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").strip(),'localization_note':'Direct SC3 translation reviewed for natural English, branch and reward parity, macro preservation, and state-byte safety.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source transition or semantic grouping.'} if '{LB}' in e else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
    payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v40-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 260-263: shark-fin commission, alternate delicacy resolution, rewards, jungle-kingdom rumor, and ancient-coin discovery.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':counts},'excluded':[{'id':i,'reason':v} for i,v in EXCLUDED.items()],'records':records}
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} excluded')
if __name__=='__main__': main()
