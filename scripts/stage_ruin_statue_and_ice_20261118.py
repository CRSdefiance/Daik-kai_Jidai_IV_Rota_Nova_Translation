"""Review the compassionate statue, the ice puzzle and the local ruin replies."""

from inspect import getsource
from pathlib import Path

from scripts import register_figurehead_and_ruins_20261118 as parent
from scripts import ruin_puzzle_fe_20261118 as fe
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_fe

native, base = precedent.native, precedent.base
ROOT = Path("work/ruin_statue_and_ice_20261118_v1")
ROM = ROOT / "Ruin_Statue_and_Ice_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("ruin_statue_and_ice_20261118_v1.json")
FIRST_BLOCK = (260, 251, 250, 220)
SCENES = (
    "The captain senses warmth or compassion in the statue. Cesare admires the figurehead, then worries about taking it. If taken, Cesare hears a protective voice and the captain and Cesare gain Luck. Leaving it preserves Cesare's private reflection and the Charm notices.",
    "The crew reads the floating-ice inscription and chooses a stone. Front and left lead to separate wrong-answer sequences. The right stone opens the wall. The unwoken and awakened exchanges lead to different responses from the unknown voice. Fernando wonders about a curse, which remains unconfirmed.",
    "The resident decides to make an exception for the visiting captain and shares a local ruin's whereabouts.",
    "The resident considers the captain's worldwide search, then says the town has no particularly famous ruins.",
    "Another resident recognizes the captain and regrets that there are no notable ruins to suggest.",
)
BLOCKS = {(r, start + i): (r, start + i) for r, start in enumerate(FIRST_BLOCK) for i in range(len(SCENES))}
CONTEXT = {(r, start + i): note for r, start in enumerate(FIRST_BLOCK) for i, note in enumerate(SCENES)}
HISTORY = (
    ("rafael_B241_B260_final_review_v1", "rafael_B261_B280_final_review_v1"),
    ("hodram_B251_B280_final_review_v1",),
    ("lil_B243_B282_final_review_v1",),
    ("maria_B216_B252_final_review_v1",),
)
EDITS = {}


def align(scene, ids, text, phrases, note):
    for route, number in enumerate(ids):
        if number is not None:
            EDITS[route, FIRST_BLOCK[route] + scene, number] = (text, phrases, note)


align(0, (9, None, None, None), "It's this statue. There's something strange about it. I feel something like compassion coming from it...",
      ("this statue.", "something like compassion", "coming from it..."), "Rafael senses compassion before Cesare recognizes the figurehead. Preserve this as Rafael's impression.")
align(0, (None, 9, None, None), "Look at this statue. Do you feel it too? There's a strange warmth to it.",
      ("this statue.", "feel it too?", "a strange warmth"), "Hodram checks whether Cesare senses the same unusual warmth.")
align(0, (None, None, 9, None), "This statue feels strange. Can you feel the warmth coming from it?",
      ("feels strange.", "feel the warmth", "coming from it?"), "Lil senses a strange warmth and asks if Cesare feels it too.")
align(0, (None, None, None, 8), "Do you feel that warmth coming from this statue?",
      ("feel that warmth", "from this statue?"), "Maria asks whether Cesare can feel what she senses from the statue.")
align(0, (31, 26, 26, 25), "Oh, it's a figurehead! Look at all that detail. Yes, I can feel it, too.",
      ("it's a figurehead!", "all that detail.", "I can feel it, too."), "Cesare recognizes the nautical object, admires the workmanship and shares the captain's impression.")
align(0, (43, 37, 36, 36), "Never heard of it. Wait, do you mean to take it?",
      ("Never heard of it.", "to take it?"), "Cesare says he doesn't know its reputation and catches on to the captain's idea.")
align(0, (58, 53, 52, 51), "It's a magnificent figurehead. If we mounted it, it might bring us good fortune. But can we take it without asking?",
      ("a magnificent figurehead.", "bring us good fortune.", "without asking?"), "Cesare connects the hope of good fortune to mounting the figurehead. Preserve his question about permission.")
align(0, (66, 60, 59, 58), "How kind of you, Admiral! Let's move it, then!",
      ("How kind of you, Admiral!", "move it, then!"), "Cesare admires the captain's stated concern and eagerly moves to help.")
align(0, (70, 64, 63, 62), "Pardon us. Please come along, figurehead.",
      ("Pardon us.", "come along, figurehead."), "Cesare addresses the figurehead politely as if it can hear him. The protective voice follows.")
align(0, (79, None, None, None), "W-wait! Don't let go like that. It's dangerous!",
      ("Don't let go like that.", "It's dangerous!"), "Rafael reacts to Cesare suddenly taking his hands away and warns about the danger.")
align(0, (102, 92, 91, 90), "(Whose voice was that? It sounded so warm and kind...)",
      ("Whose voice was that?", "warm and kind..."), "The thought remains private. Cesare remembers the warmth and kindness without identifying the voice.")

align(1, (54, None, None, None), "I got it wrong! Let's get back to town for now!",
      ("I got it wrong!", "to town for now!"), "Rafael realizes his mistake and calls off the attempt for now.")
align(1, (95, None, None, None), "I got it wrong! Let's get back to town for now!",
      ("I got it wrong!", "to town for now!"), "The same wrong-answer reaction applies to the other incorrect stone.")
