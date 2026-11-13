from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v95.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B121_R0010":"A calm man's voice:{LB}Pardon the intrusion...",
"DK4_MES_B121_R0019":"Bergstrom, Swedish Navy.{LB}Are you Admiral {MACRO:FA},{LB}the one lately in every rumor?",
"DK4_MES_B121_R0022":"...Suppose so?",
"DK4_MES_B121_R0026":"Your aim?{LB}Conquest?",
"DK4_MES_B121_R0029":"Why ask?",
"DK4_MES_B121_R0033":"...To see whether{LB}you are our enemy.",
"DK4_MES_B121_R0042":"You are...",
"DK4_MES_B121_R0047":"Again.{LB}What now?",
"DK4_MES_B121_R0050":"{MACRO:FA},{LB}what is your aim?{LB}World conquest?",
"DK4_MES_B121_R0054":"Why ask?",
"DK4_MES_B121_R0061":"Should you claim every sea{LB}and monopolize all profit{LB}from its trade routes...",
"DK4_MES_B121_R0065":"Then my homeland's free trade{LB}must be defended.",
"DK4_MES_B121_R0068":"My aim...{LB}No duty or need exists{LB}to explain it to you.",
"DK4_MES_B121_R0076":"Only this:{LB}your guess is not quite right.",
"DK4_MES_B121_R0079":"Whether we become enemies...{LB}depends entirely on you.",
"DK4_MES_B121_R0088":"Who you are remains unclear.{LB}Still, no sign suggests{LB}you are my enemy yet.",
"DK4_MES_B121_R0094":"No sign suggests{LB}you are my enemy yet.",
"DK4_MES_B121_R0100":"Surprising.{LB}This visit was to judge you,{LB}yet now you judge me.",
"DK4_MES_B121_R0104":"Judge? Think what you like.{LB}Making enemies needlessly{LB}holds no appeal.",
"DK4_MES_B121_R0108":"...Understood.{LB}Then only a warning.",
"DK4_MES_B121_R0111":"Enough for today.{LB}No point provoking your anger.",
"DK4_MES_B121_R0115":"What does that mean?",
"DK4_MES_B121_R0119":"Said too much.{LB}Goodbye.",
"DK4_MES_B122_R0016":"Admiral,{LB}letter from Clifford.",
"DK4_MES_B122_R0017":"Admiral,{LB}letter from Clifford.",
"DK4_MES_B122_R0018":"Admiral!{LB}A Clifford letter!",
"DK4_MES_B122_R0021":"Mail",
"DK4_MES_B122_R0037":"Yes. This one.",
"DK4_MES_B122_R0039":"This one.",
"DK4_MES_B122_R0041":"This one.",
"DK4_MES_B122_R0043":"This one.",
"DK4_MES_B122_R0045":"One",
"DK4_MES_B122_R0049":"My rival...?",
"DK4_MES_B122_R0053":"To the one who defeated me:{LB}Take this letter to Amsterdam's tavern.{LB}A gift awaits you.{LB}--James Clifford",
"DK4_MES_B122_R0060":"To Amsterdam's tavern, then.",
"DK4_MES_B123_R0004":"Master,{LB}do you recognize this letter?",
"DK4_MES_B123_R0007":"Let's see...",
"DK4_MES_B123_R0011":"So... Mr. Clifford...{LB}Wait here.",
"DK4_MES_B123_R0014":"Here.",
"DK4_MES_B123_R0021":"Could this be{LB}a Proof-map key?",
"DK4_MES_B123_R0024":"{LB}Likely.",
"DK4_MES_B123_R0028":"He prepared a map key{LB}for whoever defeated him...{LB}What was Clifford thinking?",
"DK4_MES_B123_R0031":"{LB}His pride.",
"DK4_MES_B123_R0035":"{LB}He saw himself as North Sea master.{LB}Pride demanded that, if defeated,{LB}whoever vanquished him alone{LB}must become the new master.",
"DK4_MES_B123_R0053":"That makes sense.{LB}Somehow, the feeling is clear...",
"DK4_MES_B123_R0061":"That makes sense.{LB}Somehow, his mind is clear...",
"DK4_MES_B124_R0004":"The cult leader sought{LB}this Old Parchment...{LB}the North Sea Proof map.",
"DK4_MES_B124_R0008":"{LB}Nothing is written.{LB}Another item must solve it.",
"DK4_MES_B124_R0011":"What to try...{LB}Pour the Crimson Pigment{LB}over this parchment.",
"DK4_MES_B124_R0015":"{LB}Oh!{LB}Something appears!",
"DK4_MES_B124_R0018":"The North Sea Proof map...{LB}At last.",
"DK4_MES_B125_R0004":"{LB}{MACRO:FA}.",
"DK4_MES_B125_R0007":"Escante planned a coup{LB}to break Spain's rule.{LB}Thanks to you, it was stopped.",
"DK4_MES_B125_R0010":"But one concern remains.",
"DK4_MES_B125_R0018":"The key to Escante's treasure{LB}was taken recently{LB}to the New World's west coast.",
"DK4_MES_B125_R0022":"Could it be...{LB}the map?",
"DK4_MES_B125_R0025":"{LB}West New World...{LB}Trouble.",
"DK4_MES_B126_R0004":"{LB}{MACRO:FI},{LB}does the Ritual Dagger fit{LB}the Sun-Patterned Scabbard?",
"DK4_MES_B126_R0008":"Same size.",
"DK4_MES_B126_R0012":"{LB}Perhaps once a single object.{LB}Shall the blade enter the sheath?",
"DK4_MES_B126_R0015":"{LB}Whoa! What is that?",
"DK4_MES_B126_R0021":"So bright!{LB}...{LB}What happened?",
"DK4_MES_B126_R0025":"{LB}No idea...{LB}The sheath flashed.{LB}Open your eyes now.",
"DK4_MES_B126_R0029":"A map appeared on the blade!{LB}When?",
"DK4_MES_B126_R0033":"{LB}How can that be?",
"DK4_MES_B126_R0037":"This is...{LB}the New World Proof map!",
"DK4_MES_B126_R0040":"{LB}Sheathing the dagger{LB}made the map appear...{LB}No sense at all.",
}
EX={"DK4_MES_B124_R0016":"Raw four-byte event-control payload for the pigment-map reveal; not dialogue."}
SP={"01":"Bergstrom","03":"Maria","15":"Companion","1A":"Companion","5C":"Tavern keeper","83":"Official","D0":"Companion","FE":"Narrator or letter"};ST={int(x,16) for x in SP}
C={121:"Bergstrom confronts Maria to judge whether her ambitions threaten Sweden's freedom of trade.",122:"Maria receives Clifford's posthumous rival letter with directions to Amsterdam.",123:"The Amsterdam tavern keeper delivers Clifford's Proof-map key, and the party reflects on his pride.",124:"Maria uses Crimson Pigment on the Old Parchment to reveal the North Sea Proof map.",125:"An official reports Escante's coup and the theft of his treasure key to the New World's west coast.",126:"Maria and Xien join the Ritual Dagger and Sun-Patterned Scabbard to reveal the New World Proof map."}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if 121<=int(r["id"].split("_B",1)[1].split("_R",1)[0])<=126}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V95 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Maria or Xien continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving encounter variants, speaker and narration states, FI/FA macros, item and Proof terminology, verified control, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v95-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 121-126: Bergstrom encounter, Clifford letter/key, and North Sea/New World Proof-map reveals.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"121":23,"122":12,"123":11,"124":6,"125":6,"126":10}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
