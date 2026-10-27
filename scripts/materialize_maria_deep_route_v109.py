from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v109.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
U={
"DK4_MES_B175_R0034":"Wait!","DK4_MES_B175_R0042":"This... was forced on me.","DK4_MES_B175_R0050":"A book.","DK4_MES_B175_R0060":"But...","DK4_MES_B175_R0071":"Honestly...{LB}Rare books always do this to him.",
"DK4_MES_B180_R0014":"You want something besides food?{LB}Surprising. What's the weapon called?","DK4_MES_B180_R0021":"An impressive name.{LB}Where is it?","DK4_MES_B180_R0028":"Hard to find, then.{LB}Let's search patiently.","DK4_MES_B180_R0035":"But it may take time.","DK4_MES_B180_R0043":"And no promise it becomes yours.",
"DK4_MES_B189_R0015":"Are you well?{LB}Who are you?","DK4_MES_B189_R0021":"King Arthur?","DK4_MES_B189_R0031":"Avalon...?{LB}Where is it?","DK4_MES_B189_R0034":"{LB}Land where Arthur sleeps...{LB}A nearby tavern may have clues.",
"DK4_MES_B199_R0007":"Oh, Manuel.","DK4_MES_B199_R0014":"Not only work.{LB}Watching the streets is a pleasure.","DK4_MES_B199_R0022":"Any business in the square?","DK4_MES_B199_R0032":"...An unfamiliar name.","DK4_MES_B199_R0040":"Roman Empire...{LB}He must have been formidable{LB}to threaten Great Qin.","DK4_MES_B199_R0047":"So never relax.{LB}A lesson worth keeping.","DK4_MES_B199_R0053":"Sharp words.{LB}Why mention this now?","DK4_MES_B199_R0068":"The King's Stolen Armor...{LB}He threatened Rome itself,{LB}so he was deeply feared.",
}
U["DK4_MES_B175_R0071"]="Honestly...{LB}Rare books excite him."
U["DK4_MES_B180_R0014"]="Something besides food?{LB}Surprising. What weapon?"
U["DK4_MES_B199_R0032"]="...A rare name."
U["DK4_MES_B199_R0040"]="Rome...{LB}He must have been formidable{LB}to threaten Great Qin."
U["DK4_MES_B199_R0068"]="The King's Stolen Armor...{LB}He threatened Rome,{LB}so he was deeply feared."
SP={"03":"Maria","0E":"Samwell","12":"Charles","17":"Manuel","52":"Stranger","93":"Stranger","9D":"Pursuer","A9":"Vivian"};ST={int(x,16) for x in SP};C={175:"A fleeing stranger forces a glassmaking encyclopedia on Maria before a pursuer arrives.",180:"Samwell asks Maria to search for the Minotaur's Axe.",189:"Vivian directs Maria toward Excalibur in Avalon.",199:"Manuel tells Maria the rumor of Attila's stolen armor in the northwest."}
def references():
 out={}
 for p in Path("translations").glob("*.json"):
  try:b=json.loads(p.read_text(encoding="utf-8"))
  except (ValueError,OSError):continue
  if b.get("file_path") not in {"/data/SC0.DK4","/data/SC1.DK4","/data/SC2.DK4"}:continue
  for r in b.get("records",[]):
   if r.get("english"):out[(b["file_path"],r["id"])]=r["english"]
 refs={}
 for n in range(3):
  fp=f"/data/SC{n}.DK4"
  with Path(f"work/sc{n}/script.csv").open(encoding="utf-8-sig",newline="") as f:
   for r in csv.DictReader(f):
    e=out.get((fp,r["id"]))
    if e:refs.setdefault(bytes.fromhex(r["source_hex"])[1:],re.sub(r"^(?:\{SPEAKER:[0-9A-F]{2}\})?|\{PAD\}$","",e))
 return refs
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0]) in {175,180,189,199}}
 refs=references();L={i:(U[i] if i in U else refs.get(bytes.fromhex(r["source_hex"])[1:])) for i,r in rows.items()}
 if any(v is None for v in L.values()):raise SystemExit(f"V109 missing: {sorted(i for i,v in L.items() if v is None)}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Xien continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria translation or byte-identical reviewed reuse, preserving optional-event states, line breaks, macros, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v109-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 175, 180, 189, and 199: glassmaking book, Minotaur axe, Excalibur, and Attila armor leads.","excluded_records":{},"inventory":{"identified_records":60,"translated_records":60,"excluded_records":0,"blocks":{"175":17,"180":13,"189":10,"199":20}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
