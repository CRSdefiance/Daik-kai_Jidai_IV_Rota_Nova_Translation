"""Verify the original price handoff, digit ring and complete confirmation glyphs."""

from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_SP

from scripts import check_departure_numerals_native_20261119 as departure
from scripts import check_swimmer_leak_square_dialogue_20261120 as sample
from scripts import replay_madeira_resupply_numerals_20261120 as play
from scripts import stage_madeira_resupply_numerals_20261120 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import STACK, call
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_inn_numerals_native_20261119 import normalize, read_cstring
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold
from scripts.verify_personal_gameplay_v841 import get_machine


batch = stage.batch
NATIVE = stage.ROOT / 'native_price.json'
LIVE = stage.ROOT / 'played_resupply.json'
CAPTURE = Path('E:/Rota Nova translations/Generated/work/madeira_resupply_numerals_20261120_replay_v2/capture/capture_report.json')
AMOUNTS = (1, 9, 10, 99, 100, 260, 999, 1000, 65535, 2147483647)
RECORD = 49


def digest(path):
    return batch.digest(Path(path).read_bytes())


def models():
    assert not NATIVE.exists()
    proof = batch.load(stage.PROOF)
    assert digest(stage.ROM) == proof['candidate_sha256'] and digest(batch.ROM) == proof['staged_parent_sha256']
    old, new, clean = map(batch.NdsImage.open, (batch.ROM, stage.ROM, batch.CLEAN))
    old_arm, arm, source_arm = [rom.read_file(batch.ARM) for rom in (old, new, clean)]
    common = new.read_file(batch.COMMON)
    assert old.read_file(batch.COMMON) == common
    assert stage.patch(old_arm, source_arm)[0] == arm
    old_report = batch.load(play.REFERENCE)
    assert old_report['ROM_sha256'] == proof['staged_parent_sha256']
    snapshot, ram = sample.ram_at(old_report, 10427)
    at = stage.CALL - stage.BASE
    assert ram[at:at+4] == old_arm[at:at+4]
    actual = ram[:at] + arm[at:at+4] + ram[at+4:]
    old_cpu, _ = get_machine(old_arm, ram)
    new_cpu, get = get_machine(arm, actual)
    actor = get(0xB2CD8, get(0xB6618), 3)
    assert actor != 0
    verify_ring = FunctionType(departure.verify_numbers.__code__, departure.verify_numbers.__globals__ |
                               {'CASES': {stage.CALL: AMOUNTS}})
    ring = verify_ring(old_cpu, new_cpu)
    assert len(ring) == len(AMOUNTS) * 32
    table = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    source = batch.common_message_entries(clean.read_file(batch.COMMON), source_arm)
    template = table[RECORD].text
    assert template == b'Want to resupply for %s gold?' and source[RECORD].text.count(b'%s') == 1
    painter, _, font = font_tools(new)
    kanji = new.read_file('/GRP/KANJI.FNT')
    pages, cases = [], []
    def call_modal(cpu, offset, arguments):
        return call(cpu, offset, arguments, instruction_limit=2_000_000)

    layout = FunctionType(native_layout.__code__, native_layout.__globals__ | {'call': call_modal}, argdefs=native_layout.__defaults__)
    for amount in AMOUNTS:
        values = []
        for cpu in (old_cpu, new_cpu):
            cpu.mem_write(STACK, pack('<8I', *(0,) * 3, actor, *(0,) * 4))
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.reg_write(UC_ARM_REG_R4, amount)
            cpu.emu_start(0x020607C4, 0x020607E0, count=10000)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x020607E0 and cpu.reg_read(UC_ARM_REG_SP) == STACK
            assert cpu.reg_read(UC_ARM_REG_R0) == actor and cpu.reg_read(UC_ARM_REG_R1) == RECORD
            values.append(read_cstring(cpu, cpu.reg_read(UC_ARM_REG_R2)))
        old_value, value = values
        assert value == normalize(old_value) == str(amount).encode('ascii')
        body, lines = layout(new_cpu, template, RECORD, (value.decode('ascii'),), parent=0x02053FCC)
        assert b' '.join(body.split()) == (template % (value,)) and 1 <= len(lines) <= 2
        pixels, glyphs = render_portrait(painter, arm, kanji, body)
        codes = [glyph['code'] for glyph in glyphs]
        assert codes == glyph_codes(body) and (codes[0], codes[-1]) == (ord('W'), ord('?'))
        assert all(code < 128 for code in codes)
        pages.append((f'Resupply / {amount}', pixels))
        cases.append(dict(amount=amount, before_argument_hex=old_value.hex(), after_argument_hex=value.hex(),
                          native_handoff_actor=actor, native_handoff_message=RECORD, display_hex=body.hex(),
                          lines=lines, full_glyph_mask_sha256=batch.digest(pixels), page_count=1))
    sheets = portrait_sheets(stage.ROOT, pages)
    batch.write(NATIVE, dict(candidate_sha256=proof['candidate_sha256'], record=RECORD, font=font,
                            source_reference=reference(source[RECORD]), current_reference=reference(table[RECORD]),
                            source_hex=source[RECORD].text.hex(), current_hex=template.hex(), source_RAM=snapshot,
                            decision='retention', reason='The Port Worker’s price question fits the Yes and No prompt and retains the exact cost argument.',
                            ascii_regular_digit_correction=True, tested_ring_cases=ring,
                            tested_natural_layouts=cases, sheets=sheets))
    print(f'{len(ring)} native ring cases and {len(cases)} original price handoffs and display cases passed.')


