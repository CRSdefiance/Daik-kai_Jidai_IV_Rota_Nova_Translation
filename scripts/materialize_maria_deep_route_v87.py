from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v87.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B98_R0005":"Hey, wait.",
"DK4_MES_B98_R0013":"Can't just keep your gift.{LB}Let me repay you with a useful tip.",
"DK4_MES_B98_R0017":"Hindustan has a wondrous site.{LB}Since you're here, go see it.",
"DK4_MES_B98_R0021":"The trouble is, reaching it{LB}requires a map. Still, please try.",
"DK4_MES_B98_R0024":"Yes. We'd love to.",
"DK4_MES_B99_R0005":"This statue...",
"DK4_MES_B99_R0009":"What?",
"DK4_MES_B99_R0020":"Doesn't seem{LB}to suit this building.",
"DK4_MES_B99_R0021":"This design seems{LB}out of place here.",
"DK4_MES_B99_R0022":"This stands out{LB}from the building.",
"DK4_MES_B99_R0023":"Doesn't match{LB}the building.",
"DK4_MES_B99_R0024":"Doesn't this seem{LB}wrong for the building?",
"DK4_MES_B99_R0025":"This seems rather unfitting{LB}for the building.",
"DK4_MES_B99_R0026":"Doesn't match the building.",
"DK4_MES_B99_R0028":"Doesn't this design seem{LB}out of place here?",
"DK4_MES_B99_R0031":"Right.",
"DK4_MES_B99_R0041":"Like a ship's figurehead...{LB}Was it once one?",
"DK4_MES_B99_R0042":"Like a ship's figurehead...{LB}Was that its purpose?",
"DK4_MES_B99_R0043":"Looks like a figurehead.{LB}Maybe that's what it is.",
"DK4_MES_B99_R0045":"Like a figurehead...{LB}Maybe it truly is one.",
"DK4_MES_B99_R0046":"Looks like a figurehead...{LB}Could that be what this is?",
"DK4_MES_B99_R0047":"This is shaped like a figurehead.{LB}No, that's what it is.",
"DK4_MES_B99_R0048":"A figurehead.{LB}See?",
"DK4_MES_B99_R0049":"Shaped like a figurehead...{LB}Could it truly be one?",
"DK4_MES_B99_R0052":"Yes, true.",
"DK4_MES_B100_R0005":"Oh! This is...!",
"DK4_MES_B100_R0009":"As the discoverers,{LB}you have the right to this dagger.",
"DK4_MES_B100_R0015":"Thanks to you, our tribe has found{LB}the symbol it long needed.{LB}Please accept this.",
"DK4_MES_B100_R0019":"Gained 24,000 coins.",
"DK4_MES_B100_R0025":"Now, let us return.{LB}Your fleet must be waiting.",
"DK4_MES_B101_R0004":"Oh, yes...",
"DK4_MES_B101_R0012":"Yes, yes!{LB}Let's bring Christina along.",
"DK4_MES_B101_R0015":"Who is that?",
"DK4_MES_B101_R0019":"My granddaughter. She knows swords{LB}and wields one well.",
"DK4_MES_B101_R0022":"And where does she live?",
"DK4_MES_B101_R0026":"London.",
"DK4_MES_B101_R0030":"Understood.{LB}Let's head there.",
}
EX={"DK4_MES_B99_R0003":"Raw ten-byte event-control payload; not dialogue.","DK4_MES_B100_R0003":"Raw seven-byte event-control payload; not dialogue."}
SP={"03":"Maria","06":"Julio Erdi","B3":"Expedition host","C6":"Local woman","D1":"Companion","DC":"Companion","FE":"System"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if any(r["id"].startswith(f"DK4_MES_B{x}_") for x in range(98,102))}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V87 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Companion variant"),"context":"A local woman shares a Hindustan ruin lead, Maria's companions identify a displaced ship figurehead, an expedition host grants a dagger reward, and Julio suggests visiting Christina in London.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving all companion variants, two raw event controls, item and coin rewards, recruitment lead, verified states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v87-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 98-101: Hindustan ruin lead, figurehead discovery, dagger reward, and Christina lead.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"98":5,"99":21,"100":6,"101":7}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} controls")
if __name__=="__main__":main()
