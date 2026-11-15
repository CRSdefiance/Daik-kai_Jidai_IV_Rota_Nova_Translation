"""Clean-source shipyard packet and bounded original caller/number contracts.

Research only. No ROM, release profile, patch or completion credit is produced.
"""

import struct
from itertools import product
from ndspy.code import MainCodeFile
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shipyard_editorial_v759')
CURRENT = Path('out/all_routes_combined_v758_candidate.nds')
MANUSCRIPT = Path('translations/shipyard_editorial_manuscript_v1.json')
IDS = tuple(range(784, 805))
TEXT = {
    784: 'A fleet can only have five ships. The new ship will have to stay in the dock.',
    785: "Which ship's design should I copy?",
    786: 'Masts: %s. Durability: %s.',
    787: "We'll keep it in the dock.",
    788: 'Which ship do you want to sell?',
    789: 'How about %s gold coins?',
    790: 'No ships need repairs!',
    791: "Admiral, I'll help with the repairs, too.",
    792: 'Admiral, I can help with the repairs, too!',
    793: 'Admiral, let me help with the repairs, too.',
    794: "Admiral, I'll lend a hand, too!",
    795: "Admiral, I'll lend a hand with the repairs, too.",
    796: "Admiral! I'll help with the repairs, too!",
    797: 'Admiral, I could help with the repairs, too...',
    798: "If they're helping, I'll knock %s percent off the repair bill.",
    799: "Repairs will cost %s gold coins, but you don't have enough.",
    800: 'Repairs will cost %s gold coins. Is that okay?',
    801: "Repairs will take one day. Please wait until they're finished.",
    802: 'I can repair it completely for %s gold coins. Should I go ahead?',
    803: "The same specifications as %s? That'll cost %s gold coins and take %s days to prepare. Buy it?",
    804: "No remodeling is needed to match %s. That's %s gold coins. Buy it?",
}
GLOSS = {
    784: 'A fleet is limited to five ships, so the new ship will be placed in the dock.',
    785: 'Asks which existing ship should be copied exactly in a newly purchased remodeled ship.',
    786: 'The selected ship has the supplied number of masts and the supplied durability.',
    787: 'Agrees to keep the ship in the dock for the player.',
    788: 'Asks which ship the player wants to sell.',
    789: 'Proposes the supplied amount of gold coins as the sale price and asks whether that is acceptable.',
    790: 'There are no ships in need of repairs.',
    791: 'Polite crew voice offers to help with repairs as well.',
    792: 'Familiar crew voice offers to help with repairs as well. IC is a first-person pronoun; both Japanese alternatives become I in English.',
    793: 'Crew voice asks to be allowed to help with repairs as well.',
    794: 'Rough familiar crew voice offers to lend a hand as well.',
    795: 'Measured older-register crew voice offers to lend a hand with repairs as well.',
    796: 'Upbeat youthful-register crew voice offers to help with repairs as well.',
    797: 'Hesitant polite crew voice begins offering help with repairs and trails off.',
    798: 'With that crew member helping, the yard will discount the repair bill by the supplied percentage.',
    799: 'Repairs cost the supplied amount of gold coins; the player appears not to have enough.',
    800: 'Quotes the supplied repair cost and asks for confirmation.',
    801: 'Asks the player to wait one day until repairs finish.',
    802: 'Offers complete repairs for the supplied amount of gold coins and asks whether to proceed.',
    803: 'Matching the supplied ship specifications costs the supplied amount of gold coins and takes the supplied number of preparation days; asks whether to buy.',
    804: 'Matching the supplied ship needs no remodeling; quotes the supplied gold-coin price and asks whether to buy.',
}
CALLS = {
    784: (0x6339C, 0x633A0, 0x53FE4), 785: (0x63008, 0x63010, 0x53FE4),
    786: (0x63494, 0x634A0, 0x53FE4), 787: (0x636BC, 0x636C0, 0x53FE4),
    789: (0x62650, 0x62658, 0x53F9C), 790: (0x62294, 0x6229C, 0x53FE4),
    798: (0x624D8, 0x624E0, 0x53FE4), 799: (0x6235C, 0x62364, 0x53FE4),
    800: (0x62380, 0x62384, 0x53F9C), 801: (0x623C8, 0x623D0, 0x53FE4),
    802: (0x620C0, 0x620C8, 0x53F9C), 803: (0x63188, 0x63198, 0x53F9C),
}
NUMERIC_RAM = Path('E:/Rota Nova translations/Generated/work/emulation_v193/market_contract_v758_palace_758/frame_003200_arm9_ram.bin')


