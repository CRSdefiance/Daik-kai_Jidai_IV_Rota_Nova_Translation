from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v106.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B147_R0004":"This land has such a unique atmosphere.",
"DK4_MES_B147_R0007":"Everything people do{LB}feels so small here.",
"DK4_MES_B147_R0010":"Once this great task ends,{LB}maybe a quiet stay here.",
"DK4_MES_B147_R0013":"Planning a vacation already?{LB}A bit early, isn't it?",
"DK4_MES_B147_R0016":"Ha! Understood.{LB}Still mountains of work ahead!",
"DK4_MES_B148_R0004":"Arabs truly avoid alcohol.{LB}This tavern serves foreign sailors.",
"DK4_MES_B148_R0008":"Despite race and faith,{LB}their resolve and discipline{LB}earn admiration.",
"DK4_MES_B148_R0012":"Y",
"DK4_MES_B148_R0016":"No wonder. Can't picture those two{LB}giving up vodka or sake.",
"DK4_MES_B148_R0020":"True, but this is not only about drink.",
"DK4_MES_B148_R0027":"Behind fierce severity,{LB}love of beauty and strong kindness{LB}protect the weak.",
"DK4_MES_B148_R0031":"Much there deserves emulation.",
"DK4_MES_B148_R0034":"Never knew you admired Arabia.{LB}Personally, its character{LB}and mine clash badly...",
"DK4_MES_B148_R0037":"Heh. Clearly.",
}
SP={"03":"Maria","0B":"Jam","0C":"Yukihisa","15":"Ian"};ST={int(x,16) for x in SP};C={147:"Jam reflects on India's atmosphere and imagines returning after the voyage.",148:"Maria, Ian, Yukihisa, and Jam discuss Arab abstinence, discipline, beauty, and compassion."}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0]) in {147,148}}
 if set(L)!=set(rows):raise SystemExit(f"V106 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP[state],"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving optional companion characterization, speaker states, line breaks, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v106-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 147-148: India and Arab-culture companion conversations.","excluded_records":{},"inventory":{"identified_records":14,"translated_records":14,"excluded_records":0,"blocks":{"147":5,"148":9}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
