"""Keep full clauses together across the Frozen Rose continuation pages."""

from inspect import getsource
from json import dumps
from types import FunctionType

from scripts import stage_janus_and_frozen_rose_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("janus_and_frozen_rose_20261118_v2")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("janus_and_frozen_rose_20261118_v2.json")
RETURN_LINE = (
    "Take it back to its rightful owner. That crook must have other scams going. Next time I see him, I'll turn him in to the governor's office!",
    ("rightful owner.", "other scams going.", "Next time I see him,", "I'll turn him in", "to the governor's office!"),
    "Return the rose to its owner. Keep the suspected scams distinct from the proprietor's promise to report him. Start the continuation at that complete promise.",
)
PAGE_EDITS = {
    (0, 252, 116): RETURN_LINE,
    (2, 240, 120): RETURN_LINE,
    (3, 213, 107): RETURN_LINE,
    (3, 212, 109): (
        "Someone a friend knows told me about a swindler in Havana. They pass glass off as jade or crystal. They charge a fortune for it.",
        ("a swindler in Havana.", "jade or crystal.", "charge a fortune"),
        "The secondhand lead identifies a swindler, a city, fake stones and a price. The last sentence is a full thought and begins the continuation.",
    ),
}
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
    assert not proofs and len(needed) == 4
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
