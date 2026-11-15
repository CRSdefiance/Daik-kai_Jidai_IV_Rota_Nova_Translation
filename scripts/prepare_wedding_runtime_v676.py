"""Bind original block/selector/factory entry observation and native host controls."""

import struct
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import factory_filter_controls_v674 as controls
from scripts.inspect_committed_gpu_v646 import CORE
from scripts.inspect_graphic_paints_v669 import units
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.research_wedding_command_v676 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    source = read('work/analysis/maria_opening_v674/source_contract.json')
    source['targets'] = source['targets'][:3]
    raw = CORE.read_bytes()
    imagebase, table = tables(raw)
    for pc, name in ((0x02024134, 'original_CS_block_loader_arguments_only'),
                     (0x02028A28, 'original_chapter_movie_selector_arguments_only'),
                     (0x020D2B1C, 'original_FLS_factory_arguments_only')):
        words = [next(data[pc - base:pc - base + 4] for base, data in units(image)
                      if base <= pc < base + len(data)) for image in (rom, clean)]
        assert words[0] == words[1]
        word = int.from_bytes(words[0], 'little')
        index = (word >> 16 & 0xFF0) | (word >> 4 & 15)
        handler = struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - imagebase
        assert index in (0x921, 0x927, 0x92F) and handler == 0x513F0
        source['targets'].append({'PC': pc, 'name': name, 'original_instruction': word,
                                  'instruction_index': index, 'handler_RVA': handler})
    source['additional_FLS_entry_first12_fields_only'] = True
    source['additional_CS_loader_and_chapter_selector_first12_fields_only'] = True
    save(ROOT / 'source_contract.json', source)
    for target in source['targets'][3:]:
        local = ROOT / ('controls_' + target['name'])
        local.mkdir(exist_ok=True)
        value = deepcopy(source)
        value['targets'] = source['targets'][:3] + [target]
        save(local / 'source_contract.json', value)
        controls.ROOT = local
        result = controls.factory_controls()
        save(local / 'native_host_controls.json', result)
    inputs = Path(read('work/analysis/route_opening_movies_v647/run_configs.json')['lil']['inputs'])
    save(ROOT / 'ordinary_inputs.json', read(inputs))
    save(ROOT / 'runtime_contract.json', {'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'inputs_sha256': sha((ROOT / 'ordinary_inputs.json').read_bytes()),
        'input_source': str(inputs), 'input_source_sha256': sha(inputs.read_bytes()),
        'ordinary_Lil_New_Game_no_save_or_gameplay_fixture': True,
        'capture_frames': [2000, 2200, 2300, 2400, 2600, 2800, 3000, 3400, 4000],
        'frames': 4000, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V676 source-pinned entries and39 native host controls prepared.', flush=True)


if __name__ == '__main__':
    main()
