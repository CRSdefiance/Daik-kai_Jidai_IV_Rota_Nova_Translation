"""Bind the crew notices' stored native pages and focused emulator transitions."""

import gzip
import struct
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import ARM, HEIGHT, OUT, WIDTH, font_tools, render
from scripts.probe_button_prompt_native import BASE
from scripts.review_ship_loss_context_v1 import OUTPUT
from scripts.run_shared_crew_notices_live_v1 import LIVE, NAME, PREFLIGHT, fixture
from scripts.run_shared_crew_startup_v1 import STARTUP
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shared_crew_selector_v1 import RESULT as SCOPE


ROOT = OUTPUT.parent / 'native_and_live_v1'


def live_proof(rom, arm, sha):
    terminal = load(LIVE / 'terminal.json')
    report_path = Path(terminal['report'])
    journal = LIVE / 'navigation.jsonl'
    assert terminal['exit_code'] == 0 and terminal['donor_unchanged']
    assert digest(report_path) == terminal['report_sha256'] and digest(journal) == terminal['journal_sha256']
    report, _ = checked_report(report_path, sha, 8500)
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and digest(donor['source']) == donor['source_sha256']
    fixture_key = 'synthetic_battle_recovery_proximity_fixtures'
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != fixture_key)
    observed_fixture, = report[fixture_key]
    assert observed_fixture['frame'] == 7600 and observed_fixture['both_fixture_fields_only']
    snapshots = {r['frame']: r for r in report['read_only_pause_RAM_snapshots']}
    frames = {r['frame']: r for r in report['frames_captured'] if r['path'].endswith('navigation.png')}

    def raw(frame):
        row = snapshots[frame]
        path = Path(row['path'])
        assert digest(path) == row['sha256'] and row['read_only_export']
        return path.read_bytes()

    _, expected = fixture(arm, raw(7600), observed_fixture['action'])
    assert observed_fixture == {**expected, 'frame': 7600}
    assert frames[8000]['framebuffer_sha256'] == frames[8500]['framebuffer_sha256']
    assert frames[8100]['framebuffer_sha256'] != frames[8300]['framebuffer_sha256']
    commands = load(LIVE / 'capture/navigation_command_journal.json')['commands_received']
    assert all(row['validation_passed'] for row in commands)
    assert [(row['frame'], row['command'].get('buttons')) for row in commands[-5:]] == [
        (7800, ['A']), (8000, ['DOWN']), (8100, ['B']), (8300, ['B']), (8500, None)]

    raster, _, _ = font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    verified = []
    cases = (
        (339, 7800, HEIGHT, (0x54890, 0x54894), NAME + b' has no sailors!', NAME + b' has no sailors!'),
        (2680, 8300, 64, (0x5444C, 0x54450), b"So, we're abandoning " + NAME + b', right?',
         b" So, we're abandoning\n  " + NAME + b', right?'),
    )
    for number, frame, height, offsets, expected_plain, expected_wrapped in cases:
        state = raw(frame)
        plain, wrapped = [state[(address := struct.unpack_from('<I', arm, off)[0] - BASE):address + 256].split(b'\0')[0]
            for off in offsets]
        assert plain == expected_plain and wrapped == expected_wrapped, (number, plain, wrapped)
        renderer = FunctionType(render.__code__, {**render.__globals__, 'HEIGHT': height})
        plane, glyphs = renderer(raster, arm, kanji, wrapped)
        crop = (16, 296, 16 + WIDTH, 296 + height)
        with Image.open(frames[frame]['path']) as screenshot:
            found = screenshot.convert('RGB').crop(crop)
        assert bytes(p == (0, 8, 0) for p in found.get_flattened_data()) == bytes(p == 1 for p in plane)
        verified.append(dict(message_ID=number, frame=frame, crop=crop, complete_ordered_glyph_count=len(glyphs),
            foreground_pixels=plane.count(1), complete_foreground_and_blank_margins_exact=True,
            resident_expanded_hex=plain.hex(), resident_rendered_hex=wrapped.hex(), frame_capture=frames[frame]))

    cpu, get = get_machine(arm, raw(8500))
    ship = get(0x36C70, observed_fixture['fleet'] + 12 + 8 * observed_fixture['ship_slot'])
    field = get(observed_fixture['native_name_getter'] - BASE, ship)
    assert field == observed_fixture['ship_name_field'] and get(0x55444, ship) == 0
    assert bytes(cpu.mem_read(field, 19)) == NAME + b'\0'
    native = report['read_only_native_state']
    assert native['read_only_export'] and not native['state_loaded'] and native['main_RAM_unchanged_by_export']
    assert digest(native['path']) == native['sha256']
    itcm = native['regions']['ITCM']
    assert digest(itcm['path']) == itcm['sha256']
    image = Path(itcm['path']).read_bytes()
    patch, tail = MainCodeFile(arm, BASE).sections[-2:]
    patch_at, tail_at = (s.ramAddress & 0x7FFF for s in (patch, tail))
    loaded = image[patch_at:patch_at + len(patch.data)]
    cache = 0x2D8
    assert loaded[:cache] == patch.data[:cache] and loaded[cache + 4:] == patch.data[cache + 4:]
    assert image[tail_at:tail_at + len(tail.data)] == tail.data
    return dict(candidate_sha256=sha, actual_emulator=True, earned_crew_loss=False,
        original_ship_preserved_after_No=True, genuine_save_isolated=True,
        disclosed_fixture=observed_fixture, captured_notices=verified, both_selectors_exact_in_live_ITCM=True,
        menu_after_No_pixel_identical=True, hardware=False,
        evidence={str(p): digest(p) for p in (report_path, journal, LIVE / 'terminal.json')})


