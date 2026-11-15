"""Reconcile the remaining Online and scene label drafts with current storage and Gallery."""

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.gallery_caption_bounds import validate as gallery_captions
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_common_scene_caption_duplicates import captions as source_captions
from scripts import register_sound_bgm_titles_v1 as parent
from scripts import review_sound_bgm_titles_v1 as review


base, ARM, COMMON = parent.base, review.ARM, review.COMMON
ONLINE = Path('translations/common_online_promotional_manuscript_v2.json')
SCENES = Path('translations/common_scene_labels_manuscript_v1.json')
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/online_and_scene_consumer_comparison_v1.json')


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(review.CLEAN) == release['clean_input_sha256']
    clean, candidate = (base.NdsImage.open(p) for p in (review.CLEAN, parent.ROM))
    source_arm, arm = (rom.read_file(ARM) for rom in (clean, candidate))
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    directory = sha256(arm[review.DIRECTORY_OFFSET:review.TABLE_OFFSET]).hexdigest()
    current = review.owned_entries(candidate.read_file(COMMON), arm, directory)
    clean_titles = {(row['route_index'], row['index']): row for row in source_captions(source_arm)}
    duplicate = defaultdict(list)
    for current_title in gallery_captions(arm):
        source_title = clean_titles[current_title['route'], current_title['position']]
        assert current_title['field'] == source_title['pointer_field']
        duplicate[source_title['source_hex']].append(
            dict(route=current_title['route'], position=current_title['position'], field=current_title['field'],
                 source_pointer=source_title['offset'] + 0x02000000, source_hex=source_title['source_hex'],
                 current_pointer=current_title['pointer'], current_English=current_title['English'],
                 current_arrow_safe_bounds=current_title['bounds']))

    ledger = base.load(base.LEDGER)
    credited = {(row['file_path'], row['id']) for row in ledger[base.CONTEXT]['integrated_record_keys']}
    rows = []
    for path, ids, family in ((ONLINE, range(3289, 3320), 'online'), (SCENES, range(3393, 3607), 'scene')):
        drafts = base.load(path)['records']
        assert [row['message_id'] for row in drafts] == list(ids)
        for draft, n in zip(drafts, ids, strict=True):
            a, b = source[n], current[n]
            assert a.message_id == b.message_id == n
            assert a.text == bytes.fromhex(draft['source_hex']) and (COMMON, draft['id']) not in credited
            same_gallery = duplicate.get(a.text.hex(), [])
            rows.append(dict(message_ID=n, id=draft['id'], clean_reference=review.reference(a),
                current_reference=review.reference(b), clean_hex=a.text.hex(), current_hex=b.text.hex(),
                clean_Japanese=a.text.decode('cp932'), current_text=b.text.decode('cp932'), family=family,
                identical_to_clean_in_current_COMMON=a.text == b.text, independent_gallery_captions=same_gallery,
                existing_draft=str(path), existing_draft_English=draft['english'].removesuffix('{PAD}'),
                COMMON_consumer_classification='pending'))
    counts = Counter(row['family'] for row in rows)
    assert counts == {'online': 31, 'scene': 214}
    overlap = Counter(row['family'] for row in rows if row['independent_gallery_captions'])
    assert overlap == {'scene': 123}
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        source_draft_sha256={str(p): base.digest(p) for p in (ONLINE, SCENES)},
        exact_native_records=rows, counts=counts, current_equals_clean=sum(row['identical_to_clean_in_current_COMMON'] for row in rows),
        distinct_mapped_Gallery_titles=len(clean_titles), keys_with_exact_independent_Gallery_copy=overlap,
        records_with_new_editorial_credit=0,
        scope='Exact stored sources and independent Gallery title relationships. The separate COMMON display uses remain pending.'))
    print(f'Bound {len(rows)} exact pending COMMON records and {len(clean_titles)} arrow-safe current Gallery titles.')


if __name__ == '__main__':
    main()
