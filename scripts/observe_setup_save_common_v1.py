"""Record native COMMON requests during the current DS startup and options flow."""

import argparse
import inspect
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import observe_market_context_v2112 as observer
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_captain_biographies_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/setup_save_common_20261111_v1')
REQUESTS = {0x020534F4: 5, 0x0205528C: 4}
FOCUS = {*range(98, 125), *range(315, 330), 750, 751, 752}
SCHEDULE = {
    'setup': [(1601, 'START'), (2001, 'DOWN'), (2401, 'A'), (2801, 'Y'),
              (3201, 'DOWN'), (3601, 'DOWN'), (4001, 'DOWN'), (4401, 'DOWN'),
              (4801, 'A'), (5201, 'RIGHT'), (5601, 'A'), (6001, 'B'),
              (6401, 'B'), (6801, 'A'), (7201, 'B')],
    'storage': [(1601, 'START'), (2001, 'A'), (2401, 'B'), (2801, 'DOWN'),
                (3201, 'DOWN'), (3601, 'A'), (4001, 'DOWN'), (4401, 'A'),
                (4801, 'LEFT'), (5201, 'RIGHT'), (5601, 'B'), (6001, 'B')],
}


def scoped_observer(rom, folder):
    env = {**vars(observer), 'ROOT': folder, 'ROM': rom, 'REQUESTS': REQUESTS}
    setup = checked_text(inspect.getsource(observer.prepare_contract), {
        'for pc in(REQUEST,FONT):': 'for pc in REQUESTS:',
    })
    exec(compile(setup, __file__ + '::same-source-core-contract', 'exec'), env)
    env['prepare_contract']()
    source = inspect.getsource(observer.Observer)
    start = source.index('    if frame<31000:return')
    end = source.index('   except BaseException as exc:', start)
    replacement = """    self.requests.append(dict(frame=frame, PC=pc, message_ID=v[REQUESTS[pc]], caller_LR=v[18]))
    return
"""
    source = source[:start] + replacement + source[end:]
    exec(compile(source, __file__ + '::read-only-request-entry', 'exec'), env)
    return env['Observer']


def main(case):
    release = load(RELEASE)
    rom = Path(release['candidate'])
    assert digest(rom) == release['candidate_sha256']
    ROOT.mkdir(exist_ok=True)
    folder = ROOT / case
    cls = scoped_observer(rom, folder)
    inputs = [{'start': frame, 'duration': 8, 'buttons': [key]} for frame, key in SCHEDULE[case]]
    save(folder / 'inputs.json', inputs)
    frames = [event['start'] + 199 for event in inputs]
    argv = [sys.argv[0], '--rom', str(rom), '--out', str(folder / 'capture'),
        '--frames', str(frames[-1] + 10), '--inputs-json', str(folder / 'inputs.json'),
        '--capture-every', '999999', '--capture-at', *map(str, frames)]
    installed = []
    native = harness.ct

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(native, name)

        def CDLL(self, path, *args, **kwargs):
            core = native.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                trace = cls(core, folder)
                trace.install()
                installed.append(trace)
                advance = core.retro_run
                advance.restype = None

                def tick():
                    trace.header[0] += 1
                    advance()

                core.retro_run = tick
            return core

    original = sys.argv
    try:
        harness.ct = CoreLoader()
        sys.argv = argv
        harness.main()
    finally:
        harness.ct = native
        sys.argv = original
        for trace in installed:
            trace.close()
    assert len(installed) == 1
    trace, = installed
    trace.save()
    capture = folder / 'capture/capture_report.json'
    requests = folder / 'requests.json'
    result = load(capture)
    assert result['cold_boot'] and not result['savestate_loaded'] and not result['callback_errors']
    assert result['ROM_sha256'] == release['candidate_sha256']
    assert not any(value for key, value in result.items() if key.startswith('synthetic_'))
    focus = [row for row in trace.requests if row['message_ID'] in FOCUS]
    save(folder / 'terminal.json', dict(case=case, candidate_sha256=result['ROM_sha256'],
        native_common_entries_traced=list(REQUESTS), original_controller_only=True,
        battery_save_preloaded=False, native_request_rows=len(trace.requests), target_requests=focus,
        scoped_absence_is_not_proof_of_global_unreachability=True,
        evidence={str(path): digest(path) for path in (capture, requests, Path(__file__))}))
    print(f'{case}: {len(trace.requests)} native requests, {len(focus)} in focus.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=SCHEDULE)
    main(parser.parse_args().case)
