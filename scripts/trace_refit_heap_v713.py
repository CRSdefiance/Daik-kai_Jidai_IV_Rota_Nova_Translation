"""Observe actual Refit allocation/cleanup during ordinary navigation and exit."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_layout_v2 import CLEANUP, INIT_END, INIT_START
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble, main_read
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_room_gender_v694 import Observer as HostMethods
from scripts.probe_button_prompt_native import machine
from scripts.run_refit_display_v712 import ROM
from scripts.run_room_gender_v694 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v713')
FOLDER = CAP / 'refit_help_v713_heap_lifetime'


def prepare():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'producer_locks.json').exists()
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    base, table = tables(core)
    u = machine(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    targets = []
    for name, pc in (('layout_begin', 0x02000000 + INIT_START), ('native_new', 0x02005154),
                     ('layout_ready', 0x02000000 + INIT_END), ('cleanup_begin', CLEANUP),
                     ('native_delete', 0x02005180), ('cleanup_ready', CLEANUP + 40)):
        word = int.from_bytes(u.mem_read(pc, 4), 'little')
        index = word >> 16 & 0xFF0 | word >> 4 & 15
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table})
    old_root = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = old_root
    inputs = read('work/analysis/yard_selection_v705/full_inputs.json')
    inputs += [{'start': f, 'duration': 8, 'buttons': [b]} for f, b in
        ((19701, 'A'), (20001, 'B'), (20301, 'B'))]
    save(ROOT / 'inputs.json', inputs)
    pre = read('work/analysis/refit_help_v712/preflight.json')
    save(ROOT / 'preflight.json', {k: pre[k] for k in ('donor', 'donor_sha256')})
    paths = ('scripts/trace_refit_heap_v713.py', 'scripts/observe_file_requests_v681.py',
        str(ROOT / 'source_contract.json'), str(ROOT / 'inputs.json'), str(ROM),
        str(ROM.with_suffix('.manifest.json')), 'translations/release_stack.json')
    save(ROOT / 'producer_locks.json', {p: sha(Path(p).read_bytes()) for p in paths})
    print('V713 six actual allocation/cleanup entries pinned; original inputs plus explicit cancel/exit.', flush=True)


class Observer:
    install, close = HostMethods.install, HostMethods.close

    def __init__(self, core):
        self.folder = FOLDER / 'observer'
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm, self.md = self.image.anchor('DTCM', 1, 0x4000), self.image.anchor('MDTC', 4, 1)
        self.source = read(ROOT / 'source_contract.json')
        self.header = (ct.c_uint32 * 4)(0, 0, 0, 0)
        self.rows, self.errors, self.slots, self.closed = [], [], [], False
        kinds = {t['PC']: t['name'] for t in self.source['targets']}

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                v = struct.unpack('<32I', cpu)
                kind = kinds[v[2]]
                if kind == 'native_new' and v[18] != 0x02019F9C:
                    return
                if kind == 'native_delete' and v[18] != CLEANUP + 32:
                    return
                raw, dtcm, md = ct.string_at(self.wram, 0x400000), ct.string_at(self.dtcm, 0x4000), ct.string_at(self.md, 4)
                prefix = self.folder / f'{len(self.rows):03d}_{kind}_{frame:06d}'
                rp, dp = prefix.with_suffix('.RAM.bin'), prefix.with_suffix('.DTCM.bin')
                rp.write_bytes(raw)
                dp.write_bytes(dtcm)
                surface = v[8] if kind == 'cleanup_ready' else v[4] if kind == 'cleanup_begin' else v[9] + 16 if kind.startswith('layout_') else None
                fields = {}
                if surface is not None:
                    words = struct.unpack('<12I', main_read(raw, surface, 48))
                    fields = {'surface': surface, 'surface_words': list(words)}
                    if words[4]:
                        h = struct.unpack('<5I', main_read(raw, words[4], 20))
                        pixels = (words[4] + h[4]) & 0xFFFFFFFF
                        fields.update(header=words[4], header_words=list(h), pixels=pixels)
                        if kind in ('layout_ready', 'cleanup_begin'):
                            fields['whole9072_pixel_bytes_sha256'] = sha(main_read(raw, pixels, 9072))
                self.rows.append({'frame': frame, 'kind': kind, 'CPU128_hex': cpu.hex(),
                    'R0': v[4], 'LR': v[18], **fields,
                    'RAM': str(rp), 'RAM_sha256': sha(raw), 'DTCM': str(dp), 'DTCM_sha256': sha(dtcm)})
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert ct.string_at(self.dtcm, 0x4000) == dtcm and ct.string_at(self.md, 4) == md
                assert len(self.rows) <= 60
            except BaseException as exc:  # noqa: BLE001
                self.errors.append({'frame': frame, 'error': repr(exc)})
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        for index in sorted({t['instruction_index'] for t in self.source['targets']}):
            targets = [t for t in self.source['targets'] if t['instruction_index'] == index]
            slot = core._handle + self.source['interpreter_table']['RVA'] + index * 8
            original = self.image.qword(slot)
            assert all(original == core._handle + t['handler_RVA'] for t in targets)
            address = self.native.alloc(None, 4096, 0x3000, 0x04)
            code, asm = assemble(self.cpu, ct.addressof(self.header), ct.cast(self.callback, ct.c_void_p).value,
                original, targets, address)
            ct.memmove(address, code, len(code))
            old = ct.c_uint32()
            assert self.native.protect(address, 4096, 0x20, ct.byref(old))
            assert self.native.flush(self.native.process, address, len(code))
            self.slots.append({'slot': slot, 'original': original, 'address': address,
                'code_hex': code.hex(), 'assembly': asm})

    def next_frame(self, frame):
        self.header[0] = frame
        self.header[1] = int(frame >= 11800 and not self.errors)

    def save(self):
        assert self.closed
        save(self.folder / 'events.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'mismatches': self.header[3],
            'whole_CPU_WRAM_DTCM_and_configuration_unchanged': True,
            'all_host_slots_restored': True, 'filters': self.slots,
            'producer_sha256': sha(Path(__file__).read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare()
        return
    for path, digest in read(ROOT / 'producer_locks.json').items():
        assert sha(Path(path).read_bytes()) == digest
    pre = read(ROOT / 'preflight.json')
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert not FOLDER.exists()
    FOLDER.mkdir()
    loader, installed, frame = ct.CDLL, [], 0
    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core)
            observer.install()
            installed.append(observer)
            original = core.retro_run
            original.restype = None
            def run():
                nonlocal frame
                frame += 1
                observer.next_frame(frame)
                original()
            core.retro_run = run
        return core
    ct.CDLL = loaded
    frames = read('work/analysis/yard_selection_v705/capture_frames.json') + [20000, 20300, 20600]
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(FOLDER),
        '--frames', '20600', '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen',
        '--battery-save', pre['donor'], '--capture-every', '999999', '--capture-at', *map(str, frames),
        '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    assert frame == 20600
    print('V713 terminal original allocator/lifetime trace:', [(r['kind'], r['frame']) for r in installed[0].rows], flush=True)


if __name__ == '__main__':
    main()
