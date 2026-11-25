"""Review the church figurehead and town clues across all story routes."""

from inspect import getsource
from pathlib import Path

from scripts import register_janus_and_frozen_rose_20261118 as parent
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

native, base = precedent.native, precedent.base
ROOT = Path("work/figurehead_and_ruins_20261118_v1")
ROM = ROOT / "Figurehead_and_Ruins_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("figurehead_and_ruins_20261118_v1.json")
SCENES = (
    "Julio spots a figurehead in the church. The priest explains its strange history of accepting or refusing a person. Each captain can decline or try to move it. Failure and acceptance each have their own replies.",
    "A town resident greets a returning captain and retells a sailor's story of gold dust in a New World river, then shares her delight at the thought.",
    "A resident asks Rafael about the Lamenting Jar, said to be older than pottery. She speculates while Rafael tries to keep up and asks if the jar has been found.",
    "A resident who also likes ancient history points the captain to the ruins on top of the hill visible from town.",
    "A resident insists the captain should visit the pyramid site while in town and offers directions.",
    "A resident greets the captain, mentions the rumor about King Solomon's treasury, and suggests a visit in the good weather.",
)
BLOCK_BY_SCENE = ((254, 255, 256, 257, 258, 259), (243, 244, None, 245, 246, 247),
                  (242, 243, None, 244, 245, 246), (215, 216, None, 217, 218, 219))
BLOCKS = {(r, block): (r, block) for r, blocks in enumerate(BLOCK_BY_SCENE) for block in blocks if block is not None}
CONTEXT = {(r, block): SCENES[i] for r, blocks in enumerate(BLOCK_BY_SCENE)
           for i, block in enumerate(blocks) if block is not None}
HISTORY = (
    ("rafael_B241_B260_final_review_v1",),
    ("hodram_B231_B250_final_review_v1",),
    ("lil_residual_A_382_final_review_v1", "lil_B243_B282_final_review_v1"),
    ("maria_B196_B215_final_review_v1", "maria_B216_B252_final_review_v1"),
)
EDITS = {}


def align(scene, ids, english, phrases, note):
    for route, record in enumerate(ids):
        if record is not None:
            EDITS[route, BLOCK_BY_SCENE[route][scene], record] = (english, phrases, note)


align(0, (15, None, None, None), "Look at this! What a fine figurehead!",
      ("a fine figurehead!",), "Julio interrupts the captain to show off his discovery. Keep the ordinary nautical term together.")
align(0, (18, 17, 17, 16), "You have a good eye.", ("You have a good eye.",),
      "The priest acknowledges that the crew noticed the figurehead. The brief reply leaves space for the captain's question.")
align(0, (30, 29, 28, 28), "No known history. But...", ("No known history.",),
      "The priest has no account of its origin. His trailing qualification leads into the tale of how it behaves.")
align(0, (37, 36, 35, 35), "Only those it likes can take the figurehead.",
      ("those it likes", "take the figurehead."), "The figurehead itself chooses who may take it. The priest states the rule plainly.")
align(0, (41, 40, 39, 39), "People have tried. Most left empty-handed and injured.",
      ("Most left", "empty-handed and injured."), "Distinguish the earlier attempts from the result most people experienced.")
align(0, (45, 44, 43, 43), "It somehow comes back here when whoever took it dies.",
      ("comes back here", "took it dies."), "The priest describes the unexplained return after the taker's death. He gives no cause for the death.")
align(0, (49, None, None, None), "Really? That's strange...",
      ("That's strange...",), "Rafael is startled by the history and describes it as odd before the priest offers a test.")
align(0, (57, 56, 54, 55), "You've got to be joking! We don't need a thing like that, do we, Admiral?",
      ("got to be joking!", "do we, Admiral?"), "Julio recoils and looks to the captain for agreement. The question tag completes the comic beat.")
align(0, (95, 91, 88, 90), "Fine, I'll help! Happy now? Honestly!",
      ("Fine, I'll help!", "Happy now?"), "Julio volunteers after being told he can leave. His mock annoyance carries the reversal.")
align(0, (None, None, 85, None), "Go on ahead. We can handle this.",
      ("Go on ahead.", "handle this."), "The captain offers Julio the chance to leave before he reluctantly joins in.")
align(0, (None, None, None, 86), "You can go on ahead.", ("go on ahead.",),
      "Maria offers Julio the chance to leave before he decides to help.")
align(0, (None, 154, None, None), "What else could it be? We must have been lucky.",
      ("else could it be?", "have been lucky."), "Hodram rejects the priest's suggestion of modesty and attributes the success to luck.")
align(0, (166, 158, None, 158), "I'm glad it worked out. May God bless you all.",
      ("worked out.", "May God bless you all."), "The priest welcomes the good outcome and blesses the group before the system notice.")
