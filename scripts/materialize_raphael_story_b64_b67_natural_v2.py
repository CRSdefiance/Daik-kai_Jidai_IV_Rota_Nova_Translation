from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_story_natural_v2_b64_b67.json")
SC0_SHA256 = "cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"
EXCLUDED = {
    "DK4_MES_B64_R0035": "Unverified 0x97 presentation state.",
    "DK4_MES_B64_R0043": "Unverified 0x97 presentation state.",
    "DK4_MES_B64_R0293": "Corrupt six-byte non-prose command fragment.",
    "DK4_MES_B64_R0320": "Four-byte non-prose command fragment.",
}

# One tab-delimited entry per independently addressable source record. Explicit
# {MACRO:FI} tokens preserve the player-name expansion used by this route.
TRANSLATIONS = r"""
DK4_MES_B64_R0006	Wow, there's a village even out here.
DK4_MES_B64_R0009	Quiet village. No life.
DK4_MES_B64_R0013	Hmm. Ships from other countries do stop here.
DK4_MES_B64_R0018	Huh? What's that noise?
DK4_MES_B64_R0021	Looks like trouble.
DK4_MES_B64_R0026	Let's go!
DK4_MES_B64_R0031	Wait! You said you'd pay more last time!
DK4_MES_B64_R0039	What's wrong? These are our very best!
DK4_MES_B64_R0047	Such flimsy junk. No fair price for this. Beat it!
DK4_MES_B64_R0051	Stop! Break more and you'll regret it! Everyone worked hard!
DK4_MES_B64_R0055	Ow! What was that for, woman?!
DK4_MES_B64_R0058	Ah!
DK4_MES_B64_R0063	Stop! A man doesn't strike a woman!
DK4_MES_B64_R0067	Want a fight? Take me on!
DK4_MES_B64_R0071	Tch!
DK4_MES_B64_R0075	Hmph. He ran away.
DK4_MES_B64_R0080	Okay?
DK4_MES_B64_R0088	That brute picked on a girl. Did he accuse you?
DK4_MES_B64_R0092	These for sale? We could buy them.
DK4_MES_B64_R0095	Perhaps?!
DK4_MES_B64_R0098	What would a rich boy know? Keep your pity!
DK4_MES_B64_R0102	What's her problem?! We save her, and she curses us!
DK4_MES_B64_R0107	Was our attitude really that offensive...?
DK4_MES_B64_R0111	She had no right to complain! We helped her!
DK4_MES_B64_R0115	Easy, Clau. Anger makes you hungry. Let's eat and clear our heads.
DK4_MES_B64_R0119	So that is what happened...
DK4_MES_B64_R0123	What an awful woman! Makes my blood boil!
DK4_MES_B64_R0127	No, that was wrong. Saying we'd buy them sounded condescending.
DK4_MES_B64_R0131	She had reason to be angry. Was she hurt? What can be done...?
DK4_MES_B64_R0134	{MACRO:FI}, let us stop dwelling on what is done.
DK4_MES_B64_R0138	Recognize the mistake, then never repeat it.
DK4_MES_B64_R0141	Exactly! Helping people in need is what our {MACRO:FI} does!
DK4_MES_B64_R0144	Clumsy, yes. Surely she knows you meant no harm.
DK4_MES_B64_R0148	Thanks, all.
DK4_MES_B64_R0152	Wait! She cursed us without any thanks! This isn't {MACRO:FI}'s fault!
DK4_MES_B64_R0155	Never mind. Everyone aboard is hopelessly softhearted.
DK4_MES_B64_R0158	Whew! All full.
DK4_MES_B64_R0162	Um... hello!
DK4_MES_B64_R0167	Huh?
DK4_MES_B64_R0171	Hey! You're that rude woman!
DK4_MES_B64_R0174	Please... buy these after all.
DK4_MES_B64_R0177	What?! Enough games! Who turned us down so boldly?
DK4_MES_B64_R0181	Of course, there's no pressure...
DK4_MES_B64_R0184	Obviously! What do you say, {MACRO:FI}?
DK4_MES_B64_R0188	We will judge the goods. Bring them to port.
DK4_MES_B64_R0191	Thank you! Judge them fairly. They'll be there!
DK4_MES_B64_R0195	They still may not meet our needs...
DK4_MES_B64_R0198	No risk. Don't worry.
DK4_MES_B64_R0202	Um... well...
DK4_MES_B64_R0206	Sorry about earlier!
DK4_MES_B64_R0211	Huh?
DK4_MES_B64_R0215	See you later!
DK4_MES_B64_R0219	So she is good at heart.
DK4_MES_B64_R0222	You called her rude, Clau. That was cruel.
DK4_MES_B64_R0225	She's the cruel one! We helped her, and she left us with an insult!
DK4_MES_B64_R0229	She rejects our pity, then asks us to buy. Shameless!
DK4_MES_B64_R0232	That was courage, not shamelessness.
DK4_MES_B64_R0235	She came trembling, pride cast aside, to plead for her family and village.
DK4_MES_B64_R0240	She's kind.
DK4_MES_B64_R0244	So that's it...
DK4_MES_B64_R0248	All right! Let's hurry and prepare to load her cargo!
DK4_MES_B64_R0253	You're rushing. We haven't negotiated yet.
DK4_MES_B64_R0256	{MACRO:FI}, you don't care about inspecting it, right? Buy everything! Come on!
DK4_MES_B64_R0261	C-Clau...
DK4_MES_B64_R0265	He is pushy, but Clau's directness is admirable.
DK4_MES_B64_R0269	Absolutely.
DK4_MES_B64_R0275	Then it's a deal.
DK4_MES_B64_R0279	Thank you. Good news for the village. Everyone will cheer!
DK4_MES_B64_R0284	We never exchanged names. Mine is {MACRO:FI}. And yours?
DK4_MES_B64_R0287	{MACRO:FI}... Mine is Charlotte.
DK4_MES_B64_R0291	Charlotte, why build a village on such barren land?
DK4_MES_B64_R0295	We were once wandering Romani, traveling throughout Europe.
DK4_MES_B64_R0298	Mother led me by the hand as we walked endlessly.
DK4_MES_B64_R0301	Then came an offer to settle in the New World.
DK4_MES_B64_R0305	They said gold lay everywhere, with vast fertile lands untouched.
DK4_MES_B64_R0309	We pooled every coin we had and decided to cross the sea.
DK4_MES_B64_R0313	My parents and the others were full of hope. Land and a village of our own...
DK4_MES_B64_R0316	But hope soon became despair.
DK4_MES_B64_R0319	Random digging found no gold. There was only endless wilderness.
DK4_MES_B64_R0323	Lies for money... unforgivable.
DK4_MES_B64_R0326	Though crushed, we encouraged each other and built this village.
DK4_MES_B64_R0330	We'd never owned land. Crops were hard. They still are.
DK4_MES_B64_R0334	After this, did you consider going home?
DK4_MES_B64_R0337	Home? The Romani have no country. There is nowhere for us to return to.
DK4_MES_B64_R0340	Lost goods? Blame us. Disease too? Blame us.
DK4_MES_B64_R0343	Across Europe, people looked at us like filth.
DK4_MES_B64_R0352	Two or three years ago, our crops finally fed us. At last, our own village lived!
DK4_MES_B64_R0355	A year ago, a ship stopped here. Barter began bringing us new goods.
DK4_MES_B64_R0358	But most traders pay us next to nothing, like that man did. We have no choice.
DK4_MES_B64_R0363	Your help, {MACRO:FI}, made me truly happy.
DK4_MES_B64_R0367	Never once had anyone stood up for me.
DK4_MES_B64_R0371	Charlotte... My first words hurt you.
DK4_MES_B64_R0375	You meant well. You deserved my thanks.
DK4_MES_B64_R0379	Will you come back here?
DK4_MES_B64_R0384	Yes, of course!
DK4_MES_B64_R0388	Really?
DK4_MES_B64_R0393	Promise!
DK4_MES_B64_R0397	You'd better! We'll wait
DK4_MES_B64_R0402	See you!
DK4_MES_B64_R0406	Promise...!
DK4_MES_B64_R0411	She's gone... Clau? You were here?
DK4_MES_B64_R0414	What a heartbreaking story!
DK4_MES_B64_R0418	Poor girl. She suffered in Europe and here in the New World.
DK4_MES_B64_R0423	Arcadius too?
DK4_MES_B64_R0427	Sorry. Eavesdropping was not intended, but curiosity won.
DK4_MES_B64_R0440	As Spain moved to annex Portugal, losing my own place seemed possible.
DK4_MES_B64_R0445	Yet they have had no place to live since birth...
DK4_MES_B64_R0451	{MACRO:FI}! We must do something for them!
DK4_MES_B64_R0455	Let us find a way to help the village grow, even if the benefit comes later.
DK4_MES_B64_R0459	You're right. Let's do it!
DK4_MES_B64_R0468	Charlotte...
DK4_MES_B64_R0472	Such an honest, wonderful girl.
DK4_MES_B64_R0476	Yes.
DK4_MES_B64_R0481	Yes...
DK4_MES_B64_R0486	(What can we do with our own hands?)
DK4_MES_B65_R0005	Here. This load.
DK4_MES_B65_R0010	Thank you. By the way, Charlotte...
DK4_MES_B65_R0013	What?
DK4_MES_B65_R0018	To conduct real trade, you should build a proper trading post.
DK4_MES_B65_R0022	A post?
DK4_MES_B65_R0027	More goods could be traded by specialists.
DK4_MES_B65_R0031	Ships would detour to trade here.
DK4_MES_B65_R0035	But a proper post needs workers. Everyone here is already overwhelmed.
DK4_MES_B65_R0040	Hire workers. Ships will bring people seeking work.
DK4_MES_B65_R0043	How would we pay their wages?
DK4_MES_B65_R0047	Seek merchant investment. Once funded, trade profits can sustain it.
DK4_MES_B65_R0051	Would that work? We have nothing special worth merchants' attention.
DK4_MES_B65_R0055	New investment means growth and new specialties!
DK4_MES_B65_R0058	Would anyone really invest here?
DK4_MES_B65_R0062	Of course! Count on me!
DK4_MES_B65_R0066	No... won't work.
DK4_MES_B65_R0070	Why not?
DK4_MES_B65_R0074	There is almost no stone or timber nearby. We cannot build anything large.
DK4_MES_B65_R0079	Then we'll bring timber! Just wait here!
DK4_MES_B66_R0010	Hello, Charlotte! Timber is here. Now let's build the trading post!
DK4_MES_B66_R0014	Amazing! But the village cannot afford this much timber.
DK4_MES_B66_R0019	No payment needed.
DK4_MES_B66_R0023	But...!
DK4_MES_B66_R0028	This is an investment. Once goods flourish, we'll be your first buyer!
DK4_MES_B66_R0031	Thank you, {MACRO:FI}! We'll build a splendid trading post!
DK4_MES_B66_R0036	Can't wait!
DK4_MES_B66_R0040	Now we'll be busy! Time to work!
DK4_MES_B67_R0005	Here. This load.
DK4_MES_B67_R0010	Thank you. Charlotte, there's something for you.
DK4_MES_B67_R0014	What?
DK4_MES_B67_R0019	Corn seed. Perhaps it can become a new village trade good.
DK4_MES_B67_R0023	Oh... {MACRO:FI}, you are always so kind to me...
DK4_MES_B67_R0027	D-don't worry. More specialties benefit us too.
DK4_MES_B67_R0031	Right. Thanks. They'll be glad.
DK4_MES_B67_R0035	Good! But that load looks heavy.
DK4_MES_B67_R0038	No problem. The work made me strong.
DK4_MES_B67_R0042	But...
DK4_MES_B67_R0046	{MACRO:FI}, escort her!
DK4_MES_B67_R0050	Huh?
DK4_MES_B67_R0054	No, really. See? No problem.
DK4_MES_B67_R0057	Come on! Hand that over.
DK4_MES_B67_R0060	We'll split it. Give {MACRO:FI} the heavier half...
DK4_MES_B67_R0064	There! Take this.
DK4_MES_B67_R0068	Whoa! Clau!
DK4_MES_B67_R0071	Sorry... Heavy, isn't it?
DK4_MES_B67_R0075	What? Not at all!
DK4_MES_B67_R0079	Be back soon. Clau, take care of things.
DK4_MES_B67_R0082	Leave it to me! Now get going!
DK4_MES_B67_R0085	Whew. What a pair.
DK4_MES_B67_R0088	{MACRO:FI} needs my help to follow through.
DK4_MES_B67_R0097	Come in. Tea will be ready.
DK4_MES_B67_R0101	Yes.
DK4_MES_B67_R0105	Oh... Sorry. This place shocked you.
DK4_MES_B67_R0109	There's nothing here. Barely a roof and walls.
DK4_MES_B67_R0114	When did you arrive, Charlotte?
DK4_MES_B67_R0118	We left Europe when we were eleven. Six years ago. Here.
DK4_MES_B67_R0123	Thanks. Wait, eleven six years ago means...
DK4_MES_B67_R0127	Seventeen? We're the same age, Charlotte?!
DK4_MES_B67_R0132	You looked older. Oh!
DK4_MES_B67_R0136	Surprised? My skin is rough, and look at my hands...
DK4_MES_B67_R0140	Hardly an ordinary girl our age.
DK4_MES_B67_R0144	That's not true! You seem older because you're so capable, that's all.
DK4_MES_B67_R0148	{MACRO:FI}, you're so pretty. Almost like a girl...
DK4_MES_B67_R0153	A girl?! Do you find me unreliable?
DK4_MES_B67_R0156	No, not that. The person beside you must...
DK4_MES_B67_R0161	Charlotte?
DK4_MES_B67_R0165	Nothing. Oh! The sun is already setting!
DK4_MES_B67_R0170	Right! Better hurry home.
DK4_MES_B67_R0174	Well then...
DK4_MES_B67_R0178	Wait, {MACRO:FI}!
DK4_MES_B67_R0186	Here... yours.
DK4_MES_B67_R0191	A lovely flower. Mine?
DK4_MES_B67_R0194	(Nods) Thanks for today. Sorry it's so little.
DK4_MES_B67_R0199	Thank you, Charlotte! This makes me happy.
DK4_MES_B67_R0202	May your seeds grow tall before the next visit.
DK4_MES_B67_R0207	Can't wait! See you again.
DK4_MES_B67_R0210	Yes. Goodbye.
DK4_MES_B67_R0214	Hey, Arcadius. Seen {MACRO:FI}?
DK4_MES_B67_R0218	Hello, Clau. {MACRO:FI} returned and was watering a flower.
DK4_MES_B67_R0221	A flower?
DK4_MES_B67_R0225	Yes. We brought a vase. The flower brought a smile.
DK4_MES_B67_R0229	Perhaps something nice happened.
DK4_MES_B67_R0233	Hmm. Maybe...
DK4_MES_B67_R0237	You know something, Clau.
DK4_MES_B67_R0241	W-well, a little.
DK4_MES_B67_R0245	That's unfair! Tell me. This is about that girl from before, isn't it?
DK4_MES_B67_R0249	Heh. Well...
DK4_MES_B67_R0256	So the village grows, and now another pleasure awaits us.
DK4_MES_B67_R0260	Yep.
"""

