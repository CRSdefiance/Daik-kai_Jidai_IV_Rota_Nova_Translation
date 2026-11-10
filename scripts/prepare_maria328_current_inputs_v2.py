"""Enrich exact census references with original command-owned style/menu metadata."""
import struct
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text


def enrich(row, source):
    group = next(g for g in source['groups'] if g['block'] == row['block'])
    block = bytes.fromhex(group['clean_block_hex'])
    ref = row['source_reference']
    at, raw = ref['offset'], bytes.fromhex(row['source_hex'])
    assert block[at:at+len(raw)] == raw
    command = next(c for c in group['all_source_commands'] if c['offset'] == ref['command_offset'])
    whole = bytes.fromhex(command['whole_command_hex'])
    assert block[command['offset']:command['offset']+len(whole)] == whole
    row['source_record_index'] = block[:at].count(b'\0')
    row['source_macros'] = {t:len(re.findall(t,row['source_Japanese'])) for t in ['FI','FA','FO','FU']}
    row['source_command_offset'] = command['offset']
    row['source_word'] = command['word']
    if row['kind'] == 'physical-style-alternative':
        assert command['word'] == 0x4100
        offsets = list(struct.unpack_from('<8H',whole,2))
        indices = [i for i,v in enumerate(offsets) if command['offset']+20+v == at]
        assert indices and all(whole[20+offsets[i]:whole.index(0,20+offsets[i])] == raw for i in indices)
        row.update(source_header_hex=whole[:20].hex(), source_style_indices=indices,
            source_style_offsets=offsets, source_selector=whole[19])
    elif row['kind'] == 'typed-menu-caption':
        assert command['word'] == 0x2200
        offsets = list(struct.unpack_from('<3H',whole,2))
        index = int(row['id'].rsplit('_',1)[1])
        assert index in range(3) and command['offset']+8+offsets[index] == at
        assert whole[8+offsets[index]:whole.index(0,8+offsets[index])] == raw
        row.update(source_index=index, source_count=3, source_choice_object_hex=whole.hex())
    else:
        assert command['word'] == 0x4000 and row['kind'] == 'ordinary-speech'
        assert whole[:6].hex() == row['source_complete_preamble_hex']
    return row


source = checked_text(Path('scripts/prepare_maria328_current_inputs_v1.py').read_text(encoding='utf-8'), {
    "ROOT/'current_inputs_v1'": "ROOT/'current_inputs_v2'",
    "    out.mkdir()\n    sealed": "    out.mkdir()\n    source=deepcopy(source)\n    source['original_selected_packet']=str(source_path)\n    source['original_selected_packet_sha256']=digest(source_path)\n    for g in source['groups']:g['clean_block_sha256']=sha(bytes.fromhex(g['clean_block_hex']))\n    source_path=out/'source_packet.json'\n    save(source_path,source)\n    sealed",
    '        row = deepcopy(original)': '        row = enrich(deepcopy(original),source)',
    "row['kind'] == '4100-style-alternative'": "row['kind'] == 'physical-style-alternative'",
    "row['kind'] == 'typed-choice-label'": "row['kind'] == 'typed-menu-caption'",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-projection-exact-native-command-owned-metadata', 'exec'), globals())