align(0, (None, None, 156, None), None, ("May God bless you.",),
      "The existing blessing suits the priest. Keep the complete blessing on one line.")
align(0, (186, 178, 176, 178), "Right! I was afraid you'd take it!",
      ("afraid you'd take it!",), "On the branch where the captain leaves it, Julio admits how worried he was.")
align(0, (190, None, None, None), None, ("May God bless you all.",),
      "The farewell includes a complete blessing for the group. Avoid leaving May God detached on the previous line.")

align(1, (None, 6, None, 5), "You're back!", ("you're back!",),
      "The resident warmly recognizes a returning visitor before asking about gold dust.")
align(1, (None, None, 10, None), "Ever seen gold dust?", ("gold dust?",),
      "The river rumor concerns particles of gold. Use the same phrasing as the other versions of the clue.")
align(1, (None, None, 14, None), "Gold dust?", ("Gold dust?",),
      "Lil echoes the term in surprise. It refers to the gold in the next line, not the color of sand.")
align(1, (19, 18, 18, 17), "A sailor who'd been to the New World told me about a river that carries gold dust.",
      ("to the New World", "carries gold dust."), "Keep the New World, the river and the sailor's firsthand travel. The resident passes on his story.")
align(1, (23, 22, 22, 21), "Just imagine it. Isn't it romantic?", ("Isn't it romantic?",),
      "The resident imagines the scene and asks a short, complete follow-up question.")

align(2, (15, None, None, None), "They say there's a clay jar that was made before people invented pottery.",
      ("a clay jar", "invented pottery."), "The timeline is the mystery in the rumor. Keep the apparent contradiction and the attribution.")
align(2, (22, None, None, None), "The mystery is what makes it interesting!",
      ("makes it interesting!",), "The resident delights in the unanswered question rather than trying to resolve it.")
align(2, (26, None, None, None), "Maybe there was a civilization way ahead of its time, and then it died out for some reason...",
      ("ahead of its time,", "for some reason..."), "Keep her tentative idea of a very old advanced society and its unknown fate.")
align(2, (29, None, None, None), None, ("came down", "from the sky"),
      "The resident's second wild guess comes right after the idea of a vanished civilization. Preserve the people-from-the-sky speculation.")
align(2, (32, None, None, None), "Ha ha... (This is getting a little wild.) But nobody's found the jar yet, right?",
      ("a little wild.", "the jar yet, right?"), "Rafael laughs politely, privately doubts the story, and asks whether anyone has found the jar.")
align(2, (36, None, None, None), "Nobody has, but I think it's real. It has to be!",
      ("I think it's real.", "It has to be!"), "She confirms it has not been found and insists that is no reason to give up the idea.")
align(2, (39, None, None, None), "You really think so?", ("think so?",),
      "Rafael answers her confidence with gentle skepticism.")

align(3, (11, 11, 11, 10), "Interested in ancient civilizations, too? We have ruins right here in town.",
      ("ancient civilizations, too?", "right here in town."), "The speaker finds a shared interest in the people of antiquity and points out the nearby ruins.")
align(3, (14, 14, 14, 13), "Didn't you know? They're close by. See that hill? The ruins are at the top.",
      ("They're close by.", "at the top."), "Keep the visible hill as a practical landmark and the ruins at its top.")

align(4, (16, 15, 15, 14), "You really should go while you're here. I'll show you how to get there.",
      ("while you're here.", "how to get there."), "The speaker encourages a visit and offers directions. The first question already names the site.")

align(5, (10, 10, 10, 9), "Have you visited the ruins near town? Some say they were King Solomon's treasury.",
      ("the ruins near town?", "King Solomon's treasury."), "The ruin is local. The treasury association is a rumor and the full name stays together.")
align(5, (18, None, 17, None), "It's perfect picnic weather. Why not go take a look?",
      ("perfect picnic weather.", "go take a look?"), "The speaker offers a casual incentive to explore after mentioning the ruins.")

RETENTIONS = {
    (0, 254, 22): "Julio recognizes the priest and addresses him as Father in the church. Preserve the Christian form of address.",
    (1, 243, 25): "Hodram notices the figure's regal air. Keep this route's observation distinct from the other captains' reactions.",
    (3, 215, 47): "Maria remarks that the statue almost seems alive. Keep her own inference from the priest's explanation.",
    (1, 243, 126): "Hodram tells the group to flee on the failure branch. Keep the immediate command.",
    (2, 242, 130): "The priest reports that the figurehead rejected the group. His measured words match the failed attempt.",
    (0, 256, 6): "Retain the Lamenting Jar title and the native first-name substitution in the opening address.",
}
for route, block, number in ((0, 254, 171), (1, 243, 163), (2, 242, 161), (3, 215, 163)):
    RETENTIONS[route, block, number] = "The original system notice awards one Spirit after acceptance. Preserve the exact first-name substitution and notice presentation."

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
