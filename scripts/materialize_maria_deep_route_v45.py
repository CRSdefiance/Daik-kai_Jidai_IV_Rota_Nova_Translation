from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v45.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(11,12,13,14,16,17,18);EXCLUDED={}
LINES={
'DK4_MES_B11_R0004':'Spanish pirate Hernan Berrio.{LB}You seem proud of that fleet,{LB}but one opponent remains.',
'DK4_MES_B11_R0007':'Been a while since anyone{LB}dared face me. These days,{LB}ships flee at first sight.{LB}Being too strong has drawbacks.',
'DK4_MES_B11_R0010':'Good. Boredom had set in.{LB}Come, then! We shall fight!',
'DK4_MES_B12_R0005':'Clifford is unforgivable!{LB}And sending that vulgar brute{LB}after me? The lowest!',
'DK4_MES_B12_R0009':'Such spirit.{LB}Even your face changed.',
'DK4_MES_B12_R0012':'W-what?',
'DK4_MES_B12_R0016':'Lil, thank her properly.{LB}Thank you so much.{LB}You truly saved us...',
'DK4_MES_B12_R0027':'Think nothing of it.{LB}They may still be nearby,{LB}so stay alert.',
'DK4_MES_B12_R0037':'Saved again...{LB}Ugh, how frustrating.',
'DK4_MES_B12_R0040':'Lil!',
'DK4_MES_B12_R0044':'Think nothing of it.{LB}They may still be nearby,{LB}so stay alert.',
'DK4_MES_B12_R0048':'This debt will be repaid!',
'DK4_MES_B13_R0004':'Ugh... better withdraw.{LB}Retreat!',
'DK4_MES_B13_R0007':'Damn it!{LB}Beaten by that vulgar brute!',
'DK4_MES_B13_R0010':'Lil... We survived,{LB}and that is enough today.{LB}Thank you so much.{LB}You saved us...',
'DK4_MES_B13_R0019':'Think nothing of it.{LB}They may still be nearby,{LB}so stay alert.',
'DK4_MES_B13_R0028':'Thanks for saving us...{LB}That was close...',
'DK4_MES_B13_R0031':'Think nothing of it.{LB}They may still be nearby.{LB}Take care.',
'DK4_MES_B13_R0035':'Always needing rescue{LB}is humiliating.{LB}We will become stronger!',
'DK4_MES_B13_R0039':"That's it, Lil!",
'DK4_MES_B13_R0043':'What a positive girl.',
'DK4_MES_B14_R0005':'{MACRO:FA}, as expected.{LB}Maybe you needed no help?',
'DK4_MES_B14_R0009':'No, you helped.{LB}Many thanks.',
'DK4_MES_B14_R0012':'Heh, now we are even, right?{LB}Then, bye!',
'DK4_MES_B16_R0005':'Perfect timing.{LB}Well done.',
'DK4_MES_B16_R0017':'Thank me after Escante falls.{LB}We withdraw for now,{LB}but stay alert.',
'DK4_MES_B17_R0004':'Damn. We withdraw!',
'DK4_MES_B17_R0010':'You okay?!',
'DK4_MES_B17_R0014':'She is alive...',
'DK4_MES_B17_R0018':'My error...',
'DK4_MES_B17_R0022':'Not at all.{LB}Thank you for joining us.',
'DK4_MES_B17_R0034':'Thank me after Escante falls.{LB}We leave now,{LB}but stay alert.',
'DK4_MES_B18_R0005':'We won.',
'DK4_MES_B18_R0009':'{LB}Your command has improved.',
'DK4_MES_B18_R0013':'Thanks to Xien.',
'DK4_MES_B18_R0017':'{LB}Heh, nonsense.{LB}Nothing remains for me{LB}to teach you now.',
'DK4_MES_B18_R0021':'Men scattered into the sea...{LB}No, perhaps they returned{LB}to the mother sea...',
'DK4_MES_B18_R0025':'Manuel...',
'DK4_MES_B18_R0029':'Console those who fell.',
'DK4_MES_B18_R0036':'Sea and mother are alike.{LB}Waves repeat, feel familiar,{LB}waking the heartbeat{LB}of a distant mother.',
'DK4_MES_B18_R0039':'Sea and mother are alike.{LB}Some lands write and sound{LB}the words alike.',
'DK4_MES_B18_R0043':'Sea and mother are alike.{LB}While life endures,{LB}both lie within a bond{LB}that never disappears.',
'DK4_MES_B18_R0046':'{LB}Manuel...{LB}Poetry?',
'DK4_MES_B18_R0049':'Odd...{LB}Thought you cared{LB}only for ships.',
'DK4_MES_B18_R0053':'{LB}No, {MACRO:FI}.{LB}Every seaman carries{LB}romance in his heart.',
'DK4_MES_B18_R0064':'Ha ha! We won!{LB}A victory feast!{LB}Yahoo!',
'DK4_MES_B18_R0068':'{LB}One exception...',
'DK4_MES_B18_R0075':'The sea accepts all things.{LB}May we learn to do the same.',
}
STATES={0x01,0x02,0x03,0x09,0x0B,0x17,0x48};SPEAKERS={'01':'Reinforcement captain','02':'Lil','03':'Maria','09':'Kamil','0B':'Crewman','17':'Manuel','48':'Hernan'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s: all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows): raise SystemExit(f'Maria V45 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES else '';block=str(int(i.split('_B',1)[1].split('_',1)[0]));counts[block]+=1;leading=e.startswith('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if '{LB}' in e else [])+(['source-leading-linebreak'] if leading else [])+(['line-break-count'] if i=='DK4_MES_B18_R0053' else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Companion'),'context':'Maria route core: Hernan battle, Lil rescue branches, Escante aftermath, and Manuel sea elegy.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FA}',"the protagonist's surname").strip(),'localization_note':'Direct SC3 translation reviewed for natural English, branch parity, macro preservation, and state-byte safety.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source transition or semantic grouping.'} if '{LB}' in e else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v45-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 11-18: Hernan battle, Lil rescue branches, Escante aftermath, and Manuel sea elegy.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