def voice_cases(arm):
    u, rows = machine(arm), []
    for index in range(8):
        def choose(cpu, address, size, unused):
            if address == BASE + 0x7E988:
                cpu.reg_write(UC_ARM_REG_R0, index)
                cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, choose)
        try:
            call(u, 0x53F4C, (13, 0x02118460))
        finally:
            u.hook_del(hook)
        result = u.reg_read(UC_ARM_REG_R0)
        assert result == (791 if index in (0, 1) else 790 + index)
        rows.append({'supplied_voice_index': index, 'selected_message': result})
    return rows


def number_contract(arm, clean_arm):
    assert arm[0xABF50:0xABFCC] == clean_arm[0xABF50:0xABFCC]
    assert arm[0xAC000:0xAC07C] == clean_arm[0xAC000:0xAC07C]
    raw = NUMERIC_RAM.read_bytes()
    u = machine(arm)
    u.mem_write(BASE, raw)
    result = {}
    for n in sorted({*range(17), 22, 25, 27, 40, 99, 100, 999, 1000, 12345, 50000, 65535, 1000000, 2147483647}):
        call(u, 0xABF50, (n,))
        ptr = u.reg_read(UC_ARM_REG_R0)
        text = bytes(u.mem_read(ptr, 80)).split(b'\0')[0]
        assert text.decode('cp932') == str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
        result[n] = text
    return result


