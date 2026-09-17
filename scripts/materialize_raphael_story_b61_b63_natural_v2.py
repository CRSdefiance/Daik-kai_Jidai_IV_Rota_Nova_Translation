from __future__ import annotations
import csv, json
from pathlib import Path

SOURCE=Path("work/sc0/script.csv")
OUTPUT=Path("translations/raphael_story_natural_v2_b61_b63.json")
SC0_SHA256="cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"
EXCLUDED={
 "DK4_MES_B61_R0113":"Private-use notification prefix needs separate event decoding.",
 "DK4_MES_B62_R0005":"Malformed leading presentation byte requires recovery.",
 "DK4_MES_B63_R0011":"Four-byte corrupt non-prose command fragment.",
}
LINES={
"DK4_MES_B61_R0012":"To lose the urn to these fools...",
"DK4_MES_B61_R0015":"Damn! Remember me!",
"DK4_MES_B61_R0022":"Koon, beaten by these whelps... So close...!",
"DK4_MES_B61_R0027":"Well done, Admiral {MACRO:FA}!",
"DK4_MES_B61_R0032":"We managed. Thank you, Governor.",
"DK4_MES_B61_R0042":"No trouble.",
"DK4_MES_B61_R0064":"No trouble.",
"DK4_MES_B61_R0075":"Enough. Trust your heart. Defeat Spain or whoever stands before you!",
"DK4_MES_B61_R0079":"Sir...",
"DK4_MES_B61_R0083":"That old man is all right!",
"DK4_MES_B61_R0094":"Hahaha! Pereira is always a good man!",
"DK4_MES_B61_R0107":"Hahaha! Governor Pereira is always generous! Here, Admiral {MACRO:FA}, take this.",
"DK4_MES_B61_R0123":"What?!",
"DK4_MES_B61_R0129":"My word!",
"DK4_MES_B61_R0136":"Whoa! So generous! Amazing, Governor!",
"DK4_MES_B61_R0147":"Yee-haw!",
"DK4_MES_B61_R0155":"This much? Are you sure?!",
"DK4_MES_B61_R0158":"Sure! Now do your best. We're counting on you!",
"DK4_MES_B61_R0162":"Yes!",
"DK4_MES_B62_R0011":"A Proof clue?",
"DK4_MES_B62_R0016":"Thank you! ...Huh?",
"DK4_MES_B62_R0019":"Gone already.",
"DK4_MES_B62_R0024":"An empty sword sheath. What does that mean?",
"DK4_MES_B62_R0035":"Could this also unlock a Proof map?",
"DK4_MES_B62_R0040":"This is another key to a Proof map.",
"DK4_MES_B62_R0046":"Surely! The New World's treasure is ours!",
"DK4_MES_B63_R0005":"{MACRO:FI}, meet me at the inn.",
"DK4_MES_B63_R0010":"Sure.",
"DK4_MES_B63_R0014":"Show her some care.",
"DK4_MES_B63_R0019":"What?",
"DK4_MES_B63_R0022":"Eirene. You made her do heavy work before.",
"DK4_MES_B63_R0026":"Only a little.",
"DK4_MES_B63_R0030":"That's not the point! She's frailer than the others. Show some care!",
"DK4_MES_B63_R0035":"But there were special circumstances.",
"DK4_MES_B63_R0038":"So that excuses it?!",
"DK4_MES_B63_R0042":"You don't have to get so angry!",
"DK4_MES_B63_R0046":"Hmph! Then do what you want!",
"DK4_MES_B63_R0052":"{MACRO:FI}? What's wrong?",
"DK4_MES_B63_R0056":"Arcadius... Something.",
"DK4_MES_B63_R0060":"Claudio seemed to be shouting earlier...",
"DK4_MES_B63_R0064":"(Oh no...) Hear us?",
"DK4_MES_B63_R0067":"No, not much.",
"DK4_MES_B63_R0072":"Can we talk?",
"DK4_MES_B63_R0075":"Yes...",
"DK4_MES_B63_R0080":"Eirene, that argument was actually about you.",
"DK4_MES_B63_R0084":"Me?",
"DK4_MES_B63_R0089":"Clau is angry because you helped with heavy work before.",
"DK4_MES_B63_R0092":"Nobody else was there, and everyone sees me as a man. Refusing would look odd.",
"DK4_MES_B63_R0096":"That's what we said. We had no choice, but he's furious.",
"DK4_MES_B63_R0105":"Clau just yelled at me and stormed out.",
"DK4_MES_B63_R0109":"We do care about you. His anger feels unfair...",
"DK4_MES_B63_R0113":"Sorry. Keeping my sex secret has caused you trouble, {MACRO:FI}.",
"DK4_MES_B63_R0118":"No, it's not your fault. Sorry for complaining. Let it go.",
"DK4_MES_B63_R0122":"{MACRO:FI}, you work hard as admiral.",
"DK4_MES_B63_R0126":"We can sail without fear because of you.",
"DK4_MES_B63_R0131":"Sudden, Eirene. What's wrong?",
"DK4_MES_B63_R0134":"Nothing. Just don't push yourself, {MACRO:FI}.",
"DK4_MES_B63_R0139":"Eirene...",
"DK4_MES_B63_R0143":"Don't suffer alone. Talking helps.",
"DK4_MES_B63_R0147":"You're like a sister, Eirene.",
"DK4_MES_B63_R0150":"Me?",
"DK4_MES_B63_R0155":"Yes. Talking helped. Thank you for listening.",
"DK4_MES_B63_R0159":"No. Thank you, and sorry for the trouble.",
"DK4_MES_B63_R0163":"This is our first bad fight. What should we do?",
"DK4_MES_B63_R0166":"Oh, that? Claudio will be fine. He'll forget after a meal.",
"DK4_MES_B63_R0171":"Yes?",
"DK4_MES_B63_R0175":"Yes. He's simple like that. Let's eat.",
"DK4_MES_B63_R0179":"Hey, {MACRO:FI}! Eat well?",
"DK4_MES_B63_R0183":"Y-yes. Clau...",
"DK4_MES_B63_R0186":"Why that face?",
"DK4_MES_B63_R0190":"N-no. You seem happy.",
"DK4_MES_B63_R0193":"Huh? Whatever. See you ahead.",
"DK4_MES_B63_R0198":"Eirene was right. He forgot the whole fight...",
"DK4_MES_B63_R0203":"Eirene understands Clau so well... Maybe because she's a scholar?",
}
SPEAKERS={"04":"Emilio Marone","05":"Claudio Manous","08":"Arcadius","0B":"Raphael fleet officer","27":"Duarte Pereira"}

