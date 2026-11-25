"""Review follow-up guild favors, bounties, and ruin clues on all four routes."""

from types import FunctionType

from scripts import register_port_favors_and_searches_20261118 as parent
from scripts import stage_port_favors_and_searches_20261118 as workflow


base, native, precedent = workflow.base, workflow.native, workflow.precedent
ROOT = workflow.ROOT.with_name("followup_favors_20261118_v1")
ROM = ROOT / "Followup_Favors_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = workflow.MANUSCRIPT.with_name("followup_favors_20261118_v1.json")
HISTORY = (workflow.HISTORY[0] + ("rafael_B281_B300_final_review_v1",), *workflow.HISTORY[1:])
INDEX_MAP = {(0, 280): {6: 5, 9: 8, 13: 12}, (3, 244): {65: 64, 69: 68, 73: 72}}
CONTEXT = {
    (0, 279): "Rafael recalls Julian's fleet location. The guild urges him to catch Julian, repeating the rumor that he works as a courier of some kind.",
    (0, 280): "The contact appeals to Rafael's sympathy for a young woman who wants to avenge her father and names the English outlaw who killed him.",
    (0, 281): "The contact rejects Plett's claim of remorse, leaves his fate to the young woman, pays Rafael and offers discreet advice about the Forbidden City.",
    (0, 282): "Rafael reminds himself to deal with Plett soon. The contact repeats the request to catch him.",
    (0, 283): "The guild hires Rafael to pursue Peralonso, a wanted former Spanish spy reportedly commanding a local squadron, and pays him an advance.",
    (0, 284): "Rafael reports the capture. The guild rewards him, then shares a rumor about the intact ruins of an ancient kingdom in the inland jungle.",
    (0, 285): "Rafael remembers the former spy. The guild expresses confidence that he is close by.",
    (1, 267): "The guild mocks Julian after his capture, takes responsibility for him and gives Hodram the reward and a lead to the Sahara mosque.",
    (1, 268): "Hodram recalls Julian's fleet in the Mediterranean. The guild urges him to bring in the reported courier.",
    (1, 269): "A port worker passes along word that the Sao Jorge guild was looking for Hodram.",
    (1, 270): "A contact appeals to Hodram on behalf of a young woman seeking to avenge her father and identifies Plett as the outlaw who killed him.",
    (1, 271): "The contact rejects Plett's apology, leaves the decision to the young woman and offers Hodram a reward and a discreet clue about the Forbidden City.",
    (1, 272): "Hodram recalls the urgent assignment. The contact repeats the request to capture Plett.",
    (1, 273): "The guild wants the smuggler Jean brought in after he defeats their task force in India. His fleet is reportedly formidable and the guild pays an advance.",
    (2, 265): "Peralonso realizes Lil tricked him. The guild mocks him, rewards her and offers the rumor of a mosque with treasure and a king whose approval is required.",
    (2, 266): "Lil recalls part of Peralonso's name and the region where he was reported. The guild gives Brunei as a lead.",
    (2, 267): "The guild asks Lil to find Yuris, a Dutch nobleman reported to have plotted with outsiders and fled in a stolen ship. Its last lead was Manila.",
    (2, 268): "Yuris is indignant at the label ship thief. Lil is tired of hearing it. The guild pays her and shares the rumor of a demon statue.",
    (2, 269): "Lil recalls Yuris's fleet and the guild reports his likely hideout in Southeast Asia.",
    (2, 270): "The contact asks Lil to help a young woman avenge her father and names the English outlaw who killed him.",
    (2, 271): "Plett claims remorse. The contact leaves his fate to the woman, pays Lil and shares a discreet tip about the Forbidden City.",
    (3, 239): "Maria recalls where the ship thief's fleet should be. The guild repeats the rumor that Yuris is hiding in Southeast Asia.",
    (3, 240): "The guild puts up an advance for bringing in Jacob, a Dutch smuggler who reportedly struck it rich in Africa and fancies himself a pirate.",
    (3, 241): "The guild dismisses Jacob's claim to the cargo, pays Maria and recommends exploring beyond the city gate with a map.",
    (3, 242): "Maria reminds herself to look for Jacob's fleet. The guild asks whether she has found him yet.",
    (3, 243): "The guild wants Maria to stop Gabriel's treaty-breaking trade. His fleet is too strong for its guards, so it advances her funds for preparations.",
    (3, 244): "Gabriel apologizes and promises to stop. The guild doubts him, pays Maria and tells her about a religious traveler who discovered a northern village and disappeared.",
    (3, 245): "Maria recalls where to find Gabriel's fleet. The guild presses her to bring him in quickly.",
}
BLOCKS = {key: key for key in CONTEXT}
EDITS = {}