def native_fragments(arm, numbers):
    rows = []
    # The original copy-purchase constructor seeds804. Preparation zero takes
    #804; positive supplied preparation takes803, preserving name/price/day order.
    for days in (0, 1, 2, 16):
        u = machine(arm)
        model, table, getter, name = 0x02450000, 0x02451000, 0x02452000, 0x02453000
        u.mem_write(model, struct.pack('<I', table))
        u.mem_write(table + 4, struct.pack('<I', getter))
        u.mem_write(name, b'Vestaros\0')
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.emu_start(BASE + 0x63038, BASE + 0x63044, count=10)
        assert struct.unpack('<I', u.mem_read(STACK + 0x18, 4))[0] == 804
        u.reg_write(UC_ARM_REG_R6, model)
        u.reg_write(UC_ARM_REG_R8, 50000)
        u.reg_write(UC_ARM_REG_R9, 0x02454000)
        u.reg_write(UC_ARM_REG_R10, 0x02455000)
        events, formatted = [], []
        def observe(cpu, address, size, unused):
            if address == BASE + 0x62B8C:
                cpu.reg_write(UC_ARM_REG_R0, days)
            elif address == getter:
                cpu.reg_write(UC_ARM_REG_R0, name)
            elif address == BASE + 0xABF50:
                n = cpu.reg_read(UC_ARM_REG_R0)
                ptr = 0x02456000 + len(formatted) * 128
                cpu.mem_write(ptr, numbers[n] + b'\0')
                formatted.append(n)
                cpu.reg_write(UC_ARM_REG_R0, ptr)
            elif address == BASE + 0x53F9C:
                n = cpu.reg_read(UC_ARM_REG_R1)
                pointers = [cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3)]
                if n == 803:
                    pointers.append(struct.unpack('<I', cpu.mem_read(STACK, 4))[0])
                values = [bytes(cpu.mem_read(p, 80)).split(b'\0')[0] for p in pointers]
                events.append({'message_id': n, 'argument_hex': [b.hex() for b in values]})
                cpu.emu_stop()
                return
            else:
                return
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, observe)
        try:
            u.emu_start(BASE + 0x63114, 0x027E0000, count=100)
        finally:
            u.hook_del(hook)
        expected = [b'Vestaros', numbers[50000]] + ([numbers[days]] if days else [])
        assert len(events) == 1 and events[0]['message_id'] == (803 if days else 804)
        assert events[0]['argument_hex'] == [b.hex() for b in expected]
        rows.append({'kind': 'copy_purchase', 'supplied_preparation_days': days, 'events': events, 'original_numeric_inputs': formatted})
    # Complete discount helper arithmetic with explicitly supplied crew/level
    # and tagged actor/town roots. This is not an earned qualification test.
    for helper, level in ((208, 25), (16, 24), (16, 25), (16, 26), (16, 50), (16, 111), (16, 200)):
        u = machine(arm)
        price, events = 0x02458000, []
        u.mem_write(price, struct.pack('<I', 50000))
        def observe(cpu, address, size, unused):
            replies = {BASE + 0xCB1A8: 0x02450000, BASE + 0x8261C: helper, BASE + 0xCB184: 0x02451000,
                       BASE + 0x7F244: 1, BASE + 0x7E728: level, BASE + 0xB6618: 0x02452000,
                       BASE + 0xB2CD8: 0x02453000}
            if address in replies:
                cpu.reg_write(UC_ARM_REG_R0, replies[address])
            elif address == BASE + 0xABF50:
                n = cpu.reg_read(UC_ARM_REG_R0)
                cpu.mem_write(0x02454000, numbers[n] + b'\0')
                cpu.reg_write(UC_ARM_REG_R0, 0x02454000)
            elif address == BASE + 0x53D44:
                events.append({'queued_role': cpu.reg_read(UC_ARM_REG_R0), 'table': cpu.reg_read(UC_ARM_REG_R1)})
            elif address == BASE + 0x53FE4:
                ptr = cpu.reg_read(UC_ARM_REG_R2)
                events.append({'direct_message': cpu.reg_read(UC_ARM_REG_R1), 'argument_hex': bytes(cpu.mem_read(ptr, 80)).split(b'\0')[0].hex()})
            else:
                return
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, observe)
        try:
            call(u, 0x6242C, (price,), instruction_limit=1000)
        finally:
            u.hook_del(hook)
        applicable = helper != 208 and level >= 25
        discount = level // 5 if applicable else 0
        actual = struct.unpack('<I', u.mem_read(price, 4))[0]
        assert actual == 50000 - 50000 * discount // 100
        assert events == ([{'queued_role': 13, 'table': 0x02118460}, {'direct_message': 798, 'argument_hex': numbers[discount].hex()}] if applicable else [])
        rows.append({'kind': 'repair_discount', 'supplied_helper': helper, 'supplied_level': level,
                     'discount_percent': discount, 'original_cost': 50000, 'discounted_cost': actual, 'events': events})
    return rows


