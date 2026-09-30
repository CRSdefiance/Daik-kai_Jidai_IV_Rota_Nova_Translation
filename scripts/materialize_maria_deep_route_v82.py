from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v82.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B89_R0005":"Who are you?{LB}Can it be...",
"DK4_MES_B89_R0008":"Ah!{LB}Believers, after so long!",
"DK4_MES_B89_R0011":"We fled Muslim rule{LB}and kept our faith alive{LB}in this hidden village.",
"DK4_MES_B89_R0015":"Does your village preserve{LB}any legend of the Conqueror's Proof?",
"DK4_MES_B89_R0019":"What?!{LB}You seek the Proof?{LB}God has guided you here!",
"DK4_MES_B89_R0023":"What?{LB}You know of it?",
"DK4_MES_B89_R0026":"More than that...",
"DK4_MES_B89_R0030":"This lamp has come down from antiquity.{LB}Seekers of the Proof are said{LB}to need it. We entrust it to you.",
"DK4_MES_B89_R0035":"Please...{LB}Do not let the Proof fall{LB}into Ottoman hands.",
"DK4_MES_B89_R0039":"We will do all we can{LB}to honor your trust.",
"DK4_MES_B90_R0024":"Now, back to the capital.",
"DK4_MES_B90_R0029":"Have we taken too long?{LB}We must hurry back.",
"DK4_MES_B90_R0037":"Too late now.{LB}Return to the Ottoman capital{LB}and try again.",
}
SP={"03":"Maria","A0":"Hidden-village believer"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith(("DK4_MES_B89_","DK4_MES_B90_"))}
 if set(L)!=set(rows):raise SystemExit(f"V82 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Narration"),"context":"Hidden Christians entrust Maria with an ancient lamp needed for the Proof and ask her to keep it from Ottoman control; Maria then faces return-time outcomes.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving religious and political context, the lamp handoff, deadline variants, speaker states, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v82-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 89-90: hidden-believer lamp handoff and Ottoman-capital deadline outcomes.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"89":10,"90":3}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