def gameplay():
    assert not LIVE.exists()
    native = batch.load(NATIVE)
    earlier, current = map(batch.load, (play.REFERENCE, CAPTURE))
    previous = batch.load(stage.PROOF)
    assert current['ROM_sha256'] == previous['candidate_sha256'] == native['candidate_sha256']
    assert earlier['ROM_sha256'] == previous['staged_parent_sha256']
    for report in (earlier, current):
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert digest(report['battery_save_preloaded']['source']) == report['battery_save_preloaded']['source_sha256']
    assert current['scripted_input_schedule'][:len(earlier['scripted_input_schedule'])] == earlier['scripted_input_schedule']
    rom = batch.NdsImage.open(stage.ROM)
    arm, kanji = [rom.read_file(path) for path in (batch.ARM, '/GRP/KANJI.FNT')]
    at = unpack_from('<I', arm, 0x54450)[0] - stage.BASE
    quote_frame = 10427
    old_ram, new_ram = [sample.ram_at(report, quote_frame) for report in (earlier, current)]
    old_quote, new_quote = [ram[at:at+256].split(b'\0')[0] for _, ram in (old_ram, new_ram)]
    assert old_quote == b' Want to resupply for \x82Q\x82U\x82O gold?'
    assert new_quote == b' Want to resupply for 260 gold?'
    assert normalize(old_quote) == new_quote
    shots = [sample.one_frame(report, quote_frame) for report in (earlier, current)]
    for left, right in (((0, 192, 256, 294), (0, 192, 256, 294)), ((100, 340, 250, 380), (100, 340, 250, 380))):
        assert shots[0][1].crop(left).tobytes() == shots[1][1].crop(right).tobytes()
    paint, _, _ = font_tools(rom)
    old_pixels, _ = render_portrait(paint, arm, kanji, old_quote)
    new_pixels, _ = render_portrait(paint, arm, kanji, new_quote)
    ink = [native_hold(shot[1], plane) for shot, plane in zip(shots, (old_pixels, new_pixels), strict=True)]
    follow = []
    for frame in (10227, 10627, 10827):
        before, after = [sample.one_frame(report, frame)[0] for report in (earlier, current)]
        assert before['framebuffer_sha256'] == after['framebuffer_sha256']
        follow.append(after)
    comparison = stage.ROOT / 'resupply_comparison.png'
    sheet = sample.Image.new('RGB', (1024, 404), '#263238')
    draw = sample.ImageDraw.Draw(sheet)
    for i, (_, photo) in enumerate(shots):
        draw.text((i*512+5, 4), ('Previous', 'Regular digits')[i], fill='white')
        sheet.paste(photo.crop((0, 192, 256, 384)).resize((512, 384), sample.Image.Resampling.NEAREST), (i*512, 19))
    sheet.save(comparison)
    batch.write(LIVE, dict(candidate_sha256=previous['candidate_sha256'], quote_frame=quote_frame,
                           before_body=old_quote.hex(), after_body=new_quote.hex(), quote_masks=ink,
                           quote_shots=[row for row, _ in shots], read_only_quote_RAM=[row for row, _ in (old_ram, new_ram)],
                           exact_speaker_choices_and_return_frames=True, later=follow,
                           observed_gold_before=6740, observed_gold_after=6480,
                           fixture_scope='Starting voyage coordinates and restored selector only. Docking and purchase used ordinary input.',
                           report=str(CAPTURE), report_sha256=digest(CAPTURE),
                           comparison=str(comparison), comparison_sha256=digest(comparison)))
    print('Complete before and after masks, the 260-gold quote and its purchase transition matched.')


if __name__ == '__main__':
    import sys

    (gameplay if sys.argv[1:] == ['gameplay'] else models)()
