"""Refine the figurehead and town wraps found in the native previews."""

from inspect import getsource
from json import dumps
from types import FunctionType

from scripts import stage_figurehead_and_ruins_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("figurehead_and_ruins_20261118_v2")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("figurehead_and_ruins_20261118_v2.json")
PAGE_EDITS = {}


def refine(scene, numbers, text, phrases, note):
    for route, number in enumerate(numbers):
        if number is not None:
            PAGE_EDITS[route, prior.BLOCK_BY_SCENE[route][scene], number] = (text, phrases, note)


refine(0, (15, None, None, None), "Look at this fine figurehead!", ("fine figurehead!",),
       "Julio points out the figurehead in one excited line.")
refine(0, (57, 56, 54, 55), "You're joking! We don't need that strange thing, do we, Admiral?",
       ("You're joking!", "that strange thing, do we, Admiral?"),
       "Julio recoils and tries to get the captain to agree. Keep the entire question tag attached.")
refine(1, (19, 18, 18, 17), "A sailor who visited the New World told me about a river that carries gold dust.",
       ("A sailor who visited the New World", "carries gold dust."),
       "Keep the sailor's firsthand travel and the source of the river story. Use the first line for a complete phrase.")
refine(2, (26, None, None, None),
       "Maybe some ancient civilization was way ahead of its time. It might've died out for some reason...",
       ("way ahead of its time.", "for some reason..."),
       "The resident supplies a possible ancient civilization and leaves its fate uncertain.")
refine(3, (11, 11, 11, 10), "You like ancient civilizations too? We have ruins right here in town.",
       ("You like ancient civilizations too?", "We have ruins right here in town."),
       "Let the question and the disclosure occupy their own complete lines.")
refine(4, (16, 15, 15, 14), "You should go while you're here. I'll show you the way.",
       ("You should go while you're here.", "I'll show you the way."),
       "Keep the encouragement and the offer of directions as complete beats.")
refine(5, (10, 10, 10, 9), "Seen the ruins near town? Rumor is they were once King Solomon's treasury.",
       ("Seen the ruins near town?", "King Solomon's treasury."),
       "Keep the local question and mark the origins as a rumor. Keep the complete name intact.")
refine(5, (18, None, 17, None), "Perfect picnic weather. Why not take a look?",
       ("Perfect picnic weather.", "Why not take a look?"),
       "Use the sunny weather as an invitation to visit. Keep the question together.")

EDITS = prior.EDITS | PAGE_EDITS
BLOCKS = prior.BLOCKS


def verify_predecessor_preview_dependencies(ctx):
    previous = base.load(prior.STORED)
    staged = base.load(prior.MANUSCRIPT)
    assert previous["manuscript_sha256"] == base.digest(prior.MANUSCRIPT)
    assert previous["candidate_sha256"] == base.digest(prior.ROM)
    assert previous["previous_sha256"] == ctx.release["candidate_sha256"]
    current = base.NdsImage.open(prior.ROM)
    for path in (native.ARM, "/GRP/KANJI.FNT"):
        assert current.read_file(path) == ctx.image.read_file(path)
    return staged


def render_changed(ctx, edited):
    staged = verify_predecessor_preview_dependencies(ctx)
    proofs = {(r["route"], r["id"]): r for r in staged["records"] if r["decision"] == "revision"}
    needed = []
    pictures = []
    for row in edited:
        key = row["route"], row["id"]
        reused = proofs.pop(key, None)
        assert reused is not None
        turn = row["source_reference"]["record_index"]
        if (row["route"], row["block"], turn) in PAGE_EDITS:
            needed.append(row)
            continue
        for field in ("source_reference", "current_reference", "english", "target_hex", "automatic_layout"):
            assert dumps(row[field], sort_keys=True) == dumps(reused[field], sort_keys=True), (key, field)
        assert all(value == reused["staged_reference"][name]
                   for name, value in row["staged_reference"].items() if name != "block_sha256")
        for page in reused["after_native"]["pages"]:
            assert native.digest(bytes.fromhex(page["native_plane_hex"])) == page["plane_sha256"]
        row["after_native"] = reused["after_native"]
    assert not proofs and len(needed) == len(PAGE_EDITS)
    precedent.validate_native(ctx, needed)
    for row in edited:
        pages = row["after_native"]["pages"]
        for page in pages:
            title = f"SC{row['route']} {row['id'].split('_B')[1]} {page['page']}/{len(pages)}"
            pictures.append((title, bytes.fromhex(page["native_plane_hex"])))
    return pictures


SCOPE = prior.SCOPE | globals()
for function in ("review_exchange", "collect"):
    SCOPE[function] = FunctionType(prior.SCOPE[function].__code__, SCOPE)
source = checked_text(getsource(precedent.main), {
    "    assert len(groups) == 20": "    assert len(groups) == len(BLOCKS)",
    "    pictures = validate_native(ctx, edited)": "    pictures = render_changed(ctx, edited)",
})
exec(compile(source, __file__ + "::cumulative-stage", "exec"), SCOPE)


if __name__ == "__main__":
    SCOPE["main"]()
