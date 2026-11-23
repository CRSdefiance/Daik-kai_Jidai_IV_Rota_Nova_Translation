"""Replay both original tutorial choice paths with the revised text."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
import sys

from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from scripts import run_Rafael_B46_scenes_v7945 as workflow
from scripts import stage_rafael_sailing_modes_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "play"
FIXTURE = ROOT / "Rafael_Sailing_Choices_RESEARCH_ONLY.nds"
FIXTURES = ROOT / "fixtures.json"
FILE = "/data/SC0.DK4"
FRAMES = 10401


def prepare():
    assert not ROOT.exists()
    stored = base.load(stage.PROOF)
    assert stored["candidate_sha256"] == base.digest(stage.ROM)
    earlier = base.load(workflow.FIXTURES)
    historic, = (r for r in earlier["fixtures"] if r["version"] == "English")
    original = base.NdsImage.open(stage.ROM)
    arm = original.read_file(native.ARM)
    raw_file = original.read_file(FILE)
    archive = native.IlnkContainer.parse(raw_file)
    host, lesson = (archive.blocks[n] for n in (44, 46))
    prelude = bytes.fromhex(historic["original_opening_prelude_hex"])
    assert host[8:40] == prelude and len(prelude) == 32
    assert (host[:4], host[6:8]) == (lesson[:4], lesson[6:8])
    logical = bytearray(host[:8] + prelude + lesson[8:stage.logical_end(lesson)])
    pack_into("<H", logical, 4, len(logical) - 8)
    fixture = bytes(logical) + bytes(-len(logical) % 4)
    inventory, _, _ = native.scoped_inventory()
    commands, speeches = inventory(arm, fixture)
    _, host_speeches = inventory(arm, host)
    assert host_speeches[0]["offset"] == 40
    assert len(commands) == 47 and len(speeches) == 24
    assert commands[-1]["word"] == 0 and commands[-1]["offset"] + 4 == len(logical)
    group, = stored["groups"]
    assert native.digest(lesson) == group["after"]
    records, menu, command_ids = [], [], []
    for row, parsed in zip(group["commands"], commands[10:], strict=True):
        at = row["stored_offset"] + 32
        raw = bytes.fromhex(row["stored"])
        word = row["word"]
        ids = row["record_ids"]
        assert parsed["offset"] == at and parsed["word"] == word
        parsed_raw = bytes.fromhex(parsed["whole_command_hex"])
        assert raw == fixture[at:at+len(raw)]
        if word == 0x100:
            assert len(raw) == 4 and parsed_raw.startswith(raw)
        else:
            assert parsed_raw == raw
        command_ids.append(dict(offset=at, source_offset=row["source_offset"], word=word, ids=ids))
        if word == 0x4000:
            ident, = ids
            records.append(dict(id=ident, source_selector=raw[5], fixture_command_offset=at))
        elif word == 0x2100:
            count, start = count_and_base(raw)
            assert len(ids) == count == 2
            for i, (ident, caption) in enumerate(zip(ids, labels(raw), strict=True)):
                offset = at + start + unpack_from("<H", raw, 2 + 2*i)[0]
                assert fixture[offset:offset+len(caption)+1] == caption + b"\0"
                menu.append(dict(id=ident, option_index=i, label=caption.decode("ascii"), offset=offset))
    assert [r["label"] for r in menu] == ["Please do.", "No, thanks."]
    assert len(records) == 24 and len(command_ids) == 37
    ROOT.mkdir()
    archive.blocks[44] = fixture
    original.replace_file(FILE, archive.to_bytes())
    original.save(FIXTURE)
    deployed = base.NdsImage.open(FIXTURE)
    archive.blocks[44] = host
    assert archive.to_bytes() == raw_file
    deployed.replace_file(FILE, raw_file)
    assert bytes(deployed.rom.save()) == stage.ROM.read_bytes()
    base.save(FIXTURES, dict(candidate_sha256=stored["candidate_sha256"],
        fixtures=[dict(route=0, version="English", source_file=FILE, research_ROM=str(FIXTURE),
            research_ROM_sha256=base.digest(FIXTURE), original_menu_records=menu,
            original_text_records=records, command_ids=command_ids, all_fixture_commands=commands,
            disclosure="Original block 46 runs after the preserved block 44 New Game prelude.")],
        historical_input_fixture_sha256=base.digest(workflow.FIXTURES),
        exact_candidate_inverse=True, natural_activation=False, hardware=False))
    print("Prepared the entire sailing tutorial behind the original Rafael prelude.")


def capture(choice):
    recipe = checked_text(Path(workflow.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B46_scene_runs_v7945')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B46_scene_fixtures_v7944/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_FIXTURES",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B46_route{route}_{version}_{choice}_v7945'":
            "cap=folder/'capture'",
        "range(2350,16001,60))|{16000,*MENU_SNAPSHOT_FRAMES}":
            "range(2350,FRAME_LIMIT,45))|{FRAME_LIMIT-1,*MENU_SNAPSHOT_FRAMES}",
        "'16001'": "str(FRAME_LIMIT)",
        "16001": "FRAME_LIMIT",
    })
    env = {"__name__": "__main__", "__file__": __file__, "ACTIVE_ROOT": ROOT, "ACTIVE_FIXTURES": FIXTURES,
           "FRAME_LIMIT": FRAMES if choice == "accept" else 6501}
    prior = sys.argv
    try:
        sys.argv = [__file__, "--route", "0", "--version", "English", "--choice", choice]
        if choice == "decline":
            sys.argv += ["--down-frame", "4900"]
        exec(compile(recipe, __file__ + "::original-choice-replay", "exec"), env)
    finally:
        sys.argv = prior


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "accept", "decline"))
    action = parser.parse_args().action
    prepare() if action == "prepare" else capture(action)
