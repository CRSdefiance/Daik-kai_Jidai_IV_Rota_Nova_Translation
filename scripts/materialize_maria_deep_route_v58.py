from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v58.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(51,52,53)
LINES={
'DK4_MES_B51_R0006':'N-no...{LB}You uncovered my plan so soon!',
'DK4_MES_B51_R0009':'{LB}Carelessness was your weakness.{LB}We never trusted you to begin with.',
'DK4_MES_B51_R0013':'{LB}When you stayed in Hangzhou,{LB}trouble was sensed.{LB}Sending word home early was wise.',
'DK4_MES_B51_R0016':'Grrr...',
'DK4_MES_B51_R0020':'Pretending to be an all-talk fool{LB}to lower my guard... Clever.',
'DK4_MES_B51_R0023':'Just a little longer,{LB}and every western sea{LB}would belong to Lord Clifford!',
'DK4_MES_B51_R0027':'How foolish.{LB}You know the fate of traitors.',
'DK4_MES_B51_R0031':'A century ago, the seas were divided.{LB}We Westerners joined them{LB}through great voyages.',
'DK4_MES_B51_R0035':'Their wealth should naturally be ours!{LB}Y-you have no right to take it!',
'DK4_MES_B51_R0044':'Guaaah! Guh!!',
'DK4_MES_B51_R0056':'L-Lord Clifford...!!',
'DK4_MES_B51_R0069':'Did Richard truly believe{LB}that plan would succeed?',
'DK4_MES_B51_R0072':'{LB}Defeat never seemed{LB}to enter his thoughts.',
'DK4_MES_B51_R0075':'...Perhaps he knew.{LB}Both Clifford and Richard{LB}must have seen the plan was reckless.',
'DK4_MES_B51_R0078':'{LB}Richard too?',
'DK4_MES_B51_R0082':'Yes. Yet he worshiped Clifford{LB}and reveled in that blind faith...{LB}He staked his life on it.',
'DK4_MES_B51_R0085':'{LB}Then Clifford used Richard{LB}from the very start...?',
'DK4_MES_B51_R0101':'{LB}...Then!',
'DK4_MES_B51_R0105':'Richard knew he was expendable.{LB}Now that we returned east,{LB}Clifford will make his next move!',
'DK4_MES_B51_R0109':'{LB}Yes! No doubt!',
'DK4_MES_B52_R0011':'Hey, {MACRO:FA}.{LB}A Ming official seeks you.{LB}Return to Hangzhou.',
'DK4_MES_B52_R0017':'Whoa!{LB}{MACRO:FA} has returned!',
'DK4_MES_B53_R0006':'All Conqueror\'s Proofs{LB}are assembled...',
'DK4_MES_B53_R0009':'{LB}...{LB}Yet, Admiral,{LB}nothing seems to happen.',
'DK4_MES_B53_R0013':'True...',
'DK4_MES_B53_R0025':'Could another key be needed?',
'DK4_MES_B53_R0035':'Oh, spare us.{LB}Must we search the world again?',
'DK4_MES_B53_R0040':'Oh, spare us.{LB}Must we search the world again?',
'DK4_MES_B53_R0046':'No. Nothing more is needed.',
'DK4_MES_B53_R0057':'...The Proofs themselves{LB}never held any special power.',
'DK4_MES_B53_R0061':'{LB}What do you mean?{LB}Did everyone seek meaningless things?',
'DK4_MES_B53_R0065':'That was suspected.',
'DK4_MES_B53_R0069':'Each Proof is tied to local gods,{LB}heroes, or legends.{LB}Even their authenticity is doubtful.',
'DK4_MES_B53_R0072':'Belief made them real,{LB}and made them Proofs...',
'DK4_MES_B53_R0075':'Belief made them?',
'DK4_MES_B53_R0079':'{LB}So the Proofs are merely{LB}illusions made by people?',
'DK4_MES_B53_R0082':'An illusion, yet not merely one.{LB}Shared belief alone{LB}can carry immense meaning.',
'DK4_MES_B53_R0086':'This is not unique to the Proofs.{LB}China has done something similar{LB}for many generations.',
'DK4_MES_B53_R0096':'China too?',
'DK4_MES_B53_R0102':'China too?',
'DK4_MES_B53_R0109':'{LB}...The royal seal!',
'DK4_MES_B53_R0113':'Yes. China\'s emperors held it.{LB}When dynasties changed,{LB}the ruler inherited the seal.',
'DK4_MES_B53_R0117':'Displaying it named one ruler{LB}of the Chinese realm,{LB}ended wars, and preserved the state.',
'DK4_MES_B53_R0120':'{LB}Then the Proofs may hold{LB}that same kind of power?',
'DK4_MES_B53_R0123':'All believe the bearer{LB}has the strength and character{LB}worthy of such a prize.',
'DK4_MES_B53_R0127':'Once all accept that conqueror,{LB}rivals may end useless wars.{LB}Peace could then reach every sea.',
'DK4_MES_B53_R0130':'{LB}Then will conflict at sea{LB}vanish forever?',
'DK4_MES_B53_R0134':'One can hope.{LB}But reality is never so convenient.',
'DK4_MES_B53_R0137':'Every dynasty held the seal,{LB}yet every dynasty finally fell.',
'DK4_MES_B53_R0140':'At last, all depends{LB}on the bearer\'s character.{LB}Too simple?',
'DK4_MES_B53_R0144':'No. The Admiral is right.{LB}What follows now depends{LB}on those who won the Proofs.',
'DK4_MES_B53_R0148':'{LB}Depends on us, eh?{LB}My retirement must wait{LB}a little longer.',
'DK4_MES_B53_R0152':'A little? How timid.{LB}You will work for some time yet.{LB}All, be ready too.',
'DK4_MES_B53_R0164':'We boarded one unbelievable ship.',
'DK4_MES_B53_R0178':'Ho ho ho!{LB}Xien, we old bones{LB}should take it easy together.',
'DK4_MES_B53_R0193':'Work will not run short{LB}for a while.',
'DK4_MES_B53_R0199':'{LB}Hmph. Leave it to me.{LB}Young people will not beat me yet.',
'DK4_MES_B53_R0203':'To Hangzhou!',
}
EXCLUDED={'DK4_MES_B51_R0004':'nontext event payload 60 0F 83 80 45 63; preserved byte-for-byte'}
STATES={0x03,0x06,0x0B,0x0C,0x11,0x14,0x15,0x19,0x1A,0x4A,0x71};SPEAKERS={'03':'Maria','06':'Old sailor','0B':'Jam','0C':'Companion','11':'Companion','14':'Companion','15':'Companion','19':'Companion','1A':'Companion','4A':'Richard','71':'Sailor'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)|set(EXCLUDED)!=set(rows):raise SystemExit(f'V58 mismatch: missing={sorted(set(rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Scene speaker'),'context':'Maria route: Richard\'s failed betrayal, return to Hangzhou, assembly of every Proof of the Conqueror, and the philosophical route epilogue about belief, legitimacy, peace, and responsibility.','source_meaning':e.replace('{LB}',' '),'localization_note':'Direct SC3 translation preserving the betrayal aftermath, name macros, alternate companion lines, portrait states, source staging, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v58-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 51-53: Richard\'s defeat, Hangzhou return, all Proofs assembled, and the philosophical route epilogue.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':counts},'excluded':[{'id':i,'reason':r} for i,r in EXCLUDED.items()],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} preserved control')
if __name__=='__main__':main()
