"""Review the four consecutive crew item rumors in every storyline."""

from inspect import getsource
from pathlib import Path

from scripts import register_proof_of_conquest_terms_20261118 as parent
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

native, base = precedent.native, precedent.base
ROOT = Path("work/crew_item_rumors_20261118_v1")
ROM = ROOT / "Crew_Item_Rumors_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("crew_item_rumors_20261118_v1.json")
FIRST_BLOCK = (240, 231, 228, 201)
SCENES = (
    "Samwell introduces the armadillo and its supposedly iron-hard hide. The captain recognizes the shield's usefulness, then tempers Samwell's excitement when the lead proves vague.",
    "Samwell pitches a shield made from a giant tortoise shell. The captain catches him repeating his armadillo pitch, then agrees to remember the Indian Ocean lead despite its vagueness.",
    "The captain predicts Samwell's third pitch. This time he has done his own research and offers Britain as a more specific lead. The captain acknowledges his effort. Maria also compares the phoenix with China's Vermilion Bird.",
    "The crew member describes an ancient medical book and reports a possible treatment for fatigue at sea. The captain shows interest, asks for leads and reassures the speaker when the location is uncertain.",
)
BLOCKS = {(r, start + i): (r, start + i) for r, start in enumerate(FIRST_BLOCK) for i in range(len(SCENES))}
CONTEXT = {(r, start + i): note for r, start in enumerate(FIRST_BLOCK) for i, note in enumerate(SCENES)}
HISTORY = (
    ("rafael_B221_B240_final_review_v1", "rafael_B241_B260_final_review_v1"),
    ("hodram_B231_B250_final_review_v1",),
    tuple(f"lil_B{block}_contextual_final_review_v1" for block in range(228, 232)),
    ("maria_B196_B215_final_review_v1",),
)
ARMADILLO_INTRO = ("I just heard about armadillos. Have you heard of them? They say their hides are harder than iron.",
                  ("heard of them?", "harder than iron."),
                  "Samwell passes on a story he just heard and checks whether the captain knows the animal. The hardness remains hearsay.")
TORTOISE_INTRO = ("I just heard a rumor about a giant tortoise. Ever heard of one? They say its shell is harder than iron.",
                  ("giant tortoise.", "Ever heard of one?", "harder than iron."),
                  "Keep the singular animal, the conversational question, and the hearsay about its shell.")
ARMADILLO_SHIELD = (None, ("from its hide", "They called", "Armadillo Hide."),
                    "The official shield name stays intact. Carry its introduction over from the armadillo's unusual hide without breaking the naming clause.")
TORTOISE_SHIELD = ("They say someone made a shield from its shell. Everyone called it the Giant Tortoise Shield.",
                   ("from its shell.", "Giant Tortoise Shield."),
                   "Keep the shield's origin as rumor and keep the complete item name together.")
PHOENIX_HELMET = ("I heard of a helmet made from iron forged in a phoenix's flames. I think they called it the Phoenix Bascinet.",
                  ("a phoenix's flames.", "Phoenix Bascinet."),
                  "The flames forged the iron used for the helmet. Samwell remains tentative about the name, which fits on one line.")
HEROPHILUS_GREETING = ("Heard of Herophilus, Admiral?", ("Heard of Herophilus, Admiral?",),
                       "A short spoken question fits on one line, keeps the respectful address and sets up the captain's reply.")
FATIGUE = ("They say the book explains how to keep a crew from getting so tired...",
           ("a crew", "getting so tired..."),
           "Keep the report tentative and say plainly what the book may teach about fatigue at sea.")
