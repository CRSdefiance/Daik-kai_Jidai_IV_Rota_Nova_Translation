"""Exercise the Town Summary and Market with one disclosed stock status byte."""

from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from json import dumps
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import observe_market_context_v2112 as traces
from scripts import register_town_summary_20261119 as current
from scripts import replay_trade_labels_20261119 as trade
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine

base = current.base
ROOT = Path('work/town_shortage_20261119')
FRAMES = [3200, 9200, 9600, 10400, 11600]
PAUSE = 2845
REQUEST = dict(mode='Town-status display', town='Lisbon', state='Luxury Shortage')
TRADE_INIT, FRAME_READY, BITMAP_ALLOC, SHOW = 0x020BB238, 0x020BB244, 0x020C1AFC, 0x020C1B9C


def observer(rom, folder):
    scope = vars(traces) | dict(ROOT=folder,ROM=rom,TARGETS=(TRADE_INIT,FRAME_READY,BITMAP_ALLOC,SHOW),
        BITMAP_ALLOC=BITMAP_ALLOC, SHOW=SHOW)
    code = checked_text(getsource(traces.prepare_contract),{'for pc in(REQUEST,FONT):':'for pc in TARGETS:'})
    exec(compile(code,__file__+'::trade-stack-contract','exec'),scope)
    scope['prepare_contract']()
    source = getsource(traces.Observer)
    lo, hi = source.index('    if frame<31000:return'), source.index('   except BaseException as exc:')
    body = '''    if pc in self.seen:return
    self.seen.add(pc)
    sp = v[17]
    origin = struct.unpack('<I', self.image.read(self.dtcm_base,4))[0]
    def read(address, length):
     if 0x02000000 <= address <= 0x02400000-length:
      return ct.string_at(self.wram+address-0x02000000,length)
     assert origin<=address<=origin+0x4000-length,(address,origin)
     return self.image.read(self.dtcm+address-origin,length)
    row = dict(frame=frame, PC=pc, sp=sp, DTCM=origin, trade_object=v[14])
    if pc == BITMAP_ALLOC:
     header = v[5]
     row.update(bitmap_header=header, header_fields=list(struct.unpack('<5I',read(header,20))),
                width_height=list(struct.unpack('<2I',read(sp,8))))
    if pc == SHOW:
     row['destination'] = list(struct.unpack('<4i',read(v[6],16)))
    self.rows.append(row)
'''
    exec(compile(source[:lo]+body+source[hi:],__file__+'::trade-stack','exec'),scope)
    return scope['Observer']


def fixture(arm, raw, request):
    assert request == REQUEST
    assert len(raw) == 0x400000
    cpu, get = get_machine(arm,raw)
    source = get(0xCB178)
    town = get(0xB6618)
    assert town == source + 4 + 11*0x6C
    status = town + 0x6A
    assert raw[status-0x02000000] == get(0xB2E04,town) == 12
    data = bytearray(raw)
    data[status-0x02000000] = 7
    cpu.mem_write(status,b'\x07')
    text = get(0xB2D58,town)
    full = bytes(cpu.mem_read(text,20)).split(b'\0')[0]
    assert full == b'Luxury Shortage'
    return bytes(data), dict(synthetic_status_selection=True, town_index=11, town_address=town,
        state_before='Normal', state_after=full.decode('ascii'), natural_shortage_unverified=True,
        changes=[dict(address=status,before=12,after=7)])


def capture(case, pause):
    rom, release = current.ROM, current.RELEASE
    if case == 'corrected':
        from scripts import stage_town_shortage_20261119 as stage
        rom, release = stage.ROM, stage.PROOF
    expected = base.load(release)['candidate_sha256']
    assert base.digest(rom) == expected
    plan = base.load(trade.PLAN)
    inputs = Path(plan['unchanged_inputs'])
    donor = plan['source_save']
    assert base.digest(inputs) == plan['unchanged_inputs_sha256']
    assert base.digest(donor['source']) == donor['source_sha256']
    version = 3 if case == 'corrected' else 2
    output = ROOT/f'{case}_{pause}_v{version}'
    assert not output.exists()
    argv = [harness.__file__,'--rom',str(rom),'--out',str(output),'--battery-save',donor['source'],
        '--inputs-json',str(inputs),'--press-start','-1','--touchscreen','--frames','11600','--capture-every','999999',
        '--capture-at',*map(str,FRAMES),'--pause-at',str(pause),'--dump-capture-ram','--dump-pause-ram','--allow-condition-fixtures']
    stack_trace = output.with_name(output.name+'_stack')
    cls = observer(rom,stack_trace)
    ctypes = harness.ct
    installed = []

    class CoreLoader:
        def __getattr__(self,name):
            return getattr(ctypes,name)

        def CDLL(self,path,*args,**kwargs):
            core = ctypes.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                trace = cls(core,stack_trace)
                trace.install()
                installed.append(trace)
                original = core.retro_run
                original.restype = None

                def tick():
                    trace.header[0] += 1
                    original()

                core.retro_run = tick
            return core

    old, stdin, original_args = adapter.set_condition, sys.stdin, sys.argv
    try:
        adapter.set_condition = fixture
        harness.ct = CoreLoader()
        sys.argv = argv
        commands = (dict(until=11600,duration=1,condition_fixture=REQUEST),dict(stop=True))
        sys.stdin = StringIO(''.join(dumps(command)+'\n' for command in commands))
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = old, stdin, original_args
        harness.ct = ctypes
        for trace in installed:
            trace.close()
    trace, = installed
    trace.save()
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case',choices=('baseline','corrected'))
    parser.add_argument('--pause',type=int,default=PAUSE)
    args=parser.parse_args()
    capture(args.case,args.pause)
