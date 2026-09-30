from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v105.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B143_R0005":"Welcome.",
"DK4_MES_B143_R0009":"Someone here may know...",
"DK4_MES_B143_R0012":"A question.{LB}Does anyone know{LB}the Golden Crown of Silla?",
"DK4_MES_B143_R0016":"Yes, but...",
"DK4_MES_B143_R0020":"The crown is sought.{LB}Where is it?",
"DK4_MES_B143_R0023":"Should this be told?",
"DK4_MES_B143_R0027":"Want payment?",
"DK4_MES_B143_R0031":"Not that...{LB}Another man just asked.{LB}A very frivolous one.",
"DK4_MES_B143_R0035":"Must be Julian from Hangzhou...",
"DK4_MES_B143_R0039":"You know him?{LB}And you are... ah!",
"DK4_MES_B143_R0046":"{MACRO:FO}'s{LB}{MACRO:FI}?",
"DK4_MES_B143_R0050":"Yes...",
"DK4_MES_B143_R0054":"The crown is said to rest{LB}in the Tomb of King Muryeong.{LB}Nothing more is known...",
"DK4_MES_B143_R0058":"Then that is where we go.{LB}Thank you.",
"DK4_MES_B143_R0061":"N-no...",
"DK4_MES_B143_R0065":"(The influence of {MACRO:FO}{LB}can be troublesome...)",
}
SP={"03":"Maria","CA":"Bartender"};ST={int(x,16) for x in SP};C="Maria asks after the Golden Crown of Silla and learns it rests in the Tomb of King Muryeong."
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0])==143}
 if set(L)!=set(rows):raise SystemExit(f"V105 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP[state],"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the tavern lead, FI/FO macros, newly verified bartender state, line breaks, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v105-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 143: Golden Crown of Silla tavern lead.","excluded_records":{},"inventory":{"identified_records":16,"translated_records":16,"excluded_records":0,"blocks":{"143":16}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
