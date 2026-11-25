"""Render every changed late-trade body and exercise the original macro wrapper."""

from inspect import getsource
from types import SimpleNamespace

from scripts import generic_name_macro_owned_v5886b as macro
from scripts import stage_late_trade_exchanges_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts import verify_rafael_mosque_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def lil_context():
    report = base.load(build.ROOT / "lil_snapshot/capture_report.json")
    snapshot, = report["read_only_capture_RAM_snapshots"]
    candidate = base.digest(build.ROM)
    assert report["ROM_sha256"] == candidate == base.digest(build.ROOT / "clean_rebuilt.nds")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == base.load(build.ROOT / "lil_snapshot_inputs.json")
    boot = build.ROOT / "lil_native_context.json"
    rep = build.ROOT / "lil_native_ROM_identity.json"
    base.save(boot, dict(candidate_sha256=candidate, cold_boot=True, savestate=False,
                         actual_captain_getter=2, read_only_snapshot=snapshot))
    base.save(rep, dict(candidate=str(build.ROM), candidate_sha256=candidate,
                        own_registered_startup_pending=False, clean_input_patch_byte_exact=True))
    return native.RegisteredRuntime(rep, boot, captain=2)


def current_names(ctx):
    expansion = ctx.execute(macro.expand, b"FI FA FO", 2)
    assert {bytes.fromhex(row["output_hex"]) for row in expansion["cases"]} == {b"Lil Argot Argot Co."}
    return {"FI": "Lil", "FA": "Argot", "FO": "Argot Co."}


def expander():
    source = checked_text(getsource(macro.expand), {
        "assert identity==prefix and captain==2": "assert identity == prefix and captain in (2, 3)",
    })
    scope = vars(macro).copy()
    exec(compile(source, __file__ + "::original-selector-and-actor", "exec"), scope)
    return scope["expand"]


def no_dynamic_roles(ctx, proof):
    assert not any(207 <= plan.get("source_selector", 254) < 224 for group in proof["groups"]
                   for plan in group["plans"].values())
    return []


paragraph_source = checked_text(getsource(previous.paragraph), {
    '{macro: example for macro in tokens}':
        '{macro: example + " Co." if macro == "FO" else example for macro in tokens}',
})
source = checked_text(template.source, {
    'ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)':
        'ctx = lil_context()\n    maria = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)',
    'result = paragraph(ctx, font, paint, expand, fe_paint, names, row, value, group["plans"][ident])':
        'result = paragraph(ctx if group["route"] == 2 else maria, font, paint, expand,'
        ' fe_paint, names, row, value, group["plans"][ident])',
    'roles = inherited.validate_roles(ctx, proof)': 'roles = no_dynamic_roles(ctx, proof)',
    "assert len(rendered) == 27 and not styles": "assert len(rendered) == 42 and not styles",
    "original_style_resolution=roles, native_default_given_and_surname=names, actual_gameplay=False,":
        "original_style_resolution=roles, native_default_name_expansions=names, actual_gameplay=False,",
})
adapter = SimpleNamespace(**(vars(build) | {"review": SimpleNamespace(**(
    vars(build.review) | {"TOKEN": previous.build.review.TOKEN, "logical": previous.build.review.logical}
))}))
env = vars(previous) | globals() | {"build": adapter}
for code, label in ((paragraph_source, "original-consumers"), (source, "all-revised-pages")):
    exec(compile(code, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
