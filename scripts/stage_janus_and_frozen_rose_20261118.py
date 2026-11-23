"""Review Janus's glove rumor and each route's Frozen Rose quest."""

from inspect import getsource
from pathlib import Path

from scripts import register_crew_accounts_20261118 as parent
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

native, base = precedent.native, precedent.base
ROOT = Path("work/janus_and_frozen_rose_20261118_v1")
ROM = ROOT / "Janus_and_Frozen_Rose_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("janus_and_frozen_rose_20261118_v1.json")
SCENES = (
    "Janus catches his hand on a mast fitting. A dockside man offers to show the crew his gloves, realizes he has lost them, and offers them to the crew if they find them near Denmark.",
    "The tavern keeper brushes off a despondent Francisca. The captain asks her what is wrong. Her father's birthday gift was stolen, and a secondhand report about imitation jewels in Havana gives them a lead.",
    "The tavern keeper demands payment, then nearly takes the glass ornament as amethyst. The captain and companions expose the swindle. The keeper intervenes, and the swindler gets away without the ornament.",
    "The captain returns the Frozen Rose. Francisca thanks the crew and suggests the unusual wooden church outside town. Each captain responds in their own voice.",
)
BLOCK_BY_SCENE = ((250, 251, 252, 253), (241, None, None, 242), (238, 239, 240, 241), (211, 212, 213, 214))
BLOCKS = {(r, block): (r, block) for r, blocks in enumerate(BLOCK_BY_SCENE) for block in blocks if block is not None}
CONTEXT = {(r, block): SCENES[i] for r, blocks in enumerate(BLOCK_BY_SCENE)
           for i, block in enumerate(blocks) if block is not None}
CONTEXT[1, 242] = (
    "Francisca recognizes the Frozen Rose after Hodram has already recovered it from Gabriel. She identifies the gift and receives it. "
    "Hodram declines another reward because the guild already paid him. She suggests the wooden church outside town."
)
HISTORY = (
    ("rafael_B241_B260_final_review_v1",),
    ("hodram_B231_B250_final_review_v1",),
    ("lil_residual_A_382_final_review_v1",),
    ("maria_B196_B215_final_review_v1",),
)
EDITS = {}


def align(scene, ids, english, phrases, note):
    for route, record in enumerate(ids):
        if record is not None:
            EDITS[route, BLOCK_BY_SCENE[route][scene], record] = (english, phrases, note)


align(0, (13, 12, 12, 11), "It's nothing serious. I caught my hand on a mast fitting while working on the ship.",
      ("caught my hand", "a mast fitting"), "Janus reassures the captain and explains the mishap. Preserve the fitting and the work he was doing.")
align(0, (17, 16, None, 15), "Hey, what's the matter?",
      ("what's the matter?",), "The man addresses Janus familiarly and asks about his injury. An ordinary greeting carries the familiarity.")
align(0, (None, 23, None, None), "One of my navigators hurt his hand.",
      ("my navigators", "hurt his hand."), "Hodram names Janus's role in this route and tells the man about his injury.")
align(0, (None, None, 23, None), "Looks like my crewmate hurt his hand.",
      ("hurt his hand.",), "The captain explains the injury to the man who just approached them. The surrounding exchange identifies Janus.")
align(0, (None, 26, None, None), "That's no good. Let me see.",
      ("Let me see.",), "The man sympathizes and offers to look at the hand. His contractions fit his casual manner.")
align(0, (35, 33, 33, 32), "Hmm. Happens to sailors all the time.",
      ("all the time.",), "The man recognizes a common shipboard injury. Use the casual voice he carries into the glove pitch.")
align(0, (38, 36, 36, 35), "Heh. I've got just the gloves to keep that from happening.",
      ("just the gloves", "from happening."), "The man claims to have gloves that would have prevented the injury, setting up his realization that they are gone.")
align(0, (46, 44, 44, 43), "You bet! Hard to find gloves this handy. Hang on... Where'd I put them?",
      ("gloves this handy.", "Where'd I put them?"), "The boast gives way to a pause while he looks for them. Keep the sudden shift in confidence.")
align(0, (56, 54, 53, 53), "Sorry about that. If I dropped them... Oh, that's it! Somewhere around Denmark!",
      ("If I dropped them...", "around Denmark!"), "He searches his memory and offers an approximate place before he narrows it down.")
align(0, (64, 62, 61, 61), "It's the Jutland Peninsula! Believe me!",
      ("Jutland Peninsula!", "Believe me!"), "Keep the complete geographic name. The eager reassurance follows his uncertainty about losing the gloves.")
align(0, (None, 66, None, None), "We'll look.", ("We'll look.",),
      "The captain accepts the lead with a simple response and commits the crew to a search.")
align(0, (None, None, None, 65), "All right. We'll look.", ("We'll look.",),
      "Maria accepts the lead after the rocky sales pitch.")
align(0, (73, 70, 69, 69), "You believe me? Good! Find them and they're yours.",
      ("You believe me?", "they're yours."), "He is relieved and offers the gloves if the crew can find them.")
