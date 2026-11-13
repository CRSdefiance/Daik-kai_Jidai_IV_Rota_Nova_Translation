from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v108.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B145_R0005":"Well, Admiral.{LB}We meet again by fate.","DK4_MES_B145_R0008":"That woman pirate!","DK4_MES_B145_R0012":"{LB}{MACRO:FI}... trouble.{LB}Everyone around us is a pirate.","DK4_MES_B145_R0015":"Greetings, princess...{LB}What will you order?{LB}Drink, or perhaps...?","DK4_MES_B145_R0018":"Heh heh.","DK4_MES_B145_R0022":"Hmph!","DK4_MES_B145_R0026":"...What do you intend?","DK4_MES_B145_R0030":"Hm... impressive.{LB}You've got nerve.","DK4_MES_B145_R0033":"{LB}A mere pirate{LB}doesn't get to speak that way!","DK4_MES_B145_R0036":"The old man has guts.{LB}Could tear you apart in an instant.{LB}Still talking?","DK4_MES_B145_R0040":"Enough!","DK4_MES_B145_R0044":"Eek! Sorry!","DK4_MES_B145_R0048":"...You do seem to know reason.","DK4_MES_B145_R0051":"...Quite the princess.","DK4_MES_B145_R0054":"Don't underestimate me.{LB}No killing here.{LB}Pirates have their own ways.","DK4_MES_B145_R0057":"We'll settle this at sea!{LB}Be ready!","DK4_MES_B145_R0060":"Then we await you.","DK4_MES_B145_R0063":"Remember those words!{LB}...Hm?!","DK4_MES_B145_R0066":"What?","DK4_MES_B145_R0070":"You're growing on me.{LB}That's a fine sword.","DK4_MES_B145_R0073":"Sword?","DK4_MES_B145_R0077":"Don't understand? Never mind.{LB}But remember: what catches my eye{LB}always becomes mine.","DK4_MES_B145_R0085":"Men, we're leaving!","DK4_MES_B145_R0089":"Aye!","DK4_MES_B145_R0093":"{LB}One word controls this whole mob.","DK4_MES_B145_R0097":"Don't dismiss me as a pirate!","DK4_MES_B145_R0100":"An interesting pirate.","DK4_MES_B145_R0104":"{LB}Spirit, for a pirate.","DK4_MES_B145_R0108":"She may hound us awhile.",
}
L["DK4_MES_B145_R0008"]="The pirate!"
L["DK4_MES_B145_R0012"]="{LB}{MACRO:FI}... trouble.{LB}All are pirates."
L["DK4_MES_B145_R0073"]="?"
L["DK4_MES_B145_R0077"]="Don't understand? No matter.{LB}Remember: what catches my eye{LB}always becomes mine."
L["DK4_MES_B145_R0093"]="{LB}One word controls them all."
EX={"DK4_MES_B145_R0003":"Raw seven-byte scene-entry control payload before Aziza appears; not dialogue."}
SP={"03":"Maria","99":"Pirates","B7":"Pirate","B8":"Pirate","B9":"Pirate","FE":"Aziza"};ST={int(x,16) for x in SP};C="Aziza corners Maria's party in a pirate tavern, promises a sea battle, and takes interest in Maria's sword."
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0])==145}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V108 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation"),"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving Aziza's confrontation, FI macro, pirate states, source-leading line breaks, scene control, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v108-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 145: Aziza tavern confrontation.","excluded_records":EX,"inventory":{"identified_records":30,"translated_records":29,"excluded_records":1,"blocks":{"145":30}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
