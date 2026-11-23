"""Bind the retail disband flow and exercise its original signed wallet update."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_fleet_debt_disband_20261115 as playback
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.preflight_setup_save_equipment_v1 import check_modal, font_tools, WIDTH, HEIGHT
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine


base, current = playback.base, playback.current
ARM, COMMON, CLEAN = current.stage.ARM, current.stage.COMMON, current.stage.CLEAN
ROOT = playback.ROOT
PROOF = Path('translations/editorial_checkpoints/SharedText_20261110_v1/fleet_debt_disband_20261115_v2.json')
SHEET = ROOT / 'controlled_debt_warning_v2.png'
FORMATION = Path('work/analysis/regional_fleet_v615/formed_original_regional_fleet.json')
FLEET_SAVE = FORMATION.with_name('formed_fixture_manifest.json')
BODY = (16, 294, 244, 351)
BEGIN, COMPLETE = 0x0205A2CC, 0x0205A368
CONFIRM, NOTICE = 0x0205466C, 0x020546B8
WALLET = 0x0203CC80
SCENARIOS = ((37, -500, False), (37, -500, True), (0, -500, True), (500, -500, True),
             (501, -500, True), (37, 0, True), (37, 500, True), (99_999_990, 500, True))
WORDING = "This fleet is operating at a loss. You can't afford to pay its debt."


def field(raw, addr):
    return unpack_from('<I', raw, addr - BASE)[0]


def setup(raw, arm, fleet_id):
    cpu, get = get_machine(arm, raw)
    fleets = get(0xCB1A8)
    companies = get(0xCB160)
    company_id = get(0x397D8)
    wallet_object = companies + 4 + company_id * 0x4c
    fleet = fleets + 4 + fleet_id * 0x84
    wallet = wallet_object + 0xc
    finances = fleets + 0x20c4 + (fleet_id - 57) * 0x18
    assert get(0x3CCC8, wallet_object) == field(raw, wallet)
    assert 57 <= fleet_id <= 62
    return cpu, dict(fleet=fleet, fleet_id=fleet_id, finance=finances, wallet=wallet, company=company_id)


def controlled_cases(arm, snapshot, fleet_id):
    raw = Path(snapshot['path']).read_bytes()
    results = []
    maximum, = unpack_from('<I', arm, 0x3CCC4)
    assert maximum == 99_999_999
    k, = unpack_from('<I', arm, 0x5A37C)
    assert k == 100_000
    for starting, delta, accept in SCENARIOS:
        cpu, owner = setup(raw, arm, fleet_id)
        fleet, finances, wallet = (owner[key] for key in ('fleet', 'finance', 'wallet'))
        before_fields = bytes(cpu.mem_read(finances + 0x0c, 12))
        # Supply bounded ledger words to the actual arithmetic segment. Invoke
        # the original wallet getter, dock transfer and wallet setter below.
        values = (k - delta, 0, 0)
        cpu.mem_write(finances + 0x0c, pack('<3I', *values))
        cpu.mem_write(wallet, pack('<I', starting))
        cpu.mem_write(STACK, pack('<6I', 4, 5, 6, 7, 8, STOP))
        for register, value in ((UC_ARM_REG_R4, fleet), (UC_ARM_REG_R5, fleet_id - 57), (UC_ARM_REG_R6, fleet_id),
                                (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
            cpu.reg_write(register, value)
        dialogs, updates = [], []

        def dialog(u, pc, size, data):
            dialogs.append((pc, u.reg_read(UC_ARM_REG_R0)))
            if pc == CONFIRM:
                u.reg_write(UC_ARM_REG_R0, int(accept))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        def change(u, pc, size, data):
            updates.append((u.reg_read(UC_ARM_REG_R0) + 0xc, u.reg_read(UC_ARM_REG_R1)))

        for entry in (CONFIRM, NOTICE):
            cpu.hook_add(UC_HOOK_CODE, dialog, begin=entry, end=entry)
        cpu.hook_add(UC_HOOK_CODE, change, begin=WALLET, end=WALLET)
        before_fleet = bytes(cpu.mem_read(fleet, 0x84))
        cpu.emu_start(BEGIN, COMPLETE if accept else STOP, count=200000)
        assert cpu.reg_read(UC_ARM_REG_PC) == (COMPLETE if accept else STOP)
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK + (0 if accept else 24)
        assert dialogs == ([(CONFIRM, 285), (NOTICE, 286)] if accept else [(CONFIRM, 285)])
        assert updates == ([(wallet, delta & 0xffffffff)] if accept else [])
        remaining = unpack_from('<I', cpu.mem_read(wallet, 4))[0]
        expected = max(0, min(maximum, starting + delta)) if accept else starting
        assert remaining == expected and bytes(cpu.mem_read(finances + 0x0c, 12)) == pack('<3I', *values)
        fleet_after = bytes(cpu.mem_read(fleet, 0x84))
        if not accept:
            assert fleet_after == before_fleet
        results.append(dict(starting_gold=starting, supplied_signed_delta=delta, accepted=accept,
            original_ledger_hex=before_fields.hex(), supplied_ledger_values=list(values), selected_messages=dialogs,
            wallet_updates=updates, final_gold=remaining, fleet_state_changed=(fleet_after != before_fleet)))
    return results


def main():
    assert not PROOF.exists() and not SHEET.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    clean, image = map(base.NdsImage.open, (CLEAN, current.ROM))
    source, arm = (img.read_file(ARM) for img in (clean, image))
    assert current.stage.digest(arm) == release['target_ARM9_sha256']
    spans = ((0x5A27C, 0x5A388), (0x5A4B4, 0x5A528), (0x3CC80, 0x3CCD0), (0x3FA9C, 0x3FAA0))
    assert all(source[lo:hi] == arm[lo:hi] for lo, hi in spans)
    assert unpack_from('<2I', arm, 0x5A380) == (285, 286)
    folder = ROOT / 'fleet'
    terminal, capture, trace = map(base.load, (folder / 'terminal.json', folder / 'capture/capture_report.json', folder / 'requests.json'))
    assert terminal['ROM_sha256'] == capture['ROM_sha256'] == release['candidate_sha256'] and capture['cold_boot']
    assert not (capture['callback_errors'] or capture['savestate_loaded'])
    assert not any(v for k,v in capture.items() if k.startswith('synthetic_'))
    assert all(base.digest(p) == sha for p, sha in terminal['evidence'].items())
    donor = capture['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == base.load(FLEET_SAVE)['fixture_sha256']
    assert base.digest(donor['source']) == donor['source_sha256']
    calls = [row for row in trace['source_requests'] if row['PC'] == 0x0205528C]
    keys = [r['message_ID'] for r in calls if r['message_ID'] in {280, 281, 284, 285, 286}]
    assert keys == [280, 281, 285, 281, 285, 286], keys
    assert all(r['message_ID'] != 284 for r in calls)
    snapshots = {r['frame']: r for r in capture['read_only_capture_RAM_snapshots']}
    for row in snapshots.values():
        assert base.digest(row['path']) == row['sha256'] and row['read_only_export']
    fleet_id = base.load(FORMATION)['regional_fleet_index']
    assert fleet_id == 57
    actual = []
    before = None
    for frame in (10840, 11080, 11560, 11680, 11800):
        raw = Path(snapshots[frame]['path']).read_bytes()
        _, owner = setup(raw, arm, fleet_id)
        funds = field(raw, owner['wallet'])
        assert before is None or owner == before
        before = owner
        signed_parts = unpack_from('<3I', raw, owner['finance'] + 0x0c - BASE)
        actual.append(dict(frame=frame, funds=funds, ledger_parts=list(signed_parts), owner=owner))
    amount0, after_no, amount1, before_yes, after_yes = actual
    assert amount0['funds'] == after_no['funds'] == amount1['funds'] == before_yes['funds']
    a, b, c = before_yes['ledger_parts']
    delta = (100_000 + b - a - c + 0x80000000) % 0x100000000 - 0x80000000
    assert after_yes['funds'] == max(0, min(99_999_999, before_yes['funds'] + delta))
    offline = controlled_cases(arm, snapshots[11560], fleet_id)

    panels = []
    by_frame = shots(capture)
    font = GameAsciiFont.from_arm9(arm)
    for ident, n, text in ((280, 9400, 'Choose a fleet to reorganize.'), (281, 10360, 'Choose a fleet to disband.'),
                           (285, 10840, 'Disband this fleet?'), (286, 11680, "We'll put all the ships in the dock.")):
        for x in (16, 22):
            try:
                pixels = font_mask(captured(by_frame[n]), font, text, x, 297, BODY, (0, 8, 0))
            except AssertionError:
                continue
            panels.append(dict(message_ID=ident, frame=n, text=text, complete_dark_ink=pixels, screenshot=by_frame[n]))
            break
        else:
            raise AssertionError((ident, n, text))

    original = common_message_entries(clean.read_file(COMMON), source)
    stored = owned_entries(image.read_file(COMMON), arm, current.stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    runtime = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    gloss = original[284].text.decode('cp932')
    assert '赤字' in gloss and '借金' in gloss and 'Trade-good description.' in stored[284].text.decode('ascii')
    raster, _, _ = font_tools(image)
    draft, pixels = check_modal(runtime, dict(id='COMMON_MESSAGE_284', message_ID=284, english=WORDING,
        current_hex=stored[284].text.hex(), native_callers=[dict(target=NOTICE)]), (), raster, font)
    assert pixels is not None and draft['complete_glyphs_bounds_and_words']
    assert draft['native_lines'] == ['This fleet is operating at a loss.', "You can't afford to pay its debt."]
    encoded = draft['storage_markup'].replace('{LB}', '\n').encode('ascii')
    assert len(encoded) + 1 <= stored[284].copy_end - stored[284].block_offset
    sheet = Image.new('RGB', (480, 124), '#263238')
    ImageDraw.Draw(sheet).text((12, 5), 'COMMON 284  Controlled notice preview', fill='white')
    paper = Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if v else 255 for v in pixels))
    sheet.paste(paper.resize((456, 96), Image.Resampling.NEAREST), (12, 22))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        exact_clean_native_spans=spans, observed_requests=calls, observed_complete_panels=panels, actual_normal_gold=actual,
        actual_wallet_adjustment=delta, saved_fleet_prerequisites_inherited=True,
        arithmetic_cases_with_stubbed_modal_response_only=offline,
        debt_warning=dict(message_ID=284, Japanese=gloss, current=stored[284].text.decode('ascii'), staged_draft=WORDING,
            source_reference=reference(original[284]), current_reference=reference(stored[284]), layout_only=draft,
            other_callers_open=True), sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        release_changed=False, new_editorial_credit=0, evidence=terminal['evidence']))
    print('Four actual panels, eight isolated wallet branches, and the prospective debt warning passed.')


if __name__ == '__main__':
    main()
