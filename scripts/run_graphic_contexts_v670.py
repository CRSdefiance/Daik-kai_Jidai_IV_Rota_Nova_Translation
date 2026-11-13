"""Trace actual crew and isolated Grand Race UI through the unchanged observer."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.observe_graphic_paints_v669 import Observer
from scripts.prepare_graphic_contexts_v670 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('crew', 'race'), required=True)
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['observer_source']).read_bytes()) == pre['observer_source_sha256']
    assert sha(Path(pre['observer_contract']).read_bytes()) == pre['observer_contract_sha256']
    config = read(ROOT / 'run_cases.json')['cases'][args.case]
    for key in ('inputs', 'donor'):
        assert sha(Path(config[key]).read_bytes()) == config[key + '_sha256']
    folder = CAP / f"graphic_contexts_v670_{args.case}_{'baseline' if args.baseline else 'observed'}"
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': args.case, 'baseline': args.baseline,
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'], 'config': config,
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'race_uses_retained_receive_ring_and_readiness_UI_fixture_not_wireless': args.case == 'race'})
    loader, installed, frame, originals, events = ct.CDLL, [], 0, {}, []
    arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    names = []
    if args.case == 'race':
        for i, expected in enumerate((b'Rafael', b'Hodram', b'Lil')):
            pointer = struct.unpack_from('<I', arm, 0x120B80 + i * 32)[0] - BASE
            name = arm[pointer:pointer + 17].split(b'\0')[0]
            assert name == expected
            names.append(name)

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if not str(path).lower().endswith('desmume_libretro.dll'):
            return core
        observer = None if args.baseline else Observer(core, folder / 'observer')
        if observer:
            observer.install()
            installed.append(observer)
        core.retro_get_memory_data.argtypes, core.retro_get_memory_data.restype = [ct.c_uint], ct.c_void_p
        core.retro_get_memory_size.argtypes, core.retro_get_memory_size.restype = [ct.c_uint], ct.c_size_t
        original_run = core.retro_run
        original_run.restype = None

        def run():
            nonlocal frame
            frame += 1
            if args.case == 'race' and 4401 <= frame <= 4601:
                pointer = core.retro_get_memory_data(2)
                assert pointer and core.retro_get_memory_size(2) == 0x400000
                raw = ct.string_at(pointer, 0x400000)
                assert struct.unpack_from('<H', raw, 0x37BBC0 + 0x810)[0] == 52
                assert raw[0x37B640:0x37B642] == b'\x0f\x00'
                if frame == 4401:
                    assert raw[0x192820:0x192824] == struct.pack('<I', 0x0216B0E4)
                    for address, size in [(0x0237BBC0 + i * 512, 212) for i in range(4)] + [(0x0237D9F0, 2)]:
                        originals[address] = raw[address - BASE:address - BASE + size]
                if frame <= 4600:
                    own = raw[0x37B644:0x37B678]
                    assert struct.unpack_from('<I', own, 8)[0] == 3
                    packets = bytearray()
                    for index, name in enumerate(names):
                        packet = bytearray(own)
                        struct.pack_into('<I', packet, 8, index)
                        packet[16:33] = name.ljust(17, b'\0')
                        packet[33:52] = f'Test Ship {index + 2}'.encode('ascii').ljust(19, b'\0')
                        packets.extend(packet)
                    received = struct.pack('<2H', 15, 15) + own + packets
                    assert len(received) == 212
                    updates = {0x0237BBC0 + i * 512: bytes(received) for i in range(4)}
                    updates[0x0237D9F0] = struct.pack('<H', 2 if frame >= 4501 else 0)
                else:
                    updates = originals
                changed = []
                after = bytearray(raw)
                for address, value in updates.items():
                    ct.memmove(pointer + address - BASE, value, len(value))
                    after[address - BASE:address - BASE + len(value)] = value
                    changed.append({'address': address, 'bytes': len(value),
                        'before_sha256': sha(raw[address - BASE:address - BASE + len(value)]), 'after_sha256': sha(value)})
                assert ct.string_at(pointer, 0x400000) == bytes(after)
                events.append({'before_frame': frame, 'writes': changed,
                    'only_declared_ring_payloads_and_readiness_halfword_changed': True})
            if observer:
                observer.next_frame()
            original_run()
        core.retro_run = run
        return core

    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--battery-save', config['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, config['capture_frames'])]
    if args.case == 'race':
        sys.argv += ['--allow-gallery-fixtures', '--gallery-save-fixture-manifest', config['gallery_unlock_manifest']]
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
        save(folder / 'fixture_events.json', {'case': args.case, 'final_frame': frame, 'events': events,
            'synthetic_packet_and_readiness_UI_fixture': args.case == 'race',
            'originals': {hex(a): b.hex() for a, b in originals.items()},
            'wireless_or_race_outcome_verified': False, 'no_gameplay_fixtures_for_crew': args.case == 'crew'})
    for observer in installed:
        observer.save()
    assert frame == config['frames'] and len(events) == (201 if args.case == 'race' else 0)
    print('V670 terminal:', args.case, 'observer:', not args.baseline, flush=True)


if __name__ == '__main__':
    main()
