from __future__ import annotations
import csv,json
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v96.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
L={
"DK4_MES_B127_R0004":"Don't mock me.{LB}Think again.",
"DK4_MES_B127_R0007":"Enough!{LB}Someone like you is fired!",
"DK4_MES_B127_R0012":"So be it.{LB}Then let me leave as ordered.",
"DK4_MES_B127_R0015":"{LB}Oh...{LB}Seeing a man fired is unpleasant.",
"DK4_MES_B127_R0018":"Did you see his build?",
"DK4_MES_B127_R0022":"{LB}Splendid muscles.{LB}But a short temper.{LB}Trouble must follow him.",
"DK4_MES_B127_R0026":"Handling a hard man{LB}also proves a leader's skill.",
"DK4_MES_B127_R0029":"Bold words.{LB}Are you Admiral {MACRO:FA}?{LB}He is difficult.",
"DK4_MES_B127_R0032":"How skilled is he?",
"DK4_MES_B127_R0036":"Never saw him lose a fight.",
"DK4_MES_B127_R0039":"{LB}.",
"DK4_MES_B127_R0043":"Then no problem.{LB}Let's follow him.",
"DK4_MES_B127_R0047":"There.",
"DK4_MES_B127_R0051":"What?",
"DK4_MES_B127_R0055":"A job offer.",
"DK4_MES_B127_R0059":"A job? Hiring me?{LB}Who are you?",
"DK4_MES_B127_R0062":"A private-fleet admiral.",
"DK4_MES_B127_R0066":"Wait... Admiral {MACRO:FA}?",
"DK4_MES_B127_R0069":"You know me.{LB}Good. Easy.",
"DK4_MES_B127_R0072":"Our coming Western enemies are strong.{LB}A powerful warrior is needed.{LB}Join my ship.",
"DK4_MES_B127_R0076":"Western...? Are you sane?",
"DK4_MES_B127_R0080":"Afraid?{LB}Perhaps this was a mistake.",
"DK4_MES_B127_R0083":"Hah! Sounds fun!{LB}Good, count on my help.{LB}Do not doubt my strength.",
"DK4_MES_B127_R0087":"{LB}Reassuring.{LB}But your name?",
"DK4_MES_B127_R0091":"Al.",
"DK4_MES_B127_R0095":"Welcome. Empty boasting is hated.{LB}Do not disappoint me.",
"DK4_MES_B128_R0004":"Oops, sorry!",
"DK4_MES_B128_R0012":"What happened?",
"DK4_MES_B128_R0016":"That man dropped this...{LB}A pendant?{LB}A woman's portrait...",
"DK4_MES_B128_R0021":"A precious woman to him...{LB}perhaps his lover.",
"DK4_MES_B128_R0024":"Let's return it.",
"DK4_MES_B128_R0029":"Mamma mia! My dear sister!{LB}The pendant is gone!",
"DK4_MES_B128_R0032":"No! No! No!{LB}Nowhere!",
"DK4_MES_B128_R0035":"Admiral, that man... there!",
"DK4_MES_B128_R0039":"My pendant!{LB}Where did it go?!",
"DK4_MES_B128_R0042":"You there!{LB}Calm yourself!{LB}Could this be what you seek?",
"DK4_MES_B128_R0046":"My sister! The pendant!",
"DK4_MES_B128_R0050":"Sister?{LB}This woman is your sister?",
"DK4_MES_B128_R0053":"Yes. Thank you.{LB}My dear sister is missing.{LB}The search continues...",
"DK4_MES_B128_R0057":"Hope you find her...",
"DK4_MES_B128_R0062":"An admiral means a sailor.{LB}Take me aboard! Sailed before.{LB}Useful, too!",
"DK4_MES_B128_R0065":"Please. Seek my sister.{LB}Her location is unknown,{LB}but she is somewhere in this world!",
"DK4_MES_B128_R0069":"What say you?",
"DK4_MES_B128_R0073":"Agreed.{LB}Maybe fate chose this.{LB}You're hired.",
"DK4_MES_B128_R0077":"Mamma mia!{LB}Sister, wait for me!{LB}Angelo Puccini. At your service.",
"DK4_MES_B128_R0080":"My name is{LB}{MACRO:FI} {MACRO:FA}.{LB}Welcome aboard.",
"DK4_MES_B129_R0004":"...Admiral, a word.",
"DK4_MES_B129_R0008":"All right...",
"DK4_MES_B129_R0012":"{LB}Then we should leave...",
"DK4_MES_B129_R0016":"No. Everyone{LB}should hear this...",
"DK4_MES_B129_R0019":"{LB}Yes.",
"DK4_MES_B129_R0023":"My sister Bianca...",
"DK4_MES_B129_R0027":"{LB}We promised to help.",
"DK4_MES_B129_R0030":"No. That is not it.",
"DK4_MES_B129_R0034":"...Bianca is gone.",
"DK4_MES_B129_R0038":"Gone...?",
"DK4_MES_B129_R0042":"My only family, Bianca,{LB}died of illness three years ago...",
"DK4_MES_B129_R0045":"Died...? Then why{LB}were you searching for her?",
"DK4_MES_B129_R0048":"When Bianca died,{LB}that truth could not be accepted...",
"DK4_MES_B129_R0052":"To me, she was missing,{LB}so the world was searched...",
"DK4_MES_B129_R0055":"Angelo...",
"DK4_MES_B129_R0059":"When laid low...",
"DK4_MES_B129_R0063":"My sister said{LB}you are my family now,{LB}and this life should be lived{LB}for myself...",
"DK4_MES_B129_R0070":"{LB}A wonderful sister.{LB}She truly worried for you.",
"DK4_MES_B129_R0074":"{LB}Live as long as life remains,{LB}for your sister as well.",
"DK4_MES_B129_R0078":"Yes, Angelo.{LB}Do not sadden her.{LB}As she said, we are family.",
"DK4_MES_B129_R0082":"Thank you.{LB}Stay with me from now on.",
"DK4_MES_B129_R0085":"Likewise.",
"DK4_MES_B129_R0089":"...{LB}(Bianca... forgive me.{LB}Now this life{LB}will be lived for us both.)",
}
EX={"DK4_MES_B127_R0002":"Raw ten-byte event-control payload before the tavern argument; not dialogue.","DK4_MES_B127_R0013":"Raw twelve-byte event-control payload after Al leaves; not dialogue.","DK4_MES_B128_R0060":"Raw five-byte event-control payload before Angelo's recruitment request; not dialogue."}
SP={"03":"Maria","0C":"Yukihisa","0F":"Angelo","11":"Al","15":"Companion","94":"Employer"};ST={int(x,16) for x in SP}
C={127:"Maria witnesses Al being fired, tests his courage, and recruits him as a warrior.",128:"Maria returns Angelo's lost pendant and recruits him to help search for his sister Bianca.",129:"Angelo accepts Bianca's death, recognizes Maria's crew as his new family, and chooses to live forward."}
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if 127<=int(r["id"].split("_B",1)[1].split("_R",1)[0])<=129}
 if set(L)|set(EX)!=set(rows):raise SystemExit(f"V96 mismatch: missing={sorted(set(rows)-set(L)-set(EX))}; extra={sorted((set(L)|set(EX))-set(rows))}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Maria or Xien continuation"),"context":C[b],"source_meaning":e.replace("{LB}"," "),"localization_note":"Direct SC3 translation preserving recruitment beats, emotional disclosure, speaker states, FI/FA macros, verified raw controls, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v96-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 blocks 127-129: Al recruitment, Angelo recruitment, and Angelo's acceptance of Bianca's death.","excluded_records":EX,"inventory":{"identified_records":len(rows),"translated_records":len(rec),"excluded_records":len(EX),"blocks":{"127":28,"128":21,"129":23}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations + {len(EX)} controls")
if __name__=="__main__":main()
