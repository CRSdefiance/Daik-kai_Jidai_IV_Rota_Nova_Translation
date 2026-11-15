"""Bind real script-modal entries/returns so a cached cursor alone is not proof."""

import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as controls
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.run_opening_holds_v686 import CLEAN, CURRENT, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    assert not (ROOT / 'wait_source_contract.json').exists()
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (CLEAN, CURRENT)]
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    targets = []
    for pc, name in ((0x02054E44, 'modal_entry'), (0x0202A218, 'script_wait_return')):
        at = pc - 0x02000000
        assert arms[0][at:at + 4] == arms[1][at:at + 4]
        word = struct.unpack_from('<I', arms[1], at)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    source = {'targets': targets, 'interpreter_table': table, 'core_sha256': CORE_SHA,
        'original_assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'chapter_sha256': {name: sha(IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC3.DK4')).blocks[33])
                           for name, p in (('source', CLEAN), ('current', CURRENT))}}
    save(ROOT / 'wait_source_contract.json', source)
    # The existing bounded native-prefix checker accepts an isolated target file.
    scratch = ROOT / 'wait_prefix_controls'
    scratch.mkdir()
    save(scratch / 'source_contract.json', source)
    old_root = controls.ROOT
    controls.ROOT = scratch
    try:
        controls.main()
    finally:
        controls.ROOT = old_root
    result = read(scratch / 'native_prefix_controls.json')
    assert len(result['native_host_cases']) == 10
    result['current_observer_sha256'] = sha(Path('scripts/observe_wait_entries_v686.py').read_bytes())
    save(ROOT / 'wait_native_prefix_controls.json', result)
    manifest = read(pre['source_unlock_manifest'])
    manifest.update(production_ROM=str(CURRENT), production_ROM_sha256=pre['candidate_sha256'])
    save(ROOT / 'current_unlock_manifest.json', manifest)
    print('V686 two actual script-modal targets and10 native-prefix controls bound.', flush=True)


if __name__ == '__main__':
    main()
