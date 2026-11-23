"""Verify the installed Hodram dialogue, retained controls, and original menu outcomes."""

from argparse import ArgumentParser
from pathlib import Path
import re
from types import FunctionType, SimpleNamespace

from scripts import replay_hodram_midroute_followups_20261123 as prior
from scripts import review_hodram_midroute_nameplates_20261123 as nameplates
from scripts import stage_current_story_wraps_20261122 as compiler
from scripts import stage_hodram_late_midroute_wraps_20261123 as staged
from scripts import stage_rafael_midroute_exchanges_20261122 as rendered
from scripts import verify_hodram_midroute_followups_20261123 as typed
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(staged) | {"established": compiler, "typed": rendered.typed, "Path": Path}))
base, native, gameplay = stage.base, stage.native, prior.gameplay
menu, branch, fixture = prior.menu, prior.branch, prior.fixture
BOOT = prior.BOOT
ROOT = stage.ROOT / "focused_gameplay"
LIVE, GLYPHS = ROOT / "verified_gameplay.json", stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES = stage.ROOT / "original_choice_tables.json"
ROLES = stage.ROOT / "speaker_roles.json"
PROMPTS = {167: 86}
RESULTS = {167: ((118, (122, 0), (122, 1), 125, 129, 132, 135, 138, 141, 145), (104, 108))}
RUNS = {"b167_0": (167, 0), "b167_1": (167, 1)}
MODAL_SAMPLE = "DK4_MES_B160_R0219"
record_id, branch_fixture = prior.record_id, prior.branch_fixture
TOKEN = re.compile(rb"\b(?:FI|FA|FO|FU)\b")

NOTES = {
    1: "Keep Hodram Bergstrom. The royal appointment and his retirement are stated in the scene.",
    11: "Keep Jam Ludwyan in the heading and his full introduction in speech.",
    13: "Keep Cesare Tony. He introduces himself and separately identifies his former role aboard the Elysion.",
    16: "Keep Gerhard Adernkatz for Hodram's longtime officer, who chooses to sail with him again.",
    18: "Keep Charles Rochefort in the heading and Jean in the separate native catalogue field.",
    19: "Keep Carlo Sinat. He names himself after accepting the invitation to join.",
    20: "Keep Fernando Dias for the conditional reaction to Carlo and Jam.",
    23: "Keep Manuel Almeida for the officer who teases Hodram and later works on the new ship.",
    24: "Keep Sera Shahrbaraz in the heading. Sera Altos Shahrbaraz is preserved in her spoken introduction.",
    25: "Keep Yifa Sol. Her affection for the fellow student she grew up with is expressed in dialogue.",
    26: "Keep Julian Lopes across the connected crown scenes and his later recruitment.",
    38: "Keep Zamorin Nagarpur for the former leader recognized by Hodram. His losses are explained in speech.",
    78: "Keep Sirwood Eme. His attempt to answer in Hodram's language belongs in his dialogue.",
    81: "Keep Sanghyeon Kan. His seniority and his relationship to Yifa are explained in the dream exchange.",
    92: "Keep Barkeep for the unnamed tavern workers in the extortion, tab, and Lotion Jar exchanges.",
    105: "Keep Trader as the role heading. Carlo supplies the trader's name, Adil, in speech.",
    116: "Keep Port Worker for the dock attendant who spots the returning ship.",
    120: "Keep Guard for the person announcing the royal audience.",
    125: "Keep King for the monarch in the audience. The role identifies his part in the scene.",
    142: "Keep Innkeeper for the speaker who thanks Carlo after Adil falls ill.",
    153: "Keep Sailor for the crew response as the pirates depart.",
    183: "Keep Angel, whom the pirate calls by name before ordering him back.",
    201: "Keep Mihwa for the speaker who asks Julian to find the Silla Gold Crown.",
    202: "Keep Reika for the tavern worker who tells Hodram where the crown might be found.",
}


