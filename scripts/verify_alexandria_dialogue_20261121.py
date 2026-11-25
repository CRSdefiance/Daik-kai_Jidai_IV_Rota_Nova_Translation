"""Verify the revised dialogue and original speakerless forecast layouts."""
from inspect import getsource
from types import SimpleNamespace

from scripts import stage_alexandria_dialogue_20261121 as build
from scripts import verify_stockholm_dialogue_display_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town = build.base, build.native, precedent.town
ROOT = build.ROOT / "native_display_v2"
PROOF = ROOT / "native_display.json"


if __name__ == "__main__":
    stage = SimpleNamespace(PROOF=build.PROOF, REBOUND=build.review.OUTPUT, ROM=build.ROM, parent=build.parent,
                            author=build.review, stage=build.compiler.stage)
    source = checked_text(getsource(precedent.main), {
        "len(receipts) == 39 and len(previews) == 3": "len(receipts) == 48 and len(previews) == 10",
        "newly_rendered_pages=3": "newly_rendered_pages=len(previews)",
        "Three Stockholm pages passed native checks, and all 36 retained records are byte-exact.":
            "Ten Alexandria pages passed native checks, and all 38 retained records are byte-exact.",
    })
    scope = vars(precedent) | globals() | {"build": stage}
    exec(compile(source, __file__, "exec"), scope)
    scope["main"]()
