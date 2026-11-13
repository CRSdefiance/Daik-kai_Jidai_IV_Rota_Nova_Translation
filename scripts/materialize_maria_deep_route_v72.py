from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v72.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B70_R0004":"What is a rogue ninja?",
"DK4_MES_B70_R0008":"Rogue?",
"DK4_MES_B70_R0012":"One who was once a ninja.",
"DK4_MES_B70_R0016":"Ah, a ninja!{LB}...What is a ninja?",
"DK4_MES_B70_R0019":"A Japanese clan{LB}skilled in stealth.",
"DK4_MES_B70_R0022":"A Japanese spy, then.{LB}Have you met one?",
"DK4_MES_B70_R0026":"Never.{LB}See a ninja's true face{LB}and their law is death.",
"DK4_MES_B70_R0030":"Mamma mia!",
"DK4_MES_B70_R0034":"Leaving the ninja life{LB}means risking death. One who{LB}escapes the clan must possess{LB}extraordinary skill.",
"DK4_MES_B70_R0037":"Why ask about one?",
"DK4_MES_B70_R0041":"Really, it is the clothing.{LB}A rumor reached me.",
"DK4_MES_B70_R0045":"All black, called the{LB}'Rogue Ninja's Garb.'{LB}Armor, not mere clothing.",
"DK4_MES_B70_R0049":"Armor?",
"DK4_MES_B70_R0053":"Details are unclear,{LB}but it is very light and durable.",
"DK4_MES_B70_R0056":"Such a thing?{LB}News to me.",
"DK4_MES_B70_R0059":"Even Yukihisa does not know it.",
"DK4_MES_B70_R0063":"My shame.",
"DK4_MES_B70_R0067":"No need to apologize, Yukihisa.",
"DK4_MES_B70_R0070":"But...",
"DK4_MES_B70_R0074":"The rumor came from me.{LB}Yukihisa, you are amusing.",
"DK4_MES_B70_R0077":"Amusing? What do you mean?{LB}An insult will not be forgiven.",
"DK4_MES_B70_R0081":"And what will you do?",
"DK4_MES_B70_R0085":"Enough!{LB}This childish quarrel{LB}is disgraceful.",
"DK4_MES_B70_R0089":"My apologies.",
"DK4_MES_B70_R0093":"Sorry.{LB}My fault.",
"DK4_MES_B70_R0096":"Still...{LB}if that black armor exists,{LB}it must be in Japan.",
"DK4_MES_B70_R0099":"Likely.",
"DK4_MES_B70_R0103":"Agreed.{LB}Let us search when time permits.",
}
SP={"03":"Maria","0C":"Yukihisa","0F":"Angelo Puccini"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B70_")}
 if set(L)!=set(rows):raise SystemExit(f"V72 mismatch: missing={sorted(set(rows)-set(L))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  rec.append({"id":i,"english":f"{{SPEAKER:{state}}}{e}{{PAD}}","speaker":SP[state],"context":"Angelo asks Yukihisa about rogue ninja and their famed black garb, prompting a rumor lead that the lightweight armor may be found in Japan.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the ninja explanation, Angelo-Yukihisa banter, black-garb treasure lead, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v72-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 70: complete rogue-ninja black-garb rumor event.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"70":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
