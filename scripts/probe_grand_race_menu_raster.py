"""Lock the derived menu label rasterizer and separate it from image painting."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_menu_image_accessor import OWNER, execute, execute_raster_dispatch
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_wireless_return import check_branch, resolve_pc_load, word


def main():
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned ROM differs')
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    if hashlib.sha256(sources[0]).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese source differs')
    spans = ((0x52600, 0x5269C), (0x1409D0, 0x140A34), (0x140AB0, 0x140B04),
             (0xACB10, 0xACBEC), (0xD5160, 0xD51AC), (0xD5404, 0xD5814),
             (0x521E8, 0x52228), (0x116438, 0x116448),
             (0xADFDC, 0xAE0F0), (0xD4914, 0xD4988),
             (0x163D8, 0x163E8), (0xAD734, 0xAD76C), (0xAD608, 0xAD638))
    locks = []
    for lo, hi in spans:
        if sources[1][lo:hi] != sources[2][lo:hi]:
            raise ValueError(f'Candidate raster source/context differs from canonical at {lo:#x}')
        differences = [offset for offset in range(lo, hi) if sources[0][offset] != sources[1][offset]]
        if differences and (lo != 0xD5404 or any(not (0xD5514 <= offset < 0xD556C or 0xD5804 <= offset < 0xD5808) for offset in differences)):
            raise ValueError(f'Unmapped clean/canonical raster difference at {lo:#x}')
        locks.append({'start': lo, 'end': hi,
                      'clean_sha256': hashlib.sha256(sources[0][lo:hi]).hexdigest(),
                      'canonical_candidate_sha256': hashlib.sha256(sources[1][lo:hi]).hexdigest(),
                      'inherited_changed_bytes': differences})
    source = sources[0]
    # Constructor installs the derived raster subobject at +0x10 and final
    # image access subobject at +0xAC. They are distinct native interfaces.
    resolve_pc_load(source, 0x5262C, 2, 0x52688)
    resolve_pc_load(source, 0x5260C, 2, 0x52678)
    if word(source, 0x52688) != 0x02140A10 or word(source, 0x52678) != 0x02140AC4:
        raise ValueError('Derived subobject vtable differs')
    if word(source, 0x140A30) != 0x020ACB10 or word(source, 0x140ACC) != 0x020163D8:
        raise ValueError('Rasterizer or final image accessor differs')
    for field, instruction in ((0x52638, 0xE5842010), (0x52618, 0xE58420AC),
                               (0xACB30, 0xE2840068), (0xACBA8, 0xE2841068)):
        if word(source, field) != instruction:
            raise ValueError('Native object text/subobject offset differs')
    check_branch(source, 0xACB54, 0xD5160)
    check_branch(source, 0xACB88, 0xD5340)
    check_branch(source, 0xACBC8, 0xD5404)
    check_branch(source, 0xAE0E4, 0xD4914)
    metrics = struct.unpack_from('<4I', source, 0x116438)
    if metrics != (0, 4, 6, 12):
        raise ValueError('Menu margin/glyph metrics differ')
    accessor_executions = []
    raster_dispatch = execute_raster_dispatch(sources[2])
    for state, normal, selected, expected in ((0, 0, 0, OWNER + 0x10),
                                             (0, OWNER + 0x2000, OWNER + 0x3000, OWNER + 0x2000),
                                             (2, OWNER + 0x2000, OWNER + 0x3000, OWNER + 0x3000),
                                             (2, OWNER + 0x2000, 0, OWNER + 0x2000)):
        result = execute(sources[2], state=state, normal=normal, selected=selected)
        if result['returned_image_pointer'] != expected:
            raise ValueError('Actual image accessor owner/selection differs')
        accessor_executions.append(result)
    report = {'status': 'research-derived-menu-raster-path-locked', 'rom_written': False,
              'source_locks': locks, 'label_buffer_offset': 0x68,
              'raster_subobject_offset': 0x10, 'raster_vtable': 0x140A10,
              'raster_method_slot': 0x20, 'rasterizer': 0xACB10,
              'text_context_constructor': 0xD5160,
              'label_draw_branches': {'aligned': 0xD5340, 'centered': 0xD5404},
              'image_access_subobject_offset': 0xAC, 'image_accessor': 0x163D8,
              'bounded_image_accessor_executions': accessor_executions,
              'bounded_owner_raster_dispatch': raster_dispatch,
              'primary_owner_raster_slot': 0x4C,
              'metrics': {'horizontal_margin': 0, 'vertical_margin': 4,
                          'ascii_width': 6, 'line_height': 12},
              'limitations': ['Static interface/source proof, not live graphics execution.',
                              'Canonical D5404 includes inherited LF/cursor changes; candidate preserves them exactly, and their menu behavior is not yet verified.',
                              'Raster callback owner is verified; caller activation, active alignment/context flags and complete screen geometry need verification.',
                              'Final supplied graphics context remains to be mapped; it is not the label font renderer.',
                              'Native D5404 character dispatch/context must be verified for these labels before integration.']}
    output = Path('work/analysis/grand_race_menu_raster')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Derived label rasterizer, buffer, native draw branches and metrics locked; integration/runtime pending')


if __name__ == '__main__':
    main()
