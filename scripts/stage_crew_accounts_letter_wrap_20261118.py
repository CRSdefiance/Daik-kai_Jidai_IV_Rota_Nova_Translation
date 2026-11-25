"""Fix the letter's escape line and reuse the exact 98 checked candidate pages."""

from inspect import getsource
from json import dumps
from pathlib import Path
from types import FunctionType

from scripts import stage_crew_accounts_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("crew_accounts_20261118_v3")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("crew_accounts_20261118_v3.json")
LETTER_WRAPS = {
    (0, 247, 44): (None, ("Spanish navy", "happen by.", "managed to escape."), "Keep the escape with its subject and remove the stranded continuation page observed in Rafael's letter."),
    (1, 238, 44): ("They held out until the Spanish navy happened by. The pirates scattered, and the merchant convoy escaped.", ("Spanish navy", "happened by.", "merchant convoy escaped."), "Keep the chance encounter and the scattered retreat. Finish the escape clause with its subject on the same page."),
    (2, 235, 44): ("They held out until the Spanish navy happened by. The pirates fled in confusion. The fleet narrowly escaped, or so the story goes.", ("Spanish navy", "happened by.", "fled in confusion.", "The fleet narrowly escaped,", "or so the story goes."), "Finish the pirates' retreat before the page break. The escape and the letter writer's qualification stay together."),
    (3, 208, 43): (None, ("Spanish navy", "pass by.", "narrowly escaped disaster."), "Keep the escape phrase intact within the existing two-page allocation."),
}
EDITS = prior.EDITS | LETTER_WRAPS
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
    for row in edited:
        key = row["route"], row["id"]
        reused = proofs.pop(key, None)
        if reused is None:
            needed.append(row)
            continue
        for field in ("source_reference", "current_reference", "english", "target_hex", "automatic_layout"):
            assert dumps(row[field], sort_keys=True) == dumps(reused[field], sort_keys=True), (key, field)
        assert all(value == reused["staged_reference"][name]
                   for name, value in row["staged_reference"].items() if name != "block_sha256")
        for page in reused["after_native"]["pages"]:
            assert native.digest(bytes.fromhex(page["native_plane_hex"])) == page["plane_sha256"]
        row["after_native"] = reused["after_native"]
    assert not proofs
    return precedent.validate_native(ctx, needed)


def save_sheets_and_count(root, new_pictures):
    previous = base.load(prior.STORED)
    checked = previous["sheets"]
    assert all(base.digest(row["path"]) == row["sha256"] for row in checked)
    fresh = FunctionType(precedent.layout.contact_sheets.__code__,
                        vars(precedent.layout) | dict(ROOT=root))(new_pictures)
    for index, sheet in enumerate(fresh, 1):
        old = Path(sheet["path"])
        path = root / f"letter_wrap_review_{index}.png"
        assert not path.exists()
        old.rename(path)
        sheet["path"] = path.as_posix()
    return checked + fresh, previous["preview_count"] + len(new_pictures)


SCOPE = prior.SCOPE | globals()
for function in ("review_exchange", "collect"):
    SCOPE[function] = FunctionType(prior.SCOPE[function].__code__, SCOPE)
source = checked_text(getsource(precedent.main), {
    "    assert len(groups) == 20": "    assert len(groups) == len(BLOCKS)",
    "    pictures = validate_native(ctx, edited)": "    pictures = render_changed(ctx, edited)",
    "    sheets = FunctionType(layout.contact_sheets.__code__, vars(layout) | dict(ROOT=ROOT))(pictures)":
        "    sheets, preview_count = save_sheets_and_count(ROOT, pictures)",
    "preview_count=len(pictures)": "preview_count=preview_count",
    'len(pictures), "revised display previews"': 'preview_count, "revised display previews"',
})
exec(compile(source, __file__ + "::cumulative-stage", "exec"), SCOPE)


if __name__ == "__main__":
    SCOPE["main"]()
