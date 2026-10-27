"""Capture the original Refit font consumer without modifying emulated state."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble, main_read
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_room_gender_v694 import Observer as HostMethods
from scripts.probe_button_prompt_native import machine
from scripts.run_room_gender_v694 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v708_candidate.nds')
ROOT = Path('work/analysis/refit_help_v709')
IDS = tuple(range(1247, 1256)) + tuple(range(1268, 1290))


def prepare():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'producer_locks.json').exists()
    old = read('work/analysis/refit_help_v708/preflight.json')
    old = {**old, 'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'), Path('work/clean.nds'),
            Path('out/raphael_natural_v2_accepted_base.nds'))}}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'preflight.json', {**{k: old[k] for k in ('candidate', 'candidate_sha256', 'release_hashes', 'donor', 'donor_sha256')},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V705 ordinary Sell/Refit and five source-bound wrap defects',
        'full_goal_complete': False})
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    pc = 0x020D5404
    words = [bytes(machine(arm).mem_read(pc, 4)) for arm in arms]
    assert words[0] == words[1]
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    base, table = tables(core)
    word = int.from_bytes(words[0], 'little')
    index = word >> 16 & 0xFF0 | word >> 4 & 15
    target = {'PC': pc, 'name': 'original_font_painter', 'word': word, 'instruction_index': index,
        'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - base}
    save(ROOT / 'source_contract.json', {'targets': [target], 'interpreter_table': table,
        'native_message_IDs': list(IDS), 'original_font_painter': pc})
    old_root = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = old_root
    save(ROOT / 'producer_locks.json', {p: sha(Path(p).read_bytes()) for p in (
        'scripts/trace_refit_text_v709.py', 'scripts/observe_file_requests_v681.py',
        str(ROOT / 'source_contract.json'), 'work/analysis/yard_selection_v705/full_inputs.json')})
    print('V709 original font entry and native host controls pinned.', flush=True)


class Observer:
    install, close = HostMethods.install, HostMethods.close

    def __init__(self, core, folder):
        self.folder = Path(folder) / 'observer'
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm, self.md = self.image.anchor('DTCM', 1, 0x4000), self.image.anchor('MDTC', 4, 1)
        self.source = read(ROOT / 'source_contract.json')
        self.header = (ct.c_uint32 * 4)(0, 0, 0, 0)
        self.rows, self.errors, self.slots, self.seen = [], [], [], set()
        self.closed = False
        rom = NdsImage.open(ROM)
        entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), clean=False)
        self.messages = {entries[i].text.rstrip(b' '): i for i in IDS}
        self.starts = {r['start'] for r in read('work/analysis/yard_selection_v705/full_inputs.json') if r['start'] >= 12801}

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                values = struct.unpack('<32I', cpu)
                pointer = values[5]
                if not 0x02000000 <= pointer <= 0x023FFEC0:
                    return
                text = ct.string_at(self.wram + pointer - 0x02000000, 320).split(b'\0')[0].rstrip(b' ')
                if text not in self.messages:
                    return
                message_id = self.messages[text]
                context = values[4]
                if not 0x02000000 <= context <= 0x023FFF80:
                    raise ValueError(f'Font context outside mapped main RAM: {context:#x}')
                bounds = struct.unpack('<4I', ct.string_at(self.wram + context - 0x02000000 + 4, 16))
                dimensions = struct.unpack('<2I', ct.string_at(self.wram + 0x312098 + 4, 8))
                key = (message_id, values[18], bounds, dimensions)
                if key in self.seen:
                    return
                self.seen.add(key)
                raw = ct.string_at(self.wram, 0x400000)
                dtcm, md = ct.string_at(self.dtcm, 0x4000), ct.string_at(self.md, 4)
                assert values[2] == 0x020D5404 and values[1] == self.source['targets'][0]['word']
                ctx = main_read(raw, values[4], 128)
                prefix = self.folder / f'message_{message_id}_{frame:06d}'
                ram_path, dtcm_path = prefix.with_suffix('.RAM.bin'), prefix.with_suffix('.DTCM.bin')
                ram_path.write_bytes(raw)
                dtcm_path.write_bytes(dtcm)
                self.rows.append({'frame': frame, 'message_id': message_id, 'CPU128_hex': cpu.hex(),
                    'R0_context': values[4], 'R1_text': pointer, 'LR': values[18], 'context128_hex': ctx.hex(),
                    'bounds': list(bounds), 'font_dimensions': list(dimensions),
                    'text_hex': text.hex(), 'RAM': str(ram_path), 'RAM_sha256': sha(raw),
                    'DTCM': str(dtcm_path), 'DTCM_sha256': sha(dtcm), 'MDTC_hex': md.hex()})
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert ct.string_at(self.dtcm, 0x4000) == dtcm and ct.string_at(self.md, 4) == md
            except BaseException as exc:  # noqa: BLE001 - never throw across the native callback.
                self.errors.append({'frame': frame, 'error': repr(exc)})
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        target = self.source['targets'][0]
        slot = core._handle + self.source['interpreter_table']['RVA'] + target['instruction_index'] * 8
        original = self.image.qword(slot)
        assert original == core._handle + target['handler_RVA']
        address = self.native.alloc(None, 4096, 0x3000, 0x04)
        code, assembly = assemble(self.cpu, ct.addressof(self.header), ct.cast(self.callback, ct.c_void_p).value,
            original, [target], address)
        ct.memmove(address, code, len(code))
        old = ct.c_uint32()
        assert self.native.protect(address, 4096, 0x20, ct.byref(old))
        assert self.native.flush(self.native.process, address, len(code))
        self.slots.append({'slot': slot, 'original': original, 'address': address, 'code_hex': code.hex(), 'assembly': assembly})

    def next_frame(self, frame):
        self.header[0] = frame
        self.header[1] = int(any(start <= frame < start + 40 for start in self.starts) and not self.errors)

    def save(self):
        assert self.closed and not self.errors and not self.header[3]
        save(self.folder / 'events.json', {'rows': self.rows, 'errors': self.errors, 'mismatches': self.header[3],
            'callbacks': self.header[2], 'all_host_slots_restored': True,
            'whole_selected_CPU_WRAM_DTCM_and_configuration_unchanged': True,
            'anchors': self.image.entries, 'filters': self.slots,
            'producer_sha256': sha(Path(__file__).read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare()
        return
    pre = read(ROOT / 'preflight.json')
    for path, digest in {**pre['release_hashes'], **read(ROOT / 'producer_locks.json')}.items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    folder = CAP / 'refit_help_v709_all_consumers'
    assert not folder.exists()
    folder.mkdir()
    loader, installed, frame = ct.CDLL, [], 0

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if not str(path).lower().endswith('desmume_libretro.dll'):
            return core
        observer = Observer(core, folder)
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
    captures = read('work/analysis/yard_selection_v705/capture_frames.json')
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', '19700', '--inputs-json', 'work/analysis/yard_selection_v705/full_inputs.json',
        '--touchscreen', '--battery-save', pre['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, captures), '--dump-capture-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    assert frame == 19700
    print('V709 terminal original font consumer trace', [r['message_id'] for r in installed[0].rows], flush=True)


if __name__ == '__main__':
    main()
