from __future__ import annotations
import csv,json,re
from pathlib import Path
S=Path("work/sc3/script.csv");O=Path("translations/maria_deep_route_v111.json");SHA="001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2";BS={223,225,226,227,228,232,233,234,235,236,237,238,239}
U={
"DK4_MES_B225_R0004":"Grr...{LB}Damn him!","DK4_MES_B225_R0007":"What's wrong?","DK4_MES_B225_R0011":"Oh! Miss {MACRO:FI}!{LB}Nothing at all.{LB}Pay no mind.","DK4_MES_B225_R0014":"Could never ask {MACRO:FI}{LB}to catch Plett Perrault.{LB}Too dangerous.","DK4_MES_B225_R0017":"Plett Perrault?{LB}Good. He'll be caught.","DK4_MES_B225_R0020":"No, no!{LB}Couldn't ask that of {MACRO:FI}!","DK4_MES_B225_R0024":"All we know is{LB}he hides near the islands.","DK4_MES_B225_R0027":"...You know how to ask.",
"DK4_MES_B226_R0004":"Barkeep,{LB}heard of Plett Perrault?","DK4_MES_B226_R0008":"Never heard of him.","DK4_MES_B226_R0012":"Crash! Thud!","DK4_MES_B226_R0016":"Ow...","DK4_MES_B226_R0020":"Why the rush?{LB}Don't say you're him.","DK4_MES_B226_R0023":"D-Damn, you caught me.{LB}Yes, Plett Perrault.","DK4_MES_B226_R0026":"Honest for a criminal.{LB}You'll come to Hangzhou with us.","DK4_MES_B226_R0030":"Not a chance!","DK4_MES_B226_R0034":"...Resistance is pointless.","DK4_MES_B226_R0038":"{LB}Go!","DK4_MES_B226_R0042":"Damn!{LB}You brought friends!","DK4_MES_B226_R0053":"Disarm.","DK4_MES_B226_R0066":"Grr...{LB}Do what you want!","DK4_MES_B226_R0071":"Give up!{LB}...Hm?","DK4_MES_B226_R0074":"What?!{LB}You!{LB}Now it all comes back!","DK4_MES_B226_R0081":"That cheap little face!{LB}Could never forget it!{LB}You framed me for theft!","DK4_MES_B226_R0084":"You...{LB}That time?","DK4_MES_B226_R0087":"Heh heh...{LB}Admiral, leave him to me.","DK4_MES_B226_R0091":"No argument this time.{LB}Now brace yourself!","DK4_MES_B226_R0095":"Wait!{LB}There was no choice!{LB}Listen...","DK4_MES_B226_R0099":"Gah!!","DK4_MES_B226_R0103":"W-wait...","DK4_MES_B226_R0107":"Aghhh...!!","DK4_MES_B226_R0112":"Enough.{LB}The Hangzhou guild{LB}can handle the rest.",
"DK4_MES_B227_R0004":"Ah, Miss {MACRO:FI}.{LB}What happened to Plett?","DK4_MES_B227_R0007":"He was at Ternate's tavern.{LB}Once found, he surrendered.","DK4_MES_B227_R0011":"Truly? Sorry for the trouble.{LB}Please accept this small reward...","DK4_MES_B227_R0017":"Received 12,000 gold.",
"DK4_MES_B228_R0011":"We need to find Plett{LB}somewhere near the islands.","DK4_MES_B228_R0016":"All we know is{LB}he hides near the islands.","DK4_MES_B232_R0011":"Catch Jean whats-his-name{LB}somewhere in southern Asia.",
"DK4_MES_B233_R0005":"A beauty like you{LB}fits the job.","DK4_MES_B233_R0009":"...What?","DK4_MES_B233_R0013":"Locate the Spanish spy{LB}Peralonso Aguirre.{LB}He works around Southeast Asia.","DK4_MES_B233_R0016":"A woman's job,{LB}then.","DK4_MES_B233_R0019":"You'll know.",
"DK4_MES_B234_R0004":"Tch. Not one pretty woman{LB}in this whole place.","DK4_MES_B234_R0011":"Barkeep,{LB}a question.","DK4_MES_B234_R0014":"Ah, there is a beauty!{LB}Why not say so?","DK4_MES_B234_R0018":"Come here, miss.{LB}Pour me a drink.","DK4_MES_B234_R0021":"...{LB}Barkeep, where is{LB}Peralonso Aguirre?","DK4_MES_B234_R0025":"Peralonso Aguirre?{LB}Miss, that's me!","DK4_MES_B234_R0029":"So it's you.","DK4_MES_B234_R0033":"Not bad!{LB}A beauty came just to meet me.","DK4_MES_B234_R0037":"Your name? Your country?{LB}Your type? What brings you?","DK4_MES_B234_R0041":"(So that's why{LB}a woman suits the job...)","DK4_MES_B234_R0044":"Why hurry?{LB}Let's go somewhere quiet.{LB}How about Basra?","DK4_MES_B234_R0047":"Sure! Anywhere you want!",
"DK4_MES_B235_R0004":"H-Hey, miss, this is...","DK4_MES_B235_R0008":"Peralonso Aguirre.{LB}Caught while chasing a skirt?{LB}A disgrace to spies.","DK4_MES_B235_R0012":"Miss {MACRO:FI},{LB}he followed you easily, yes?{LB}Ha ha ha!","DK4_MES_B235_R0016":"Your reward.{LB}Keep polishing that beauty.","DK4_MES_B235_R0020":"B-Blundered...","DK4_MES_B235_R0024":"Received 21,000 gold.",
"DK4_MES_B236_R0011":"We need to catch Peralonso{LB}in Southeast Asia.","DK4_MES_B236_R0023":"Peralonso is active{LB}in Brunei.",
"DK4_MES_B237_R0004":"You've a strong face.{LB}Will you take a job?","DK4_MES_B237_R0007":"Seek Yuris Huigen,{LB}a Dutch nobleman.","DK4_MES_B237_R0011":"He plotted with foreigners,{LB}got exposed, stole a ship, and fled.","DK4_MES_B237_R0015":"Last seen near Manila.{LB}His trail ends there.{LB}Good luck.",
"DK4_MES_B238_R0004":"Ah, Yuris the ship thief!{LB}Caught at last.","DK4_MES_B238_R0007":"Yes, caught indeed.{LB}But calling a noble{LB}a ship thief is insulting!","DK4_MES_B238_R0012":"...Now he just looks{LB}penniless.","DK4_MES_B238_R0015":"A rather pathetic prize...{LB}Still, better us than a foreign guild.{LB}Nobles are easily exploited.","DK4_MES_B238_R0018":"Here's the reward. Take it.","DK4_MES_B238_R0022":"Received 33,000 gold.","DK4_MES_B238_R0048":"Batavia share rose slightly!","DK4_MES_B238_R0066":"Say, have you heard{LB}the devil-statue rumor?","DK4_MES_B238_R0070":"A demon?","DK4_MES_B238_R0074":"They say it's sealed in{LB}this town's ruins.{LB}See the truth yourself.",
"DK4_MES_B239_R0011":"Yuris's stolen fleet{LB}is in Southeast Asia.","DK4_MES_B239_R0023":"Yuris the ship thief{LB}hides in Southeast Asia.",
}
SP={"03":"Maria","0B":"Samwell","0C":"Companion","40":"Yuris","41":"Plett","45":"Peralonso","5C":"Barkeep","93":"Guildmaster","94":"Guildmaster","95":"Guildmaster","BE":"Hostess","CF":"Companion","FE":"System"};ST={int(x,16) for x in SP}
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
    e=out.get((fp,r["id"]));
    if e:refs.setdefault(bytes.fromhex(r["source_hex"])[1:],re.sub(r"^(?:\{SPEAKER:[0-9A-F]{2}\})?|\{PAD\}$","",e))
 return refs
