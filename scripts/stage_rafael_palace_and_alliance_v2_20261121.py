"""Stage the visually refined palace and alliance dialogue as a new ROM."""

from types import FunctionType

from scripts import stage_rafael_palace_and_alliance_20261121 as first
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, review = first.base, first.native, first.parent, first.review
ROOT = first.ROOT.with_name("palace_and_alliance_staged_v2")
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = review.OUTPUT
GUARD_SC0, GUARD = ROOT / first.GUARD_SC0.name, ROOT / first.GUARD.name


if __name__ == "__main__":
    compiler = first.precedent.prior.compiler
    qualify = FunctionType(first.qualify_format_controls.__code__,
                          first.qualify_format_controls.__globals__ | {"GUARD_SC0": GUARD_SC0, "GUARD": GUARD})
    source = checked_text(compiler.source, {
        "    assert not ROOT.exists()": "    assert not ROM.exists() and not PROOF.exists()",
        "stage.system.native_painter(ctx)": "current_fe_painter(ctx)",
        'g for g in packet["groups"]}': 'g for g in packet["groups"] if g["block"] in review.BLOCKS[0]}',
        '    controls = bind_registered_story_percent_guard(guard)(native.files(clean), final)\n'
        '    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7':
        '    ROOT.mkdir(exist_ok=True)\n    controls = qualify_format_controls(guard, native.files(clean), initial, final, verified)\n'
        '    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7',
        "    ROOT.mkdir()\n    ROM.write_bytes(payload)": "    ROM.write_bytes(payload)",
    })
    scope = (compiler.env | vars(first.precedent.prior) | globals() |
             {"paired": review, "qualify_format_controls": qualify})
    exec(compile(source, __file__ + "::stage", "exec"), scope)
    scope["main"]()
