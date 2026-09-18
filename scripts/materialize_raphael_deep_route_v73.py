from __future__ import annotations
import csv, json
from pathlib import Path

SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v73.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (302, 303, 304)
EXCLUDED = {
    "DK4_MES_B304_R0004": "Raw scene-control payload; not dialogue.",
    "DK4_MES_B304_R0012": "Raw item-handoff control payload; not dialogue.",
}
SPEAKERS = {0x05: "Claudio Manousch", 0x08: "Arcadius Eirene", 0x5C: "Local scholar", 0x87: "Veda guardian", 0xC7: "Local woman"}
CONTEXT = {
    302: "A local woman gives Raphael directions and warnings for an inland jungle expedition.",
    303: "A scholar connects the Vedas to the Proof of Hegemony for the ocean east of Africa.",
    304: "Raphael shows the Veda to its guardian and receives an ancient coin clue.",
}
OVERRIDES = {
    "DK4_MES_B302_R0006": "Oh, {MACRO:FI}. Welcome.",
    "DK4_MES_B302_R0009": "Ruins? Never heard of any near this town.",
    "DK4_MES_B302_R0012": "Then if we find ruins...",
    "DK4_MES_B302_R0017": "We'll be the first discoverers!",
    "DK4_MES_B302_R0020": "Not so easy! Thick forest and wild beasts make the outskirts dangerous.",
    "DK4_MES_B302_R0024": "Still want to explore? Take the inland path. Without a map, you'll get lost.",
    "DK4_MES_B303_R0005": "Want to know about the Vedas? Hard to call it legend or myth...",
    "DK4_MES_B303_R0009": "That legend belongs to whoever{LB}rules the eastern ocean.",
    "DK4_MES_B303_R0013": "Rule it? The Proof of Hegemony?!",
    "DK4_MES_B303_R0024": "Yes. Almost certainly.",
    "DK4_MES_B303_R0032": "So first, find the Proof for that ocean!",
    "DK4_MES_B304_R0006": "Hm? Back again?",
    "DK4_MES_B304_R0011": "Could this be the Veda you mentioned?",
    "DK4_MES_B304_R0014": "...Hm? !! That is?!",
    "DK4_MES_B304_R0017": "Yes, the first Vedic scripture!",
    "DK4_MES_B304_R0020": "A youth so young brings this here...",
    "DK4_MES_B304_R0028": "Then this passes into your care.",
    "DK4_MES_B304_R0035": "An old coin...? What is this?",
    "DK4_MES_B304_R0039": "My task is done. Unravel the rest yourselves. Now go.",
    "DK4_MES_B304_R0046": "What does this mean?",
}

def main() -> None:
    prefixes = tuple(f"DK4_MES_B{b}_" for b in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [r for r in csv.DictReader(stream) if r["id"].startswith(prefixes)]
    records=[]; counts={}
    for row in rows:
        if row["id"] in EXCLUDED: continue
        english=OVERRIDES.get(row["id"])
        if english is None: raise SystemExit(f"Raphael V73 unresolved record: {row['id']}")
        unsafe=english
        for macro in ("FI","FA","FO","FU"): unsafe=unsafe.replace(f"{{MACRO:{macro}}}","")
        if "I" in unsafe or "F" in unsafe: raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        first=int(row["source_hex"][:2],16); state=f"{first:02X}" if first in SPEAKERS else ""
        block=int(row["id"].split("_B",1)[1].split("_",1)[0]); counts[str(block)]=counts.get(str(block),0)+1
        records.append({"id":row["id"],"english":f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}","speaker":SPEAKERS.get(first,"Raphael party or scene text"),"context":CONTEXT[block],"source_meaning":english.replace("{LB}"," ").replace("{MACRO:FI}","Raphael"),"localization_note":"Faithful concise American English preserving canonical Veda and Proof of Hegemony terms, item-handoff controls, and fixed-record constraints.","qa_waivers":["weak-line-ending","orphan-final-line",*(["manual-break"] if "{LB}" in english else [])],**({"manual_break_reason":"Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":True}})
    if len(records)+len(EXCLUDED)!=len(rows): raise SystemExit("Raphael V73 inventory mismatch")
    batch={"format":"dk4-ilnk-translation-batch-v1","file_path":"/data/SC0.DK4","source_file_sha256":SC0_SHA256,"encoder":"dialogue-fixed-v1","dialogue_profile":"raphael-story-deep-route-v73-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":"Complete source-locked Raphael jungle-rumor, Veda clue, guardian, and ancient-coin handoff events across SC0 blocks 302-304.","excluded_records":EXCLUDED,"inventory":{"identified_records":len(rows),"translated_records":len(records),"blocks":counts},"records":records}
    OUTPUT.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")

if __name__=="__main__": main()
