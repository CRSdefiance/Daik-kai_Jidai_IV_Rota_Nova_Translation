"""Cold-boot the refined research ROM through the existing Maria startup replay."""

import sys

from scripts import headless_desmume_v193 as harness
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_diplomatic_outcomes_layout_v2 import EVIDENCE, ROM, ROOT
from scripts.run_shared_crew_startup_v1 import STARTUP as PRIOR


STARTUP = ROOT / 'own_startup'


def main():
    staged = load(EVIDENCE)
    assert digest(ROM) == staged['research_ROM_sha256']
    parent = load(PRIOR / 'capture/capture_report.json')
    assert parent['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert parent['cold_boot'] and not parent['savestate_loaded']
    args = load(PRIOR / 'worker_argv.json')
    flag = '--gallery-save-fixture-manifest'
    fixture = load(args[args.index(flag) + 1])
    assert fixture['production_ROM_sha256'] == parent['ROM_sha256']
    assert digest(fixture['fixture_save']) == fixture['fixture_save_sha256']
    STARTUP.mkdir()
    manifest = STARTUP / 'system_unlock_manifest.json'
    save(manifest, fixture | dict(production_ROM=str(ROM), production_ROM_sha256=digest(ROM),
        current_test_scope='Ordinary Maria startup with the previously verified system-unlock fixture.'))
    for name, path in (('--rom', ROM), ('--out', STARTUP / 'capture'), (flag, manifest)):
        args[args.index(name) + 1] = str(path)
    save(STARTUP / 'worker_argv.json', args)
    original = sys.argv
    try:
        sys.argv = [sys.argv[0], *args]
        harness.main()
    finally:
        sys.argv = original
    assert digest(fixture['fixture_save']) == fixture['fixture_save_sha256']
    report = STARTUP / 'capture/capture_report.json'
    save(STARTUP / 'terminal.json', dict(report=str(report), report_sha256=digest(report),
        candidate_sha256=digest(ROM), unchanged_unlock_fixture=True))


if __name__ == '__main__':
    main()