def revise(route, block, turn, text, note, *phrases):
    EDITS[route, block, turn] = (text, phrases, note)


revise(0, 279, 13, "If I remember right, Julian's fleet is in the Mediterranean.",
       "Rafael recalls the reported location of Julian's fleet.", "If I remember right,", "in the Mediterranean.")
revise(0, 279, 26, "Catch that traitor Julian as soon as you can. I hear he's a sort of courier in the Mediterranean.",
       "The guild repeats the urgency and the qualified rumor from B277.", "that traitor Julian", "as soon as you can.", "a sort of courier", "the Mediterranean.")
revise(0, 281, 15, "Thank you. The young woman who asked for our help will decide what to do with him.",
       "The contact leaves the decision to the woman who made the request.", "The young woman", "what to do with him.")
revise(0, 281, 72, "Ever been to the Forbidden City? It's worth seeing at least once. It's a bit of a trip from here.",
       "Keep the conversational change of subject, the recommendation and the distance.", "the Forbidden City?", "It's worth seeing at least once.", "a bit of a trip")
revise(0, 283, 11, "They say he commands a squadron in these waters. Here's your advance. I'll pay the rest when the job is done.",
       "Keep command of the squadron a report, and distinguish the advance from the later payment.",
       "commands a squadron", "Here's your advance.", "I'll pay the rest", "the job is done.")
revise(0, 284, 18, "Thanks. Things should quiet down around here now. It may not be much, but take this.",
       "The guild expects less trouble after the capture and offers the balance modestly.", "quiet down", "around here now.")
revise(0, 284, 74, "They say the ruins of an ancient kingdom still stand intact in the jungle far inland from here.",
       "Keep the ruins intact and far inland, and frame their existence as a report.", "an ancient kingdom", "still stand intact", "far inland from here.")

revise(1, 267, 5, "They got Julian! What a sorry sight.",
       "Keep the guildmaster's spontaneous recognition and mockery.", "What a sorry sight.")
revise(1, 267, 12, "Well done. We'll take it from here. Take this.",
       "The guildmaster thanks Hodram, accepts responsibility and hands over the reward.", "We'll take it from here.")
revise(1, 267, 59, "The mosque is deep in the Sahara. Take a map. Use the gate at the edge of town.",
       "Keep the mosque, the map and the gate's location as separate necessary details.", "deep in the Sahara.", "Use the gate at the edge of town.")
revise(1, 268, 12, "Julian's fleet... in the Mediterranean.",
       "Hodram recollects the report as a practical reminder.", "the Mediterranean.")
revise(1, 269, 6, "The guild in Sao Jorge was looking for you.",
       "The worker relays a past inquiry without making a new demand.", "Sao Jorge")
revise(1, 270, 6, "Hey, you've got a heart, don't you?",
       "The contact makes a familiar appeal to sympathy as the lead-in to the request.", "don't you?")
revise(1, 270, 9, "An English outlaw killed a young woman's father. She wants revenge. Will you help her?",
       "Keep the woman and her reason for asking as in Rafael's equivalent exchange.", "a young woman's father.", "She wants revenge.", "Will you help her?")
