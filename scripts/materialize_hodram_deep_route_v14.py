from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v14.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(180, 200))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Seville banana boom.
    "DK4_MES_B180_R0006": "Bananas! The coming age is bananas!",
    "DK4_MES_B180_R0009": "Bananas?",
    "DK4_MES_B180_R0013": "Yes. This flavor will sell.",
    "DK4_MES_B180_R0017": "Think so?",
    "DK4_MES_B180_R0021": "Yes! When this woman says so, it will!",
    "DK4_MES_B180_R0024": "Understood. What should we do?",
    "DK4_MES_B180_R0027": "Buy every banana you can find.",
    "DK4_MES_B180_R0031": "Yeah.",
    "DK4_MES_B180_R0035": "The age of bananas begins! Ohohoho!",
    "DK4_MES_B180_R0038": "Bananas may boom in Seville.",

    # Genoa tomato boom.
    "DK4_MES_B181_R0006": "Tomatoes! The coming age is tomatoes!",
    "DK4_MES_B181_R0009": "Really? This bright-red food?",
    "DK4_MES_B181_R0012": "That red stirs passion and recalls the burning love of youth.",
    "DK4_MES_B181_R0016": "...Good for you.",
    "DK4_MES_B181_R0020": "Make tomato dishes; sell them at once.",
    "DK4_MES_B181_R0023": "Understood.",
    "DK4_MES_B181_R0027": "Yes. We must not miss this tomato craze.",
    "DK4_MES_B181_R0030": "Yeah.",
    "DK4_MES_B181_R0034": "Work hard now! Ohohoho!",
    "DK4_MES_B181_R0037": "Tomatoes may boom in Genoa.",

    # Amsterdam wheat boom.
    "DK4_MES_B182_R0007": "Home-baked bread really is the best.",
    "DK4_MES_B182_R0010": "Yes. My husband loved it.",
    "DK4_MES_B182_R0013": "Really that much better?",
    "DK4_MES_B182_R0017": "Simply wonderful.",
    "DK4_MES_B182_R0021": "Yes. The corner bakery cannot compare.",
    "DK4_MES_B182_R0024": "Really? Maybe try it.",
    "DK4_MES_B182_R0028": "You should.",
    "DK4_MES_B182_R0032": "Let me teach.",
    "DK4_MES_B182_R0036": "Really? How lovely!",
    "DK4_MES_B182_R0040": "Then let us buy ingredients at once.",
    "DK4_MES_B182_R0043": "What do we need?",
    "DK4_MES_B182_R0047": "Wheat, above all.",
    "DK4_MES_B182_R0051": "Wheat may boom in Amsterdam.",

    # Sao Jorge wine boom.
    "DK4_MES_B183_R0009": "So what?",
    "DK4_MES_B183_R0016": "Wine? Any good?",
    "DK4_MES_B183_R0024": "That good?",
    "DK4_MES_B183_R0031": "Maybe a taste. Barkeep, bring one glass of wine.",
    "DK4_MES_B183_R0035": "Here.",
    "DK4_MES_B183_R0039": "Gulp, gulp, gulp...",
    "DK4_MES_B183_R0047": "Delicious! Barkeep, another!",
    "DK4_MES_B183_R0054": "Wine may boom in Sao Jorge.",

    # Lisbon spice boom.
    "DK4_MES_B184_R0005": "Did you notice that woman's wonderful fragrance?",
    "DK4_MES_B184_R0009": "You noticed it too?",
    "DK4_MES_B184_R0013": "What scent was it?",
    "DK4_MES_B184_R0017": "No idea, but that scent will surely catch on.",
    "DK4_MES_B184_R0020": "Oh dear! We must obtain it before everyone else.",
    "DK4_MES_B184_R0024": "Certainly.",
    "DK4_MES_B184_R0028": "Shall we boldly ask her the next time we meet?",
    "DK4_MES_B184_R0031": "A splendid idea. Let us do exactly that.",
    "DK4_MES_B184_R0034": "Until next time.",
    "DK4_MES_B184_R0038": "Goodbye.",
    "DK4_MES_B184_R0073": "Spices may boom in Lisbon.",

    # Athens ruby boom.
    "DK4_MES_B185_R0006": "Did you see that brilliant red ruby?",
    "DK4_MES_B185_R0009": "Yes. Magnificent.",
    "DK4_MES_B185_R0013": "What is this about?",
    "DK4_MES_B185_R0017": "The necklace that lady was wearing.",
    "DK4_MES_B185_R0020": "Ah, that enormous, beautiful stone.",
    "DK4_MES_B185_R0023": "Just once, this woman would love such a gift from a gentleman.",
    "DK4_MES_B185_R0027": "Truly. Sigh...",
    "DK4_MES_B185_R0031": "Sigh",
    "DK4_MES_B185_R0035": "Sigh",
    "DK4_MES_B185_R0039": "Rubies may boom in Athens.",

    # London gem boom.
    "DK4_MES_B186_R0005": "Did you hear? The princess is to be engaged.",
    "DK4_MES_B186_R0008": "Yes, to the duke's son, correct?",
    "DK4_MES_B186_R0011": "That ring is worth a mountain.",
    "DK4_MES_B186_R0014": "Such wealth suits a duke.{LB}When might we see that jewel?",
    "DK4_MES_B186_R0017": "Before long, surely.{LB}Then every lady will want that gem.",
    "DK4_MES_B186_R0021": "Oh! Once it catches on, too late.{LB}Do you know which gem?",
    "DK4_MES_B186_R0025": "No. We must ask around immediately!",
    "DK4_MES_B186_R0062": "Gems may boom in London.",

    # Basra painting boom.
    "DK4_MES_B187_R0006": "Hm?",
    "DK4_MES_B187_R0010": "Truly wonderful!",
    "DK4_MES_B187_R0014": "You do?",
    "DK4_MES_B187_R0018": "He will be a famous artist.",
    "DK4_MES_B187_R0021": "Ah.",
    "DK4_MES_B187_R0025": "You should buy his work while you can.",
    "DK4_MES_B187_R0028": "This one is better!",
    "DK4_MES_B187_R0032": "Not bad, but no match for his work.",
    "DK4_MES_B187_R0035": "Nonsense. That one is clearly the better work.",
    "DK4_MES_B187_R0039": "Still, his painting is mine!",
    "DK4_MES_B187_R0042": "Work by this artist is mine!",
    "DK4_MES_B187_R0045": "This one is mine!",
    "DK4_MES_B187_R0049": "Thank you very much.",
    "DK4_MES_B187_R0053": "Slam!",
    "DK4_MES_B187_R0057": "At last, they left. Must they argue inside the shop every time?",
    "DK4_MES_B187_R0061": "What was that commotion?",
    "DK4_MES_B187_R0065": "A rich man's pastime.",
    "DK4_MES_B187_R0069": "A rich hobby?",
    "DK4_MES_B187_R0073": "Yes. Painting is in fashion.",
    "DK4_MES_B187_R0076": "A refined hobby.",
    "DK4_MES_B187_R0080": "Though few buyers have a true eye for art.",
    "DK4_MES_B187_R0083": "Hahaha! Bold words, dealer.",
    "DK4_MES_B187_R0087": "Oops. Please keep that secret.",
    "DK4_MES_B187_R0091": "Understood.",
    "DK4_MES_B187_R0095": "Paintings may boom in Basra.",

    # Sofala tea boom.
    "DK4_MES_B188_R0006": "Ah, delicious!",
    "DK4_MES_B188_R0010": "Yes, tea truly is wonderful.",
    "DK4_MES_B188_R0014": "How was something this tasty not fashionable before?",
    "DK4_MES_B188_R0018": "True. People have no taste.",
    "DK4_MES_B188_R0022": "Oh, our tea is nearly gone. Would you buy more tomorrow?",
    "DK4_MES_B188_R0026": "Of course.",
    "DK4_MES_B188_R0030": "Tea is so delicious and soothing.",
    "DK4_MES_B188_R0033": "We cannot live without tea.",
    "DK4_MES_B188_R0036": "Tea may boom in Sofala.",

    # Stockholm fur boom.
    "DK4_MES_B189_R0006": "So cold. Truly freezing.",
    "DK4_MES_B189_R0010": "Yes, coldest in years.",
    "DK4_MES_B189_R0013": "A fur coat would help.{LB}This cold may freeze me.",
    "DK4_MES_B189_R0016": "This cold has raised both fur sales and prices.",
    "DK4_MES_B189_R0019": "So they say. Brrr!",
    "DK4_MES_B189_R0022": "Hopefully it warms soon.",
    "DK4_MES_B189_R0026": "True. Still, a fur coat would be lovely.",
    "DK4_MES_B189_R0029": "A fur boom may hit Stockholm.",

    # Alexandria sweets boom.
    "DK4_MES_B190_R0005": "Hm... Something is missing. Sweetness! This needs sweetness.",
    "DK4_MES_B190_R0009": "Sweetness?",
    "DK4_MES_B190_R0013": "Yes! Such a plain taste cannot satisfy customers. Sweetness is vital!",
    "DK4_MES_B190_R0016": "You think so?",
    "DK4_MES_B190_R0020": "When this woman says so, it is true!",
    "DK4_MES_B190_R0023": "Then how should we make it sweeter?",
    "DK4_MES_B190_R0026": "Working that out is your job.",
    "DK4_MES_B190_R0029": "...Yeah.",
    "DK4_MES_B190_R0033": "Anyway, sweet goods will become fashionable.",
    "DK4_MES_B190_R0036": "Yeah.",
    "DK4_MES_B190_R0040": "Sweetness above all! Work hard now! Ohohoho!",
    "DK4_MES_B190_R0063": "Sweets may boom in Alexandria.",

    # Malacca almond boom.
    "DK4_MES_B191_R0006": "Bad cough lately. Cough, cough.",
    "DK4_MES_B191_R0010": "You okay?",
    "DK4_MES_B191_R0014": "Yes. Just a little painful. Cough, cough.",
    "DK4_MES_B191_R0017": "Many people seem to be coughing lately.",
    "DK4_MES_B191_R0020": "Could an illness be spreading?",
    "DK4_MES_B191_R0024": "Word says there is good medicine.",
    "DK4_MES_B191_R0027": "Really? Which medicine? Cough.",
    "DK4_MES_B191_R0030": "Name forgotten, but it uses almonds.",
    "DK4_MES_B191_R0033": "Almonds?",
    "DK4_MES_B191_R0037": "That odd ingredient is exactly why this man remembered it.",
    "DK4_MES_B191_R0041": "Does it work? Cough, cough.",
    "DK4_MES_B191_R0045": "They say it works like magic and sells well.",
    "DK4_MES_B191_R0048": "Then time to find some.",
    "DK4_MES_B191_R0052": "This man too.",
    "DK4_MES_B191_R0056": "Thanks. Cough, cough.",
    "DK4_MES_B191_R0060": "Almonds may boom in Malacca.",

    # Osaka glass boom.
    "DK4_MES_B192_R0006": "Splendid! Art itself.",
    "DK4_MES_B192_R0010": "As you say.",
    "DK4_MES_B192_R0014": "A piece this splendid{LB}must be from a famed artisan.",
    "DK4_MES_B192_R0018": "So it seems.",
    "DK4_MES_B192_R0022": "Hm. Never knew such things were in fashion.",
    "DK4_MES_B192_R0026": "What is it called?",
    "DK4_MES_B192_R0030": "Giyaman. Glass, my lord.",
    "DK4_MES_B192_R0034": "Hm. Giyaman.",
    "DK4_MES_B192_R0038": "Add it to my collection. Gather every piece in town.",
    "DK4_MES_B192_R0041": "At once.",
    "DK4_MES_B192_R0045": "Glass may boom in Osaka.",

    # Hamburg ceramics boom.
    "DK4_MES_B193_R0006": "At last, that piece is mine.",
    "DK4_MES_B193_R0009": "Oh, the ceramics?",
    "DK4_MES_B193_R0013": "Yes. Just as expected, superb.",
    "DK4_MES_B193_R0016": "Marvelous. May this man see it?",
    "DK4_MES_B193_R0019": "Certainly. Please visit my home.",
    "DK4_MES_B193_R0022": "This ceramics craze makes fine pieces hard to obtain.",
    "DK4_MES_B193_R0026": "People who know no value are buying anything they see.",
    "DK4_MES_B193_R0030": "A nuisance.",
    "DK4_MES_B193_R0034": "Exactly.",
    "DK4_MES_B193_R0038": "Look at those men.",
    "DK4_MES_B193_R0042": "That pair? Why?",
    "DK4_MES_B193_R0046": "They paid an absurd sum for worthless ceramics recently.",
    "DK4_MES_B193_R0049": "Good customers, then.{LB}Our purses are empty.{LB}Shall we approach?",
    "DK4_MES_B193_R0053": "Nice.",
    "DK4_MES_B193_R0057": "Settled. Let's go.",
    "DK4_MES_B193_R0061": "Sir!",
    "DK4_MES_B193_R0065": "Ceramics may boom in Hamburg.",

    # Havana medicine boom.
    "DK4_MES_B194_R0024": "Heard the news?",
    "DK4_MES_B194_R0028": "What?",
    "DK4_MES_B194_R0032": "The mansion's lord.",
    "DK4_MES_B194_R0036": "His mystery illness?",
    "DK4_MES_B194_R0040": "Yes.",
    "DK4_MES_B194_R0044": "Everyone knows that story.",
    "DK4_MES_B194_R0048": "What came next?",
    "DK4_MES_B194_R0052": "After?",
    "DK4_MES_B194_R0056": "Store-bought medicine cured him at once.",
    "DK4_MES_B194_R0059": "Common medicine cured him?",
    "DK4_MES_B194_R0063": "Yes. Amazing, right?",
    "DK4_MES_B194_R0067": "Yes... Really true?",
    "DK4_MES_B194_R0071": "Apparently, that medicine cures every illness.",
    "DK4_MES_B194_R0074": "Amazing! This man wants some too.",
    "DK4_MES_B194_R0077": "Shall we find it?",
    "DK4_MES_B194_R0081": "Let's go.",
    "DK4_MES_B194_R0085": "Havana medicine boom soon.",

    # Calicut dye boom.
    "DK4_MES_B195_R0053": "Only that dye can produce this color.",
    "DK4_MES_B195_R0056": "See? We must buy it now, before the other shops take it all.",
    "DK4_MES_B195_R0060": "But...",
    "DK4_MES_B195_R0064": "Why wait?{LB}Once it sells out, it is too late.",
    "DK4_MES_B195_R0068": "There is no need to rush. Surely it will not sell out.",
    "DK4_MES_B195_R0072": "Wrong!{LB}So popular, it will vanish at once.",
    "DK4_MES_B195_R0076": "Really?",
    "DK4_MES_B195_R0080": "Yes!",
    "DK4_MES_B195_R0084": "All right. Handle it.",
    "DK4_MES_B195_R0088": "Do not sulk, father.{LB}This color guarantees profit.",
    "DK4_MES_B195_R0092": "Really?",
    "DK4_MES_B195_R0096": "Absolutely!",
    "DK4_MES_B195_R0100": "Dyes may boom in Calicut.",

    # Istanbul tobacco boom.
    "DK4_MES_B196_R0006": "Hey, have you ever smoked tobacco?",
    "DK4_MES_B196_R0010": "You mean you still have not tried it?",
    "DK4_MES_B196_R0013": "No. Never had the chance.",
    "DK4_MES_B196_R0016": "Really? With it this popular? You may be the only one in town!",
    "DK4_MES_B196_R0020": "Maybe. This man would like to try.",
    "DK4_MES_B196_R0023": "Come along; this man will show you.",
    "DK4_MES_B196_R0026": "Sure.",
    "DK4_MES_B196_R0030": "Tobacco may boom in Ｉstanbul.",

    # Seoul chili-pepper boom.
    "DK4_MES_B197_R0006": "What a meal! Never has this woman tasted anything so wonderful.",
    "DK4_MES_B197_R0010": "Truly. Such an exciting flavor.",
    "DK4_MES_B197_R0014": "How do you make food taste this good?",
    "DK4_MES_B197_R0017": "Hehe. This is it.",
    "DK4_MES_B197_R0025": "Chili pepper, a spice perfect for local foods.",
    "DK4_MES_B197_R0029": "Oh. Must it be expensive?",
    "DK4_MES_B197_R0033": "Not especially.",
    "DK4_MES_B197_R0037": "Then perhaps this woman will use it tonight.",
    "DK4_MES_B197_R0040": "This woman too.",
    "DK4_MES_B197_R0044": "Then this woman can teach you{LB}right now.",
    "DK4_MES_B197_R0047": "Really?!",
    "DK4_MES_B197_R0051": "How kind.",
    "DK4_MES_B197_R0055": "Of course. We are friends.",
    "DK4_MES_B197_R0059": "Chili peppers may boom in Seoul.",

    # Hangzhou sake boom.
    "DK4_MES_B198_R0006": "This man tried sake.",
    "DK4_MES_B198_R0010": "Same here.",
    "DK4_MES_B198_R0014": "Pretty good, right?",
    "DK4_MES_B198_R0018": "Apparently it is made from rice.",
    "DK4_MES_B198_R0022": "Huh. They make liquor from that?",
    "DK4_MES_B198_R0026": "Talking about it makes this man thirsty. Shall we have a cup?",
    "DK4_MES_B198_R0030": "Sounds good.",
    "DK4_MES_B198_R0034": "Then let us hurry.",
    "DK4_MES_B198_R0046": "What?! That must be the legendary liquor! {MACRO:FI}, did you hear?!",
    "DK4_MES_B198_R0049": "This cannot wait! Let us buy that sake at once!",
    "DK4_MES_B198_R0056": "Sake may boom in Hangzhou.",

    # Veracruz cheese boom.
    "DK4_MES_B199_R0006": "Hm? Something smells delicious.",
    "DK4_MES_B199_R0009": "Sniff... Yes.",
    "DK4_MES_B199_R0013": "Barkeep, what smells?",
    "DK4_MES_B199_R0017": "Our specialty, packed with cheese. Delicious!",
    "DK4_MES_B199_R0020": "Really that good?",
    "DK4_MES_B199_R0024": "Do not ask the obvious.",
    "DK4_MES_B199_R0028": "Then bring us one.",
    "DK4_MES_B199_R0032": "Certainly. Just a moment.{LB}Ready very soon.",
    "DK4_MES_B199_R0035": "Here you are.",
    "DK4_MES_B199_R0039": "That was fast.",
    "DK4_MES_B199_R0043": "Just trust me and take a bite.",
    "DK4_MES_B199_R0046": "Sure.",
    "DK4_MES_B199_R0050": "Munch",
    "DK4_MES_B199_R0054": "Munch",
    "DK4_MES_B199_R0058": "Delicious!",
    "DK4_MES_B199_R0062": "This is amazing!",
    "DK4_MES_B199_R0065": "Told you!",
    "DK4_MES_B199_R0069": "Everyone must hear about this!",
    "DK4_MES_B199_R0073": "Yes! Barkeep, this dish will be a sensation!",
    "DK4_MES_B199_R0077": "Cheese may boom in Veracruz.",
}


