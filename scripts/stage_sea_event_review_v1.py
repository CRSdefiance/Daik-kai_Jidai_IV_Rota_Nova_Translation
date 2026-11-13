"""Verify the reviewed sea events through the original stored portrait consumers."""

from hashlib import sha256
from pathlib import Path
import struct
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.layout import format_markup
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sea_event_review_v1 import ARM, BASE, COMMON, OUTPUT, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import PROFILE as STATIC_PROFILE
from scripts.preflight_diplomatic_outcome_wrap_v1 import preview_sheets
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/sea_events_20261110_v1')
ROM = ROOT / 'sea_events_RESEARCH_ONLY.nds'
EVIDENCE = ROOT / 'stored_verification.json'
PARENTS = {
    0x53F0C: (0x02053F40, 0x274),
    0x53D44: (0x02053DB8, 0x27C),
    0x53C24: (0x02053C5C, 0x270),
    0x53BD8: (0x02053C14, 0x270),
}


def native_stored(ctx, row, group, stored):
    number = row['message_ID']
    entry = group['source_native_caller']['consumer'] - BASE
    key = group['selector']
    actor_id = next((i for i, _, n in group['original_actor_voice_choices'] if n == number),
                    3 if number == 469 else number - 477)
    assert 0 <= actor_id < 207
    actor = ctx.actor_root + (0x19E4 if actor_id == 3 else 4 + 32 * actor_id)
    arguments = {
        0x53F0C: (actor, key),
        0x53D44: (group['original_role_argument'], key),
        0x53C24: (number, 0),
        0x53BD8: (key, 0),
    }[entry]
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    seen = {}

    def hook(u, pc, size, _):
        if pc == 0x02053D70:
            # Supply the named test actor as the original role getter's result.
            u.reg_write(UC_ARM_REG_R0, actor_id)
        elif pc == 0x02053C7C:
            # Only the captain-table index varies in this offline fixture.
            u.reg_write(UC_ARM_REG_R0, actor_id)
        elif pc == 0x0205408C:
            u.reg_write(UC_ARM_REG_PC, 0x02054144)
        elif pc == 0x01FFCF3C:
            parent, offset = PARENTS[entry]
            sp = u.reg_read(UC_ARM_REG_SP)
            assert struct.unpack('<I', u.mem_read(sp + 0x264, 4))[0] == parent
            assert struct.unpack('<I', u.mem_read(sp + offset, 4))[0] == key
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), len(stored) + 1)) == stored + b'\0'
            assert u.reg_read(UC_ARM_REG_R2) == (actor if entry in (0x53F0C, 0x53D44) else ctx.actor_root + 0x19E4)
            seen.update(parent=parent, selector_offset=offset, selector=key, output=u.reg_read(UC_ARM_REG_R0))
        else:
            seen['display'] = bytes(u.mem_read(seen['output'], 256)).split(b'\0', 1)[0]
            u.emu_stop()

    hooks = [0x0205408C, 0x01FFCF3C, 0x02054164]
    if entry == 0x53D44:
        hooks.append(0x02053D70)
    if entry == 0x53BD8 and actor_id != 3:
        hooks.append(0x02053C7C)
    for pc in hooks:
        cpu.hook_add(UC_HOOK_CODE, hook, begin=pc, end=pc)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (*arguments, 0, 0), strict=True):
        cpu.reg_write(reg, value)
    cpu.emu_start(BASE + entry, STOP, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x02054164
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    seen.update(message_ID=number, original_entry=BASE + entry,
        supplied_role_actor_ID=actor_id if entry == 0x53D44 else None,
        supplied_captain_index=actor_id if entry == 0x53BD8 and actor_id != 3 else None,
        native_formatter_addresses=sorted(provider.executed_current & {0x01FFCA00, 0x01FFCF78, 0x02132020}))
    ctx.calls.clear()
    return seen


def main():
    assert not ROOT.exists()
    manuscript, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == manuscript['registered_input']
    rows = {row['message_ID']: row for row in manuscript['records']}
    groups = {row['first_ID']: row for row in manuscript['exact_native_event_groups']}
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    # The direct blizzard caller has no paragraph wrapper. Protect the closing
    # idiom as one unit while the validated static profile generates the break.
    body = rows[392]['english']
    markup = format_markup(body.replace('on our hands!', 'on_our_hands!'), STATIC_PROFILE)
    storage[392] = markup.replace('_', ' ').replace('{LB}', '\n  ').encode('ascii')
    assert storage[392].endswith(b'\n  on our hands!') and b' '.join(storage[392].split()) == body.encode('ascii')
    assert all(raw.isascii() and b'%' not in raw for raw in storage.values())
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, target_entries, packing = repack(runtime.common, runtime.arm, rows, storage)
    table = slice(DIRECTORY_OFFSET, TABLE_OFFSET + len(target_entries) * 4)
    assert arm[:table.start] == runtime.arm[:table.start] and arm[table.stop:] == runtime.arm[table.stop:]
    staged = with_components(runtime, arm, common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    cases, pages = [], []
    for n, row in rows.items():
        lookup = current_copy(staged, row | {'current_hex': storage[n].hex()}, BASE + 0x5528C)
        staged.calls.clear()
        case = native_stored(staged, row, groups[row['native_group_first_ID']], storage[n])
        display = case.pop('display')
        assert display.isascii() and b' '.join(display.split()) == row['english'].encode('ascii'), (n, display)
        pixels, glyphs = render(raster, arm, kanji, display)
        assert glyphs[0]['code'] == ord(row['english'][0]) and glyphs[-1]['code'] == ord(row['english'][-1])
        if n == 479:
            assert display.split(b'\n')[-1].strip() == b'All hands to your stations!'
        cases.append(case | dict(arguments=(), display_hex=display.hex(), visible_lines=display.decode('ascii').split('\n'),
            glyphs=len(glyphs), native_ink_sha256=sha256(pixels).hexdigest(), original_stored_lookup=lookup,
            source_reference=row['source_reference'], current_reference=row['current_reference'],
            staged_reference=reference(target_entries[n]), staged_hex=storage[n].hex()))
        pages.append(pixels)
    assert len(cases) == 98
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    rebound = NdsImage.open(ROM)
    assert rebound.read_file(ARM) == arm and rebound.read_file(COMMON) == common
    sheets = FunctionType(preview_sheets.__code__, {**preview_sheets.__globals__, 'ROOT': ROOT})
    save(EVIDENCE, dict(
        registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        storage=packing, complete_serialized_parent_inverse=True,
        ARM9_changes_only_original_COMMON_directory_offsets_and_sizes=True, source_execution_code_unchanged=True,
        source_consumer_scopes=sorted(PARENTS), original_renderer_and_macros_unchanged=True,
        cases=cases, contact_sheets=sheets(cases, pages), font=font, actual_gameplay=False,
        staged_no_release_credit=True, evidence={str(path): digest(path) for path in (OUTPUT, Path(__file__))},
    ))
    print('98 original stored lookups, portrait paths and complete glyph planes pass.')


if __name__ == '__main__':
    main()
