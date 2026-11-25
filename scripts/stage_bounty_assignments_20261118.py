"""Review consecutive bounty assignments and their guild handovers."""

from types import FunctionType

from scripts import register_followup_favors_20261118 as parent
from scripts import stage_followup_favors_20261118 as workflow


base, native, precedent = workflow.base, workflow.native, workflow.precedent
ROOT = workflow.ROOT.with_name("bounty_assignments_20261118_v1")
ROM = ROOT / "Bounty_Assignments_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = workflow.MANUSCRIPT.with_name("bounty_assignments_20261118_v1.json")
HISTORY = workflow.HISTORY
INDEX_MAP = {(0, 287): {69: 68, 72: 71, 76: 75}, (1, 274): {73: 72, 76: 75},
             (2, 277): {65: 64, 69: 68, 73: 72}}
CONTEXT = {
    (0, 286): "The guild hires Rafael to pursue English pirate William Clive, passes along the Havana lead and offers an advance. The guildmaster struggles to describe the threat.",
    (0, 287): "The guildmaster recognizes Clive's screech. Rafael tries to leave, receives the reward, then hears that a map to nearby ruins was found.",
    (0, 288): "Rafael remembers his assignment. The guild places Clive's fleet in the New World.",
    (0, 289): "The guild asks Rafael to deal with Zaganos Bey, suggests looking near Cyprus and pays an advance.",
    (0, 290): "The guild is surprised Zaganos was caught. He resigns himself to his captors. The guild pays Rafael and recommends visiting Roman ruins with a map.",
    (0, 291): "Rafael and the guild recall that Zaganos is in the Mediterranean.",
    (0, 292): "A port worker recognizes Rafael's faction and passes on the Genoa guild's inquiry.",
    (1, 274): "Jean insists that his smuggling charge is a misunderstanding. The guild tells him to work honestly, pays Hodram and describes a mosque and its treasure.",
    (1, 275): "Hodram remembers Jean's fleet in India. The guild reports that Jean is hiding there.",
    (1, 276): "The guild asks Hodram to bring in Jacob and offers an advance. Jacob reportedly struck it rich in Africa and now fancies himself a pirate.",
    (1, 277): "Jacob calls the cargo his. The guild rejects the claim, pays Hodram and gives a treasure lead with a reminder to bring a map.",
    (1, 278): "Hodram reminds himself to find Jacob's fleet. The guild asks whether he has found him.",
    (1, 279): "Other captains are too afraid to take the Hernan job. The guild asks Hodram, reports the Mediterranean lead and advances him money.",
    (1, 280): "Hernan still acts like royalty in custody. Hodram has no patience for it. The guild pays the bounty and points out a city landmark.",
    (2, 272): "Lil remembers the Plett assignment and the contact urges her to catch him.",
    (2, 273): "Lil teases the guildmaster about his immediate confidence in her. The guild asks her to bring in Jacob, explains his reputation and pays an advance.",
    (2, 274): "Jacob claims the cargo. The guildmaster rejects the claim, thanks Lil and offers the city-gate exploration clue.",
    (2, 275): "Lil remembers the hunt for Jacob's fleet. The guild asks if she has found him.",
    (2, 276): "The guild asks Lil to deal with Gabriel's violation of an agreement. Its guards cannot challenge the fleet, so Lil receives an advance to prepare.",
    (2, 277): "Gabriel repeats his apology. The guild doubts him, pays Lil the balance and tells her about the northern village and a missing monk.",
    (2, 278): "Lil recalls Gabriel's fleet in the New World. The guild presses for a quick arrest.",
    (3, 246): "The guild hires Maria to pursue Clive, passes along the Havana lead and offers an advance. The guildmaster struggles to describe the threat.",
    (3, 247): "The guildmaster recognizes Clive from his cry. Maria tries to leave. She receives the reward and asks about the map to the nearby ruins.",
    (3, 248): "Maria recalls the Clive assignment. The guild expects his fleet to be in the New World.",
    (3, 249): "The guild turns to Maria after others refuse to pursue Hernan. The location is a report and the money is an advance.",
    (3, 250): "Hernan boasts after his capture. Maria calls out his bluster. The guild pays her and suggests seeing the city's landmark.",
    (3, 251): "Maria recalls the Mediterranean lead for Hernan. The guild wants him dealt with promptly.",
}
BLOCKS = {key: key for key in CONTEXT}
EDITS = {}


def revise(route, block, turn, english, note, *phrases):
    EDITS[route, block, turn] = (english, phrases, note)


clive_warning = ("One more thing. He's dangerous, I hear. Strong isn't the word... "
                 "You'll see when you meet him. I'm counting on you.")
warning_note = "The guildmaster hesitates over how to describe Clive. The next scene pays off that hesitation with his strange cry."
for route, block, turn in ((0, 286, 26), (3, 246, 24)):
    revise(route, block, turn, clive_warning, warning_note, "He's dangerous,", "Strong isn't the word...",
           "when you meet him.", "I'm counting on you.")
