"""Extract complete original 2100/2200 menus; keep label-free 2000 controls separate."""
import argparse
import struct
from pathlib import Path

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    packet = load(args.packet)
    objects, rows, controls = [], [], []
    for group in packet['groups']:
        block = bytes.fromhex(group['clean_block_hex'])
        for command in group['all_source_commands']:
            word, at = command['word'], command['offset']
            if word == 0x2000:
                assert command['native_extent'] == 2 and command['whole_command_hex'] == '0020'
                controls.append(dict(block=group['block'], offset=at, word=word, source_hex='0020',
                                     label_free_two_byte_original_control=True, not_a_caption_object=True))
                continue
            if word not in [0x2100, 0x2200]:
                continue
            count = 2 if word == 0x2100 else 3
            raw = bytes.fromhex(command['whole_command_hex'])
            assert block[at:at + len(raw)] == raw and command['native_extent'] == len(raw)
            values = labels(raw)
            assert len(values) == count
            offsets = struct.unpack_from('<' + str(count) + 'H', raw, 2)
            members = []
            for index, value in enumerate(values):
                relative = 2 + 2 * count + offsets[index]
                where = at + relative
                assert raw[relative:relative + len(value) + 1] == value + b'\0'
                row = dict(id=f'SC{packet["route"]}_B{group["block"]}_CHOICE_{at}_{index}', file_path=packet['file_path'],
                    block=group['block'], kind='typed-choice-label', source_command_offset=at, source_index=index,
                    source_count=count, source_word=word, source_byte_offset=where, source_hex=value.hex(),
                    source_Japanese=value.decode('cp932'), source_choice_object_hex=raw.hex(),
                    source_reference=dict(file_path=packet['file_path'], block=group['block'], command_offset=at,
                                          source_index=index, offset=where, length=len(value)),
                    earlier_English_unconsulted=True, all_five_review_gates_pending=True, new_credit=0)
                rows.append(row)
                members.append(row['id'])
            objects.append(dict(block=group['block'], source_command_offset=at, source_word=word,
                                source_count=count, source_hex=raw.hex(), source_indices=list(range(count)), record_ids=members))
    save(args.out, dict(source_packet=str(args.packet), source_packet_sha256=sha(args.packet.read_bytes()),
        objects=objects, records=rows, object_count=len(objects), caption_count=len(rows), label_free2000_controls=controls,
        source_only_not_current_orlocalized_English=True, individual_meanings_andconsumer_qualification_pending=True,
        new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(menus=len(objects), captions=len(rows), preserved_label_free2000=len(controls), earlier_English_unconsulted=True))


if __name__ == '__main__':
    main()
