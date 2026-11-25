"""Review the library, trader, two letters and Cesare scenes across all routes."""

from inspect import getsource
from pathlib import Path

from scripts import register_crew_item_rumors_20261118 as parent
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

native, base = precedent.native, precedent.base
ROOT = Path("work/crew_accounts_20261118_v1")
ROM = ROOT / "Crew_Accounts_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("crew_accounts_20261118_v1.json")
FIRST_BLOCK = (245, 236, 233, 206)
SCENES = (
    "Manuel reads an old scrap found in Alexandria's library. The captain realizes he wants to use the legendary chisel for repairs. Manuel defends the idea with his joke about Roman policy.",
    "Carlo's familiar teasing brings a distracted Filippo back to the present. Filippo recalls his great-grandfather's account of church trade, and Carlo hears a lead worth following.",
    "In a letter from West Africa, Charles recounts a Spanish merchant fleet's escape after an unearthly roar rallies the sailors. His signature ends the letter and each captain reacts in their own voice.",
    "Jam writes from India about a legendary Gupta dynasty statue. His idea of using it to beat Fernando at gambling earns a boastful reply before the captain assesses the lead.",
    "Cesare rants about sailors neglecting their work to discuss a legendary arrow. His accidental account of the two rumored locations moves the plot as the captain lets him keep grumbling.",
)
BLOCKS = {(r, start + i): (r, start + i) for r, start in enumerate(FIRST_BLOCK) for i in range(len(SCENES))}
CONTEXT = {(r, start + i): note for r, start in enumerate(FIRST_BLOCK) for i, note in enumerate(SCENES)}
HISTORY = (
    ("rafael_B241_B260_final_review_v1", "papal_trade_contextual_final_review_v1"),
    ("hodram_B231_B250_final_review_v1", "papal_trade_contextual_final_review_v1"),
    ("lil_B233_contextual_final_review_v1", "lil_B234_contextual_final_review_v1", "lil_residual_A_382_final_review_v1"),
    ("maria_B196_B215_final_review_v1", "maria_B207_contextual_final_review_v1"),
)

EDITS = {}
RETENTIONS = {}


def align(scene, ids, english, phrases, note):
    for route, record in enumerate(ids):
        if record is not None:
            EDITS[route, FIRST_BLOCK[route] + scene, record] = (english, phrases, note)


align(0, (13, 12, 12, 11), "I found an interesting scrap of paper the other day in the library at Alexandria.",
      ("scrap of paper", "the library at Alexandria."), "Manuel tells the captain where he found the paper and when. Keep his spoken lead-in and the location together.")
align(0, (None, 20, None, 19), "It tells of a chisel Phidias, the legendary sculptor of ancient Greece, supposedly used.",
      ("ancient Greece,", "supposedly used."), "Attribute the chisel to the sculptor as a claim from the paper. Preserve the ancient Greek context of Manuel's account.")
align(0, (30, 27, 26, 26), "They say he lives on in the chisel. Whoever uses it can sculpt with miraculous skill.",
      ("lives on in the chisel.", "miraculous skill."), "Preserve the two linked beliefs and the specific sculpting talent. The claim remains hearsay.")
align(0, (None, 30, 29, 29), "It's supposed to be buried somewhere on the Balkan Peninsula, near Greece. The note doesn't say exactly where.",
      ("Balkan Peninsula,", "near Greece.", "exactly where."), "The peninsula and proximity to Greece form one clue. Keep the report tentative and the place name intact.")
align(0, (36, None, None, None), "Manuel, you don't mean to use that chisel to repair ships, do you?",
      ("repair ships, do you?",), "Rafael is surprised by a practical use for a legendary relic. Attach the question tag.")
align(0, (41, 37, 36, 36), "Why not? The Romans supposedly used even kings as tools of state. Now that's a fine set of tools!",
      ("tools of state.", "set of tools!"), "Manuel compares his idea to an old Roman policy. The joke reuses tools in its literal sense without claiming the kings were physical implements.")
align(0, (44, 40, None, 39), "A ship is a work of art, too. The finer the tools, the better. Have a look for it if you get the chance.",
      ("a work of art,", "if you get the chance."), "Manuel respects a ship as a craft and invites the captain to look if opportunity permits.")

align(1, (12, 12, None, 11), "Carlo! When'd you get back?", ("get back?",),
      "Filippo recognizes Carlo with a start and asks when he returned. The familiarity fits their banter.")
