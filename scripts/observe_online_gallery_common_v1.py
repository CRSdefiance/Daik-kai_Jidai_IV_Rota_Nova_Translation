"""Observe current-ROM COMMON access and the actual Online/Gallery caption calls."""

import argparse
import inspect
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import observe_market_context_v2112 as native_observer
from scripts import register_sound_bgm_titles_v1 as parent
from scripts import replay_sound_bgm_titles_v1 as sound
from scripts.source_locked_derivation_v5118 import checked_text


base = parent.base
ROOT = Path('out/online_and_gallery_common_consumers_20261111_v1')
REQUESTS = {0x020534F4: 5, 0x0205528C: 4}
ONLINE, GALLERY = 0x02104D24, 0x02043008
TARGETS = (*REQUESTS, ONLINE, GALLERY)
FOCUS = {*range(3289, 3320), *range(3393, 3607)}


def observer(rom, folder):
    env = vars(native_observer) | dict(ROOT=folder, ROM=rom, TARGETS=TARGETS,
                                       REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY)
    setup = checked_text(inspect.getsource(native_observer.prepare_contract), {
        'for pc in(REQUEST,FONT):': 'for pc in TARGETS:',
    })
    exec(compile(setup, __file__ + '::source-checked-observer', 'exec'), env)
    env['prepare_contract']()
    source = inspect.getsource(native_observer.Observer)
    start = source.index('    if frame<31000:return')
    end = source.index('   except BaseException as exc:', start)
    replacement = """    if pc in REQUESTS:
     self.requests.append(dict(frame=frame,PC=pc,message_ID=v[REQUESTS[pc]],caller_LR=v[18]))
     return
    ptr=v[6]
    assert 0x02000000<=ptr<=0x023fff00
    key=pc,ptr,v[7]
    if key in self.seen:return
    self.seen.add(key)
    raw=ct.string_at(self.wram+ptr-0x02000000,256)
    assert 0<raw.find(b'\\0')<256
    self.rows.append(dict(frame=frame,PC=pc,pointer=ptr,text=raw.split(b'\\0',1)[0].decode('ascii'),
                          x=v[7],gallery_position=v[11] if pc==GALLERY else None,
                          gallery_table=v[12] if pc==GALLERY else None))
"""
    exec(compile(source[:start] + replacement + source[end:], __file__ + '::observe-caption-owners', 'exec'), env)
    return env['Observer']


def get_schedule(case):
    if case == 'sound':
        events = sound.inputs()[:4]
        return events, [3200], 3250, None, None
    if case == 'online':
        source = Path('work/emulation_v193/v190_all_online/capture_report.json')
        events = base.load(source)['scripted_input_schedule']
        events = [*events, *(dict(start=n, duration=8, buttons=['B']) for n in (16601, 16901, 17201))]
        frames = [int(row['start']) + 190 for row in events[5:]]
        return events, frames, 17500, source, None
    source = Path('work/emulation_v193/gallery_all_v523/capture_report.json')
    old = base.load(source)
    events = list(old['scripted_input_schedule'][:7])
    next_frame = 3201
    for route in range(4):
        if route:
            position = {1: [170, 50], 2: [84, 130], 3: [170, 130]}[route]
            events.extend([dict(start=next_frame, duration=8, buttons=[], touch=position),
                           dict(start=next_frame + 200, duration=8, buttons=['A'])])
            next_frame += 400
        for key in ('RIGHT', 'LEFT', 'LEFT', 'B'):
            events.append(dict(start=next_frame, duration=8, buttons=[key]))
            next_frame += 200
        next_frame += 200
    events.extend([dict(start=next_frame + i * 200, duration=8, buttons=['B']) for i in range(2)])
    frames = [row['start'] + 199 for row in events[4:]]
    return events, frames, next_frame + 430, source, old['battery_save_preloaded']


def main(case):
    rom = parent.ROM
    release = base.load(parent.RELEASE)
    assert base.digest(rom) == release['candidate_sha256']
    ROOT.mkdir(exist_ok=True)
    folder = ROOT / case
    cls = observer(rom, folder)
    events, frames, end, source, donor = get_schedule(case)
    inputs = folder / 'inputs.json'
    base.save(inputs, events)
    argv = [sys.argv[0], '--rom', str(rom), '--out', str(folder / 'capture'), '--frames', str(end),
        '--inputs-json', str(inputs), '--press-start', '-1', '--capture-every', '999999',
        '--capture-at', *map(str, frames)]
    if donor:
        assert base.digest(donor['source']) == donor['source_sha256']
        argv += ['--battery-save', donor['source'], '--touchscreen']
    installed = []
    native, original_argv = harness.ct, sys.argv

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

    try:
        harness.ct = CoreLoader()
        sys.argv = argv
        harness.main()
    finally:
        harness.ct, sys.argv = native, original_argv
        for trace in installed:
            trace.close()
    trace, = installed
    trace.save()
    capture = folder / 'capture/capture_report.json'
    report = base.load(capture)
    assert report['ROM_sha256'] == release['candidate_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert bool(report.get('battery_save_preloaded')) == bool(donor)
    if donor:
        assert base.digest(donor['source']) == donor['source_sha256']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    target = [request for request in trace.requests if request['message_ID'] in FOCUS]
    evidence = (capture, folder / 'requests.json', inputs, folder / 'source_contract.json', Path(__file__))
    base.save(folder / 'terminal.json', dict(case=case, ROM_sha256=report['ROM_sha256'], completed_frames=end,
        caption_calls=trace.rows, COMMON_requests=len(trace.requests), target_COMMON_calls=target,
        historical_input_source=str(source) if source else None, prepared_gallery_save=bool(donor),
        evidence={str(path): base.digest(path) for path in (*evidence, source) if path}))
    print(f'{case}: {len(trace.rows)} unique caption calls, {len(trace.requests)} COMMON entries, {len(target)} pending keys requested.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('online', 'gallery', 'sound'))
    main(parser.parse_args().case)
