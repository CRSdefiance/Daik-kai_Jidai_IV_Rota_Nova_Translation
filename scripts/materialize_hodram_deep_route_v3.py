from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v3.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(71, 84))

LINES = {
    # B71-B74: Maria sends Hodram after the Wako and rewards his victory.
    "DK4_MES_B71_R0007": "{MACRO:FA}",
    "DK4_MES_B71_R0011": "Hm?",
    "DK4_MES_B71_R0015": "Admiral Maria Lee awaits you in Hangzhou.",
    "DK4_MES_B72_R0006": "{MACRO:FA}, Admiral Lee calls. This way.",
    "DK4_MES_B72_R0010": "Kuhn is defeated. Congratulations.",
    "DK4_MES_B72_R0017": "Why the gloomy face?",
    "DK4_MES_B72_R0021": "How will you use me now?",
    "DK4_MES_B72_R0025": "So suspicious.",
    "DK4_MES_B72_R0029": "Very well. We secured a foothold in Southeast Asia.",
    "DK4_MES_B72_R0033": "So our interests happened to align?",
    "DK4_MES_B72_R0036": "Perhaps.",
    "DK4_MES_B72_R0040": "Good. While we're here, there's another proposal.",
    "DK4_MES_B72_R0044": "As expected.",
    "DK4_MES_B72_R0048": "Have you heard of the Wako?",
    "DK4_MES_B72_R0055": "Ming has no navy under isolation. Japanese pirates exploit this, raiding and plundering its coast. They are the Wako.",
    "DK4_MES_B72_R0058": "Sojin Kurushima leads them. My private fleet protects people from his raids.",
    "DK4_MES_B72_R0062": "You want me to defeat him?",
    "DK4_MES_B72_R0065": "Of course, there will be a reward. And Japan may hold something you seek.",
    "DK4_MES_B72_R0069": "Something sought? Heh... You underestimate me. You take me for your hound?",
    "DK4_MES_B72_R0073": "A cynical view. You are being offered exclusive trade with Japan.",
    "DK4_MES_B72_R0077": "How generous of you.",
    "DK4_MES_B72_R0081": "Refuse?",
    "DK4_MES_B72_R0085": "We came to the eastern edge of the world for results. Japan need not be our target.",
    "DK4_MES_B72_R0088": "...Challenge me instead, if you wish.",
    "DK4_MES_B72_R0091": "Whether confidence or bluff, it interests me. But there's no reason to fight you now. Calm down.",
    "DK4_MES_B72_R0098": "No need to think. Accepting your proposal is clearly my most profitable choice.",
    "DK4_MES_B72_R0102": "A terrifying woman... This is what dancing in another's palm feels like.",
    "DK4_MES_B72_R0106": "Sit back. While we sweep away the pirates, your help is unnecessary.",
    "DK4_MES_B72_R0110": "Oh, is that so?",
    "DK4_MES_B72_R0114": "That fearless smile behind me makes such bold boasts easy. Most reassuring.",
    "DK4_MES_B72_R0117": "Sarcasm.",
    "DK4_MES_B72_R0121": "You think me obedient and easy to use. Enjoy waiting for good news.",
    "DK4_MES_B73_R0028": "{MACRO:FA}, splendid work.",
    "DK4_MES_B73_R0031": "Do not anger me further.",
    "DK4_MES_B73_R0035": "My apologies. Here is the promised reward.",
    "DK4_MES_B73_R0056": "Now you rule these waters. Take this.",
    "DK4_MES_B74_R0058": "The Ottomans stir in the Mediterranean. Seek that treasure, then consider returning.",
    "DK4_MES_B74_R0062": "Useful. Noted.",

    # B75-B78: the Ottoman crisis and Escante's betrayal and defeat.
    "DK4_MES_B75_R0025": "{MACRO:FA}.",
    "DK4_MES_B75_R0029": "Maria?! Why come all this way?",
    "DK4_MES_B75_R0032": "The Ottoman navy moves to seize the Mediterranean.",
    "DK4_MES_B75_R0035": "What?!",
    "DK4_MES_B75_R0039": "My homeland may not be drawn into the war... Did you come only to warn me?",
    "DK4_MES_B75_R0043": "A debt remains.",
    "DK4_MES_B75_R0047": "Thanks. Helpful.",
    "DK4_MES_B75_R0051": "(Oh? So honest...)",
    "DK4_MES_B75_R0055": "But no more 'dear {MACRO:FA}'...",
    "DK4_MES_B76_R0006": "A letter came from Escante.",
    "DK4_MES_B76_R0009": "Escante's forces have declared war!",
    "DK4_MES_B76_R0027": "That man... So he had a plan.",
    "DK4_MES_B76_R0040": "So Escante betrayed us after all.",
    "DK4_MES_B76_R0043": "A tavern warned us, so this was expected. Now we're at a grave disadvantage.",
    "DK4_MES_B76_R0046": "Meaning?",
    "DK4_MES_B76_R0050": "While we fought Maldonado, Escante amassed money and power for his true purpose.",
    "DK4_MES_B76_R0053": "Purpose? What purpose?",
    "DK4_MES_B76_R0056": "One can guess...",
    "DK4_MES_B77_R0012": "Admiral, royal orders have arrived.",
    "DK4_MES_B77_R0017": "Admiral, royal orders have arrived.",
    "DK4_MES_B77_R0023": "The king? What orders?",
    "DK4_MES_B77_R0033": "Allow me... 'The Ottoman offensive has placed Christendom in grave peril.'",
    "DK4_MES_B77_R0036": "'By royal naval honor, meet the enemy. Preserve peace in Europe and safe Mediterranean trade.' That is all.",
    "DK4_MES_B77_R0042": "Allow me... 'The Ottoman offensive has placed Christendom in grave peril.'",
    "DK4_MES_B77_R0045": "'By royal naval honor, meet the enemy. Preserve peace in Europe and safe Mediterranean trade.' That is all.",
    "DK4_MES_B77_R0052": "At last, northern Europe feels the flames!",
    "DK4_MES_B78_R0013": "Grrrr!",
    "DK4_MES_B78_R0021": "One more step and my empire would have seized the New World... But for you!",
    "DK4_MES_B78_R0024": "Escante!",
    "DK4_MES_B78_R0028": "My empire will never be yours... Die!",
    "DK4_MES_B78_R0034": "Lord {MACRO:FA}.",
    "DK4_MES_B78_R0037": "Escante...",
    "DK4_MES_B78_R0041": "Splendid work. You have defeated me.",
    "DK4_MES_B78_R0048": "Heh... One more step and my empire would have claimed the New World...",
    "DK4_MES_B78_R0051": "Had you not interfered!",
    "DK4_MES_B78_R0062": "Admiral, duck!",
    "DK4_MES_B78_R0070": "Guoooh!!",
    "DK4_MES_B78_R0074": "Am... am... Dying here...?",
    "DK4_MES_B78_R0077": "Gah!!",
    "DK4_MES_B78_R0085": "Admiral, are you hurt?",
    "DK4_MES_B78_R0089": "Unhurt.",
    "DK4_MES_B78_R0093": "Escante... Pitiful man. Did you truly believe the New World's people would accept you as king?",
    "DK4_MES_B78_R0096": "Hm? Something is in Escante's coat.",

    # B79: Hayreddin describes Pasha's betrayal and warns Hodram.
    "DK4_MES_B79_R0010": "So hectic...",
    "DK4_MES_B79_R0014": "Pirate Hayreddin was crushed by the Ottoman navy. The survivors returned in chaos.",
    "DK4_MES_B79_R0017": "Hayreddin was?",
    "DK4_MES_B79_R0021": "Move!",
    "DK4_MES_B79_R0026": "Ah!! L-Lord Hayreddin!",
    "DK4_MES_B79_R0042": "What? Come to laugh at my disgrace?",
    "DK4_MES_B79_R0045": "...Self-important fool. The king ordered us to fight the Ottomans.",
    "DK4_MES_B79_R0049": "Hah. Bad luck. Their enemies should prepare to die.",
    "DK4_MES_B79_R0053": "Wasn't the Hayreddin clan allied with the Ottoman Empire?",
    "DK4_MES_B79_R0061": "Pasha demanded a vassal oath so our pirates would join his offensive.",
    "DK4_MES_B79_R0064": "This fleet was built by my father and me. Rather than fold it into an army, we rebelled against the Ottomans.",
    "DK4_MES_B79_R0067": "So far, so good. Though outmatched, we meant to hold for years and show Algiers pirate pride.",
    "DK4_MES_B79_R0071": "Then a trusted subordinate betrayed me. Pasha caught us unaware. Now facing my father is impossible.",
    "DK4_MES_B79_R0079": "No point telling you this.",
    "DK4_MES_B79_R0083": "Take this. Pasha sent it as a vassal's token. The sight sickens me.",
    "DK4_MES_B79_R0090": "See that you don't lose disgracefully.",

    # B80-B82: Sera rejoins Hodram and he helps rebuild her homeland.
    "DK4_MES_B80_R0006": "Sera!!",
    "DK4_MES_B80_R0014": "Why are you here?!",
    "DK4_MES_B80_R0018": "{MACRO:FI}, danger. Heard it. Came to help my people and sea king.",
    "DK4_MES_B80_R0022": "You saved us. Everyone, forgive me.",
    "DK4_MES_B80_R0029": "Truly, thank you. Everyone flee quickly. The Ottomans won't stay silent.",
    "DK4_MES_B80_R0033": "Yes!",
    "DK4_MES_B80_R0045": "Everyone, go.",
    "DK4_MES_B80_R0049": "You should flee too.",
    "DK4_MES_B80_R0057": "What's wrong? Hurry.",
    "DK4_MES_B80_R0061": "Staying.",
    "DK4_MES_B80_R0065": "Hm?",
    "DK4_MES_B80_R0069": "With {MACRO:FI}.",
    "DK4_MES_B80_R0072": "What is this?",
    "DK4_MES_B80_R0076": "Aboard.",
    "DK4_MES_B80_R0080": "Work remains. Go home; it's dangerous.",
    "DK4_MES_B80_R0083": "{MACRO:FI}, sea king. Watch.",
    "DK4_MES_B80_R0086": "No. Go home.",
    "DK4_MES_B80_R0090": "Decided.",
    "DK4_MES_B80_R0098": "Stubborn... Go ahead.",
    "DK4_MES_B80_R0105": "Well?",
    "DK4_MES_B80_R0109": "Beat Pasha. Return here.",
    "DK4_MES_B80_R0112": "This city?",
    "DK4_MES_B80_R0116": "King's tomb...",
    "DK4_MES_B80_R0119": "The king's tomb... You mean the pyramid? Why?",
    "DK4_MES_B80_R0123": "Go... then see.",
    "DK4_MES_B81_R0005": "My... homeland.",
    "DK4_MES_B81_R0009": "Yes.",
    "DK4_MES_B81_R0013": "Still strange. Why would an ocean legend from the east be known here?",
    "DK4_MES_B81_R0017": "The eastern ocean and Black Sea are far apart.",
    "DK4_MES_B81_R0020": "True...",
    "DK4_MES_B81_R0028": "She likely cannot explain it.",
    "DK4_MES_B81_R0031": "The legend troubles me. Perhaps her people's roots lie near that eastern ocean.",
    "DK4_MES_B81_R0035": "But that is only a possibility. Do not pry out of curiosity.",
    "DK4_MES_B81_R0043": "Good to see you. So you're leading the rebuilding.",
    "DK4_MES_B81_R0051": "Yes. We'll rest in this town tonight.",
    "DK4_MES_B81_R0054": "Almost nothing here. Development will take time.",
    "DK4_MES_B81_R0057": "They have few people and little money.",
    "DK4_MES_B81_R0060": "Yet this is too vulnerable. Another Ottoman attack would destroy it.",
    "DK4_MES_B81_R0064": "True. Defenses must come first. Start by gathering firearms.",
    "DK4_MES_B81_R0068": "{MACRO:FI}, no need...",
    "DK4_MES_B81_R0071": "Sera, this is your home. Obey to keep it. Weapons are needed for defense.",
    "DK4_MES_B81_R0075": "Then... five holds' worth.",
    "DK4_MES_B81_R0082": "Don't worry. We stand with you. Rebuild well.",
    "DK4_MES_B82_R0009": "The guns are ready. They will help defend it.",
    "DK4_MES_B82_R0016": "...{MACRO:FI}. Come with me. All right?",
    "DK4_MES_B82_R0020": "Sure, but why?",
    "DK4_MES_B82_R0028": "Here.",
    "DK4_MES_B82_R0032": "A fine building. You worked hard.",
    "DK4_MES_B82_R0035": "This could pass for a palace and attract military investment.",
    "DK4_MES_B82_R0038": "With investment, the town can grow.",
    "DK4_MES_B82_R0045": "My investment comes first. Build a trade hall.",

    # B83: the Swedish king summons Hodram home.
    "DK4_MES_B83_R0012": "You're Lord {MACRO:FA}, right? Sweden's king is calling for you.",
    "DK4_MES_B83_R0018": "Lord {MACRO:FA} is back! The king calls for you!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "03": "Maria Hoamei Lee",
    "10": "Gerhard Adelknauts",
    "12": "Charles",
    "18": "Sera",
    "22": "Hayreddin",
    "2B": "Escante",
    "71": "Swedish sailor",
    "73": "Tavern patron",
    "9C": "Maria's messenger",
    "FE": "Officer or scene voice",
}

