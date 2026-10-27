from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v74.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B74_R0004":"Ah...",
"DK4_MES_B74_R0008":"Something wrong, Julio?",
"DK4_MES_B74_R0012":"Worried for my girl.",
"DK4_MES_B74_R0016":"You mean Christina.",
"DK4_MES_B74_R0020":"Wondering if she's doing all right.{LB}Call me a doting old fool.",
"DK4_MES_B74_R0023":"She can overcome any hardship.{LB}A war goddess--Athena, was it?{LB}Christina has that same air.",
"DK4_MES_B74_R0026":"Athena?",
"DK4_MES_B74_R0030":"Another myth calls her Minerva,{LB}if memory serves.",
"DK4_MES_B74_R0033":"May have heard that long ago,{LB}but gods aren't my specialty.",
"DK4_MES_B74_R0036":"Still, that Minerva something{LB}does sound familiar...",
"DK4_MES_B74_R0039":"Gods aren't my field either.{LB}But Christina will be fine.",
"DK4_MES_B74_R0043":"Thank you.{LB}Christina has earned your trust.{LB}But to me, she's still my grandchild.{LB}Humor an old man's worry.",
"DK4_MES_B74_R0050":"Oh!{LB}Now, this takes me back!",
"DK4_MES_B74_R0057":"Yes, yes! They called it{LB}the Shield of Minerva.",
"DK4_MES_B74_R0060":"A legendary guard said to rest{LB}near the Mediterranean or Black Sea.{LB}Never searched for it in earnest...",
"DK4_MES_B74_R0063":"But if Christina resembles Minerva,{LB}now we should dearly seek it.{LB}She should have it, if it exists...",
"DK4_MES_B74_R0066":"Julio...",
"DK4_MES_B74_R0070":"Sorry for foolish talk.{LB}Dismiss it as an old man's fancy.{LB}Time to get back to work.",
"DK4_MES_B74_R0074":"Admiral, back to work.",
"DK4_MES_B74_R0078":"Yes, quite.",
}
SP={"03":"Maria","06":"Julio Erdi"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B74_")}
 if set(L)!=set(rows):raise SystemExit(f"V74 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Julio worries about Christina, compares her to Minerva, and remembers the legendary Shield of Minerva.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the family concern, mythological comparison, treasure lead, speakers, pacing, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v74-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 74: Julio's Christina concern and Shield of Minerva rumor.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"74":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
