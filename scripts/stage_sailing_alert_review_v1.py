"""Exercise every stored sailing alert and the floating notice's native text path."""

from hashlib import sha256
from pathlib import Path
import struct
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0
from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R6, UC_ARM_REG_SP

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import ARM, BASE, COMMON, OUTPUT, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_diplomatic_outcome_wrap_v1 import preview_sheets
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.probe_button_prompt_native import STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/sailing_alerts_20261111_v1')
ROM = ROOT / 'sailing_alerts_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_sailing_alert_verification.json'


def crew_case(ctx, row, group, argument):
    number = row['message_ID']
    actor_id = next(i for i, _, n in group['original_voice_choices'] if n == number)

    def assigned_role(arm, common, raw, plan):
        cpu, get, provider = ctx.machine(arm, common, raw, plan)

        def use_actor(u, pc, size, unused):
            u.reg_write(UC_ARM_REG_R0, actor_id)

        cpu.hook_add(UC_HOOK_CODE, use_actor, begin=0x02053D70, end=0x02053D70)
        return cpu, get, provider

    native = FunctionType(consumer.__code__, {**consumer.__globals__, 'portrait_machine': assigned_role},
                          argdefs=consumer.__defaults__)
    result = native(ctx.arm, ctx.common, ctx.raw, ctx.plan, 0x53D44, group['original_role_argument'],
                    group['table'], argument)
    assert bytes(ctx.calls[0].mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return result | {'offline_role_actor': actor_id}


def floating_cases(ctx, row):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    original, expected_pc = 0x0207E3A8, 0x0207E444
    printf_owner = struct.unpack_from('<I', ctx.arm, 0x7E5B4)[0]
    rectangle = (84, 60, 188, 84)
    slot_size, slots = 128, 32
    received = {}

    def boundary(u, pc, size, unused):
        if pc == 0x0203F0F8:
            u.reg_write(UC_ARM_REG_R0, 0x02123400)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif pc == 0x02090698:
            assert u.reg_read(UC_ARM_REG_R0) == STACK + 40
            assert u.reg_read(UC_ARM_REG_R1) == 0x02123400
            u.mem_write(STACK + 40, struct.pack('<4i', *rectangle))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif pc == 0x020ABFCC:
            assert u.reg_read(UC_ARM_REG_R0) == printf_owner
            template = row['english'].encode('ascii') + b'\0'
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), len(template))) == template
            assert u.reg_read(UC_ARM_REG_R2) == received['name_pointer']
            received['actual_native_template_hex'] = template.hex()
        else:
            raise AssertionError(hex(pc))

    for pc in (0x0203F0F8, 0x02090698, 0x020ABFCC):
        cpu.hook_add(UC_HOOK_CODE, boundary, begin=pc, end=pc)
    cases = []
    for i in range(207):
        actor = ctx.actor_root + (0x19E4 if i == 3 else 4 + i * 32)
        table = struct.unpack('<I', cpu.mem_read(actor, 4))[0]
        getter = struct.unpack('<I', cpu.mem_read(table + 0x20, 4))[0]
        name_pointer = get(getter - BASE, actor)
        name = bytes(cpu.mem_read(name_pointer, 64)).split(b'\0', 1)[0]
        assert name and len(name) < 64 and name.isascii() and b'\n' not in name
        expected = row['english'].encode('ascii').replace(b'%s', name)
        assert len(expected) < slot_size
        received.clear()
        received['name_pointer'] = name_pointer
        index = struct.unpack('<I', cpu.mem_read(printf_owner + 8, 4))[0]
        assert index < slots
        buffer = printf_owner + 12 + slot_size * index
        cpu.mem_write(buffer, b'\xA5' * slot_size)
        ring = bytes(cpu.mem_read(printf_owner + 12, slot_size * slots))
        cpu.reg_write(UC_ARM_REG_CPSR, 0xA0000010)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_R6, actor)
        cpu.emu_start(original, expected_pc, count=1000000)
        assert cpu.reg_read(UC_ARM_REG_PC) == expected_pc and not cpu.reg_read(UC_ARM_REG_CPSR) & 32
        result = cpu.reg_read(UC_ARM_REG_R1)
        assert result == buffer and cpu.reg_read(UC_ARM_REG_R3) == 90
        assert struct.unpack('<I', cpu.mem_read(printf_owner + 8, 4))[0] == (index + 1) % slots
        write_start = index * slot_size
        assert bytes(cpu.mem_read(printf_owner + 12, len(ring))) == (
            ring[:write_start] + expected + b'\0' + ring[write_start + len(expected) + 1:])
        assert received['actual_native_template_hex']
        cases.append(dict(actor_ID=i, actor_name=name.decode('ascii'), original_name_getter=getter,
            native_text_hex=expected.hex(), widget_entry=0x02005E4C, lifetime=90))
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return dict(cases=cases, native_file_reads=provider.reads,
        text_buffer_and_adjacent_guards_exact=True,
        offline_boundaries=['coordinate manager return', 'rectangle input', 'widget entry before drawing'])


