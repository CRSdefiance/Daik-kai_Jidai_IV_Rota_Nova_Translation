"""Continue Rafael's ordinary voyage while tracing COMMON requests and scene commands."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from
import sys

from scripts import headless_desmume_v193 as harness
from scripts import observe_lil_B180_v4810 as story
from scripts import observe_setup_save_common_v1 as common
from scripts import register_rafael_voyage_ceuta_20261119 as active
from scripts import replay_rafael_voyage_ceuta_20261119 as prior
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text

base, native = active.base, active.native
ROOT = Path('work/rafael_ceuta_arrival_20261119_v2')
PREFIX = prior.staged.ROOT / 'revised_v3' / 'capture' / 'capture_report.json'
CONTRACT = Path('work/analysis/script_sources_v733/source_contract.json')
JOURNAL = ROOT / 'navigation.jsonl'
CAPTURE = ROOT / 'capture'
START = 34421


def make_observer():
    arm = base.NdsImage.open(active.ROM).read_file(native.ARM)
    clean = base.NdsImage.open(native.CLEAN).read_file(native.ARM)
    core = story.CORE.read_bytes()
    assert story.sha(core) == story.CORE_SHA
    image_base, table = tables(core)
    contract = base.load(CONTRACT)
    assert table == contract['interpreter_table']
    for pc in common.REQUESTS:
        at = pc-0x02000000
        word = unpack_from('<I', arm, at)[0]
        assert arm[at:at+4] == clean[at:at+4]
        index = word >> 16 & 0xff0 | word >> 4 & 15
        rva = unpack_from('<Q', core, table['file_offset']+index*8)[0]-image_base
        contract['targets'].append(dict(PC=pc, word=word, instruction_index=index, handler_RVA=rva, name='COMMON_request'))
    assert all(unpack_from('<I', arm, r['PC']-0x02000000)[0] == r['word'] for r in contract['targets'])
    base.save(ROOT / 'source_contract.json', contract)
    code = checked_text(getsource(story.Observer), {
        '        self.saved, self.unknown_saved = {}, 0': '        self.saved, self.unknown_saved = {}, 0\n        self.common_requests = []',
        "                assert values[1] == target['word']":
            """                assert values[1] == target['word']
                if target['name'] == 'COMMON_request':
                    self.common_requests.append(dict(frame=frame, PC=values[2], caller_LR=values[18],
                        message_ID=values[REQUESTS[values[2]]]))
                    assert ct.string_at(self.cpu, len(cpu)) == cpu and ct.string_at(self.wram, len(raw)) == raw
                    assert self.image.read(self.dtcm, len(dtcm)) == dtcm and self.image.read(self.itcm, len(itcm)) == itcm
                    assert self.image.read(self.dtcm_base, len(base_raw)) == base_raw
                    return""",
        "'callbacks': self.header[2], 'mismatches': self.header[3],":
            "'callbacks': self.header[2], 'mismatches': self.header[3], 'COMMON_requests': self.common_requests,",
    })
    env = vars(story) | dict(ROOT=ROOT, ROM=active.ROM, REQUESTS=common.REQUESTS, __file__=__file__)
    exec(compile(code, __file__+'::observer', 'exec'), env)
    return env['Observer']


def main():
    release, prefix = map(base.load, (active.RELEASE, PREFIX))
    assert base.digest(active.ROM) == release['candidate_sha256'] == prefix['ROM_sha256']
    assert prefix['frames'] == START and prefix['cold_boot'] and not prefix['savestate_loaded']
    donor = prefix['battery_save_preloaded']
    assert donor['source_sha256'] == base.digest(donor['source'])
    ROOT.mkdir(parents=True)
    JOURNAL.touch(exist_ok=False)
    keys = ROOT / 'ordinary_prefix_inputs.json'
    base.save(keys, prefix['scripted_input_schedule'])
    observer = make_observer()
    old_ct, old_stdin, old_argv = harness.ct, sys.stdin, sys.argv
    stream = GrowingCommands(JOURNAL)
    attached = []

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(old_ct, name)

        def CDLL(self, path, *args, **kwargs):
            core = old_ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                trace = observer(core, ROOT / 'observer')
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
        harness.ct, sys.stdin = CoreLoader(), stream
        sys.argv = [harness.__file__, '--rom', str(active.ROM), '--out', str(CAPTURE), '--frames', '90000',
            '--inputs-json', str(keys), '--press-start', '-1', '--touchscreen', '--battery-save', donor['source'],
            '--capture-every', '999999', '--capture-at', '29295', '33860', '34420', '--pause-at', str(START),
            '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        harness.ct, sys.stdin, sys.argv = old_ct, old_stdin, old_argv
        stream.close()
        for trace in attached:
            trace.close()
    trace, = attached
    trace.save()
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    main()
