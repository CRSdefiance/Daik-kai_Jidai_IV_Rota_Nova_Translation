"""Observe the newly reviewed early Hodram dialogue and choice displays."""

import sys
from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
from types import SimpleNamespace

from scripts import headless_desmume_v193 as harness
from scripts import replay_hodram_early_confrontations_20261119 as host
from scripts import replay_rafael_B261_B280_20261122 as template
from scripts import verify_hodram_opening_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = display.base, display.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
ALIASES = ROOT / "verified_full_header.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (24, 12), (25, 8), (25, 16), (27, 9), (41, "style10"),
    (42, 27), (42, 31), (42, 34), (42, 62), (42, 76), (42, 82), (42, 86), (42, 90),
    (42, 93), (42, 96), (42, 100), (42, 113), (42, 120),
    (44, 6), (44, 14), (44, 37), (44, 41), (44, 49), (44, 79), (44, 84), (44, 111),
    (46, 10), (46, 14), (46, 19), (47, 13), (48, 6), (48, 11), (48, 14),
    (49, 43), (49, "574"), (49, 58), (49, 64), (49, 81), (50, 7), (50, 13),
    (52, 6), (52, "68"), (52, 33), (53, 7),
)
schedule = template.schedule
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))


def replay():
    assert not ROOT.exists()
    stage_report, proof = map(base.load, (writer.PROOF, host.HISTORICAL))
    candidate = base.digest(writer.ROM)
    assert candidate == stage_report["candidate_sha256"] and stage_report["whole_parent_inverse"]
    image = base.NdsImage.open(writer.ROM)
    archive = image.read_file(PATH)
    bank = native.IlnkContainer.parse(archive)
    opening = bank.blocks[host.ENTRY]
    prelude = b"".join(bytes.fromhex(row["whole_command_hex"]) for row in proof["original_initializers"])
    leave = bytes.fromhex(proof["source_bound_QA_host_exit_hex"])
    assert opening[8:8 + len(prelude)] == prelude
    assert opening[writer.logical_end(opening) - len(leave):writer.logical_end(opening)] == leave
    groups = {group["block"]: group for group in stage_report["groups"]}
    compiled, copied = [], []
    logical = bytearray(opening[:8] + prelude)
    for block, index in SELECTED:
        group = groups[block]
        owner = bank.blocks[block]
        assert native.digest(owner) == group["after"]
        if isinstance(index, int):
            ident = f"DK4_MES_B{block}_R{index:04d}"
            command, = [r for r in group["commands"] if r["word"] == 0x4000 and r["record_ids"] == [ident]]
            plan = group["plans"].get(ident)
        elif index.startswith("style"):
            command, = [r for r in group["commands"] if r["word"] == 0x4100 and r["source_offset"] == int(index[5:])]
            plan = None
        else:
            command, = [r for r in group["commands"] if r["word"] in (0x2100, 0x2200)
                        and any(f"_CHOICE_{index}_" in ident for ident in r["record_ids"])]
            plan = None
        raw, at = bytes.fromhex(command["stored"]), command["stored_offset"]
        assert owner[at:at + len(raw)] == raw
        copied.append(dict(block=block, ids=command["record_ids"], fixture_offset=len(logical), actual_block_offset=at,
                           word=command["word"], hex=raw.hex()))
        compiled.append(command | {"stored_offset": len(logical), "plan": plan, "fixture_block": block})
        logical.extend(raw)
    logical.extend(leave)
    pack_into("<H", logical, 4, len(logical) - 8)
    body = bytes(logical) + bytes(-len(logical) % 4)
    assert len(body) < proof["source_bound_QA_block_limit"]
    inventory, _, _ = native.scoped_inventory()
    parsed, _ = inventory(image.read_file(native.ARM), body)
    indexed = {row["offset"]: row["whole_command_hex"] for row in parsed}
    assert all(indexed[row["fixture_offset"]] == row["hex"] for row in copied)
    bank.blocks[host.ENTRY] = body
    image.replace_file(PATH, bank.to_bytes())
    ROOT.mkdir()
    rom = ROOT / "Hodram_B24_B53_FOCUSED_ONLY.nds"
    image.save(rom)
    inverse = base.NdsImage.open(rom)
    inverse.replace_file(PATH, archive)
    assert bytes(inverse.rom.save()) == writer.ROM.read_bytes()
    events, requests, frames = schedule(compiled)
    inputs = ROOT / "inputs.json"
    initial = base.load(Path("work/analysis/papal_trade_route_runs_v7625/route1/ordinary_NewGame_inputs.json"))
    assert sum(event["buttons"] == ["RIGHT"] for event in initial) == 1 and max(event["start"] for event in initial) <= 2200
    base.save(inputs, initial + events)
    base.save(ROOT / "fixture.json", dict(candidate_sha256=candidate, fixture_ROM=str(rom), fixture_ROM_sha256=base.digest(rom),
        original_prelude=prelude.hex(), copied=copied, requested_holds=requests, end=frames, exact_candidate_inverse=True,
        original_story_branches_unexecuted=True, natural_activation=False,
        source_entry_proof=str(host.HISTORICAL), source_entry_proof_sha256=base.digest(host.HISTORICAL)))
    holds = [frame for request in requests for frame in request["holds"]] + [frames - 1]
    sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(REPORT.parent), "--frames", str(frames),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, holds)]
    harness.main()


