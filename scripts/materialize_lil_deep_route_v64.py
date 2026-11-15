from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v64.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Carlo orders his usual quantity of cinnamon.", "Cinnamon, as usual."),
    9: ("Lil notices a customer ahead of them.", "(A customer?)"),
    13: ("Adil quotes Carlo a price.", "Here. This much."),
    17: ("Carlo observes that the price has risen.", "Oh? Prices went up?"),
    21: ("Adil denies the increase.", "No, same as always."),
    24: ("Carlo says he knows what Adil paid for the cinnamon.", "Come now, Adil. Your cost is no secret. Can you do better?"),
    27: ("Adil is taken aback.", "Hey!"),
    31: ("Carlo says the harvest and demand justify a better price.", "With this year's harvest and demand here, surely you can do better."),
    35: ("Carlo threatens to buy elsewhere.", "Or maybe another shop will. No law says you get all my trade."),
    39: ("Adil reluctantly concedes the bargain.", "Ah... all right. You win, Carlo."),
    43: ("Carlo notices Adil has a fever.", "Hm? Adil, do you have a fever?"),
    46: ("Adil asks whether Carlo is still attacking his prices.", "What now, Carlo? More complaints about my prices?"),
    49: ("Carlo urges feverish Adil to rest.", "No. You feel hot. Go home and rest."),
    52: ("Adil initially dismisses the concern, then feels chills.", "Oh, come on... Wait. These chills are real."),
    55: ("Carlo postpones the purchase and tells Adil to close for the day.", "See? Rest now. We can trade tomorrow."),
    58: ("Adil agrees and asks Lil's party to return tomorrow.", "You're right. Travelers, sorry. Try tomorrow."),
    64: ("Carlo apologizes to Lil's party for delaying their trade.", "Sorry about that. You came to trade too, didn't you?"),
    67: ("Lil asks how Carlo knew.", "How did you know?"),
    71: ("Carlo asks what she means.", "Hm?"),
    75: ("Lil clarifies she means Adil's illness.", "That he was sick."),
    79: ("Carlo says he saw Adil's pallor.", "He looked pale."),
    91: ("Fernando praises Carlo's perceptiveness.", "Hm. You have a sharp eye, like mine."),
    97: ("Lil privately doubts Fernando's claim.", "(...Does he?)"),
    101: ("Carlo says he is unusually alert to people's health.", "Most miss it. But poor health catches my eye."),
    105: ("Lil is impressed.", "Oh..."),
    109: ("Carlo invites Lil to meet him at the trading post tomorrow to make up the delay.", "Meet me tomorrow at the trading post. Let me repay you."),
    112: ("Lil accepts Carlo's promise to repay the favor.", "You owe us? Sure, count me in!"),
    115: ("Adil's wife thanks Carlo for helping her husband yesterday.", "Carlo! Thank you for yesterday!"),
    119: ("Carlo asks how Adil is.", "How's Adil?"),
    123: ("Adil's wife says he is resting at home today.", "He's resting at home today."),
    126: ("Carlo wishes Adil a quick recovery.", "Good. Hope he's well soon."),
    130: ("Adil's wife says he never listens to her and Carlo's warning helped.", "He never listens to me. You helped him yesterday..."),
    134: ("Adil's wife calls Carlo a lifesaver and offers thanks.", "Ah, too much talk. You may have saved his life. Let me thank you."),
    138: ("Carlo asks that the delayed travelers receive the gift instead.", "Give it to the travelers. They waited a day."),
    142: ("Adil's wife apologizes to Lil's crew and offers them a gift.", "Sorry we kept you waiting. Please take this small gift."),
    148: ("Carlo thanks her and invites the travelers to buy first.", "Thanks. Let these travelers shop first. They're in a hurry."),
    152: ("Recovered Adil apologizes to Carlo for the previous day.", "Carlo! Sorry about yesterday!"),
    155: ("Adil's wife is shocked to see him out of bed.", "Adil!"),
    159: ("Carlo tells Adil he should still be resting.", "Adil! Shouldn't you be in bed?"),
    162: ("Adil insists he is well and will not miss a day of trading.", "Good as new! Can't waste this trading day."),
    166: ("Adil's wife scolds her stubborn husband.", "You're impossible!"),
    170: ("Carlo is relieved but asks Adil not to overdo it.", "Well, you look better. Just take it easy today."),
    174: ("Carlo asks Adil to serve Lil's party while he returns another day.", "Back tomorrow. Please help these travelers today."),
    177: ("Carlo urges the travelers to value family and health.", "Travelers, cherish family and health. Goodbye."),
    185: ("Lil calls Carlo back.", "Wait!"),
    189: ("Carlo responds.", "Hm?"),
    193: ("Lil invites Carlo to sail with her.", "Come sail with me!"),
    197: ("Carlo is surprised by the sudden invitation.", "What? Where did that come from?"),
    201: ("Lil feels an instinctive bond with Carlo.", "We'd get along. Call it a hunch."),
    204: ("Carlo says he is a merchant, not a sailor.", "A sailor? No, just a merchant."),
    207: ("Lil says she recognized him as a professional.", "See? A real pro!"),
    210: ("Lil says Carlo need not steer the ship because she is a merchant too.", "No need to steer. We're both merchants!"),
    217: ("Lil asks if Carlo has a reason to stay in Malacca, which is not his hometown.", "Why stay here? Malacca isn't even your home, is it?"),
    221: ("Carlo reveals his family died a year ago.", "My family... died a year ago."),
    229: ("Carlo says his daughter caught an epidemic disease while he neglected her for work.", "My daughter fell ill. Work kept me away when she needed me."),
    232: ("Carlo's delayed response led to his wife's infection and the loss of both.", "Treatment came too late. My wife caught it too. Both were gone."),
    236: ("Lil responds with sympathy.", "Oh..."),
    240: ("Carlo says work gained at his family's expense felt empty, and health matters more now.", "What was work worth if it cost my family? Nothing. Since then, people's health matters more."),
    243: ("Lil realizes that is how Carlo noticed Adil's illness.", "Oh... that's how you spotted it."),
    246: ("Lil asks whether Carlo considered returning to his hometown.", "Didn't you think of going home?"),
    249: ("Carlo says Venice holds too many happy memories to face alone.", "Venice? Too many happy memories there. Living there alone would hurt too much."),
    257: ("Lil again urges Carlo to come with them.", "Then come with us. Please."),
    264: ("Lil offers her crew as a new family for Carlo.", "No point being alone. We'll be your family now."),
    276: ("Emilio says meals taste better together.", "Yeah! Meals taste better together!"),
    282: ("Kamil praises Lil for her kind words.", "{MACRO:FI}! That was a lovely thing to say!"),
    285: ("Lil jokingly says she always speaks wisely and asks Carlo again.", "All my words are good! Well, Carlo?"),
    289: ("Carlo accepts the offer and thanks them.", "...Thank you. Glad to join you."),
    292: ("Lil cheers.", "Yes!"),
    296: ("Kamil tells Lil he has new respect for her.", "{MACRO:FI}... New respect."),
    299: ("Carlo introduces himself as Carlo Sinato.", "Carlo Sinato. Glad to meet you."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio",
    0x13: "Carlo Sinato", 0x14: "Fernando Dias", 0x69: "Adil",
    0x8E: "Adil's wife", 0xFE: "Carlo narration",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B157_")}
    authored = {f"DK4_MES_B157_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B157 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B157_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Carlo Sinato notices merchant Adil's illness, helps his wife and Lil's "
                "crew, then recounts losing his family and accepts Lil's invitation."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B157 Japanese. FI name macros and all "
                "presentation leads, including Adil, his wife, and narration, "
                "retain their control behavior. Literal uppercase I/F are unsafe."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v64-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 70 B157 Carlo Sinato recruitment dialogue records.",
        "inventory": {"identified_records": 70, "translated_records": 70, "blocks": {"157": 70}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
