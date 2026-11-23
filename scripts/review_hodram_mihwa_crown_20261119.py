"""Bind Julian's request for the crown to the Hangzhou bartender's name."""
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_story_market_terms_20261119 as parent
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = pairing.base, pairing.native, pairing.stage
ROOT = Path("work/hodram_mihwa_crown_20261119_v1")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
NAMES = Path("work/actor_display_names_20261119_v1/current_actor_getters.json")
BINDINGS = ROOT / "mihwa_name_binding.json"
BLOCKS = ((), (89,), (), ())
CONTEXT = ("", "Hodram followed Julian's lead from a Hangzhou tavern and found the Silla Gold Crown first. Julian meant it as a gift for Mihwa. He begs to take it. Hodram gives it up and permits Julian to say he found it. Gerhard tries to introduce Hodram after Julian has already gone.", "", "")
paired = SimpleNamespace(base=base, native=native, stage=stage, parent=parent, ROOT=ROOT, SOURCE=SOURCE, BLOCKS=BLOCKS)
NOTES = """11|Gerhard recognizes the Silla Gold Crown.|Match the item card while keeping his awe at seeing it.|Ah, so this is the Silla Gold Crown...
15|Hodram senses both the crown's imposing presence and its dignity.|Keep the two qualities in the order he notices them and use spoken English.|It's imposing... but graceful, too.
19|Gerhard understands why anybody would want the crown, even men.|The existing phrasing follows his admiration and admits its wider appeal.|
24|Julian notices what Hodram holds.|Keep the startled stammer and the unfinished recognition.|
28|Hodram recalls Julian's name and says Julian left first but arrived a little late.|Keep Hodram's dry observation after Julian realizes what has happened.|
32|Julian asks who Hodram is and whether they've met.|Both questions fit Julian's surprise when addressed by name.|
35|Hodram gives his name and says he heard Julian discuss the crown at the tavern in Hangzhou.|Preserve the live name and location and match the item card.|I'm FI. I heard you talking about the Silla Gold Crown at the tavern in Hangzhou.
39|The talk made Hodram interested enough to come find the crown himself.|Keep what piqued Hodram's interest and match the item card.|You piqued my interest. I came all this way to look for the Silla Gold Crown myself.
43|Julian is distressed because the crown was meant as a gift for her.|Restore the startled stammer and keep the recipient implicit until Julian names her.|Th-that's not fair... I meant to give it to her.
47|Hodram pauses.|The silent reaction leaves space for Julian to press his case.|
51|Julian fears embarrassment and cannot face Mihwa. He asks Hodram to let him have the crown.|Use Mihwa, the Hangzhou bartender's installed name. Keep Julian's embarrassment, rising urgency and courteous request.|I'll look like a fool! How can I face Mihwa now? Please, could you let me have it?
55|Gerhard asks what Hodram will do.|The brief question puts the decision back with Hodram.|
59|Hodram agrees after a pause.|The terse assent suits his reserved response.|
63|Julian is surprised and checks that he means it.|The one-word question captures disbelief.|
67|Hodram gives away the crown because his sailors cannot use it and lets Julian claim to have found it.|Keep the permission explicit and make his dismissal of a treasure sound conversational.|Take it. We're sailors. We've no use for it, and I'd hate to see it gather dust. You can say you found it yourself.
70|Julian praises Hodram, promises to repay him and rushes off.|His renewed enthusiasm and quick goodbye fit the abrupt exit.|
77|Gerhard starts to identify Hodram by his company.|Keep the interrupted introduction and original runtime company name.|
80|Hodram notices Julian has left and would like to talk more if they meet again.|The existing line leaves the future encounter open and shows his interest.|"""


def bind_name():
    receipt = base.load(NAMES)
    assert receipt["runtime"]["candidate_sha256"] == base.digest(parent.ROM)
    actor = receipt["records"][201]
    source_field = actor["clean_source_fields"][0]["clean"]
    assert source_field["text"] == "美華"
    assert [r["text"] for r in actor["current_consumers"]] == ["Mihwa", "Mihwa"]
    clean = base.NdsImage.open(native.CLEAN)
    current = base.NdsImage.open(parent.ROM)
    names = []
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        before, after = (image.read_file(path) for image in (clean, current))
        banks = [native.IlnkContainer.parse(raw).blocks for raw in (before, after)]
        for block, (jp, en) in enumerate(zip(*banks, strict=True)):
            mentions = jp.count(bytes.fromhex(source_field["hex"]))
            if mentions:
                installed = [term for term in (b"Mihwa", b"Meihua") if term in en]
                assert len(installed) == 1 and en.count(installed[0]) == mentions
                names.append(dict(file_path=path, block=block, source_mentions=mentions,
                                  current_name=installed[0].decode("ascii"), source_block_sha256=native.digest(jp),
                                  current_block_sha256=native.digest(en)))
    assert [(x["file_path"], x["block"]) for x in names if x["current_name"] == "Meihua"] == [("/data/SC1.DK4", 89)]
    base.save(BINDINGS, dict(actor=actor, source_mentions=names, current_getter_evidence_sha256=base.digest(NAMES),
                             source_actor_name=source_field["text"], current_installed_name="Mihwa",
                             scene_name_consistency_findings=1, actual_gameplay=False))


def main():
    if not SOURCE.exists():
        ctx = vars(pairing) | dict(parent=parent, ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=CONTEXT)
        FunctionType(pairing.main.__code__, ctx)()
    bind_name()
    packet = base.load(SOURCE)
    group, = packet["groups"]
    notes = [row.split("|") for row in NOTES.splitlines()]
    assert [int(n) for n, *_ in notes] == [r["source_record_index"] for r in group["records"]]
    exchanges = {(1, 89): (0, "\n".join(f"{meaning}|{reason}" for _, meaning, reason, _ in notes))}
    phrases = {
        11: ("Silla Gold Crown",),
        35: ("Silla Gold Crown", "tavern in Hangzhou"),
        39: ("Silla Gold Crown",),
        43: ("I meant to give it to her.",),
        51: ("How can I face Mihwa now?", "Please, could you let me have it?"),
        67: ("We've no use for it", "see it gather dust", "You can say you found it yourself."),
    }
    edits = {(1, 89, int(n)): (english, phrases.get(int(n), ()))
             for n, _, _, english in notes if english}
    source = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n                meaning, reason = note.split("|", 1)',
        'source_meaning=note, localization_note=note,': 'source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | dict(exchanges=exchanges, EDITS=edits)
    exec(compile(source, __file__ + "::crown_story_review", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
