"""Inventory mutations in patch-owned resident storage after real screen transitions."""

import json
import hashlib
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/patch_interaction_audit_20261027')


def unexpected(addresses, owners):
    return [a for a in addresses if not any(lo <= a < hi for lo, hi in owners)]


def spans(offsets):
    result = []
    for offset in offsets:
        if result and offset == result[-1][1]:
            result[-1][1] += 1
        else:
            result.append([offset, offset + 1])
    return result


def main():
    target = json.loads((ROOT / 'target.json').read_text())
    rom_path = Path(target['ROM'])
    assert hashlib.sha256(rom_path.read_bytes()).hexdigest() == target['sha256']
    sections = MainCodeFile(NdsImage.open(rom_path).read_file('/__arm9__.bin'), 0x02000000).sections
    clean_sections = MainCodeFile(NdsImage.open(Path('work/clean.nds')).read_file('/__arm9__.bin'), 0x02000000).sections
    clean = clean_sections[0]
    main_bytes = bytes(sections[0].data)
    patched = [i for i, (a,b) in enumerate(zip(clean.data, main_bytes)) if a != b]
    old_itcm = bytes(sections[1].data)
    old_itcm_patched = [i for i,b in enumerate(old_itcm) if i >= len(clean_sections[1].data) or b != clean_sections[1].data[i]]
    assert sections[2].data == clean_sections[2].data, 'DTCM patch ownership requires review'
    manifest = json.loads(rom_path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    metadata = manifest['relocations']['/__arm9__.bin']
    square = metadata['square_shop_labels']
    stock = metadata['town_stock_rows']
    owners = {
        'ITCM': [(0x01FFC2D8, 0x01FFC2DC), (0x01FFC680, 0x01FFC684)],
        'pool': [(square['buffers'], square['buffers']+square['slot_bytes']*square['slots'])],
        # Five captured rows and one count are writable. The trailing self-pointer
        # is an immutable literal and deliberately excluded.
        'main_patched': [(stock['cache'], stock['cache']+24)],
        'old_ITCM_patched': [],
    }
    itcm = bytes(sections[4].data)
    # The original private-market constructor owns one cached native-new image.
    # Bind the exception to the actual allocation, store instruction and literal.
    assert struct.unpack_from('<I',itcm,0x194)[0] == 0x01FFC680
    assert struct.unpack_from('<I',itcm,0x6c)[0] == 0xE58A8000
    assert struct.unpack_from('<I',itcm,0x28)[0] == 0xE3A00A01
    pool = bytes(sections[3].data[:-48])
    cases = {}
    totals = {kind:set() for kind in owners}
    for case in sorted((ROOT / 'cases').iterdir()):
        capture = case / 'capture'
        if not capture.exists():
            continue
        records = []
        for state in sorted(p for p in capture.iterdir() if p.is_dir() and 'native_state_' in p.name):
            frame = int(state.name.rsplit('_', 1)[1])
            complete_itcm = (state / 'arm9_itcm.bin').read_bytes()
            native = complete_itcm[0x4000:0x5000]
            ram = (capture / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
            resident = ram[POOL-0x02000000:POOL-0x02000000+len(pool)]
            changed = {'ITCM': [i for i,(a,b) in enumerate(zip(itcm,native)) if a!=b],
                       'pool': [i for i,(a,b) in enumerate(zip(pool,resident)) if a!=b],
                       'main_patched': [i for i in patched if ram[i] != main_bytes[i]],
                       'old_ITCM_patched': [i for i in old_itcm_patched if complete_itcm[i] != old_itcm[i]]}
            assert len(native) == len(itcm) and len(resident) == len(pool) and len(ram) == 0x400000
            # Do not interpret pre-startup unmapped/uncopied bytes as corruption.
            if frame < 2000:
                continue
            market_pointer = struct.unpack_from('<I',native,0x680)[0]
            footer_pointer = struct.unpack_from('<I',native,0x2D8)[0]
            if footer_pointer:
                assert POOL+len(pool) <= footer_pointer < footer_pointer+1792 <= 0x023E0000
            if market_pointer:
                assert POOL+len(pool) <= market_pointer < market_pointer+4096 <= 0x023E0000
                header = struct.unpack_from('<5I',ram,market_pointer-0x02000000)
                assert header[:3] == (4,46,36) and header[4] == 32
                assert (market_pointer+header[3]) & 0xFFFFFFFF == 0x02125A20
            if footer_pointer and market_pointer:
                assert footer_pointer+1792 <= market_pointer or market_pointer+4096 <= footer_pointer
            for kind, offsets in changed.items():
                base = {'ITCM': 0x01FFC000, 'pool': POOL, 'main_patched':0x02000000, 'old_ITCM_patched':0x01FF8000}[kind]
                totals[kind].update(base+i for i in offsets)
            records.append(dict(frame=frame,
                ITCM_changed_ranges=[[0x01FFC000+a,0x01FFC000+b] for a,b in spans(changed['ITCM'])],
                pool_changed_ranges=[[POOL+a,POOL+b] for a,b in spans(changed['pool'])],
                main_patched_changed_ranges=[[0x02000000+a,0x02000000+b] for a,b in spans(changed['main_patched'])],
                old_ITCM_patched_changed_ranges=[[0x01FF8000+a,0x01FF8000+b] for a,b in spans(changed['old_ITCM_patched'])]))
        if records:
            cases[case.name] = records
    invalid = {kind:spans(unexpected(sorted(rows), owners[kind])) for kind,rows in totals.items()}
    assert not any(invalid.values()), invalid
    # Negative controls prove that instruction/literal changes are rejected while
    # the three explicit mutable allocations are accepted. They do not modify ROM/RAM.
    for kind, addresses in {'ITCM':[0x01FFC200,0x01FFC388], 'pool':[POOL],
                            'main_patched':[0x02000000+patched[0],stock['cache']+24],
                            'old_ITCM_patched':[0x01FF8000+old_itcm_patched[0]]}.items():
        assert unexpected(addresses, owners[kind]) == addresses
    assert all(not unexpected([lo,hi-1], [ (lo,hi) ]) for spans_ in owners.values() for lo,hi in spans_)
    result = dict(ROM_sha256=target['sha256'], cases=cases,
        compared_bytes_per_snapshot=dict(ITCM=len(itcm),pool=len(pool),main_patched=len(patched),old_ITCM_patched=len(old_itcm_patched)),
        mutable_owners=owners, unexpected_mutations=invalid, negative_controls_passed=True,
        union_ranges={kind:spans(sorted(rows)) for kind,rows in totals.items()},
        scope='Same-frame snapshots only; mutable exceptions are two cached heap-pointer words, eighteen Square bitmap slots and six town-stock cache words. No full-playthrough claim.')
    (ROOT / 'runtime_storage_mutations.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Cases inspected:',len(cases))
    for kind, rows in result['union_ranges'].items():
        print(kind, len(rows),'mutation ranges; all within',[(hex(a),hex(b)) for a,b in owners[kind]])


if __name__ == '__main__':
    main()
