"""Refine the phrase boundaries in the port favor and search exchanges."""

from types import FunctionType

from scripts import stage_guild_survey_wraps_20261118 as format_proofs
from scripts import stage_port_favors_and_searches_20261118 as prior


base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("port_favors_and_searches_20261118_v2")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("port_favors_and_searches_20261118_v2.json")
TUNINGS = {
    (0, 273, 11): ("He stole our client list and fled with it to the Netherlands.",
                   ("our client list", "fled with it to the Netherlands.")),
    (0, 275, 13): ("Jacks's fleet is near Africa. I'd better catch him soon.",
                   ("near Africa.", "I'd better catch him soon.")),
    (0, 277, 6): (None, ("counting on you", "bring someone in.")),
    (0, 277, 9): ("His name's Julian Vermeer. He's Portuguese, but he turned on his country and sided with Spain. I hear he's a sort of courier in the Mediterranean.",
                  ("His name's Julian Vermeer.", "turned on his country", "sided with Spain.",
                   "I hear he's a sort of courier", "in the Mediterranean.")),
    (0, 278, 12): (None, ("take it from here.", "Please take this.")),
    (1, 261, 10): (None, ("Gabriel Cardocci,", "bring him back here?")),
    (1, 264, 5): (None, ("today, sir.", "how much you owe?")),
    (1, 265, 60): ("Hold on to the stolen item. If no one finds the owner, do with it as you like.",
                   ("the stolen item.", "If no one finds the owner,", "do with it as you like.")),
    (1, 266, 6): (None, ("counting on you", "bring someone in.")),
    (2, 262, 17): ("Julian headed for Copenhagen, I hear. It's up in the North Sea.",
                   ("headed for Copenhagen,", "up in the North Sea.")),
    (2, 263, 13): (None, ("Peralonso Aguirre.", "around Southeast Asia.")),
    (2, 264, 42): ("(Ugh, he's so forward! I'd love to knock this creep flat... I've got to keep my cool.)",
                   ("he's so forward!", "I'd love", "knock this creep flat...", "I've got to keep my cool.)")),
    (2, 264, 45): ("(Smiles.) Come with me to Basra and I'll tell you everything.",
                   ("Come with me to Basra", "I'll tell you everything.")),
    (3, 234, 44): ("My, you're in a hurry. Let's go somewhere we can take our time. How about Basra?",
                   ("Let's go somewhere", "take our time.", "How about Basra?")),
    (3, 236, 11): (None, ("Peralonso fellow", "Southeast Asia.")),
    (3, 238, 15): ("Some prize. At least no foreign guild got him. People find ways to use a nobleman.",
                   ("no foreign guild got him.", "People find ways")),
}
PHRASES = TUNINGS.keys()
EDITS = prior.EDITS.copy()
for key, (wording, protected) in TUNINGS.items():
    earlier, _, note = EDITS[key]
    EDITS[key] = (wording or earlier, protected, note)

scope = prior.scope | globals()
review = FunctionType(prior.review_exchange.__code__, scope)
scope["review_exchange"] = FunctionType(prior.bind_current_indices.__code__, scope | {"review_exchange": review})
scope["validate_native"] = FunctionType(format_proofs.validate_native.__code__, scope)
for name in ("historical", "collect", "main"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)


if __name__ == "__main__":
    scope["main"]()
