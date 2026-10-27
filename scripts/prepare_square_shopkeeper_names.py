"""Research complete Square Shopkeeper in two shared original name allocations."""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import BASE, STOP, machine_for
from scripts.inventory_arm9_text import components


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--joint', action='store_true', help='Layer onto the verified joint item/entity pool research.')
    args = parser.parse_args()
    image = NdsImage.open('out/all_routes_combined_v147_candidate.nds')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source_path = ('joint_name_runtime_pool_arm9.bin' if args.joint else 'entity_name_runtime_rebased_arm9.bin')
    proof_path = ('joint_name_runtime_pool_proof.json' if args.joint else 'entity_name_runtime_rebase_proof.json')
    source = Path('work/analysis', source_path).read_bytes()
    proof = json.loads(Path('work/analysis', proof_path).read_text(encoding='utf-8'))
    if sha(source) != proof['research_sha256' if args.joint else 'research_arm9_sha256']:
        raise ValueError('Exact runtime-rebased entity research required')
    start, end = 0x15D088, 0x15D0A0
    raw = '広場の店主'.encode('cp932') + b'\0\0'
    if source[start:end] != raw * 2 or clean[start:end] != raw * 2:
        raise ValueError('Both original complete square-shopkeeper owners required')
    refs = []
    for name, _, original in components(image):
        data = source if name == 'arm9' else original
        for p in range(len(data) - 3):
            target = struct.unpack_from('<I', data, p)[0] - BASE
            if start <= target < end:
                refs.append({'component': name, 'field': p, 'target': target})
    if (not refs or any(r['component'] != 'arm9' or r['target'] not in (start, start + 12)
                        or start <= r['field'] < end for r in refs)):
        raise ValueError('Square-shopkeeper ownership has unclassified interior references')
    english = 'Square Shopkeeper'
    saved = bytearray(source)
    saved[start:end] = (english.encode('ascii') + b'\0').ljust(24, b'\0')
    for ref in refs:
        struct.pack_into('<I', saved, ref['field'], BASE + start)
    saved = bytes(saved)
    restored = bytearray(saved)
    restored[start:end] = source[start:end]
    for ref in refs:
        at = ref['field']
        restored[at:at + 4] = source[at:at + 4]
    if restored != source:
        raise ValueError('Square-shopkeeper repair changes unrelated research bytes')
    machine = machine_for(saved)
    machine.mem_map(0x01FF0000, 0x10000)
    deferred = []

    def startup(uc, address, size, _):
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            deferred.append(address)
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    handle = machine.hook_add(UC_HOOK_CODE, startup)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    machine.hook_del(handle)
    machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
    code = MainCodeFile(saved, BASE)
    bss_start, bss_end = struct.unpack_from('<2I', saved, code.codeSettingsOffs + 12)
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x8AC
            or bytes(machine.mem_read(bss_start, bss_end - bss_start)) != bytes(bss_end - bss_start)):
        raise ValueError('Square-shopkeeper native BSS preparation fails')
    cases = []
    previous = {r['index']: r['text'] if args.joint else r['complete_text']
                for r in proof['native_ordinary_given_names' if args.joint else 'native_given_name_cases']}
    for index in range(207):
        selected = ordinary_getter(saved, index, machine)
        text = bytes(machine.mem_read(selected, 128)).split(b'\0', 1)[0].decode('cp932')
        expected = english if index in (82, 83) else previous[index]
        if text != expected:
            raise ValueError('Native square-shopkeeper repair changes another given name')
        cases.append({'index': index, 'selected_pointer': selected, 'complete_text': text})
    inherited_names = []
    if args.joint:
        for move in proof['pointer_moves']:
            pointer = struct.unpack_from('<I', saved, move['field'])[0]
            text = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')
            if pointer != move['runtime_pointer'] or text != move['text']:
                raise ValueError('Shopkeeper integration changes inherited joint-pool name')
            inherited_names.append({'id': move['id'], 'pointer': pointer, 'text': text})
        section = MainCodeFile(saved, BASE).sections[2]
        if bytes(machine.mem_read(section.ramAddress, len(section.data))) != bytes(section.data):
            raise ValueError('Shopkeeper getters overwrite inherited joint DTCM storage')
    records = [{'id': f'SQUARE_SHOPKEEPER_{index}', 'offset': at, 'capacity': 12,
                'source_hex': clean[at:at + 12].hex().upper(), 'japanese': '広場の店主',
                'english': english + '{PAD}', 'speaker': 'Square shopkeeper nameplate',
                'context': 'Ordinary character table indices 82 and 83 select duplicate role names for the square shopkeeper through native 7EB0C/CDAB4. Source explicitly identifies the square location.',
                'source_meaning': 'The shopkeeper in the square.',
                'localization_note': 'Complete natural American English retains both location and role. Identical source labels share complete storage across their two original allocations; no authored breaks or abbreviation. Display layout and physical gameplay remain pending.',
                'review': {'source': True, 'context': True, 'localization': True,
                           'naturalness': True, 'formatting': False}}
               for index, at in ((82, start), (83, start + 12))]
    manuscript = {'format': 'dk4-arm9-prompt-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'encoder': 'dialogue-fixed-v1',
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': records}
    Path('translations/square_shopkeeper_names_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = {'status': 'pass-research-square-shopkeeper-source-sharing-native-getters-display-pending',
              'source_arm9_sha256': sha(source), 'research_arm9_sha256': sha(saved),
              'source_span': [start, end], 'complete_text': english, 'used_bytes': len(english) + 1,
              'owned_bytes': 24, 'references': refs, 'native_given_name_cases': cases,
              'joint_pool_composed': args.joint, 'inherited_joint_names_verified': inherited_names,
              'remaining_japanese_given_name_indices': [61, 77], 'candidate_changed': False,
              'limits': ['Actual startup copying/BSS clearing and ordinary getters execute; cache maintenance is contracted.',
                         'Runtime class/captain eligibility, nameplate layout and physical gameplay remain pending.',
                         'Other inherited wording/role names still need full source-fidelity review; no complete name-coverage claim.']}
    prefix = 'joint_square_shopkeeper' if args.joint else 'square_shopkeeper'
    Path(f'work/analysis/{prefix}_research_arm9.bin').write_bytes(saved)
    Path(f'work/analysis/{prefix}_native_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Complete Square Shopkeeper fits {len(english) + 1}/24 owned bytes; {len(refs)} references and all 207 native given-name selections pass.')


if __name__ == '__main__':
    main()
