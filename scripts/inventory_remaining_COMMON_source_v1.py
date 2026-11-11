"""Preserve every remaining COMMON source key, including punctuation-only messages."""

import gzip
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_shared_text_source_v1 import reference


ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
SOURCE = ROOT / 'remaining_COMMON_source_catalog.json.gz'
SUMMARY = ROOT / 'remaining_COMMON_source_summary.json'


def main():
    assert not SOURCE.exists() and not SUMMARY.exists()
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = load(ledger_path)
    keys = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    clean = NdsImage.open('work/clean.nds')
    rows = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    source_rows = []
    for number, row in enumerate(rows):
        ident = f'COMMON_MESSAGE_{number}'
        if ('/COMMON/MESFILE.DK4', ident) in keys:
            continue
        text = row.text.decode('cp932')
        source_rows.append(dict(id=ident, message_ID=number, file_path='/COMMON/MESFILE.DK4',
            source_reference=reference(row), source_hex=row.text.hex(), clean_Japanese=text,
            Japanese_character_detection_diagnostic_only=contains_japanese(text),
            consumer_andwhole_exchange_classification_pending=True, new_credit=0))
    assert len(rows) == 3668 and len(source_rows) == 2068
    other = [r['message_ID'] for r in source_rows if not r['Japanese_character_detection_diagnostic_only']]
    assert other == [97, 469, 2196]
    initial = load(ROOT / 'clean_source_packet.json')
    assert {r['message_ID'] for r in initial['records']} <= {r['message_ID'] for r in source_rows}
    document = dict(source_ROM='work/clean.nds', source_ROM_sha256=digest('work/clean.nds'),
        records=source_rows, native_message_count=3668, individually_credited_COMMON_keys=1600,
        native_COMMON_keys_without_completed_contextual_credit=2068,
        decoding_is_not_reachability_orplayer_facing_classification=True,
        no_original_source_key_dropped_based_on_Japanese_detection=True,
        full_ROM_prose_denominator_not_established=True, no_new_source_prose_orcompletion_credit=True,
        evidence={str(p):digest(p) for p in [ledger_path, Path(__file__)]}, full_goal_complete=False)
    raw = (json.dumps(document, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    SOURCE.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    assert gzip.decompress(SOURCE.read_bytes()) == raw
    supplements = []
    for number, english, note in [
        (97, '%s leveled up!', 'The named person gains a level. Normalize the full-width Latin level-up lettering through the validated text consumer. Confirm the entity argument before final approval.'),
        (469, '?', 'A question reaction. Keep the exact source object and its surrounding sea-event branch in scope. Punctuation alone does not make the message non-player-facing.'),
        (2196, '...?', 'A hesitant or puzzled reaction. Read it with the adjacent idle-crew responses and original speaker dispatch before final approval.'),
    ]:
        row = rows[number]
        supplements.append(dict(message_ID=number, id=f'COMMON_MESSAGE_{number}',
            source_reference=reference(row), source_hex=row.text.hex(), clean_Japanese=row.text.decode('cp932'),
            independent_English=english, source_meaning_andcontext_note=note,
            current_English_not_extracted_for_this_supplement=True, all_five_review_gates_pending=True, new_credit=0))
    save(SUMMARY, dict(source_catalog=str(SOURCE), source_catalog_sha256=digest(SOURCE),
        uncompressed_source_sha256=__import__('hashlib').sha256(raw).hexdigest(), native_messages=3668,
        existing_individual_COMMON_credits=1600, remaining_native_COMMON_keys=2068,
        source_Japanese_character_leads=2065, other_source_keys_preserved=other,
        supplementary_source_first_drafts=supplements, initial_clean_source_drafts=54,
        initial_current_comparisons=54, supplementary_clean_source_drafts=3,
        font_glyph_andpunctuation_only_objects_in_scope=True,
        all_four_story_censuses_reused=True, all_source_consumer_display_andrelease_requirements_preserved=True,
        source_prose_orcompletion_credit_added=0, full_goal_complete=False))
    print('Preserved all 2068 uncredited COMMON source keys and three additional source-first drafts.')


if __name__ == '__main__':
    main()
