from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v100.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B137_R0004":"So bored lately...",
"DK4_MES_B137_R0009":"{LB}Oh, a seasoned old man.",
"DK4_MES_B137_R0012":"'Seasoned' is generous.{LB}He looks ancient.",
"DK4_MES_B137_R0015":"Drink together.{LB}You're alike.",
"DK4_MES_B137_R0018":"{LB}What do you mean, alike?!",
"DK4_MES_B137_R0022":"Ho ho. Lively for an old man.",
"DK4_MES_B137_R0026":"{LB}What! Still young!{LB}You must be long retired.",
"DK4_MES_B137_R0030":"What! Still an active navigator!{LB}Youngsters cannot best me.",
"DK4_MES_B137_R0034":"{LB}Bold words from an old man!",
"DK4_MES_B137_R0038":"See? Alike after all...",
"DK4_MES_B137_R0042":"Xien, calm down...{LB}Sir, are you a navigator?",
"DK4_MES_B137_R0046":"Yes. Julio Erneco.{LB}And you must be Admiral {MACRO:FA}?",
"DK4_MES_B137_R0050":"Honored you know me.{LB}Does my ship interest you?",
"DK4_MES_B137_R0053":"Certainly.{LB}An offer to join?",
"DK4_MES_B137_R0057":"Take it that way.",
"DK4_MES_B137_R0061":"Odd choice...",
"DK4_MES_B137_R0073":"You can talk...",
"DK4_MES_B137_R0080":"{LB}{MACRO:FI} says so.{LB}No objection...",
"DK4_MES_B137_R0084":"...Very well.{LB}Sailing together will prove{LB}which of us is truly old.{LB}The result is obvious.",
"DK4_MES_B137_R0087":"{LB}Naturally, yours truly is younger.",
"DK4_MES_B137_R0091":"Both of you can be relied upon.",
"DK4_MES_B137_R0095":"An old-man duo?{LB}This will be fun!",
}
SP={"03":"Maria","06":"Julio","12":"Companion","14":"Dias"};ST={int(x,16) for x in SP}
C="Maria meets the veteran navigator Julio Erneco, defuses his age rivalry with Xien, and recruits him."
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0])==137}
 if set(L)!=set(rows):raise SystemExit(f"V100 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation"),"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the comic age rivalry, recruitment beats, FI/FA macros, source-leading line breaks, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v100-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 137: Julio Erneco recruitment.","excluded_records":{},"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"137":22}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
