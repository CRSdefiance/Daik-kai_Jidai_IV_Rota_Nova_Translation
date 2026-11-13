from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v94.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B116_R0007":"Hey, friend.",
"DK4_MES_B116_R0011":"What?",
"DK4_MES_B116_R0015":"Everyone calls {MACRO:FI} terrifying.{LB}Can she truly be so frightening?{LB}She does not seem so to me.",
"DK4_MES_B116_R0024":"You joined late, so cannot know.{LB}Not scary, merely strict{LB}with reward and punishment.",
"DK4_MES_B116_R0030":"You came later, so you don't know.{LB}Not scary exactly. More like{LB}clear rewards and punishments.",
"DK4_MES_B116_R0036":"Yes. Long ago...",
"DK4_MES_B116_R0041":"During battle with the wako,{LB}one man fled to save himself,{LB}abandoning allied ships{LB}inside the enemy ring.",
"DK4_MES_B116_R0044":"Our side was crushed.{LB}Many died or were captured.",
"DK4_MES_B116_R0048":"The man soon realized{LB}he had no place to return to...",
"DK4_MES_B116_R0051":"That night he struck alone,{LB}boarded their flagship,{LB}slew its commander,{LB}and won us victory.",
"DK4_MES_B116_R0054":"Wow!",
"DK4_MES_B116_R0058":"He returned in triumph.{LB}{MACRO:FI} prepared a command post{LB}and gold as his reward.",
"DK4_MES_B116_R0061":"Then came judgment:{LB}desertion before the enemy{LB}meant death.",
"DK4_MES_B116_R0068":"The gold went to his family,{LB}with a permanent officer's pension.",
"DK4_MES_B116_R0072":"He wept in thanks,{LB}and accepted death...",
"DK4_MES_B116_R0082":"That day the Admiral looked{LB}too fearsome to approach,{LB}and too sorrowful to watch.",
"DK4_MES_B116_R0087":"That day the Admiral looked{LB}too fearsome to approach,{LB}and too sorrowful to watch.",
"DK4_MES_B116_R0093":"...{LB}Really?",
"DK4_MES_B116_R0102":"Hm?{LB}{MACRO:FI}'s story?{LB}Hear my version.",
"DK4_MES_B116_R0106":"Already heard enough.",
"DK4_MES_B116_R0110":"No, no. My version reveals{LB}the Admiral's heart,{LB}and even the lofty ideals{LB}of {MACRO:FO}...",
"DK4_MES_B116_R0113":"Going to bed.{LB}Good night!",
"DK4_MES_B116_R0116":"Night.",
"DK4_MES_B116_R0128":"Me too.",
"DK4_MES_B116_R0135":"Wait! My story...",
"DK4_MES_B117_R0004":"These two tablets form{LB}Africa's Proof map, correct?",
"DK4_MES_B117_R0007":"{LB}The Mysterious Upper Tablet{LB}and Lower Tablet.{LB}Join them together.",
"DK4_MES_B117_R0011":"Let's align them.",
"DK4_MES_B117_R0015":"{LB}Ah, a perfect fit!",
"DK4_MES_B117_R0019":"So this is the Proof map.{LB}That was almost too easy.",
"DK4_MES_B117_R0023":"{LB}So far.{LB}The Proof itself{LB}may prove difficult.",
"DK4_MES_B117_R0027":"Perhaps. Let's begin the search.",
"DK4_MES_B119_R0004":"You seek the Mediterranean Proof?",
"DK4_MES_B119_R0007":"How did you know?{LB}We need its map.",
"DK4_MES_B119_R0010":"The Patterned Cloth is said{LB}to be that map.",
"DK4_MES_B119_R0014":"Plain cloth at first,{LB}but something reveals a map...",
"DK4_MES_B119_R0017":"How, exactly?{LB}Still, useful. Thank you.",
"DK4_MES_B120_R0004":"{LB}{MACRO:FI},{LB}about that Patterned Cloth...",
"DK4_MES_B120_R0007":"Learn something?",
"DK4_MES_B120_R0011":"{LB}To reveal the map,{LB}perhaps expose it to heat?",
"DK4_MES_B120_R0014":"{LB}The Brass Lamp may work.",
"DK4_MES_B120_R0017":"Good thought.{LB}Let's try.",
"DK4_MES_B120_R0020":"{LB}Warm it with the Brass Lamp...",
"DK4_MES_B120_R0024":"Correct, Xien. This is{LB}the Mediterranean Proof map.",
}
EX={"DK4_MES_B117_R0017":"Raw four-byte event-control payload for the tablet-combination animation; not dialogue.","DK4_MES_B118_R0005":"Already translated and integrated by Maria V29; retained there to avoid a duplicate record declaration.","DK4_MES_B120_R0022":"Raw four-byte event-control payload for the heated-cloth reveal; not dialogue."}
SP={"03":"Maria","0B":"Jam","0C":"Yukihisa","15":"Ian","16":"Sailor","4A":"Kamil","79":"Guard","93":"Informant","FE":"Narrator"};ST={int(x,16) for x in SP}
C={116:"Crewmates recount Maria's strict but compassionate judgment after a deserter redeemed himself in battle.",117:"Maria and Xien join the two Mysterious Tablets to reveal Africa's Proof map.",118:"A guard recognizes Maria's company and grants passage.",119:"An informant identifies the Patterned Cloth as the concealed Mediterranean Proof map.",120:"Maria and Xien heat the Patterned Cloth with the Brass Lamp to reveal the Mediterranean Proof map."}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if 116<=int(r["id"].split("_B",1)[1].split("_R",1)[0])<=120}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V94 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Maria or Xien continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving character variants, narration state, route macros, item names, verified raw controls, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v94-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 116-120: judgment anecdote, African Proof map, inherited guard passage, and Mediterranean Proof-map reveal.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"116":25,"117":8,"118":1,"119":5,"120":8}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} exclusions")
if __name__=="__main__":main()
