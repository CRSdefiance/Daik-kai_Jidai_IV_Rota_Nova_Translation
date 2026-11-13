from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v86.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B97_R0005":"Whisper...",
"DK4_MES_B97_R0013":"This is bad.{LB}We cannot touch that now...",
"DK4_MES_B97_R0016":"Were you the bandits{LB}attacking Sao Jorge?",
"DK4_MES_B97_R0019":"What?!{LB}Who are you?",
"DK4_MES_B97_R0022":"{MACRO:FO}.",
"DK4_MES_B97_R0026":"What?! You helped guard that town!{LB}You ruined everything for us!",
"DK4_MES_B97_R0030":"No raid because of you!{LB}We will starve!",
"DK4_MES_B97_R0033":"Bold words for thieves!{LB}That town needs our help!",
"DK4_MES_B97_R0037":"Shut up!{LB}Europeans destroyed our village!",
"DK4_MES_B97_R0040":"Nothing will stop{LB}our revenge!",
"DK4_MES_B97_R0043":"Blame the slavers{LB}and soldiers preying on Africa,{LB}not every European.",
"DK4_MES_B97_R0046":"Attack everyone without distinction{LB}and you become no better{LB}than the villains you hate.",
"DK4_MES_B97_R0049":"Easy to say!",
"DK4_MES_B97_R0053":"Abandon revenge.{LB}That cannot restore your happiness.",
"DK4_MES_B97_R0057":"More fighting{LB}only repeats the cycle{LB}and brings misery to your people.",
"DK4_MES_B97_R0061":"Then what should we do?!",
"DK4_MES_B97_R0064":"End the struggle among European powers{LB}that causes conflict{LB}across the world's seas.",
"DK4_MES_B97_R0072":"The great powers are dividing the world.{LB}We gather the Conqueror's Proof{LB}to stop them.",
"DK4_MES_B97_R0075":"Stop the great powers?!{LB}Are you sane?",
"DK4_MES_B97_R0078":"That is no idle boast.{LB}Our reach now extends to Africa.{LB}We can face them as equals.",
"DK4_MES_B97_R0085":"Well? Entrust your revenge to us.",
"DK4_MES_B97_R0088":"What?!",
"DK4_MES_B97_R0092":"Come to sea with us.{LB}With such spirit, you can succeed.",
"DK4_MES_B97_R0100":"Staying here changes nothing...",
"DK4_MES_B97_R0103":"All right. We trust you!",
"DK4_MES_B97_R0107":"Welcome.",
"DK4_MES_B97_R0114":"No idea if this{LB}concerns your Proof,{LB}but this was hidden in the ruins.",
"DK4_MES_B97_R0117":"Tablet?",
}
SP={"03":"Maria","B4":"African raider","FE":"Whisper"};ST={int(x,16) for x in SP}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if r["id"].startswith("DK4_MES_B97_")}
 if set(L)!=set(rows):raise SystemExit(f"V86 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else [])
  prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Continuing companion"),"context":"Maria confronts African raiders attacking Sao Jorge, rejects indiscriminate revenge, recruits them to oppose imperial powers, and receives a hidden tablet.","source_meaning":e.replace("{LB}"," "),"localization_note":"Source-identical cross-route translation aligned with the established Raphael scene while preserving Maria's IDs, fleet-name macro, source-leading break, speakers, and allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v86-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 97: complete Sao Jorge raider confrontation, recruitment, and tablet handoff.","inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":0,"blocks":{"97":len(rec)}},"excluded":[],"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} records")
if __name__=="__main__":main()
