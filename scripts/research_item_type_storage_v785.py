"""Source-bound letter phrase storage leads, not a production type transform."""

import re
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R4, UC_ARM_REG_R6, UC_ARM_REG_R8, UC_ARM_REG_LR, UC_ARM_REG_PC)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census, CURRENT, ROOT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read, save


def main():
    clean, current = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    source, arm = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    # Exact NUL/padding allocations from the original ten-entry scheme table.
    slots = [(3, 0x0214C538, 8), (0, 0x0214C540, 8), (5, 0x0214C548, 8),
             (1, 0x0214C564, 12), (2, 0x0214C570, 12),
             (4, 0x0214C588, 12), (7, 0x0214C594, 12)]
    labels = []
    for kind, lo, length in slots:
        field = 0x14C5E8+kind*4
        assert struct.unpack_from('<I', source, field)[0] == lo
        raw = source[lo-BASE:lo-BASE+length]
        assert arm[lo-BASE:lo-BASE+length] == raw
        end = raw.index(0)
        assert not any(raw[end:]) and (end+1+3)//4*4 == length
        if kind == 7:
            assert struct.unpack_from('<I', arm, field)[0] == 0x02143B77
            assert arm[0x143B77:0x143B77+13] == b'Forge Papers\0'
        else:
            assert struct.unpack_from('<I', arm, field)[0] == lo
        labels.append({'type': kind, 'span': [lo, lo+length],
            'source_Japanese': raw[:end].decode('cp932'), 'source_hex': raw.hex(),
            'source_pointer_field': BASE+field,
            'current_pointer': struct.unpack_from('<I', arm, field)[0]})
    # Excluded 57C..588 is the original C++ RTTI name and is never owned here.
    assert arm[0x14C57C:0x14C588] == source[0x14C57C:0x14C588] == b'7CScheme\0\0\0\0'

    previous = read('work/analysis/tavern_storage_v764/retired_source_inventory.json')
    replacements = read('work/analysis/shipyard_storage_v760/owned_source_storage.json')
    village = []
    for n, lo in ((3, 0x02147AD0), (6, 0x02147CD8)):
        old = next(r for r in previous['source_allocations'] if r['lo'] == lo)
        hi = old['hi']
        assert arm[lo-BASE:hi-BASE] == source[lo-BASE:hi-BASE]
        assert arm[lo-BASE:lo-BASE+len(bytes.fromhex(old['source_hex']))] == bytes.fromhex(old['source_hex'])
        active = next(r for r in replacements['all54_village_and3_Deck_active_replacements_verified']
                      if r['id'] == f'VILLAGE_CLUE_{n}')
        field = active['pointer_field']
        assert struct.unpack_from('<I', source, field)[0] == lo == active['original_pointer']
        assert struct.unpack_from('<I', arm, field)[0] == active['active_pointer']
        expected = bytes.fromhex(active['active_complete_text_hex'])+b'\0'
        value = next(raw[active['active_pointer']-base:active['active_pointer']-base+len(expected)]
            for _, base, raw in units(current) if base <= active['active_pointer'] < base+len(raw))
        assert value == expected
        village.append({'id': active['id'], 'span': [lo, hi], 'source_hex': arm[lo-BASE:hi-BASE].hex(),
            'complete_active_replacement': active})

    spans = [[0x0214C538, 0x0214C550], [0x0214C564, 0x0214C57C],
             [0x0214C588, 0x0214C5A0], [0x02147AD0, 0x02147AE4], [0x02147CD8, 0x02147D00]]
    references = census(current, spans, [])
    save(ROOT/'type_phrase_storage_raw_leads.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'spans': spans, 'scheme_labels': labels, 'retired_village_spans': village,
        'references': references, 'not_a_free_space_or_production_approval': True})

    # These are the two exact unaligned matches spanning MOV and BL words,
    # rather than data pointers. Execute both original instruction pairs to
    # their original callee; never globally waive unaligned matches.
    controls = []
    cpu = machine(arm)
    disassembler = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for alias, lo, callee in ((0x0204FA9F, 0x0204FA9C, 0x020D4C90),
                              (0x0202FBDF, 0x0202FBDC, 0x020B4DD8)):
        raw = arm[lo-BASE:lo-BASE+8]
        assert raw == source[lo-BASE:lo-BASE+8]
        inst = list(disassembler.disasm(raw, lo))
        assert [i.mnemonic for i in inst] == ['mov', 'bl']
        assert inst[1].op_str == f'#{hex(callee)}'
        regs = {UC_ARM_REG_R0: 0x02430000, UC_ARM_REG_R1: 0x02431000,
                UC_ARM_REG_R2: 0x02432000, UC_ARM_REG_R4: 0x02434000,
                UC_ARM_REG_R6: 0x02436000, UC_ARM_REG_R8: 0x02438000}
        for reg, value in regs.items():
            cpu.reg_write(reg, value)
        before = bytes(cpu.mem_read(BASE, 0x800000))
        hook = cpu.hook_add(UC_HOOK_CODE, lambda c, p, s, d: c.emu_stop(), begin=callee, end=callee)
        try:
            cpu.emu_start(lo, callee+4, count=8)
        finally:
            cpu.hook_del(hook)
        assert cpu.reg_read(UC_ARM_REG_PC) == callee and cpu.reg_read(UC_ARM_REG_LR) == lo+8
        expected = dict(regs)
        expected[UC_ARM_REG_R2 if lo == 0x0204FA9C else UC_ARM_REG_R1] = 1 if lo == 0x0204FA9C else regs[UC_ARM_REG_R6]
        assert all(cpu.reg_read(reg) == value for reg, value in expected.items())
        assert bytes(cpu.mem_read(BASE, 0x800000)) == before
        controls.append({'unaligned_match': alias, 'native_instruction_span': [lo, lo+8],
            'source_current_code_hex': raw.hex(), 'original_callee': callee,
            'arguments_LR_and_whole8MiB_unchanged_except_declared_MOV_destination': True})

    expected_references = sorted([
        ['absolute', 'section0', 0x0214C5E8+kind*4, lo, False]
        for kind, lo, _ in slots if kind != 7]+[
        ['absolute', 'section0', 0x0204FA9F, 0x02147AE3, False],
        ['absolute', 'section0', 0x0202FBDF, 0x02147CE1, False]])
    assert sorted(references) == expected_references, references
    # A proposed complete phrase placement. The six live type0-5 pointer
    # fields still need an atomic registered redirect, and every name-getter
    # consumer/crop must be mapped before this can become production work.
    texts = ['goodwill letter', 'pact proposal', 'pact termination notice',
             'truce proposal', 'declaration of war', 'demand for submission']
    pointers = [0x0214C538, 0x02147CD8, 0x0214C564, 0x02147CE6, 0x02147AD0, 0x0214C588]
    placements = []
    for kind, (pointer, text) in enumerate(zip(pointers, texts)):
        raw = text.encode()+b'\0'
        assert any(lo <= pointer and pointer+len(raw) <= hi for lo, hi in spans)
        placements.append({'type': kind, 'pointer': pointer, 'text': text, 'bytes': len(raw)})
    occupied = sorted((r['pointer'], r['pointer']+r['bytes']) for r in placements)
    assert all(hi <= following for (_, hi), (following, _) in zip(occupied, occupied[1:]))
    assert sum(r['bytes'] for r in placements) == 110
    save(ROOT/'letter_type_localization_DRAFT_v2.json', {
        'source_plan': 'work/analysis/item_diplomacy_editorial_v784/letter_type_localization_DRAFT.json',
        'source_plan_sha256': sha(Path('work/analysis/item_diplomacy_editorial_v784/letter_type_localization_DRAFT.json').read_bytes()),
        'phrases': placements,
        'type2_Japanese': '協定破約',
        'type2_editorial_note': 'Pact termination notice is an idiomatic English document name. It preserves the complete meaning of notice of pact termination, including the notice and the ended pact, and reads naturally after our/this in the reviewed dialogue. No brevity waiver or omitted source meaning.',
        'all_source_meaning_and_naturalness_reviewed': True,
        'all_generic_getter_consumers_crops_and_production_formatting_pending': True})
    save(ROOT/'type_phrase_storage_research.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'scheme_source_labels': labels, 'retired_village_replacements': village,
        'all132_source_owned_bytes': spans, 'proposed110_phrase_bytes': placements,
        'current_exact_six_live_table_references': [r for r in references if 0x0214C5E8 <= r[2] < 0x0214C600],
        'all_current_incoming_reference_leads': references,
        'two_exact_source_instruction_pair_classifications': controls,
        'no_unclassified_direct_reference_leads': True,
        'preserved_RTTI_and_old_strategist_code': True,
        'future_atomic_six_field_redirect_complete_getter_consumer_write_and_crop_closure_pending': True,
        'no_binary_ROM_registry_or_formatting_approval': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('110 complete English phrase bytes fit132 source-bound bytes;two original instruction-pair leads verified. Consumer closure and production transform remain pending.', flush=True)


if __name__ == '__main__':
    main()
