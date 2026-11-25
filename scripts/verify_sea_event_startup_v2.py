"""Seal the sea-event candidate's exact startup and prior review evidence."""

from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_diplomatic_outcome_startup_v2 import STARTUP as PARENT_STARTUP
from scripts.run_sea_event_startup_v2 import STARTUP
from scripts.stage_sea_event_balanced_wrap_v2 import ARM, EVIDENCE, OUTPUT, PREVIOUS, PROOF as LAYOUT, ROM, ROOT
from scripts.verify_sea_event_bubbles_focused_v2 import PROOF as LIVE


BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
OBSERVED = [457, 463, 469, 470, 478]


def main():
    assert not BOOT.exists() and not CHECKPOINT.exists()
    staged, live, source, baseline, refined = map(load, (EVIDENCE, LIVE, OUTPUT, PREVIOUS, LAYOUT))
    sha = digest(ROM)
    assert sha == staged['research_ROM_sha256'] == live['candidate_sha256']
    assert [page['message_ID'] for page in live['observed']] == OBSERVED
    assert all(page['native_ink_matches_live_foreground_and_margins'] for page in live['observed'])
    assert live['selector_word_restored'] and live['original_compiler_generated_captain_wrap_visible']
    assert len(staged['cases']) == 98 and source['original_voice_selector_cases'] == 2898
    assert staged['exact_viewed_original_pages'] == 72 and staged['exact_viewed_balanced_pages'] == 26
    assert staged['selector_scope']['tested'] == 1232 and staged['storage']['all_41_blocks_fit_8KiB']
    assert all(digest(p) == expected for p, expected in (staged['evidence'] | live['evidence']).items())
    for sheet in (*baseline['contact_sheets'], *refined['contact_sheets']):
        assert digest(sheet['path']) == sheet['sha256']
    report_path = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert terminal['candidate_sha256'] == sha and terminal['report_sha256'] == digest(report_path)
    report, raw = checked_report(report_path, sha, 31000)
    prior_path = PARENT_STARTUP / 'capture/capture_report.json'
    prior = load(prior_path)
    assert prior['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert prior['scripted_input_schedule'] == report['scripted_input_schedule']
    assert prior['core_options'] == report['core_options']
    frames = (1600, 2200, 3340, 4000, 16000, 31000)
    previous_frames, current_frames = ({s['frame']: s for s in r['frames_captured']} for r in (prior, report))
    assert all(previous_frames[n]['framebuffer_sha256'] == current_frames[n]['framebuffer_sha256'] for n in frames)
    arm = NdsImage.open(ROM).read_file(ARM)
    check_names = FunctionType(startup_proof.__code__, {**startup_proof.__globals__, 'STARTUP': report_path})
    result = check_names(arm, sha)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    result.update(candidate_sha256=sha, cold_boot=True, savestate=False, actual_captain_getter=3,
        read_only_snapshot=report['read_only_RAM_snapshot'], complete_deployed_payload_exact=True,
        exact_predecessor_capture_sha256=digest(prior_path))
    save(BOOT, result)
    save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=OBSERVED, stored_cases=98, crew_voice_choices=2898, fresh_viewed_pages=26,
        reused_exact_viewed_pages=72, native_selector_cases=1232,
        fresh_viewed_sheets=refined['contact_sheets'], first_pass_sheets=baseline['contact_sheets'],
        evidence={str(p): digest(p) for p in (EVIDENCE, LIVE, BOOT, OUTPUT, LAYOUT, Path(__file__))}))
    print('Exact sea-event startup, six predecessor frame matches, catalogue and 24 protected name getters pass.')


if __name__ == '__main__':
    main()