align(0, (77, 74, 73, 73), "They never fit me. I was going to sell them anyway, but I swear they work.",
      ("sell them anyway,", "I swear they work."), "He planned to sell them because of the fit. Keep his assurance as a claim and the scene's final joke.")

align(1, (29, None, 27, 27), "Oh, don't mind us. Just enjoy your drink.",
      ("don't mind us.", "enjoy your drink."), "The tavern keeper brushes off the captain and redirects the customer to their drink.")
align(1, (47, None, 43, 43), "Um... You sail to towns all over the world, right?",
      ("the world, right?",), "Francisca builds up to the New World question. Keep her hesitation and fold the short tag into the question.")
align(1, (None, None, None, 87), "What was it?", ("What was it?",),
      "The captain asks what was stolen, prompting the story about the birthday gift.")
align(1, (100, None, 91, 91), "It may not be worth much, but it's a glass ornament Dad bought me for my birthday. He knows how much I love roses...",
      ("glass ornament", "for my birthday.", "love roses..."), "Keep its modest value, the glass, Dad's birthday gift and her love of roses in her own explanation.")
align(1, (103, None, 94, 94), "It's like a real rose frozen solid. Such a beautiful thing. I loved it...",
      ("a real rose", "frozen solid.", "I loved it..."), "Francisca describes the ornament's appearance and grieves its loss. The glass looks like a frozen rose.")
align(1, (None, None, 106, None), "That's not much to go on. Why'd you ask about the New World?",
      ("go on.", "the New World?"), "Lil is puzzled, then returns to Francisca's question. She makes no claim that the thief cannot be found.")
align(1, (119, None, 110, 109), "Someone a friend knows told me about a swindler in Havana. They pass glass off as jade or crystal and charge a fortune.",
      ("swindler in Havana.", "jade or crystal", "charge a fortune."), "The tip is secondhand. Preserve Havana, the imitation stones and the inflated price without identifying the swindler as the thief.")
align(1, (138, None, None, None), "If it has nothing to do with the rose, we can still go after the swindler.",
      ("the rose,", "after the swindler."), "Rafael gives a fallback reason for the trip. Keep the condition and his initiative.")
align(1, (None, None, 129, None), "If he took it, he could sell it soon. Let's hurry!",
      ("sell it soon.", "Let's hurry!"), "Camille explains why time matters if the swindler did take the piece.")
align(1, (None, None, 137, None), "Hang tight! I'll find it, I promise!",
      ("I'll find it,", "it, I promise!"), "Lil promises to return with the ornament and asks Francisca to wait. Keep her confidence and the phrase together.")
align(1, (None, None, None, 101), "No...", (), "Francisca quietly admits she does not know who stole it.")
align(1, (None, None, None, 105), "That makes it difficult. When you asked about the New World, I thought the thief might be there...",
      ("the New World,", "might be there..."), "Maria tentatively connects the earlier question to the thief's possible location.")
align(1, (None, None, None, 116), "Let's try Havana. It's the only lead we have.",
      ("the only lead",), "Maria decides to follow the one lead without promising a result.")

align(2, (6, None, 6, 5), "You're paying up today. Do you remember how much you owe me?",
      ("how much you owe me?",), "The tavern keeper insists on payment today and challenges the customer's memory of the full debt.")
align(2, (9, None, 9, 8), "I'll pay next time! When have I ever skipped out?",
      ("ever skipped out?",), "The debtor repeats his promise, then leaves an opening for the keeper's punch line.")
align(2, (13, None, 13, 12), "When have you ever paid?", ("When have you ever paid?",),
      "The keeper turns the debtor's question around. The joke depends on his never having paid.")
align(2, (None, None, None, 16), "Here. For the drinks.",
      ("For the drinks.",), "The debtor reluctantly offers the ornament to cover the tab.")
align(2, (32, None, 33, 31), "Worth a pretty penny. Call the rest interest. Keep the change! Ha!",
      ("a pretty penny.", "Keep the change!"), "He brags about the ornament's supposed value and treats the difference as interest. His laugh is part of the act.")
align(2, (53, None, None, None), "I knew it! It's glass. It has to be her rose!",
      ("her rose!",), "Rafael recognizes the glass piece and connects it to Francisca's description.")
align(2, (None, None, None, 45), "What?! You trying to ruin my business?",
      ("ruin my business?",), "The swindler reacts aggressively to Maria questioning the amethyst claim.")
align(2, (None, None, None, 64), "Give it up. The owner asked us to find that ornament. Save your excuses.",
      ("the owner", "that ornament.", "Save your excuses."), "Maria is composed and firm. She has the owner's request and rejects further excuses.")
align(2, (72, None, 69, 71), "I put up with you because you were a customer. Today you've gone too far.",
      ("were a customer.", "gone too far."), "The keeper explains his former restraint and why he intervenes now.")
align(2, (79, None, 76, 78), "I deal with rough sailors every day! Think I'd last if I couldn't fight?",
      ("rough sailors", "couldn't fight?"), "He deals with tough sailors every day and uses a rhetorical question to answer the threat.")