def main():
    assert not ROOT.exists()
    preflight, scope = load(PREFLIGHT), load(SCOPE)
    sha = preflight['research_ROM_sha256']
    assert digest(preflight['research_ROM']) == sha == scope['research_ROM_sha256']
    assert len(preflight['cases']) == 110 and len(preflight['source_choices']) == 621
    assert preflight['storage']['all_unselected_native_copy_spans_exact'] and preflight['complete_serialized_parent_inverse']
    assert scope['modal_literal_IDs'] == [338, 339] and scope['modal_unchanged_IDs'] == 3666
    assert scope['exact_portrait_controls'] == 603
    image = NdsImage.open(preflight['research_ROM'])
    arm = image.read_file(ARM)
    live = live_proof(image, arm, sha)
    startup_report = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert terminal['exit_code'] == 0 and terminal['report_sha256'] == digest(startup_report)
    verify_startup = FunctionType(startup_proof.__code__, {**startup_proof.__globals__, 'STARTUP': startup_report})
    boot = verify_startup(arm, sha)
    report, raw = checked_report(startup_report, sha, 31000)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    boot.update(candidate_sha256=sha, cold_boot=True, savestate=False, actual_captain_getter=3,
        read_only_snapshot=report['read_only_RAM_snapshot'], complete_deployed_payload_exact=True)
    reviewed = preflight['sheets']
    assert sum(sheet['pages'] for sheet in reviewed) == 66
    for sheet in reviewed:
        assert digest(sheet['path']) == sheet['sha256']
    ROOT.mkdir()
    packed = ROOT / 'native_preflight.json.gz'
    packed.write_bytes(gzip.compress(PREFLIGHT.read_bytes(), mtime=0))
    assert gzip.decompress(packed.read_bytes()) == PREFLIGHT.read_bytes()
    save(ROOT / 'live_verification.json', live)
    save(ROOT / 'own_startup_verification.json', boot)
    save(ROOT / 'selector_scope.json', scope)
    save(ROOT / 'checkpoint.json', dict(candidate_sha256=sha, researched_candidate=preflight['research_ROM'],
        verified_native_cases=110, original_voice_selections=621, native_scope_checks=scope,
        exact_original_record_references=preflight['exact_record_references'],
        visually_approved_sheets=[{**sheet, 'viewed': True} for sheet in reviewed],
        live_messages=[339, 2680], both_native_modal_and_portrait_consumers_observed=True,
        stored_and_rendered_names_literal=True, original_ship_preserved_after_No=True,
        approved_for_registered_successor=True, registered_integration_pending=True, new_credit=0,
        evidence={str(p): digest(p) for p in (PREFLIGHT, SCOPE, OUTPUT, packed,
            ROOT / 'live_verification.json', ROOT / 'own_startup_verification.json', Path(__file__))}))
    print('All 22 crew records pass stored, visual and representative gameplay review on the exact research ROM.')


if __name__ == '__main__':
    main()
