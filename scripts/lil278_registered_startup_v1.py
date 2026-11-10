"""Capture and verify the exact registered-successor startup."""

from pathlib import Path
import sys

from scripts.source_locked_derivation_v5118 import checked_text


RELEASE = Path('work/lil278_B299_B311_release_v1')


def main():
    mode = sys.argv.pop(1)
    if mode == 'run':
        from scripts import headless_desmume_v193 as harness
        from scripts.audit_story_glyph_consistency import load
        from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

        root = RELEASE / 'own_startup_run_v1'
        plan, worker = map(load, (root / 'run_plan.json', root / 'worker_argv.json'))
        assert digest(plan['candidate']) == plan['candidate_sha256'] == worker['candidate_sha256']
        sys.argv = [sys.argv[0], *worker['argv']]
        harness.main()
        return
    if mode == 'prepare':
        from scripts.prepare_lil361_own_startup_v1 import source
    elif mode == 'render':
        from scripts.render_lil361_startup_v1 import source
    elif mode == 'bind':
        source = checked_text(Path('scripts/bind_lil269_startup_visual_v1.py').read_text(encoding='utf-8'), {
            'work/lil269_B243_B282_release_v1': RELEASE.as_posix(),
        })
    elif mode == 'verify':
        from scripts.verify_lil361_startup_v1 import source

        source = checked_text(source, {
            '    save(STARTUP,dict(candidate=':
                """    visual_path = OUT/'own_startup_visual_v1/direct_visual_review.json'
    visual = load(visual_path)
    assert visual['all_six_original_captures_andexact_composite_directly_viewed']
    assert visual['selected_captures'] == selected and digest(visual['sheet']) == visual['sheet_sha256']
    save(STARTUP,dict(candidate=""",
            '[CAPTURE,plan_path,PARENT,old_report_path,Path(__file__)]':
                '[CAPTURE,plan_path,PARENT,old_report_path,visual_path,Path(__file__)]',
        })
    else:
        raise SystemExit('Expected prepare, run, render, bind, or verify.')
    source = (source.replace('scripts.build_registered_lil361_v1', 'scripts.build_registered_lil278_v1')
                    .replace('work/lil361_B283_B298_release_v1', RELEASE.as_posix())
                    .replace('Lil361 B283-B298', 'Lil278 B299-B311')
                    .replace('Lil361 cumulative', 'Lil278 cumulative'))
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})


if __name__ == '__main__':
    main()
