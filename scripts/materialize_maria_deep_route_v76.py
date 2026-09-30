from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v76.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B76_R0004":"Admiral, a moment?",
"DK4_MES_B76_R0008":"What is it?",
"DK4_MES_B76_R0012":"Seek the Jaguar God's Vest!",
"DK4_MES_B76_R0016":"What is that?",
"DK4_MES_B76_R0020":"A vest bearing the Jaguar God.{LB}They say it's in the New World.",
"DK4_MES_B76_R0024":"Another new rumor, then.",
"DK4_MES_B76_R0028":"Yeah.{LB}The last one.",
"DK4_MES_B76_R0031":"Last?",
"DK4_MES_B76_R0035":"Tracking down locations is hard.{LB}And now it bores me.",
"DK4_MES_B76_R0038":"My interests fade fast.{LB}Animals are fun, but only if you{LB}can cook them. Any rumor that{LB}finds me, you'll hear.",
"DK4_MES_B76_R0041":"R-right.{LB}Back to the vest--where{LB}in the New World is it?",
"DK4_MES_B76_R0045":"Hmm.{LB}Maybe the western side?",
"DK4_MES_B76_R0048":"Can you narrow that down?",
"DK4_MES_B76_R0052":"Sorry.{LB}That's all we know.{LB}Just keep it in mind, okay?",
"DK4_MES_B76_R0055":"Heh. All right.",
}
SP={"03":"Maria","16":"Samwell"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B76_")}
 if set(L)!=set(rows):raise SystemExit(f"V76 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Samwell shares his final deliberately vague equipment rumor, the Vest of the Jaguar God in the New World.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Samwell's fickle humor, the treasure clue, speakers, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v76-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 76: Samwell's complete Vest of the Jaguar God rumor.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"76":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