revise(1, 271, 8, "I-I'm sorry...",
       "Plett stammers and insists that he is remorseful. Retain enough to set up the rebuke.")
revise(1, 271, 15, "Thank you. The young woman who came to us for help can decide what to do with him.",
       "The contact leaves the decision to the woman who asked for help.", "who came to us for help", "what to do with him.")
revise(1, 271, 69, "Don't tell the officials I told you.",
       "Keep the contact's personal request for discretion about his lead.", "Don't tell the officials")
revise(1, 273, 5, "I'm counting on you to bring in Jean Ramusio. He's a wanted man.",
       "The guild trusts Hodram with a bounty and names the target.", "bring in", "Jean Ramusio.", "a wanted man.")
revise(1, 273, 13, "I hear his fleet rivals a pirate's. Be ready for a fight. Here's an advance.",
       "Keep the assessment tentative, warn Hodram to take it seriously and distinguish the advance.", "I hear his fleet rivals a pirate's.", "Be ready for a fight.", "Here's an advance.")

revise(2, 265, 9, "Back again, Peralonso Aguirre. A pretty face got you caught. Some spy you are!",
       "Carry the original tease about pursuing a woman into the joke about his competence.", "Peralonso Aguirre.", "A pretty face got you caught.", "Some spy you are!")
revise(2, 265, 21, "I-I blew it.",
       "Peralonso stammers as he realizes he gave himself away.")
revise(2, 265, 68, "Here's a tip. There's a mosque far inland with a great treasure hidden inside.",
       "The guild rewards Lil with a rumor about the inland mosque and its treasure.", "There's a mosque", "far inland", "hidden inside.")
revise(2, 267, 5, "You look capable. Can you do me a favor?",
       "The guildmaster assesses Lil's ability and asks for help.", "do me a favor?")
revise(2, 267, 12, "Word is he was plotting something with foreigners. It came to light before they could act. He stole a ship and fled.",
       "Keep the plot reported, leave the discoverer unidentified, and preserve the theft and flight.", "It came to light", "He stole a ship and fled.")
revise(2, 268, 13, "Still at it? Ugh.",
       "Lil is exasperated that Yuris keeps bringing up the insult.")
revise(2, 268, 17, "Some prize. At least no foreign guild got him. People find ways to use a nobleman.",
       "The guildmaster is relieved another guild cannot use Yuris for his status.", "no foreign guild got him.", "use a nobleman.")
revise(2, 268, 74, "They say it's sealed in the ruins here. See for yourself if it's true.",
       "Keep the existence of the statue uncertain and end with the invitation.", "in the ruins here.", "See for yourself")
revise(2, 270, 9, "A young woman wants revenge. An English outlaw killed her father. Help her?",
       "Keep the young woman and her reason for seeking help.", "A young woman wants revenge.", "An English outlaw")
revise(2, 271, 15, "Thanks. We'll let the young woman decide what to do with him.",
       "The contact leaves the decision to the woman who sought help.", "The young woman", "what to do with him.")
revise(2, 271, 70, "Oh, and don't tell the officials I told you.",
       "Preserve the request for discretion after the Forbidden City clue.", "the officials")

revise(3, 240, 11, "Bring in Jacob Portunto, a wanted Dutch smuggler.",
       "Keep the assignment, name, nationality and offense in the guild's introduction.", "Jacob Portunto,")
revise(3, 240, 18, "Here's an advance. He's more than we can handle, but I think you can manage. We're counting on you.",
       "The guild is outmatched and asks Maria to take on the job after offering an advance.", "Here's an advance.", "more than we can handle,", "We're counting on you.")
revise(3, 241, 12, "What are you talking about? None of it was yours!",
       "The guildmaster answers Jacob's claim directly and says the cargo belonged to others.", "None of it was yours!")
revise(3, 241, 65, "Explore past the city gate. They say a building there holds great treasure.",
       "Keep a practical starting point, a building beyond it and the tentative treasure report.", "past the city gate.")
