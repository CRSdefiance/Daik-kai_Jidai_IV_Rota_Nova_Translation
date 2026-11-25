"""Put Cesare's four long or split phrases into complete lines."""

from inspect import getsource
from json import dumps
from types import FunctionType

from scripts import stage_ruin_statue_and_ice_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("ruin_statue_and_ice_20261118_v2")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("ruin_statue_and_ice_20261118_v2.json")
WRAP_REVISIONS = {}


def refine(numbers, text, phrases, note):
    for route, number in enumerate(numbers):
        WRAP_REVISIONS[route, prior.FIRST_BLOCK[route], number] = (text, phrases, note)


refine((31, 26, 26, 25), "Oh, it's a figurehead! Look at all that detail. Yes, I can feel it, too.",
       ("Oh, it's a figurehead!", "Look at all that detail.", "Yes, I can feel it, too."),
       "Keep Cesare's recognition, admiration and confirmation as three complete beats.")
refine((58, 53, 52, 51),
       "It's a magnificent figurehead. If we mount it on the ship, it could bring us good fortune. Can we take it without asking?",
       ("a magnificent figurehead.", "If we mount it on the ship,", "bring us good fortune.", "Can we take it without asking?"),
       "Keep the condition about mounting it and Cesare's concern about permission. The fixed storage holds four complete lines.")
refine((66, 60, 59, 58), "How kind of you, Admiral! Let's move it, then!",
       ("How kind of you, Admiral!", "Let's move it, then!"),
       "Keep the compliment and the encouragement intact.")
refine((70, 64, 63, 62), "Pardon us. Please come along, figurehead.",
       ("Pardon us.", "Please come along, figurehead."),
       "Keep Cesare's polite request to the figurehead as one phrase.")

EDITS = prior.EDITS | WRAP_REVISIONS
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
        if (row["route"], row["block"], turn) in WRAP_REVISIONS:
            needed.append(row)
            continue
        for field in ("source_reference", "current_reference", "english", "target_hex", "automatic_layout"):
            assert dumps(row[field], sort_keys=True) == dumps(reused[field], sort_keys=True), (key, field)
        assert all(value == reused["staged_reference"][name]
                   for name, value in row["staged_reference"].items() if name != "block_sha256")
        for page in reused["after_native"]["pages"]:
            assert native.digest(bytes.fromhex(page["native_plane_hex"])) == page["plane_sha256"]
        row["after_native"] = reused["after_native"]
    assert not proofs and len(needed) == len(WRAP_REVISIONS)
    precedent.validate_native(ctx, needed)
    for row in edited:
        pages = row["after_native"]["pages"]
        for page in pages:
            title = f"SC{row['route']} {row['id'].split('_B')[1]} {page['page']}/{len(pages)}"
            pictures.append((title, bytes.fromhex(page["native_plane_hex"])))
    return pictures


_storage = vars(precedent.layout).copy()
_source = checked_text(getsource(precedent.layout.fit_storage_padding),
                       {"(35 - len(line))": "(36 - len(line))"})
exec(compile(_source, __file__ + "::one-Rafael-fixed-allocation", "exec"), _storage)


def compile_row(row, fixed, phrases):
    try:
        precedent.compile_row(row, fixed, phrases)
    except AssertionError:
        if (row["route"], row["id"], len(fixed)) != (0, "DK4_MES_B260_R0058", 144):
            raise
        plan = row["automatic_layout"]
        assert len(plan["lines"]) == 4 and len(bytes.fromhex(plan["encoded_hex"])) < len(fixed)
        # This fixed payload uses one extra column for zero-ink padding.
        # The native validator compares every resulting pixel with the unpadded version.
        _storage["fit_storage_padding"](row)


SCOPE = prior.SCOPE | globals()
SCOPE["review_exchange"] = FunctionType(prior.SCOPE["review_exchange"].__code__, SCOPE)
oral_collect = FunctionType(prior.oral_collect.__code__, SCOPE)


def collect():
    release, ctx, inv, groups, errors = oral_collect()
    if errors:
        return release, ctx, inv, groups, errors
    staged = verify_predecessor_preview_dependencies(ctx)
    earlier = {(r["route"], r["id"]): r for r in staged["records"]
               if r["source_selector"] == 254 and r["decision"] == "revision"}
    assert len(earlier) == 8
    fields = ("target_hex", "english", "decision", "localization_note", "automatic_layout", "after_native")
    for rows, _ in groups.values():
        for row in rows:
            old = earlier.pop((row["route"], row["id"]), None)
            if old is not None:
                assert all(row[key] == old[key] for key in ("source_reference", "current_reference", "source_selector", "current_hex"))
                row.update({key: old[key] for key in fields})
    assert not earlier
    return release, ctx, inv, groups, errors


SCOPE["collect"] = collect
source = checked_text(getsource(precedent.main), {
    "    assert len(groups) == 20": "    assert len(groups) == len(BLOCKS)",
    "    pictures = validate_native(ctx, edited)": "    pictures = render_changed(ctx, edited)",
})
exec(compile(source, __file__ + "::cumulative-stage", "exec"), SCOPE)


if __name__ == "__main__":
    SCOPE["main"]()
