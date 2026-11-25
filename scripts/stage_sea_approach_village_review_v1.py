"""Prove stored and native portrait display for the sea and village review."""

from hashlib import sha256
from pathlib import Path
import struct
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.sea_approach_village_wrap_v1 import DYNAMIC, PRIOR, STATIC, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import stage_ship_emergency_review_v1 as emergency
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sea_approach_village_review_v1 import ARM, BASE, COMMON, IDS, OUTPUT, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_call_abi_v764 import call
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/sea_approach_village_20261111_v1')
ROM = ROOT / 'sea_approach_village_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_sea_approach_village_verification.json'
PARENTS = {0x53CB0: 0x02053D24, 0x53D44: 0x02053DB8}
PHRASES = {
    1320: ('a village in sight!',),
    1321: ('their food and water with us.',),
    1322: ('food and water', 'from the villagers.'),
    1323: ('some food and water with us.',),
    1324: ('some of their food and water.',),
    1325: ('food and water with us.',),
    1326: ('their food and water with us.',),
    1327: ('food and water', 'from the villagers!'),
    1328: ('were kind enough', 'to share their food and water.'),
    1329: ('Their hospitality cheered everyone.',),
    1330: ('The villagers welcomed us,', "everyone's in good spirits."),
    1331: ('The villagers made us feel welcome.', "Everyone's happy about it."),
    1332: ('The villagers treated us well.', 'Put everybody in a good mood.'),
    1333: ('feel right at home.', "Everyone's pleased."),
    1334: ('That meal from the villagers', "Everyone's happy."),
    1335: ('Their hospitality cheered everyone.',),
    1336: ('took care of our ship repairs.',),
    1337: ('fixed up the fleet for us.',),
    1338: ('did our ship repairs for us.',),
    1339: ('handled the ship repairs for us.',),
    1340: ("the fleet's repairs.",),
    1341: ('fixed up the fleet for us!',),
    1342: ('taken care of our ship repairs.',),
}


def compile_storage(rows):
    static = {n: row for n, row in rows.items() if not row['original_substitutions']}
    phrases = {n: tokens for n, tokens in PHRASES.items() if len(rows[n]['english']) > 36}
    compiler = FunctionType(compile_layouts.__code__, {**compile_layouts.__globals__, 'PHRASES': phrases})
    compiled = compiler(static)
    return {n: compiled[n] if n in compiled else row['english'].encode('ascii') for n, row in rows.items()}


