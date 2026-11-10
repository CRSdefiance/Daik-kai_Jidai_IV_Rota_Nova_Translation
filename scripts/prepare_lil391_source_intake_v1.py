"""Qualify the existing SC2 census against current credit and select391 clean-only objects."""
from collections import Counter
from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil391_residual_A_clean_20261110')
CENSUS = Path('work/story_source_coverage_20261109_SC2_v2/coverage.json')
PACKET = CENSUS.with_name('residual_clean_source_packet.json')
RELEASE = Path('work/maria315_B286_B302_release_v1/registered_release_verification.json')
BLOCKS = list(range(20)) + [21, 115] + list(range(235, 243))


def main():
    assert not ROOT.exists()
    census, packet, release = map(load, [CENSUS, PACKET, RELEASE])
    ledgerpath = Path('translations/editorial_review_current_v1.json')
    ledger = load(ledgerpath)
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert packet['source_only_not_current_English'] and packet['file_path'] == '/data/SC2.DK4'
    assert digest(packet['source_ROM']) == packet['source_ROM_sha256'] == census['source_ROM_sha256']
    clean = NdsImage.open(packet['source_ROM'])
    archive = clean.read_file(packet['file_path'])
    assert sha(archive) == packet['source_archive_sha256'] == census['source_archive_sha256']
    assert sha(clean.read_file('/__arm9__.bin')) == packet['source_ARM9_sha256']
    blocks = IlnkContainer.parse(archive).blocks
    positions = set()
    for row in census['records']:
        ref = row['source_reference']
        raw = bytes.fromhex(row['source_hex'])
        assert blocks[row['block']][ref['offset']:ref['offset']+len(raw)] == raw
        key = (row['block'], ref['offset'], row['source_hex'])
        assert key not in positions
        positions.add(key)
        assert row['covered'] == bool(row['exact_credited_source_bindings'])
        assert not row['covered'] or len(row['exact_credited_source_bindings']) == 1
    assert len(positions) == 6720 and len(census['missing']) == packet['records'] == 1805
    credits = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
        if r['file_path'] == packet['file_path']}
    matched = {(packet['file_path'], b['id']) for r in census['records'] for b in r['exact_credited_source_bindings']}
    assert credits == matched and len(credits) == 4915
    for path, expected in census['source_packets'].items():
        assert digest(path) == expected, path
    assert digest(census['release']) == census['release_sha256']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    assert digest(release['candidate']) == release['candidate_sha256']
    old = load(census['release'])
    assert digest(old['candidate']) == old['candidate_sha256']
    # Byte comparison only: no current story text is decoded or exposed here.
    current_archive = NdsImage.open(release['candidate']).read_file(packet['file_path'])
    assert current_archive == NdsImage.open(old['candidate']).read_file(packet['file_path'])
    selected = deepcopy([g for g in packet['groups'] if g['block'] in BLOCKS])
    assert [g['block'] for g in selected] == BLOCKS and len(selected) == 30
    keys = []
    for group in selected:
        block = blocks[group['block']]
        assert bytes.fromhex(group['clean_block_hex']) == block
        assert len(group['records']) == sum(r['block'] == group['block'] for r in census['records'])
        for command in group['all_source_commands']:
            at, size = command['offset'], command['native_extent']
            assert block[at:at+size].hex() == command['whole_command_hex']
        for row in group['records']:
            assert not row['covered'] and not row['exact_credited_source_bindings']
            assert not row['existing_key_without_exact_source_binding']
            keys.append((row['file_path'], row['id']))
    assert len(keys) == len(set(keys)) == 391 and not set(keys) & credits
    ROOT.mkdir()
    out = ROOT/'clean_source_packet.json'
    save(out, dict(packet, groups=selected, records=391, selected_blocks=BLOCKS, complete_exchanges=30,
        complete_native_inventory_reused_not_rerun=True,
        original_census=str(CENSUS), original_census_sha256=digest(CENSUS),
        source_only_not_current_English=True, new_credit=0))
    counts = Counter(r['kind'] for g in selected for r in g['records'])
    evidence = {str(p): digest(p) for p in [CENSUS, PACKET, RELEASE, ledgerpath, out, Path(__file__)]}
    save(ROOT/'source_selection_v1.json', dict(source_objects=391, complete_exchanges=30, consumer_counts=dict(counts),
        blocks=[dict(block=g['block'], records=len(g['records'])) for g in selected],
        all_exact_clean_source_positions_rechecked=True, exact_disjoint_credited_keys=True,
        full_existing_native_inventory_reused_without_reexecuting_decoder=True,
        source_census_positions_checked=6720, exact_current_SC2_credit_bindings=4915, residual_objects=1805,
        current_SC2_archive_byte_identical_to_census_release=True, current_SC2_archive_sha256=sha(current_archive),
        source_packets_hashes_qualified_without_reading_prior_dialogue=True,
        stale_whole_ledger_hash_replaced_by_exact_current_archive_credit_set_comparison=True,
        no_meanings_drafts_orlocalization_approval_yet=True, no_current_English_read_orapproval=True,
        all_five_review_gates_pending=True, registered_parent=release['candidate'],
        registered_parent_sha256=release['candidate_sha256'], evidence=evidence, new_credit=0, full_goal_complete=False))
    print(dict(source_objects=391, complete_exchanges=30, consumers=dict(counts),
        prior_SC2_credit_exact=4915, source_inventory_not_replayed=True, current_English_not_exposed=True, new_credit=0))


if __name__ == '__main__':
    main()