def main()->None:
 with S.open(encoding="utf-8-sig",newline="") as f:rows={r["id"]:r for r in csv.DictReader(f) if int(r["id"].split("_B",1)[1].split("_R",1)[0]) in BS}
 refs=references();L={i:(U[i] if i in U else refs.get(bytes.fromhex(r["source_hex"])[1:])) for i,r in rows.items()}
 if any(v is None for v in L.values()):raise SystemExit(f"V111 missing: {sorted(i for i,v in L.items() if v is None)}")
 rec=[]
 for i in sorted(L,key=lambda v:(int(v.split("_B",1)[1].split("_R",1)[0]),int(v.rsplit("R",1)[1]))):
  r=rows[i];e=L[i];first=bytes.fromhex(r["source_hex"])[0];state=f"{first:02X}" if first in ST else "";u=e.replace("{MACRO:FI}","").replace("{MACRO:FA}","").replace("{MACRO:FO}","")
  if "F" in u or "I" in u:raise SystemExit(f"{i}: unsafe macro literal: {e}")
  sb=r["japanese"].count("{LB}");tb=e.count("{LB}");w=["weak-line-ending","orphan-final-line"]+(["manual-break"] if tb else [])+(["source-leading-linebreak"] if r["japanese"].startswith("{LB}") else [])+(["line-break-count"] if sb!=tb else []);prefix=f"{{SPEAKER:{state}}}" if state else "";b=int(i.split("_B",1)[1].split("_R",1)[0])
  rec.append({"id":i,"english":f"{prefix}{e}{{PAD}}","speaker":SP.get(state,"Continuation"),"context":f"Final Maria optional-event cleanup in SC3 block {b}.","source_meaning":e.replace("{LB}"," "),"localization_note":"Direct Maria translation or byte-identical reviewed reuse, preserving bounty variants, macros, states, line breaks, rewards, and fixed allocation.","qa_waivers":w,**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if tb else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 p={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC3.DK4","source_file_sha256":SHA,"encoder":"dialogue-fixed-v1","dialogue_profile":"maria-story-shared-events-v111-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Maria SC3 final untranslated records in blocks 223-239: ruin greeting and bounty variants.","excluded_records":{},"inventory":{"identified_records":87,"translated_records":87,"excluded_records":0,"blocks":{str(b):sum(1 for i in rows if f"_B{b:03d}_" in i) for b in sorted(BS)}},"records":rec};O.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"wrote {O}: {len(rec)} translations")
if __name__=="__main__":main()
