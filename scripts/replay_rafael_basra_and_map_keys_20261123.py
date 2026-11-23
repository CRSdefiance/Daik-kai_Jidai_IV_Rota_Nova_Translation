"""Check the revised Rafael pages and all three original two-option choices."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_midroute_exchanges_20261122 as previous
from scripts import review_rafael_midroute_nameplates_20261122 as names
from scripts import stage_rafael_basra_and_map_keys_20261123 as stage
from scripts import verify_rafael_midroute_exchanges_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
EXCERPTS = ROOT / "verified_excerpts.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES = stage.ROOT / "original_choice_tables.json"
ROLES = stage.ROOT / "speaker_roles.json"
PROMPTS = {146: 34, 148: 17, 154: 117}
RESULTS = {146: ((50,), (85,)), 148: ((33,), (196,)), 154: ((185,), (140,))}
RUNS = {f"b{block}_{slot}": (block, slot) for block in PROMPTS for slot in range(2)}
MODAL_SAMPLE = {(148, 121), (148, 152)}
record_id = previous.record_id
NOTES = {
    0: "Keep Rafael Castor. The crew uses the original first-name field and Uddin can address him by surname or full name.",
    4: "Keep Janus Pasar for the speaker who cautiously interprets the tablets and bamboo map.",
    5: "Keep Claudio Manaus in the nameplate and Clau in familiar crew conversation.",
    6: "Keep Julio Erneco for the crew member who advises Rafael about expansion and fighting.",
    8: "Keep Arcadius Eudoxios in the active nameplate and Eirene in the separate native catalogue component.",
    25: "Keep Yifa Sol for the alternate speaker who disassembles the Tang Bamboo Craft. Rafael calls her Yifa.",
    37: "Keep Abraham Uddin in the nameplate. His self-introduction supplies the fuller Abraham Ibn Uddin.",
    42: "Keep Vasquez Maldonado for the leader overheard by the crew. His own lines state his authority and intentions.",
    54: "Keep Ibn Niyadi for the named attendant Uddin asks to show Rafael into the reception room.",
    60: "Keep Juan Blanco for the man who insists on discretion while the sailor speaks.",
    92: "Keep Barkeep for the unnamed witness who explains Maldonado's actions and their effect on his business.",
    151: "Keep Sailor for the unnamed speakers in the two separate overheard conversations.",
}


def sample():
    draft = base.load(stage.REVIEW)
    return {0: tuple(
        (row["block"], int(row["id"].rsplit("R", 1)[1]))
        for row in draft["records"]
        if (row["decision"] == "revision" and row["id"] != record_id(146, 34))
        or (row["block"], int(row["id"].rsplit("R", 1)[1])) in MODAL_SAMPLE
    )}


def report(run):
    folder = "route0" if run == "0" else run
    return ROOT / folder / "capture/capture_report.json"


def choice_paths(block):
    folder = ROOT / f"b{block}_choice"
    return folder, folder / f"Rafael_B{block}_Choice_FOCUSED_ONLY.nds", folder / "fixture.json"


branch_scope = previous.branch_scope | globals()
exec(compile(previous.prepare_source, __file__ + "::exact-source-choice-suffix", "exec"), branch_scope)
excerpt_scope = previous.excerpt_scope | globals() | dict(LIVE=EXCERPTS)
excerpt_scope["scope"] = excerpt_scope
for name in ("receipt", "report_path", "run_file", "play"):
    inherited = previous.excerpt_scope[name]
    excerpt_scope[name] = FunctionType(inherited.__code__, excerpt_scope)
fixture_source = checked_text(previous.excerpt_source, {
    "Rafael_Midroute_Exchanges_FOCUSED_ONLY.nds": "Rafael_Basra_And_Map_Keys_FOCUSED_ONLY.nds",
})
exec(compile(fixture_source, __file__ + "::focused-fixture", "exec"), excerpt_scope)
excerpt_verify = checked_text(previous.excerpt_verify, {
    'r["layouts"] and r["block"] != 118': 'r["layouts"] and r["id"] != record_id(146, 34)',
    "rafael_midroute_excerpt_": "rafael_basra_excerpt_",
    "including four original modal panels": "including both original market-share notices",
})
exec(compile(excerpt_verify, __file__ + "::focused-display-verification", "exec"), excerpt_scope)
branch_frames = FunctionType(previous.branch_frames.__code__, previous.branch_frames.__globals__ | globals())
play_choice = FunctionType(previous.play_choice.__code__, previous.play_choice.__globals__ | globals())


def panel_mask(row, bodies, modals, ctx, paint, font):
    if row["id"] != record_id(154, 140):
        return previous.branch_fixture.panel_mask(row, bodies, modals, ctx, paint, font)
    raw = bytes.fromhex(bodies[0, row["id"]]["body_hex"])[1:]
    assert raw.rstrip(b" ") == b"FI..."
    given = base.load(stage.NATIVE)["default_names"]["0"]["FI"].encode("ascii")
    expanded = raw.replace(b"FI", given)
    result = paint(ctx.arm, font, expanded)
    assert result["complete_consumed_bytes"] == len(expanded)
    page, = result["pages"]
    return 216, bytes.fromhex(page["native_plane_hex"])


def formatting():
    if not stage.NATIVE.exists():
        FunctionType(display.progressive["native_display"].__code__, stage.compiler_scope)()
    if not GLYPHS.exists():
        glyphs = display.verification.glyphs
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    if not stage.FE_PROOF.exists():
        original = display.verification
        code = checked_text(getsource(original.check_modal), {
            'len(records) == 10 and sum(r["second_page"] for r in records) == 2':
                'len(records) == 2 and not any(r["second_page"] for r in records)',
            'Verified all ten modal pages, including both original two-page Maria sequences.':
                'Verified both market-share panels with the original modal consumer.',
        })
        scope = vars(original) | dict(stage=stage)
        exec(compile(code, __file__ + "::market-share-notices", "exec"), scope)
        scope["check_modal"]()
    if not CHOICES.exists():
        code = checked_text(getsource(display.check_choices), {
            "len(choices) == 5": "len(choices) == 6",
            "Verified all five original choice captions, slots and complete objects.":
                "Verified all six original captions, slots and complete choice objects.",
        })
        scope = vars(display) | dict(stage=stage, CHOICES=CHOICES)
        exec(compile(code, __file__ + "::retained-choice-labels", "exec"), scope)
        scope["check_choices"]()


def role_labels():
    scope = names.scope | dict(PROOF=ROLES, NOTES=NOTES, parent=stage.parent,
        stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
        display=SimpleNamespace(PROOF=stage.NATIVE), live_receipt=LIVE)
    exec(compile(names.source, __file__ + "::reviewed-nameplates", "exec"), scope)
    scope["main"]()


def verify():
    code = checked_text(getsource(previous.verify_branches), {
        "branch_fixture.panel_mask(row, bodies, modals, ctx, paint, font)": "panel_mask(row, bodies, modals, ctx, paint, font)",
        "rafael_midroute_menus_": "rafael_basra_menus_",
    })
    scope = vars(previous) | globals() | dict(checked=SimpleNamespace(CHOICES=CHOICES))
    exec(compile(code, __file__ + "::native-choice-outcomes", "exec"), scope)
    verify_source = checked_text(getsource(previous.verify), {
        "len(choices) == 5": "len(choices) == 6",
        "all five original menu outcomes.": "all six original menu outcomes.",
    })
    exec(compile(verify_source, __file__ + "::combined-gameplay", "exec"), scope)
    scope["verify"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "role_labels", "replay", "prepare_choices", "verify", *RUNS))
    action = cli.parse_args().action
    if action == "prepare_choices":
        for block in PROMPTS:
            branch_scope["prepare_choice"](block)
    elif action == "replay":
        excerpt_scope["SAMPLE"] = sample()
        excerpt_scope["fixture"](0)
        excerpt_scope["play"](0)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
