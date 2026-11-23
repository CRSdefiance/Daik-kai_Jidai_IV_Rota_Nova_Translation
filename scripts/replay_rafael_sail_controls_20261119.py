"""Exercise the unchanged structure of B128 behind Rafael's original New Game prelude."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType
import sys

from scripts import check_rafael_ceuta_contract_routes_20261119 as previous
from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_B180_v4810 as original
from scripts import review_rafael_sail_controls_20261119 as stage
from scripts import run_Rafael_B46_scenes_v7945 as prelude

base, native = stage.base, stage.native
ROOT = stage.STAGED / 'initialized_lesson'
FIXTURE = ROOT / 'Rafael_Sail_Controls_QA_ONLY.nds'
MANIFEST = ROOT / 'fixture.json'
SC0 = '/data/SC0.DK4'
INPUT = Path('work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json')
CONTRACT = original.ROOT / 'source_contract.json'
FRAMES = 16601


def prepare():
    assert not ROOT.exists()
    staged = base.load(stage.PROOF)
    assert staged['candidate_sha256'] == base.digest(stage.ROM)
    group, = staged['groups']
    assert group['file_path'] == SC0 and group['block'] == 128
    earlier, = (r for r in base.load(prelude.FIXTURES)['fixtures'] if r['version'] == 'English')
    original_prelude = bytes.fromhex(earlier['original_opening_prelude_hex'])
    image = base.NdsImage.open(stage.ROM)
    bank = native.IlnkContainer.parse(image.read_file(SC0))
    host, lesson = bank.blocks[44], bank.blocks[128]
    assert native.digest(lesson) == group['after'] and host[8:40] == original_prelude
    assert (host[:4], host[6:8]) == (lesson[:4], lesson[6:8])
    delta = len(original_prelude)
    assert delta == 32
    logical = bytearray(host[:8] + original_prelude + lesson[8:stage.workflow.logical_end(lesson)])
    pack_into('<H', logical, 4, len(logical) - 8)
    fixture = bytes(logical) + bytes(-len(logical) % 4)
    arm = image.read_file(native.ARM)
    inventory, _, _ = native.scoped_inventory()
    parsed, speeches = inventory(arm, fixture)
    assert len(speeches) == 45 and len(parsed) == 78 and parsed[-1]['word'] == 0
    for check, command in zip(parsed[10:], group['commands'], strict=True):
        at = command['stored_offset'] + delta
        exact = bytes.fromhex(command['stored'])
        assert check['offset'] == at and check['word'] == command['word']
        assert fixture[at:at + len(exact)] == exact
    ROOT.mkdir()
    bank.blocks[44] = fixture
    image.replace_file(SC0, bank.to_bytes())
    image.save(FIXTURE)
    result = base.NdsImage.open(FIXTURE)
    legacy = base.NdsImage.open(stage.ROM).read_file(SC0)
    result.replace_file(SC0, legacy)
    assert result.rom.save() == stage.ROM.read_bytes()
    base.save(MANIFEST, dict(stage_sha256=staged['candidate_sha256'], fixture_sha256=base.digest(FIXTURE),
        block_44_sha256=native.digest(fixture), original_block_128_sha256=group['after'],
        offset_delta=delta, complete_script_inverse=True, natural_activation=False,
        historical_prelude_sha256=base.digest(prelude.FIXTURES)))
    print('Prepared the complete B128 interpreter path with the original Rafael initialization.')


def capture():
    receipt = base.load(MANIFEST)
    assert receipt['fixture_sha256'] == base.digest(FIXTURE)
    schedule = base.load(INPUT)
    assert schedule and max(item['start'] for item in schedule) <= 2200
    schedule += [dict(start=frame, duration=5, buttons=['A']) for frame in range(4000, FRAMES, 240)]
    inputs = ROOT / 'ordinary_inputs.json'
    assert not inputs.exists()
    base.save(inputs, schedule)
    (ROOT / CONTRACT.name).write_bytes(CONTRACT.read_bytes())
    arm = base.NdsImage.open(FIXTURE).read_file(native.ARM)
    for target in base.load(CONTRACT)['targets']:
        assert unpack_from('<I', arm, target['PC'] - 0x02000000)[0] == target['word']

    scope = vars(original) | dict(ROOT=ROOT, ROM=FIXTURE)

    class Observer(original.Observer):
        __init__ = FunctionType(original.Observer.__init__.__code__, scope)
        save = FunctionType(original.Observer.save.__code__, scope)

    attached = []
    old_ct, old_argv = harness.ct, sys.argv

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(old_ct, name)

        def CDLL(self, path, *args, **kwargs):
            core = old_ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer = Observer(core, ROOT / 'observer')
                observer.install()
                attached.append(observer)
                advance = core.retro_run
                advance.restype = None

                def tick():
                    observer.next_frame()
                    advance()

                core.retro_run = tick
            return core

    frames = sorted(set(range(2500, FRAMES, 45)) | {FRAMES - 1})
    try:
        harness.ct = CoreLoader()
        sys.argv = [harness.__file__, '--rom', str(FIXTURE), '--out', str(ROOT / 'capture'),
            '--frames', str(FRAMES), '--inputs-json', str(inputs), '--press-start', '-1',
            '--capture-every', '999999', '--capture-at', *map(str, frames)]
        harness.main()
    finally:
        harness.ct, sys.argv = old_ct, old_argv
        for observer in attached:
            observer.close()
    observer, = attached
    observer.save()
    report = base.load(ROOT / 'capture/capture_report.json')
    assert report['frames'] == FRAMES and report['ROM_sha256'] == receipt['fixture_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert report['scripted_input_schedule'] == schedule and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'capture', 'patch', 'capture-startup', 'startup'))
    action = parser.parse_args().action
    if action in ('prepare', 'capture'):
        globals()[action]()
    else:
        precedent = previous.precedent
        scope = vars(precedent) | dict(stage=stage, STARTUP=stage.STAGED / 'own_startup_verification.json',
            STARTUP_DIR=stage.STAGED / 'own_startup')
        if action == 'patch':
            FunctionType(precedent.patch.__code__, scope)()
        else:
            FunctionType(precedent.startup.__code__, scope)(action == 'capture-startup')
