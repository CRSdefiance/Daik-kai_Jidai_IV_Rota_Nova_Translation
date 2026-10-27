"""Research native portrait geometry and monthly tribute glyph/pixel preservation."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_common_native_word_wrap import execute as word_wrap
from scripts.probe_common_tribute_modal_pixels import verify


def geometry(source):
    machine = machine_for(source)
    machine.emu_start(BASE + 0x5408C, BASE + 0x540C8, count=1000)
    machine.emu_start(BASE + 0x54174, BASE + 0x5419C, count=1000)
    rect = list(struct.unpack('<4I', machine.mem_read(STACK + 0x34, 16)))
    if rect != [0, 96, 256, 192]:
        raise ValueError('Native portrait viewport differs from mapped lower-screen rectangle')
    window = 0x02426000
    machine.reg_write(UC_ARM_REG_R0, window)
    machine.emu_start(BASE + 0x54DB0, STOP, count=10000)
    fields = list(struct.unpack('<4I', machine.mem_read(window + 0x40, 16)))
    if fields != [8, 16, 0, 0] or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native portrait constructor fields or return differ')
    return {'native_viewport_rect': rect, 'native_constructor_fields_40_through_4c': fields,
            'client_size': [256, 96], 'bitmap_origin_and_physical_routing_are_contracts': True}


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    prepared = json.loads(Path('work/analysis/common_monthly_tribute_preparation_proof.json').read_text(encoding='utf-8'))
    unique = {(c['message_id'], c['amount']): c['complete_prepared_text'] for c in prepared['cases']
              if c['amount'] in (999999, 42949672)}
    cases, wrapped_cases = [], []
    for (message, amount), text in unique.items():
        for mode in (4, 16):
            native = verify(source, font, text, mode, portrait=True)
            content = [event for event in native['glyph_events'] if event['code'] != 32]
            cursor, splits = 0, []
            for word in text.split():
                rows = sorted({e['y'] for e in content[cursor:cursor + len(word)]})
                if len(rows) > 1:
                    splits.append({'word': word, 'row_origins': rows})
                cursor += len(word)
            cases.append({'message_id': message, 'amount': amount, 'mode': mode,
                          'complete_prepared_text': text, 'pixels_sha256': sha(native['pixels']),
                          'full_glyph_order_and_independent_pixels_match': True,
                          'split_words': splits, 'formatting_approved': False})
            wrapped = word_wrap(source, text)
            protected = verify(source, font, wrapped, mode, portrait=True, guarded=True)
            content = [event for event in protected['glyph_events'] if event['code'] != 32]
            cursor = 0
            for word in text.split():
                if len({e['y'] for e in content[cursor:cursor + len(word)]}) != 1:
                    raise ValueError('Native guarded monthly portrait splits a word or amount')
                cursor += len(word)
            wrapped_cases.append({'message_id': message, 'amount': amount, 'mode': mode,
                                  'native_wrapped_text': wrapped, 'pixels_sha256': sha(protected['pixels']),
                                  'whole_words_and_amounts_preserved': True,
                                  'formatting_approved': False})
    report = {'status': 'native-monthly-portrait-pixels-pass-layout-review-pending',
              'geometry': geometry(source), 'cases': cases, 'native_word_wrapped_cases': wrapped_cases,
              'limitations': 'Native geometry arithmetic, constructor, ARM word helper and shared 548A8 text raster execute across separate invocations. Parent bitmap origin, client setup, portrait image composition, input and physical routing remain contracts. Monthly runtime helper connection and visual review remain pending; these results do not approve formatting.'}
    Path('work/analysis/common_monthly_tribute_pixels_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native monthly portrait pixel cases pass; {sum(bool(c["split_words"]) for c in cases)} cases split words.')
    print(f'{len(wrapped_cases)} ARM-word-wrapped portrait pixel cases preserve whole words and amounts.')


if __name__ == '__main__':
    main()
