"""Correct the remaining Christina spelling in Lil's recruitment exchange."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_ritual_officiant_labels_20261115 as parent
from scripts.audit_story_glyph_consistency import independent_pixels
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue, digest
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_release_baseline import files


base = parent.base
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
FILE = '/data/SC2.DK4'
COMMON = '/COMMON/MESFILE.DK4'
BLOCK, ORDINAL = 123, 2
ROOT = Path('work/cristina_recruitment_name_20261115_v1')
ROM = ROOT / 'Cristina_Recruitment_Name_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
BEFORE = "Yes! Let's bring Christina along."
AFTER = "Yes! Let's bring Cristina along."
REASONS = (
    ('Julio', 'Keep his quiet recollection as he thinks of someone who could join them.'),
    ('Lil', 'Keep the silent look of confusion before Julio explains what he has in mind.'),
    ('Julio', 'Use Cristina, the spelling on her nameplate. Keep his sudden enthusiasm and suggestion to bring her along.'),
    ('Lil', 'Keep her brief question. Julio has used the name without introducing her.'),
    ('Julio', 'Keep the source relationship and his proud remark about her skill with a sword. The two short beats answer Lil and then explain his suggestion.'),
    ('Lil', 'Keep the immediate practical question about where Cristina lives.'),
    ('Julio', 'Keep the direct answer. The next line supplies the decision to travel.'),
    ('Lil', 'Keep her ready agreement to go after hearing the destination.'),
)


def name_counts(image):
    counts = {}
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        blocks = IlnkContainer.parse(image.read_file(path)).blocks
        counts[path] = dict(blocks=len(blocks), Christina=sum(blob.lower().count(b'christina') for blob in blocks),
                            Cristina=sum(blob.lower().count(b'cristina') for blob in blocks))
    arm, common = [image.read_file(path) for path in (ARM, COMMON)]
    shared = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    assert len(shared) == 3668 and all(b'christina' not in row.text.lower() for row in shared)
    assert b'christina' not in arm.lower() and b'christina' not in image.read_file('/COMMON/HELP.DK4').lower()
    return counts


def plan(clean, current, manifest):
    source_arm, arm = [image.read_file(ARM) for image in (clean, current)]
    source, before = [IlnkContainer.parse(image.read_file(FILE)).blocks[BLOCK] for image in (clean, current)]
    inventory, _, _ = scoped_inventory()
    source_commands, source_rows = raw_speeches(source_arm, source, inventory)
    old_commands, old_rows = raw_speeches(arm, before, inventory)
    assert len(source_rows) == len(old_rows) == len(REASONS) == 8
    assert [row['word'] for row in source_commands] == [row['word'] for row in old_commands]
    assert [row['complete_preamble_hex'] for row in source_rows] == [row['complete_preamble_hex'] for row in old_rows]
    prior = old_rows[ORDINAL]
    offset = prior['offset'] + 1
    assert prior['selector'] == 6 and prior['record_index'] == 14 and source_rows[ORDINAL]['record_index'] == 13
    assert before[offset:offset + len(BEFORE) + 1] == BEFORE.encode('ascii') + b'\0'
    edited = AFTER.encode('ascii').ljust(len(BEFORE), b' ')
    after = before[:offset] + edited + before[offset + len(BEFORE):]
    all_commands, all_rows = raw_speeches(arm, after, inventory)
    assert all_rows[:ORDINAL] + all_rows[ORDINAL + 1:] == old_rows[:ORDINAL] + old_rows[ORDINAL + 1:]
    assert [tuple(row[k] for k in ('offset', 'word', 'native_extent', 'ancestor_0100_offsets')) for row in all_commands] == [
        tuple(row[k] for k in ('offset', 'word', 'native_extent', 'ancestor_0100_offsets')) for row in old_commands]
    assert after[:offset] + BEFORE.encode('ascii') + after[offset+len(edited):] == before
    memo = manifest['relocations'][ARM]['reviewed_name_integration']['catalog']
    archives = [IlnkContainer.parse(current.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)]
    assert len(memo['records']) == 467
    for banned in (bytes.fromhex(prior['raw_hex']), bytes.fromhex(all_rows[ORDINAL]['raw_hex'])):
        assert all(bytes.fromhex(row['key_hex']) + b'\0' not in (banned + b'\0', banned[1:] + b'\0')
                   for row in memo['records'] if row['route_mask'] & 4)
    # Validate the packed helper, lookup pointers and key bytes that the ROM actually uses.
    catalogue(arm, memo, archives)
    pixels = []
    for text in (BEFORE.encode('ascii'), edited):
        drawn, events, font = raster(arm, text)
        assert drawn == independent_pixels(arm, font, events)
        assert all(event['kind'] == 'ascii' and event['y'] == 0 and event['x'] + 6 <= 216 for event in events)
        assert ''.join(chr(event['code']) for event in events).rstrip() == text.decode('ascii').rstrip()
        pixels.append(dict(full_native_plane_sha256=digest(drawn), width=216, native_pages=1,
                           terminator_and_canaries_intact=True, complete_first_to_final_glyphs=True))
    rows = []
    for index, (source_row, previous_row, target_row, (speaker, reason)) in enumerate(zip(source_rows, old_rows, all_rows, REASONS, strict=True)):
        japanese = bytes.fromhex(source_row['raw_hex'])[1:].decode('cp932')
        before_english = bytes.fromhex(previous_row['raw_hex'])[1:].decode('ascii')
        english = bytes.fromhex(target_row['raw_hex'])[1:].decode('ascii')
        rows.append(dict(id=f"DK4_MES_B123_R{source_row['record_index']:04d}", source=source_row, current=previous_row,
                         target=target_row, Japanese=japanese, previous_English=before_english,
                         english=' '.join(english.split()), speaker=speaker, reason=reason,
                         decision='revision' if index == ORDINAL else 'retention'))
    assert 'クリスティナ' in rows[ORDINAL]['Japanese'] and rows[ORDINAL]['english'] == AFTER
    return after, dict(file=FILE, block=BLOCK, source_block_sha256=digest(source), previous_block_sha256=digest(before),
                       target_block_sha256=digest(after), all_eight_dialogue_records=rows, identical_command_extents=True,
                       all_source_selectors_preserved=True, single_trailing_storage_space=True,
                       literal_native_font_results=pixels, current_route_catalogue_keys_checked=len(memo['records']))


def main():
    assert not ROM.exists()
    receipt, manifest = map(base.load, (parent.RELEASE, parent.MANIFEST))
    assert base.digest(base.REGISTRY) == receipt['registry_sha256']
    assert base.digest(parent.ROM) == receipt['candidate_sha256'] == manifest['candidate_sha256']
    assert base.digest(parent.MANIFEST) == receipt['manifest_sha256']
    assert base.digest(CLEAN) == receipt['clean_input_sha256']
    clean, current = [base.NdsImage.open(path) for path in (CLEAN, parent.ROM)]
    counts_before = name_counts(current)
    assert sum(x['Christina'] for x in counts_before.values()) == counts_before[FILE]['Christina'] == 1
    before = files(current)
    revised, notes = plan(clean, current, manifest)
    blocks = IlnkContainer.parse(before[FILE]).blocks
    blocks[BLOCK] = revised
    current.replace_file(FILE, IlnkContainer(blocks).to_bytes())
    counts_after = name_counts(current)
    assert not any(x['Christina'] for x in counts_after.values()) and counts_after[FILE]['Cristina'] == counts_before[FILE]['Cristina'] + 1
    assert sum(x['blocks'] for x in counts_after.values()) == 1307
    assert {path for path, raw in files(current).items() if raw != before[path]} == {FILE}
    ROOT.mkdir(parents=True, exist_ok=True)
    current.save(ROM)
    current.replace_file(FILE, before[FILE])
    assert bytes(current.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, notes | dict(candidate_sha256=base.digest(ROM), previous_sha256=receipt['candidate_sha256'],
        previous_spelling_census=counts_before, target_spelling_census=counts_after, current_COMMON_keys_checked=3668,
        complete_NDS_inverse_exact=True, research_only=True))
    print('Staged one Cristina spelling correction. The other seven lines and all native command extents are exact.')


if __name__ == '__main__':
    main()
