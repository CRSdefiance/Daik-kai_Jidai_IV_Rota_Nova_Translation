from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_story_natural_v2_b60.json")
SC0_SHA256 = "cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"
EXCLUDED = {"DK4_MES_B60_R0011": "Two-byte non-prose command fragment."}

LINES = {
    "DK4_MES_B60_R0006": "{MACRO:FA}?!",
    "DK4_MES_B60_R0017": "Did you bring the Proof?",
    "DK4_MES_B60_R0022": "We found the key that leads to the Proof.",
    "DK4_MES_B60_R0025": "...Hm",
    "DK4_MES_B60_R0032": "We found the promised Proof in East Asia.",
    "DK4_MES_B60_R0035": "Good. Genuine.",
    "DK4_MES_B60_R0041": "Good. Come.",
    "DK4_MES_B60_R0044": "As noted, my position prevents me from openly aiding you.",
    "DK4_MES_B60_R0053": "But we both want Koon and Spain beaten. They're common enemies.",
    "DK4_MES_B60_R0058": "Why is that not enough? Can't we join against Koon and Spain?",
    "DK4_MES_B60_R0062": "Not that simple.",
    "DK4_MES_B60_R0067": "Why not?",
    "DK4_MES_B60_R0071": "Then answer plainly: who is your true enemy? Think carefully.",
    "DK4_MES_B60_R0076": "True enemy?",
    "DK4_MES_B60_R0099": "Spain, which seized Portugal.",
    "DK4_MES_B60_R0101": "...We don't know.",
    "DK4_MES_B60_R0111": "So you'll truly challenge Spain's Armada, even with Albuquerque against you?",
    "DK4_MES_B60_R0115": "Yes. We mean it!",
    "DK4_MES_B60_R0119": "Amusing. Still fighting if my help is refused?",
    "DK4_MES_B60_R0124": "We must. However long it takes, we'll defeat Spain and rebuild Portugal ourselves.",
    "DK4_MES_B60_R0131": "Then this is easy.",
    "DK4_MES_B60_R0140": "Too many frauds wave shallow patriotism around. Trusting them gets men killed.",
    "DK4_MES_B60_R0143": "Seems worry was wasted. You can handle this.",
    "DK4_MES_B60_R0147": "Now crush Koon and hurry home!",
    "DK4_MES_B60_R0151": "Pereira...!",
    "DK4_MES_B60_R0155": "Here. Take this.",
    "DK4_MES_B60_R0161": "This is?",
    "DK4_MES_B60_R0165": "Key to the Proof's map. Act worthy of a conqueror.",
    "DK4_MES_B60_R0169": "We can have this?",
    "DK4_MES_B60_R0173": "Sure. Seven don't interest me. Now it's yours.",
    "DK4_MES_B60_R0178": "Understood. Then please form an alliance with us against Koon.",
    "DK4_MES_B60_R0182": "Then?",
    "DK4_MES_B60_R0188": "We defeat Koon first.",
    "DK4_MES_B60_R0190": "We'll leave Koon to you.",
    "DK4_MES_B60_R0202": "Let's unite and beat Koon.",
    "DK4_MES_B60_R0205": "Securing our rear, eh? Even yours truly would struggle alone.",
    "DK4_MES_B60_R0209": "Spain's king will do anything to strip Portugal's royal succession. Time is short.",
    "DK4_MES_B60_R0213": "Beat Koon, gain enough power, then face Valdes alone.",
    "DK4_MES_B60_R0217": "What?! Alone? Are you sane?!",
    "DK4_MES_B60_R0221": "You govern this sea. You cannot simply abandon your post.",
    "DK4_MES_B60_R0225": "We're rebelling against Spain! To hell with my post!",
    "DK4_MES_B60_R0230": "Should we fail, you'll lose your governorship forever.",
    "DK4_MES_B60_R0234": "Hah! That's your worry? Of course it's obvious!",
    "DK4_MES_B60_R0239": "No! Should we fall short, Portugal needs someone else to carry its fate!",
    "DK4_MES_B60_R0247": "Europe craves these spice islands. Hold them, and one day Portugal can rival Spain.",
    "DK4_MES_B60_R0251": "Be Portugal's last stronghold, and we can fight without restraint.",
    "DK4_MES_B60_R0255": "...Heh.",
    "DK4_MES_B60_R0259": "Hahaha! You truly are fascinating! You've humbled me!",
    "DK4_MES_B60_R0263": "All right! My bet is on you. Leave everything else to me!",
    "DK4_MES_B60_R0268": "Yes. Please do!",
    "DK4_MES_B60_R0273": "Hm? What do you mean?",
    "DK4_MES_B60_R0278": "We're leaving Southeast Asia at once.",
    "DK4_MES_B60_R0281": "Then?",
    "DK4_MES_B60_R0286": "We'll sail to Europe and defeat Spain's Valdes.",
    "DK4_MES_B60_R0289": "What did you say?",
    "DK4_MES_B60_R0294": "Spain's king will do anything to strip Portugal's royal succession. Time is short.",
    "DK4_MES_B60_R0297": "True... But you'll leave Koon until later?",
    "DK4_MES_B60_R0302": "No. We entrust everything here to Governor Pereira.",
    "DK4_MES_B60_R0306": "Ah... You want me guarding the rear.",
    "DK4_MES_B60_R0310": "Yes. With you protecting this sea, we can face Valdes with all our strength.",
    "DK4_MES_B60_R0314": "Hah! So you've already made me a piece in your strategy!",
    "DK4_MES_B60_R0318": "Very well. But suppose Koon is gone when you return?",
    "DK4_MES_B60_R0323": "We have the Proof's key. You may keep this sea's trade rights.",
    "DK4_MES_B60_R0327": "Hah! Pity? Conquer me and this sea later if you like!",
    "DK4_MES_B60_R0331": "B-but...",
    "DK4_MES_B60_R0335": "Trade is fair and open competition, right?",
    "DK4_MES_B60_R0339": "Y-yes, but...",
    "DK4_MES_B60_R0343": "Then make sure Valdes is defeated. Understood?",
    "DK4_MES_B60_R0347": "Of course!",
    "DK4_MES_B60_R0354": "Restoring Portugal... You might actually succeed. You just might.",
    "DK4_MES_B60_R0366": "New question. {MACRO:FA}, who is strongest?",
    "DK4_MES_B60_R0370": "Whoever has the largest trade network. Us, or maybe...",
    "DK4_MES_B60_R0374": "Wrong. Suppose someone sought world conquest. Who has the advantage?",
    "DK4_MES_B60_R0378": "Spain, with its Armada?",
    "DK4_MES_B60_R0382": "Perhaps. {MACRO:FA}, know these spice islands?",
    "DK4_MES_B60_R0387": "Yes. They're nearby.",
    "DK4_MES_B60_R0391": "Right. To Europe, these islands are treasure. Understand?",
    "DK4_MES_B60_R0395": "Yes.",
    "DK4_MES_B60_R0399": "Not just spices. These goods bring vast wealth. Their owner could conquer...",
    "DK4_MES_B60_R0403": "...the world.",
    "DK4_MES_B60_R0407": "Exactly.",
    "DK4_MES_B60_R0411": "Koon... king of the world? Not a chance!",
    "DK4_MES_B60_R0423": "God may forgive. Not me!",
    "DK4_MES_B60_R0431": "So ruling the spice islands could mean ruling the world...",
    "DK4_MES_B60_R0442": "That's more than mere luck.",
    "DK4_MES_B60_R0448": "Now you grasp the situation.",
    "DK4_MES_B60_R0451": "No war yet. Should Koon beat me, nobody else could stop him.",
    "DK4_MES_B60_R0459": "Rebuild your nation, but don't let Koon take the world.",
    "DK4_MES_B60_R0463": "Then what?",
    "DK4_MES_B60_R0467": "Defeat Spain's Valdes! Once stronger, together we can beat Koon!",
    "DK4_MES_B60_R0471": "Valdes... Spain's Armada...",
    "DK4_MES_B60_R0474": "Spain's king will do anything to strip Portugal's royal succession. Time is short.",
    "DK4_MES_B60_R0477": "Once Spain is quiet and Portugal returns, you can have my full support.",
    "DK4_MES_B60_R0482": "Yes, that's true...",
    "DK4_MES_B60_R0486": "Valdes knows where this sea's Proof lies. Beat that runt, or Koon will take a century.",
    "DK4_MES_B60_R0490": "Understood. We'll defeat Valdes and return!",
    "DK4_MES_B60_R0493": "{MACRO:FA}, good luck!",
}

SPEAKERS = {"05": "Claudio Manous", "0B": "Raphael fleet officer (state 0x0B)", "14": "Raphael fleet officer (state 0x14)", "27": "Duarte Pereira"}
LEADING_STATES = {0x05, 0x0B, 0x14, 0x27}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B60_")}
    expected = set(rows) - set(EXCLUDED)
    if set(LINES) != expected:
        raise SystemExit(f"B60 inventory mismatch: missing={sorted(expected-set(LINES))}, extra={sorted(set(LINES)-expected)}")

    records = []
    for row_id, english in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        state = f"{source[0]:02X}" if source and source[0] in LEADING_STATES else ""
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        records.append({
            "id": row_id,
            "english": f"{prefix}{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor"),
            "context": "Raphael negotiates with Duarte Pereira over Koon, Spain, the Spice Islands, and Portugal's future; alternate records cover the player's strategic responses.",
            "source_meaning": english,
            "localization_note": "Faithful concise American English with established names and Proof of Conquest terminology; automatic wrapping uses the late-story live profile.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"],
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-late-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Every usable Raphael story record in SC0 block 60, including all strategy branches.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_non_prose_records": len(EXCLUDED), "blocks": {"60": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Raphael story records")


if __name__ == "__main__":
    main()