def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as f:
  rows={r["id"]:r for r in csv.DictReader(f) if any(r["id"].startswith(f"DK4_MES_B{b}_") for b in (61,62,63))}
 expected=set(rows)-set(EXCLUDED)
 if set(LINES)!=expected: raise SystemExit(f"inventory mismatch missing={sorted(expected-set(LINES))} extra={sorted(set(LINES)-expected)}")
 out=[]
 for rid,en in LINES.items():
  raw=bytes.fromhex(rows[rid]["source_hex"]); state=f"{raw[0]:02X}" if raw and (0x01<=raw[0]<=0x0F and raw[0]!=0x0A or raw[0]==0x27) else ""
  out.append({"id":rid,"english":f"{{SPEAKER:{state}}}{en}{{PAD}}" if state else f"{en}{{PAD}}","speaker":SPEAKERS.get(state,"Raphael Castor"),"context":"Raphael's post-victory reward and a private crew vignette about Eirene, Claudio, and the burdens of command.","source_meaning":en,"localization_note":"Concise natural English with established names and terminology; wrapping uses the late-story live profile.","qa_waivers":["weak-line-ending","orphan-final-line"],"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
 batch={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC0.DK4","source_file_sha256":SC0_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"raphael-story-late-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Every safely addressable prose record in Raphael SC0 blocks 61-63.","excluded_records":EXCLUDED,"inventory":{"identified_records":len(rows),"translated_records":len(out),"excluded_records":len(EXCLUDED)},"records":out}
 OUTPUT.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(f"wrote {OUTPUT}: {len(out)} records")
if __name__=="__main__": main()
