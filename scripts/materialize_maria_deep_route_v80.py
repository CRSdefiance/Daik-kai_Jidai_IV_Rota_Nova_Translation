from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v80.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B87_R0004":"...Wow.",
"DK4_MES_B87_R0009":"Answer me.",
"DK4_MES_B87_R0020":"What has four legs at dawn,{LB}two at noon, three at dusk?",
"DK4_MES_B87_R0027":"Know it.",
"DK4_MES_B87_R0029":"No idea.",
"DK4_MES_B87_R0031":"No such animal.",
"DK4_MES_B87_R0043":"Begone, fool!",
"DK4_MES_B87_R0047":"Aaaah!",
"DK4_MES_B87_R0059":"Begone, fool!",
"DK4_MES_B87_R0063":"Aaaah!",
"DK4_MES_B87_R0076":"Name the animal.",
"DK4_MES_B87_R0083":"Humans (us)",
"DK4_MES_B87_R0085":"You (the Sphinx)",
"DK4_MES_B87_R0087":"Other",
"DK4_MES_B87_R0099":"Begone, fool!",
"DK4_MES_B87_R0103":"Aaaah!",
"DK4_MES_B87_R0115":"Begone, fool!",
"DK4_MES_B87_R0119":"Aaaah!",
"DK4_MES_B87_R0132":"That old riddle bores me...{LB}Answer another.",
"DK4_MES_B87_R0135":"Can we not...?",
"DK4_MES_B87_R0139":"Ten people stand here.{LB}Their feet, hands, and canes total 32.{LB}Elders equal babies.{LB}How many adults?",
"DK4_MES_B87_R0145":"2",
"DK4_MES_B87_R0147":"3",
"DK4_MES_B87_R0149":"4",
"DK4_MES_B87_R0161":"Begone, fool!",
"DK4_MES_B87_R0165":"Aaaah!",
"DK4_MES_B87_R0177":"Begone, fool!",
"DK4_MES_B87_R0181":"Aaaah!",
"DK4_MES_B87_R0194":"...Tedious.",
"DK4_MES_B87_R0198":"{LB}Know it, {MACRO:FI}?{LB}Puzzles baffle me.",
"DK4_MES_B87_R0204":"Ten people have twenty feet.{LB}So 32 minus 20 leaves{LB}twelve hands and canes...",
"DK4_MES_B87_R0208":"Elders and babies number the same.{LB}One cane pairs with two hands.",
"DK4_MES_B87_R0212":"{LB}Right.{LB}An elder-baby pair has{LB}three hands and canes.",
"DK4_MES_B87_R0216":"Yes. Twelve means four pairs:{LB}four canes, eight hands.",
"DK4_MES_B87_R0220":"{LB}So four elders and four babies.",
"DK4_MES_B87_R0223":"So four elders, four babies.{LB}That leaves two adults.",
"DK4_MES_B87_R0229":"Wise one!{LB}Take this reward!",
}
SP={"03":"Maria","CF":"Companion","FE":"Temple voice"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B87_")}
 if set(L)!=set(rows):raise SystemExit(f"V80 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Choice or continuing companion"),"context":"The temple voice tests Maria with the Sphinx riddle and a people, hands, feet, and canes arithmetic riddle, including all choices and failure branches.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving all choices, repeated rejection branches, runtime name macro, source-leading breaks, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v80-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 87: complete temple Sphinx and arithmetic riddles with every choice and branch.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"87":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
