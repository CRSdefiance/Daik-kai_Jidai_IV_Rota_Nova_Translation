"""Bind both Palace displays to original fees, native layout, and gameplay."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R2, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_SP

from scripts import stage_palace_contract_fee_20261120 as stage
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame, ram_at
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import STACK, call
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_inn_numerals_native_20261119 import normalize, read_cstring
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = stage.ROOT
PROOF, SHEET = ROOT / 'contract_verification.json', ROOT / 'contract_gameplay.png'
CAPTURE = Path('E:/Rota Nova translations/Generated/work/palace_contract_fee_20261120/paired_v1')
BASE, batch = stage.ruin.BASE, stage.batch
digest = stage.parent.base.digest
CASES = dict(paid=(1156, (3440, 3620, 4160, 4340, 4520, 4700, 4880, 5060)),
             refused=(1149, (3440, 3620, 4160, 4340, 4520, 4700)))
WORDING = {
    1149: 'The ruler’s formal question and the exact minimum fee set up his refusal. The line gives the amount without implying that the captain can pay it.',
    1156: 'The ruler briefly considers the request and agrees to a contract. The existing hesitation and the exact minimum fee lead naturally into the offer question.',
    1157: 'The follow-up distinguishes the minimum fee from the offer that determines the market share. The question asks for a decision.',
    1162: 'The refusal states the reason plainly and tells the captain to return with enough money. It leaves the option open.',
}


def amount(arm, raw):
    _, get = get_machine(arm, raw)
    root, index = get(0xCB160), get(0x397D8)
    assert get(0xB65E4) == 22
    return get(0x3CCC8, root + 4 + index * 76)


def actual(arm, painter, kanji, table):
    contact = Image.new('RGB', (1032, 2 * 404), '#263238')
    draw = ImageDraw.Draw(contact)
    pointers = [unpack_from('<I', arm, off)[0] - BASE for off in (0x5444C, 0x54450)]
    observations = {}
    for row, (case, (message, controls)) in enumerate(CASES.items()):
        reports = [CAPTURE / f'{case}_{side}' / 'capture_report.json' for side in ('current', 'revised')]
        inputs, screens, records, source_rams = [], [], [], []
        expected_money = [8371, 5529] if case == 'paid' else [1, 1]
        for index, path in enumerate(reports):
            report = batch.load(path)
            rom = stage.ROM if index else stage.parent.ROM
            assert report['ROM_sha256'] == digest(rom) and not report['callback_errors']
            assert report['cold_boot'] and not report['savestate_loaded']
            fixtures = report.get('synthetic_condition_fixtures', [])
            assert len(fixtures) == int(case == 'refused')
            assert all(row['only_original_company_money_field_changed'] for row in fixtures)
            donor = report['battery_save_preloaded']
            assert donor['copied_byte_exact_before_cold_boot'] and digest(donor['source']) == donor['source_sha256']
            snap, raw = ram_at(report, 3980)
            source_rams.append(snap)
            amounts = [amount(arm, ram_at(report, frame)[1]) for frame in (3980, controls[-1])]
            assert amounts == expected_money
            fee = b'2842' if index else '２８４２'.encode('cp932')
            paragraph, wrapped = [raw[ptr:ptr + 256].split(b'\0', 1)[0] for ptr in pointers]
            assert paragraph == table[message].text % fee
            assert b' '.join(wrapped.split()) == paragraph.strip()
            body = wrapped.replace(b'\r', b'')
            plane, glyphs = render_portrait(painter, arm, kanji, body)
            assert glyphs[0]['code'] == ord('Y') and glyphs[-1]['code'] == ord('.')
            shot, screen = one_frame(report, 3980)
            native_hold(screen, plane)
            screens.append(screen)
            inputs.append(batch.load(path.with_name('navigation_command_journal.json'))['commands_received'])
            assert all(command['validation_passed'] for command in inputs[-1])
            records.append(dict(ROM_sha256=report['ROM_sha256'], paragraph_hex=paragraph.hex(),
                wrapped_hex=wrapped.hex(), held_frame=shot, amounts=amounts,
                control_frames=[one_frame(report, n)[0] for n in controls], report=str(path), report_sha256=digest(path)))
            x, y = index * 516, row * 404
            draw.text((x + 5, y + 4), f'{case.title()} | {("Previous", "Regular digits")[index]}', fill='white')
            contact.paste(screen.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 2, y + 19))
        assert inputs[0] == inputs[1]
        assert [row['framebuffer_sha256'] for row in records[0]['control_frames']] == [
            row['framebuffer_sha256'] for row in records[1]['control_frames']]
        diff = ImageChops.difference(*screens).getbbox()
        assert diff is not None and diff[1] >= 328 and diff[3] <= 344
        assert normalize(bytes.fromhex(records[0]['wrapped_hex'])) == bytes.fromhex(records[1]['wrapped_hex'])
        observations[case] = dict(message_ID=message, transaction_funds=expected_money, complete_before_after_masks=True,
            difference_bbox=diff, records=records, read_only_original_and_revised_RAM=source_rams)
    contact.save(SHEET)
    return observations


def native(arm, old_arm, source_arm, painter, kanji, table):
    old_report = batch.load(CAPTURE / 'paid_current/capture_report.json')
    snapshot, raw = ram_at(old_report, 3980)
    ram = bytearray(raw)
    for address, _ in stage.CALLS.values():
        offset = address - BASE
        assert ram[offset:offset + 4] == old_arm[offset:offset + 4]
        ram[offset:offset + 4] = arm[offset:offset + 4]
    old_cpu, _ = get_machine(old_arm, raw)
    cpu, get = get_machine(arm, bytes(ram))
    assert arm[0x5E004:0x5E03C] == source_arm[0x5E004:0x5E03C]
    towns = get(0xCB178) + 4
    fees = []
    for town in range(114):
        cpu.reg_write(UC_ARM_REG_R7, towns + town * 108)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.emu_start(BASE + 0x5E004, BASE + 0x5E03C, count=100000)
        assert cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x5E03C
        fees.append(cpu.reg_read(UC_ARM_REG_R6))
    assert min(fees) == 75 and fees[22] == 2842
    amounts = sorted(set(fees))
    selected = {min(fees), max(fees), fees[22]}
    pages, layouts = [], []

    def call_full(cpu, offset, arguments):
        return call(cpu, offset, arguments, instruction_limit=2_000_000)

    layout = FunctionType(native_layout.__code__, native_layout.__globals__ | {'call': call_full}, argdefs=native_layout.__defaults__)
    for message, (address, _) in stage.CALLS.items():
        for fee in amounts:
            values = []
            for machine in (old_cpu, cpu):
                machine.reg_write(UC_ARM_REG_R6, fee)
                machine.reg_write(UC_ARM_REG_SP, STACK)
                machine.emu_start(address - 4, address + 8, count=10000)
                assert machine.reg_read(UC_ARM_REG_PC) == address + 8 and machine.reg_read(UC_ARM_REG_SP) == STACK
                values.append(read_cstring(machine, machine.reg_read(UC_ARM_REG_R2)))
            assert normalize(values[0]) == values[1] == str(fee).encode('ascii')
            formatted, lines = layout(cpu, table[message].text, message, (str(fee),))
            assert len(lines) == 3 and lines[-1] == f'is {fee} gold coins.'
            assert [glyph_codes(formatted)[i] for i in (0, -1)] == [ord('Y'), ord('.')]
            if fee in selected:
                pixels, _ = render_portrait(painter, arm, kanji, formatted.replace(b'\r', b''))
                pages.append((f'{message} / {fee} gold', pixels))
            layouts.append(dict(message_ID=message, amount=fee, display_hex=formatted.hex(), page_count=1))
    return dict(source_snapshot=snapshot, original_town_fees=fees, original_format_handoffs=layouts,
                representatives=portrait_sheets(ROOT, pages), catalog_counts_do_not_assert_eligibility=True)


def main():
    assert not PROOF.exists() and not SHEET.exists()
    clean, old, rom = map(batch.NdsImage.open, (batch.CLEAN, stage.parent.ROM, stage.ROM))
    source_arm, old_arm, arm = [image.read_file(batch.ARM) for image in (clean, old, rom)]
    common, kanji = [rom.read_file(path) for path in (batch.COMMON, '/GRP/KANJI.FNT')]
    assert stage.patch(old_arm, source_arm)[0] == arm
    painter, _, _ = font_tools(rom)
    table = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    source = batch.common_message_entries(clean.read_file(batch.COMMON), source_arm)
    rows = [dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=batch.COMMON, speaker='King',
                 clean_Japanese=source[n].text.decode('cp932'), english=table[n].text.decode('ascii').strip(),
                 source_reference=batch.reference(source[n]), current_reference=batch.reference(table[n]),
                 source_hex=source[n].text.hex(), current_hex=table[n].text.hex(), localization_note=reason,
                 decision='retention', review=dict.fromkeys(batch.GATES, True))
            for n, reason in WORDING.items()]
    offline = native(arm, old_arm, source_arm, painter, kanji, table)
    observed = actual(arm, painter, kanji, table)
    batch.write(PROOF, dict(candidate_sha256=digest(stage.ROM), predecessor_sha256=digest(stage.parent.ROM),
        records=rows, offline=offline, observed_gameplay=observed, gameplay_sheet=dict(path=str(SHEET), sha256=digest(SHEET)),
        initial_funds_fixture_only_in_refusal=True, hardware=False))
    print(f'{len(offline["original_format_handoffs"])} native quote layouts and two paired gameplay branches passed.')


if __name__ == '__main__':
    main()
