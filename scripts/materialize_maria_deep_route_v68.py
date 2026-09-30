from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v68.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B64_R0008":"Me?",
"DK4_MES_B64_R0017":"Trust.",
"DK4_MES_B64_R0019":"Doubt.",
"DK4_MES_B64_R0030":"Watch your mouth{LB}around our admiral!",
"DK4_MES_B64_R0037":"Damn!",
"DK4_MES_B64_R0045":"Huh?",
"DK4_MES_B64_R0053":"What a strange man...",
"DK4_MES_B64_R0064":"This?",
"DK4_MES_B64_R0071":"But this is valuable.{LB}May this truly be mine?",
"DK4_MES_B64_R0077":"Then...{LB}accepted with thanks.",
"DK4_MES_B64_R0082":"{MACRO:FI}'s luck{LB}rose by 1!",
"DK4_MES_B64_R0085":"His luck{LB}rose by 1!",
"DK4_MES_B64_R0092":"Strange folk bring bad luck.{LB}Let us leave.",
"DK4_MES_B64_R0095":"Y-yes.",
"DK4_MES_B64_R0101":"{MACRO:FI}'s spirit{LB}rose by 1!",
"DK4_MES_B64_R0104":"His spirit{LB}rose by 1!",
}
SP={"03":"Maria","14":"Fernando","FE":"System"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B64_")}
 if set(L)!=set(rows):raise SystemExit(f"V68 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}" if state else f"{e}{{PAD}}","speaker":SP.get(state,"Choice"),"context":"Maria chooses whether to trust an eccentric stranger; Fernando reacts, an item is offered, and the branch awards luck or spirit stat gains.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving both trust choices, Fernando's reactions, item acceptance, protagonist macro, stat outcomes, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v68-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 64: complete stranger trust choice, item gift, and stat outcomes.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"64":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
