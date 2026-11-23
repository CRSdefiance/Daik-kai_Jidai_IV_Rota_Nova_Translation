"""Review the port favors and guild searches in four consecutive route groups."""

from types import FunctionType

from scripts import register_guild_search_and_survey_20261118 as parent
from scripts import stage_guild_search_and_survey_20261118 as workflow


base, native, precedent = workflow.base, workflow.native, workflow.precedent
ROOT = workflow.ROOT.with_name("port_favors_and_searches_20261118_v1")
ROM = ROOT / "Port_Favors_and_Searches_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = workflow.MANUSCRIPT.with_name("port_favors_and_searches_20261118_v1.json")
HISTORY = workflow.HISTORY
INDEX_MAP = {
    (1, 266): {6: 5, 9: 8},
    (3, 233): {5: 4, 9: 8, 13: 12, 16: 15, 19: 18},
}
CONTEXT = {
    (0, 273): "The guild hires Rafael to catch Jacks Bloom after he steals a client list and flees. The last lead is Africa.",
    (0, 274): "A port worker passes along the Hamburg guild's earlier search for the captain.",
    (0, 275): "Rafael recalls where to look for Jacks's fleet. The guildmaster asks whether he has found him.",
    (0, 276): "The guild holds Jacks responsible for the loss, pays Rafael, and suggests a nearby church.",
    (0, 277): "The guild recruits Rafael to apprehend Julian Vermeer, describing his allegiance and rumored Mediterranean activity.",
    (0, 278): "Julian is brought in, the guild pays Rafael and offers directions to a mosque deep in the Sahara.",
    (1, 261): "The guild asks Hodram to find Gabriel Cardocci following a breach of agreement. The Caribbean is the last known lead.",
    (1, 262): "A port worker remembers the Stockholm guild looking for a sailor willing to take on a job.",
    (1, 263): "Hodram recalls the Caribbean and the guild asks after Gabriel.",
    (1, 264): "A barkeep presses Gabriel about his tab. Hodram recognizes his target and takes him in. The crew finds what appears to be stolen property.",
    (1, 265): "Gabriel repeats an excuse Hodram heard at the tavern. The guild pays Hodram and entrusts the recovered object to him subject to finding the owner.",
    (1, 266): "The guild wants Julian Vermeer apprehended. He reportedly works as something like a courier in the Mediterranean.",
    (2, 259): "The guild asks Lil to find Julian after losing contact. His letter mentioned Copenhagen.",
    (2, 260): "Lil finds Julian drunk at the tavern. He refuses to return to Seville and she agrees to pass on the message.",
    (2, 261): "The guild accepts news of Julian's whereabouts, pays Lil, and tells her about Santiago Cathedral.",
    (2, 262): "Lil recalls the lead and the guild reiterates Julian's last known destination.",
    (2, 263): "The assignment flatters Lil and names a Spanish spy near Southeast Asia. Lil wonders how her appearance bears on it.",
    (2, 264): "Peralonso comes on strong. Lil hides her irritation, flirts to persuade him to follow her to Basra, and he takes the bait.",
    (3, 233): "The guild frames the spy search as a job for a beautiful woman. Maria coolly infers that a woman has an advantage.",
    (3, 234): "Peralonso interrupts Maria and pesters her with questions. She realizes why the guild asked her and coaxes him to Basra.",
    (3, 235): "In Basra, the guild mocks Peralonso for being caught, thanks Maria and tells her about the mosque and its treasure.",
    (3, 236): "Maria recalls the spy's assignment and a port lead places him in Brunei.",
    (3, 237): "The guild reports a possible plot and the theft of a ship. Its last lead for Yuris is near Manila.",
    (3, 238): "Yuris bristles at being called a thief. After explaining why his nobility made the case sensitive, the guild pays Maria and mentions a rumored statue.",
}
BLOCKS = {key: key for key in CONTEXT}
EDITS = {}


def revise(route, block, turn, text, note, *phrases):
    EDITS[route, block, turn] = (text, phrases, note)


revise(0, 273, 11, "He stole our guild's client list and fled to the Netherlands with it.",
       "Keep the theft and flight in one account, with the client list still in his possession.", "the Netherlands")
revise(0, 275, 13, "Jacks's fleet is somewhere near Africa. I'd better catch him soon.",
       "Rafael recalls the fleet's general location and feels some urgency.", "catch him soon.")
revise(0, 276, 68, "There's a church nearby. The priest is known for his learning.",
       "Keep the nearby church and the priest's reputation with the full phrase intact.", "known for his learning.")
