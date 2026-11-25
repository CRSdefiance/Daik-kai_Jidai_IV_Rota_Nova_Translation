"""Compare the mutiny dialogue through the original progressive story display."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import replay_london_stockholm_dialogue_20261115 as startup
from scripts import stage_aziza_mutiny_dialogue_20261115 as stage
from scripts.replay_ritual_officiant_labels_20261115 import INPUTS as RAFAEL_INPUTS


base, ROOT = stage.base, stage.ROOT
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = (RAFAEL_INPUTS, Path('out/hodram_opening_wraps_20261114_v2/inputs.json'))
HOSTS = ((44, 40), (42, 42))
ORDINALS = ((20, 21, 22, 23, 24), (10, 22, 23, 24, 25))
PULSES = range(4000, 5500, 300)
HOLDS = (3900, 4230, 4530, 4830, 5130)
FRAMES = (2200, 2800, *HOLDS, 5700, 6000)
END = 6001


def prepare(route, side, folder):
    info = base.load(stage.STORED)
    assert base.digest(stage.REVIEW) == info['review_sha256']
    rom, expected = (stage.parent.ROM, info['previous_sha256']) if side == 'before' else (
        stage.ROM, info['candidate_sha256'])
    assert base.digest(rom) == expected
    image, clean = map(base.NdsImage.open, (rom, stage.CLEAN))
    arm = image.read_file(stage.ARM)
    path = f'/data/SC{route}.DK4'
    archive = image.read_file(path)
    blocks = stage.IlnkContainer.parse(archive).blocks
    clean_blocks = stage.IlnkContainer.parse(clean.read_file(path)).blocks
    host, end = HOSTS[route]
    block = stage.ROUTES[route][1]
    opening, scene = blocks[host], blocks[block]
    host_exit = 8 + unpack_from('<H', opening, 4)[0]
    clean_end = 8 + unpack_from('<H', clean_blocks[host], 4)[0]
    expected_exit = (bytes(4), bytes.fromhex('00c200000000'))[route]
    footer = opening[host_exit - len(expected_exit):host_exit]
    assert footer == clean_blocks[host][clean_end - len(expected_exit):clean_end] == expected_exit
    assert opening[8:end] == clean_blocks[host][8:end]
    inventory, _, _ = stage.scoped_inventory()
    commands, spoken = stage.raw_speeches(arm, scene, inventory)
    index = {row['offset']: row for row in commands}
    chosen = [index[spoken[i]['offset'] - 5] for i in ORDINALS[route]]
    assert all(row['word'] == 0x4000 for row in chosen)
    fixture = bytearray(opening[:end] + b''.join(bytes.fromhex(row['whole_command_hex']) for row in chosen) + footer)
    pack_into('<H', fixture, 4, len(fixture) - 8)
    packed = bytes(fixture) + bytes(-len(fixture) % 4)
    wrapped, shown = stage.raw_speeches(arm, packed, inventory)
    assert [r['raw_hex'] for r in shown] == [spoken[i]['raw_hex'] for i in ORDINALS[route]]
    assert [r['whole_command_hex'] for r in wrapped if r['word'] == 0x4000] == [r['whole_command_hex'] for r in chosen]
    blocks[host] = packed
    image.replace_file(path, stage.IlnkContainer(blocks).to_bytes())
    scratch = folder / 'initialized_dialogue_RESEARCH_ONLY.nds'
    image.save(scratch)
    image.replace_file(path, archive)
    assert bytes(image.rom.save()) == rom.read_bytes()
    return scratch, {'candidate_sha256': expected, 'fixture_sha256': base.digest(scratch), 'source_route': route,
                     'source_block': block, 'source_block_sha256': stage.sha(scene), 'host_block': host,
                     'real_complete_commands': chosen, 'speech_rows': [spoken[i] for i in ORDINALS[route]],
                     'whole_candidate_inverse': True, 'initialized_only': True}


def replay(route, side):
    folder = ROOT / f'SC{route}_{side}'
    folder.mkdir()
    scratch, result = prepare(route, side, folder)
    inputs = folder / 'inputs.json'
    flow = [row for row in base.load(INPUTS[route]) if row['start'] <= 2200]
    flow.extend({'start': frame, 'duration': 5, 'buttons': ['A']} for frame in PULSES)
    base.save(inputs, flow)
    original_argv = sys.argv
    try:
        sys.argv = [harness.__file__, '--rom', str(scratch), '--out', str(folder / 'capture'), '--frames', str(END),
                    '--inputs-json', str(inputs), '--press-start', '-1', '--capture-every', '999999',
                    '--capture-at', *map(str, FRAMES)]
        harness.main()
    finally:
        sys.argv = original_argv
    path = folder / 'capture/capture_report.json'
    report = base.load(path)
    assert report['frames'] == END and report['scripted_input_schedule'] == flow
    assert report['ROM_sha256'] == result['fixture_sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    base.save(folder / 'fixture.json', result | {'capture_report': str(path), 'capture_sha256': base.digest(path)})


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('startup', 'before', 'after'))
    parser.add_argument('--route', type=int, choices=(0, 1), default=0)
    options = parser.parse_args()
    if options.mode == 'startup':
        FunctionType(startup.cold_boot.__code__, startup.cold_boot.__globals__ | {'stage': stage})()
    else:
        replay(options.route, options.mode)
