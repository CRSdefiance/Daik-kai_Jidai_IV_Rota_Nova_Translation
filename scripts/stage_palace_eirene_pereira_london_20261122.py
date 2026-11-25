"""Bind and stage the palace lesson, Eirene, Pereira, and London exchanges."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_aziza_shamshir_20261122 as checkpoint
from scripts import register_aziza_shamshir_20261122 as current
from scripts import stage_aziza_shamshir_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/palace_eirene_pereira_london_20261122/corrected")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("palace_eirene_pereira_london_20261122.md")
ROOT = BATCH / "staged"
ROM = ROOT / "Palace_And_London_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CHOICE_PROOF = ROOT / "unchanged_choice_proof.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
CHOICES = {
    (0, 143, 0): ("Ask Silveira to explain why investment alone is insufficient, or say Rafael already knows.",
                  "Why not? asks for the reason after Silveira's direct correction. I already know preserves the alternate response and both stay in the native branch order."),
}

load = FunctionType(template.load.__code__, template.load.__globals__ | globals())
CONTEXT, DECISIONS = load()
review_source = checked_text(template.review_source, {
    'len(checked) == 78 and not choice_proofs and all(r["source_selector"] != 254 for r in checked)':
        'len(checked) == 275 and len(choice_proofs) == 1 and sum(r["source_selector"] == 254 for r in checked) == 7',
    'in the complete Aziza exchange.': 'in four complete exchanges.',
})
review_scope = template.review_scope | globals() | dict(ROOT=BATCH, established=template.template.binder.established)
exec(compile(review_source, __file__ + "::source-paired-review", "exec"), review_scope)
preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))

renderer_source = checked_text(template.renderer_source, {
    'DK4_MES_B26_R0060': 'DK4_MES_B143_R0005',
})
compiler_scope = template.compiler_scope | globals()
exec(compile(renderer_source, __file__ + "::palace-name-context", "exec"), compiler_scope)


def verify_choice():
    manuscript, stored = map(base.load, (REVIEW, PROOF))
    assert base.digest(ROM) == stored["candidate_sha256"]
    row, = manuscript["retained_choice_objects"]
    old = row["current"]
    path, number = old["file_path"], old["block"]
    assert (path, number) == ("/data/SC0.DK4", 143)
    group, = (g for g in stored["groups"] if (g["file_path"], g["block"]) == (path, number))
    block = native.IlnkContainer.parse(base.NdsImage.open(ROM).read_file(path)).blocks[number]
    command, = (c for c in group["commands"] if c["current_offset"] == old["command_offset"])
    assert command["word"] == 0x2100 and command["source"] == row["source"]["exact_command_hex"]
    assert command["current"] == command["stored"] == old["exact_command_hex"]
    at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
    assert native.digest(block) == group["after"] and block[at:at+len(raw)] == raw
    base.save(CHOICE_PROOF, dict(candidate_sha256=stored["candidate_sha256"], offline_exact=True,
        choice=row | dict(installed_offset=at, installed_command_hex=raw.hex(), installed_block_sha256=group["after"])))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup", "choice"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"](False)
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    elif action == "choice":
        verify_choice()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
