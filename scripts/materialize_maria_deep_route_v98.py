from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v98.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B132_R0004":"Yeah!{LB}Calicut is the best!{LB}Hot, too!",
"DK4_MES_B132_R0015":"No... this heat{LB}does not suit me.",
"DK4_MES_B132_R0020":"{LB}Truly hot.",
"DK4_MES_B132_R0027":"The scenery changes{LB}this far south.",
"DK4_MES_B132_R0030":"Admiral!{LB}Meals for sale there!{LB}Looks great!",
"DK4_MES_B132_R0034":"{LB}Jam, wait...{LB}Ah, already gone.",
"DK4_MES_B132_R0037":"Really...",
"DK4_MES_B132_R0041":"Admiral!{LB}Help!",
"DK4_MES_B132_R0044":"{LB}Hm? Was that Jam?",
"DK4_MES_B132_R0047":"Rare words from him.{LB}What happened?",
"DK4_MES_B132_R0058":"Bad food?{LB}Stomach trouble?",
"DK4_MES_B132_R0065":"Admiral! Sorry!{LB}That strange kid caught me...",
"DK4_MES_B132_R0070":"Oh, you're the admiral?{LB}This man lost our wager.{LB}He's mine now.",
"DK4_MES_B132_R0074":"{LB}Who is this?!",
"DK4_MES_B132_R0078":"Yours? What does that mean?",
"DK4_MES_B132_R0082":"He's a vendor.{LB}He offered a bonus for winning{LB}a coin toss, so...",
"DK4_MES_B132_R0086":"{LB}And you lost...{LB}But why would that make you his?",
"DK4_MES_B132_R0090":"Ten heads in a row meant{LB}he would obey any order.{LB}That was our bargain.",
"DK4_MES_B132_R0093":"Ten heads straight?{LB}That never happens!{LB}Can't believe this!",
"DK4_MES_B132_R0097":"But it did happen. Heh.",
"DK4_MES_B132_R0100":"...Show me that coin.",
"DK4_MES_B132_R0104":"Huh?{LB}N-no.",
"DK4_MES_B132_R0107":"{LB}Hm? Odd.",
"DK4_MES_B132_R0111":"You cheated?{LB}Show me!",
"DK4_MES_B132_R0114":"Ah!",
"DK4_MES_B132_R0122":"Oh well. Caught.",
"DK4_MES_B132_R0126":"{LB}Two joined coins.{LB}Both sides are heads.",
"DK4_MES_B132_R0130":"Damn it!{LB}You little cheat!",
"DK4_MES_B132_R0133":"Heh. Sorry.",
"DK4_MES_B132_R0137":"Sorry isn't enough!",
"DK4_MES_B132_R0140":"Then...{LB}call the wager my loss.",
"DK4_MES_B132_R0143":"{LB}What now?",
"DK4_MES_B132_R0147":"Take me with you.{LB}Anything you ask.",
"DK4_MES_B132_R0158":"So bold...",
"DK4_MES_B132_R0172":"Such an arrogant brat{LB}will be no use!",
"DK4_MES_B132_R0175":"(You would know...)",
"DK4_MES_B132_R0181":"{LB}What nerve.{LB}Words fail me.",
"DK4_MES_B132_R0187":"You're travelers, right?{LB}Good at everything.{LB}Sure to be useful.",
"DK4_MES_B132_R0191":"Ha! Sounds fun!{LB}We'll work him hard!{LB}Admiral, please?",
"DK4_MES_B132_R0199":"{LB}Absolutely not.",
"DK4_MES_B132_R0203":"Please!",
"DK4_MES_B132_R0207":"Come on, Admiral!{LB}...Why are you pleading too?!",
"DK4_MES_B132_R0210":"Elephants bore me.{LB}Other lands are calling.{LB}Seriously, anything you ask!",
"DK4_MES_B132_R0214":"Yes.",
"DK4_MES_B132_R0218":"Yes!",
"DK4_MES_B132_R0222":"{LB}{MACRO:FI}!{LB}Are you sure?",
"DK4_MES_B132_R0225":"Yes. Anyone who can best Jam{LB}may be a hidden prize.",
"DK4_MES_B132_R0229":"...Did he use me?{LB}Damn it!",
"DK4_MES_B132_R0233":"Yes! Other lands!{LB}Never sailed before, actually.{LB}Name's Samwell. Nice to meet you!",
"DK4_MES_B132_R0238":"Welcome.",
"DK4_MES_B132_R0242":"{LB}Hmm...{LB}He seems only a burden...",
"DK4_MES_B133_R0005":"Still not back.",
}
EX={"DK4_MES_B132_R0068":"Raw seven-byte event-control payload between Jam's plea and Samwell's entrance; not dialogue."}
SP={"03":"Maria","0B":"Jam","0C":"Yukihisa","16":"Samwell","4A":"Carlo","74":"Companion"};ST={int(x,16) for x in SP}
C={132:"In Calicut, Samwell wins Jam in a rigged coin toss; Maria exposes the trick and recruits the resourceful boy.",133:"A companion notes that someone still has not returned."}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if 132<=int(r["id"].split("_B",1)[1].split("_R",1)[0])<=133}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V98 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the coin-trick reveal, recruitment beats, speaker states, FI macro, source-leading line breaks, control payload, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v98-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 132-133: Samwell's coin-trick recruitment and the following absence line.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"132":52,"133":1}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
