"""Rebind the previous wrap queue to the current four native story archives."""

from hashlib import sha256
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from scripts import register_visible_gallery_captions_v1 as baseline
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches


base = baseline.base
HISTORY = next(Path('work/analysis/completed_contraction_wrap_leads_v7831').glob('*with_live_storage_refs.json'))
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/historical_wrap_leads_current_v1.json')


def main():
    assert not OUTPUT.exists()
    old = base.load(HISTORY)
    assert old['lead_count'] == len(old['leads']) == 13
    release = base.load(baseline.RELEASE)
    assert base.digest(baseline.CLEAN) == release['clean_input_sha256']
    assert base.digest(baseline.ROM) == release['candidate_sha256']
    images = [base.NdsImage.open(path) for path in (baseline.CLEAN, baseline.ROM)]
    arms = [image.read_file(baseline.ARM) for image in images]
    paths = {row['file_path'] for row in old['leads']}
    banks = [{route: IlnkContainer.parse(image.read_file(route)) for route in paths} for image in images]
    inventory, _, _ = scoped_inventory()
    groups, rows = {}, []
    for lead in old['leads']:
        path, block = lead['file_path'], lead['block']
        if (path, block) not in groups:
            source, current = [bank[path].blocks[block] for bank in banks]
            (clean_commands, clean_speeches), (commands, speeches) = [
                raw_speeches(arm, blob, inventory) for arm, blob in zip(arms, (source, current), strict=True)]
            assert [row['word'] for row in clean_commands] == [row['word'] for row in commands]
            assert [row['complete_preamble_hex'] for row in clean_speeches] == [row['complete_preamble_hex'] for row in speeches]
            groups[path, block] = clean_speeches, speeches, sha256(source).hexdigest(), sha256(current).hexdigest()
        clean_speeches, speeches, source_sha, current_sha = groups[path, block]
        index = next(i for i, row in enumerate(clean_speeches) if row['offset'] == lead['source_reference']['offset'])
        source, current = clean_speeches[index], speeches[index]
        assert source['raw_hex'] == lead['source_reference']['raw_hex']
        current_body = bytes.fromhex(current['raw_hex'])[1:].decode('cp932')
        integrated = lead['id'] == 'DK4_MES_B218_R0027' and path == '/data/SC2.DK4'
        if integrated:
            assert [row.strip() for row in current_body.splitlines()] == ["(Ian's interested?", "That's a surprise.)"]
        else:
            assert current['raw_hex'] == lead['current_reference']['raw_hex']
        rows.append(dict(id=lead['id'], file_path=path, block=block, source_block_sha256=source_sha,
            current_block_sha256=current_sha, source_reference=source, current_reference=current,
            source_Japanese=bytes.fromhex(source['raw_hex'])[1:].decode('cp932'), current_stored_English=current_body,
            disposition='prior correction still present' if integrated else 'recorded split remains in native storage',
            further_contextual_and_consumer_review=not integrated))
    assert sum(row['further_contextual_and_consumer_review'] for row in rows) == 12
    base.save(OUTPUT, dict(current_ROM_sha256=release['candidate_sha256'], clean_ROM_sha256=release['clean_input_sha256'],
        history=str(HISTORY), history_sha256=base.digest(HISTORY), records=rows,
        scope='Typed command order and every speech preamble matched in each sampled block. This is a storage inventory, not a gameplay or effective catalogue test.',
        new_dialogue_credit=0, full_goal_complete=False))
    print('Rebound all 13 historical wraps. One prior repair remains present and 12 stored splits need contextual follow-up.')


if __name__ == '__main__':
    main()