for route, block, turn in ((0, 287, 5), (3, 247, 4)):
    revise(route, block, turn, "Eek! Eeeek!", "Keep the two sharp cries recognizable as the voice the guildmaster names in the next line.")

revise(0, 287, 69, "An old kingdom's ruins are said to lie near town. Someone found an illustrated map that shows the way.",
       "Keep the nearby ruins a rumor and identify the map by its illustrations and purpose.", "An old kingdom's ruins", "an illustrated map")
revise(0, 287, 76, "I don't know where it is. If you're curious, why not look for it?",
       "The guildmaster does not know where the map is and suggests Rafael look for it.", "I don't know where it is.", "why not look for it?")
revise(0, 290, 8, "Damn. Do what you want!",
       "Zaganos curses and leaves his fate to the people who caught him.")
revise(0, 290, 63, "I hear you're looking for ruins. We have some from Roman times here in Italy. Why not go take a look?",
       "Avoid repeating ruins while retaining the Roman period, Italy and the invitation.", "looking for ruins.", "from Roman times", "take a look?")

revise(1, 274, 8, "They call me a smuggler, but it's all a misunderstanding! I'm the one they keep bothering!",
       "Jean indignantly insists on his innocence and portrays himself as the one being inconvenienced.", "a misunderstanding!")
revise(1, 274, 11, "All talk. Think about the trouble you've caused others.",
       "The guildmaster dismisses the excuses and tells Jean to think of others.", "the trouble", "caused others.")
revise(1, 274, 19, "Make an honest living. That's all I ask. And don't tell me you've been doing that all along.",
       "Keep the contrast with smuggling and the guildmaster's anticipation of Jean's next excuse.", "Make an honest living.", "all along.")
revise(1, 274, 26, "Sorry you had to deal with him. It's not much, but take it.",
       "The guildmaster apologizes to Hodram and downplays the reward.", "deal with him.")
revise(1, 274, 73, "Here's a tip. There's a mosque far inland with a great treasure hidden inside.",
       "Retain the same practical clue as on Lil and Maria's routes.", "There's a mosque", "far inland", "hidden inside.")
revise(1, 276, 12, "Bring in Jacob Portunto, a wanted Dutch smuggler.",
       "Name the wanted man and keep his nationality and occupation.", "Jacob Portunto,", "Dutch smuggler.")
revise(1, 276, 19, "Here's an advance. We can't take him on, but I think you can. We're counting on you.",
       "The same guildmaster trusts Hodram to act despite being outmatched.", "Here's an advance.", "We can't take him on,", "We're counting on you.")
revise(1, 277, 13, "What are you talking about? None of it was yours!",
       "The guildmaster rejects Jacob's personal claim to the cargo.", "None of it was yours!")
revise(1, 277, 16, "Thanks for catching him. It's not much, but here.",
       "Keep the grateful handover and the guild's modest description of the reward.", "Thanks for catching him.")
revise(1, 277, 66, "Set out from the city gate. They say there's a building out that way with a great treasure hidden inside.",
       "Keep the place to start exploring, the building and the report of a hidden treasure.",
       "from the city gate.", "out that way", "hidden inside.")
revise(1, 279, 11, "He's making trouble for every merchant around here. Mention his name and nobody's brave enough to take the job.",
       "The guild explains both the harm to merchants and the reason others refuse the work.", "Mention his name", "take the job.")
revise(1, 280, 8, "Tied up and still playing king. Fool.",
       "Hodram is astonished at Hernan's royal airs even while bound.")
revise(1, 280, 11, "You finally caught him! I was right to ask you. Well done. Please take this.",
       "The guild shifts from relief to gratitude and hands Hodram the reward.", "I was right to ask you.", "Please take this.")

revise(2, 273, 8, "You already trust me that much? What's the job?",
       "Lil teasingly reacts to the guild's confidence before she even knows the assignment.", "that much?", "What's the job?")
revise(2, 273, 15, "He used to be a small-time thug. Word is he struck it rich in Africa. Now he thinks he's a big-shot pirate.",
       "Keep his rise tentative and preserve the guildmaster's contempt for his self-image.", "a small-time thug.", "struck it rich in Africa.", "a big-shot pirate.")
revise(2, 273, 18, "Here's an advance. We can't take him on. I think you can. Please help.",
       "The guild gives the advance before explaining its own limits and asking Lil to help.", "Here's an advance.", "We can't take him on.", "I think you can.")
revise(2, 274, 66, "Explore past the city gate. They say a building there holds great treasure.",
       "Give the same directions and tentative treasure report as in the parallel handovers.", "past the city gate.", "holds great treasure.")
revise(2, 275, 12, "I was supposed to find Jacob's fleet, right? He's our wanted man.",
       "Lil recalls the fleet and its association with the bounty.", "Jacob's fleet, right?", "our wanted man.")
revise(2, 276, 9, "Gabriel Cardocci is Italian. He trades here in breach of our agreement and gets in our way.",
       "Preserve the specific agreement he violates through trade.", "Gabriel Cardocci", "in breach of our agreement")
