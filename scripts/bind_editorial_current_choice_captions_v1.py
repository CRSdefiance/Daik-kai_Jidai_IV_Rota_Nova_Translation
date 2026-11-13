"""Bind sealed typed captions by complete source/current command and index, without message lookup."""
import argparse
import re
import struct
from pathlib import Path
from dk4tool.dialogue.reviewed_choice_object_v2 import labels, count_and_base
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['current', 'sealed', 'out']:
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    current, sealed = map(load, [args.current, args.sealed])
    assert sealed['source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake']
    rows = []
    for row in sealed['records']:
        if row['kind'] != 'typed-choice-label':
            continue
        assert row['earlier_English_unconsulted']
        group = next(g for g in current['groups'] if g['block'] == row['block'])
        mapping = next(c for c in group['command_map'] if c['source_offset'] == row['source_command_offset'])
        source, raw = map(bytes.fromhex, [mapping['source_hex'], mapping['current_hex']])
        assert source.hex() == row['source_choice_object_hex']
        assert mapping['word'] in (0x2100, 0x2200) and source[:2] == raw[:2] == struct.pack('<H', mapping['word'])
        values = labels(raw)
        count, base = count_and_base(raw)
        index = row['source_index']
        assert count == row['source_count'] and 0 <= index < count
        offset = mapping['current_offset']+base+struct.unpack_from('<H', raw, 2+index*2)[0]
        rows.append({**row, 'current_reference':dict(file_path=current['file_path'], block=row['block'],
            command_offset=mapping['current_offset'], offset=offset, source_index=index, length=len(values[index])),
            'current_hex':values[index].hex(), 'current_choice_object_hex':raw.hex(),
            'current_English':values[index].decode('cp932'), 'current_English_now_exposed':True,
            'earlier_English_unconsulted':False, 'source_meaning_anddraft_precede_old_English_comparison':True,
            'native_choice_provider_not_run_as_message_catalogue':True})
    expected = [r for r in sealed['records'] if r['kind'] == 'typed-choice-label']
    assert len(rows) == len(expected) and len({r['id'] for r in rows}) == len(rows)
    non_ascii = []
    for group in current['groups']:
        for row in group['records']:
            text = row['current_effective_text']
            characters = [dict(index=i, character=c, codepoint=f'U+{ord(c):04X}') for i,c in enumerate(text) if ord(c)>127]
            if characters:
                non_ascii.append(dict(id=row['id'], current_reference=row['current_reference'], current_hex=row['current_hex'],
                    current_effective_hex=row['current_effective_hex'], characters=characters,
                    current_equals_clean_Japanese=' '.join(text.split()) == ' '.join(row['source_Japanese'].split()),
                    contains_Japanese_script=bool(re.search('[\u3040-\u30ff\u3400-\u9fff]', text)),
                    per_record_editorial_andconsumer_review_required=True))
    save(args.out, dict(choices=rows, choice_count=len(rows), current_non_ASCII_findings=non_ascii,
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
        exact_current_command_mapping_used=True, typed_captions_not_sent_through_speech_catalogue=True,
        no_automatic_unicode_normalization_orfont_approval=True, new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.current,args.sealed,Path(__file__)]}))
    print(dict(bound_captions=len(rows), speech_records_with_non_ASCII=len(non_ascii), new_credit=0))
    for row in rows:
        print(row['id'], repr(row['current_English']))
    for row in non_ascii:
        print(row['id'], 'unchanged Japanese' if row['current_equals_clean_Japanese'] else repr(''.join(c['character'] for c in row['characters'])))


if __name__ == '__main__':
    main()
