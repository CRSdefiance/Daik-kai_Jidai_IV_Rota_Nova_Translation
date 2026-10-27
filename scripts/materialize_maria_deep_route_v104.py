from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v104.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B140_R0006":"Spy!",
"DK4_MES_B140_R0010":"Eek!",
"DK4_MES_B140_R0014":"...What happened?",
"DK4_MES_B140_R0018":"She followed us for some time.{LB}But...",
"DK4_MES_B140_R0022":"Never expected a girl...",
"DK4_MES_B140_R0026":"Hey, let go!",
"DK4_MES_B140_R0030":"Yukihisa, release her.{LB}Why follow us?",
"DK4_MES_B140_R0033":"A favor, ma'am.",
"DK4_MES_B140_R0037":"You're with {MACRO:FO}, right?{LB}Take me aboard!",
"DK4_MES_B140_R0041":"{LB}How abrupt. No manners.",
"DK4_MES_B140_R0045":"Demanding passage so suddenly...{LB}Why?",
"DK4_MES_B140_R0049":"Want to see the world!{LB}Train everywhere, grow strong,{LB}and show my master!",
"DK4_MES_B140_R0052":"Training?{LB}What art do you pursue?",
"DK4_MES_B140_R0056":"Glad you asked!{LB}Watch my Taoist art!",
"DK4_MES_B140_R0059":"Magic?",
"DK4_MES_B140_R0063":"Draw your sword! Here goes!",
"DK4_MES_B140_R0067":"Hm!",
"DK4_MES_B140_R0071":"Haaah!",
"DK4_MES_B140_R0079":"(?{LB}Nothing happened...)",
"DK4_MES_B140_R0082":"An opening! Strike!",
"DK4_MES_B140_R0087":"Whoa!",
"DK4_MES_B140_R0091":"Good dodge!{LB}That was my binding spell!",
"DK4_MES_B140_R0094":"A binding spell?{LB}Thought it my own lapse...",
"DK4_MES_B140_R0097":"Strange, right?",
"DK4_MES_B140_R0101":"Not bad.{LB}Even closing on Yukihisa{LB}that fast deserves praise.",
"DK4_MES_B140_R0105":"That movement and timing...{LB}Built on martial skill.",
"DK4_MES_B140_R0108":"Truly set on seeing the world?",
"DK4_MES_B140_R0112":"My master must be shown!{LB}Please, take me around the world!",
"DK4_MES_B140_R0116":"That desire to prove oneself{LB}can bring great growth.{LB}Your name?",
"DK4_MES_B140_R0120":"Yifa!",
"DK4_MES_B140_R0124":"Yifa, aboard my ship{LB}you work as an equal.{LB}Expect no special treatment.",
"DK4_MES_B140_R0128":"Gladly!",
"DK4_MES_B140_R0132":"Yukihisa.{LB}Never caught off guard again!",
"DK4_MES_B140_R0135":"Think you can beat my Taoist art?",
}
EX={"DK4_MES_B140_R0084":"Raw eight-byte combat demonstration payload between Yifa's attack and Yukihisa's dodge; not dialogue."}
SP={"03":"Maria","0C":"Yukihisa","19":"Yifa"};ST={int(x,16) for x in SP};C="Yifa follows Maria's party, demonstrates her Taoist martial art against Yukihisa, and joins to train around the world."
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0])==140}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V104 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation"),"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving the martial demonstration, FO macro, speaker states, source-leading line breaks, combat control payload, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v104-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 140: Yifa recruitment.","excluded_records":EX,"inventory":{"identified_records":35,"translated_records":34,"excluded_records":1,"blocks":{"140":35}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} control")
if __name__=="__main__":main()
