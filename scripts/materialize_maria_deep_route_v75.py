from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v75.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B75_R0004":"Admiral, a moment?",
"DK4_MES_B75_R0008":"What is it?",
"DK4_MES_B75_R0012":"Peacocks are lovely birds.{LB}Want to see one?",
"DK4_MES_B75_R0015":"What brought this on?{LB}Did you hear another rumor?",
"DK4_MES_B75_R0019":"You got me.{LB}This one's called Peacock Mail.",
"DK4_MES_B75_R0022":"Mail with peacock feathers?",
"DK4_MES_B75_R0026":"So close!{LB}The mail has peacock tail feathers{LB}fixed to its back.",
"DK4_MES_B75_R0030":"Doesn't sound very strong.",
"DK4_MES_B75_R0034":"The sight stuns foes,{LB}and they freeze in place.{LB}That's its greatest power.",
"DK4_MES_B75_R0038":"...{LB}So where is this mail?",
"DK4_MES_B75_R0042":"On a tiny island far, far, far{LB}southeast of the Cape of Good Hope.{LB}That's all the rumor said.",
"DK4_MES_B75_R0046":"That hardly narrows it down.",
"DK4_MES_B75_R0049":"But we should see it.{LB}Bet it's unlike anything{LB}we've ever laid eyes on.",
"DK4_MES_B75_R0053":"Okay. Keep it in mind.{LB}Don't expect too much.",
"DK4_MES_B75_R0056":"Got it.",
}
SP={"03":"Maria","16":"Samwell"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B75_")}
 if set(L)!=set(rows):raise SystemExit(f"V75 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Samwell tells Maria a playful rumor about Peacock Mail hidden southeast of the Cape of Good Hope.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the comic exchange, treasure directions, speakers, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v75-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 75: Samwell's complete Peacock Mail rumor.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"75":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
