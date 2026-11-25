"""Exercise the King's Shield rumor in the original Lisbon Guild purchase flow."""

from argparse import ArgumentParser
import sys
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType, SimpleNamespace

from scripts import check_rafael_voyage_ceuta_20261119 as checks
from scripts import headless_desmume_v193 as harness
from scripts import observe_setup_save_common_v1 as observer
from scripts import replay_twisted_horn_rumor_20261119 as prior
from scripts import stage_artifact_rumor_wraps_20261119 as stage

base = stage.base
ROOT = stage.ROOT / 'initialized_kings_shield'
CAPTURE = ROOT / 'capture'
RECEIPT = ROOT / 'fixture.json'
PARENT_CAPTURE = prior.CAPTURE / 'capture_report.json'
STARTUP_DIR = stage.ROOT / 'own_startup'
STARTUP = stage.ROOT / 'own_startup_verification.json'
FRAMES = (56260, 56500, 56740, 56980, 57220, 57460)
END = FRAMES[-1] + 1
TABLE, FIRST_SLOT = 0x023800CC, 195
SHIELD, INSERT, RESTORE = 196, 56501, 56981
ID = 3666


def capture():
    assert not ROOT.exists()
    original, compiled = map(base.load, (PARENT_CAPTURE, stage.PROOF))
    assert original['ROM_sha256'] == compiled['predecessor_sha256'] == base.digest(stage.parent.ROM)
    assert base.digest(stage.ROM) == compiled['candidate_sha256']
    assert original['cold_boot'] and not original['savestate_loaded'] and not original['callback_errors']
    donor = original['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    events = [r for r in original['scripted_input_schedule'] if r['start'] + r['duration'] <= END]
    assert dict(start=INSERT, duration=8, buttons=['A']) in events and dict(start=RESTORE, duration=8, buttons=['A']) in events
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.ARM)
    assert unpack_from('<I', arm, 0x5C454)[0] == TABLE
    assert unpack_from('<I', arm, 0x5C45C)[0] + SHIELD - 188 == ID
    stock_arm = base.NdsImage.open(stage.native.CLEAN).read_file(stage.ARM)
    assert arm[0x5C188:0x5C1D0] == stock_arm[0x5C188:0x5C1D0]
    report = next(r for r in original['read_only_capture_RAM_snapshots'] if r['frame'] == INSERT - 1)
    historical = Path(report['path']).read_bytes()
    assert base.digest(report['path']) == report['sha256'] and report['read_only_export']
    offset = TABLE - 0x02000000
    assert unpack_from('<5I', historical, offset) == (FIRST_SLOT, 189, SHIELD, 190, 191)

    observer_class = observer.scoped_observer(stage.ROM, ROOT)
    schedule = ROOT / 'inputs.json'
    base.save(schedule, events)
    original_ct, old_args = harness.ct, sys.argv
    attached, mutations = [], []

    def set_entry(trace, frame, old, new):
        raw = original_ct.string_at(trace.wram, 0x400000)
        assert unpack_from('<I', raw, offset)[0] == old
        if frame == INSERT:
            assert raw[offset:offset + 20] == historical[offset:offset + 20]
        original_ct.memmove(trace.wram + offset, pack('<I', new), 4)
        actual = original_ct.string_at(trace.wram, 0x400000)
        assert actual == raw[:offset] + pack('<I', new) + raw[offset + 4:]
        mutations.append(dict(frame=frame, address=TABLE, before=old, after=new, all_other_WRAM_exact=True))

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(original_ct, name)

        def CDLL(self, path, *args, **kwargs):
            core = original_ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                trace = observer_class(core, ROOT)
                trace.install()
                attached.append(trace)
                advance = core.retro_run
                advance.restype = None

                def tick():
                    trace.header[0] += 1
                    frame = trace.header[0]
                    if frame == INSERT:
                        set_entry(trace, frame, FIRST_SLOT, SHIELD)
                    elif frame == RESTORE:
                        set_entry(trace, frame, SHIELD, FIRST_SLOT)
                    advance()

                core.retro_run = tick
            return core

    try:
        harness.ct = CoreLoader()
        sys.argv = [harness.__file__, '--rom', str(stage.ROM), '--out', str(CAPTURE), '--frames', str(END),
            '--inputs-json', str(schedule), '--battery-save', donor['source'], '--press-start', '-1',
            '--touchscreen', '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-capture-ram']
        harness.main()
    finally:
        harness.ct, sys.argv = original_ct, old_args
        for trace in attached:
            trace.close()
    trace, = attached
    trace.save()
    target = [row for row in trace.requests if row['message_ID'] == ID and INSERT <= row['frame'] < RESTORE]
    assert len(target) == 2 and {r['PC'] for r in target} == {0x020534F4, 0x0205528C}
    assert len(mutations) == 2 and base.digest(donor['source']) == donor['source_sha256']
    base.save(RECEIPT, dict(candidate_sha256=compiled['candidate_sha256'], original_ROM_sha256=original['ROM_sha256'],
        original_rumor_index=FIRST_SLOT, supplied_rumor_index=SHIELD, actual_COMMON_requests=target,
        temporary_runtime_input=mutations, runtime_table_restored=True, natural_selection=False,
        no_rom_code_text_or_script_fixture=True, source_save_unchanged=True,
        evidence={str(p):base.digest(p) for p in (PARENT_CAPTURE, schedule, CAPTURE/'capture_report.json', ROOT/'requests.json')}))
    print('Observed the original Guild selector requesting COMMON 3666 after one temporary artifact-table input.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('capture', 'patch', 'capture-startup', 'startup'))
    action = parser.parse_args().action
    adapted = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, STAGED=stage.ROOT, parent=stage.parent)
    scope = vars(checks) | dict(stage=adapted, STARTUP=STARTUP, STARTUP_DIR=STARTUP_DIR)
    if action == 'capture':
        capture()
    elif action == 'patch':
        FunctionType(checks.patch.__code__, scope)()
    else:
        FunctionType(checks.startup.__code__, scope)(action == 'capture-startup')
