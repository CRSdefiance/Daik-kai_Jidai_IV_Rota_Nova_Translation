"""Review and render Rafael's ship-buying, refitting and sailing exchanges."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import pair_rafael_ship_lessons_20261123 as packet
from scripts import register_rafael_basra_and_map_keys_20261123 as parent
from scripts import stage_rafael_basra_and_map_keys_20261123 as prior
from scripts import verify_rafael_midroute_exchanges_20261122 as verification
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = BATCH = packet.OUTPUT.parent
REVIEW, PREFLIGHT = (ROOT / name for name in ("lesson_review.json", "native_preflight.json"))
STAGED = Path(".codex-release-work/rafael_ship_lessons_20261123/staged")
ROM = STAGED / "Rafael_Ship_Lessons_STAGED.nds"
PROOF, NATIVE = (STAGED / name for name in ("stored_proof.json", "native_display.json"))
MANUSCRIPTS = tuple(Path(__file__).with_name(name) for name in (
    "rafael_ship_buying_20261123.md", "rafael_refitting_and_sailing_20261123.md",
))
paired = SimpleNamespace(OUTPUT=packet.OUTPUT)
checkpoint = SimpleNamespace(QUEUE=packet.QUEUE)

review_source = checked_text(prior.review_source, {
    '    for group in packet["groups"]:':
        '    for group in packet["groups"]:\n'
        '        if group["block"] not in (177, 179, 180):\n'
        '            continue',
    'len(records)==207 and len(captions)==6 and len(leads)==14 and sum(r["kind"]=="system" for r in records)==2':
        'len(records)==112 and len(captions)==6 and len(leads)==8 and sum(r["kind"]=="system" for r in records)==1',
    'Reviewed 213 texts across ten Rafael exchanges.':
        'Reviewed 118 texts across Rafael’s ship-buying, refitting and sailing exchanges.',
})
review_scope = prior.review_scope | globals()
for source in (prior.section_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_scope = prior.preflight_scope | globals()
exec(compile(prior.preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)

compiler_scope = prior.compiler_scope | globals() | dict(
    ROOT=STAGED, review=SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT),
)
compiler_scope["compilers"] = FunctionType(prior.established.compilers.__code__, compiler_scope)
stage_source = checked_text(prior.prior.stage_source, {
    "    paint_fe = modal_painter()":
        '    assert not any(r["kind"] == "system" and r["decision"] == "revision" for r in draft["records"])\n'
        "    paint_fe = None",
})
exec(compile(stage_source, __file__ + "::stage", "exec"), compiler_scope)
compiler_scope["native_display"] = FunctionType(verification.progressive["native_display"].__code__, compiler_scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "preflight", "stage", "native_display"))
    action = parser.parse_args().action
    if action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope["preflight"]()
    else:
        compiler_scope[action]()