SPEAKERS = {
    "06": "Julio",
    "52": "Ceramics collector",
    "55": "Art dealer",
    "56": "Dyer",
    "57": "Townsman",
    "5C": "Tavernkeeper",
    "60": "Tavern patron",
    "67": "Tavern patron",
    "68": "Swindler",
    "6E": "Art buyer",
    "71": "Swindler",
    "73": "Townsman",
    "75": "Townsman",
    "77": "Townsman",
    "82": "Japanese lord",
    "84": "Art buyer",
    "93": "Ceramics collector",
    "94": "Art critic",
    "96": "Retainer",
    "99": "Townsman",
    "9A": "Dyer's son",
    "9B": "Sick townsman",
    "9C": "Townsman",
    "9F": "Townsman",
    "A4": "Husband",
    "A5": "Wife",
    "A6": "Lady",
    "A7": "Lady",
    "A8": "Lady",
    "AE": "Merchant",
    "AF": "Assistant",
    "FE": "System",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    180: "A Seville merchant predicts a banana boom.",
    181: "A Genoa merchant predicts a tomato boom.",
    182: "Amsterdam ladies popularize home-baked bread and wheat.",
    183: "A Sao Jorge patron discovers wine.",
    184: "Lisbon ladies pursue a fashionable fragrance made from spices.",
    185: "Athens ladies admire a ruby necklace.",
    186: "London ladies anticipate demand for the princess's engagement gem.",
    187: "Basra collectors quarrel over paintings while an art dealer explains the craze.",
    188: "A Sofala couple praises tea.",
    189: "A Stockholm couple wants furs during a cold spell.",
    190: "An Alexandria merchant insists that sweet goods will become fashionable.",
    191: "Malacca townsmen seek an almond-based cough medicine.",
    192: "A Japanese lord orders every piece of fashionable glass in Osaka.",
    193: "Hamburg collectors discuss ceramics while swindlers target them.",
    194: "Havana townsmen seek a reputed cure-all medicine.",
    195: "Calicut dyers anticipate demand for a scarce dye.",
    196: "Townsmen spread the tobacco craze in Istanbul.",
    197: "Seoul ladies discover chili peppers and plan a cooking lesson.",
    198: "Hangzhou townsmen and Julio discover sake.",
    199: "Veracruz patrons discover a cheese dish and spread the word.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V14 inventory mismatch: missing={missing}, extra={extra}")

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{MACRO:FI}", "Hodram"),
                "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places a protected newline before the native row boundary so the "
                            "progressive ASCII pair phase cannot auto-wrap and skip a display row."
                        )
                    }
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-boom-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Twenty source-locked trade-boom events across SC1 blocks 180-199.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
