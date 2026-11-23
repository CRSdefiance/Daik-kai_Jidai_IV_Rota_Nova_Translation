"""Refine the bounty warning, illustrated map, and short phrase boundaries."""

from types import FunctionType

from scripts import stage_bounty_assignments_20261118 as prior
from scripts import stage_guild_survey_wraps_20261118 as format_proofs


base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("bounty_assignments_20261118_v2")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("bounty_assignments_20261118_v2.json")
INDEX_MAP, BLOCKS = prior.INDEX_MAP, prior.BLOCKS
TUNINGS = {
    (0, 286, 26): ("One thing I nearly forgot. I hear he's very dangerous. Strong isn't quite the word... You'll see when you meet him. I'm counting on you.",
                   ("One thing I nearly forgot.", "I hear he's very dangerous.", "Strong isn't quite the word...",
                    "You'll see when you meet him.", "I'm counting on you.")),
    (0, 287, 69): (None, ("An old kingdom's ruins", "near town.", "Someone found an illustrated map", "that shows the way.")),
    (1, 276, 19): (None, ("Here's an advance.", "We can't take him on,", "I think you can.", "We're counting on you.")),
    (1, 280, 8): ("Tied up, still playing king. Fool.", ("still playing king.",)),
    (2, 273, 15): ("He was a petty thug not long ago. Word is he struck it rich in Africa. Now he thinks he's a big-shot pirate.",
                   ("He was a petty thug not long ago.", "Word is he struck it rich", "in Africa.", "a big-shot pirate.")),
    (2, 275, 12): ("That wanted man, Jacob... I've got to find his fleet, right?",
                   ("That wanted man, Jacob...", "I've got to find his fleet, right?")),
    (3, 247, 60): ("Have you heard the news? An old kingdom's ruins are said to lie somewhere near town. Someone found an illustrated map that shows the way.",
                   ("Have you heard the news?", "An old kingdom's ruins", "somewhere near town.",
                    "Someone found an illustrated map", "that shows the way.")),
    (3, 247, 63): (None, ("An illustrated map...", "I'd like to see it.", "Where is it?")),
}
PHRASES = TUNINGS.keys()
EDITS = prior.EDITS.copy()
for key, (wording, phrases) in TUNINGS.items():
    earlier, _, note = EDITS[key]
    EDITS[key] = (wording or earlier, phrases, note)

scope = prior.scope | globals()
raw_review = FunctionType(prior.review.__code__, scope)
scope["review_exchange"] = FunctionType(prior.scope["review_exchange"].__code__, scope | {"review_exchange": raw_review})
scope["validate_native"] = FunctionType(format_proofs.validate_native.__code__, scope)
for name in ("historical", "collect", "main"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)


if __name__ == "__main__":
    scope["main"]()
