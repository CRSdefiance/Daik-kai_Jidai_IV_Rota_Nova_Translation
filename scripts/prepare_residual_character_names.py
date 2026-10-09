"""Translate both remaining ordinary given names from source-owned spans."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.inventory_arm9_text import components
from scripts.probe_fleet_name_display_callers import execute

SOURCE = '30ae21c22c5f2d1e42a986331aa52a0df6e9d69fcf6a8f9d195726e751f4ea66'
NAMES = [(61, 0x15C1E8, 'ヴェルス', 'Vels'), (77, 0x15C7D0, 'アカブー', 'Akaboo')]


def prepare():
    image = NdsImage.open('out/all_routes_combined_v149_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if sha(source) != SOURCE or sha(clean) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731':
        raise ValueError('Exact V149 and clean Japanese required')
    references = []
    for name, _, raw in components(image):
        for field in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, field)[0] - BASE
            for index, at, _, _ in NAMES:
                if at <= pointer < at + 12:
                    references.append((name, field, pointer, index))
    if references != [('arm9', 0x121320, 0x15C1E8, 61), ('arm9', 0x121520, 0x15C7D0, 77)]:
        raise ValueError('Residual names have unclassified owner/interior references')
    saved = bytearray(source)
    for index, at, japanese, english in NAMES:
        expected = japanese.encode('cp932').ljust(12, b'\0')
        if source[at:at + 12] != expected or clean[at:at + 12] != expected:
            raise ValueError('Source Japanese given-name owner differs')
        saved[at:at + 12] = (english.encode('ascii') + b'\0').ljust(12, b'\0')
    restored = bytearray(saved)
    for _, at, _, _ in NAMES:
        restored[at:at + 12] = source[at:at + 12]
    if restored != source:
        raise ValueError('Residual names change unrelated bytes')
    return source, bytes(saved), references


def loaded(source):
    machine = machine_for(source)
    machine.mem_map(0x01FF0000, 0x10000)

    def cache(uc, address, size, _):
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    hook = machine.hook_add(UC_HOOK_CODE, cache)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    machine.hook_del(hook)
    machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    return machine


def main():
    source, saved, references = prepare()
    before, after = loaded(source), loaded(saved)
    names, rows = [], []
    replacements = {index: english for index, _, _, english in NAMES}
    for index in range(207):
        old, new = ordinary_getter(source, index, before), ordinary_getter(saved, index, after)
        original = bytes(before.mem_read(old, 128)).split(b'\0', 1)[0].decode('cp932')
        text = bytes(after.mem_read(new, 128)).split(b'\0', 1)[0].decode('cp932')
        japanese = any('\u3040' <= c <= '\u30ff' or '\u3400' <= c <= '\u9fff'
                       or '\uff66' <= c <= '\uff9f' for c in text)
        if old != new or text != replacements.get(index, original) or japanese or not all(c.isprintable() for c in text):
            raise ValueError(f'Native given-name preservation or complete English coverage differs: {index=}, {original=}, {text=}, {old=}, {new=}')
        names.append({'index': index, 'text': text, 'pointer': new})
    for index, at, japanese, english in NAMES:
        rows.append({'id': f'ORDINARY_GIVEN_NAME_{index}', 'offset': at, 'capacity': 12,
                     'source_hex': source[at:at + 12].hex(), 'japanese': japanese,
                     'english': english + '{PAD}', 'speaker': 'Ordinary character nameplate',
                     'context': f'Native ordinary-name table index {index}; immutable given-name getter selects the source-owned label.',
                     'source_meaning': 'The character name ' + japanese + '.',
                     'localization_note': ('Established Raphael story spelling Vels.' if index == 61 else
                                           'Phonetic project spelling Akaboo retains the source long final vowel; no official Latin spelling claimed.'),
                     'review': {'source': True, 'context': True, 'localization': True,
                                'naturalness': True, 'formatting': False}})
    manuscript = {'format': 'dk4-arm9-prompt-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                  'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': rows}
    Path('translations/residual_character_names_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    font = NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    fleet = [execute(saved, kind, '', raster=True, kanji_font=font, captain_index=index)[0]
             for kind in ('fixed', 'centered') for index in replacements]
    proof = {'status': 'pass-complete-ordinary-name-getters-paired-pixels-pending',
             'source_sha256': SOURCE, 'research_sha256': sha(saved), 'references': references,
             'native_given_names': names, 'fleet_rasters': fleet,
             'all_207_ordinary_given_names_printable_without_japanese': True,
             'preserved_non_ascii_latin_names': [r for r in names if not r['text'].isascii()],
             'candidate_changed': False,
             'limits': ['Ordinary constructor/type and fleet eligibility remain fixtures.',
                        'Paired native pixels and other display consumers remain pending.',
                        'Japanese-script coverage does not prove semantic fidelity or formatting of every older English role label; inherited full-width Latin is preserved.',
                        'Physical gameplay and canonical acceptance are not claimed.']}
    Path('work/analysis/residual_character_names_arm9.bin').write_bytes(saved)
    Path('work/analysis/residual_character_names_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Both residual names translated; all 207 ordinary getter strings preserved without Japanese script; inherited full-width Latin retained; four fleet rasters pass.')


if __name__ == '__main__':
    main()