def main():
    assert not ROOT.exists()
    manuscript, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    assert all(digest(path) == expected for path, expected in manuscript['evidence'].items())
    rows = {row['message_ID']: row for row in manuscript['records']}
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(runtime.common, runtime.arm, rows, storage)
    assert arm[:DIRECTORY_OFFSET] == runtime.arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == runtime.arm[TABLE_END:]
    assert len(packing['changed_visible_templates']) == 28 and packing['all_41_blocks_fit_8KiB']
    staged = with_components(runtime, arm, common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    groups = {n: group for group in manuscript['exact_native_crew_groups']
              for n in range(group['first_ID'], group['last_ID'] + 1)}
    condition_names = [case['English'] for case in manuscript['condition_labels'] if 16 <= case['index'] <= 19]
    cases, pages, stored = [], [], []
    for n, row in rows.items():
        lookup = current_copy(staged, row | {'current_hex': storage[n].hex()}, BASE + 0x5528C)
        staged.calls.clear()
        stored.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=storage[n].hex(), original_stored_lookup=lookup))
        if n == 97:
            continue
        for name in condition_names if row['original_substitutions'] else [None]:
            argument = name.encode('ascii') if name else None
            native = crew_case(staged, row, groups[n], argument)
            expected = storage[n].replace(b'%s', argument) if name else storage[n]
            display = bytes.fromhex(native['formatted_hex'])
            assert bytes.fromhex(native['input_hex']) == expected
            assert display.isascii() and b' '.join(display.split()) == expected, (n, display)
            pixels, glyphs = render(raster, arm, kanji, display)
            assert glyphs[0]['code'] == expected[0] and glyphs[-1]['code'] == expected[-1]
            cases.append(dict(message_ID=n, arguments=[name] if name else [], native=native,
                visible_lines=[line.strip() for line in display.decode('ascii').split('\n')],
                glyphs=len(glyphs), native_ink_sha256=sha256(pixels).hexdigest()))
            pages.append(pixels)
    assert len(cases) == 45
    floating = floating_cases(staged, rows[97])
    assert {c['actor_name'] for c in floating['cases']} >= {'Gerhard', 'Manuel'}

    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    assert NdsImage.open(ROM).read_file(COMMON) == common
    assert NdsImage.open(ROM).read_file(ARM) == arm
    sheets = FunctionType(preview_sheets.__code__, {**preview_sheets.__globals__, 'ROOT': ROOT})
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        stored=stored, storage=packing, complete_serialized_ROM_parent_inverse=True,
        crew_cases=cases, floating_notice=floating, crew_contact_sheets=sheets(cases, pages), font=font,
        original_335_and_all_unselected_records_preserved=True, candidate_gameplay_and_floating_GPU_pending=True,
        new_credit=0, evidence={str(path): digest(path) for path in (OUTPUT, Path(__file__))}))
    print('28 exact stored lookups, 45 native portrait pages and 207 native floating expansions pass.')


if __name__ == '__main__':
    main()
