"""Extend the frozen read-only room observer with actual mutable ITCM state."""

import argparse
import copy
import ctypes as ct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_room_gender_v694 as observer
from scripts import run_room_gender_v694 as runner
from scripts.observe_file_requests_v681 import assemble
from scripts.verify_village_wrap_v608 import read, save

ROOT = runner.ROOT / 'native_ITCM'


class WithITCM(observer.Observer):
    def __init__(self, core, folder):
        super().__init__(core, folder)
        self.original_callback = self.callback
        self.itcm = self.image.anchor('ITCM', 1, 0x8000)

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                itcm = ct.string_at(self.itcm, 0x8000)
                count = len(self.rows)
                self.original_callback(frame)
                if len(self.rows) > count:
                    assert len(self.rows) == count + 1
                    row = self.rows[-1]
                    assert bytes.fromhex(row['CPU128_hex']) == cpu
                    path = Path(row['RAM']).with_suffix('.ITCM.bin')
                    path.write_bytes(itcm)
                    row['ITCM'] = str(path)
                    row['ITCM_sha256'] = sha(itcm)
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.itcm, 0x8000) == itcm
            except BaseException as exc:  # noqa: BLE001 - never throw across native callbacks.
                self.errors.append({'frame': frame, 'ITCM_extension_error': repr(exc)})
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        # All slots are still uninstalled. Assemble the same validated native
        # prefixes with the extended callback, preserving the original observer.
        for row in self.slots:
            index = (row['slot'] - core._handle - self.source['interpreter_table']['RVA']) // 8
            targets = [t for t in self.source['targets'] if t['instruction_index'] == index]
            assert targets
            code, assembly = assemble(self.cpu, ct.addressof(self.header), ct.cast(self.callback, ct.c_void_p).value,
                                      row['original'], targets, row['address'])
            assert len(code) < 4096
            old = ct.c_uint32()
            assert self.native.protect(row['address'], 4096, 0x04, ct.byref(old))
            ct.memmove(row['address'], code, len(code))
            assert self.native.protect(row['address'], 4096, 0x20, ct.byref(old))
            assert self.native.flush(self.native.process, row['address'], len(code))
            row['code_hex'], row['assembly'] = code.hex(), assembly

    def save(self):
        super().save()
        path = self.folder / 'events.json'
        data = read(path)
        data['ITCM_extension_sha256'] = sha(Path(__file__).read_bytes())
        data['all_recorded_CPU_and_ITCM_state_preserved_by_extension'] = True
        save(path, data)


def prepare():
    ROOT.mkdir()
    original = read(runner.ROOT / 'preflight.json')
    for case, source in (('hodram', runner.ROOT), ('maria', runner.ROOT / 'selection')):
        folder = ROOT / case
        folder.mkdir()
        pre = copy.deepcopy(read(source / 'preflight.json'))
        pre['native_ITCM_extension_sha256'] = sha(Path(__file__).read_bytes())
        pre['initial_generic_RAM_only_replay_failure'] = 'The original buffered-text constructor reaches D54CC with a missing runtime ITCM dispatch-state model. Full captured ITCM is required; no source font or renderer call is skipped.'
        save(folder / 'preflight.json', pre)
        (folder / 'inputs.json').write_bytes((source / 'inputs.json').read_bytes())
        (folder / 'source_contract.json').write_bytes((runner.ROOT / 'source_contract.json').read_bytes())
    assert original['observer_sha256'] == sha(Path(observer.__file__).read_bytes())
    print('V694 frozen room observer plus read-only exact ITCM extension pinned.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('prepare', 'hodram', 'maria'))
    args = parser.parse_args()
    if args.case == 'prepare':
        prepare()
    else:
        folder = ROOT / args.case
        assert read(folder / 'preflight.json')['native_ITCM_extension_sha256'] == sha(Path(__file__).read_bytes())
        observer.ROOT, runner.ROOT, runner.Observer = folder, folder, WithITCM
        runner.run(args.case + '_ITCM', args.case, False)
