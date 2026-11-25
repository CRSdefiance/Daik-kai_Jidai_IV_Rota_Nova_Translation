"""Verify the original loss report, shortfall calculation and return to sailing."""

from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import replay_fleet_reports_shortfall_v1 as shortfall
from scripts import verify_fleet_reports_v1 as checked
from scripts.native_call_abi_v764 import call
from scripts.native_inventory_fixture_v481 import machine
from scripts.verify_captain_biographies_v1 import captured


replay, stage, base = checked.replay, checked.stage, checked.base
LIVE = stage.ROOT / 'fleet_reports_gameplay_verification.json'
CHECKPOINT = stage.ROOT / 'approved_checkpoint.json'
PAPER = (16, 296, 244, 360)


def checked_replay(root, sha, final_frame):
    terminal_path = root / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(commands) == terminal['commands_sha256']
    report = base.load(report_path)
    assert terminal['candidate_sha256'] == report['ROM_sha256'] == sha
    assert report['frames'] == final_frame and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and terminal['unchanged_original_save']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == replay.DONOR_SHA
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = base.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    return report, frames, snapshots, (terminal_path, report_path, commands, journal_path)


def snapshot(arm, snapshots, frame):
    row = snapshots[frame]
    assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
    raw = Path(row['path']).read_bytes()
    assert len(raw) == 0x400000
    cpu = machine(arm)
    base_address = stage.first.BASE
    cpu.mem_write(base_address, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    clock = unpack_from('<I', raw, get(0xCB1B4) + 8 - base_address)[0]
    fleet = get(0xCB1A8) + 4 + 57 * 132
    finance = get(0x367FC, fleet) - base_address
    companies = get(0xCB160)
    money = get(0x3CCC8, companies + 4 + 76 * get(0x397D8, companies))
    return raw, dict(clock=clock, company_funds=money, finance=unpack_from('<6I', raw, finance), capture=row)


def main():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (stage.PROOF, checked.VISUAL, checked.BOOT))
    sha = base.digest(stage.ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.first.ARM)
    raster, _, _ = stage.first.portrait.font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    addresses = [unpack_from('<I', arm, offset)[0] - stage.first.BASE for offset in (0x5444C, 0x54450)]
    stored = {row['message_ID']: row for row in proof['records']}

    def display(raw):
        return tuple(raw[at:at + 256].split(b'\0', 1)[0] for at in addresses)

    def screen_match(raw, frame, expected_input, expected_english):
        formatter_input, visible = display(raw)
        assert formatter_input == expected_input
        assert b' '.join(visible.split()) == expected_english
        pixels, glyphs = stage.first.portrait.render_portrait(raster, arm, kanji, visible)
        seen = bytes(pixel == (0, 8, 0) for pixel in captured(frame).crop(PAPER).get_flattened_data())
        assert seen == bytes(bool(pixel) for pixel in pixels)
        return dict(formatter_input_hex=formatter_input.hex(), visible_hex=visible.hex(),
            visible_lines=[line.strip() for line in visible.decode('ascii').split('\n')], complete_glyphs=len(glyphs),
            ink_sha256=sha256(seen).hexdigest(), original_emulator_capture=frame)

    observations, evidence = [], []
    for root, end, supplied in ((replay.ROOT, 14000, False), (shortfall.ROOT, 14400, True)):
        report, frames, snapshots, paths = checked_replay(root, sha, end)
        evidence.extend(paths)
        raw_prompt, prompt = snapshot(arm, snapshots, 13200)
        assert b'Would you like to hear them?' in display(raw_prompt)[1]
        assert prompt['company_funds'] == 897400 and prompt['finance'][3:] == (691, 0, 0)
        fixtures = {key: value for key, value in report.items() if key.startswith('synthetic_') and value}
        if supplied:
            _, applied = shortfall.fund_company(arm, raw_prompt, 100)
            assert fixtures == {'synthetic_finance_fixtures': [applied | {'frame': 13200}]}
        else:
            assert not fixtures
        raw_loss, loss = snapshot(arm, snapshots, 13600)
        assert loss['finance'] == prompt['finance']
        assert loss['company_funds'] == (100 if supplied else 897400)
        record = bytes.fromhex(stored[2565]['staged_hex'])
        shown = screen_match(raw_loss, frames[13600], record % ('６９１'.encode('cp932'),), record % (b'691',))
        observation = dict(ordinary_month_rollover=True, supplied_funds=supplied, prompt=prompt,
            loss=dict(message_ID=2565, loss=691, state=loss, **shown))
        if supplied:
            raw_carry, carry = snapshot(arm, snapshots, 14000)
            assert carry['company_funds'] == 0 and carry['finance'][:4] == (691, 0, 0, 591)
            exact = bytes.fromhex(stored[2575]['staged_hex'])
            rendered = screen_match(raw_carry, frames[14000], exact, b' '.join(exact.split()))
            observation.update(fixture=applied, carryover=dict(message_ID=2575, unpaid_amount=591, state=carry, **rendered))
        _, returned = snapshot(arm, snapshots, end)
        assert returned['clock'] > prompt['clock']
        assert returned['company_funds'] == (0 if supplied else 897400 - 691)
        assert frames[end]['framebuffer_sha256'] != frames[14000 if supplied else 13600]['framebuffer_sha256']
        observations.append(observation | {'returned': returned, 'return_capture': frames[end]})
    paths = (stage.PROOF, checked.VISUAL, checked.BOOT, checked.QA, Path(replay.__file__),
             Path(shortfall.__file__), Path(__file__), *evidence)
    bindings = {str(path): base.digest(path) for path in paths}
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=[2565, 2575], observations=observations,
        actual_emulator=True, hardware=False, ordinary_loss_and_deduction=True,
        focused_shortfall_and_carried_balance=True, original_A_advance_and_return_to_sailing=True,
        fleet_encounter_and_outcome_variants_offline=True, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=[2565, 2575], stored_cases=47, viewed_pages=89, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print('Verified the ordinary 691-gold loss, the focused 591-gold carryover and both original returns.')


if __name__ == '__main__':
    main()
