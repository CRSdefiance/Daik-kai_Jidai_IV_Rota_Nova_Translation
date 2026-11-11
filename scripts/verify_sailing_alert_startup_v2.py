"""Bind sailing-alert render proofs and the candidate's own registered startup."""

import json
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.run_sailing_alert_startup_v2 import PARENT, STARTUP
from scripts.stage_sailing_alert_balanced_v2 import ARM, ORDINARY, OUTPUT, PROOF, ROM, ROOT
from scripts.verify_sailing_alert_replays_v2 import BECALMED, LEVELUP, REEFS, prove_levelup


BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
LIVE = ROOT / 'sailing_alert_gameplay_verification.json'
QA = ROOT / 'repo_qa_sailing_alerts.xml'
OBSERVED = [97, 493]


def main():
    assert not CHECKPOINT.exists()
    staged, ordinary, manuscript = map(load, (PROOF, ORDINARY, OUTPUT))
    sha = digest(ROM)
    assert sha == staged['research_ROM_sha256']
    assert len(staged['stored']) == 28 and len(staged['crew_cases']) == 45
    assert staged['fresh_crew_pages'] == 10 and staged['exact_crew_pages_reused'] == 35
    assert staged['selector_scope']['tested'] == 1512 and staged['storage']['all_41_blocks_fit_8KiB']
    assert manuscript['native_crew_voice_cases'] == 828 and len(manuscript['condition_labels']) == 26
    assert len(ordinary['floating_notice']['cases']) == 207
    assert all(digest(path) == expected for path, expected in staged['evidence'].items())
    for sheet in (*ordinary['crew_contact_sheets'], *staged['fresh_crew_contact_sheets']):
        assert digest(sheet['path']) == sheet['sha256']

    levelup, becalmed, reefs = map(load, (LEVELUP, BECALMED, REEFS))
    assert {proof['candidate_sha256'] for proof in (levelup, becalmed, reefs)} == {sha}
    assert all(digest(path) == expected for proof in (becalmed, reefs)
               for path, expected in proof['evidence'].items())
    assert [row['message_ID'] for row in becalmed['observed']] == [493]
    assert becalmed['ordinary_A_dismisses_warning'] and becalmed['selector_restored']
    assert reefs['ordinary_controller_schedule'] and not reefs['target_reef_warning_observed']
    assert not reefs['observed']

    image = NdsImage.open(ROM)
    arm = image.read_file(ARM)
    level_terminal = load(LEVELUP.with_name('terminal.json'))
    assert level_terminal['candidate_sha256'] == sha
    assert digest(level_terminal['report']) == level_terminal['report_sha256']
    level_report, level_raw = checked_report(level_terminal['report'], sha, 10627)
    raster, _, _ = font_tools(image)
    pixels = prove_levelup(level_report, level_raw, level_terminal, raster, arm, image.read_file('/GRP/KANJI.FNT'))
    assert {key: levelup[key] for key in pixels} == json.loads(json.dumps(pixels))
    assert [row['actor_name'] for row in pixels['observed']] == ['Gerhard', 'Manuel']
    live = dict(candidate_sha256=sha, observed_record_IDs=OBSERVED, floating_notice=pixels,
        becalmed=becalmed, ordinary_reefs_sample=reefs, hardware=False,
        source_proofs={str(p): digest(p) for p in (LEVELUP, BECALMED, REEFS)})

    report_path = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert terminal['candidate_sha256'] == sha and terminal['report_sha256'] == digest(report_path)
    report, raw = checked_report(report_path, sha, 31000)
    parent_path = PARENT / 'capture/capture_report.json'
    parent = load(parent_path)
    assert parent['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert parent['scripted_input_schedule'] == report['scripted_input_schedule']
    assert parent['core_options'] == report['core_options']
    frames = (1600, 2200, 3340, 4000, 16000, 31000)
    previous, actual = ({s['frame']: s for s in run['frames_captured']} for run in (parent, report))
    assert all(previous[n]['framebuffer_sha256'] == actual[n]['framebuffer_sha256'] for n in frames)
    check_names = FunctionType(startup_proof.__code__, {**startup_proof.__globals__, 'STARTUP': report_path})
    startup = check_names(arm, sha)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    startup.update(candidate_sha256=sha, cold_boot=True, savestate=False, actual_captain_getter=3,
        read_only_snapshot=report['read_only_RAM_snapshot'], complete_deployed_payload_exact=True,
        exact_predecessor_capture_sha256=digest(parent_path))
    for path, receipt in ((LIVE, live), (BOOT, startup)):
        if path.exists():
            assert load(path) == json.loads(json.dumps(receipt))
        else:
            save(path, receipt)
    save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True, live_messages=OBSERVED,
        stored_cases=28, portrait_pages=45, fresh_viewed_pages=10, reused_exact_viewed_pages=35,
        native_selector_cases=1512, crew_voice_choices=828, floating_expansion_cases=207,
        evidence={str(p): digest(p) for p in (PROOF, ORDINARY, OUTPUT, BOOT, LIVE, QA, Path(__file__))}))
    print('Exact startup, six predecessor frame matches, 24 protected getters and the two changed display paths pass.')


if __name__ == '__main__':
    main()
