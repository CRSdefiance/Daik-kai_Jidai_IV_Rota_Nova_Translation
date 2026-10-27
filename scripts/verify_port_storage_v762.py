"""Revalidate two retired-bank tails against the complete current component."""

import re
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

from dk4tool.patch import port_services_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS, DISPATCH, FIRST_WIDTH, LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import units
from scripts.probe_port_services_v761 import assemble as research_assemble
from scripts.verify_shipyard_storage_v760 import cstring_in_units
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/port_services_v762')
CURRENT = Path('out/all_routes_combined_v760_candidate.nds')
FREE = ((owned.PREFIX, owned.PREFIX + 16), (owned.TAIL, owned.TAIL + 80))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT); arm = rom.read_file('/__arm9__.bin')
    assert sha(arm) == owned.SOURCE
    prior = read('work/analysis/shipyard_storage_v760/owned_source_storage.json')
    plan = read('work/analysis/shipyard_storage_v760/runtime_plan.json')
    arm9_units = units(rom)
    current = arm9_units + [('ARM7', rom.rom.arm7RamAddress, bytes(rom.rom.arm7))]
    assert prior['owned_banks'] == [list(p) for p in BANKS]
    assert len(prior['all54_village_and3_Deck_active_replacements_verified']) == 57
    for row in prior['all54_village_and3_Deck_active_replacements_verified']:
        assert struct.unpack_from('<I', arm, row['pointer_field'])[0] == row['active_pointer']
        assert cstring_in_units(arm9_units, row['active_pointer']).hex() == row['active_complete_text_hex']
    # Every new byte lies in an exactly mapped retired allocation, outside all
    # executable/data bytes introduced by the complete V760 component.
    old_patches = read('work/analysis/shipyard_storage_v760/registered_verification.json')['proof']['owned_runtime']['patches']
    for lo, hi in FREE:
        assert any(a <= lo < hi <= b for a, b in BANKS)
        regions = prior['complete_const_string_allocations']
        assert all(any(r['lo'] <= at < r['hi'] for r in regions) for at in range(lo, hi))
        assert all(not (lo < p['address'] + len(bytes.fromhex(p['target_hex'])) and p['address'] < hi) for p in old_patches)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    # Prefix tail follows the final unconditional B of the width adapter. The
    # literal routine returns before its literal word; that word targets the
    # existing Thumb balance helper, and cannot fall through into the new tail.
    end_width = next(cs.disasm(arm[FIRST_WIDTH + 24 - owned.BASE:FIRST_WIDTH + 28 - owned.BASE], FIRST_WIDTH + 24))
    assert end_width.mnemonic == 'b' and int(end_width.op_str.removeprefix('#'), 16) == 0x0213B9CC
    instructions = list(cs.disasm(arm[LITERAL - owned.BASE:LITERAL - owned.BASE + 132], LITERAL))
    assert instructions[-1].mnemonic == 'pop' and 'pc' in instructions[-1].op_str
    assert struct.unpack_from('<I', arm, LITERAL + 132 - owned.BASE)[0] == 0x02147AE5
    aliases, branches, adr, crossing, metadata = [], [], [], [], []
    for name, base, raw in current:
        for match in re.finditer(rb'(?=(...\x02))', raw, flags=re.DOTALL):
            target = int.from_bytes(match.group(1), 'little')
            if any(lo <= target < hi for lo, hi in FREE): aliases.append([name, base + match.start(), target])
            if not owned.BASE + 0x130000 <= target < 0x02171E48: continue
            end = arm.find(b'\0', target - owned.BASE, min(len(arm), target - owned.BASE + 1024))
            if end < 0 or not any(target < lo <= owned.BASE + end for lo, _ in FREE): continue
            try:
                text = arm[target - owned.BASE:end].decode('cp932')
                is_text = bool(text) and all(ord(c) >= 32 or c in '\n\r\t' for c in text)
            except UnicodeError:
                is_text = False
            row = [name, base + match.start(), target, owned.BASE + end + 1]
            (crossing if is_text else metadata).append(row)
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if word & 0x0E000000 == 0x0A000000:
                delta = word & 0xFFFFFF
                if delta & 0x800000: delta -= 0x1000000
                target = base + at + 8 + delta * 4
                if any(lo <= target < hi for lo, hi in FREE): branches.append([name, base + at, target])
            if word & 0x0E0F0000 == 0x020F0000 and (word >> 21) & 15 in (2, 4):
                imm, shift = word & 255, ((word >> 8) & 15) * 2
                value = ((imm >> shift) | (imm << (32 - shift))) & 0xFFFFFFFF if shift else imm
                target = base + at + 8 + (value if (word >> 21) & 15 == 4 else -value)
                if any(lo <= target < hi for lo, hi in FREE): adr.append([name, base + at, target])
    assert aliases == branches == adr == crossing == [], (aliases, branches, adr, crossing)
    blobs = owned.assemble(); assert blobs == research_assemble()
    assert arm[DISPATCH - owned.BASE:DISPATCH - owned.BASE + 4] == blobs[owned.PREFIX][:4]
    save(owned.OWNERSHIP, {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
        'free_spans_with_retired_source_allocation_ownership': [list(p) for p in FREE],
        'prior_full_bank_proof_sha256': sha(Path('work/analysis/shipyard_storage_v760/owned_source_storage.json').read_bytes()),
        'all57_active_replacements_current_and_prior_source_ownership_verified': True,
        'all_current_sections_overlays_and_ARM7_included': True,
        'free_span_absolute_aliases': aliases, 'free_span_ARM_branches': branches, 'free_span_ADR': adr,
        'crossing_Cstrings': crossing, 'nontext_metadata_crossing_strings_not_assumed': metadata,
        'preceding_unconditional_branch_return_and_literal_pool_verified': True,
        'source_patch_spans': {hex(at): arm[at - owned.BASE:at - owned.BASE + len(raw)].hex() for at, raw in blobs.items()},
        'module_sha256': sha(Path(owned.__file__).read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'native_write_watch_and_actual_loading_still_required': True})
    target, runtime = owned.runtime_transform(arm)
    (ROOT / 'research_runtime_ARM9.bin').write_bytes(target)
    save(ROOT / 'runtime_plan.json', runtime)
    print('96 retired-bank bytes owned;57 active replacements preserved;no current alias/branch/ADR/crossing-string owner;no fallthrough or growth.', flush=True)


if __name__ == '__main__': main()