align(2, (106, None, 115, 102), "Thanks. He nearly fooled me. This is what you came for, right?",
      ("nearly fooled me.", "came for, right?"), "The keeper thanks the group and recognizes the object they wanted. Keep the question tag attached.")
align(2, (116, None, 120, 107), "Take it back to its owner. I'll bet he's pulled other tricks. Next time I see him, I'll turn him in to the governor's office!",
      ("back to its owner.", "other tricks.", "Next time I see him,", "turn him in", "governor's office!"), "He returns the ornament for its owner, suspects more schemes and will report the swindler if he sees him again.")

align(3, (None, 10, None, None), "Oh! May I see that ornament you're carrying?",
      ("that ornament", "you're carrying?"), "Francisca recognizes the object already in Hodram's possession. Let her question carry the surprise.")
align(3, (None, 24, None, None), "It's mine! It meant so much to me, and someone stole it...",
      ("so much to me,", "someone stole it..."), "Francisca identifies the piece and reveals the theft. Keep the sentimental value she explains in the next line.")
align(3, (None, 32, None, None), "Then it's back where it belongs.",
      ("where it belongs.",), "Hodram acknowledges the rightful owner and hands the rose back. The dry phrasing suits his response.")
align(3, (None, 53, None, None), "The guild already paid me for catching Gabriel. That's enough.",
      ("for catching Gabriel.", "That's enough."), "Hodram declines a second reward. Preserve the guild payment and Gabriel's capture.")
align(3, (None, 84, None, None), "Right under my nose. I never thought of looking there. I'll go see it.",
      ("under my nose.", "I'll go see it."), "Hodram uses the established English idiom for overlooking something nearby and agrees to visit.")
align(3, (32, None, None, None), "I'm glad you're happy. I'd better get going.",
      ("I'd better get going.",), "Rafael shares her happiness and begins to leave. Francisca interrupts with the church lead.")
align(3, (47, 76, 45, 43), "You sail all over the world, right?",
      ("the world, right?",), "Francisca checks that the crew travels widely before offering the local lead. Keep the tag with the question.")
align(3, (50, None, 48, 46), "There's a wooden church outside town. They're rare in Europe. You should visit if you get the chance.",
      ("a wooden church", "outside town.", "in Europe.", "get the chance."), "Keep the local directions, rarity of the wooden building, and invitation.")
align(3, (None, None, 53, None), "Sounds interesting! I'll take a look!",
      ("I'll take a look!",), "Lil responds promptly and with interest before Francisca thanks her again.")
align(3, (None, None, None, 12), "You found it! Thank you!",
      ("Thank you!",), "Francisca is relieved and grateful. The exclamations carry her reaction without changing the information.")
align(3, (None, None, None, 51), "A wooden church? That's rare. I'll go see.",
      ("A wooden church?",), "Maria recognizes the unusual construction and decides to follow the lead.")

RETENTIONS = {
    (0, 250, 52): "Rafael is skeptical that someone could lose a useful pair of gloves so easily. Keep the distinct question from his route.",
    (1, 241, 50): "Hodram dismisses the lead briefly and dryly, prompting the man to remember Denmark.",
    (2, 238, 50): "Lil directly questions whether the man had the gloves at all. Keep her sharper skepticism.",
    (3, 211, 49): "Maria's clipped reprimand prompts the man to compose himself and remember Denmark.",
    (0, 251, 130): "Julio raises the practical cost of crossing the Atlantic on a shaky lead. Preserve the objection before Rafael insists.",
    (2, 239, 117): "Camille argues for helping Francisca despite the weak lead. Lil's reluctant reply and later promise rely on his initiative.",
    (3, 212, 127): "Maria offers to look without promising success. Her caution differs from Lil's promise.",
    (0, 252, 24): "The swindler specifically claims amethyst. Keep it separate from the earlier reports of jade and crystal.",
    (3, 213, 53): "Xien examines the ornament and confirms it is glass. His role in the reveal is specific to Maria's route.",
    (1, 242, 21): "Hodram identifies Gabriel as the person who had the ornament and leaves Francisca to confirm ownership.",
    (1, 242, 57): "Francisca addresses Hodram by the runtime first name after he refuses payment. Preserve the original substitution.",
}
for route, block, number in ((0, 253, 19), (1, 242, 36), (2, 241, 18), (3, 214, 16)):
    RETENTIONS[route, block, number] = "The item-transfer notification identifies the installed Frozen Rose title. Preserve the exact system control and handoff phrasing."

SCOPE = vars(precedent) | globals()
for function in (precedent.historical, precedent.review_exchange, precedent.collect, precedent.main):
    changes = {
        "collect": {
            "        for group, blocks in BLOCKS.items():\n            n = blocks[route]":
                "        for group, (owner, n) in BLOCKS.items():\n            if owner != route:\n                continue",
        },
        "main": {"    assert len(groups) == 20": "    assert len(groups) == len(BLOCKS)"},
    }
    source = getsource(function)
    if function.__name__ in changes:
        source = checked_text(source, changes[function.__name__])
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), SCOPE)


if __name__ == "__main__":
    SCOPE["main"]()
