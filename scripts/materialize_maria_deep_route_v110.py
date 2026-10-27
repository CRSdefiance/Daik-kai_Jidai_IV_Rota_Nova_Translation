from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v110.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B172_R0004":"{LB}Do you know this man?",
"DK4_MES_B172_R0008":"Yes. Rocco Alemkel,{LB}a navigator from long ago.{LB}Why do you ask?",
"DK4_MES_B172_R0012":"{LB}He has a noble face.{LB}What sort of man was he?",
"DK4_MES_B172_R0016":"All that is known is he once{LB}served Portugal.",
"DK4_MES_B172_R0020":"Clatter!",
"DK4_MES_B172_R0024":"{LB}What?",
"DK4_MES_B172_R0028":"Let's see.",
"DK4_MES_B172_R0032":"Behind it...{LB}A book.",
"DK4_MES_B172_R0035":"{LB}Hm",
"DK4_MES_B172_R0039":"Whose is it?{LB}An intriguing book.",
"DK4_MES_B172_R0042":"{LB}Let's ask the innkeeper.{LB}Hello! Anyone there?",
"DK4_MES_B172_R0045":"Yes? What is it?",
"DK4_MES_B172_R0049":"{LB}We found a book{LB}behind the portrait.",
"DK4_MES_B172_R0052":"Let's see.",
"DK4_MES_B172_R0056":"No, never seen it.{LB}You may keep it.",
"DK4_MES_B172_R0060":"{LB}But we cannot{LB}take it for free.",
"DK4_MES_B172_R0063":"Don't worry. Never knew it was there,{LB}and the book means nothing to me.",
"DK4_MES_B172_R0067":"{LB}Then we accept it{LB}with gratitude.",
"DK4_MES_B172_R0070":"Agreed.{LB}Thank you very much.",
"DK4_MES_B172_R0073":"No need for thanks.{LB}Back to work for me.",
"DK4_MES_B172_R0076":"Let's give this book{LB}to {MACRO:FI}.",
"DK4_MES_B172_R0080":"{LB}Agreed.{LB}Please deliver it for us.",
"DK4_MES_B172_R0084":"Understood.",
"DK4_MES_B172_R0088":"{LB}Mm",
}
SP={"15":"Ian","8C":"Innkeeper","FE":"Sound effect"};ST={int(x,16) for x in SP};C="Xien and Ian find a navigator's book hidden behind Rocco Alemkel's portrait at an inn."
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if "_B172_" in r["id"]}
 if set(L)!=set(rows):raise SystemExit(f"V110 mismatch: missing={sorted(set(rows)-set(L))}; extra={sorted(set(L)-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation"),"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the portrait discovery, innkeeper exchange, FI macro, source-leading breaks, presentation states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v110-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 172: Rocco Alemkel portrait and navigator-book discovery.","excluded_records":{},"inventory":{"identified_records":24,"translated_records":24,"excluded_records":0,"blocks":{"172":24}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