align(1, (16, 16, 16, 15), "I just stopped by on business. Filippo, you'll scare away the customers if you keep staring into space!",
      ("on business.", "staring into space!"), "Carlo is only passing through. His jab about the customers follows his observation that Filippo is distracted.")
align(1, (None, None, None, 18), "Mind your own business! Still, if you're teasing me again, you must be your old self.",
      ("teasing me again,", "your old self."), "Filippo snaps back, then uses Carlo's teasing as a sign that he has recovered.")
align(1, (26, 26, 26, 25), "Oh, customers! Sorry. I was thinking about a story my great-grandfather told me.",
      ("a story", "great-grandfather told me."), "Filippo notices the customers and apologizes. Preserve the explicit family relationship and what distracted him.")
align(1, (33, 33, 33, None), "It was about trade in the Papal States. The pope once ruled lands almost to Venice.",
      ("Papal States.", "almost to Venice."), "Name the Papal States and describe the old extent of direct rule in Filippo's straightforward voice.")
align(1, (47, 47, None, 46), "The pope lost power, and trade with the Church dried up.",
      ("trade with the Church", "dried up."), "Carlo finishes Filippo's thought in natural speech and connects the decline to Church trade.")
align(1, (57, 57, None, 56), "So they say. Something a pope once used might carry a blessing. I could use a little help from above!",
      ("once used", "help from above!"), "Filippo thinks a relic may carry a blessing and grumbles that he could use one. Keep the religious meaning and wry delivery.")
align(1, (60, 60, None, 59), "A blessing...", ("A blessing...",),
      "Carlo echoes the idea of a blessing as he considers whether the relic story may be worth pursuing.")

align(2, (27, 27, 27, None), "I'm in West Africa. The sailors here told me a strange story I'd like to pass on.",
      ("West Africa.", "a strange story"), "The letter opens in Charles's measured voice and explains why he is passing on local hearsay.")
align(2, (None, None, None, 26), "Sailors here in West Africa told me a curious story.",
      ("West Africa", "a curious story."), "The letter opens by identifying both the source and the origin of the story.")
align(2, (31, None, None, None), None, ("Spanish merchant fleet", "New World", "West Africa."),
      "Keep the existing chronology and route. Wrap the merchant fleet as a unit.")
align(2, (35, 35, 35, None), "The merchant ships were badly outmatched. They tried to flee, but the pirates were faster. It seemed only a matter of time before the whole fleet was lost.",
      ("merchant ships", "a matter of time", "the whole fleet"), "Maintain the sequence of disadvantage, attempted escape and certainty of loss before the roar changes their fortunes.")
align(2, (None, None, None, 34), "Outmatched, they tried to flee, but their ships were slower. The fleet seemed doomed.",
      ("tried to flee,", "seemed doomed."), "Restore the attempt to escape and keep the imminent loss in the realm of the sailors' expectations.")
align(2, (38, 38, 38, 37), "But when they reached the waters far west of Lisbon, they say they heard an unearthly roar.",
      ("far west of Lisbon,", "an unearthly roar."), "Keep the offshore clue specific and the roar extraordinary without identifying what made it.")
align(2, (41, 41, 41, 40), "Somehow, the roar rallied the crew. They fought like lions and held their own against the pirates.",
      ("fought like lions", "their own", "against the pirates."), "Preserve the startling change in courage, the lion image and the sailors' ability to stand their ground.")
align(2, (47, None, None, 46), "What made the sound is still a mystery. We don't even know if it was a natural phenomenon.",
      ("still a mystery.", "natural phenomenon."), "Charles still cannot identify or explain the sound. Phrase the uncertainty naturally before his invitation to investigate.")
align(2, (57, None, None, None), "What a strange story. It does make me wonder...", ("strange story.", "make me wonder..."),
      "Rafael acknowledges the oddity and trails into genuine curiosity after the letter.")

align(3, (30, 30, 30, 29), "Wow, India's something else! I wouldn't know where to begin. Oh, right! I heard a good rumor.",
      ("where to begin.", "Oh, right!", "a good rumor."), "Jam's enthusiasm interrupts his account before he remembers the reason for writing.")
align(3, (33, 33, 33, 32), "They say a statue of a sacred beast from the Gupta dynasty can see the future.",
      ("sacred beast", "Gupta dynasty", "see the future."), "Use one ordinary description of the same sacred creature. The power belongs to the statue and remains a rumor.")
