"""Keep nine flagged story phrases intact through the existing dialogue formatter."""

from inspect import getsource
from pathlib import Path

from scripts import register_palace_and_village_exchanges_20261115 as parent
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

native, base = precedent.native, precedent.base
ROOT = Path("work/story_phrase_wraps_20261118_v1")
ROM = ROOT / "Story_Phrase_Wraps_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("story_phrase_wraps_20261118_v1.json")

# Each key names the route, block and clean-source record index.
EDITS = {
    (0, 48, 406): (None, ("heard a rumor", "Proof of Conquest", "southern Africa."),
                   "Hans passes on a recent rumor about a map taken to southern Africa. Keep the title together."),
    (0, 79, 22): ("This must be another map to a Proof of Conquest. The Mediterranean treasure is some kind of crown, if I recall...", ("Proof of Conquest.", "some kind of crown,", "if I recall..."),
                  "The map identification and the tentative recollection about a crown are separate beats."),
    (1, 81, 13): (None, ("Indian Ocean's", "Proof of Conquest"),
                  "The question concerns the legend's appearance in the Black Sea. Keep the two regions distinct."),
    (1, 146, 5): (None, ("Evergreen Lotus Leaf", "Indian Ocean's", "Proof of Conquest"),
                  "Hodram is certain the leaf is the map. His doubt concerns using it with the platter."),
    (2, 213, 72): (None, ("Shandong Peninsula.", "the emperor's greatsword"),
                   "The elder's directions and expectation about the greatsword stay intact."),
    (3, 53, 6): ("We have all the Proofs of Conquest...", ("Proofs of Conquest...",),
                 "The complete collection is acknowledged before the crew wonders why nothing happened."),
    (3, 54, 12): ("We have all the Proofs of Conquest...", ("Proofs of Conquest...",),
                  "The parallel opening keeps the identical wording and complete title."),
    (3, 112, 4): ("What's the map to the Proof of Conquest in Southeast Asia?", ("Southeast Asia?", "Proof of Conquest"),
                  "Maria is asking which object serves as the map, before Xien suggests the coin."),
    (3, 130, 100): (None, ("trade house", "tomorrow morning?", "make up for today."),
                    "Carlo proposes going together the next morning and says he thinks he can make amends."),
}
OFFSETS = dict(zip(EDITS, (4363, 175, 59, 17, 1021, 17, 33, 13, 1285), strict=True))
BLOCKS = {(route, block): (route, block) for route, block, _ in EDITS}
HISTORY = (
    ("rafael_B48_contextual_final_review_v1", "rafael_B61_B80_contextual_final_review_v1"),
    ("hodram_B81_B89_contextual_final_review_v1", "hodram_B131_B150_contextual_final_review_v1"),
    ("lil_B213_contextual_final_review_v1",),
    ("maria_B51_B57_final_review_v1", "maria_B96_B124_final_review_v1", "maria_B125_B136_final_review_v1"),
)
CONTEXT = {
    (0, 48): "The crew discusses the Proofs and Rafael resolves to find them. Hans hears their ambitions, gives them a lead in southern Africa, and joins them as naturalist.",
    (0, 79): "The Mediterranean reward looks like another clue. The crew recalls a crown, while Rafael notices the patterns don't look like a map.",
    (1, 81): "Hodram's group visits Sera's homeland. The distant legend puzzles the crew before the discussion turns to the town's defenses.",
    (1, 146): "The crew works out how the Evergreen Lotus Leaf and Kushan Platter reveal the map to the Indian Ocean's Proof.",
    (2, 213): "The old man interprets the prophecy and tells Lil where to search for the emperor's greatsword.",
    (3, 53): "Maria and her crew have gathered the Proofs and debate why nothing has happened.",
    (3, 54): "The parallel collection scene begins with Maria acknowledging that the crew now has every Proof.",
    (3, 112): "Maria and Xien experiment with the Ancient Kingdom Coin and the Lotion Jar to reveal the map.",
    (3, 130): "Carlo offers to make up for the day's events by going to the trade house with Maria the next morning.",
}
SCOPE = vars(precedent) | globals() | {"RETENTIONS": {}}
exec(compile(getsource(precedent.historical), __file__ + "::history", "exec"), SCOPE)
exchange_source = checked_text(getsource(precedent.review_exchange), {
    '        if edit:': '        if edit:\n            assert current["offset"] == OFFSETS[route, block, number]',
})
exec(compile(exchange_source, __file__ + "::exact-exchanges", "exec"), SCOPE)
collect_source = checked_text(getsource(precedent.collect), {
    '        for group, blocks in BLOCKS.items():\n            n = blocks[route]':
        '        for group, (owner, n) in BLOCKS.items():\n            if owner != route:\n                continue',
})
exec(compile(collect_source, __file__ + "::current-input", "exec"), SCOPE)
main_source = checked_text(getsource(precedent.main), {
    '    assert len(groups) == 20': '    assert len(groups) == len(EDITS) == len(edited)',
})
exec(compile(main_source, __file__ + "::validated-output", "exec"), SCOPE)

if __name__ == "__main__":
    SCOPE["main"]()