def retained_panels():
    proof, draft, current = map(base.load, (stage.PROOF, stage.REVIEW, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert proof["candidate_sha256"] == candidate and proof["predecessor_sha256"] == current["candidate_sha256"]
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, current["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for asset in compiler.display.ASSETS)
    paint = rendered.current_fe_painter(ctx)
    bank = native.IlnkContainer.parse(image.read_file(stage.ARCHIVE)).blocks
    owners = {row["id"]: row for row in draft["records"] if row["kind"] == "system"}
    records = []
    defaults = {b"FI": b"Hodram", b"FA": b"Bergstrom", b"FO": b"Bergstrom Fleet"}
    maximum = {b"FI": b"W" * 16, b"FA": b"W" * 16, b"FO": b"W" * 20}
    for group in proof["groups"]:
        block = group["block"]
        assert native.digest(bank[block]) == group["after"]
        for command in group["commands"]:
            raw = bytes.fromhex(command["stored"])
            if command["word"] != 0x4000 or raw[5] != 254:
                continue
            ident, = command["record_ids"]
            owner = owners.pop(ident)
            at = command["stored_offset"]
            assert raw[:6] == bytes.fromhex("0040ffff00fe")
            assert raw.hex() == owner["current_reference"]["exact_command_hex"] == command["current"]
            assert bank[block][at:at+len(raw)] == raw
            stop = raw.index(0, 6)
            assert not any(raw[stop:])
            body = raw[6:stop]
            tokens = TOKEN.findall(body)
            assert set(tokens) <= defaults.keys()
            widths = {}
            for name, mapping in (("default", defaults), ("maximum", maximum)) if tokens else (("default", defaults),):
                expanded = TOKEN.sub(lambda match: mapping[match[0]], body)
                page = paint(expanded)
                assert page["complete_consumed_bytes"] == len(expanded), (ident, name)
                plane = page["physical"]
                assert all(not any(plane[y*228+216:(y+1)*228]) for y in range(64)), (ident, name)
                events = page["events"]
                assert all(e["kind"] == "ascii" and 0 <= e["code"] < 128 for e in events), (ident, name)
                assert all(e["y"] in range(0, 64, 12) for e in events), (ident, name)
                actual = [bytes(e["code"] for e in events if e["y"] == y).strip(b" ")
                          for y in range(0, 64, 12)]
                assert b"".join(b"".join(actual).split()) == b"".join(expanded.split()), (ident, name)
                membership = dict(actual_rows=[row.decode("ascii") for row in actual],
                    stored_rows=expanded.decode("ascii").split("\n"), complete_nonspace_glyph_sequence=True)
                widths[name] = dict(expanded_hex=expanded.hex(), membership=membership,
                    physical_plane_sha256=native.digest(plane), physical_plane_hex=plane.hex())
            records.append(dict(route=1, block=block, id=ident, second_page=False, stored_offset=at,
                exact_command_hex=raw.hex(), physical_plane_hex=widths["default"]["physical_plane_hex"], layouts=widths))
    assert len(records) == 50 and not owners
    base.save(stage.FE_PROOF, dict(candidate_sha256=candidate, records=records, sheets=[],
        original_modal_consumer=True, complete_stored_page_count=len(records), retained_macro_bytes_exact=True,
        runtime_assets_match_predecessor=True))
    print("Verified 50 retained speakerless commands and applicable name widths.")


def formatting():
    glyphs = typed.previous.verification.glyphs
    if not GLYPHS.exists():
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    if not stage.FE_PROOF.exists():
        retained_panels()
    if not CHOICES.exists():
        choice_source = checked_text(typed.choice_source, {
            'len(choices) == 8': 'len(choices) == 2',
            'Verified all eight original choice captions, slots and complete objects.':
                'Verified both original choice captions and the complete native choice command.',
        })
        local = vars(typed) | globals()
        exec(compile(choice_source, __file__ + "::choice-captions", "exec"), local)
        local["check_choices"]()
    if not ROLES.exists():
        local = nameplates.scope | dict(PROOF=ROLES, NOTES=NOTES, parent=stage.parent,
            stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
            display=SimpleNamespace(PROOF=stage.NATIVE), assets=compiler.display.ASSETS)
        exec(compile(nameplates.source, __file__ + "::speaker-roles", "exec"), local)
        local["main"]()


def samples():
    return {1: tuple((row["block"], int(row["id"].rsplit("R", 1)[1]))
        for row in base.load(stage.REVIEW)["records"]
        if row["id"] == MODAL_SAMPLE or (row["decision"] == "revision" and row["block"] != 167))}


def route_rom(route):
    return ROOT / f"route{route}/Hodram_Late_Midroute_FOCUSED_ONLY.nds"


def choice_paths(block):
    directory = ROOT / f"b{block}_choice"
    return directory, directory / f"Hodram_B{block}_Choice_FOCUSED_ONLY.nds", directory / "fixture.json"


def report(run):
    return ROOT / run / "capture/capture_report.json"


scope = prior.scope | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)
exec(compile(prior.previous.prepare_source, __file__ + "::original-choice-suffix", "exec"), scope)
branch_frames = FunctionType(branch.branch_frames.__code__, globals())
play_choice = FunctionType(branch.play_choice.__code__, branch.play_choice.__globals__ | globals())
checked = SimpleNamespace(CHOICES=CHOICES)
source = checked_text(prior.source, {
    '            row = source[record_id(block, ordinal)]\n'
    '            width, plane = branch_fixture.panel_mask(row, bodies, modals, ctx, paint, font)':
        '''            page_index = None
            if isinstance(ordinal, tuple):
                ordinal, page_index = ordinal
            row = source[record_id(block, ordinal)]
            if page_index is None:
                width, plane = branch_fixture.panel_mask(row, bodies, modals, ctx, paint, font)
            else:
                assert (block, ordinal) == (167, 122)
                raw = bytes.fromhex(bodies[1, row["id"]]["body_hex"])[1:]
                result = paint(ctx.arm, font, raw)
                assert result["complete_consumed_bytes"] == len(raw) and len(result["pages"]) == 2
                width = 216
                plane = bytes.fromhex(result["pages"][page_index]["native_plane_hex"])
'''.rstrip(),
    'observations.append(branch_fixture.observation(row, run, hold, bodies[1, row["id"]]["command_offset"]))':
        'observation = branch_fixture.observation(row, run, hold, bodies[1, row["id"]]["command_offset"])\n'
        '            observations.append(observation | {"page_number":1 + (page_index or 0)})',
    '[record_id(block, v) for v in responses]': '[record_id(block, v[0] if isinstance(v, tuple) else v) for v in responses]',
    "hodram_midroute_menus_": "hodram_late_midroute_menus_",
})
exec(compile(source, __file__ + "::choice-gameplay", "exec"), globals())


def verify():
    observations, pictures, reports, exits = scope["verify_excerpts"]()
    branch_observations, choices, menu_reports, sheets = verify_branches()
    observations.extend(branch_observations)
    reports.update(menu_reports)
    for offset in range(0, len(pictures), 6):
        path, digest = gameplay.make_sheet(ROOT / f"hodram_late_midroute_excerpts_{1+offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=digest))
    revisions = {row["id"] for row in base.load(stage.REVIEW)["records"] if row["decision"] == "revision"}
    assert revisions <= {row["id"] for row in observations}
    assert len(choices) == 2 and len(observations) == 39
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, report_sha256=reports, return_frames=exits, original_menu_choices=choices,
        sheets=sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(observations)} focused holds and both original ship-lesson outcomes.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "replay", "prepare_choice", "verify", *RUNS))
    action = cli.parse_args().action
    scope["SAMPLES"] = samples()
    if action == "replay":
        scope["replay"](1)
    elif action == "prepare_choice":
        scope["prepare_choice"](167)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
