"""Observe Julio's Deck lesson through the ordinary post-Trade transition."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_B180_v4810 as original
from scripts import register_town_shortage_20261119 as parent

base = parent.base
ROOT = Path('work/rafael_deck_after_trade_20261119')
CONTRACT = Path('work/analysis/script_sources_v733/source_contract.json')
PRIOR = parent.stage.ROOT/'ordinary_trade_return_verification.json'
INPUTS = parent.stage.ROOT/'ordinary_trade_return_inputs.json'
AFTER = tuple(range(12401,16601,300))
FRAMES = [12000,12400,*[n+260 for n in AFTER],16800]
END = 16801


def capture(case):
    if case == 'current':
        rom, proof = parent.ROM, parent.RELEASE
    else:
        from scripts import stage_rafael_deck_after_trade_20261119 as build
        rom, proof = build.ROM, build.PROOF
    assert base.digest(rom) == base.load(proof)['candidate_sha256']
    prior = base.load(PRIOR)
    assert prior['candidate_sha256'] == base.digest(parent.ROM)
    assert base.digest(INPUTS) == prior['evidence'][str(INPUTS)]
    report = base.load(parent.stage.ROOT/'ordinary_trade_return/capture_report.json')
    donor = report['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    directory = ROOT/case
    assert not directory.exists()
    directory.mkdir(parents=True)
    inputs = directory/'inputs.json'
    events = base.load(INPUTS) + [dict(start=f,duration=8,buttons=['A']) for f in AFTER]
    assert events[:len(report['scripted_input_schedule'])] == report['scripted_input_schedule']
    base.save(inputs,events)
    arm = base.NdsImage.open(rom).read_file(parent.stage.ARM)
    for row in base.load(CONTRACT)['targets']:
        assert unpack_from('<I',arm,row['PC']-0x02000000)[0] == row['word']
    (directory/'source_contract.json').write_bytes(CONTRACT.read_bytes())
    env = vars(original) | dict(ROM=rom, ROOT=directory)

    class DeckObserver(original.Observer):
        __init__ = FunctionType(original.Observer.__init__.__code__,env)
        save = FunctionType(original.Observer.save.__code__,env)

    ctypes, argv = harness.ct, sys.argv
    attached = []

    class CoreLoader:
        def __getattr__(self,name):
            return getattr(ctypes,name)

        def CDLL(self,path,*args,**kwargs):
            core = ctypes.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                trace = DeckObserver(core,directory/'observer')
                trace.install()
                attached.append(trace)
                advance = core.retro_run
                advance.restype = None

                def tick():
                    trace.next_frame()
                    advance()

                core.retro_run = tick
            return core

    try:
        harness.ct = CoreLoader()
        sys.argv = [harness.__file__,'--rom',str(rom),'--out',str(directory/'capture'),'--frames',str(END),
            '--inputs-json',str(inputs),'--press-start','-1','--touchscreen','--battery-save',donor['source'],
            '--capture-every','999999','--capture-at',*map(str,FRAMES)]
        harness.main()
    finally:
        harness.ct,sys.argv = ctypes,argv
        for trace in attached:
            trace.close()
    trace, = attached
    trace.save()
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case',choices=('current','corrected'))
    capture(parser.parse_args().case)
