"""Source-gate all direct wrapper modes and execute complete wrapper pixels."""

import hashlib
import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_scene_caption_raster import expected_pixels

CALLS = (0x42D54, 0x42D74, 0x42D94, 0x42FA4, 0x42FCC, 0x43008,
         0x441A0, 0x441C4, 0x441E8, 0x44230, 0x4473C, 0x44768)
# Mode stack store, expected instruction, definition of its source register.
MODES = ((0x42D50, 0xE58D6004, 0x42CD8, 0xE3A06001),
         (0x42D70, 0xE58D6004, 0x42CD8, 0xE3A06001),
         (0x42D90, 0xE58D6004, 0x42CD8, 0xE3A06001),
         (0x42FA0, 0xE58D6004, 0x42CD8, 0xE3A06001),
         (0x42FB8, 0xE58D6004, 0x42CD8, 0xE3A06001),
         (0x42FF0, 0xE58D5004, 0x42CD0, 0xE3A05000),
         (0x4419C, 0xE58D1004, 0x4418C, 0xE3A01001),
         (0x441B0, 0xE58D0004, 0x441AC, 0xE3A00001),
         (0x441D4, 0xE58D0004, 0x441D0, 0xE3A00001),
         (0x4422C, 0xE58D4004, 0x44218, 0xE3A04001),
         (0x44738, 0xE58D1004, 0x44728, 0xE3A01001),
         (0x4474C, 0xE58D1004, 0x44748, 0xE3A01001))


def validate_callers(source):
    found = []
    for offset in range(0, len(source) - 3, 4):
        word = struct.unpack_from('<I', source, offset)[0]
        if word >> 28 != 15 and word & 0x0F000000 == 0x0B000000:
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            if offset + 8 + delta * 4 == 0x456A0:
                found.append(offset)
    if tuple(found) != CALLS or struct.pack('<I', 0x020456A0) in source:
        raise ValueError('Unmapped direct/literal caption wrapper caller')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    # R6 is callee-preserved and defined once in this native viewer; R5 is
    # likewise zero throughout the call region. Inspect actual register writes.
    writes = {5: [], 6: []}
    for instruction in decoder.disasm(source[0x42CD0:0x4300C], 0x42CD0):
        _, changed = instruction.regs_access()
        for identity, offsets in writes.items():
            if any(instruction.reg_name(reg) == f'r{identity}' for reg in changed):
                offsets.append(instruction.address)
    if writes != {5: [0x42CD0], 6: [0x42CD8]}:
        raise ValueError('Caption viewer mode registers have another definition')
    rows = []
    for call, (store, word, definition, value) in zip(CALLS, MODES, strict=True):
        if struct.unpack_from('<I', source, store)[0] != word or struct.unpack_from('<I', source, definition)[0] != value:
            raise ValueError('Mapped wrapper mode producer/store differs')
        # Inherited stack arguments survive intervening callee-preserved calls.
        for instruction in decoder.disasm(source[store + 4:call], store + 4):
            if instruction.mnemonic.startswith('str') and '[sp, #4]' in instruction.op_str:
                raise ValueError('Wrapper mode argument is overwritten')
        rows.append({'call': call, 'store': store, 'definition': definition,
                     'mode': 0 if call == 0x43008 else 1})
    return rows


def main():
    digest = lambda data: hashlib.sha256(data).hexdigest()
    directory = Path('work/analysis/scene_caption_complete_scoped_raster_v137')
    source = (directory / 'proposed_arm9.bin').read_bytes()
    prior = json.loads((directory / 'report.json').read_text())
    if digest(source) != prior['proposed_arm9_sha256']:
        raise ValueError('Scoped raster proposal changed')
    callers = validate_callers(source)
    original = NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')
    if digest(original) != '13f89291781011e0835acc025870a0c748299075ea45e713c96bdc9676aae9ab':
        raise ValueError('Combined V137 wrapper reference changed')
    path = Path('translations/scene_caption_manuscript_v2.json')
    if digest(path.read_bytes()) != prior['manuscript_sha256']:
        raise ValueError('Full manuscript changed')
    cases = []
    for entry in json.loads(path.read_text(encoding='utf-8'))['records']:
        text = entry['english']
        x = 128 - len(text) * 5 // 2
        for mode in (4, 16):
            result = execute(source, text, x=x, mode=mode, wrapper=True, caller_mode=0)
            expected = [{'code': ord(c), 'style': 1, 'x': x + i * 5, 'y': 70} for i, c in enumerate(text)]
            if result['glyphs'] != expected or result['pixels'] != expected_pixels(source, text, x, 70, mode):
                raise ValueError('Complete native caption wrapper glyph/pixel result differs')
            if result['actual_tracking'] != 0xFFFFFFFF or result['clear_calls']:
                raise ValueError('Native caption wrapper mode or clear differs')
            cases.append({'id': entry['id'], 'mode': mode, 'pixels_sha256': digest(result['pixels']),
                          'glyph_count': len(text), 'native_cleanup_executed': 0xD5A58 in result['executed_offsets']})
    compatibility = []
    for text in ('Ironclad', 'Grand Race', 'Maria', 'A港町B', '港町'):
        for mode in (4, 16):
            for clear in (0, 1):
                before = execute(original, text, mode=mode, wrapper=True, caller_mode=1, clear=clear)
                after = execute(source, text, mode=mode, wrapper=True, caller_mode=1, clear=clear)
                for field in ('glyphs', 'cp932_glyphs', 'pixels', 'final_x', 'clear_calls'):
                    if before[field] != after[field]:
                        raise ValueError('Original mode-one wrapper behavior changed')
                compatibility.append({'text': text, 'mode': mode, 'clear': clear})
    report = {'status': 'pass-complete-native-caption-wrappers-and-inherited-compatibility',
              'proposed_arm9_sha256': digest(source), 'manuscript_sha256': digest(path.read_bytes()),
              'raster_proof_sha256': digest((directory / 'report.json').read_bytes()),
              'callers': callers, 'cases': cases, 'compatibility_cases': compatibility,
              'limitations': ['Native wrapper/init/render/ASCII pixels/cleanup execute; bitmap clear, origin and glyph copy are contracts.',
                             'Japanese ITCM painter is request-only; physical screen routing/gameplay remain pending.',
                             'Direct ARM/literal callers are gated; computed/Thumb/overlay caller ownership remains separate.']}
    output = Path('work/analysis/scene_caption_complete_wrapper_v137_proof.json')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(callers)} source-gated callers; {len(cases)} full native wrapper rasters; {len(compatibility)} inherited wrapper cases pass.')


if __name__ == '__main__':
    main()
