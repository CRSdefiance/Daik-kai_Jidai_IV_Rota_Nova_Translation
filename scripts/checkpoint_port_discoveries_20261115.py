"""Bind the current discovery replay and stock name substitutions to original consumers."""

from pathlib import Path
from struct import unpack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts import observe_port_discoveries_20261115 as replay
from scripts.preflight_shared_dynamic_notice_wrap_v1 import HEIGHT, WIDTH, font_tools, render
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.record_navigation_v327 import dark_text
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference

base, current = replay.base, replay.current
COMMON, ARM = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/port_discovery_consumers_20261115_v1.json')
WRAPPER, VARARGS, FORMATTED = 0x020546B8, 0x02054774, 0x0205479C
PATHS = (
    ('city', 297, 90, 0x78DD0, 0x78DE8, UC_ARM_REG_R7, 0xCB178, 0x6C),
    ('remote port', 297, 24, 0x7877C, 0x78794, UC_ARM_REG_R6, 0xCB118, 0),
    ('announced item', 340, 218, 0x2BAA8, 0x2BAC0, UC_ARM_REG_R5, 0xCB190, 0x14),
)


def observed(ctx, stored):
    folder = replay.ROOT / 'ports'
    receipt = folder / 'terminal.json'
    capture = folder / 'capture/capture_report.json'
    requests = folder / 'requests.json'
    terminal, report, trace = map(base.load, (receipt, capture, requests))
    events, _, end, _, donor = replay.schedule('ports')
    assert terminal['completed_frames'] == report['frames'] == end
    assert terminal['ROM_sha256'] == report['ROM_sha256'] == ctx.release['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == events
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert trace['source_requests'] == terminal['target_COMMON_calls']
    pairs = trace['source_requests']
    assert len(pairs) == 18 and [r['message_ID'] for r in pairs[::2]] == [85, 86, 65, 1296, 297, 1296, 297, 97, 97]
    for direct, cache in zip(pairs[::2], pairs[1::2], strict=True):
        assert (direct['PC'], cache['PC']) == (0x0205528C, 0x020534F4)
        assert all(direct[k] == cache[k] for k in ('frame', 'message_ID', 'caller_LR'))
    frames = {row['frame']: row for row in report['frames_captured']}
    font = GameAsciiFont.from_arm9(ctx.arm)
    checked = []
    for at, (n, frame, place) in enumerate(((1296, 6290, 'Tunis'), (297, 6390, 'Tunis'),
                                            (1296, 7455, 'Syracuse'), (297, 7555, 'Syracuse')), start=3):
        event = pairs[at * 2]
        assert event['message_ID'] == n and 0 <= frame - event['frame'] < 100
        text = stored[n].text.decode('ascii')
        text = text % place if n == 297 else text
        row = frames[frame]
        assert base.digest(row['path']) == row['PNG_sha256']
        with Image.open(row['path']) as screenshot:
            mask = dark_text(font, text, screenshot.convert('RGB'), (8, 292, 250, 345))
            assert mask['complete_ink_and_blank_cells_exact']
        checked.append({'port': place, 'frame': frame, 'source_request': event, 'mask': mask, 'capture': row})
    return {'replay_receipts': {str(p): base.digest(p) for p in (receipt, capture, requests)},
                'battery_source_sha256': donor['source_sha256'], 'prepared_save': True,
                'normal_input_no_state_fixture': True, 'requests': pairs[::2], 'complete_panels': checked}


def native_cases(ctx, clean_arm, path, template):
    owner, n, count, start, branch, model_reg, root_getter, stride = path
    assert ctx.arm[start:branch + 4] == clean_arm[start:branch + 4]
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    root = get(root_getter)
    fmt, output = unpack_from('<2I', ctx.arm, 0x54890)
    recorded = []

    def read_text(at, maximum):
        before, terminator, _ = bytes(cpu.mem_read(at, maximum)).partition(b'\0')
        assert terminator
        return before

    def check_template(u, pc, size, _):
        ptr = u.reg_read(UC_ARM_REG_R1)
        vector = u.reg_read(UC_ARM_REG_R2)
        assert read_text(ptr, len(template) + 1) == template
        recorded.append((ptr, unpack('<I', u.mem_read(vector, 4))[0]))

    cpu.hook_add(UC_HOOK_CODE, check_template, begin=VARARGS, end=VARARGS)
    results = []
    for index in range(count):
        obj = root + 4 + index * stride if stride else get(0xCACAC, root, index)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.reg_write(model_reg, obj)
        cpu.emu_start(BASE + start, BASE + branch, count=5000)
        assert cpu.reg_read(UC_ARM_REG_PC) == BASE + branch and cpu.reg_read(UC_ARM_REG_R0) == n
        ptr = cpu.reg_read(UC_ARM_REG_R1)
        assert ptr and ptr != obj
        name = read_text(ptr, 64)
        assert name and all(32 <= byte <= 126 for byte in name)
        cpu.reg_write(UC_ARM_REG_R2, 0)
        cpu.reg_write(UC_ARM_REG_R3, 0)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.emu_start(WRAPPER, FORMATTED, count=3000000)
        assert cpu.reg_read(UC_ARM_REG_PC) == FORMATTED and recorded[-1][1] == ptr
        expanded, display = read_text(fmt, 256), read_text(output, 256)
        assert expanded == template % name and b' '.join(display.split()) == expanded
        lines = display.split(b'\n')
        assert 1 <= len(lines) <= 3 and all(0 < len(line) <= 36 for line in lines)
        results.append({'index': index, 'name': name.decode('ascii'), 'pointer': ptr,
                            'display_hex': display.hex(), 'lines': [line.decode('ascii') for line in lines]})
    assert len(recorded) == count and len({ptr for ptr, _ in recorded}) == 1
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return {'consumer': owner, 'message_ID': n, 'first_instruction': BASE + start,
                'call_instruction': BASE + branch, 'original_caller_hex': ctx.arm[start:branch + 4].hex(),
                'wrapper': WRAPPER, 'stored_template_pointer': recorded[0][0], 'verified_cases': results,
                'complete_relevant_instructions_executed': len(provider.executed_current)}


def preview(ctx, groups):
    raster, _, _ = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    sheet = Image.new('RGB', (936, 115 * len(groups)), '#263238')
    draw = ImageDraw.Draw(sheet)
    pages = []
    for j, group in enumerate(groups):
        rows = group['verified_cases']
        def rank(row):
            return (sum(map(len, row['lines'])), row['index'])
        for i, row in enumerate((min(rows, key=rank), max(rows, key=rank))):
            raw = bytes.fromhex(row['display_hex'])
            pixels, glyphs = render(raster, ctx.arm, kanji, raw)
            x, y = 468 * i + 4, 115 * j
            label = f"{group['consumer']}  {'shortest' if i == 0 else 'longest'}"
            draw.text((x, y + 1), label, fill='white')
            page = Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if value else 255 for value in pixels))
            sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x, y + 16))
            pages.append(dict(consumer=group['consumer'], **row, native_ink_glyphs=len(glyphs)))
    path = replay.ROOT / 'discovery_name_samples.png'
    sheet.save(path)
    return {'path': str(path), 'sha256': base.digest(path), 'pages': pages}


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    clean = base.NdsImage.open(current.stage.CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = base.sha256(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    stored = owned_entries(ctx.common, ctx.arm, directory)
    gameplay = observed(ctx, stored)
    groups = [native_cases(ctx, clean_arm, path, stored[path[1]].text) for path in PATHS]
    assert [(g['message_ID'], len(g['verified_cases'])) for g in groups] == [(297, 90), (297, 24), (340, 218)]
    assert 'Inuvik' in {row['name'] for row in groups[1]['verified_cases']}
    decisions = {
        1296: 'Already reviewed. Spotted a port is an idiomatic lookout call and keeps Admiral and the excitement.',
        297: 'Already reviewed. Discovered is the concise official result after the lookout speaks and accepts the original place name.',
        340: 'Already reviewed. You got preserves a direct acquisition announcement and the original item name.',
        287: 'The emphatic stored variant sounds natural. The observed ports and tested callers did not select it. Other display ownership remains open.',
    }
    references = {n: {'source_reference': reference(source[n]), 'current_reference': reference(stored[n]),
        'Japanese': source[n].text.decode('cp932'), 'English': stored[n].text.decode('cp932'),
        'source_hex': source[n].text.hex(), 'current_hex': stored[n].text.hex(), 'finding': note,
        'revision': False, 'previously_reviewed': n != 287} for n, note in decisions.items()}
    base.save(OUTPUT, {'runtime': ctx.receipt(), 'gameplay': gameplay, 'offline_native_cases': groups,
        'records': references, 'native_preview': preview(ctx, groups), 'original_287_caller_verified': False,
        'new_editorial_credit': 0, 'ROM_changed': False, 'hardware': False, 'producer_sha256': base.digest(__file__)})
    print('Two port discoveries, four complete captured panels and 332 stock name expansions verified.')


if __name__ == '__main__':
    main()