revise(3, 243, 4, "Think you can handle a wanted man for us?",
       "The request makes a conditional appeal to Maria's skill. Gabriel is later brought in alive.", "a wanted man")
revise(3, 243, 11, "The guards can't take on his fleet. Take this advance and prepare well.",
       "Keep the comparison to the guards, the advance and the warning to prepare thoroughly.", "take on his fleet.", "Take this advance")
revise(3, 244, 16, "Anyway, thank you. Here's the rest of your reward.",
       "The guildmaster shifts from Gabriel to Maria and pays the balance.", "Here's the rest of your reward.")
revise(3, 244, 69, "Long ago, a respected monk from here went to the northern continent to spread the faith...",
       "The source identifies a religious traveler without specifying an order.", "a respected monk", "the northern continent", "spread the faith...")
revise(3, 244, 73, "They say he disappeared after discovering that village. I hope he's safe.",
       "Keep the disappearance reported and the guildmaster's hope for his safety.", "discovering that village.", "I hope he's safe.")
revise(3, 245, 23, "Get that bastard Gabriel and bring him in quick.",
       "The guild keeps its contempt and urgency after Maria's fleet reminder.", "bring him in quick.")

RETENTIONS = {
    (0, 280, 6): "The familiar appeal to Rafael's sympathy sets up the woman's request.",
    (0, 280, 9): "The young woman, the murder of her father and her desire for revenge are already clear.",
    (0, 280, 13): "The contact names Plett and presses Rafael for a commitment.",
    (0, 281, 8): "Plett stammers and claims remorse before the contact rejects the excuse.",
    (0, 281, 19): "The contact is surprised Plett was brought back alive and promises a substantial payment.",
    (0, 284, 82): "The guildmaster distinguishes a rumor from a confirmed discovery and encourages Rafael to try.",
    (1, 267, 16): "The 32,000-gold reward stays exact.",
    (1, 271, 12): "The short rebuke turns Plett's claim of remorse back on him.",
    (1, 273, 9): "The guild was already tracking Jean as a smuggler. He defeated their force in India.",
    (2, 265, 13): "The guild's mocking question follows the failed flirtation. Keep the runtime given name.",
    (2, 265, 71): "The king's approval is a rumor and a requirement for the treasure, as in Maria's parallel exchange.",
    (2, 268, 8): "Yuris admits being caught and objects to what he sees as an insult to his noble standing.",
    (2, 268, 70): "The short echo gives the guildmaster room to explain the rumor. Keep the original dynamic speaker control.",
    (2, 269, 12): "Lil's reminder keeps the ship thief epithet, the fleet, its region and her quick question tag.",
    (2, 271, 8): "Plett's stammer and defensive 'all right?' convey his insistence that he is sorry.",
    (3, 239, 11): "Maria recalls where to find the ship thief's fleet. The question tag gives the memory room for doubt.",
    (3, 240, 4): "The guild expresses confidence directly to the captain. Keep the runtime surname.",
    (3, 240, 15): "The rise from petty thug to self-styled pirate is already clear. The success in Africa stays reported.",
    (3, 241, 76): "The guild gives the map requirement after describing where to explore.",
    (3, 243, 8): "Gabriel's nationality, trade, breach of the agreement and interference with the guild are explicit.",
    (3, 244, 8): "Gabriel repeats that he is sorry and promises to stop, setting up the guild's skepticism.",
    (3, 244, 12): "The guildmaster's brief question conveys doubt about Gabriel's promise.",
}

scope = workflow.scope | globals()
review_exchange = FunctionType(workflow.review_exchange.__code__, scope)
scope["review_exchange"] = FunctionType(workflow.bind_current_indices.__code__, scope | {"review_exchange": review_exchange})
scope["validate_native"] = precedent.validate_native
for name in ("historical", "collect", "main"):
    scope[name] = FunctionType(workflow.scope[name].__code__, scope)


if __name__ == "__main__":
    scope["main"]()
