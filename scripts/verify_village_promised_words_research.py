"""Native village table, comparison, input-boundary and portrait text research."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE
from dk4tool.patch.village_promised_words_release import PREFIX, SUFFIX
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_grand_race_name_append import execute as append
from scripts.execute_map_entity_tooltip_copy import STACK
from scripts.probe_common_copy_arm946_alignment import matrix
from scripts.probe_common_itcm_arena_reservation import initialize as arenas
from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
from scripts.probe_common_monthly_tribute_pixels import geometry
from scripts.probe_common_monthly_tribute_preparation import execute as monthly
from scripts.probe_common_tribute_modal_pixels import verify
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.verify_ordinary_name_fidelity_research import initialized


def text(machine, pointer):
    return bytes(machine.mem_read(pointer, 256)).split(b'\0', 1)[0].decode('ascii')


def caller(source, start, index, captain, expected, *, clue=None):
    machine = initialized(source)
    machine.emu_start(BASE + 0x788C0, BASE + 0x78904, count=1000)
    copied_sp = machine.reg_read(UC_ARM_REG_SP)
    if bytes(machine.mem_read(copied_sp + 0x5C, 96)) != source[0x1192A8:0x119308] or bytes(
            machine.mem_read(copied_sp + 0xBC, 96)) != source[0x1191E8:0x119248]:
        raise ValueError('Actual village table copies change selector order or pointers')
    executed = set()

    def fixture(uc, address, size, _):
        executed.add(address)
        # Native captain selector still executes. Only its live crew-list provider
        # is supplied: current captain zero and the selected nonplayer companion.
        if address == BASE + 0x829C8:
            uc.mem_write(uc.reg_read(UC_ARM_REG_R2), struct.pack('<2I', 0, captain))
            uc.reg_write(UC_ARM_REG_R0, 2)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = machine.hook_add(UC_HOOK_CODE, fixture)
    machine.reg_write(UC_ARM_REG_R4, 1)
    machine.reg_write(UC_ARM_REG_R8, index)
    machine.emu_start(BASE + start, BASE + 0x54058, count=10000)
    machine.hook_del(hook)
    if not {BASE + 0x53E4C, BASE + 0x82478, BASE + 0x7F244, BASE + 0xCB184} <= executed:
        raise ValueError('Village caller bypasses native captain selection or portrait wrapper')
    template = machine.reg_read(UC_ARM_REG_R2)
    actor = machine.reg_read(UC_ARM_REG_R1)
    arguments = machine.reg_read(UC_ARM_REG_R3)
    root = struct.unpack_from('<I', source, 0xCB18C)[0]
    if actor != root + 4 + captain * 32:
        raise ValueError('Native wrapper changes selected companion actor')
    raw = text(machine, template)
    if clue is not None:
        substitute = struct.unpack('<I', machine.mem_read(arguments, 4))[0]
        if text(machine, substitute) != clue:
            raise ValueError('Native clue selector differs')
        wanted = raw.replace('%s', clue)
    else:
        wanted = raw
    if wanted != expected:
        raise ValueError('Native caller/template/substitution differs from complete compilation')
    # Run the actual shared portrait sprintf/macro segment after explicit frame
    # setup. Widget composition/input remain outside this bounded execution.
    prep_sp = STACK - 0x4000
    machine.reg_write(UC_ARM_REG_SP, prep_sp)
    machine.mem_write(prep_sp + 0x264, struct.pack('<I', BASE + 0x53EAC))
    machine.mem_write(prep_sp + 0x274, bytes(4))
    for reg, value in ((UC_ARM_REG_R9, template), (UC_ARM_REG_R10, actor), (UC_ARM_REG_R11, arguments)):
        machine.reg_write(reg, value)
    buffers = [struct.unpack_from('<I', source, at)[0] for at in (0x5444C, 0x54450)]
    for buffer in buffers:
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    prep_trace = set()
    hook = machine.hook_add(UC_HOOK_CODE, lambda uc, addr, size, data: prep_trace.add(addr))
    machine.emu_start(BASE + 0x54144, BASE + 0x54164, count=100000)
    machine.hook_del(hook)
    resident_end = 0x01FF8000 + 7596
    if (not {BASE + 0xCE898, resident_end} <= prep_trace
            or BASE + 0x53914 in prep_trace or 0x01FF9BC8 in prep_trace):
        raise ValueError('Native formatter/literal wrapper or monthly-wrapper scope differ')
    for buffer in buffers:
        encoded = wanted.encode('ascii')
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xa5' * 32 + encoded + b'\0' + b'\xa5' * (287 - len(encoded)):
            observed = bytes(machine.mem_read(buffer, 256)).split(b'\0', 1)[0]
            raise ValueError(f'Village preparation differs: index={index}, buffer={buffer:08X}, wanted={encoded!r}, observed={observed!r}')
    return {'village_index': index, 'captain_fixture_index': captain, 'actor_pointer': actor,
            'template_pointer': template, 'complete_prepared_text': wanted,
            'native_table_copies_captain_selector_wrapper_formatter_executed': True,
            'scoped_literal_wrapper_preserves_capital_F_and_I': True,
            'live_crew_list_is_fixture': True, 'window_frame_initialization_is_contract': True,
            'word_wrapper_not_invoked': True, 'buffer_canaries_intact': True}


def main():
    image = NdsImage.open('out/all_routes_combined_v154_candidate.nds')
    original = image.read_file('/__arm9__.bin')
    source = Path('work/analysis/village_promised_words_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/village_promised_words_plan.json').read_text(encoding='utf-8'))
    if sha(original) != plan['source_arm9_sha256'] or sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Prepared village identities differ')
    # Both the scoped monthly path and ordinary fallback must keep V154 output.
    scope = []
    for parent, table in ((BASE + 0x53F40, BASE + 0x1189C0),
                          (BASE + 0x53EAC, 0), (BASE + 0x53F40, BASE + 0x1189C4)):
        for amount in (0, 999999, 42949672):
            wrapped = parent == BASE + 0x53F40 and table == BASE + 0x1189C0
            args = {'word_wrapped': wrapped, 'parent_return': parent, 'selector_table': table}
            old = monthly(original, 'Payment: %s gold coins.', amount, 0x02428000, **args)
            new = monthly(source, 'Payment: %s gold coins.', amount, 0x02428000, **args)
            if old != new:
                raise ValueError('Village literal wrapper changes an unrelated/monthly path')
            scope.append({'parent_return': parent, 'selector_table': table, 'amount': amount,
                          'original_and_research_output_identical': True, 'monthly_wrapper_active': wrapped})
    rows = plan['records']
    prompt_machine = initialized(source)
    state = struct.unpack_from('<I', source, 0xAEA38)[0]
    prompt_machine.mem_write(state + 0x54, struct.pack('<I', 1))
    prompt_machine.reg_write(UC_ARM_REG_R0, 0x02425000)
    prompt_machine.reg_write(UC_ARM_REG_R1, 100)
    prompt_machine.emu_start(BASE + 0xAE960, BASE + 0x5479C, count=100000)
    prompt = next(r for r in rows if r['kind'] == 'MESSAGE' and r['index'] == 4)['english']
    for at in (0x54890, 0x54894):
        if text(prompt_machine, struct.unpack_from('<I', source, at)[0]) != prompt:
            raise ValueError('Native input prompt formatter damages English')
    machine = initialized(source)
    machine.emu_start(BASE + 0x788C0, BASE + 0x78904, count=1000)
    copied_sp = machine.reg_read(UC_ARM_REG_SP)
    comparison_hook = machine.hook_add(UC_HOOK_CODE, lambda uc, address, size, data:
                                      uc.emu_stop() if address == BASE + 0x78BB0 else None)
    comparisons, insertion = [], []
    for row in rows:
        if row['kind'] != 'ANSWER':
            continue
        index, answer = row['index'], row['english']
        for value, accepted in ((answer, True), ('!' + answer[1:], False), (answer.lower(), False), ('', False)):
            machine.mem_write(0x02420000, value.encode('ascii') + b'\0')
            machine.reg_write(UC_ARM_REG_SP, copied_sp)
            machine.reg_write(UC_ARM_REG_R8, index)
            machine.reg_write(UC_ARM_REG_R11, 0x02420000)
            machine.emu_start(BASE + 0x78AF4, BASE + 0x78B0C, count=1000)
            branch = machine.reg_read(UC_ARM_REG_PC)
            success = branch == BASE + 0x78B0C
            if not success and branch != BASE + 0x78BB0:
                raise ValueError('Native comparison escaped expected success/failure branches')
            if success != accepted:
                raise ValueError('Localized answer changes native accepted/rejected behavior')
            comparisons.append({'index': index, 'input': value, 'accepted': success,
                                'native_selector_strcmp_and_branch_executed': True})
        built = b''
        for character in answer.encode('ascii'):
            case = append(source, built, bytes([character]), 18, full_return=True)
            built = bytes.fromhex(case['result_hex'])
        if built != answer.encode('ascii'):
            raise ValueError('Native incremental entry cannot enter complete English answer')
        insertion.append({'index': index, 'answer': answer, 'bytes': len(built), 'native_incremental_entry_complete': True,
                          'input_bytes_and_widget_capacity_18_are_fixtures': True})
    machine.hook_del(comparison_hook)
    boundaries = []
    for size in range(19):
        for incoming in (b'B', 'ア'.encode('cp932')):
            case = append(source, b'A' * size, incoming, 18, full_return=True)
            expected = b'A' * size + (incoming if size + len(incoming) <= 18 else b'')
            if bytes.fromhex(case['result_hex']) != expected:
                raise ValueError('Actual 18-byte input boundary drops or overflows characters')
            boundaries.append(case)
    prepared, panels = [], []
    messages = {r['index']: r for r in rows if r['kind'] == 'MESSAGE'}
    for captain in (4, 19):
        for index, start in ((0, 0x78ADC), (2, 0x78BA0), (3, 0x78BB0)):
            row = messages[index]
            prepared.append(caller(source, start, 0, captain, bytes.fromhex(row['compiled_hex']).decode('ascii')))
        for row in rows:
            if row['kind'] == 'CLUE':
                clue = bytes.fromhex(row['compiled_hex']).decode('ascii')
                prepared.append(caller(source, 0x78B8C, row['index'], captain, PREFIX + clue + SUFFIX, clue=clue))
    font = image.read_file('/GRP/KANJI.FNT')
    destination = Path('work/qa/village_promised_words_native')
    destination.mkdir(parents=True, exist_ok=True)
    unique = list(dict.fromkeys(c['complete_prepared_text'] for c in prepared)) + [prompt]
    sheet = Image.new('RGB', (1044, len(unique) * 220), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, value in enumerate(unique):
        for mode in (4, 16):
            native = verify(source, font, value, mode, guarded=True, portrait=index < len(unique) - 1)
            events = [e for e in native['glyph_events'] if e['code'] != 32]
            cursor = 0
            for word in value.split():
                if len({e['y'] for e in events[cursor:cursor + len(word)]}) != 1:
                    raise ValueError('Native village wrapping splits a word')
                cursor += len(word)
            panels.append({'index': index, 'mode': mode, 'text': value, 'pixels_sha256': sha(native['pixels']),
                           'complete_glyphs_bounds_independent_pixels_and_whole_words': True})
            if mode == 16:
                panel = Image.new('RGB', (256, 192))
                colors = struct.unpack('<49152H', native['pixels'])
                panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14 else (0, 0, 0) for c in colors])
                panel = panel.crop((0, 0, 256, 96)).resize((1024, 192), Image.Resampling.NEAREST)
                panel.save(destination / f'panel_{index:02d}.png')
                draw.text((10, index * 220 + 2), str(index), fill='black')
                sheet.paste(panel, (10, index * 220 + 20))
    sheet.save(destination / 'native_sheet.png')
    code = MainCodeFile(source, BASE)
    before, after = initialized(original), initialized(source)
    names = []
    for index in range(207):
        old = ordinary_getter(original, index, before)
        new = ordinary_getter(source, index, after)
        # A getter near the inherited pool end may read beyond its NUL into
        # the new appended strings. Compare only the complete actual name.
        if old != new or bytes(before.mem_read(old, 128)).split(b'\0', 1)[0] != bytes(after.mem_read(new, 128)).split(b'\0', 1)[0]:
            raise ValueError('Village addition changes an inherited ordinary name/getter')
        names.append({'index': index, 'pointer': new, 'complete_string_preserved': True})
    inherited_plan = json.loads(Path('work/analysis/ordinary_name_fidelity_plan.json').read_text(encoding='utf-8'))
    owners = []
    for move in inherited_plan['inherited_pointer_moves']:
        field = move['field']
        old, new = [struct.unpack_from('<I', raw, field)[0] for raw in (original, source)]
        if old != new or bytes(before.mem_read(old, 128)).split(b'\0', 1)[0] != bytes(after.mem_read(new, 128)).split(b'\0', 1)[0]:
            raise ValueError('Village addition changes inherited shared item/name ownership')
        owners.append({'field': field, 'pointer': new, 'complete_string_preserved': True})
    shared = image.read_file('/COMMON/MESFILE.DK4')
    if common_message_entries(shared, original, clean=False) != common_message_entries(shared, source, clean=False):
        raise ValueError('Village addition changes inherited COMMON selectors')
    copy_cases = matrix(source)
    initial = arenas(source)
    if (initial['low'][3] != plan['literal_wrapper']['reserved_arena_low']
            or initial['low'][0] != plan['final_pool_span'][1]):
        raise ValueError('Native initial arenas fail to reserve village helper')
    old_initial = arenas(original)
    if initial['high'] != old_initial['high'] or any(initial['low'][i] != old_initial['low'][i] for i in range(9) if i not in (0, 3)):
        raise ValueError('Village addition changes an unrelated heap arena')
    boot_result = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                       plan['copy_entry'], bytes(code.sections[3].data[:-48]))
    if boot_result['arm7_source_changed_bytes_after_arm9_autoload'] or not all(r['matches_original'] for r in boot_result['arm7_native_loaded_sections']) or not boot_result['repaired_pool_matches_complete_payload']:
        raise ValueError('Village research corrupts ARM7 source or persistent pool at startup')
    proof = {'status': 'research-native-village-tables-comparison-append-and-portrait-pixels-pass',
             'source_arm9_sha256': sha(original), 'target_arm9_sha256': sha(source),
             'comparisons': comparisons, 'incremental_answer_entry': insertion, 'boundary_cases': boundaries,
             'inherited_monthly_and_unrelated_scope_cases': scope,
             'native_preparation_cases': prepared, 'paired_pixel_cases': panels,
             'input_prompt': {'actual_caller': BASE + 0xAE960, 'native_formatter_endpoint': BASE + 0x5479C,
                              'english': prompt, 'live_state_flag_is_fixture': True, 'modal_composition_pending': True},
             'geometry': geometry(source), 'boot': boot_result,
             'inherited_names': names, 'inherited_shared_owners': owners,
             'common_selections_preserved': len(common_message_entries(shared, source, clean=False)),
             'shared_copy_alignment_cases': copy_cases,
             'native_initial_arenas': initial,
             'resident_arena_bounds': arena_bounds(source, plan['literal_wrapper']['reserved_arena_low']),
             'visual_review': {'complete': False},
             'limitations': ['Crew-list contents and portrait-frame setup are explicit fixtures.',
                             'Real keyboard/title/input-redraw proofs are recorded separately; full widget composition remains pending.',
                             'Standalone append cases supply capacity 18; the separate actual keyboard proof verifies the real parent/child capacity alias and setter.',
                             'Native case-sensitive answer spelling is preserved; gameplay usability remains to be reviewed.',
                             'Not registered or built as a playable release.']}
    Path('work/analysis/village_promised_words_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(comparisons)} native comparisons; {len(insertion)} complete answers; {len(boundaries)} input boundaries; {len(prepared)} native callers; {len(panels)} pixel cases. Research only.')


if __name__ == '__main__':
    main()