def preparation_cases(arm):
    u = machine(arm)
    model, prototype, current_vtable, default_vtable = 0x02450000, 0x02452004, 0x02453000, 0x02453100
    u.mem_write(model, struct.pack('<I', current_vtable))
    u.mem_write(prototype, struct.pack('<I', default_vtable))
    tags = {0x02454000 + k * 4: label for k, label in enumerate(('index', 'sail', 'default_sail', 'flags', 'room', 'default_room', 'end', 'default_end'))}
    ptr = {v: k for k, v in tags.items()}
    for offset, label in ((8, 'index'), (16, 'sail'), (24, 'room'), (28, 'end')):
        u.mem_write(current_vtable + offset, struct.pack('<I', ptr[label]))
    for offset, label in ((16, 'default_sail'), (20, 'flags'), (24, 'default_room'), (28, 'default_end')):
        u.mem_write(default_vtable + offset, struct.pack('<I', ptr[label]))
    rows = []
    for sail, count, first_group, second_group, end in product((0, 1), range(10), (0, 1), (0, 1), (0, 1)):
        def observe(cpu, address, size, unused):
            index = cpu.reg_read(UC_ARM_REG_R1)
            if address == BASE + 0xCB154:
                value = prototype - 4
            elif address == BASE + 0xAB8A8:
                value = int(sail and index == 0)
            elif address == BASE + 0xAB8C8:
                value = int(index < count)
            elif address in tags:
                label = tags[address]
                value = (1 if label == 'sail' else end if label == 'end' else
                         7 if label == 'room' and first_group and index == 0 else
                         12 if label == 'room' and second_group and index == 1 else 0)
            else:
                return
            cpu.reg_write(UC_ARM_REG_R0, value)
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, observe)
        try:
            call(u, 0x62B8C, (0, model), instruction_limit=10000)
        finally:
            u.hook_del(hook)
        expected = 2 * sail + count + 2 * first_group + 2 * second_group + end
        assert u.reg_read(UC_ARM_REG_R0) == expected
        rows.append({'sail_difference': sail, 'nine_flag_difference_count': count, 'room_groups': [first_group, second_group],
                     'last_property_difference': end, 'native_preparation_days': expected})
    assert len(rows) == 160 and {r['native_preparation_days'] for r in rows} == set(range(17))
    return rows