revise(2, 276, 12, "The guards can't take on his fleet. Take this advance and prepare well.",
       "Name the guards' limitation and the purpose of the advance.", "take on his fleet.", "Take this advance")
revise(2, 277, 17, "Anyway, thank you. Here's the rest of your reward.",
       "The guildmaster turns from Gabriel's promise to Lil and hands over the balance.", "Here's the rest of your reward.")
revise(2, 277, 69, "Long ago, a respected monk from here went to the northern continent to spread the faith...",
       "Keep the same place, era and reason for traveling as in Maria's exchange.", "a respected monk", "the northern continent", "spread the faith...")
revise(2, 277, 73, "They say he disappeared after discovering that village. I hope he's safe.",
       "The disappearance is reported and the guildmaster hopes the monk is safe.", "discovering that village.", "I hope he's safe.")

revise(3, 246, 4, "I've got a tough one worthy of you.",
       "The guildmaster flatters Maria by suggesting a worthy challenge.", "worthy of you.")
revise(3, 247, 11, "If you'll excuse me.",
       "Maria takes her leave with her usual composure before the guildmaster interrupts.")
revise(3, 247, 60, "Have you heard the news? The ruins of an old kingdom are said to lie near town. Someone found an illustrated map that shows the way.",
       "Keep the guildmaster's opening and rumor on the first page. The illustrated map and its purpose follow together.",
       "Have you heard the news?", "an old kingdom", "lie near town.", "Someone found an illustrated map", "that shows the way.")
revise(3, 247, 63, "An illustrated map... I'd like to see it. Where is it?",
       "Maria asks to see the specific map, leading to the guildmaster's admission.", "An illustrated map...", "Where is it?")
revise(3, 247, 66, "I don't know where it is. Why not look for it if you're interested?",
       "The guildmaster admits that he cannot give the map's location and encourages Maria to search.", "where it is.")
revise(3, 250, 7, "You're making a fool of yourself.",
       "Maria coolly dismisses Hernan's bluster as unseemly.", "a fool of yourself.")
revise(3, 250, 11, "You finally caught Hernan! I was right to ask you. Well done. Please take this.",
       "The guildmaster expresses relief, confidence in the choice and thanks before handing over the reward.", "I was right to ask you.", "Please take this.")
revise(3, 251, 23, "Get Hernan, and fast!",
       "The curt order and the final emphasis convey the guildmaster's impatience.")

RETENTIONS = {
    (0, 286, 22): "The advance is exactly 27,000 gold coins.",
    (0, 287, 9): "The guildmaster recognizes Clive by the voice before he reacts to the capture.",
    (0, 287, 17): "The stammer and abrupt request to wait motivate the reward panel.",
    (0, 287, 20): "The exact 100,000-gold reward belongs to the Clive handover.",
    (0, 289, 9): "The same line supplies the approved spelling, nationality and tentative Cyprus lead.",
    (0, 290, 14): "The exact 98,000-gold reward belongs to the Zaganos handover.",
    (0, 292, 6): "The port worker's greeting keeps the faction substitution and reports the Genoa guild's past inquiry.",
    (1, 274, 15): "Jean's indignant question invites the guildmaster's straightforward instruction.",
    (1, 274, 22): "Jean's short comic reply refers to the excuse the guildmaster just forbade.",
    (1, 274, 76): "The king's approval is rumored to be a condition for claiming the treasure.",
    (1, 276, 5): "Preserve the guild's respectful address with the captain's runtime surname.",
    (1, 279, 24): "The 30,000-gold advance comes before the Hernan encounter.",
    (1, 280, 5): "Hernan announces himself as though being escorted in triumph. The vainglory sets up Hodram's reply.",
    (1, 280, 61): "The echo invites a fuller description and keeps the dynamic speaker selector.",
    (2, 273, 5): "The guildmaster says he trusts the captain and uses her runtime surname.",
    (2, 274, 16): "The guildmaster thanks Lil, acknowledges a debt and modestly gives the reward.",
    (2, 277, 9): "The curt apology and promise are enough to set up the guildmaster's skeptical reply.",
    (2, 277, 65): "The question keeps the remote New World village and leads into the explanation of how it was discovered.",
    (3, 246, 20): "The exact 27,000-coin advance is preserved on Maria's route.",
    (3, 247, 15): "The guildmaster stammers as he calls Maria back before she leaves.",
    (3, 249, 10): "The merchants' trouble and the reluctance to take the job are already conversational and clear.",
    (3, 250, 61): "The short echo suits the guildmaster's next reply. Keep the original dynamic speaker control.",
}

scope = workflow.scope | globals()
review = FunctionType(workflow.review_exchange.__code__, scope)
scope["review_exchange"] = FunctionType(workflow.scope["review_exchange"].__code__, scope | {"review_exchange": review})
scope["validate_native"] = precedent.validate_native
for name in ("historical", "collect", "main"):
    scope[name] = FunctionType(workflow.scope[name].__code__, scope)


if __name__ == "__main__":
    scope["main"]()
