"""Find bounded ARM alpha-bit insertion leads, without inferring source consumers."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.run_room_gender_v694 import ROM
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opacity_paths_v704')


def immediate(word):
    value, shift = word & 255, ((word >> 8) & 15) * 2
    return ((value >> shift) | (value << ((32 - shift) & 31))) & 0xFFFFFFFF


def scan(parts):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    rows, constants = [], []
    for name, base, data in parts:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, at)[0]
            if word in (0x8000, 0x80008000):
                constants.append({'section': name, 'address': base + at, 'value': word})
            if word & 0x0E000000 != 0x02000000:
                continue
            opcode = word >> 21 & 15
            value = immediate(word)
            if opcode not in (1, 4, 12, 13) or value not in (0x8000, 0x80008000):
                continue
            here = next(decoder.disasm(data[at:at + 4], base + at, count=1), None)
            if here is None:
                continue
            window = []
            for offset in range(max(0, at - 32), min(len(data) - 3, at + 52), 4):
                ins = next(decoder.disasm(data[offset:offset + 4], base + offset, count=1), None)
                if ins:
                    window.append({'PC': ins.address, 'bytes': bytes(ins.bytes).hex(),
                        'mnemonic': ins.mnemonic, 'operands': ins.op_str})
            rows.append({'section': name, 'PC': base + at, 'word': word,
                'mnemonic': here.mnemonic, 'operands': here.op_str,
                'condition': word >> 28, 'immediate': value,
                'nearby_halfword_load': any(r['mnemonic'].startswith('ldrh') for r in window),
                'nearby_halfword_store': any(r['mnemonic'].startswith('strh') for r in window),
                'window': window, 'candidate_only_executability_and_pixel_import_not_established': True})
    return rows, constants


def main():
    ROOT.mkdir()
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V703 accepted raw16 caption/source control and source-bound bitmap bit15 behavior',
        'full_goal_complete': False})
    versions = {}
    for label, path in (('clean', Path('work/clean.nds')), ('current', ROM)):
        parts = sections(NdsImage.open(path))
        rows, constants = scan(parts)
        versions[label] = {'ROM': str(path), 'ROM_sha256': sha(path.read_bytes()), 'candidates': rows,
            'literal_mask_words_not_pointer_users': constants,
            'sections': [{'name': n, 'address': a, 'bytes': len(d), 'sha256': sha(d)} for n, a, d in parts]}
        print('V704', label, 'immediate leads', len(rows), 'near halfword load/store',
            [(hex(r['PC']), r['mnemonic'], r['operands']) for r in rows if r['nearby_halfword_load'] and r['nearby_halfword_store']], flush=True)
    save(ROOT / 'leads.json', {'versions': versions,
        'bounded_ARM_immediate_EOR_ADD_ORR_MOV_and_literal_mask_leads_only': True,
        'Thumb_register_masks_cross_function_dynamic_conversion_and_other_arithmetic_not_excluded': True,
        'analyzer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})


if __name__ == '__main__':
    main()
