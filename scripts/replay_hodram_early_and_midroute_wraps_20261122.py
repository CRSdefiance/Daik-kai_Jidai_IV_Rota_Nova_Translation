"""Verify Hodram's revised wording and both paths through his original menus."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_hodram_and_lil_followups_20261122 as prior
from scripts import stage_hodram_early_and_midroute_wraps_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, menu = stage.base, stage.native, prior.menu
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
SAMPLES = {1: (
    (5, 11), (6, 11), (7, 5), (15, 87), (15, 168), (15, 171), (23, 12), (26, 28), (56, 10), (56, 13),
    (72, 33), (73, 35), (75, 51), (76, 9), (76, 43), (78, 41), (79, 45), (84, 27), (84, 158),
    (87, 45), (87, 62), (87, 93), (89, 11), (91, 42), (91, 72), (91, 84), (91, 87), (91, 103), (91, 106),
    (95, 12), (95, 35), (95, 38),
)}
PROMPTS = {87: 27, 91: 13}
RESPONSES = {87: (42, 98), 91: (27, 94)}
RUNS = tuple(f"b{block}_{branch}" for block in PROMPTS for branch in ("accept", "refuse"))
HOLDS = (3900, 4300, 4970, 5350)


def route_rom(route):
    return ROOT / f"route{route}" / "Hodram_Early_And_Midroute_FOCUSED_ONLY.nds"


def report(run):
    return ROOT / run / "capture/capture_report.json"


def choice_paths(block):
    root = ROOT / f"b{block}_choice"
    return root, root / f"Hodram_B{block}_Choice_FOCUSED_ONLY.nds", root / "fixture.json"


def run_block(run):
    return int(run.split("_", 1)[0][1:])


scope = vars(prior) | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    original = getattr(prior, name)
    scope[name] = FunctionType(original.__code__, scope)

prepare_source = checked_text(getsource(prior.prepare_choice), {
    "def prepare_choice():": "def prepare_choice(block):\n    CHOICE_ROOT, CHOICE_ROM, CHOICE_RECEIPT = choice_paths(block)",
    '(row["route"], row["block"]) == (2, 133)': '(row["route"], row["block"]) == (1, block)',
    "route_config(2)": "route_config(1)",
    "archive.blocks[133]": "archive.blocks[block]",
    "record_id(133, 145)": "record_id(block, PROMPTS[block])",
    "exact_contiguous_suffix_source_block=133": "exact_contiguous_suffix_source_block=block",
})
play_source = checked_text(getsource(prior.play_choice), {
    "    fixture = base.load(CHOICE_RECEIPT)":
        "    _, CHOICE_ROM, CHOICE_RECEIPT = choice_paths(run_block(run))\n    fixture = base.load(CHOICE_RECEIPT)",
    '[(4000, "A"), (4340, "A"), (5050, "A"), (5440, "A")]': '[(4000, "A"), (5050, "A")]',
    'if run == "refuse":\n        steps.insert(2, (4770, "DOWN"))':
        'if run.endswith("_refuse"):\n        steps.insert(1, (4770, "DOWN"))',
    "base.load(INPUTS[2])": "base.load(INPUTS[1])",
})
for source in (prepare_source, play_source):
    exec(compile(source, __file__ + "::choice-fixtures", "exec"), scope)


def formatting():
    check = prior.checks
    if GLYPHS.exists():
        prior_glyphs = base.load(GLYPHS)
        assert prior_glyphs["candidate_sha256"] == base.digest(stage.ROM)
        assert base.load(stage.NATIVE)["stage_sha256"] == base.digest(stage.PROOF)
    else:
        FunctionType(check.check_glyphs.__code__, check.check_glyphs.__globals__ | dict(stage=stage, OUTPUT=GLYPHS))()
    modal_source = checked_text(getsource(check.check_modal), {
        '            body = raw[6:raw.index(0, 6)]\n            page = paint(body)':
            '''            stored_body = raw[6:raw.index(0, 6)]
            body = stored_body
            widest = None
            if b"FI" in stored_body:
                assert ident in ("DK4_MES_B91_R0084", "DK4_MES_B91_R0103")
                assert stored_body.count(b"FI") == 1
                body = stored_body.replace(b"FI", b"Hodram")
                maximum = stored_body.replace(b"FI", b"W" * 16)
                wide_page = paint(maximum)
                assert wide_page["complete_consumed_bytes"] == len(maximum)
                wide_plane = wide_page["physical"]
                assert all(not any(wide_plane[y*228+216:(y+1)*228]) for y in range(64))
                widescreen = b"".join(wide_plane[y*228:y*228+216] for y in range(64))
                pictures.append((f"SC{route} {ident} / maximum FI width", widescreen))
                spacer_events = []
                if ident == "DK4_MES_B91_R0103":
                    assert maximum == b"W" * 16 + b"'s Spirit rose by 1! "
                    spacer_events = [e for e in wide_page["events"] if e["y"] != 0]
                    assert [(e["kind"], e["code"], e["x"], e["y"]) for e in spacer_events] == [
                        ("ascii", 32, 0, 12), ("ascii", 32, 6, 12)]
                    assert not any(wide_plane[12*228:])
                    printable_page = wide_page | {"events": [e for e in wide_page["events"] if e["y"] == 0]}
                else:
                    printable_page = wide_page
                widest = dict(body_hex=maximum.hex(), native_blank_spacers=spacer_events,
                              row_membership=stage.typed.forest.system.check_FE_rows(maximum, printable_page),
                              physical_plane_sha256=native.digest(wide_plane))
            page = paint(body)''',
        'physical_plane_sha256=native.digest(plane), physical_plane_hex=plane.hex()))':
            'physical_plane_sha256=native.digest(plane), physical_plane_hex=plane.hex(),\n'
            '                display_body_hex=body.hex(), maximum_name=widest))',
        'assert len(records) == 10 and sum(r["second_page"] for r in records) == 2':
            'assert len(records) == 20 and not any(r["second_page"] for r in records)\n'
            '    assert sum(r["maximum_name"] is not None for r in records) == 2',
        'Verified all ten modal pages, including both original two-page Maria sequences.':
            'Verified the twenty original Hodram notices and two maximum-name layout cases.',
    })
    modal_scope = vars(check) | {"stage": stage}
    exec(compile(modal_source, __file__ + "::modal-verification", "exec"), modal_scope)
    modal_scope["check_modal"]()


def verify_choices(proof, draft, layout):
    candidate = proof["candidate_sha256"]
    image = base.NdsImage.open(stage.ROM)
    arc = image.read_file("/data/SC1.DK4")
    bank = native.IlnkContainer.parse(arc)
    assert layout["candidate_sha256"] == candidate == base.digest(stage.ROM)
    ctx, paint, font, names = scope["display_context"]()
    pages = {(r["route"], r["id"]):r for r in layout["records"]}
    owners = {r["id"]:r for r in draft["records"]}
    captions, observations, pictures, reports, choices, objects = [], [], [], {}, [], {}
    for block, responses in RESPONSES.items():
        _, rom, path = choice_paths(block)
        fixture = base.load(path)
        assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"] and not fixture["natural_activation"]
        group, = [r for r in proof["groups"] if (r["route"], r["block"]) == (1, block)]
        payload = bank.blocks[block]
        choice, = [c for c in group["commands"] if c["word"] == 0x2100]
        raw, start = bytes.fromhex(choice["stored"]), choice["stored_offset"]
        assert choice["current"] == choice["stored"] and payload[start:start+len(raw)] == raw
        texts = []
        for slot, row in enumerate(r for r in draft["retained_choice_labels"] if r["current_reference"]["block"] == block):
            ref = row["current_reference"]
            offset = start + ref["offset"] - ref["command_offset"]
            body = bytes.fromhex(ref["exact_body_hex"])
            assert row["slot"] == slot and raw.hex() == ref["exact_command_hex"]
            assert payload[offset:offset+len(body)+1] == body+b"\x00" and body.decode("ascii") == row["english"]
            ref = dict(file_path=group["file_path"], block=block, candidate_sha256=candidate,
                archive_sha256=native.digest(arc), block_sha256=group["after"], command_offset=start,
                offset=offset, exact_command_hex=raw.hex(), exact_body_hex=body.hex())
            captions.append(row | dict(registered_reference=ref, review=row["review"] | dict(formatting=True)))
            texts.append(row["english"])
        assert len(texts) == 2
        objects[block] = dict(exact_retained_choice_object=raw.hex(), fixture=fixture,
                              preserved_relative_branches=fixture["preserved_relative_branches"])
        for selection, (branch, ordinal) in enumerate(zip(("accept", "refuse"), responses, strict=True)):
            run = f"b{block}_{branch}"
            capture = base.load(report(run))
            prior.verify_capture(capture, rom, fixture["rom_sha256"], report(run).parent.parent / "inputs.json")
            reports[run] = base.digest(report(run))
            options = []
            for frame in (4300, 4970):
                hold, view = menu.gameplay.screen(capture, frame)
                options.append(dict(capture=hold, labels=menu.gameplay.captions(names, view, texts)))
                if frame == 4970:
                    pictures.append((f"B{block} / {branch} choice", view))
            first, final = [[item["background"] for item in look["labels"]] for look in options]
            assert first[0] == menu.gameplay.MENU_HIGHLIGHT and first[1] != menu.gameplay.MENU_HIGHLIGHT
            assert final == (first[::-1] if selection else first)
            ident = prior.record_id(block, ordinal)
            row = owners[ident]
            hold, view = menu.gameplay.screen(capture, 5350)
            width, plane = prior.panel_mask(row, pages, {}, ctx, paint, font)
            assert menu.gameplay.mask_check(plane, width, view), (run, ident)
            menu.gameplay.glyphs(names, view, row["speaker"], (16, 277), menu.gameplay.LABEL_COLOR, 226)
            cmd, = [c for c in group["commands"] if ident in c["record_ids"]]
            observations.append(prior.observation(row, run, hold, cmd["stored_offset"]))
            pictures.append((f"B{block} / {branch} response / {row['speaker']}", view))
            choices.append(dict(run=run, block=block, selected=selection, caption=texts[selection],
                response=ident, original_branch_executed=True, observations=options))
    base.save(stage.CHOICE_PROOF, dict(candidate_sha256=candidate, captions=captions, original_choice_consumer=True,
        choice_objects=objects, both_branches_observed=True))
    return observations, pictures, reports, choices


def verify():
    proof, draft, layout = map(base.load, (stage.PROOF, stage.REVIEW, stage.NATIVE))
    observations, pictures, reports, exits = scope["verify_excerpts"]()
    branches, images, branch_reports, choices = verify_choices(proof, draft, layout)
    observations.extend(branches)
    pictures.extend(images)
    reports.update(branch_reports)
    sheets = []
    for offset in range(0, len(pictures), 6):
        path, digest = menu.gameplay.make_sheet(ROOT / f"hodram_early_and_midroute_gameplay_{1+offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=digest))
    base.save(LIVE, dict(candidate_sha256=proof["candidate_sha256"], observed_speech_pages=len(observations),
        observations=observations, report_sha256=reports, return_frames=exits, original_menu_choices=choices,
        sheets=sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(observations)} focused holds, four native choices and the host exit.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "formatting", "prepare_choices", "verify", *RUNS))
    action = cli.parse_args().action
    if action == "replay":
        scope["replay"](1)
    elif action == "prepare_choices":
        for block in PROMPTS:
            scope["prepare_choice"](block)
    elif action in RUNS:
        scope["play_choice"](action)
    else:
        globals()[action]()
