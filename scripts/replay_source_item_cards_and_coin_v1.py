"""Replay the original coin prompt and Baby Shark acquisition card."""

import argparse
import inspect
from pathlib import Path
from types import SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from scripts import replay_shark_encounter_v1 as shark
from scripts import replay_shark_encounter_v2 as initialized
from scripts import replay_shark_encounter_v4 as selected
from scripts import stage_source_item_cards_and_coin_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


COIN_DIR = stage.ROOT / 'coin_fixture'
COIN_ROM = COIN_DIR / 'coin_RESEARCH_ONLY.nds'
SHARK_DIR = stage.ROOT / 'baby_shark'


def baby_shark():
    source = checked_text(inspect.getsource(shark.replay), {
        'out = stage.ROOT / choice': 'out = SHARK_DIR',
    })
    env = vars(shark) | dict(stage=SimpleNamespace(ROM=stage.ROM, PROOF=stage.PREP, ROOT=stage.ROOT),
        SHARK_DIR=SHARK_DIR, FINAL=selected.FINAL, fixture_controller=initialized.fixture_controller,
        commands=lambda choice: selected.commands())
    exec(compile(source, __file__ + '::same-original-baby-shark-card', 'exec'), env)
    env['replay']('raise')


def coin_fixture():
    assert not COIN_DIR.exists()
    proof = stage.load(stage.PREP)
    assert stage.digest(stage.ROM) == proof['research_ROM_sha256']
    path = '/data/SC0.DK4'
    clean, target = map(stage.NdsImage.open, ('work/clean.nds', stage.ROM))
    clean_blocks = IlnkContainer.parse(clean.read_file(path)).blocks
    command = clean_blocks[178][388:390]
    assert command == bytes.fromhex('01c1') and clean_blocks[44][26:28] == bytes.fromhex('0049')
    archive = IlnkContainer.parse(target.read_file(path))
    assert archive.blocks[44][26:28] == clean_blocks[44][26:28]
    blocks = list(archive.blocks)
    blocks[44] = blocks[44][:26] + command + blocks[44][28:]
    target.replace_file(path, IlnkContainer(blocks).to_bytes())
    COIN_DIR.mkdir()
    target.save(COIN_ROM)
    fixture = stage.NdsImage.open(COIN_ROM)
    original = stage.NdsImage.open(stage.ROM)
    prior_files, next_files = ({name: data for _, name, data in rom.iter_files()} for rom in (original, fixture))
    assert prior_files.keys() == next_files.keys()
    assert [name for name, data in prior_files.items() if next_files[name] != data] == [path]
    assert dict(original.iter_components()) == dict(fixture.iter_components())
    stage.save(COIN_DIR / 'fixture.json', dict(staged_ROM_sha256=proof['research_ROM_sha256'],
        research_ROM=str(COIN_ROM), research_ROM_sha256=stage.digest(COIN_ROM), changed_file=path,
        block=44, block_offset=26, original_hex='0049', fixture_hex=command.hex(),
        command_source='Clean SC0 block 178 at byte 388', natural_recruitment=False))
    print(COIN_ROM)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('shark', 'coin-fixture'))
    (baby_shark if parser.parse_args().action == 'shark' else coin_fixture)()

