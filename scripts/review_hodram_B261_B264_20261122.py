"""Review the Gabriel assignment, reminders, and tavern encounter."""

from scripts import pair_hodram_B261_B291_20261122 as paired
from scripts import review_hodram_B253_B260_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B261_B264_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    261: "The guildmaster asks Hodram to bring back Gabriel Cardocci for breaking an agreement. The Caribbean is a lead, given as hearsay.",
    262: "A port worker passes along that the Stockholm guild is looking for a sailor to take an assignment.",
    263: "Hodram and the guildmaster separately recall that Gabriel still needs to be found and was thought to be in the Caribbean.",
    264: "Gabriel argues with the barkeep about his unpaid tab and introduces himself when Hodram asks about him. Hodram insists they go to the Stockholm guild. A sailor then reports finding something Gabriel had concealed.",
}
DECISIONS = {
    261: """
6|||The guildmaster asks a favor in a familiar voice. Sir conveys his address to the captain.
10|||The guildmaster gives Gabriel Cardocci's full approved name, his origin in Italy, and the request to bring him back.
14|He went and broke an agreement. Word is he's headed for the Caribbean...|broke an agreement.;headed for the Caribbean...|The guildmaster disapproves of Gabriel's breach and gives the direction as a report.
""",
    262: """
6|Oh, the Stockholm guild was looking for a sailor to take on a job.|the Stockholm guild;to take on a job.|The port worker remembers the opportunity and describes a specific job rather than ongoing employment.
""",
    263: """
12|I need to find this Gabriel fellow. He should be in the Caribbean.|find this Gabriel fellow.;in the Caribbean.|Hodram reminds himself who he is after and where the lead suggests looking.
17|Still haven't found Gabriel? He ought to be somewhere in the Caribbean.|Still haven't found Gabriel?;somewhere in the Caribbean.|The guildmaster asks whether Gabriel has been found and repeats the broad location.
""",
    264: """
5|||The barkeep insists on payment today and asks whether Gabriel remembers how large the tab is. The wording suits his impatience.
9|I told you, I'll pay next time! Have I ever stiffed you?|I'll pay next time!;Have I ever stiffed you?|Gabriel promises to pay next time and challenges the barkeep to name a time he did not pay what he owed. His claim sets up the retort.
12|||The barkeep says Gabriel has never paid in the first place. Keep the short reply for the timing of the joke.
15|Barkeep, do you know a man in town named Gabriel Cardocci?|in town;named Gabriel Cardocci?|Hodram interrupts to ask about Gabriel by full name. The address stays with the barkeep.
18|||Gabriel overhears his name, introduces himself grandly and returns a hostile question. The brusque language belongs to him.
21|||Hodram repeats the allegation about the guild agreement. He gives Gabriel a chance to address it.
25|||Gabriel stammers, deflects the accusation and says it is none of Hodram's business.
28|Enough talk. You're coming with me to the guild in Stockholm.|Enough talk.;the guild in Stockholm.|Hodram cuts off the protest and specifies the original destination.
32|H-hey, let go of me!|let go of me!|Gabriel stammers in surprise and demands to be released.
36|||The barkeep stammers and tries to stop them on account of the unpaid tab. The unfinished thought returns to the opening dispute.
41|Admiral, he had this hidden on him. It looks stolen.|had this hidden;It looks stolen.|A sailor reports the concealed object and treats theft as a suspicion.
""",
}

review = checked_text(previous.review, {"len(records) == 42": "len(records) == 17"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::gabriel-assignment-and-tavern", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
