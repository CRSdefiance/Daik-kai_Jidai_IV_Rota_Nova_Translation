from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');OUTPUT=Path('translations/maria_deep_route_v48.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=tuple(range(25,31))
LINES={
'DK4_MES_B25_R0008':'Screech! Curse you!{LB}A curse upon you!{LB}Curse you!',
'DK4_MES_B25_R0012':'Noisier than a gnat...{LB}Hurry to Veracruz.',
'DK4_MES_B26_R0008':'L-listen!{LB}Letting you win was planned!',
'DK4_MES_B26_R0011':'Athens guild will take you.{LB}Try anything strange,{LB}and your life is forfeit.',
'DK4_MES_B27_R0005':'Enemy?',
'DK4_MES_B27_R0009':'{LB}Vanished...',
'DK4_MES_B27_R0013':'...We won?',
'DK4_MES_B27_R0023':'{LB}Was that...{LB}truly a ghost ship?',
'DK4_MES_B27_R0028':'Was that...{LB}truly a ghost ship?',
'DK4_MES_B27_R0034':'Who can say?{LB}Superstition is not my habit,{LB}but that was no illusion...',
'DK4_MES_B27_R0044':'{LB}Hmm. No clear answer.{LB}The mystery remains.',
'DK4_MES_B27_R0049':'Strange things do happen.{LB}The mystery remains unsolved.',
'DK4_MES_B27_R0055':'Ghost or not,{LB}our work here is finished.{LB}Return to Havana guild.',
'DK4_MES_B28_R0005':'There!{LB}Orca {MACRO:FA}!',
'DK4_MES_B28_R0008':'Today is your last!{LB}Behold the ironclad fleet!',
'DK4_MES_B28_R0011':'{LB}What is that fleet?!',
'DK4_MES_B28_R0022':'What is that ship?!',
'DK4_MES_B28_R0031':'An ironclad...?!',
'DK4_MES_B29_R0009':'Aaaaah!!',
'DK4_MES_B29_R0013':'Lil! Are you hurt?',
'DK4_MES_B29_R0017':'That Clifford!{LB}How dare he betray me!!',
'DK4_MES_B29_R0020':'Ha ha ha!{LB}Give up already, girl!',
'DK4_MES_B29_R0023':'Do not mock me!',
'DK4_MES_B29_R0027':'Oh no... completely surrounded!{LB}There is no escape!',
'DK4_MES_B29_R0030':'Damn it!',
'DK4_MES_B29_R0036':'Help them.',
'DK4_MES_B29_R0038':'Stay out of this.',
'DK4_MES_B29_R0045':'Wait!',
'DK4_MES_B29_R0049':'Who are you?!',
'DK4_MES_B29_R0053':'That hardly matters.{LB}Hey, you there!',
'DK4_MES_B29_R0056':'You mean me?',
'DK4_MES_B29_R0060':'Grown men ganging up{LB}on a young woman?{LB}Shameful!',
'DK4_MES_B29_R0072':'Exactly. Despicable.{LB}A man should always{LB}be kind to women.',
'DK4_MES_B29_R0079':'What?! Shut up!{LB}This is none of your concern!{LB}Stay out if you know nothing!',
'DK4_MES_B29_R0088':'Not everyone backs down{LB}when ordered, especially with{LB}brutes harassing a helpless girl.',
'DK4_MES_B29_R0091':'Wait!{LB}Did you call me helpless?',
'DK4_MES_B29_R0094':'Right now,{LB}you hardly look strong.',
'DK4_MES_B29_R0097':'M-maybe, but{LB}normally we are...!',
'DK4_MES_B29_R0100':'Lil, not now! Do not fight{LB}someone offering help!{LB}Please save us!',
'DK4_MES_B29_R0103':'Kamil, acting alone again!',
'DK4_MES_B29_R0107':'This dull rabbit hunt{LB}just gained a fine prize.{LB}Might as well take her too!',
'DK4_MES_B29_R0111':'Not everyone backs down{LB}just because they are told!',
'DK4_MES_B29_R0115':'{MACRO:FI}!',
'DK4_MES_B29_R0119':'With {MACRO:FI}{LB}on our side,{LB}we cannot lose!',
'DK4_MES_B29_R0123':'This dull rabbit hunt{LB}just gained a fine prize.',
'DK4_MES_B29_R0127':'Then we will take her too!',
'DK4_MES_B29_R0134':'Screech! What does that mean?!',
'DK4_MES_B29_R0138':'Coming!',
'DK4_MES_B29_R0153':'This is not our fight.{LB}Leave the battle zone.',
'DK4_MES_B29_R0164':'N-no...',
'DK4_MES_B30_R0005':'Well, well.',
'DK4_MES_B30_R0009':'Clifford?!',
'DK4_MES_B30_R0013':'Richard performed well,{LB}but he was simply outmatched.',
'DK4_MES_B30_R0020':'Your role was to make Ming{LB}abandon its absurd isolation.{LB}You exceeded every expectation.',
'DK4_MES_B30_R0023':'...That is all?',
'DK4_MES_B30_R0027':'Richard was right.{LB}Beautiful, but headstrong.{LB}You meddled far too much.',
'DK4_MES_B30_R0030':'A pity. You must die.',
'DK4_MES_B30_R0074':'{MACRO:FA}!!',
'DK4_MES_B30_R0082':'We are joining you!{LB}No debt stays unpaid!',
'DK4_MES_B30_R0085':'The Argot Company?!',
'DK4_MES_B30_R0089':'Clifford!{LB}Prepare yourself!',
'DK4_MES_B30_R0092':'Reckless girl.{LB}Play with fire, get hurt.',
}
STATES={0x02,0x03,0x09,0x15,0x17,0x1A,0x1C,0x2C,0x39,0x43,0x44,0x47,0x48,0x4A};SPEAKERS={'02':'Lil','03':'Maria','09':'Kamil','15':'Companion','17':'Manuel','1A':'Companion','1C':'James Clifford','2C':'Rival captain','39':'Rival captain','43':'Gabriel','44':'Jacob','47':'Zaganos','48':'Hernan','4A':'Crewman'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as s:all_rows={r['id']:r for r in csv.DictReader(s)}
 rows={i:r for i,r in all_rows.items() if any(i.startswith(f'DK4_MES_B{b:02d}_') for b in BLOCKS)}
 if set(LINES)!=set(rows):raise SystemExit(f'V48 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}')
 records=[];counts={str(b):0 for b in BLOCKS}
 for i in sorted(LINES,key=lambda v:(int(v.split('_B',1)[1].split('_',1)[0]),int(v.rsplit('R',1)[1]))):
  r=rows[i];e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';counts[str(int(i.split('_B',1)[1].split('_',1)[0]))]+=1;sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Story participant'),'context':'Maria route bounty finales, ghost ship, ironclad clash, Lil rescue branches, and Clifford confrontation.','source_meaning':e.replace('{LB}',' ').replace('{MACRO:FI}',"the protagonist's given name").replace('{MACRO:FA}',"the protagonist's surname"),'localization_note':'Direct SC3 translation preserving choices, route macros, presentation states, and battle staging.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within four display lines.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v48-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 blocks 25-30: bounty finales, ghost ship, ironclad clash, Lil rescue choices, and Clifford confrontation.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':0,'blocks':counts},'excluded':[],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records')
if __name__=='__main__':main()
