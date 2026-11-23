"""Review the complete recurring Hamburg ceramics conversation across all four routes."""

from inspect import getsource
from pathlib import Path

from scripts import prepare_hamburg_ceramics_cross_route_20261120 as paired
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = workflow.base, paired.parent
ROOT, SOURCE, BLOCKS = paired.ROOT, paired.SOURCE, paired.BLOCKS
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/hamburg_ceramics_cross_route_20261120_v2.json")
TURNS = (
    ("I finally got my hands on it the other day.",
     "After waiting, the collector obtained the object a few days earlier.",
     "The collector can speak of 'it' because the shopkeeper immediately recognizes the subject. Keep 'got my hands on it' together.",
     ("got my hands on it", "the other day.")),
    ("Oh, the ceramics?", "The shopkeeper asks if the collector means the ceramics.",
     "The same item category recurs in the second conversation and the forecast.", ()),
    ("Yes. It was every bit as fine as I'd hoped.", "The collector confirms and says the piece was as fine as expected.",
     "The collector's satisfaction leads into the request to see this particular piece.", ("as I'd hoped.",)),
    ("Splendid! May I see it?", "The shopkeeper admires the purchase and politely requests a look.",
     "The request stays courteous and points to the single piece the collector acquired.", ()),
    ("Of course! Do come by my home and have a look.", "The collector warmly invites the shopkeeper to visit the collector's home.",
     "The eager invitation keeps the destination and makes the reason for visiting clear.", ("by my home", "have a look.")),
    ("With everyone collecting ceramics these days, it's getting harder to find a good piece.",
     "The recent fashion for collecting ceramics has made fine pieces harder to get.",
     "The shopkeeper links the difficulty finding a good piece to the rush of new collectors.",
     ("collecting ceramics", "these days,", "a good piece.")),
    ("I hear people are buying them up just because they're in fashion. They don't know what they're worth.",
     "The collector has heard that people who cannot judge value are buying up ceramics because they are fashionable.",
     "The hearsay and the collectors' irritation set up the sellers' joke about making money from them.",
     ("buying them up", "they're in fashion.", "They don't know what they're worth.")),
    ("What a nuisance.", "The shopkeeper says the trend is a nuisance.",
     "The dry complaint fits the shopkeeper after the longer exchange about scarcity.", ()),
    ("Exactly.", "The collector agrees completely.",
     "The one-word agreement closes their conversation before the eavesdroppers speak.", ()),
    ("Hey, take a look at those men over there.", "One man points out the two collectors to his companion.",
     "The informal attention-getter marks the shift to the two men's private conversation.", ("over there.",)),
    ("Those two? What about them?", "The companion asks what is remarkable about the pair.",
     "The short question and follow-up sound like a quick reply to someone pointing across the room.", ()),
    ("They bought some worthless ceramics from me the other day. You won't believe what they paid!",
     "The speaker recently sold them worthless ceramics for an unbelievable price.",
     "The wry punch line keeps the high price and the seller's own role in the transaction.",
     ("worthless ceramics", "the other day.", "You won't believe what they paid!")),
    ("Now those are good customers! I'm a little short on cash. Why don't we go talk to them?",
     "The companion sees an opportunity, mentions being short of money and suggests approaching them.",
     "The compliment is opportunistic. The invitation keeps the easy register of the men's exchange.",
     ("Now those are good customers!", "I'm a little short on cash.", "Why don't we go talk to them?")),
    ("Sounds good.", "The first man likes the idea.", "The brisk agreement suits the speed of the scheme.", ()),
    ("Right. Let's go.", "The companion settles the matter and urges them to go.",
     "The two short beats let the men act immediately.", ()),
    ("Excuse me, sir!", "The first man calls politely to a collector.",
     "The switch to a courteous address lands the joke after the men discuss their motive.", ()),
    ("Ceramics may catch on in Hamburg.", "The game predicts ceramics will become fashionable in Hamburg.",
     "The system names the goods category and the town and keeps the forecast tentative.", ("catch on in Hamburg.",)),
)


def main():
    packet = base.load(SOURCE)
    groups = packet["groups"]
    assert len(groups) == 4
    clean_bodies = [r["source_body_hex"] for r in groups[0]["records"]]
    assert len(clean_bodies) == len(TURNS) == 17
    edits, exchanges = {}, {}
    for group in groups:
        route, block = group["route"], group["block"]
        assert (block,) == BLOCKS[route]
        assert [r["source_body_hex"] for r in group["records"]] == clean_bodies
        notes = []
        for row, (english, meaning, reason, phrases) in zip(group["records"], TURNS, strict=True):
            old = row["current_English"]
            if workflow.logical(old) != english or (english == TURNS[0][0]
                    and not any("got my hands on it" in line for line in old.splitlines())):
                edits[route, block, row["source_record_index"]] = english, phrases
            notes.append(f"{meaning}|{reason}")
        exchanges[route, block] = (0, "\n".join(notes))
    source = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=group["context"], source_meaning=meaning, localization_note=reason,',
    })
    env = vars(workflow) | globals() | dict(exchanges=exchanges, EDITS=edits)
    exec(compile(source, __file__ + "::complete-hamburg-exchange", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    main()