EDITS = {
    (0, 240, 14): ARMADILLO_INTRO,
    (0, 240, 23): ARMADILLO_SHIELD,
    (0, 240, 37): (None, ("All I know", "hidden somewhere", "around Africa."), "Samwell has a single vague lead. Keep the qualification and region together across the wrap."),
    (0, 241, 14): TORTOISE_INTRO,
    (0, 241, 22): (None, ("its shell.", "Giant Tortoise Shield."), "The existing wording carries the origin and name. Avoid a mid-phrase break."),
    (0, 242, 14): ("Admiral, are phoenixes really real?", ("phoenixes really real?",), "Samwell asks a childlike, earnest question before Rafael wonders what brought it on."),
    (0, 242, 18): ("I don't know. If they're real, I'd love to see one. What brought that on?", ("If they're real,", "love to see one.", "What brought that on?"), "Rafael's curiosity prompts a separate question. Both the uncertainty and the wish to see one stay intact."),
    (0, 242, 23): PHOENIX_HELMET,
    (0, 242, 26): ("Let me guess. You want to find it because it'd help us in a fight?", ("Let me guess.", "in a fight?"), "Rafael is getting ahead of the same sales pitch. Frame the prediction as a wry question."),
    (0, 242, 55): ("Ahem! I did some digging on my own. At first, my only lead was northern Europe.", ("on my own.", "northern Europe."), "Keep Samwell's pride and the improvement from a vague region to Britain. Restore the missing subject."),
    (0, 242, 68): (None, ("all your hard work,", "Phoenix Bascinet."), "Rafael recognizes Samwell's effort and promises to remember the helmet. Preserve the item title."),
    (0, 243, 5): HEROPHILUS_GREETING,
    (0, 243, 13): ("Herophilus was an ancient physician. He wrote the world's oldest medical book.", ("ancient physician.", "oldest medical book."), "The speaker credits the ancient physician with writing the book. Remove the break between the parts of a verb."),
    (0, 243, 37): (None, ("a long time ago,", "far reaches", "the Mediterranean."), "Keep the age and uncertain recollection of the sighting. Carry the geographic phrase across the wrap intact where possible."),
    (1, 231, 13): ARMADILLO_INTRO,
    (1, 231, 21): ARMADILLO_SHIELD,
    (1, 231, 28): ("Oh, come on! It's harder than iron! Don't you want it? Think how handy it would be in a fight.", ("harder than iron!", "in a fight."), "Samwell is teasing the captain and making the practical case for taking an interest. Remove the break before the main verb."),
    (1, 231, 31): ("True. Where can we find it?", ("Where can we find it?",), "Hodram acknowledges the point and asks for a location in his direct voice."),
    (1, 231, 34): ("All I know is it's hidden somewhere around Africa.", ("somewhere", "around Africa."), "The source describes an approximate area. Hold back the certainty that prompted Hodram's skeptical reply."),
    (1, 232, 13): TORTOISE_INTRO,
    (1, 232, 20): TORTOISE_SHIELD,
    (1, 232, 34): ("Don't you want it? Think how handy it'd be in a fight.", ("Don't you want it?", "in a fight."), "Echo Samwell's armadillo pitch so Hodram's next line makes sense without splitting the main verb."),
    (1, 232, 45): ("...Where can we find it?", ("Where can we find it?",), "Keep the pause as Hodram lets the argument go and asks for a location."),
    (1, 233, 21): PHOENIX_HELMET,
    (1, 233, 49): ("Ahem! I did some digging myself. At first, all I knew was that it was somewhere in northern Europe.", ("some digging myself.", "northern Europe."), "Keep Samwell's proud throat-clearing and the regional comparison with Britain."),
    (1, 233, 61): ("You put in the work, Samwell. I'll keep the Phoenix Bascinet in mind.", ("put in the work,", "Phoenix Bascinet"), "Hodram gives Samwell credit in a direct voice and promises to remember the helmet."),
    (1, 234, 5): HEROPHILUS_GREETING,
    (1, 234, 20): FATIGUE,
    (1, 234, 43): ("That's all.", (), "The speaker only recalls one clue and confirms that before Hodram reassures him."),
    (2, 228, 13): ARMADILLO_INTRO,
    (2, 228, 28): ("Come on, keep up! It's harder than iron! Don't you want one? Think how handy it'd be in a fight.", ("harder than iron!", "in a fight."), "Keep Samwell's teasing impatience without making the crew's joke sound hostile."),
    (2, 229, 13): TORTOISE_INTRO,
    (2, 229, 20): TORTOISE_SHIELD,
    (2, 230, 13): ("Admiral, are phoenixes really real?", ("phoenixes really real?",), "Keep the earnest question and address together before Lil's curious response."),
    (2, 230, 21): PHOENIX_HELMET,
    (2, 231, 5): HEROPHILUS_GREETING,
    (2, 231, 20): ("They say the book shows how to keep a crew from tiring so fast...", ("a crew", "tiring so fast..."), "Keep the modest claim about managing sailors' fatigue and the speaker's uncertainty."),
    (2, 231, 62): ("If we want that book, we'll have to look in the Mediterranean.", ("we'll have to", "the Mediterranean."), "Lil draws the same practical conclusion. Keep the verb phrase together."),
    (3, 201, 12): ARMADILLO_INTRO,
    (3, 201, 20): ARMADILLO_SHIELD,
    (3, 201, 44): ("I'll keep it in mind. With luck, we'll find it.", ("keep it in mind.", "we'll find it."), "Maria personally agrees to keep the lead in mind and speaks for the group in the hope of finding it."),
    (3, 202, 12): TORTOISE_INTRO,
    (3, 202, 19): TORTOISE_SHIELD,
    (3, 202, 37): ("There it is again. That's exactly what you said about the armadillo.", ("There it is again.", "about the armadillo."), "Maria confirms the repetition. Preserve the callback without doubling emphasis."),
    (3, 202, 58): ("I'll keep it in mind. With luck, we'll find it.", ("keep it in mind.", "we'll find it."), "Maria echoes her earlier answer, keeping the light pattern and her own commitment."),
    (3, 203, 12): ("Admiral, are phoenixes really real?", ("phoenixes really real?",), "Keep Samwell's earnest question on one line before Maria makes her cultural comparison."),
    (3, 203, 20): PHOENIX_HELMET,
    (3, 203, 44): ("Oh? That narrows it down.", ("narrows it down.",), "Maria is surprised Britain is a more useful lead. Use the spoken idiom."),
    (3, 203, 47): ("Ahem! I did some digging myself. At first, all I knew was that it was somewhere in northern Europe.", ("some digging myself.", "northern Europe."), "Keep Samwell's proud introduction and preserve the discovery that this was originally a broader lead."),
    (3, 203, 59): ("You went to all that trouble, Samwell. I'll keep the Phoenix Bascinet in mind.", ("all that trouble,", "Phoenix Bascinet"), "Maria appreciates the effort and promises to remember the helmet by name."),
    (3, 204, 4): HEROPHILUS_GREETING,
    (3, 204, 11): ("He was an ancient physician who wrote the world's oldest medical book.", ("ancient physician", "oldest medical book."), "The response introduces the man and his distinction. His name is already the subject of the question."),
    (3, 204, 19): FATIGUE,
    (3, 204, 45): ("Oh... That's not much to go on.", ("not much to go on.",), "Maria gives the speaker a sympathetic acknowledgment before explaining the difficulty."),
}
# Verify and retain these distinctive responses in the complete exchanges.
RETENTIONS = {
    (0, 241, 25): "Rafael recognizes Samwell's repeat performance and recalls the earlier shield imprecisely as the armadillo thing. The hesitation and plain phrasing work.",
    (1, 231, 38): "Hodram's dry reaction communicates how little the large region helps and gives Samwell room to concede the point.",
    (1, 232, 51): "The repeated dry reply makes the same joke land when the new region still gives no practical place to start.",
    (1, 234, 39): "Hodram's clipped follow-up asks for any additional clue. The speaker immediately confirms there is just the one.",
    (2, 230, 54): "Lil's exuberant praise answers Samwell's proud announcement. The deliberate sentence beat builds enthusiasm.",
    (3, 203, 16): "Maria compares the phoenix to China's Vermilion Bird, hopes to see a phoenix and asks about the sudden question. Preserve her cultural reference and her particular response.",
    (3, 204, 33): "The source gives a very old, half-remembered report of someone seeing the book deep in the Mediterranean. The current wording preserves this double uncertainty.",
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


if __name__ == "__main__":
    SCOPE["main"]()
