"""Replay the tactics and Pasha dialogue with the original Hodram entry and exit."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
import sys
from types import FunctionType

from scripts import replay_ceuta_lesson_20261119 as inherited
from scripts import run_Rafael_B48_scenes_v8050 as observer
from scripts import stage_hodram_early_confrontations_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "hodram_replay"
STARTUP = build.ROOT / "startup_fixture"
FIXTURE = ROOT / "Hodram_Tactics_and_Pasha_RESEARCH_ONLY.nds"
FIXTURES = ROOT / "fixtures.json"
HISTORICAL = Path("work/Hodram_B0_B41_clean_20261107/wrap_followup_fixtures_v1/hodram_all_hands_wrap_fixture.json")
FILE = "/data/SC1.DK4"
ENTRY = 42
FRAMES = 9901
EXCERPTS = {
    29: (67, 71, 74, 77, 81, 85, 88, 92),
    33: (5,),
    40: (72, 76, 79, 82, 88, 92, 96, 125, 129),
}


def prepare():
    assert not ROOT.exists()
    prior, stored = map(base.load, (HISTORICAL, build.PROOF))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    image = base.NdsImage.open(build.ROM)
    arm, original = image.read_file(native.ARM), image.read_file(FILE)
    bank = native.IlnkContainer.parse(original)
    inventory, _, _ = native.scoped_inventory()
    old = prior["original_initializers"]
    prelude = b"".join(bytes.fromhex(c["whole_command_hex"]) for c in old)
    candidates = [i for i, block in enumerate(bank.blocks) if block[8:8 + len(prelude)] == prelude]
    assert ENTRY in candidates, candidates
    opening = bank.blocks[ENTRY]
    commands, real_speeches = inventory(arm, opening)
    assert real_speeches[0]["offset"] == 8 + len(prelude)
    leave = bytes.fromhex(prior["source_bound_QA_host_exit_hex"])
    assert opening[build.stage.logical_end(opening) - len(leave):build.stage.logical_end(opening)] == leave
    assert [c["word"] for c in commands[-2:]] == [0xC200, 0]
    records = []
    body = bytearray(opening[:real_speeches[0]["offset"]])
    groups = {g["block"]: g for g in stored["groups"]}
    for block, indices in EXCERPTS.items():
        group = groups[block]
        by_id = {ident: c for c in group["commands"] for ident in c["record_ids"]}
        for index in indices:
            ident = f"DK4_MES_B{block}_R{index:04}"
            c = by_id[ident]
            raw = bytes.fromhex(c["stored"])
            start = c["stored_offset"]
            assert c["word"] == 0x4000 and bank.blocks[block][start:start + len(raw)] == raw
            records.append(dict(id=ident, block=block, source_selector=raw[5], offset=len(body),
                stored_command_offset=start, whole_command_hex=raw.hex(), body_hex=raw[6:raw.index(0, 6)].hex()))
            body += raw
    body += leave
    pack_into("<H", body, 4, len(body) - 8)
    fixture = bytes(body) + bytes(-len(body) % 4)
    ops, speeches = inventory(arm, fixture)
    assert len(speeches) == len(records) == 18 and len(ops) == len(old) + len(records) + 2
    assert [c["word"] for c in ops[-2:]] == [0xC200, 0]
    for c, row in zip(speeches, records, strict=True):
        assert c["offset"] == row["offset"] and c["whole_command_hex"] == row["whole_command_hex"]
    assert len(fixture) < prior["source_bound_QA_block_limit"]
    ROOT.mkdir()
    bank.blocks[ENTRY] = fixture
    image.replace_file(FILE, bank.to_bytes())
    image.save(FIXTURE)
    restored = base.NdsImage.open(FIXTURE)
    restored.replace_file(FILE, original)
    assert bytes(restored.rom.save()) == build.ROM.read_bytes()
    base.save(FIXTURES, dict(candidate_sha256=stored["candidate_sha256"], exact_candidate_inverse=True,
        fixtures=[dict(route=1, version="English", source_file=FILE, source_block=40, source_blocks=list(EXCERPTS),
            fixture_block=ENTRY, original_opening_prelude_commands=old, research_ROM=str(FIXTURE),
            research_ROM_sha256=base.digest(FIXTURE), fixture_block_sha256=native.digest(fixture),
            all_fixture_commands=ops, original_text_records=records)],
        source_entry_proof=str(HISTORICAL), source_entry_proof_sha256=base.digest(HISTORICAL),
        natural_activation=False, hardware=False))
    print("Prepared 18 exact speech commands between the original Hodram entry and exit.")


def capture():
    source = checked_text(Path(observer.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B48_scene_runs_v8050')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B48_scene_fixtures_v8049/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_FIXTURES",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B48_route{route}_{version}_v8050'":
            "cap=folder/'capture'",
        "choices=[0],required=True": "choices=[1],required=True",
        "range(4000,39521,240)": "range(4000,FRAME_LIMIT-500,240)",
        "range(2350,40001,60))|{40000}": "range(2350,FRAME_LIMIT,60))|{FRAME_LIMIT-1}",
        "frames=40001": "frames=FRAME_LIMIT",
        "'40001'": "str(FRAME_LIMIT)",
        "report['frames']==40001": "report['frames']==FRAME_LIMIT",
        "original_exchange_commands=163,original_exchange_speeches=91":
            "original_exchange_commands=18,original_exchange_speeches=18",
        ",*map(str,captures),'--dump-ram']": ",*map(str,captures)]",
        "{version}:40001-frame fixture capture terminal": "{version}:{FRAME_LIMIT}-frame fixture capture terminal",
    })
    env = dict(__name__="__main__", __file__=__file__, ACTIVE_ROOT=ROOT, ACTIVE_FIXTURES=FIXTURES, FRAME_LIMIT=FRAMES)
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "1", "--version", "English"]
        exec(compile(source, __file__ + "::hodram-excerpts", "exec"), env)
    finally:
        sys.argv = previous


def startup():
    FunctionType(inherited.startup.__code__, vars(inherited) | {"build": build, "STARTUP": STARTUP})()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