align(3, (None, None, None, 35), "Sounds fishy, right? But this is India. Maybe there's something to it.",
      ("Sounds fishy, right?", "this is India."), "Jam anticipates disbelief and wonders whether the unlikely story could be true in this place.")
align(3, (39, 39, 39, None), "With that, I might beat Fernando at gambling. Wishful thinking, huh?",
      ("beat Fernando", "Wishful thinking, huh?"), "Keep Fernando as Jam's rival at the gambling table and retain the self-mocking question.")
align(3, (42, 42, 42, None), "I can't find it for sale, and I haven't met anyone who's seen it.",
      ("for sale,", "who's seen it."), "Jam has neither a seller nor an eyewitness. No one certifies the rumor.")
align(3, (None, None, None, 63), "Ha! Even with that thing, he's five hundred years too early to beat me!",
      ("five hundred years", "to beat me!"), "Fernando's impossible boast answers Jam's hope of beating him. Preserve the five-hundred-year hyperbole.")
align(3, (None, None, 70, None), "Honestly, what did he go there for? Still, it's an interesting story. I'll keep it in mind.",
      ("go there for?", "keep it in mind."), "Lil rolls her eyes at Jam's priorities, then gives the lead its due.")

align(4, (27, None, 25, 24), "They say an angel used the Demon-Piercing Arrow to strike down a demon. That's the legend, sir.",
      ("Demon-Piercing Arrow", "strike down a demon.", "the legend, sir."), "Cesare relays what the sailors say after naming the arrow. The legend uses one angel and one demon. Keep the installed item title.")
align(4, (None, 24, None, None), "Legend says an angel used it to slay a demon, sir.",
      ("Legend says", "slay a demon, sir."), "Restore the hearsay in Cesare's quick answer after Hodram asks about the arrow.")
align(4, (31, None, 29, 28), "It supposedly makes you a master archer. They wonder if it works on cannons. Meanwhile, the ship goes untended!",
      ("a master archer.", "on cannons.", "goes untended!"), "The sailors wonder about the effect on cannons. Cesare is angry because they're gossiping instead of caring for the ship.")
align(4, (None, 28, None, None), "They say it turns you into a master archer. Now the sailors ask if it works on cannons, too. Meanwhile, they've left the ship untended!",
      ("a master archer.", "on cannons, too.", "the ship untended!"), "Give Cesare's three beats room across the two allocated pages while preserving his complaint about neglect.")
align(4, (None, 21, None, None), "You've lost me. What's the Demon-Piercing Arrow?",
      ("Demon-Piercing Arrow?",), "Hodram stops the rant to ask about the object in a direct voice. Keep the item name on one line.")
align(4, (None, None, None, 20), "Slow down, Cesare. What is this arrow?",
      ("Slow down, Cesare.", "What is this arrow?"), "Maria wants a clearer explanation and redirects him to the thing itself.")
align(4, (None, None, None, 41), "... (It's no use talking now.)",
      ("no use talking now.",), "Maria decides any reply now would be wasted as Cesare keeps grumbling.")

# Specific retentions supplement the existing source-linked reasons.
RETENTIONS.update({
    (0, 245, 33): "The current clue keeps Balkan Peninsula together and distinguishes an approximate area near Greece from an exact site.",
    (2, 233, 23): "Lil's practical description of a chisel sets up Manuel's argument for using a prized tool to build or repair ships.",
    (2, 234, 60): "Carlo picks up Filippo's phrase God's favor exactly. Keep the echo and his thoughtful pause.",
    (1, 238, 57): "Hodram doubts the account but notices that the roar gave the crew courage. This skeptical reaction belongs to his route.",
    (2, 235, 57): "Lil's question about a monster follows the unexplained roar. Her short tag already stays with its natural phrase.",
    (3, 208, 56): "Maria wants to check whether the tale is true. The current curiosity differs appropriately from Rafael's more open-ended reaction.",
    (0, 248, 64): "Fernando's five-hundred-year retort lands as a boast in plain speech and responses keep him as the opponent Jam names.",
})
for r, number in enumerate((5, 5, 5, 4)):
    RETENTIONS[r, FIRST_BLOCK[r] + 1, number] = "Filippo opens silently while lost in thought. Preserve the deliberate ellipsis and the original trader selector."
for r, numbers in enumerate(((50,49), (50,49), (50,49), (49,48))):
    for scene, number in enumerate(numbers, start=2):
        RETENTIONS[r, FIRST_BLOCK[r] + scene, number] = "Preserve the author's signed farewell and its distinct closing row before the captain or crew responds."

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