SPEAKERS = {
    "04": "Emilio Marone",
    "05": "Claudio Manous",
    "08": "Arcadius",
    "50": "Charlotte",
}
LEADING_STATES = {0x04, 0x05, 0x08, 0x50}


def parse_translations() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in TRANSLATIONS.strip().splitlines():
        record_id, english = line.split("\t", 1)
        if record_id in result:
            raise ValueError(f"duplicate translation: {record_id}")
        result[record_id] = english
    return result


def main() -> None:
    translations = parse_translations()
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in range(64, 68))
        }
    expected = set(rows) - set(EXCLUDED)
    if set(translations) != expected:
        raise SystemExit(
            f"B64-B67 inventory mismatch: missing={sorted(expected-set(translations))}, "
            f"extra={sorted(set(translations)-expected)}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for record_id, english in translations.items():
        source = bytes.fromhex(rows[record_id]["source_hex"])
        state = f"{source[0]:02X}" if source and source[0] in LEADING_STATES else ""
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        block = record_id[9:11]
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append(
            {
                "id": record_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor"),
                "context": "Raphael meets Charlotte, learns the history of her Romani village, supports its trading post, and deepens their friendship.",
                "source_meaning": english,
                "localization_note": "Natural concise American English; names, player-name macros, presentation states, and story intent are preserved.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
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
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-late-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Every safely addressable record in the contiguous Charlotte village arc, SC0 blocks 64-67.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Raphael story records")


if __name__ == "__main__":
    main()
