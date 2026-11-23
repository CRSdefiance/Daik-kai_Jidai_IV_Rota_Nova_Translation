"""Check original chart coordinates, share percentages and hidden-value draws."""

from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R8
from unicorn.arm_const import UC_ARM_REG_R10, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_town_chart_punctuation_20261120 as stage
from scripts.probe_button_prompt_native import STACK, VIEW
from scripts.verify_forces_relationships_20261115 import HEADER, font_points
from scripts.verify_inn_numerals_native_20261119 import read_cstring
from scripts.verify_personal_gameplay_v841 import get_machine


BASE, batch = stage.runtime.BASE, stage.batch
OUTPUT = stage.ROOT / 'native_chart.json'
SIZE = 256 * 192 // 2
CONTEXT = STACK + 0x27C
SLOT = 0x02470000
SHARE_X = 99  # Original r0 assignment at 0208D918.
UNKNOWN = ((56, 44), (184, 24), (184, 44), (48, 84), (180, 84))


def chart(arm, raw):
    cpu, native = get_machine(arm, raw)
    header = pack('<5I', 4, 64, 192, 20, 20)
    cpu.mem_write(HEADER - 16, b'\xa5' * 16 + header + bytes(SIZE) + b'\xa5' * 16)
    native(0xD3D80, VIEW)
    cpu.mem_write(STACK, pack('<4I', 256, 192, 0, 0))
    native(0xD3AFC, VIEW, HEADER, 0, 0)
    native(0xD5160, CONTEXT, VIEW, 1)
    return cpu, native, header


def char_plane(cpu, font, header, spans):
    raw = cpu.mem_read(HEADER + 20, SIZE)
    cells = bytes(n for b in raw for n in (b & 15, b >> 4))
    observed = {(k % 256, k // 256) for k, pix in enumerate(cells) if pix}
    expected = set()
    for x, y, text in spans:
        assert 0 <= x and x + len(text) * 6 <= 256 and y + 12 <= 192
        expected.update(font_points(font, text, x, y + 1))
    assert observed == expected
    assert cpu.mem_read(HEADER, 20) == header
    assert cpu.mem_read(HEADER - 16, 16) == cpu.mem_read(HEADER + 20 + SIZE, 16) == b'\xa5' * 16
    return dict(glyph_pixels=len(observed), plane_sha256=batch.digest(cells), full_glyph_bounds=True)


def native_cases(old_arm, arm, original_raw, raw):
    old, old_get, _ = chart(old_arm, original_raw)
    new, get, header = chart(arm, raw)
    font = GameAsciiFont.from_arm9(arm)
    town_root = get(0xCB178) + 4
    assert town_root == old_get(0xCB178) + 4
    headings = []
    for city in range(114):
        town = town_root + city * 108
        labels = []
        for cpu in (old, new):
            cpu.mem_write(HEADER + 20, bytes(SIZE))
            cpu.reg_write(UC_ARM_REG_R10, town)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            seen = []

            def observe(u, _pc, _size, _):
                assert u.reg_read(UC_ARM_REG_R0) == CONTEXT
                at = u.reg_read(UC_ARM_REG_R1)
                seen.append((read_cstring(u, at), unpack_from('<2I', u.mem_read(CONTEXT + 0x24, 8))))

            hook = cpu.hook_add(UC_HOOK_CODE, observe, begin=0x020D5404, end=0x020D5404)
            try:
                cpu.emu_start(0x0208D5B0, 0x0208D670, count=90000)
            finally:
                cpu.hook_del(hook)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x0208D670 and cpu.reg_read(UC_ARM_REG_SP) == STACK
            title, = seen
            labels.append(title)
        (jp, _), (en, (x, y)) = labels
        jp, en = jp.decode('cp932'), en.decode('ascii')
        assert jp.replace('（', ' (').replace('）', ')') == en
        assert x == 128 - (len(en) * 6) // 2 and y == 2
        plane = char_plane(new, font, header, [(x, y, en)])
        headings.append(dict(town_ID=city, old=jp, english=en, origin=[x, y], **plane))

    new.mem_write(HEADER + 20, bytes(SIZE))
    town = town_root + 11 * 108
    get(0xB50B8, town, 1)
    assert get(0xB50D8, town) == 2
    get(0xB50B8, town, 0)
    assert get(0xB50D8, town) == 0
    new.reg_write(UC_ARM_REG_R10, town)
    new.reg_write(UC_ARM_REG_SP, STACK)
    new.emu_start(0x0208D6C0, 0x0208D760, count=90000)
    assert new.reg_read(UC_ARM_REG_PC) == 0x0208D760
    unknown = char_plane(new, font, header, [(x, y, ' ? ') for x, y in UNKNOWN])
    get(0xB50B8, town, 1)
    assert get(0xB50D8, town) == 2

    shares = []
    for value in range(101):
        new.mem_write(HEADER + 20, bytes(SIZE))
        new.mem_write(SLOT, bytes([0, value]))
        new.mem_write(CONTEXT + 0x24, pack('<2I', SHARE_X, 96))
        new.reg_write(UC_ARM_REG_R8, SLOT)
        new.reg_write(UC_ARM_REG_SP, STACK)
        new.emu_start(0x0208DA04, 0x0208DA1C, count=90000)
        assert new.reg_read(UC_ARM_REG_PC) == 0x0208DA1C
        text = f'{value:>3}%'
        plane = char_plane(new, font, header, [(SHARE_X, 96, text)])
        assert SHARE_X + 6 * len(text) == 123
        shares.append(dict(value=value, exact=text, **plane))
    return headings, unknown, shares


def main():
    assert not OUTPUT.exists()
    stored = batch.load(stage.PROOF)
    parent = batch.load(stage.parent.RELEASE)
    snapshot = batch.load(Path(parent['own_registered_startup']))['read_only_snapshot']
    original_raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and batch.digest(original_raw) == snapshot['sha256']
    clean, prior, final = [batch.NdsImage.open(p).read_file(batch.ARM) for p in (batch.CLEAN, stage.parent.ROM, stage.ROM)]
    assert stage.patch(prior, clean) == (final, stored['rows'])
    raw = bytearray(original_raw)
    for row in stored['rows']:
        at, n = row['offset'], row['slot_bytes']
        assert raw[at:at+n].hex() == row['current_hex']
        raw[at:at+n] = final[at:at+n]
    headings, unknown, shares = native_cases(prior, final, original_raw, bytes(raw))
    batch.write(OUTPUT, dict(candidate_sha256=stored['candidate_sha256'], source_snapshot=snapshot,
        title_draws=headings, complete_hidden_field_plane=unknown, hidden_fields=len(UNKNOWN), percentages=shares,
        original_format_order_and_coordinate_signs=True, same_3_cell_numeric_alignment=True, offline_only=True))
    print('All 114 town headings, five hidden fields and 101 legal share percentages passed.')


if __name__ == '__main__':
    main()