def pronoun_and_literal_cases(clean_arm, current_arm):
    rows = []
    for label, arm in (('clean', clean_arm), ('current', current_arm)):
        u = machine(arm)
        if label == 'current':
            u.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
        for alternative in (0, 1):
            for text in ('IC will help.', 'I can help.', "I'll help.", 'Admiral, I can help.'):
                encoded = text.encode('ascii')
                u.mem_write(0x02420000, encoded + b'\0')
                u.mem_write(0x02421000, b'\xA5' * 256)
                def choose(cpu, address, size, unused):
                    if address == BASE + 0x7E9B8:
                        cpu.reg_write(UC_ARM_REG_R0, alternative)
                        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
                hook = u.hook_add(UC_HOOK_CODE, choose)
                try:
                    call(u, 0x53914, (0x02421010, 0x02420000, 0x02450000))
                finally:
                    u.hook_del(hook)
                output = bytes(u.mem_read(0x02421010, 200)).split(b'\0')[0]
                if text.startswith('IC'):
                    assert output == ('アタシ' if alternative else '僕').encode('cp932') + b' will help.'
                elif label == 'current':
                    assert output == encoded
                assert bytes(u.mem_read(0x02421000, 16)) == b'\xA5' * 16
                assert bytes(u.mem_read(0x02421011 + len(output), 239 - len(output))) == b'\xA5' * (239 - len(output))
                rows.append({'ROM': label, 'source_first_person_property': alternative, 'input': text, 'output_hex': output.hex(),
                             'current_literal_I_preserved_or_source_IC_expansion_proven': label == 'current' or text.startswith('IC')})
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, canonical, current = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', CURRENT)]
    assert sha(CURRENT.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    ca, arm = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    source, accepted, before = [common_message_entries(r.read_file('/COMMON/MESFILE.DK4'), r.read_file('/__arm9__.bin'), clean=(r is clean)) for r in (clean, canonical, current)]
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    bindings = []
    for n, (load, end, target) in CALLS.items():
        instructions = list(cs.disasm(ca[load:end + 4], BASE + load))
        first, last = instructions[0], instructions[-1]
        if first.mnemonic == 'mov':
            assert first.operands[1].imm == n
            literal = None
        else:
            assert first.mnemonic == 'ldr' and first.op_str.startswith('r1, [pc,')
            literal = first.address + 8 + first.operands[1].mem.disp - BASE
            assert struct.unpack_from('<I', ca, literal)[0] == n
            assert ca[literal:literal + 4] == arm[literal:literal + 4]
        assert last.mnemonic == 'bl' and last.operands[0].imm == BASE + target
        assert ca[load:end + 4] == arm[load:end + 4]
        bindings.append({'id': n, 'load': BASE + load, 'call': BASE + end, 'consumer': BASE + target,
                         'original_parent': 0x02054014 if target == 0x53FE4 else 0x02053FCC})
    #788 is held in sb through the ship-selection loop;804 is held at sp+18.
    assert ca[0x62598:0x6259C] == arm[0x62598:0x6259C]
    first = next(cs.disasm(ca[0x62598:0x6259C], BASE + 0x62598))
    assert first.mnemonic == 'mov' and first.op_str == 'sb, #0x314'
    assert ca[0x63038:0x63044] == arm[0x63038:0x63044]
    sale = list(cs.disasm(ca[0x625A8:0x625B4], BASE + 0x625A8))
    assert [(i.mnemonic, i.op_str) for i in sale] == [('mov', 'r0, r5'), ('mov', 'r1, sb'), ('bl', '#0x2053fe4')]
    assert ca[0x625A8:0x625B4] == arm[0x625A8:0x625B4]
    bindings.append({'id': 788, 'load': BASE + 0x62598, 'call': BASE + 0x625B0, 'consumer': BASE + 0x53FE4, 'original_parent': 0x02054014, 'ID_held_in_sb_through_original_selection_loop': True})
    pronoun_spans = ((0x53914, 0x53AC4), (0x7E9B8, 0x7E9D0))
    assert sha(ca[pronoun_spans[0][0]:pronoun_spans[0][1]]) == '71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87'
    assert ca[0x143A28:0x143A2B] == '僕'.encode('cp932') + b'\0'
    assert ca[0x143A2C:0x143A33] == 'アタシ'.encode('cp932') + b'\0'
    assert ca[0x62B8C:0x62D40] == arm[0x62B8C:0x62D40]
    preparation = preparation_cases(ca)
    assert preparation == preparation_cases(arm)
    pronouns = pronoun_and_literal_cases(ca, arm)
    voices = voice_cases(ca)
    assert voices == voice_cases(arm)
    numbers = number_contract(arm, ca)
    fragments = native_fragments(ca, numbers)
    assert fragments == native_fragments(arm, numbers)
    save(ROOT / 'native_context.json', {'clean_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(CURRENT.read_bytes()),
        'original_call_bindings': bindings, 'all8_original_voice_selections_each_clean_and_current': voices,
        'all11_original_copy_and_discount_fragments_each_clean_and_current': fragments,
        'all160_abstract_preparation_cases_each_clean_and_current': preparation,
        'preparation_range0_16_proven_for_supplied_native_getter_contracts': True,
        'source_IC_and_current_literal_I_complete_native_cases': pronouns,
        'IC_clean_pronoun_proof': [{'lo': lo, 'hi': hi, 'sha256': sha(ca[lo:hi])} for lo, hi in pronoun_spans],
        'source_number_formatter_identical_and_actual_initialized_contract': {
            'RAM': str(NUMERIC_RAM), 'RAM_sha256': sha(NUMERIC_RAM.read_bytes()), 'samples': {str(n): b.hex() for n, b in numbers.items()},
            'fullwidth_digit_2byte_12pixel_cell_not_ASCII_6pixel': True},
        'fragment_states_and_virtual_name_actor_roots_supplied_not_whole_transactions_or_earned_progress': True,
        'preparation1_is_supplied_upstream_case_not_claimed_earned_design_reachability': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    records = []
    retained = (787, 790, 800, 801, 803)
    for n in IDS:
        controls = {'source': True, 'context': True, 'localization': True, 'naturalness': n not in (789, 799, 800, 802, 803, 804), 'formatting': False}
        note = ('Preserve the existing natural wording; regenerate guarded formatting and check the exact native consumer.' if n in retained else
                'Restore the complete source thought as natural American English, keeping each native entry independent and preserving all numeric/name placeholders.')
        if n == 792:
            note += ' Source IC has two Japanese first-person forms, both I in English, proven in common_IC_pronoun_mapping.md. This is pronoun localization, not dropping a character name. English literal-I rendering still needs current-consumer verification.'
        if n == 798:
            note += ' Percent is written out; do not add a literal printf percent command. The original qualified-helper/level fragment confirms a discount, not a trade service price.'
        if n in (789, 799, 800, 802, 803, 804):
            note += ' Verify reachable numeric bounds and singular/plural agreement for coin quantities before approving naturalness; do not assume the singular case is impossible.'
        if n == 803:
            note += ' Preparation can be supplied as1 to the original branch; days would then disagree. Preserve the name/price/preparation argument order, verify real design bounds, and implement singular/plural handling before approving naturalness. Do not ship this pending draft unchanged.'
        if n == 786:
            note += ' Stat labels preserve mast count and hull durability and read correctly for a single mast without inventing new units.'
        records.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'source_hex': source[n].text.hex(),
            'japanese': source[n].text.decode('cp932'), 'canonical_source_hex': accepted[n].text.hex(),
            'current_text_hex': before[n].text.hex(), 'current_English': before[n].text.decode('cp932'),
            'english': TEXT[n] + '{PAD}', 'source_meaning': GLOSS[n], 'localization_note': note,
            'speaker': 'Original fleet repair volunteer selected by role13 voice table' if 791 <= n <= 797 else 'Original contextual Shipyard broker',
            'context': ('Original6242C requires a supplied eligible helper and level>=25, queues role13 table2118460, quotes798 and applies floor(level/5) percent discount. Actor/level eligibility fragments are supplied contracts, not a whole earned event.' if 791 <= n <= 798 else
                        'Original63114 selects804 for zero preparation and803 for positive preparation, with virtual ship name then numeric price then numeric days. Tagged ship-name getter and supplied upstream days prove argument order, not a completed purchase.' if n in (803, 804) else
                        'Original Shipyard function and direct/Yes-No consumer are pinned by executable instruction bindings. Review the native neighboring selections independently;788 is a complete sell-ship question and789 a separate price confirmation.'),
            'source_reference': {'block': source[n].block, 'record': source[n].record_index, 'offset': source[n].block_offset},
            'current_reference': {'block': before[n].block, 'record': before[n].record_index, 'offset': before[n].block_offset},
            'decision': 'retain-wording-pending-grammar-and-formatting' if n == 803 else 'retain-wording' if n in retained else 'revise',
            'review': controls, 'status': 'source-context-prose-draft-not-integrated'})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'file_path': '/COMMON/MESFILE.DK4', 'source_clean_COMMON_sha256': sha(clean.read_file('/COMMON/MESFILE.DK4')),
        'source_canonical_COMMON_sha256': sha(canonical.read_file('/COMMON/MESFILE.DK4')),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(CURRENT.read_bytes()),
        'context_evidence': str(ROOT / 'native_context.json'), 'records': records, 'status': 'draft-grammar-layout-integration-gameplay-pending'})
    save(ROOT / 'source_and_neighbors.json', [{'id': n, 'source_hex': source[n].text.hex(), 'japanese': source[n].text.decode('cp932'),
        'current_hex': before[n].text.hex(), 'current': before[n].text.decode('cp932')} for n in range(778, 812)])
    print('21 shipyard source drafts; clean/current caller,voice,number and discount/copy contracts pass. No ROM emitted.', flush=True)


if __name__ == '__main__':
    main()