revise(0, 277, 6, "I'm counting on you to bring someone in.",
       "The guild trusts Rafael with apprehending the man who is turned over to them in the next scene.", "bring someone in.")
revise(0, 277, 9, "Julian Vermeer. He's Portuguese, but he betrayed his country and sided with Spain. I hear he's something like a courier in the Mediterranean.",
       "Keep the accusation as the guildmaster's statement and the reported occupation tentative.", "Julian Vermeer.", "sided with Spain.")
revise(0, 278, 12, "You've done us a real service. We'll take it from here. Please take this.",
       "The guild assumes responsibility after Rafael's service and offers the reward.", "take it from here.")

revise(1, 261, 10, "If you run into an Italian named Gabriel Cardocci, could you bring him back here?",
       "The guild asks politely to have Gabriel brought back and names him plainly.", "Gabriel Cardocci,", "back here?")
revise(1, 262, 6, "Stockholm's guild was looking to hire a sailor.",
       "The port worker remembers the guild's search. It is an aside and a practical lead.", "Stockholm's guild")
revise(1, 264, 5, "You're settling your tab today, sir. Do you even remember how much you owe?",
       "The barkeep remains outwardly polite but insists that the growing tab finally be paid.", "how much you owe?")
revise(1, 264, 36, "W-wait! His tab...",
       "The barkeep tries to protest as Gabriel is taken away before paying.")
revise(1, 265, 5, "Here's Gabriel.",
       "Hodram announces that he brought Gabriel in, continuing the tavern scene.")
revise(1, 265, 17, "I heard that excuse at the tavern. I'll leave you to it.",
       "Hodram calls back to the repeated promise and excuses himself.", "at the tavern.", "leave you to it.")
revise(1, 265, 60, "We'll leave the stolen item with you. If nobody finds the owner, do with it as you like.",
       "The guild entrusts the item to the party with a condition on keeping it.", "finds the owner,")
revise(1, 266, 6, "I'm counting on you to bring someone in.",
       "Use the same guild request in the matching Julian assignment.", "bring someone in.")

revise(2, 259, 6, "I've got a favor to ask.",
       "The guildmaster's offer is conversational and leads into the request.")
revise(2, 260, 21, "That's him? He looks like a drunk. Is he really an adventurer?",
       "Lil's reaction moves from surprise to doubt while looking at Julian.", "looks like a drunk.")
revise(2, 260, 32, "Well, that's a problem. Oh, well. I'll tell them what you said.",
       "Lil is put out by the refusal, then accepts that she can only carry his answer back.", "what you said.")
revise(2, 261, 5, "I found Julian, the adventurer, but...",
       "Lil gives the result and trails off before delivering his refusal.", "the adventurer,")
revise(2, 261, 20, "Knowing where he is will do. Thanks for your trouble. Take this.",
       "The guild only needed to locate him and pays Lil despite his refusal.", "Thanks for your trouble.")
revise(2, 262, 17, "Word is Julian headed for Copenhagen, up in the North Sea.",
       "The guild reports the destination as a lead and preserves the game's geography.", "the North Sea.")
revise(2, 263, 5, "A pretty face like yours could help me.",
       "The guildmaster flatters Lil and makes her appearance sound pertinent.")
revise(2, 263, 13, "I need you to find a Spanish spy named Peralonso Aguirre. I hear he's operating around Southeast Asia.",
       "Name the spy and keep Southeast Asia as a reported lead.", "Peralonso Aguirre.", "Southeast Asia.")
revise(2, 263, 16, "Hee hee! You've got good taste. But what do my looks have to do with him?",
       "Lil enjoys the flattery but teasingly asks why her looks matter.")
revise(2, 264, 15, "Well, there is a pretty woman here! You should've said so, barkeep!",
       "Peralonso changes his tune when Lil enters and turns his complaint back on the barkeep.", "said so, barkeep!")
revise(2, 264, 42, "(Ugh, he's coming on strong! I'd love to knock this creep flat... But I've got to keep my cool.)",
       "Lil privately resents his familiarity and chooses to keep her composure.", "coming on strong!", "keep my cool.")
revise(2, 264, 45, "(Smiles.) Well, come with me to Basra and I'll tell you everything.",
       "Lil deliberately charms him into following her. The smile and promise play against the preceding private thought.", "come with me to Basra")

revise(3, 233, 5, "I've got a job that calls for someone as lovely as you.",
       "The guildmaster's flattery sets up the innuendo Maria understands later.", "as lovely as you.")
revise(3, 233, 16, "Sounds like a job a woman can do more easily.",
       "Maria reads the implication in the request with a cooler tone than Lil.")