previous_check = template.check
check = checked_text(previous_check, {
    'assert bank[44][8:40].hex() == fixture["original_prelude"]':
        'prelude = bytes.fromhex(fixture["original_prelude"])\n'
        '    assert bank[host.ENTRY][8:8 + len(prelude)] == prelude',
    '[(261, 0), (261, 1), (261, 2), (261, 0), (261, 1)]': '[(49, 0), (49, 1), (52, 0), (52, 1)]',
    '["DK4_MES_B261_R0148", "DK4_MES_B261_R0152", "DK4_MES_B261_R0155"]':
        '["DK4_MES_B42_R0093", "DK4_MES_B42_R0096", "DK4_MES_B42_R0100"]',
    'len(holds) == len(expected_speech) + 2': 'len(holds) == len(expected_speech) + 1',
    'sum("_STYLE_" in hold["id"] for hold in holds) == 2': 'sum("_STYLE_" in hold["id"] for hold in holds) == 1',
    '"Sailor" if item["word"] == 0x4100 else row["speaker"]':
        '"Sailor" if item["word"] == 0x4100 else display.CONTEXT_SHORT_NAMES.get(ident, (None, row["speaker"]))[1]',
    'rafael_B261_B280_gameplay_': 'hodram_B24_B53_gameplay_',
})
scope = template.scope | globals()
exec(compile(check, __file__ + "::focused-Hodram-replay-verification", "exec"), scope)


def aliases():
    from PIL import Image

    previous = base.load(PROOF)
    source = base.NdsImage.open(writer.ROM)
    rows = [row for row in previous["holds"] if row["id"] in display.CONTEXT_SHORT_NAMES]
    assert [row["id"] for row in rows] == ["DK4_MES_B44_R0084"]
    panel, town = scope["panel"], scope["town"]
    font = panel.GameAsciiFont.from_arm9(source.read_file(native.ARM))
    results = []
    for row in rows:
        recorded, displayed = display.CONTEXT_SHORT_NAMES[row["id"]]
        assert row["speaker"] in (recorded, displayed)
        shot = row["observed"]
        assert base.digest(shot["path"]) == shot["PNG_sha256"]
        with Image.open(shot["path"]) as image:
            panel.complete_mask(font, displayed, image.convert("RGB"), 16, 277, town.INKS[1])
        results.append(dict(id=row["id"], older_contextual_label=recorded, displayed_label=displayed, frame=shot))
    base.save(ALIASES, dict(candidate_sha256=previous["candidate_sha256"], gameplay_report_sha256=base.digest(PROOF),
                            records=results, exact_full_nameplate_glyphs=True))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check", "aliases"))
    action = parser.parse_args().action
    (aliases if action == "aliases" else scope[action])()
