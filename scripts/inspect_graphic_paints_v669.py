"""Bind three original indexed-image primitives and their exact source assets."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/graphic_paints_v669')
ROM = Path('out/all_routes_combined_v666_candidate.nds')
TARGETS = ((0x01FF8E4C, 'scaled_copy'), (0x01FF92D8, 'corner_copy'), (0x01FFAE70, 'tiled_copy'))


def units(rom):
    return [(s.ramAddress, bytes(s.data)) for s in MainCodeFile(rom.read_file('/__arm9__.bin'), 0x02000000).sections] + [
        (o.ramAddress, bytes(o.data)) for o in loadOverlayTable(rom.rom.arm9OverlayTable,
            lambda _, fid: rom.rom.files[fid]).values()]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    if not (ROOT / 'preflight.json').exists():
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
                ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
                Path('out/raphael_natural_v2_accepted_base.nds'))},
            'previous_goal_turn_classification': 'progress: V668 actual resource entries/indirect source fields and archived three-run proof',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    current_units, original_units = units(rom), units(clean)
    targets = []
    for pc, name in TARGETS:
        code = next(d[pc - a:pc - a + 4] for a, d in current_units if a <= pc <= a + len(d) - 4)
        assert code == next(d[pc - a:pc - a + 4] for a, d in original_units if a <= pc <= a + len(d) - 4)
        word = int.from_bytes(code, 'little')
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        handler = struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base
        targets.append({'PC': pc, 'name': name, 'original_instruction': word,
                        'instruction_index': index, 'handler_RVA': handler})
    assert len({t['instruction_index'] for t in targets}) == 1
    assets = [{'path': p, 'bytes': len(rom.read_file(p)), 'sha256': sha(rom.read_file(p)),
               'header20_hex': rom.read_file(p)[:20].hex()} for p in
              ('/_pxl/__frame.pxl', '/_pxl/kakutei.pxl', '/_pxl/__marker.pxl')]
    save(ROOT / 'source_contract.json', {'core_sha256': CORE_SHA, 'interpreter_table': table,
        'targets': targets, 'source_assets': assets,
        'native_observation_and_full_source_comparison_not_yet_verified': True, 'full_goal_complete': False})
    print('V669 indexed-paint source entries:', targets, flush=True)


if __name__ == '__main__':
    main()