revise(3, 234, 11, "Barkeep, may I ask you something?",
       "Maria was addressing the barkeep before being interrupted.", "ask you something?")
revise(3, 234, 44, "My, you're in a hurry. Why don't we go someplace where we can take our time? How about Basra?",
       "Maria lightly rebukes his impatience and makes the trip sound like a chance to talk.", "take our time?", "How about Basra?")
revise(3, 235, 67, "Here's a tip. A mosque far inland hides a great treasure.",
       "Preserve the guild's introductory favor, the inland mosque and the treasure.", "mosque far inland")
revise(3, 236, 11, "We've got to catch that Peralonso fellow in Southeast Asia.",
       "Maria remembers his given name and the region as a search lead.", "Southeast Asia.")
revise(3, 238, 15, "Some prize. Glad no foreign guild got him. People find ways to use a nobleman.",
       "The guildmaster finds him unimpressive but is relieved another guild cannot use him for his standing.", "no foreign guild", "use a nobleman.")

RETENTIONS = {
    (0, 273, 5): "The guild's casual offer leads immediately into the name and request.",
    (0, 273, 14): "Preserve the rumor that he headed for Africa and the point where the guild lost his trail.",
    (0, 276, 12): "The guildmaster thanks Rafael and downplays the value of the payment before the reward notice.",
    (0, 276, 16): "Keep the 34,000-gold payment on Rafael's route. Lil's meeting with Jacks has different terms.",
    (0, 276, 47): "The modest increase in Hamburg share follows the reward.",
    (0, 278, 65): "The map, gate at the edge of town and deep-Sahara mosque are all needed to follow the lead.",
    (1, 264, 9): "Gabriel's promise to pay next time is a setup for both the barkeep's comeback and the guild scene.",
    (1, 264, 12): "The barkeep's dry rejoinder is strongest in the existing short form.",
    (1, 264, 41): "The short report leaves the provenance of the hidden object uncertain at this point.",
    (1, 265, 13): "The repeat of next time is the point of the tavern callback.",
    (1, 265, 21): "Preserve the respectful address to the runtime surname and the guild's promised reward.",
    (1, 266, 9): "The current accusation preserves nationality, allegiance and the qualification on the courier activity.",
    (2, 260, 29): "The interruptions from hiccups, scorn for Seville and flat refusal make the drunken answer distinct.",
    (2, 261, 33): "The guild pays 9,800 gold coins after learning where Julian is.",
    (2, 261, 61): "The notice preserves the modest increase in Seville share on this path.",
    (2, 261, 92): "The corresponding outcome on the other path displays the same Seville increase.",
    (2, 264, 8): "The silent response lets Peralonso's complaint hang before Lil enters.",
    (2, 264, 38): "Retain the barrage of questions and presumptuous address, which motivate Lil's private reaction.",
    (3, 233, 9): "The brief pause conveys Maria's reserve before hearing the actual assignment.",
    (3, 234, 21): "Maria ignores the invitation and goes back to asking the barkeep. The full approved name remains intact.",
    (3, 234, 29): "Maria's composed recognition contrasts with Lil's shock in the parallel scene.",
    (3, 234, 41): "Maria privately connects the spy's behavior to the initial request.",
    (3, 235, 12): "The guildmaster laughs at the ease of the ruse. Preserve the captain's runtime given name.",
    (3, 235, 24): "The original reward amount is 21,000 gold.",
    (3, 235, 70): "The king's approval is a reported condition for claiming the treasure.",
    (3, 237, 11): "Keep the plot qualified, the involvement of foreigners, discovery before it could go ahead and the stolen ship.",
    (3, 238, 7): "Yuris takes offense at 'ship thief' on account of his rank while conceding that he was caught.",
    (3, 238, 74): "The guild leaves the truth of the rumor for Maria to investigate personally.",
}

scope = workflow.scope | globals()
for name in ("historical", "review_exchange", "collect", "main"):
    scope[name] = FunctionType(workflow.scope[name].__code__, scope)
scope["validate_native"] = precedent.validate_native
review_exchange = scope["review_exchange"]


def bind_current_indices(group, route, block, *inputs):
    rows, commands = review_exchange(group, route, block, *inputs)
    remapped = INDEX_MAP.get((route, block), {})
    for row in rows:
        index = row["source_reference"]["record_index"]
        assert row["current_reference"]["record_index"] == remapped.get(index, index), row["id"]
    return rows, commands


scope["review_exchange"] = bind_current_indices


if __name__ == "__main__":
    scope["main"]()
