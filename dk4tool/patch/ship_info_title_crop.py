"""Fit complete Ship Info/Refit headings in the original shared bitmap view."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'b846e39d42a0d7bded3607c672f94cf251f8d63892cf9444a02b6805713fcc29'
START, END = 0x133024, 0x133240
TABLE = 0x114D3C
OLD_RECT = (-1, 104, 2, 0, 36, 48, 12)
NEW_RECT = (-1, 95, 2, 0, 36, 66, 12)


def transform(source, plan):
    if sha(source) != SOURCE or sha(source[START:END]) != 'cb26f49e179a6c8abd5804a7de737db7483ea89e4cffd4fbfd62ae585a5bab0d':
        raise ValueError('Shared title crop requires the exact complete V627 ARM9/pool')
    if struct.unpack_from('<7i', source, TABLE) != OLD_RECT:
        raise ValueError('Original shared title crop differs')
    owners, refs = plan['owners'], plan['references']
    if len(owners) != 31 or len(refs) != 31:
        raise ValueError('Require all31 original Deck owners and references')
    expected = {(r['field'], r['pointer']) for r in refs}
    actual = {(at, word) for at in range(len(source) - 3)
              if 0x02000000 + START <= (word := struct.unpack_from('<I', source, at)[0]) < 0x02000000 + END}
    if actual != expected:
        raise ValueError('Deck pool has an unreviewed pointer or alias')
    result, packed, moves = bytearray(source), bytearray(), []
    old_end = START
    for row in owners:
        at, text = row['offset'], row['text']
        encoded = text.encode('cp932') + b'\0'
        if at != old_end or source[at:at + len(encoded)] != encoded:
            raise ValueError('Deck owner identity or source text differs')
        old_end = (at + len(encoded) + 3) & ~3
        if any(source[at + len(encoded):old_end]):
            raise ValueError('Nonzero Deck owner padding')
        replacement = '   Refit   ' if text == 'Refit' else text
        new_at = START + len(packed)
        raw = replacement.encode('cp932') + b'\0'
        packed.extend(raw)
        packed.extend(bytes(-len(packed) % 4))
        moves.append({'old': at, 'new': new_at, 'old_text': text, 'text': replacement})
    if old_end != END - 4 or len(packed) != END - START or any(source[old_end:END]):
        raise ValueError('Require the reviewed four terminal padding bytes, no growth')
    if sum(m['old_text'] != m['text'] for m in moves) != 1:
        raise ValueError('Only Refit UI centering spaces may change')
    result[START:END] = packed
    mapped = {0x02000000 + m['old']: 0x02000000 + m['new'] for m in moves}
    for row in refs:
        struct.pack_into('<I', result, row['field'], mapped[row['pointer']])
    struct.pack_into('<7i', result, TABLE, *NEW_RECT)
    restored = bytearray(result)
    restored[START:END] = source[START:END]
    restored[TABLE:TABLE + 28] = source[TABLE:TABLE + 28]
    for row in refs:
        at = row['field']
        restored[at:at + 4] = source[at:at + 4]
    if bytes(restored) != source:
        raise ValueError('Unowned ARM9 change')
    before, after = MainCodeFile(source, 0x02000000), MainCodeFile(bytes(result), 0x02000000)
    if [(s.ramAddress, len(s.data)) for s in before.sections] != [(s.ramAddress, len(s.data)) for s in after.sections]:
        raise ValueError('Section shape changed')
    if any(a.data != b.data for a, b in zip(before.sections[1:], after.sections[1:], strict=True)):
        raise ValueError('Staged payload/ITCM/startup data changed')
    return bytes(result), {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
                           'old_title_crop': OLD_RECT, 'new_title_crop': NEW_RECT,
                           'complete_31_owner_mapping': moves, 'all31_reference_fields': refs,
                           'uses_exact4_terminal_padding_bytes_no_section_or_pool_growth': True,
                           'all_prose_and_UI_meanings_preserved_only_Refit_centering_spaces_added': True,
                           'all_other_ARM9_bytes_exact': True,
                           'changed_records': ['SHIP_INFO_SHARED_TITLE_CROP_AND_COMPLETE_REFIT_CENTERING']}


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-ship-info-title-crop-v1' or config.get('status') != 'reviewed-native-previews-experimental':
        raise ValueError('Reviewed source/native title configuration required')
    result, proof = transform(source, config['plan'])
    if proof['target_arm9_sha256'] != config['target_arm9_sha256']:
        raise ValueError('Target title crop differs from reviewed preview')
    return result, proof