align(1, (None, 53, None, None), "Wrong answer. It's dangerous here. Back to town!",
      ("It's dangerous here.", "Back to town!"), "Hodram recognizes the mistake and gives a direct instruction to leave.")
align(1, (None, 90, None, None), "Wrong answer. It's dangerous here. Back to town!",
      ("It's dangerous here.", "Back to town!"), "The other wrong stone preserves Hodram's same warning and retreat.")
align(1, (None, None, 52, None), "Huh? That's odd... No time for that! Everyone, back to town!",
      ("No time for that!", "back to town!"), "Lil starts to question herself, then abandons the thought and gets the crew out.")
align(1, (None, None, 87, None), "Huh? That's odd... No time for that! Everyone, back to town!",
      ("No time for that!", "back to town!"), "The second wrong choice keeps the same reversal and retreat.")
align(1, (None, None, None, 52), "I got it wrong. We need to get out of here. Let's go back to town.",
      ("I got it wrong.", "Let's go back to town."), "Maria acknowledges her error and calls for the crew to return to town.")
align(1, (None, None, None, 89), "I got it wrong. We have to get out!",
      ("I got it wrong.", "have to get out!"), "This Maria branch calls for escape and has no separate line about returning to town.")
align(1, (None, None, 102, 104), "The water level should stay the same. It's the stone on the right!",
      ("The water level", "the same.", "on the right!"), "Keep the conclusion about the water level and make right unambiguously spatial.")
align(1, (None, None, 109, 110), "It's opening!", ("It's opening!",),
      "Fernando reacts as the wall begins to move. The animation shows which object opens.")
align(1, (137, None, None, 125), "Right here. It looks like a figurehead...",
      ("Right here.", "like a figurehead..."), "Fernando points out the object and compares it to a figurehead before the noise breaks in.")
align(1, (184, 174, None, 172), "What was that? We won't get cursed if we use it, will we?",
      ("What was that?", "use it, will we?"), "Fernando is uneasy and asks about a possible curse. Keep the tag attached and the concern tentative.")
align(1, (240, 226, 234, 225), "Huh? Ugh... My body feels so heavy.",
      ("My body feels so heavy.",), "Fernando notices heaviness after the crew runs. The line reports a sensation without identifying a curse.")

align(2, (10, 10, 10, 9), "Looking for ruins? There are some nearby.",
      ("Looking for ruins?", "some nearby."), "The resident recognizes the purpose of the visit and offers a local lead.")
align(2, (13, 13, 13, 12), "I don't usually tell visitors from abroad, but I'll tell you.",
      ("visitors from abroad,", "I'll tell you."), "The speaker ordinarily withholds the directions from people abroad and makes a personal exception.")
align(3, (None, 9, 9, 8), "Ruins all over the world? Hmm... There aren't any famous ones around here.",
      ("Ruins all over the world?", "famous ones around here."), "The resident repeats the worldwide scope, considers the question and says there are no famous local ruins.")
align(3, (9, None, None, None), "Ruins all over the world, you say? Hmm... I don't think there are any particularly famous ones around here.",
      ("all over the world,", "particularly famous"), "The resident considers the global search before saying that no particularly famous ruins come to mind.")
align(4, (10, 10, 10, 9), "Looking for ruins all over the world? I'm afraid there aren't any famous ones here.",
      ("all over the world?", "famous ones here."), "The answer regretfully distinguishes a lack of famous ruins from a lack of any ruins.")

RETENTIONS = {
    (1, 251, 56): "Hodram calls it sheer folly to leave the figurehead on land. The decisive tone belongs to his route.",
    (2, 250, 55): "Lil calls leaving such a figurehead on dry land a sin in a playful exaggeration.",
    (3, 220, 54): "Maria imagines that the figurehead itself would rather be at sea. The thought supports Cesare's next reply.",
    (0, 261, 114): "Rafael explains the unchanged water level in his own words before the wall opens.",
    (1, 252, 106): "Hodram states the unchanged level directly. His concise deduction works as written.",
    (0, 261, 148): "The disembodied voice asks whether the captain awakened it. Preserve the original FE speaker ambiguity.",
    (3, 221, 176): "Maria leaves Fernando's fear unresolved. The short answer is sufficient after his question.",
}
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



oral_collect = SCOPE["collect"]


def collect():
    release, ctx, inv, groups, errors = oral_collect()
    if errors:
        return release, ctx, inv, groups, errors
    painter = fe.native_painter(ctx)
    for route, start in enumerate(FIRST_BLOCK):
        rows = groups[route, start + 1][0]
        turns = (9, 12) if route != 3 else (8, 11)
        for turn, role in zip(turns, ("question", "directions"), strict=True):
            row, = (r for r in rows if r["source_reference"]["record_index"] == turn)
            fe.revise(row, role, painter, lambda body: ctx.execute(expand_fe, body))
    return release, ctx, inv, groups, errors


def validated_pages(ctx, edited):
    progressive = [r for r in edited if r["source_selector"] != 254]
    pictures = precedent.validate_native(ctx, progressive)
    for row in edited:
        if row["source_selector"] == 254:
            page, = row["after_native"]["pages"]
            pictures.append((f"SC{row['route']} {row['id'].split('_B')[1]} FE",
                             bytes.fromhex(page["native_plane_hex"])))
    return pictures


SCOPE["collect"] = collect
SCOPE["validate_native"] = validated_pages

if __name__ == "__main__":
    SCOPE["main"]()
