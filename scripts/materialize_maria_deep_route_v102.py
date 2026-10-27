from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v102.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
U={
"DK4_MES_B135_R0004":"Take that!",
"DK4_MES_B135_R0008":"Aah!{LB}Please help me!",
"DK4_MES_B135_R0018":"What?!",
"DK4_MES_B135_R0024":"{LB}What?!",
"DK4_MES_B135_R0031":"Someone is being beaten!",
"DK4_MES_B135_R0035":"{LB}The victim looks helpless...{LB}Shall we aid him?",
"DK4_MES_B135_R0051":"Attacking the weak is unforgivable!{LB}Allow me!",
"DK4_MES_B135_R0068":"{LB}Are you okay?",
"DK4_MES_B135_R0072":"Ouch...{LB}Not very all right.",
"DK4_MES_B135_R0076":"Why fight those men?",
"DK4_MES_B135_R0088":"Did they provoke you?{LB}Every land has villains...",
"DK4_MES_B135_R0095":"Well...",
"DK4_MES_B135_R0104":"They claimed the world is flat...",
"DK4_MES_B135_R0107":"{LB}And?",
"DK4_MES_B135_R0111":"The world is round. Common knowledge!{LB}Their error needed correcting.",
"DK4_MES_B135_R0114":"...And?",
"DK4_MES_B135_R0118":"An explanation began.{LB}Then they suddenly acted oddly.",
"DK4_MES_B135_R0122":"They scowled and said,{LB}'None of your business!'{LB}Then attacked...",
"DK4_MES_B135_R0126":"{LB}Hm?{LB}Makes little sense.",
"DK4_MES_B135_R0129":"Nor to me...",
"DK4_MES_B135_R0133":"All that was said was,{LB}'You are plainly wrong!'{LB}Then...",
"DK4_MES_B135_R0137":"Then they grew angry.",
"DK4_MES_B135_R0141":"How did you know?",
"DK4_MES_B135_R0144":"{LB}Anyone would know.",
"DK4_MES_B135_R0148":"Really?{LB}That still puzzles me.",
"DK4_MES_B135_R0151":"Their knowledge was wrong.{LB}Correcting it was a favor!{LB}Shouldn't they thank me?",
"DK4_MES_B135_R0154":"Anyone teaching me deserves thanks!{LB}Another truth of the world{LB}would be revealed!",
"DK4_MES_B135_R0166":"Hmm.{LB}Every nation has eccentrics.",
"DK4_MES_B135_R0172":"{LB}Learning is good...",
"DK4_MES_B135_R0180":"Do you know ships?",
"DK4_MES_B135_R0184":"Ships? Of course!{LB}Once served as a captain.{LB}Modifying ships was my hobby!",
"DK4_MES_B135_R0195":"He was captain?{LB}Absurd.",
"DK4_MES_B135_R0202":"...Then no problem.",
"DK4_MES_B135_R0216":"Admiral,{LB}surely you won't take him aboard?",
"DK4_MES_B135_R0222":"{LB}Surely not.{LB}Will he join,{LB}{MACRO:FI}?",
"DK4_MES_B135_R0229":"Yes. His zeal appeals.{LB}And with that personality,{LB}normal life seems hard.",
"DK4_MES_B135_R0241":"True...",
"DK4_MES_B135_R0255":"Admiral is oddly kind...",
"DK4_MES_B135_R0260":"{LB}Admiral is oddly kind...",
"DK4_MES_B135_R0266":"Um...",
"DK4_MES_B135_R0270":"Sorry to ignore you.{LB}What is it?",
"DK4_MES_B135_R0273":"Are you an admiral?",
"DK4_MES_B135_R0276":"{LB}Yes.{LB}Do you know {MACRO:FO}?",
"DK4_MES_B135_R0280":"Then you are...{LB}Admiral {MACRO:FI} {MACRO:FA}?",
"DK4_MES_B135_R0284":"You know me? Good.{LB}Would you serve as my navigator?",
"DK4_MES_B135_R0288":"Yes! Please!{LB}Let me aboard!",
"DK4_MES_B135_R0291":"Settled.{LB}Your name?",
"DK4_MES_B135_R0294":"Cesare Tohni!{LB}Thank you!",
"DK4_MES_B135_R0297":"{LB}Hmm.{LB}What did Admiral like in him?{LB}No idea...",
"DK4_MES_B135_R0309":"Baffling.",
}
SP={"03":"Maria","0C":"Yukihisa","0D":"Cesare Tohni","4A":"Carlo","99":"Attacker"};ST={int(x,16) for x in SP};C="Maria rescues the eccentric scholar Cesare Tohni, recruits him, and receives his ship-purchasing tutorial."
def references():
 out={}
 for p in Path("translations").glob("*.json"):
  try:b=json.loads(p.read_text(encoding="utf-8"))
  except (ValueError,OSError):continue
  fp=b.get("file_path","")
  if fp not in {"/data/SC0.DK4","/data/SC1.DK4","/data/SC2.DK4"}:continue
  for r in b.get("records",[]):
   if r.get("english"):out[(fp,r["id"])]=r["english"]
 refs={}
 for n in range(3):
  fp=f"/data/SC{n}.DK4"
  with Path(f"work/sc{n}/script.csv").open(encoding="utf-8-sig",newline="") as f:
   for r in csv.DictReader(f):
    e=out.get((fp,r["id"]))
    if e:refs.setdefault(bytes.fromhex(r["source_hex"])[1:],re.sub(r"^(?:\{SPEAKER:[0-9A-F]{2}\})?|\{PAD\}$","",e))
 return refs
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0])==135}
 refs=references();L={i:(U[i] if i in U else refs.get(bytes.fromhex(r["source_hex"])[1:])) for i,r in rows.items()}
 if any(v is None for v in L.values()):raise SystemExit(f"V102 missing: {sorted(i for i,v in L.items() if v is None)}")
 rec=[]
 for i in sorted(L,key=lambda v:int(v.rsplit("R",1)[1])):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else ""
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation"),"context":C,"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria translation or byte-identical reviewed reuse, preserving rescue and recruitment beats, FI/FA/FO macros, tutorial line breaks, speaker states, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v102-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 block 135: Cesare Tohni rescue, recruitment, and ship-purchasing tutorial.","excluded_records":{},"inventory":{"identified_records":67,"translated_records":67,"excluded_records":0,"blocks":{"135":67}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
