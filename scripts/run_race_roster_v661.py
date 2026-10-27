"""Isolated Grand Race UI packet/ready fixtures; never a wireless peer test."""

import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/race_roster_v661')
OUT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/race_roster_v661_controlled')
BASE = 0x02000000


def main():
    ring_mode = '--ring' in sys.argv
    output = OUT.with_name(OUT.name + '_ring') if ring_mode else OUT
    suffix = '_ring' if ring_mode else ''
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    names = []
    for i in range(3):
        p = struct.unpack_from('<I', arm, 0x120B80 + i * 32)[0] - BASE
        name = arm[p:p + 17].split(b'\0')[0]
        assert name == (b'Rafael', b'Hodram', b'Lil')[i]
        names.append(name)
    events, original, frame = [], {}, 0
    loader = ct.CDLL

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if not str(path).lower().endswith('desmume_libretro.dll'):
            return core
        core.retro_get_memory_data.argtypes = [ct.c_uint]
        core.retro_get_memory_data.restype = ct.c_void_p
        core.retro_get_memory_size.argtypes = [ct.c_uint]
        core.retro_get_memory_size.restype = ct.c_size_t
        real_run = core.retro_run
        real_run.restype = None

        def run():
            nonlocal frame
            frame += 1
            if 4401 <= frame <= 4601:
                pointer = core.retro_get_memory_data(2)
                assert pointer and core.retro_get_memory_size(2) == 0x400000
                raw = ct.string_at(pointer, 0x400000)
                assert struct.unpack_from('<H', raw, 0x37BBC0 + 0x810)[0] == 52
                assert raw[0x37B640:0x37B642] == b'\x0f\x00'
                if frame == 4401:
                    assert raw[0x192820:0x192824] == struct.pack('<I', 0x0216B0E4)
                    fields = ([(0x0237BBC0 + i * 512, 212) for i in range(4)] + [(0x0237D9F0, 2)]
                              if ring_mode else [(0x0237B642, 2), (0x0237B678, 156), (0x0237D9F0, 2)])
                    for address, size in fields:
                        original[address] = raw[address - BASE:address - BASE + size]
                    save(ROOT / ('fixture_before' + suffix + '.json'), {
                        'frame': frame, 'RAM_sha256': sha(raw),
                        'fields': {hex(a): b.hex() for a, b in original.items()},
                        'source_names': [n.decode('ascii') for n in names]})
                updates = {}
                if frame <= 4600:
                    packets = bytearray()
                    own = raw[0x37B644:0x37B678]
                    assert struct.unpack_from('<I', own, 8)[0] == 3
                    for index, name in enumerate(names):
                        packet = bytearray(own)
                        struct.pack_into('<I', packet, 8, index)
                        packet[16:33] = name.ljust(17, b'\0')
                        packet[33:52] = f'Test Ship {index + 2}'.encode('ascii').ljust(19, b'\0')
                        packets.extend(packet)
                    updates = {0x0237B642: struct.pack('<H', 15), 0x0237B678: bytes(packets),
                               0x0237D9F0: struct.pack('<H', 2 if frame >= 4501 else 0)}
                    if ring_mode:
                        received = struct.pack('<2H', 15, 15) + own + packets
                        assert len(received) == 212
                        updates = {0x0237BBC0 + i * 512: bytes(received) for i in range(4)}
                        updates[0x0237D9F0] = struct.pack('<H', 2 if frame >= 4501 else 0)
                else:
                    updates = original
                changed = []
                for address, value in updates.items():
                    before = raw[address - BASE:address - BASE + len(value)]
                    ct.memmove(pointer + address - BASE, value, len(value))
                    changed.append({'address': address, 'bytes': len(value),
                                    'before_sha256': sha(before), 'after_sha256': sha(value)})
                events.append({'before_frame': frame, 'writes': changed})
            real_run()

        core.retro_run = run
        return core

    inputs = read(ROOT / 'host_inputs.json') + [{'start': 4801, 'duration': 8, 'buttons': ['B']}]
    save(ROOT / ('controlled_inputs' + suffix + '.json'), inputs)
    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(output),
        '--frames', '5000', '--inputs-json', str(ROOT / ('controlled_inputs' + suffix + '.json')),
        '--battery-save', pre['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', str(ROOT / 'current_unlock_manifest.json'),
        '--capture-every', '999999', '--capture-at', '4400', '4450', '4490', '4550', '4590', '4690', '5000',
        '--dump-capture-ram', '--capture-native-state-at', '4490', '4590']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        save(ROOT / ('roster_fixture_events' + suffix + '.json'), {'synthetic_packet_fixture': True,
            'original_receive_ring_fixture': ring_mode,
            'synthetic_readiness_fixture': True, 'wireless_peer_verified': False,
            'test_ship_names_are_fixture_labels': True, 'ROM_changed': False,
            'events': events, 'final_frame': frame})
    assert frame == 5000 and len(events) == 201
    print('V661 terminal controlled UI run; no wireless or race-completion credit.', flush=True)


if __name__ == '__main__':
    main()
