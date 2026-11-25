"""Cold-boot the exact crew-notice research ROM through the approved Maria opening."""

import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_shared_crew_notices_live_v1 import PREFLIGHT


STARTUP = Path('out/shared_crew_notices_startup_20261110_v1')
PRIOR = Path('out/shared_notice_research_startup_20261110_v2')


def main():
    assert not STARTUP.exists() and STARTUP.resolve().drive.upper() == 'E:'
    proof = load(PREFLIGHT)
    rom = Path(proof['research_ROM'])
    assert digest(rom) == proof['research_ROM_sha256']
    parent = load(PRIOR / 'capture/capture_report.json')
    assert parent['ROM_sha256'] == proof['runtime']['candidate_sha256']
    assert parent['cold_boot'] and not parent['savestate_loaded']
    args = load(PRIOR / 'worker_argv.json')
    field = '--gallery-save-fixture-manifest'
    gallery = Path(args[args.index(field) + 1])
    fixture = load(gallery)
    assert fixture['production_ROM_sha256'] == parent['ROM_sha256']
    assert digest(fixture['fixture_save']) == fixture['fixture_save_sha256']
    STARTUP.mkdir()
    manifest = STARTUP / 'existing_system_unlock_manifest.json'
    save(manifest, {**fixture, 'production_ROM': str(rom), 'production_ROM_sha256': digest(rom),
        'current_test_scope': 'Ordinary Maria startup with the previously verified system-unlock fixture.'})
    for key, value in (('--rom', rom), ('--out', STARTUP / 'capture'), (field, manifest)):
        args[args.index(key) + 1] = str(value)
    save(STARTUP / 'worker_argv.json', args)
    original = sys.argv
    try:
        sys.argv = [sys.argv[0], *args]
        harness.main()
    finally:
        sys.argv = original
    assert digest(fixture['fixture_save']) == fixture['fixture_save_sha256']
    report = STARTUP / 'capture/capture_report.json'
    save(STARTUP / 'terminal.json', dict(exit_code=0, report=str(report), report_sha256=digest(report),
        research_ROM_sha256=digest(rom), fixture_save_unchanged=True))


if __name__ == '__main__':
    main()
