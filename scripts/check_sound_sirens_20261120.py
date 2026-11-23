"""Check selection coverage and compare native and actual SFX title pixels."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_sound_sirens_20261120 as replay
from scripts import stage_sound_sirens_20261120 as stage
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.probe_button_prompt_native import STACK, VIEW, call, machine
from scripts.verify_forces_relationships_20261115 import HEADER, font_points
from scripts.verify_inn_numerals_native_20261119 import read_cstring
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = Path('E:/Rota Nova translations/Generated/work/sound_sirens_20261120')
PROOF, SHEET = stage.ROOT / 'selector_verification.json', stage.ROOT / 'sirens_gameplay.png'
TITLE = (128, 256, 256, 272)
NATIVE_ORIGIN = (128, 208)
COLOR = (230, 230, 230)
OWNER = 0x02470000
WIDTH, HEIGHT = (128, 128)
PIXEL_BYTES = WIDTH * HEIGHT // 2
BASE, batch = stage.runtime.BASE, stage.batch
digest = stage.parent.base.digest


def slot_text(arm, pointer):
    off = pointer - BASE
    return arm[off:off + 24].split(b'\0', 1)[0]


def native_titles(clean, arm, previous, font, raw):
    assert clean[0x108C6C:0x108CB4] == arm[0x108C6C:0x108CB4] == previous[0x108C6C:0x108CB4]
    pointer_slots = unpack_from(f'<{stage.COUNT}I', arm, stage.START)
    declared = batch.load(Path('translations/sound_selector_arm9.json'))['records'][1:]
    historical = {row['offset'] for row in declared}
    assert len(historical) == 57
    assert {p - BASE for p in pointer_slots} - historical == {0x16EF80, 0x16EF8C, 0x16EF98}
    assert len(historical - {p - BASE for p in pointer_slots}) == 1
    assert sum(any(n >= 128 for n in slot_text(previous, ptr)) for ptr in pointer_slots) == 1
    u, _ = get_machine(arm, raw)
    header = pack('<5I', 4, WIDTH // 4, HEIGHT, 20, 20)
    u.mem_write(HEADER - 16, b'\xa5' * 16 + header + bytes(PIXEL_BYTES) + b'\xa5' * 16)
    call(u, 0xD3D80, (VIEW,))
    u.mem_write(STACK, pack('<4I', WIDTH, HEIGHT, 0, 0))
    call(u, 0xD3AFC, (VIEW, HEADER, 0, 0))
    call(u, 0xD5160, (STACK, VIEW, 1))
    calls = []

    def observe(cpu, _pc, _size, _):
        assert cpu.reg_read(UC_ARM_REG_R0) == STACK
        address = cpu.reg_read(UC_ARM_REG_R1)
        calls.append((address, read_cstring(cpu, address), unpack_from('<2I', cpu.mem_read(STACK + 0x24, 8))))

    handle = u.hook_add(UC_HOOK_CODE, observe, begin=0x020D5404, end=0x020D5404)
    rows = []
    try:
        for i, ptr in enumerate(pointer_slots):
            label = slot_text(arm, ptr).decode('ascii')
            assert label and len(label) * 6 <= WIDTH
            source = slot_text(clean, ptr).decode('cp932')
            other = slot_text(previous, ptr)
            assert (other != label.encode('ascii')) == (i == stage.INDEX)
            u.mem_write(HEADER + 20, bytes(PIXEL_BYTES))
            u.mem_write(OWNER + 0x10C, pack('<I', i))
            u.reg_write(UC_ARM_REG_R5, OWNER)
            u.reg_write(UC_ARM_REG_SP, STACK)
            calls.clear()
            u.emu_start(0x02108EC0, 0x02108F00, count=80000)
            assert u.reg_read(UC_ARM_REG_PC) == 0x02108F00 and u.reg_read(UC_ARM_REG_SP) == STACK
            x, y = 64 - len(label) * 3, 50
            assert calls == [(ptr, label.encode('ascii'), (x, y))]
            pix = bytes(n for b in u.mem_read(HEADER + 20, PIXEL_BYTES) for n in (b & 15, b >> 4))
            observed = {(j % WIDTH, j // WIDTH) for j, value in enumerate(pix) if value}
            expected = font_points(font, label, x, y + 1)
            assert observed == expected and u.mem_read(HEADER, 20) == header
            assert u.mem_read(HEADER - 16, 16) == u.mem_read(HEADER + 20 + PIXEL_BYTES, 16) == b'\xa5' * 16
            rows.append(dict(index=i, pointer_field=stage.START + 4 * i, text_offset=ptr - BASE,
                clean_Japanese=source, previous_hex=other.hex(), english=label, current_hex=label.encode('ascii').hex(),
                origin=[x, y], complete_native_raster=True, ink_sha256=batch.digest(pix)))
    finally:
        u.hook_del(handle)

    effect_ptr = unpack_from('<I', arm, 0x108CB4)[0]
    assert effect_ptr == unpack_from('<I', clean, 0x108CB4)[0]
    effects = bytes(arm[effect_ptr - BASE:effect_ptr - BASE + stage.COUNT])
    assert effects == clean[effect_ptr - BASE:effect_ptr - BASE + stage.COUNT]
    for i, row in enumerate(rows):
        row['effect_ID'] = effects[i]
        for step in (-1, 1):
            u.mem_write(OWNER + 0x10C, pack('<I', i))
            u.reg_write(UC_ARM_REG_R0, OWNER)
            u.reg_write(UC_ARM_REG_R1, step & 0xFFFFFFFF)
            u.emu_start(0x02108C6C, 0x02108CA8, count=32)
            assert u.reg_read(UC_ARM_REG_PC) == 0x02108CA8
            selected = (i + step) % stage.COUNT
            assert unpack_from('<2I', u.mem_read(OWNER + 0x108, 8)) == (effects[selected], selected)
    return rows


def main():
    assert not PROOF.exists() and not SHEET.exists()
    staged = batch.load(stage.PROOF)
    clean, old, new = [batch.NdsImage.open(p).read_file(batch.ARM) for p in (batch.CLEAN, stage.parent.ROM, stage.ROM)]
    font = GameAsciiFont.from_arm9(new)
    assert stage.patch(old, clean) == (new, staged['slot'])
    paths = [ROOT / s / 'capture/capture_report.json' for s in ('current', 'revised')]
    before, after = reports = [batch.load(path) for path in paths]
    assert before['core_DLL_sha256'] == after['core_DLL_sha256'] and before['core_options'] == after['core_options']
    for report, key in zip(reports, ('parent_sha256', 'candidate_sha256'), strict=True):
        assert report['ROM_sha256'] == staged[key] and report['frames'] == replay.END
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert report['scripted_input_schedule'] == replay.inputs()
    snapshot = after['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(raw) == 0x400000 and digest(snapshot['path']) == snapshot['sha256']
    rows = native_titles(clean, new, old, font, raw)
    stage_ink, evidence, equal = {}, {str(p): digest(p) for p in paths}, []
    evidence[snapshot['path']] = snapshot['sha256']
    chart = Image.new('RGB', (1032, 308), '#263238')
    draw = ImageDraw.Draw(chart)
    pair = None
    for frame in replay.FRAMES:
        both = [one_frame(report, frame) for report in reports]
        for shot, _ in both:
            evidence[shot['path']] = shot['PNG_sha256']
        delta = ImageChops.difference(*(screen for _, screen in both)).getbbox()
        if frame == replay.SELECT[stage.INDEX]:
            pair = both
            assert delta and delta[0] >= TITLE[0] and delta[1] >= TITLE[1] and delta[2] <= TITLE[2] and delta[3] <= TITLE[3]
        else:
            assert delta is None, (frame, delta)
            equal.append(frame)
        if frame in replay.SELECT or frame == replay.WRAP:
            i = replay.SELECT.index(frame) if frame in replay.SELECT else 0
            row = rows[i]
            x, y = (a + b for a, b in zip(NATIVE_ORIGIN, row['origin'], strict=True))
            stage_ink[frame] = font_mask(both[1][1], font, row['english'], x, y + 1, TITLE, COLOR)
    assert pair and len(stage_ink) == 60
    for column, (_, screen) in enumerate(pair):
        x = column * 516
        draw.text((x + 6, 3), ('Previous', 'Revised')[column], fill='white')
        chart.paste(screen.crop((0, 206, 256, 350)).resize((512, 288), Image.Resampling.NEAREST), (x + 2, 18))
    chart.save(SHEET)
    batch.write(PROOF, dict(candidate_sha256=staged['candidate_sha256'], parent_sha256=staged['parent_sha256'],
        active_selection_count=len(rows), native_direction_checks=len(rows)*2,
        complete_current_actual_title_masks=stage_ink, exact_other_frames=equal, evidence=evidence,
        original_selector_audio_ID_table_preserved=True, button_play_requested_on_Sirens=True, actual_audio_output_checked=False,
        changed_title_frame=replay.SELECT[stage.INDEX], titles=rows, sheet=str(SHEET), sheet_sha256=digest(SHEET),
        hardware=False))
    print(f'All {len(rows)} actual SFX titles, wraparound and 118 native selection transitions passed.')


if __name__ == '__main__':
    main()
