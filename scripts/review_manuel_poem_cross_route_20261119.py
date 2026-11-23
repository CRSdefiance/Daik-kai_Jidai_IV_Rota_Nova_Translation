"""Review Manuel's shared poem and each captain's complete aftermath scene."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as source_workflow
from scripts import register_rafael_contract_and_proof_20261119 as parent
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = source_workflow.base, source_workflow.native, source_workflow.stage
TOKEN, logical = workflow.TOKEN, workflow.logical
ROOT = Path("work/manuel_poem_cross_route_20261119")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v2.json"
BLOCKS = ((25,), (16,), (11,), (18,))
paired = SimpleNamespace(parent=parent, base=base, native=native, stage=stage, ROOT=ROOT, SOURCE=SOURCE, BLOCKS=BLOCKS)
SOURCE_TURNS = (
    "Manuel grieves the people lost and quietly describes their return to the mother sea.",
    "Manuel asks them to comfort the spirits of those who died.",
    "Manuel begins the poem with the resemblance between the sea and a mother. Familiar ripples seem to recall a mother's distant heartbeat.",
    "The refrain recurs. Manuel has heard that in some lands the two may be written and pronounced alike.",
    "The final refrain leads into the lasting ties that connect us to both sea and mother throughout life.",
    "Manuel says the sea accepts everything and hopes they can do the same.",
)
NOTES = (
    "Keep Manuel's gentle self-correction and the personified sea. The Japanese supplies no quantity of lives lost.",
    "Use the established invitation to pay respects and keep the turn from celebration to mourning.",
    "Use the registered verse and keep the opening quotation, the refrain and the heartbeat image on one page.",
    "Use the same refrain and the tentative report about both the written and spoken resemblance.",
    "Use the same closing stanza and retain the quotation's closing mark after the enduring bond.",
    "Return from the poem to the same quiet wish. The next response remains silence.",
)
VERSE_LINES = (
    "Lives lost at sea... No, perhaps I should say they've returned to Mother Sea...",
    "Let's pay our respects to those lost at sea.",
    "\"The sea and a mother are alike. The lapping waves sound strangely familiar, like the distant echo of a mother's heartbeat.",
    "The sea and a mother are alike. In some lands, they say, both may be written and spoken the same way.",
    "The sea and a mother are alike. Each holds us in a bond that cannot fade for as long as we live.\"",
    "...The sea welcomes everything. I hope we can do the same.",
)
PROTECTED = (
    ("perhaps I should say", "Mother Sea..."), (), ("like the distant echo", "a mother's heartbeat."),
    (), ("as long as we live.",), (),
)
MANUEL = ((16, 25, 33, 36, 40, 52), (17, 25, 32, 35, 39, 49),
          (29, 37, 44, 47, 51, 76), (21, 29, 36, 39, 43, 75))
EDITS = {
    (0, 25, 16): (VERSE_LINES[0], PROTECTED[0]),
    (2, 11, 54): ("Wait, what's gotten into you? Why the sudden poetry?", ("Why the sudden poetry?",)),
    (2, 11, 66): ("Oh, FI... You have no sense of wonder. I thought it was beautiful. It really moved me.",
                   ("no sense of wonder.", "It really moved me.")),
    (3, 18, 49): ("What a surprise. I thought all you cared about was ships.", ("all you cared about was ships.",)),
    (3, 18, 64): ("Ha ha! We won! Time for a victory feast! Woo-hoo!", ("a victory feast!",)),
    (3, 18, 68): ("Well, there's one exception...", ()),
}
for route in range(1, 4):
    for idx, pair in zip(MANUEL[route], zip(VERSE_LINES, PROTECTED, strict=True), strict=True):
        EDITS[route, BLOCKS[route][0], idx] = pair


RESPONSES = (
    {
        7: ("Rafael confirms the victory.", "The plain statement sets up Clau's boast."),
        12: ("Clau laughs and says the victory was easy.", "The short boast suits Clau before Manuel shifts the mood."),
        20: ("Rafael addresses Manuel, puzzled.", "His hesitation gives Manuel room to continue."),
        28: ("Rafael is confused by the invitation.", "The original question marks remain a silent reaction."),
        43: ("Rafael admires the poem and asks if he might set it to music.", "Keep the unprompted compliment and the request for permission."),
        48: ("Clau agrees and admits he thought Manuel was only an older man who liked ships.", "His backhanded praise lands before the earnest close."),
        55: ("Rafael is silent.", "The pause lets Manuel's wish stand."),
    }, {
        6: ("The companion confirms their victory.", "The concise report lets Hodram give it his own meaning."),
        10: ("Hodram says victory is expected if they aim to build the strongest fleet.", "Keep his deliberately demanding answer."),
        13: ("The companion observes that Hodram is as strict as ever.", "Retain the understated reaction to Hodram's own standard."),
        21: ("Hodram says Manuel's name.", "A bare name fits the interruption of the victory talk."),
        28: ("Hodram is puzzled.", "The short question makes room for the verse."),
        42: ("Hodram compliments the poem and admits Manuel's talent surprised him.", "Keep the unusually open praise in his restrained voice."),
        45: ("The companion agrees that he is impressed.", "The brief assent keeps the focus on Manuel."),
        52: ("Hodram is silent.", "The pause carries the weight of Manuel's wish."),
    }, {
        6: ("Lil celebrates their victory.", "The exclamation conveys her enthusiasm."),
        18: ("Camille praises how well Lil now commands naval battles.", "The compliment follows the victory and still addresses Lil with the original name substitution."),
        22: ("Lil credits her own ability.", "The playful boast suits her answer to Camille."),
        33: ("Lil addresses Manuel, puzzled.", "The hesitant name is enough to mark the change in tone."),
        40: ("Lil is confused by Manuel's invitation.", "Retain the original questioning silence before his recitation."),
        54: ("Lil wonders what got into Manuel and why he suddenly started reciting poetry.", "Her direct two questions set up Camille's teasing without making her cruel."),
        66: ("Camille chides Lil for lacking a sense of romance or wonder and says the poem moved him.", "The teasing is about her reaction to poetry. Preserve the form of address and genuine appreciation."),
        70: ("Lil sarcastically concedes that she does not appreciate poetry.", "The mock apology answers Camille's teasing."),
        79: ("Lil is silent.", "The pause gives the closing reflection room."),
    }, {
        5: ("Maria acknowledges the victory.", "A measured success suits her exchange with Xien."),
        9: ("Xien says she has become proficient at commanding the fleet in battle.", "His succinct praise leaves space for Maria to credit him."),
        13: ("Maria gives Xien the credit.", "The short acknowledgment keeps the relationship as established."),
        17: ("Xien laughs off the credit and says he has almost nothing left to teach her.", "Keep the warmth and the qualification."),
        25: ("Maria says Manuel's name.", "The bare name lets the solemn observation settle."),
        32: ("Maria is puzzled.", "The brief unspoken question fits immediately before the poem."),
        46: ("Xien is surprised that Manuel recites poetry.", "The clipped surprise fits Xien before Maria responds."),
        49: ("Maria is surprised and says she thought Manuel only cared about ships.", "Keep the admission in her voice and carry the thought across a readable line break."),
        53: ("Xien tells Maria that every man of the sea has a romantic or poetic streak.", "A little poetry in his heart keeps the playful claim tied to the actual recitation."),
        64: ("A companion cheers the victory and calls for a celebratory feast.", "Keep the exuberance that sets up Xien's immediate exception."),
        68: ("Xien calls that companion an exception.", "The dry line answers the shout and lands the joke."),
        78: ("Maria says nothing.", "Let Manuel's closing wish remain the last thought."),
    },
)


def main():
    packet = base.load(SOURCE)
    groups = packet["groups"]
    assert len(groups) == 4 and sum(len(g["records"]) for g in groups) == 60
    baseline = None
    exchanges = {}
    for group in groups:
        route, number = group["route"], group["block"]
        assert number == BLOCKS[route][0]
        selected = {n: (meaning, reason) for n, meaning, reason in zip(MANUEL[route], SOURCE_TURNS, NOTES, strict=True)}
        actual = [r["source_body_hex"] for r in group["records"] if r["selector"] == 23]
        assert len(actual) == 6
        assert baseline is None or baseline == actual
        baseline = actual
        notes = selected | RESPONSES[route]
        assert set(notes) == {r["source_record_index"] for r in group["records"]}
        exchanges[route, number] = (0, "\n".join("|".join(notes[r["source_record_index"]]) for r in group["records"]))
    implementation = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n'
            '                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=group["context"], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | {"exchanges": exchanges}
    exec(compile(implementation, __file__ + "::parallel-verse-and-route-responses", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
