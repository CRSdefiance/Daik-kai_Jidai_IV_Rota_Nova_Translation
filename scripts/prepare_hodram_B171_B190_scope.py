"""Inventory clean compound menus and exclude previously completed exact record keys."""
import struct
from pathlib import Path
from dk4tool.dialogue.reviewed_two_choice_object_v1 import labels
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')


if __name__ == '__main__':
    output = ROOT / 'clean_intake_scope_v1.json'
    assert not output.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    ledger_path = Path('translations/editorial_review_current_v1.json')
    packet, ledger = load(packet_path), load(ledger_path)
    completed = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    rows, objects, controls = [], [], []
    for group in packet['groups']:
        block = bytes.fromhex(group['clean_block_hex'])
        for command in group['all_source_commands']:
            if command['word'] == 0x2000:
                assert command['native_extent'] == 2 and command['whole_command_hex'] == '0020'
                controls.append(dict(block=group['block'], offset=command['offset'], hex='0020', label_free=True))
            if command['word'] not in (0x2100, 0x2200, 0x4100):
                continue
            assert command['word'] == 0x2100
            raw = bytes.fromhex(command['whole_command_hex'])
            offsets = struct.unpack_from('<2H', raw, 2)
            values = labels(raw)
            obj = dict(block=group['block'], source_command_offset=command['offset'], word=command['word'],
                source_object_hex=raw.hex(), records=[])
            for index, value in enumerate(values):
                at = command['offset'] + 6 + offsets[index]
                assert block[at:at + len(value) + 1] == value + b'\0'
                row = dict(id=f'SC1_B{group["block"]}_CHOICE_{command["offset"]}_{index}',
                    file_path=packet['file_path'], block=group['block'], kind='typed-choice-label',
                    source_index=index, source_count=2, source_command_offset=command['offset'],
                    source_choice_object_hex=raw.hex(), source_hex=value.hex(), source_Japanese=value.decode('cp932'),
                    source_reference=dict(file_path=packet['file_path'], block=group['block'], offset=at,
                        record_index=block[:at].count(b'\0'), length=len(value)),
                    source_meaning=['Choose to hear the offered sailing-ship lecture.', 'Decline the offered lecture.'][index],
                    exchange_context='Complete B171 lecture offer,expert-companion refusal andfull willing-listener lesson.',
                    no_prior_English_orlocalized_caption_draft=True)
                rows.append(row)
                obj['records'].append(row)
            objects.append(obj)
    speeches = [r for g in packet['groups'] for r in g['records']]
    assert len(speeches) == 433 and len(objects) == 1 and len(rows) == 2 and rows[0]['block'] == 171
    assert [r['source_Japanese'] for r in rows] == ['聞こう', 'いや、いい']
    overlap = [r['id'] for r in speeches + rows if (r['file_path'], r['id']) in completed]
    assert not overlap, overlap
    save(ROOT / 'clean_choice_objects.json', dict(source_packet=str(packet_path),
        source_packet_sha256=sha(packet_path.read_bytes()), records=rows, objects=objects,
        source_caption_meanings_saved=2, complete_choice_objects=1, no_current_English_exposure=True, new_credit=0))
    meanings_path = ROOT / 'B171_B172_clean_meanings_before_English.json'
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        ordinary_speeches=433, typed_choice_objects=1, typed_caption_records=2, physical_style_objects=0,
        total_editorial_objects=435, source_meanings_saved=93, ordinary_meanings_saved=91, caption_meanings_saved=2,
        remaining_ordinary_meanings=342, remaining_caption_meanings=0,
        source_meaning_parts=[dict(path=str(meanings_path), sha256=sha(meanings_path.read_bytes()))],
        source_2000_label_free_controls=controls, zero_source_decode_errors=all(r['source_decode_error'] is None for r in speeches),
        source_speaker_selectors=sorted({r['source_selector'] for r in speeches}),
        already_completed_exclusion_keys=overlap, exact_completed_record_keys_checked=len(completed),
        completed_ledger_at_intake_sha256=sha(ledger_path.read_bytes()), no_current_English_dialogue_exposure=True,
        no_new_English_drafts_orcontextual_comparisons=True, native_identity_terms_anddisplay_gates_pending=True,
        completed_records_unchanged=ledger['records_editorially_completed'],
        new_credit=0, full_goal_complete=False, guide_photos=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Next435 objects:433 speeches+two captions;93 clean meanings saved;342 ordinary meanings pending;zero completed overlaps.')
