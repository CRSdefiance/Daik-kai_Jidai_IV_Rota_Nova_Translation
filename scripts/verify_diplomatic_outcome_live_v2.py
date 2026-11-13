"""Bind original incoming-truce gameplay and candidate-owned startup to the batch."""

from pathlib import Path
import struct
from types import FunctionType

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_diplomatic_outcome_wrap_v1 import PROOF as ORIGINAL_PREVIEWS
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.refine_diplomatic_outcomes_layout_v2 import EVIDENCE, ROM, ROOT
from scripts.run_diplomatic_outcome_live_v2 import ACTION, ARM, DONOR, DONOR_SHA, SENDER, set_condition
from scripts.run_diplomatic_outcome_startup_v2 import STARTUP
from scripts.verify_personal_gameplay_v841 import get_machine


LIVE = ROOT / 'truce_decline'
LIVE_VERIFICATION = ROOT / 'live_verification.json'
STARTUP_VERIFICATION = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'


def live_proof(image, arm, sha):
    terminal = load(LIVE / 'terminal.json')
    report_path = Path(terminal['report'])
    assert terminal['candidate_sha256'] == sha
    assert digest(report_path) == terminal['report_sha256']
    assert digest(terminal['final_navigation']) == terminal['final_navigation_sha256']
    report, final_raw = checked_report(report_path, sha, 9300)
    donor = report['battery_save_preloaded']
    assert donor['source_sha256'] == digest(DONOR) == DONOR_SHA
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source'] != donor['destination']
    fixtures = report['synthetic_condition_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 3200
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}

    def read_ram(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    _, fixture = set_condition(arm, read_ram(3200), ACTION)
    assert fixtures[0] == (fixture | {'frame': 3200})
    commands = load(LIVE / 'navigation_command_journal.json')['commands_received']
    assert all(row['validation_passed'] for row in commands)
    assert [(r['frame'], r['command'].get('buttons')) for r in commands[-4:]] == [
        (8100, ['B']), (8500, ['B']), (8900, ['A']), (9300, None)]

    raster, _, _ = font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    offsets = [address - BASE for address in struct.unpack_from('<2I', arm, 0x54890)]
    crop = (16, 296, 244, 344)
    expected = (
        (349, 8100, b'An official letter from Speyer Co.', b'has arrived.'),
        (356, 8500, b'Will you accept the truce offered by', b'Speyer Co.?'),
        (352, 8900, b'Offer refused.', None),
    )
    verified = []
    for n, frame, first, second in expected:
        raw = read_ram(frame)
        expanded, drawn = [raw[at:at + 256].split(b'\0')[0] for at in offsets]
        assert expanded == (first + b' ' + second if second else first)
        assert drawn == (first + b'\n  ' + second if second else first)
        plane, glyphs = render(raster, arm, kanji, drawn)
        with Image.open(shots[frame]['path']) as screenshot:
            found = screenshot.convert('RGB').crop(crop)
        assert bytes(color == (0, 8, 0) for color in found.get_flattened_data()) == bytes(p == 1 for p in plane)
        assert raw[fixture['letter_object'] + 4 - BASE] == 3
        verified.append(dict(message_ID=n, frame=frame, crop=crop, frame_capture=shots[frame],
            expanded_hex=expanded.hex(), display_hex=drawn.hex(), glyphs=len(glyphs),
            exact_complete_foreground_and_blank_margin_match=True))

    assert read_ram(9300) == final_raw
    cpu, get = get_machine(arm, final_raw)
    assert get(0x91464, fixture['letter_object']) == 0
    root = get(0xCB160)
    assert get(0x3CB30, root + 4 + 76 * SENDER, fixture['recipient']) == 2
    assert shots[9300]['framebuffer_sha256'] != shots[8900]['framebuffer_sha256']
    return dict(candidate_sha256=sha, actual_emulator=True, observed=verified,
        original_yes_no_choices_visible_at_frame=8500, no_refused_truce_and_preserved_war=True,
        original_dispatcher_consumed_the_letter=True, inn_menu_return=shots[9300],
        disclosed_fixture=fixtures[0], natural_incoming_letter_generation=False, hardware=False,
        evidence={str(path): digest(path) for path in (
            report_path, LIVE / 'terminal.json', LIVE / 'navigation_command_journal.json')})


def main():
    assert not any(path.exists() for path in (LIVE_VERIFICATION, STARTUP_VERIFICATION, CHECKPOINT))
    storage = load(EVIDENCE)
    sha = storage['research_ROM_sha256']
    assert digest(ROM) == sha
    assert len(storage['cases']) == 176 and len(storage['records']) == 34
    old_sheets = load(ORIGINAL_PREVIEWS)['contact_sheets']
    new_sheets = storage['contact_sheets']
    assert sum(s['pages'] for s in new_sheets) == 31
    assert sum(case['reused_viewed_pixels'] for case in storage['cases']) == 145
    for sheet in (*old_sheets, *new_sheets):
        assert digest(sheet['path']) == sheet['sha256']
    image = NdsImage.open(ROM)
    arm = image.read_file(ARM)
    live = live_proof(image, arm, sha)
    startup = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert digest(startup) == terminal['report_sha256'] and terminal['candidate_sha256'] == sha
    verify_startup = FunctionType(startup_proof.__code__, {**startup_proof.__globals__, 'STARTUP': startup})
    boot = verify_startup(arm, sha)
    report, raw = checked_report(startup, sha, 31000)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    boot.update(candidate_sha256=sha, cold_boot=True, savestate=False, actual_captain_getter=3,
        read_only_snapshot=report['read_only_RAM_snapshot'], complete_deployed_payload_exact=True)
    save(LIVE_VERIFICATION, live)
    save(STARTUP_VERIFICATION, boot)
    save(CHECKPOINT, dict(
        candidate_sha256=sha, approved_for_registered_successor=True, final_wrap_pages=176,
        reused_exact_viewed_pages=145, new_directly_viewed_pages=31,
        freshly_viewed_sheets=new_sheets, previous_viewed_sheets=old_sheets,
        live_messages=[349, 356, 352], scope='One isolated incoming letter and original No transition',
        exact_stored_record_references=storage['records'], new_credit=0,
        evidence={str(path): digest(path) for path in (EVIDENCE, LIVE_VERIFICATION, STARTUP_VERIFICATION)}))
    print('Original letter notice, Yes/No prompt and refusal match all live glyphs. Maria startup and 24 name getters pass.')


if __name__ == '__main__':
    main()
