"""Bind retired source C-string slots to their preserved active replacements."""

import inspect
import re
import struct
from pathlib import Path

from dk4tool.patch import deck_filter_help, shipyard_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.village_portrait_wrap import PREFIX, paragraph
from dk4tool.patch.village_port_consistency import aligned_paragraph
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import BASE, CURRENT, ROOT, units
from scripts.verify_village_wrap_v608 import read, save
import scripts.probe_shipyard_runtime_v759 as prototype


def cstring_in_units(rom_units, pointer):
    matching = [(raw, pointer - base) for _, base, raw in rom_units if base <= pointer < base + len(raw)]
    assert len(matching) == 1, hex(pointer)
    raw, at = matching[0]
    end = raw.find(b'\0', at)
    assert end >= at
    return raw[at:end]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, current = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    source, arm = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    assert sha(arm) == owned.SOURCE
    current_units = units(current)
    village = read('translations/village_promised_words_manuscript_v1.json')
    assert len(village['records']) == 54
    regions, replacements = [], []
    for row in village['records']:
        lo = row['source_pointer']
        old = bytes.fromhex(row['source_hex']) + b'\0'
        hi = (lo + len(old) + 3) // 4 * 4
        assert source[lo - BASE:lo - BASE + len(old)] == old
        assert arm[lo - BASE:lo - BASE + len(old)] == old
        assert set(source[lo - BASE + len(old):hi - BASE]) <= {0}
        assert arm[lo - BASE:hi - BASE] == source[lo - BASE:hi - BASE]
        old_pointer = struct.unpack_from('<I', source, row['field'])[0]
        new_pointer = struct.unpack_from('<I', arm, row['field'])[0]
        assert old_pointer == lo and new_pointer != old_pointer
        replacement = cstring_in_units(current_units, new_pointer)
        expected = bytes.fromhex(row['compiled_hex'])
        if row['kind'] == 'CLUE':
            expected = aligned_paragraph(PREFIX + row['english'] + '.')[len(PREFIX):-1].encode('ascii')
        elif row['kind'] == 'MESSAGE' and row['index'] not in (1, 5):
            expected = paragraph(row['english']).encode('ascii')
        assert replacement == expected, row['id']
        replacements.append({'id': row['id'], 'pointer_field': row['field'], 'original_pointer': lo,
                             'active_pointer': new_pointer, 'active_complete_text_hex': replacement.hex()})
        if any(a <= lo < hi <= b for a, b in owned.BANKS):
            regions.append({'id': row['id'], 'lo': lo, 'hi': hi, 'source_hex': arm[lo - BASE:hi - BASE].hex()})
    batch = read('translations/common_submenus_arm9_v1.json')
    deck_rows = [r for r in batch['records'] if r['id'] in ('DK4_DECK_HELP_INTRO', 'DK4_DECK_HELP_ROOMS', 'DK4_DECK_HELP_REQUIREMENTS')]
    assert len(deck_rows) == 3
    for row, spec in zip(deck_rows, deck_filter_help.SPECS[2:], strict=True):
        field, offset, japanese, previous, english = spec
        old = bytes.fromhex(row['source_hex'])
        assert row['offset'] == offset and source[offset:offset + len(old)] == old
        expected = (previous.encode('ascii') + b'\0').ljust(len(old), b'\0')
        assert arm[offset:offset + len(old)] == expected
        pointer = struct.unpack_from('<I', arm, field)[0]
        assert pointer != BASE + offset
        if field == 0x1559C:
            english = 'Each duty needs certain abilities. Navigators must meet its requirements. Higher ability makes them more effective.'
        encoded = deck_filter_help.compiled(field, english, 2).encode('ascii')
        assert cstring_in_units(current_units, pointer) == encoded
        replacements.append({'id': row['id'], 'pointer_field': field, 'original_pointer': BASE + offset,
                             'active_pointer': pointer, 'active_complete_text_hex': encoded.hex()})
        regions.append({'id': row['id'], 'lo': BASE + offset, 'hi': BASE + offset + len(old), 'source_hex': expected.hex()})
    for lo, hi in owned.BANKS:
        rows = sorted((r for r in regions if lo <= r['lo'] < r['hi'] <= hi), key=lambda r: r['lo'])
        assert rows and rows[0]['lo'] == lo and rows[-1]['hi'] == hi
        assert all(a['hi'] == b['lo'] for a, b in zip(rows, rows[1:]))
    aliases, branches, adr, crossing_text, preceding_metadata = [], [], [], [], []
    for name, base, raw in current_units:
        for match in re.finditer(rb'(?=(...\x02))', raw, flags=re.DOTALL):
            target = int.from_bytes(match.group(1), 'little')
            if any(lo <= target < hi for lo, hi in owned.BANKS):
                aliases.append([name, base + match.start(), target])
            if not BASE + 0x130000 <= target < BASE + 0x171E48:
                continue
            end = arm.find(b'\0', target - BASE, min(target - BASE + 1024, len(arm)))
            if end < 0:
                continue
            crossed = [[lo, hi] for lo, hi in owned.BANKS if target < lo <= BASE + end]
            if not crossed:
                continue
            candidate = arm[target - BASE:end]
            try:
                decoded = candidate.decode('cp932')
                textual = bool(decoded) and all(ord(c) >= 32 or c in '\n\r\t' for c in decoded)
            except UnicodeError:
                textual = False
            row = [name, base + match.start(), target, BASE + end + 1, crossed]
            if textual:
                crossing_text.append(row)
            else:
                # Do not label vtables/pointer arrays as C strings merely
                # because their next zero occurs in an adjacent text slot.
                preceding_metadata.append(row)
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if word & 0x0E000000 == 0x0A000000:
                delta = word & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                target = base + at + 8 + delta * 4
                if any(lo <= target < hi for lo, hi in owned.BANKS):
                    branches.append([name, base + at, target])
            # ADD/SUB immediate with PC base: original ARM ADR-style constants.
            if word & 0x0E0F0000 == 0x020F0000 and (word >> 21) & 15 in (2, 4):
                imm = word & 255
                shift = ((word >> 8) & 15) * 2
                value = ((imm >> shift) | (imm << (32 - shift))) & 0xFFFFFFFF if shift else imm
                target = base + at + 8 + (value if (word >> 21) & 15 == 4 else -value)
                if any(lo <= target < hi for lo, hi in owned.BANKS):
                    adr.append([name, base + at, target])
    assert aliases == branches == adr == crossing_text == [], (aliases, branches, adr, crossing_text)
    # Assembly is instruction-for-instruction identical to the verified source;
    # only symbolic placements in this module differ.
    assert inspect.getsource(owned.assemble) == inspect.getsource(prototype.assemble)
    blobs = owned.assemble(arm)
    for address, raw in blobs.items():
        assert any(lo <= address < address + len(raw) <= hi for lo, hi in owned.BANKS)
    save(ROOT / 'owned_source_storage.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
         'owned_banks': list(owned.BANKS), 'complete_const_string_allocations': regions,
         'all54_village_and3_Deck_active_replacements_verified': replacements,
         'all_current_unaligned_absolute_aliases_into_banks': aliases, 'all_current_aligned_ARM_branches_into_banks': branches,
         'all_current_ARM_ADR_effective_targets_into_banks': adr, 'all_current_Cstrings_crossing_bank_start': crossing_text,
         'preceding_nontext_metadata_kept_outside_exact_const_slots': preceding_metadata,
         'assembler_equal_verified_V759_apart_from_symbolic_placement': True,
         'blob_lengths': {hex(a): len(b) for a, b in blobs.items()},
         'excluded_active_race_string_source_start': 0x02138162,
         'excluded_old_source_clue6_instruction_coincidence': [0x0202FBDC, 0x0202FBE4],
         'limits': 'Pointer and ADR ownership of mapped immutable constant slots and complete registered replacements. Native write-watch, exact runtime outputs, startup/cache/loading and actual gameplay are subsequent gates; no arbitrary global non-use claim.',
         'producer_sha256': sha(Path(__file__).read_bytes()), 'module_sha256': sha(Path(owned.__file__).read_bytes()),
         'no_ROM_or_storage_change_yet': True})
    print(f'{len(regions)} complete retired constant allocations cover four source banks. All57 active replacements preserved; no alias, branch, ADR or crossing C-string owner. Prototype fits without section/pool growth.', flush=True)


if __name__ == '__main__':
    main()
