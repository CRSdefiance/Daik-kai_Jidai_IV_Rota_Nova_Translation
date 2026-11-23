"""Review and stage the mosque, Elysion and Mikhail exchanges."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_trade_house_charles_and_earrings_20261122 as checkpoint
from scripts import register_trade_house_charles_and_earrings_20261122 as current
from scripts import review_lil_lessons_and_maria_scenes_20261122 as binder
from scripts import stage_trade_house_charles_and_earrings_20261122 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, compiler.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/mosque_elysion_mikhail_20261122") / "corrected"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("mosque_elysion_mikhail_20261122.md")
CHOICES = {}
bind_scope = binder.bind_scope
ROOT = BATCH / "staged"
ROM = ROOT / "Mosque_Elysion_Mikhail_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)

sections = checked_text(getsource(binder.load_sections), {"[23]": "[01]"})
binding = vars(binder) | globals()
exec(compile(sections, __file__ + "::sections", "exec"), binding)
CONTEXT, DECISIONS = binding["load_sections"]()

scope = vars(binder.template) | globals() | dict(ROOT=BATCH, established=binder.established)
review_source = checked_text(getsource(binder.template.contextual_review), {
    '    common = parse(FERNANDO)\n': '',
    '''        if block in (169, 136):
            aligned = {(i - int(route == 3 and i < 143)): value for i, value in common.items()}
            decisions = aligned | parse(ROUTE_TURNS[route])
            refinements = {i - int(route == 3 and i < 143): v for i, v in PARALLEL_REFINEMENTS.items()}
        else:
            decisions = parse(HODRAM[block])
            refinements = {}''': '        decisions = parse(DECISIONS[route, block])',
    'rows, _, _ = established.bind': 'rows, _, _ = bind_scope["bind"]',
    '''            if refined:
                replacement, protected, note = REFINEMENTS.get((route, block, ordinal),
                    refinements.get(ordinal, (replacement, protected, note)))''': '',
    'prior = " ".join(english[1:].decode("ascii").split())':
        '''prior = " ".join(english[1:].decode("cp932").split())
            if not prior.isascii():
                assert (route, block, ordinal) == (1, 168, 96) and prior == "○×△◎▲□×◇!?"
                assert not decisions[ordinal][1] and not decisions[ordinal][2]''',
    '            ident = f"DK4_MES_B{block}_R{ordinal:04d}"':
        '            assert selector != 254 or change == "retention"\n            ident = f"DK4_MES_B{block}_R{ordinal:04d}"',
    'kind="progressive", speaker=names[selector], context=context, source_meaning=meaning,':
        'kind="system" if selector == 254 else "progressive", speaker=names.get(selector, "Speakerless panel"), context=context, source_meaning=meaning,',
    'assert len(checked) == 203 and len(choice_proofs) == 4':
        'assert len(checked) == 180 and not choice_proofs and sum(r["source_selector"] == 254 for r in checked) == 7',
    'wrap_queue_sha256=base.digest(queue.OUTPUT),':
        'wrap_queue_sha256=base.digest(checkpoint.QUEUE), manuscript_sha256=base.digest(MANUSCRIPT),',
    'across five objects.': 'across three complete scenes.',
})
exec(compile(review_source, __file__ + "::source-paired-review", "exec"), scope)
preflight_source = checked_text(getsource(binder.established.preflight), {
    '("FO","FI") if t.encode("ascii") in body': '("FO","FI","FA") if t.encode("ascii") in body',
    '    for row in (r for r in draft["records"] if r["decision"]=="revision"):':
        '    default_last={0:"Castor",1:"Bergstrom",2:"Argot",3:"Li"}\n    for row in (r for r in draft["records"] if r["decision"]=="revision"):',
    '"FI":default_first[row["route"]]}': '"FI":default_first[row["route"]],"FA":default_last[row["route"]]}',
    '"FI":"W"*16}': '"FI":"W"*16,"FA":"W"*16}',
})
preflight_scope = binder.established.preflight.__globals__ | globals() | dict(ROOT=BATCH)
exec(compile(preflight_source, __file__ + "::bounded-full-names", "exec"), preflight_scope)

compiler_scope = compiler.compiler_scope | globals()
renderer_source = checked_text(compiler.renderer_source, {
    'routes = {0: native.RegisteredRuntime(identity, boot, captain=0)}':
        'routes = {0: native.RegisteredRuntime(identity, boot, captain=0), 1: display.contexts.hodram_context()}',
    'assert given == "Rafael"': 'assert given == {0: "Rafael", 1: "Hodram"}[route]',
    'captain == 0': 'captain in (0,1)',
    '                if route == 0:': '                if route in (0, 1):',
    '                assert len(encoded) == 4': '''                if ident == "DK4_MES_B123_R0115":
                    assert b".." not in expected and b"Castor Co.," in expected
                assert len(encoded) == 4''',
})
exec(compile(renderer_source, __file__ + "::two-name-contexts", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        scope["contextual_review"](False)
    elif action == "preflight":
        preflight_scope["preflight"]()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
