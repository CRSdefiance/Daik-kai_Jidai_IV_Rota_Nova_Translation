"""Count exact editorial credit against the clean story and native COMMON censuses."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
import re

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_figurehead_navigation_gift_advice_v1 as candidate


SOURCE_PACKET = Path('translations/editorial_checkpoints/SharedText_20261110_v1'
                     '/contextual_comparison_pending_consumers.json')
COMMON, ARM, HELP = '/COMMON/MESFILE.DK4', '/__arm9__.bin', '/COMMON/HELP.DK4'
JAPANESE = re.compile(r'[\u3041-\u3096\u30a1-\u30fa\u3400-\u9fff\uff66-\uff9f]')


def check_story(read, digest, clean, keys):
    result = []
    for item in read(SOURCE_PACKET)['all_four_native_story_censuses']:
        assert digest(item['path']) == item['sha256']
        census = read(item['path'])
        assert not any(census[key] for key in ('missing', 'inventory_failures', 'legacy_source_bindings_not_exact'))
        records = census['records']
        file = records[0]['file_path']
        assert sha256(clean.read_file(file)).hexdigest() == census['source_archive_sha256']
        assert len(records) == len({row['id'] for row in records}) == item['native_objects']
        credited = {record_id for path, record_id in keys if path == file}
        exact = set()
        aliases = 0
        for row in records:
            assert row['file_path'] == file and row['covered'] and not row['existing_key_without_exact_source_binding']
            possible = {binding['id'] for binding in row['exact_credited_source_bindings']
                        if binding['block'] == row['source_reference']['block']
                        and binding['offset'] == row['source_reference']['offset']
                        and binding['source_hex'] == row['source_hex'] and binding['id'] in credited}
            assert possible, (file, row['id'])
            exact.update(possible)
            aliases += row['id'] not in possible
        assert len(records) == len(credited) == len(exact) and exact == credited
        result.append(dict(path=file, source_objects=len(records), credited_objects=len(credited),
            uncredited_objects=0, historical_ID_bindings=aliases, census_path=item['path'],
            census_sha256=item['sha256'], kinds=census['object_counts']))
    return result


def check_common(clean, current, keys):
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    arm = current.read_file(ARM)
    latest = owned_entries(current.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    assert len(source) == len(latest) == 3668
    assert all(row.message_id == other.message_id == number
               for number, (row, other) in enumerate(zip(source, latest, strict=True)))
    reviewed = {record_id for path, record_id in keys if path == COMMON}
    assert reviewed <= {f'COMMON_MESSAGE_{row.message_id}' for row in source}
    pending = [row.message_id for row in source if f'COMMON_MESSAGE_{row.message_id}' not in reviewed]
    assert len(set(range(3181, 3251)) & set(pending)) == 70
    assert not set(range(2815, 3181)) & set(pending)
    by_block = Counter(source[number].block for number in pending)
    text = {number: latest[number].text.decode('cp932', errors='replace') for number in pending}
    japanese = [number for number, content in text.items() if JAPANESE.search(content)]
    replacements = [number for number, content in text.items() if '\ufffd' in content]
    return dict(total=len(source), credited=len(reviewed), pending=len(pending), pending_item_advice=70,
        pending_other_keys=len(pending) - 70, pending_with_Japanese_characters_in_current_storage=len(japanese),
        pending_decode_replacement_keys=replacements, pending_by_block=dict(sorted(by_block.items())),
        pending_ids=pending, pending_with_Japanese_characters_ids=japanese,
        scope='Native message keys include conditional, legacy and potentially non-player-facing entries. '
              'Japanese character detection is a stored-text lead.')


def main():
    read, digest = candidate.stage.load, candidate.stage.digest
    ledger, release = map(read, (candidate.base.LEDGER, candidate.RELEASE))
    keys = Counter((row['file_path'], row['id'])
                   for row in ledger[candidate.base.CONTEXT]['integrated_record_keys'])
    assert len(keys) == ledger['records_editorially_completed'] == 26899 and set(keys.values()) == {1}
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    clean_path = candidate.stage.review.CLEAN
    assert digest(release['candidate']) == release['candidate_sha256'] and digest(clean_path) == release['clean_input_sha256']
    current = candidate.stage.NdsImage.open(release['candidate'])
    clean = candidate.stage.NdsImage.open(clean_path)
    story = check_story(read, digest, clean, keys)
    story_count = sum(row['source_objects'] for row in story)
    assert story_count == 24092
    common = check_common(clean, current, keys)
    help_credited = {record_id for path, record_id in keys if path == HELP}
    assert help_credited == {f'HELP_TOPIC_{number}' for number in range(202)}
    scope = dict(candidate_sha256=release['candidate_sha256'], coverage_ledger=candidate.base.LEDGER.as_posix(),
        ledger_sha256=digest(candidate.base.LEDGER), completed_reviews=ledger['records_editorially_completed'],
        revised_records=ledger['records_revised_and_integrated'], justified_retentions=ledger['retained_wordings_editorially_completed'],
        source_census_packet=SOURCE_PACKET.as_posix(), source_census_packet_sha256=digest(SOURCE_PACKET),
        story_archives=story, typed_story_positions_reviewed=story_count, source_help_topics_credited=len(help_credited),
        shared_native_COMMON=common,
        remaining_unquantified='Player-facing ARM9 and other resource prose, retrospective name and role consistency, '
                               'earlier wrapping and glyph defects, and practical town and random-scene coverage.',
        separate_work='Deferred graphics artwork and the later older-record technical re-audit.',
        whole_game_percent_established=False, full_goal_complete=False)
    target = candidate.VERIFICATION / 'editorial_remaining_scope.json'
    assert not target.exists()
    candidate.base.save(target, scope)
    print(f"Story {story_count}, Help {len(help_credited)}, COMMON {common['credited']} credited and "
          f"{common['pending']} pending, including {common['pending_item_advice']} item advice. "
          f"Stored Japanese-character leads {common['pending_with_Japanese_characters_in_current_storage']}.")


if __name__ == '__main__':
    main()