def rebuild_components(arm, common, rows, storage):
    patched, selector = transform(arm)
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    target_common, target_arm, rebound, packing = repack(common, patched, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    return target_arm, target_common, rebound, packing, selector


def original_portrait(ctx, row, group, stored, argument):
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    actor_id = next(i for i, _, message in group['original_voice_choices'] if message == row['message_ID'])
    actor = ctx.actor_root + (0x19E4 if actor_id == 3 else 4 + 32 * actor_id)
    entry, key = group['consumer'] - BASE, group['table']
    choice = entry == 0x53CB0
    actor_return = 0x02053CDC if choice else 0x02053D70
    parent = PARENTS[entry]
    buffer = 0x02470000
    if argument:
        cpu.mem_write(buffer, argument + b'\0')
    expanded = stored % argument if argument else stored
    seen = {}

    def hook(u, pc, size, _):
        if pc == actor_return:
            u.reg_write(UC_ARM_REG_R0, actor_id)
        elif pc == 0x0205408C:
            assert struct.unpack('<I', u.mem_read(u.reg_read(UC_ARM_REG_SP) + 8, 4))[0] == int(choice)
            u.reg_write(UC_ARM_REG_PC, 0x02054144)
        elif pc == 0x01FFCF3C:
            sp = u.reg_read(UC_ARM_REG_SP)
            assert struct.unpack('<I', u.mem_read(sp + 0x264, 4))[0] == parent
            assert struct.unpack('<I', u.mem_read(sp + 0x27C, 4))[0] == key
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), len(expanded) + 1)) == expanded + b'\0'
            assert u.reg_read(UC_ARM_REG_R2) == actor
            seen['output'] = u.reg_read(UC_ARM_REG_R0)
        elif pc == 0x02054164:
            seen['display'] = bytes(u.mem_read(seen['output'], 256)).split(b'\0', 1)[0]
            u.emu_stop()

    for address in (actor_return, 0x0205408C, 0x01FFCF3C, 0x02054164):
        cpu.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3),
            (group['original_role_argument'], key, buffer if argument else 0, 0), strict=True):
        cpu.reg_write(register, value)
    cpu.emu_start(BASE + entry, STOP, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x02054164 and len(seen) == 2
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return seen['display'], dict(original_entry=group['consumer'], original_table=key, choice=choice,
        supplied_offline_actor_ID=actor_id, original_file_reads=provider.reads)


def expanded_layout(cpu, stored, group, argument):
    output, template, parameter, wrapped = (0x02420020, 0x02420400, 0x02420800, 0x02420C20)
    guard = b'\xa5' * 16
    cpu.mem_write(output - 16, guard * 18)
    cpu.mem_write(wrapped - 16, guard * 18)
    cpu.mem_write(template, stored + b'\0')
    cpu.mem_write(parameter, argument + b'\0')
    call(cpu, 0xD7720, (output, template, parameter, 0), instruction_limit=2000000)
    expected = stored % argument
    assert bytes(cpu.mem_read(output, len(expected) + 1)) == expected + b'\0'
    assert bytes(cpu.mem_read(output + len(expected) + 1, 271 - len(expected))) == b'\xa5' * (271 - len(expected))
    parent = PARENTS[group['consumer'] - BASE]
    cpu.mem_write(STACK + 0x264, struct.pack('<I', parent))
    cpu.mem_write(STACK + 0x27C, struct.pack('<I', group['table']))
    call(cpu, 0x01FFCF3C - BASE, (wrapped, output, 0, 0), instruction_limit=2000000)
    after = bytes(cpu.mem_read(wrapped, 256))
    assert b'\0' in after
    display, tail = after.split(b'\0', 1)
    assert tail == b'\xa5' * len(tail)
    for pointer in (output, wrapped):
        assert bytes(cpu.mem_read(pointer - 16, 16)) == bytes(cpu.mem_read(pointer + 256, 16)) == guard
    return display


def variants(group, arguments):
    if not group['arguments']:
        return [(None, b'')]
    kind, = group['arguments']
    if kind == 'faction_label':
        variants = [(row['label'], bytes.fromhex(row['hex'])) for row in arguments[kind]]
        return variants + [('literal-macro stress', b'FIFOFOFU'), ('long-label stress', b'Northern Compass Co.')]
    if kind == 'port_label':
        return [(row['label'], bytes.fromhex(row['hex'])) for row in arguments[kind]]
    values = arguments['decimal']
    if kind == 'gold_amount':
        values = [row for row in values if row['value'] <= 5]
    return [(row['value'], bytes.fromhex(row['hex'])) for row in values]


def main():
    assert not ROOT.exists()
    review, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert review['registered_input'] == runtime.receipt()
    assert all(digest(path) == expected for path, expected in review['evidence'].items())
    rows = {row['message_ID']: row for row in review['records']}
    assert tuple(rows) == IDS
    storage = compile_storage(rows)
    arm, common, rebound, packing, selector = rebuild_components(runtime.arm, runtime.common, rows, storage)
    check_scope = FunctionType(emergency.verify_scope.__code__, {**emergency.verify_scope.__globals__,
        'PRIOR': PRIOR, 'DYNAMIC': DYNAMIC, 'STATIC': STATIC})
    scope = check_scope(arm)
    staged = with_components(runtime, arm, common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    cpu = machine(arm)
    groups = {n: group for group in review['exact_native_groups']
              for n in range(group['first_ID'], group['last_ID'] + 1)}
    results, lookups, pages, matrix, findings = [], [], [], [], []
    for n, row in rows.items():
        stored, group = storage[n], groups[n]
        looked_up = current_copy(staged, row | {'current_hex': stored.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=stored.hex(), original_stored_lookup=looked_up))
        args = variants(group, review['original_arguments'])
        # The widest real name or largest numeric case exercises the full wrapper.
        index = max(range(len(args)), key=lambda i: len(args[i][1]))
        value, sample = args[index]
        shown, path = original_portrait(staged, row, group, stored, sample)
        images = set()
        for i, (label, argument) in enumerate(args):
            display = expanded_layout(cpu, stored, group, argument) if argument else shown
            expected = row['english'].encode('ascii')
            expected = expected % argument if argument else expected
            assert b' '.join(display.split()) == expected, (n, label, display)
            if i == index:
                assert display == shown, (n, label)
            if b'\n' in stored:
                assert display == stored, (n, display)
            lines = display.split(b'\n')
            assert 1 <= len(lines) <= 4 and all(line.strip() and len(line.strip()) * 6 <= 216 for line in lines)
            assert all(len(line.strip()) <= 35 for line in lines[1:])
            visible = [line.strip().decode('cp932') for line in lines]
            matrix.append(dict(message_ID=n, argument=label, display_hex=display.hex(), lines=visible))
            if argument and not any(argument in line for line in lines):
                findings.append(dict(message_ID=n, argument=label, issue='split substitution', lines=visible))
            if path['choice'] and '?' in visible[-1] and len(visible[-1].split()) < 3:
                findings.append(dict(message_ID=n, argument=label, issue='short final question row', lines=visible))
            if i in (0, index) and display not in images:
                pixels, glyphs = render_portrait(raster, arm, kanji, display)
                assert [g['code'] for g in (glyphs[0], glyphs[-1])] == [
                    int.from_bytes(c.encode('cp932'), 'big') for c in (visible[0][0], visible[-1][-1])]
                pages.append((f'{n} / {label}' if label is not None else str(n), pixels))
                results.append(path | dict(message_ID=n, argument=label, display_hex=display.hex(),
                    visible_lines=visible, native_ink_sha256=sha256(pixels).hexdigest(), complete_glyphs=len(glyphs)))
                images.add(display)
    assert len(lookups) == len(rows) == 67
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    assert NdsImage.open(ROM).read_file(ARM) == arm and NdsImage.open(ROM).read_file(COMMON) == common
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        stored=lookups, storage=packing, selector=selector, selector_scope=scope, native_cases=results,
        all_substitution_layouts=matrix, layout_findings=findings, contact_sheets=portrait_sheets(ROOT, pages),
        font=font, complete_serialized_ROM_parent_inverse=True, actual_gameplay=False, new_credit=0,
        evidence={str(path): digest(path) for path in (OUTPUT, Path(__file__))}))
    print(f'67 stored records, {len(matrix)} layout cases and {len(pages)} native raster pages. '
          f'{len(findings)} phrase-boundary findings to review.')


if __name__ == '__main__':
    main()