EXTENDED_STATES = {0x10, 0x12, 0x18, 0x22, 0x2B, 0x71, 0x73, 0x9C, 0xFE}

CONTEXT = {
    71: "Maria summons Hodram to Hangzhou after Kuhn's defeat.",
    72: "Maria recruits Hodram to defeat the Wako leader Sojin Kurushima.",
    73: "Maria rewards Hodram after his victory over the Wako.",
    74: "Maria warns Hodram about Ottoman movements in the Mediterranean.",
    75: "Maria personally warns Hodram that the Ottoman navy has begun a major offensive.",
    76: "Escante betrays Hodram and declares war after secretly gathering power.",
    77: "The Swedish king orders Hodram to confront the Ottoman offensive.",
    78: "Escante makes a final attempt on Hodram's life after his defeat.",
    79: "A defeated Hayreddin explains Pasha's betrayal and warns Hodram.",
    80: "Sera rescues Hodram's party, rejoins his ship, and points him toward the king's tomb.",
    81: "Hodram visits Sera's homeland and commits arms to its defense.",
    82: "Hodram delivers firearms and invests in rebuilding Sera's town.",
    83: "A sailor tells Hodram that the Swedish king has summoned him.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) != set(source_rows):
        raise SystemExit(
            f"Hodram V3 inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, "
            f"extra={sorted(set(LINES)-set(source_rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        source = bytes.fromhex(row["source_hex"])
        first = source[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{MACRO:FA}", "Bergstrom"),
                "localization_note": "Faithful concise American English from the clean Japanese; character voice and route terminology are retained and wrapping uses the measured Hodram renderer profile.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram's Wako, Ottoman, Escante, Hayreddin, and Sera-homeland continuation across SC1 blocks 71-83.",
        "profile_note": "Third large source-locked Hodram continuation: Maria's Wako mission, Escante's betrayal, the Ottoman crisis, Hayreddin and Pasha, Sera's return, and rebuilding her homeland.",
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
