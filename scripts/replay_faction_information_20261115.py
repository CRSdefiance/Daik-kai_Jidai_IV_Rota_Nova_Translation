"""Replay the original Strategist report and its company-information popup."""

from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture
from scripts import native_strategist_fixture_v624 as strategist
from scripts import observe_market_context_v2112 as native_observer
from scripts import register_ritual_officiant_labels_20261115 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('work/faction_information_20261115_v1')
REFERENCE = Path('work/emulation_v193/inn_v803_report_complete/capture_report.json')
FLEET_REFERENCE = Path('work/emulation_v193/fleet_detail_v375/capture_report.json')
FRAMES = (3200, 3600, 4000, 4400, 4800, 5200, 5600, 5740, 5940, 6000, 6400, 6800)
TRACED = (0x0205CC58, 0x0208BF74, 0x0203D678, 0x0203D6A8, 0x0203D70C, 0x0203D728, 0x0203D750,
          0x0203D7B4, 0x0203D7FC, 0x0205528C, 0x020534F4)


def observer(rom, folder):
    env = vars(native_observer) | dict(ROM=rom, ROOT=folder, TRACED=TRACED)
    setup = checked_text(getsource(native_observer.prepare_contract), {
        'for pc in(REQUEST,FONT):': 'for pc in TRACED:',
    })
    exec(compile(setup, __file__ + '::static-trace-contract', 'exec'), env)
    env['prepare_contract']()
    source = getsource(native_observer.Observer)
    start = source.index('    if frame<31000:return')
    end = source.index('   except BaseException as exc:', start)
    replacement = '''    if frame<3200:return
    row=dict(frame=frame,PC=pc,LR=v[18],arguments=list(v[4:8]),stack=v[17])
    if 0x0203D600<=pc<0x0203D800:
     pointer=v[5];assert 0x02000000<=pointer<0x023fff80
     text=ct.string_at(self.wram+pointer-0x02000000,128).split(b'\\0')[0]
     context=ct.string_at(self.wram+v[4]-0x02000000,72)
     row.update(text=text.decode('cp932'),complete_text_hex=text.hex(),context_hex=context.hex())
     if pc==0x0203D70C:
      row['fifth_argument']=struct.unpack('<I',ct.string_at(self.wram+v[17]-0x02000000,4))[0]
    self.requests.append(row)
    return
'''
    exec(compile(source[:start] + replacement + source[end:], __file__ + '::read-only-UI-observer', 'exec'), env)
    return env['Observer']


def replay(rom, expected, folder, trace=False, fleet=False):
    assert base.digest(rom) == expected
    prior = base.load(FLEET_REFERENCE if fleet else REFERENCE)
    donor = prior['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    original_arm, arm = [base.NdsImage.open(path).read_file(current.stage.ARM)
                         for path in (current.stage.CLEAN, rom)]
    spans = ((0x3D060, 0x3D15C), (0x3D344, 0x3D8F4), (0x5CB3C, 0x5CC68), (0x7DAF0, 0x7DB14))
    for lo, hi in spans:
        expected_span = original_arm[lo:hi]
        if lo <= 0x3D4F8 < hi:
            index = 0x3D4F8 - lo
            assert expected_span[index:index + 4] == bytes.fromhex('0420a0e1')
            expected_span = expected_span[:index] + bytes.fromhex('0320a0e1') + expected_span[index + 4:]
        assert arm[lo:hi] == expected_span
    env = vars(strategist) | {key: current.stage.digest(arm) for key in ('ARM', 'TARGET', 'CONTEXT', 'QUEUED')}
    apply = FunctionType(strategist.assign.__code__, env)

    def supplied_assignment(current_arm, raw, request):
        assert current_arm == arm and request == {'mode': 'Inn-strategist'}
        return apply(arm, raw, True)

    folder.mkdir(parents=True)
    traces = []
    original_loader = harness.ct
    observer_folder = folder / 'observer'
    if trace:
        trace_class = observer(rom, observer_folder)

        class CoreLoader:
            def __getattr__(self, name):
                return getattr(original_loader, name)

            def CDLL(self, path, *args, **kwargs):
                core = original_loader.CDLL(path, *args, **kwargs)
                if str(path).lower().endswith('desmume_libretro.dll'):
                    installed = trace_class(core, observer_folder)
                    installed.install()
                    traces.append(installed)
                    advance = core.retro_run
                    advance.restype = None

                    def tick():
                        installed.header[0] += 1
                        advance()

                    core.retro_run = tick
                return core

        harness.ct = CoreLoader()
    schedule = folder / 'inputs.json'
    base.save(schedule, prior['scripted_input_schedule'])
    commands = [dict(until=6800, condition_fixture=dict(mode='Inn-strategist')), dict(stop=True)]
    frames = (15600, 16000, 16400, 16800, 17000, 17100, 17200, 17400) if fleet else FRAMES
    terminal = frames[-1]
    args = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'), '--frames', str(terminal + 1),
            '--inputs-json', str(schedule), '--press-start', '-1', '--touchscreen', '--battery-save', donor['source'],
            '--capture-every', '999999', '--capture-at', *map(str, frames), '--dump-capture-ram']
    if not fleet:
        args.extend(['--pause-at', '3200', '--allow-condition-fixtures'])
    old = sys.argv, sys.stdin, fixture.set_condition
    try:
        sys.argv = args
        sys.stdin = StringIO(''.join(dumps(row) + '\n' for row in commands))
        fixture.set_condition = supplied_assignment
        harness.main()
    finally:
        harness.ct = original_loader
        sys.argv, sys.stdin, fixture.set_condition = old
        for installed in traces:
            installed.close()
            installed.save()
    assert len(traces) == int(trace)
    report = folder / 'capture/capture_report.json'
    data = base.load(report)
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert data['ROM_sha256'] == expected and data['frames'] == terminal + int(fleet)
    assert data['scripted_input_schedule'] == prior['scripted_input_schedule']
    if fleet:
        assert not any(value for key, value in data.items() if key.startswith('synthetic_'))
    else:
        assignment, = data['synthetic_condition_fixtures']
        assert assignment['frame'] == 3200 and len(assignment['changes']) == 3
        assert assignment['only_three_declared_room_type_and_assignment_bytes_changed']
    assert base.digest(donor['source']) == donor['source_sha256']
    base.save(folder / 'terminal.json', dict(ROM_sha256=expected, trace=str(report), trace_sha256=base.digest(report),
        untouched_donor=donor['source_sha256'], original_report_selection_and_renderer=True,
        test_fixture_scope='Ordinary Fleet Info inputs.' if fleet else 'Only Gerhard’s room type and two assignment bytes are supplied.'))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, default=current.ROM)
    parser.add_argument('--sha256', default=base.load(current.RELEASE)['candidate_sha256'])
    parser.add_argument('--out', type=Path, default=ROOT / 'current')
    parser.add_argument('--trace', action='store_true')
    parser.add_argument('--fleet', action='store_true')
    args = parser.parse_args()
    replay(args.rom, args.sha256, args.out, args.trace, args.fleet)
