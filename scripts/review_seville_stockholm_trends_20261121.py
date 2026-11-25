"""Pair and review the two complete town exchanges on every route."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_final_early_wrap_leads_20261121 as parent
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text


base = workflow.base
ROOT = Path("work/seville_stockholm_trends_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/seville_stockholm_trends_review_20261121_v3.json")
BLOCKS = ((188, 197), (180, 189), (176, 185), (149, 158))
PLACE = (
    "The shop owner predicts a banana craze in Seville. The cook questions her enthusiasm, asks for instructions "
    "and then answers her order with a flat aside before the owner declares the age of bananas.",
    "Two people talk about a spell of cold weather. The woman longs for a fur coat, the man relays reports of "
    "sales and rising prices, and she repeats her wish after he hopes for warmer weather. A forecast follows.",
)
CONTEXT = ("Two separate town trend scenes, one for bananas in Seville and one for furs in Stockholm.",) * 4
MEANINGS = (
    (
        ("The owner repeats the name of the fruit and announces that the coming age belongs to bananas.",
         "The repeated name and emphatic forecast establish the owner's comic certainty."),
        ("The cook repeats the unfamiliar choice as a polite question.",
         "The simple echo gives the owner room to explain her certainty."),
        ("The owner confirms and says the taste makes bananas sure to catch on.",
         "The reason is how good they taste. Keep the prediction in the owner's voice."),
        ("The cook is still unconvinced and asks whether she really thinks so.",
         "The short, doubtful reply leaves the owner room to insist."),
        ("The owner insists they will catch on because she says they will.",
         "The repeated prediction delivers the joke about her supposed authority."),
        ("The cook formally acknowledges the answer, then asks what to do.",
         "The practical question follows the polite acknowledgment and sets up the buying order."),
        ("The owner orders the cook to go and buy as many bananas as possible.",
         "The order clearly sets the objective and leaves the available quantity open."),
        ("The cook answers with a repeated and noticeably less polite acknowledgment.",
         "The double acknowledgment is the cook's dry answer after his earlier courtesy."),
        ("The owner declares that the age of bananas has begun and laughs ostentatiously.",
         "The grand claim and theatrical laugh deliver the owner's final flourish."),
        ("The system predicts that bananas may become fashionable in Seville.",
         "The notice keeps the forecast tentative and names the trade good and town."),
    ),
    (
        ("The woman complains twice that it is cold, intensifying the complaint the second time.",
         "The repeated emphasis sounds like a spontaneous reaction to the cold."),
        ("The man agrees that it has been a long time since the weather was this cold.",
         "The reply confirms her impression and recalls the last equally cold spell."),
        ("The woman says she wants a fur coat and feels as though she might freeze.",
         "The wish and the freezing remark are both hers and belong in the same turn."),
        ("The man relays a report that the cold is making furs sell well and prices rise.",
         "Keep the hearsay, the effect on sales and the rising price clear in one spoken turn."),
        ("The woman acknowledges the report and complains about the cold again.",
         "The acknowledgment and shiver keep her attention on the weather."),
        ("The man hopes it will warm up soon.",
         "A plain wish for warmth fits his response and lets her return to the coat."),
        ("The woman agrees but still wants a fur coat for as long as the weather stays cold.",
         "The repeated wish, explicitly tied to the present cold, closes their conversation."),
        ("The system forecasts that furs may become fashionable in Stockholm.",
         "The notice gives the trade good, town and prospective trend."),
    ),
)

BANANAS_OPEN = ("Bananas! Bananas are the future!", ())
BANANAS_TASTE = ("Yes! With a taste like that, they're bound to catch on.",
                ("With a taste like that,", "bound to catch on."))
BANANAS_CERTAINTY = ("I do! If I say they'll catch on, they'll catch on!",
                     ("If I say they'll catch on,", "they'll catch on!"))
BANANAS_CLOSE = ("The age of bananas begins! Ohohoho!", ("The age of bananas begins!",))
BANANAS_NOTICE = ("Bananas may catch on in Seville.", ())
FURS_REPORT = ("Furs are selling well in this cold, and prices are going up, I hear.",
               ("Furs are selling well in this cold,", "and prices are going up, I hear."))
FURS_NOTICE = ("Furs may catch on in Stockholm.", ())
CHANGES = {
    (0, 0, 0): BANANAS_OPEN,
    (0, 0, 2): ("Of course! They taste so good, they're bound to catch on.",
                ("They taste so good,", "they're bound to catch on.")),
    (1, 0, 2): BANANAS_TASTE,
    (1, 0, 4): BANANAS_CERTAINTY,
    (1, 0, 9): BANANAS_NOTICE,
    (2, 0, 4): BANANAS_CERTAINTY,
    (2, 0, 8): BANANAS_CLOSE,
    (3, 0, 0): BANANAS_OPEN,
    (3, 0, 2): BANANAS_TASTE,
    (3, 0, 4): BANANAS_CERTAINTY,
    (3, 0, 5): ("Understood. What should I do?", ()),
    (3, 0, 7): ("Yeah, yeah.", ()),
    (3, 0, 8): BANANAS_CLOSE,
    (3, 0, 9): BANANAS_NOTICE,
    (0, 1, 1): (None, ("since it was this cold.",)),
    (0, 1, 2): (None, ("I'm going to freeze",)),
    (0, 1, 3): FURS_REPORT,
    (1, 1, 3): FURS_REPORT,
    (1, 1, 5): ("I hope it warms up soon.", ()),
    (1, 1, 6): ("I hope so. Till then, I still want a fur coat.", ("I still want a fur coat.",)),
    (1, 1, 7): FURS_NOTICE,
    (2, 1, 3): FURS_REPORT,
    (2, 1, 7): FURS_NOTICE,
    (3, 1, 2): (None, ("I'll freeze in this weather.",)),
    (3, 1, 3): FURS_REPORT,
    (3, 1, 7): FURS_NOTICE,
}


def main():
    if not SOURCE.exists():
        FunctionType(paired.main.__code__, vars(paired) | globals())()

    source = base.load(SOURCE)
    groups = source["groups"]
    assert len(groups) == 8
    originals = {}
    edits, exchanges, contexts = {}, {}, {}
    for group in groups:
        route, block = group["route"], group["block"]
        scene = BLOCKS[route].index(block)
        turns = group["records"]
        assert len(turns) == len(MEANINGS[scene])
        signatures = [(r["selector"], workflow.logical(r["Japanese"])) for r in turns]
        assert signatures == originals.setdefault(scene, signatures)
        assert signatures[-1][0] == 254
        contexts[route, block] = PLACE[scene]
        exchanges[route, block] = (0, "\n".join("|".join(notes) for notes in MEANINGS[scene]))
        for i, turn in enumerate(turns):
            change = CHANGES.get((route, scene, i))
            if change:
                edits[route, block, turn["source_record_index"]] = change
    assert len(edits) == len(CHANGES)
    program = checked_text(getsource(workflow.main), {
        "        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)":
            "        excerpts = (exchanges[route, block],)",
        "            for raw, note in zip(raw_rows, notes, strict=True):":
            '            for raw, note in zip(raw_rows, notes, strict=True):\n'
            '                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=contexts[route, block], source_meaning=meaning, localization_note=reason,',
    })
    env = vars(workflow) | globals() | dict(exchanges=exchanges, contexts=contexts, EDITS=edits)
    exec(compile(program, __file__ + "::complete-town-review", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    main()
