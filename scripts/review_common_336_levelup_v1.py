"""Reconcile the native COMMON 336 growth result and its reviewed paged display."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R5, UC_ARM_REG_R7, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_SP,
)

from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_visible_online_captions_v1 as parent
from scripts import verify_levelup_runtime_v819 as earlier
from scripts.probe_button_prompt_native import STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import owned_entries, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sound_bgm_titles_v1 import get_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font


base = parent.base
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/common_336_levelup_context_v1.json')
CONFIG = Path('translations/levelup_stat_format_release_v1.json')
ENTRY = 0x01FFCE40 - 0x02000000
TEXT_SPAN = (0x7E480, 0x7E554)


def terminated(cpu, at):
    raw = bytes(cpu.mem_read(at, 256))
    assert b'\0' in raw
    return raw.split(b'\0', 1)[0]


def native_growth(ctx, amounts, original):
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    sp, observations = STACK - 0x400, []
    buffer = sp + 0x38
    cpu.mem_write(sp - 64, b'\xa5' * (0x440))
    cpu.mem_write(buffer, b'\0')
    cpu.reg_write(UC_ARM_REG_SP, sp)
    cpu.emu_start(0x0207E480, 0x0207E488, count=2)
    assert unpack_from('<I', cpu.mem_read(sp+0x14, 4))[0] == 336

    def arguments(u, _pc, _size, _data):
        args = [u.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        assert terminated(u, args[1]) == original
        observations.append(tuple(terminated(u, at) for at in args[2:]))

    cpu.hook_add(UC_HOOK_CODE, arguments, begin=0x0207E534, end=0x0207E534)
    for index, amount in enumerate(amounts):
        if not amount:
            continue
        append = buffer + len(terminated(cpu, buffer))
        cpu.reg_write(UC_ARM_REG_R7, index)
        cpu.reg_write(UC_ARM_REG_R10, amount)
        cpu.reg_write(UC_ARM_REG_R9, append)
        cpu.emu_start(0x0207E508, 0x0207E548, count=3000000)
        assert cpu.reg_read(UC_ARM_REG_PC) == 0x0207E548
    raw = b''.join(original % pair + b'\n' for pair in observations)
    assert terminated(cpu, buffer) == raw and b'\0' not in raw

    captured = []

    def modal(u, _pc, _size, _data):
        ptr = u.reg_read(UC_ARM_REG_R0)
        assert ptr == buffer + earlier.COPY_OFFSET
        captured.append(terminated(u, ptr))
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, modal, begin=0x0205473C, end=0x0205473C)
    cpu.reg_write(UC_ARM_REG_R5, 1)
    cpu.emu_start(0x0207E554, 0x0207E570, count=3000000)
    compiled = b' ' + b'\n  '.join(raw.splitlines())
    assert captured == [compiled] and cpu.reg_read(UC_ARM_REG_PC) == 0x0205473C
    assert terminated(cpu, buffer) == raw and len(compiled) < 768 - earlier.COPY_OFFSET
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return observations, raw, compiled, provider.reads


def page_masks(ctx, compiled):
    raster = get_raster(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    # Reuse the independent mask at the current ASCII Y+1 position.
    source = checked_text(getsource(independent_font), {
        '(row * 16 + y) * 228 + x + dx': '(row * 16 + y + (len(code) == 1)) * 228 + x + dx',
    })
    env = independent_font.__globals__.copy()
    exec(compile(source, __file__ + '::current-ASCII-row-origin', 'exec'), env)
    rows = [r.decode('cp932').strip() for r in compiled.splitlines()]
    remaining, pages = compiled, []
    for start in range(0, len(rows), 4):
        text = rows[start:start+4]
        plane, consumed = raster(ctx.arm, remaining, ENTRY, size=(228, 64), complete=False, instruction_limit=2000000)
        assert plane == env['independent_font'](ctx.arm, kanji, text)
        assert consumed > 0
        remaining = remaining[consumed:]
        pages.append(dict(rows=text, consumed_bytes=consumed, native_plane_sha256=sha256(plane).hexdigest()))
    assert not remaining
    return pages


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(parent.CLEAN)
    source_arm = clean.read_file(parent.ARM)
    lo, hi = TEXT_SPAN
    assert source_arm[lo:hi] == ctx.arm[lo:hi]
    config = base.load(CONFIG)
    for row in config['owned_patches']:
        offset = row['address'] - 0x02000000
        expected = bytes.fromhex(row['after_hex'])
        assert ctx.arm[offset:offset+len(expected)] == expected
    for name in ('ordinary_gameplay_proof', 'maximum_gameplay_proof'):
        path = config[name]
        assert base.digest(path) == config['dependencies'][path]
    jp = common_message_entries(clean.read_file(parent.COMMON), source_arm)[336]
    active = owned_entries(ctx.common, ctx.arm, sha256(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())[336]
    assert jp.text.decode('cp932') == '%sが\n%s上がりました！'
    assert active.text == b'%s increased by %s!'
    cases = []
    for amounts in ((1, 0, 0, 0, 0, 0), (0, 2, 0, 3, 0, 0), (3, 3, 3, 3, 3, 3)):
        observed, raw, compiled, reads = native_growth(ctx, amounts, active.text)
        assert [n.decode('cp932') for _, n in observed] == [chr(0xFF10 + gain) for gain in amounts if gain]
        pages = page_masks(ctx, compiled)
        cases.append(dict(amounts=amounts, arguments=[dict(stat=k.decode('cp932'), amount=n.decode('cp932'))
                          for k, n in observed], original_joined_hex=raw.hex(), formatted_hex=compiled.hex(),
                          native_pages=pages, native_loader_reads=reads))
    assert list(map(lambda page: len(page['rows']), cases[-1]['native_pages'])) == [4, 2]
    base.save(OUTPUT, dict(id='COMMON_MESSAGE_336', file_path=parent.COMMON,
        current_ROM_sha256=release['candidate_sha256'], source_reference=reference(jp),
        current_reference=reference(active), source_Japanese=jp.text.decode('cp932'),
        current_English=active.text.decode('ascii'), english=active.text.decode('ascii'), decision='retention',
        source_meaning='The named stat increased by the supplied amount.',
        localization_note='The current notice states the stat first and the exact increase second. Its exclamation matches the original announcement.',
        context='One row of the stat increases shown after a character’s level-up. The game joins rows and paginates up to six.',
        speaker='Stat increase notice', review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
        original_caller=0x0207E50C, original_stat_name_getter=0x0207EED8, original_amount_formatter=0x020ABF50,
        original_modal=0x0205473C, original_substitution_count=2, native_cases=cases,
        earlier_ordinary_and_maximum_gameplay={name: config[name] for name in
            ('ordinary_gameplay_proof', 'maximum_gameplay_proof')},
        new_gameplay=False, offline_native_current=True, registration_pending=True,
        full_goal_complete=False, new_editorial_credit=0))
    print('COMMON 336 verified with original stat names, full-width gain digits, and native four-plus-two pagination.')


if __name__ == '__main__':
    main()
