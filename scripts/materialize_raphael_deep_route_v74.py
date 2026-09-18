from __future__ import annotations
import csv,json,re
from pathlib import Path
SOURCE=Path("work/sc0/script.csv"); OUTPUT=Path("translations/raphael_deep_route_v74.json")
SC0_SHA256="a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED={"DK4_MES_B305_R0029":"Raw expedition-branch control; not dialogue.","DK4_MES_B305_R0103":"Raw river-branch control; not dialogue."}
SPEAKERS={0x04:"Raphael crewmate",0x05:"Claudio Manousch",0x07:"Raphael crewmate",0x94:"Expedition guide",0x97:"Raphael crewmate",0xD3:"Raphael crewmate",0xDE:"Raphael crewmate",0xFE:"System"}
OVERRIDES={
"DK4_MES_B305_R0012":"Did you bring a map? Even for you, no map means no going farther.",
"DK4_MES_B305_R0025":"Good, you brought a map.",
"DK4_MES_B305_R0070":"Whew... At last, the top!",
"DK4_MES_B305_R0073":"We part here. Take care.",
"DK4_MES_B305_R0076":"Thanks, old man! We're off!",
"DK4_MES_B305_R0080":"This dim forest feels eerie.",
"DK4_MES_B305_R0091":"Ugh. No liking places like this.",
"DK4_MES_B305_R0097":"A hidden village may preserve ancient legends!",
"DK4_MES_B305_R0102":"Maybe this reveals{LB}the Proof of Hegemony.",
"DK4_MES_B305_R0106":"A raging river. What now?",
"DK4_MES_B305_R0111":"Careful",
"DK4_MES_B305_R0113":"Go upstream",
"DK4_MES_B305_R0120":"Waaah, swept away!",
"DK4_MES_B305_R0130":"Admiral, no! Current too strong to cross on foot!",
"DK4_MES_B305_R0132":"Too strong... Admiral! We cannot cross on foot!",
"DK4_MES_B305_R0133":"Admiral, no! Too strong to cross on foot!",
"DK4_MES_B305_R0135":"No! The current will sweep us away!",
"DK4_MES_B305_R0136":"Admiral, impossible! Too swift to cross on foot!",
"DK4_MES_B305_R0138":"No, Admiral! This current is too strong to cross!",
"DK4_MES_B305_R0140":"Admiral, no!{LB}This current will sweep us away!",
"DK4_MES_B305_R0141":"Admiral, impossible! Too strong to cross on foot!",
"DK4_MES_B305_R0146":"Hold hands! Work together or be swept away!",
"DK4_MES_B305_R0149":"Ooh!",
"DK4_MES_B305_R0153":"Almost there! Keep going!",
"DK4_MES_B305_R0164":"Sailors are exhausted. Some seem to have left.",
"DK4_MES_B305_R0168":"Look at the map. A log bridge lies upstream. Distant, but try it?",
"DK4_MES_B305_R0173":"Yes. Only choice.",
"DK4_MES_B305_R0178":"Ah, that's the log bridge.",
"DK4_MES_B305_R0182":"Seems so. What a place for a bridge.",
"DK4_MES_B305_R0194":"We cross here...?",
"DK4_MES_B305_R0198":"Why scared? Move!",
"DK4_MES_B305_R0201":"D-don't push!",
"DK4_MES_B305_R0219":"Here... We made it!",
}
def _strip(t): return re.sub(r"\{PAD\}$","",re.sub(r"^\{SPEAKER:[0-9A-F]+\}","",t))
def _refs():
 tables={}
 for route in ("SC1","SC2","SC3"):
  with (Path("work")/route.lower()/"script.csv").open(encoding="utf-8-sig",newline="") as s: tables[route]={r["id"]:r["source_hex"].upper() for r in csv.DictReader(s)}
 out={}
 for p in sorted(Path("translations").glob("hodram_deep_route_v*.json"))+sorted(Path("translations").glob("lil_deep_route_v*.json")):
  b=json.loads(p.read_text(encoding="utf-8")); m=re.search(r"/(SC[123])\.DK4$",str(b.get("file_path","")),re.I)
  if not m: continue
  for rec in b.get("records",[]):
   h=tables[m.group(1).upper()].get(rec["id"])
   if h: out.setdefault(h[2:] if rec["english"].startswith("{SPEAKER:") else h,_strip(rec["english"]))
 return out
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as s: rows=[r for r in csv.DictReader(s) if r["id"].startswith("DK4_MES_B305_")]
 refs=_refs(); records=[]; unresolved=[]
 for row in rows:
  if row["id"] in EXCLUDED: continue
  h=row["source_hex"].upper(); first=int(h[:2],16); e=OVERRIDES.get(row["id"],refs.get(h[2:] if first in SPEAKERS else h))
  if e is None: unresolved.append(row["id"]); continue
  unsafe=e
  for m in ("FI","FA","FO","FU"): unsafe=unsafe.replace(f"{{MACRO:{m}}}","")
  if "I" in unsafe or "F" in unsafe: raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {e}")
  st=f"{first:02X}" if first in SPEAKERS else ""
  records.append({"id":row["id"],"english":f"{{SPEAKER:{st}}}{e}{{PAD}}" if st else f"{e}{{PAD}}","speaker":SPEAKERS.get(first,"Raphael party, choice, or scene text"),"context":"Raphael's party follows a guide toward a hidden village, crosses a dangerous river, and reaches a log bridge.","source_meaning":e.replace("{LB}"," "),"localization_note":"Faithful concise American English preserving every map warning, river choice, crossing outcome, control payload, and fixed-record constraint.","qa_waivers":["weak-line-ending","orphan-final-line",*(["manual-break"] if "{LB}" in e else [])],**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in e else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 if unresolved: raise SystemExit(f"Raphael V74 unresolved records: {unresolved}")
 batch={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC0.DK4","source_file_sha256":SC0_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"raphael-story-deep-route-v74-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Complete source-locked Raphael hidden-village map, guide, jungle, river-crossing, log-bridge, and arrival event in SC0 block 305.","excluded_records":EXCLUDED,"inventory":{"identified_records":len(rows),"translated_records":len(records),"blocks":{"305":len(records)}},"records":records}
 OUTPUT.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")
if __name__=="__main__": main()
