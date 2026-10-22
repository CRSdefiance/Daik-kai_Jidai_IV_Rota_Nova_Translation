"""Bind exact owner boundaries with complete original resource initialization."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.trace_control_aliases_v688 import ROOT, TARGETS
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    versions = []
    for version, path in [('source', 'work/clean.nds'),
                          ('current', 'out/all_routes_combined_v685_candidate.nds')]:
        rom = NdsImage.open(path)
        u = machine(rom.read_file('/__arm9__.bin'))
        scratch = 0x02443000
        u.mem_write(scratch - 16, b'\xA5' * 52)
        constructor_words = bytes(u.mem_read(0x020D6C74, 24))
        assert constructor_words == bytes.fromhex('042080e2042080e508109fe5082080e5001080e51eff2fe1')
        executed = call(u, 0xD6C74, (scratch,))
        assert len(executed) == 6
        words = struct.unpack('<5I', u.mem_read(scratch, 20))
        assert words[1:3] == (scratch + 4, scratch + 4)
        assert words[3:] == (0xA5A5A5A5, 0xA5A5A5A5)
        assert bytes(u.mem_read(scratch - 16, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(scratch + 20, 16)) == b'\xA5' * 16
        writes = []

        def observe(_u, _access, address, size, value, _data, writes=writes):
            for label, (owner, extent) in TARGETS.items():
                if owner - 20 <= address < owner + extent + 20:
                    writes.append({'target_window': label, 'address': address,
                                   'size': size, 'value': value})

        handle = u.hook_add(UC_HOOK_MEM_WRITE, observe)
        try:
            initialized = call(u, 0x10E190, (), instruction_limit=100000)
        finally:
            u.hook_del(handle)
        owners = []
        for label, (owner, size) in TARGETS.items():
            assert size == 20
            actual = bytes(u.mem_read(owner, size))
            fields = struct.unpack('<5I', actual)
            assert fields[1:3] == (owner + 4, owner + 4) and fields[4] == 0xFFFFFFFF
            filename = bytes(u.mem_read(fields[3], 128)).split(b'\0')[0].decode('ascii')
            expected = '_pxl/kakutei.pxl' if label == 'Confirm' else '_pxl/__frame.pxl'
            assert filename == expected
            owned = [r for r in writes if owner <= r['address'] < owner + size]
            assert [r['address'] - owner for r in owned] == [4, 8, 0, 0, 12, 16]
            assert all(r['size'] == 4 for r in owned)
            adjacent = struct.unpack('<5I', u.mem_read(owner + 20, 20))
            adjacent_name = bytes(u.mem_read(adjacent[3], 128)).split(b'\0')[0].decode('ascii')
            assert adjacent[1:3] == (owner + 24, owner + 24) and adjacent[4] == 0xFFFFFFFF
            if label == 'Confirm':
                assert adjacent_name == '_pxl/plate4016.pxl'
            owners.append({'label': label, 'owner': owner, 'extent': size,
                'five_initialized_words': fields, 'filename': filename,
                'native_owned_writes': owned, 'adjacent_separate_owner': owner + 20,
                'adjacent_filename': adjacent_name,
                'neighbor_is_not_a_field_or_parent_of_this_resource': True})
        versions.append({'version': version, 'ROM': path, 'ROM_sha256': sha(Path(path).read_bytes()),
            'constructor_guarded_native_six_instructions_pass': True,
            'complete_initializer_returns_with_saved_register_stack_ABI': True,
            'initializer_executed_instructions': len(initialized),
            'executed_code_sha256': sha(b''.join(struct.pack('<I', pc) + bytes(u.mem_read(pc, 4))
                                                for pc in sorted(initialized))),
            'owners': owners, 'all_observed_target_and_neighbor_writes': writes})
    assert versions[0]['owners'] == versions[1]['owners']
    assert versions[0]['executed_code_sha256'] == versions[1]['executed_code_sha256']
    save(ROOT / 'native_owner_proof.json', {
        'versions': versions, 'complete_original_initializer_no_call_or_loader_bridges': True,
        'target_owners_are20_bytes_next_address_is_distinct_resource': True,
        'initial24_byte_assumption_and_false_neighbor_leads_retained': True,
        'this_is_isolated_native_initialization_not_actual_button_display': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V688 original/current native initializers match: exact20-byte Confirm/Frame owners; neighboring resources excluded.', flush=True)


if __name__ == '__main__':
    main()
