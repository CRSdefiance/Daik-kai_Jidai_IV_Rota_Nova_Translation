"""Reflow six follow-up favors after inspecting the native pages."""

from types import FunctionType

from scripts import stage_followup_favors_20261118 as prior
from scripts import stage_guild_survey_wraps_20261118 as format_proofs


base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("followup_favors_20261118_v2")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("followup_favors_20261118_v2.json")
INDEX_MAP, BLOCKS = prior.INDEX_MAP, prior.BLOCKS
TUNINGS = {
    (0, 279, 26): (None, ("that traitor Julian", "as soon as you can.", "I hear he's a sort of courier", "in the Mediterranean.")),
    (0, 284, 74): ("An ancient kingdom's ruins are said to stand intact in the jungle far inland from here.",
                   ("An ancient kingdom's ruins", "stand intact", "far inland from here.")),
    (2, 268, 17): (None, ("no foreign guild got him.", "People find ways")),
    (2, 268, 74): ("They say it's sealed in the ruins here. Go see for yourself.",
                   ("in the ruins here.", "Go see for yourself.")),
    (3, 240, 18): ("Here's an advance. We can't take him on, but I think you can. We're counting on you.",
                   ("Here's an advance.", "We can't take him on,", "I think you can.", "We're counting on you.")),
    (3, 241, 65): (None, ("past the city gate.", "holds great treasure.")),
}
PHRASES = TUNINGS.keys()
EDITS = prior.EDITS.copy()
for key, (wording, phrases) in TUNINGS.items():
    earlier, _, note = EDITS[key]
    EDITS[key] = (wording or earlier, phrases, note)

scope = prior.scope | globals()
review = FunctionType(prior.review_exchange.__code__, scope)
checked = prior.scope["review_exchange"]
scope["review_exchange"] = FunctionType(checked.__code__, scope | {"review_exchange": review})
scope["validate_native"] = FunctionType(format_proofs.validate_native.__code__, scope)
for name in ("historical", "collect", "main"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)


if __name__ == "__main__":
    scope["main"]()
