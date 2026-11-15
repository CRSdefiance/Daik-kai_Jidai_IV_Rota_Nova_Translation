"""Refresh clean-source scene-label drafts with current caption and artwork references."""

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_expedition_report_wraps_20261115 as current
from scripts.inventory_common_scene_caption_duplicates import captions
from scripts.seal_shared_text_source_v1 import reference


BASE = 0x02000000
ROUTING = Path('work/analysis/event_still_routing_v426/routing_proof.json')
SHEETS = Path('work/common_scene_label_art_20261115_v1')
GALLERY = Path('releases/all_routes_editorial_20261111_visible_gallery_captions_candidate/verification/registered_caption_review.json')
OLD = Path('translations/common_scene_labels_manuscript_v1.json')
OUTPUT = OLD.with_name('common_scene_labels_manuscript_v2.json')
SEQUENCE_EXTRAS = {3394, 3397, 3401, 3410, 3456, 3490, 3492, 3500, 3515}
REVISIONS = {
    3410: ('Rafael and a Moonlit Violin 1 (Large)', 'Use Rafael and match the companion Moonlit Violin 2 title while preserving the first large variant.'),
    3412: ('Rafael Playing, Up Close', 'In image 015 Rafael is playing his violin. The parallel Gallery title confirms the approved spelling and the close-up framing.'),
    3456: ('Lil and Camille Running', 'The Japanese names both runners. Use Camille, as in the following image of him worn out and Lil still full of energy.'),
    3462: ('Clifford Greets a Disappointed Lil', 'The stairs and figures in image 064 show the greeting. Keep Lil’s disappointment and express the welcome as Clifford’s action.'),
    3497: ("Maria's Party at the Grand Review", 'Image 097 is between the same two Maria scenes in both sequences. Gallery 3/35 has 総見式 in place of 総見算. Use the current Gallery wording for the group at the review.'),
    3537: ('Forest 03: Right Turn', 'Forest image 135 bends right, matching the parallel Jungle 03 label and image 149. The final full-width ｔ has no counterpart in that label or the scene direction. Preserve it in the source record.'),
    3572: ('Rafael and a Tomato', 'Use Rafael in the first of the two identical Japanese tomato labels.'),
    3580: ('A Knowing Look from Sera', 'The Japanese suggests that Sera’s expression carries a hint. Keep the implication open.'),
    3583: ('The Adversaries', 'The title identifies the opposing cast as a group and leaves their allegiance and individual names unstated.'),
    3589: ('Setting Sail', 'After the anchor and sail commands, the Japanese names the departure itself. Use a scene title for that action.'),
    3593: ('Rafael and a Tomato', 'Use the same title and approved spelling as the identical first tomato label.'),
    3601: ('Rafael: Name 1', 'Preserve the distinct first name-display label and use Rafael.'),
    3602: ('Rafael: Name 2', 'Preserve the second name-display label and use Rafael.'),
    3606: ('A Knowing Look from Sera 2', 'Match the title of Sera’s first suggestive look and retain the separate second variant.'),
}
REVISED_GLOSSES = {
    3410: 'Rafael and a violin under the moon, first large variant.',
    3412: 'Close-up of Rafael as he plays, with the violin explicit in the neighboring label and artwork.',
    3456: 'Lil and Camille running.',
    3462: 'Disappointed Lil and Clifford, who has come to greet her.',
    3497: 'Maria and the others at the review. The corresponding Gallery caption uses the regular word for the grand review ceremony.',
    3537: 'Forest 03, right turn, followed by an unexplained full-width t.',
    3572: 'Rafael and a tomato.',
    3580: 'Sera looks as though there is some meaning behind her expression.',
    3583: 'The group of opposing characters.',
    3589: 'Sailing out or departing by ship.',
    3593: 'Rafael and a tomato, repeated exactly in the source.',
    3601: 'Rafael name display, first variant.',
    3602: 'Rafael name display, second variant.',
    3606: 'Sera looks as though there is some meaning behind her expression, second variant.',
}
RETENTIONS = {
    3394: 'Preserve the distinct second port town and explicitly large version. The neighboring image 000 is labeled Port Town 1.',
    3397: 'Preserve the three unnamed people, the ship and the explicitly large version.',
    3401: 'Retain the established names of both figures without assigning either a title.',
    3438: 'Wounded is the source state. The wording keeps the scene focused on Hodram and matches the subject of image 041.',
    3480: 'Image 082 shows tulips stretching across the field. In Full Bloom carries the sense of abundance and retains the large variant.',
    3490: 'The Japanese simply names Maria and Clifford. Retain the neutral pairing and approved names.',
    3500: 'Appears captures Angelo’s entrance ahead of the separate fight and loss labels.',
    3515: 'Proud captures the self-satisfied interjection in Samwell’s standalone title.',
    3527: 'Image 125 shows the tavern interior. Tavern matches the established location wording.',
    3528: 'Image 126 shows the bed and desk of the inn room. Retain the source’s place label.',
    3529: 'Image 127 shows the working office. Office leaves the occupant unspecified.',
    3530: 'Image 128 shows the furnished reception room. Retain its function and the distinction from the office.',
    3531: 'Image 129 shows the first shipboard setting. Keep the specified deck and first variant.',
    3532: 'Image 130 shows the second shipboard setting. Preserve the separate deck variant.',
    3563: 'Image 161 is a cave interior following both cave entrance families. Shared Cave retains the common designation without specifying a route or destination.',
    3570: 'Final Scene identifies the closing part of the opening sequence and pairs with the second version.',
    3571: 'The title simply pairs the sea and sun. Keep both images in the original order.',
    3573: 'Keep the separate second version of the opening finale.',
    3574: 'Retain the first Hodram opening variant and the approved name.',
    3575: 'Retain Lil’s name and distinguish her first opening variant.',
    3576: 'Retain Lil’s name and the separate second variant.',
    3577: 'Calls at Port is natural nautical English. Preserve the slave ship and its arrival without identifying a port or allegiance.',
    3578: 'Peaceful preserves the pastoral mood and the contrast with the village attack in the next label.',
    3579: 'Keep the slave traders as the attackers and the village as the target.',
    3581: 'Keep Maria, the single rose and the first numbered variant.',
    3582: 'Keep Maria and the rose in the separately numbered second variant.',
    3584: 'Irene matches the registered Gallery spelling, and Study preserves the room named in the Japanese.',
    3585: 'Keep the object and variant number. The title leaves the knife’s owner and use unstated.',
    3586: 'Map carries the short object label without specifying a world map or specific region.',
    3587: 'Weigh Anchor preserves the direct nautical order and its timing before the sail command.',
    3588: 'Set the Sails preserves the command to raise and set sailcloth before the departure scene.',
    3590: 'Evening marks the separate time of day before Night.',
    3591: 'Night preserves the time of day and its distinction from Evening.',
    3592: 'Keep Hodram’s approved spelling and the second opening variant.',
    3594: 'Transition is natural for the connecting scene. Keep the full 1A identifier.',
    3595: 'The connecting scene has its own 1B variant; keep both parts of the identifier.',
    3596: 'Keep the 2A identifier to distinguish this transition from the first pair and 2B.',
    3597: 'Keep the 2B identifier to preserve the final transition variant.',
    3598: 'The first title label has no number in the source. Keep the short unnumbered form.',
    3599: 'The second title variant keeps the source number.',
    3600: 'The third title variant keeps the source number.',
    3603: 'Retain Hodram and the number of his first name-display entry.',
    3604: 'Retain Hodram and the separate second name-display entry.',
    3605: 'Retain Lil as the named character. The source gives this entry no variant number.',
}


def gallery_titles(source, target, routing, reviews):
    tables = []
    for proof in routing['Gallery_tables'][0]['routes']:
        route = proof['route']
        literal = 0x432DC + route * 8
        pointer, = unpack_from('<I', source, literal)
        assert pointer == proof['table_pointer']
        count = proof['count']
        at = pointer - BASE
        clean_indices = unpack_from(f'<{count}I', source, at)
        assert clean_indices == tuple(proof['image_indices'])
        assert target[literal:literal + 4] == source[literal:literal + 4]
        assert target[at:at + count * 4] == source[at:at + count * 4]
        tables.append(clean_indices)

    by_source, by_asset = defaultdict(list), defaultdict(list)
    for native, active, review in zip(captions(source), validate(target), reviews, strict=True):
        route, position = active['route'], active['position']
        assert (route, position) == (native['route_index'], native['index']) == (review['route'], review['position'])
        assert active['field'] == native['pointer_field'] == review['registered_reference']['field']
        assert active['pointer'] == review['registered_reference']['pointer']
        assert active['English'] == review['english'] and all(review['review'].values())
        assert native['japanese'] == review['source_Japanese']
        index = tables[route][position]
        row = dict(image_index=index, clean_text_offset=native['offset'], clean_hex=native['source_hex'],
                   source_Japanese=native['japanese'], source_meaning=review['source_meaning'],
                   editorial_note=review['localization_note'], **active)
        by_source[native['source_hex']].append(row)
        by_asset[index].append(row)
    return by_source, by_asset


def environment_reason(message_id, english):
    assert 3535 <= message_id <= 3569
    if ':' in english:
        setting, feature = english.split(': ', 1)
        return f'Keep the numbered {setting} asset and its explicit terrain or direction, {feature.lower()}.'
    return f'The source identifies {english} by its terrain family and number. Retain both.'


def build():
    b = current.base
    release = b.load(current.RELEASE)
    assert b.digest(current.ROM) == release['candidate_sha256']
    assert b.digest(current.stage.CLEAN) == release['clean_input_sha256']
    clean, active = map(b.NdsImage.open, (current.stage.CLEAN, current.ROM))
    arm, target = (rom.read_file(current.stage.ARM) for rom in (clean, active))
    assert sha256(target).hexdigest() == release['target_ARM9_sha256']
    source_common, active_common = (rom.read_file(current.stage.COMMON) for rom in (clean, active))
    assert sha256(active_common).hexdigest() == release['target_COMMON_sha256']
    source = common_message_entries(source_common, arm)
    stored = owned_entries(active_common, target, sha256(target[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    routing = b.load(ROUTING)
    # Read back the same native image-routing code covered by the earlier execution.
    assert all(arm[lo:hi] == target[lo:hi] for lo, hi in routing['source_exact_code_ranges'])
    exact, asset_titles = gallery_titles(arm, target, routing, b.load(GALLERY)['records'])
    sheet_paths = sorted(SHEETS.glob('clean_*.png'))
    assert len(sheet_paths) == 7
    drafts = b.load(OLD)['records']
    assert [row['message_id'] for row in drafts] == list(range(3393, 3607))
    assert REVISIONS.keys() == REVISED_GLOSSES.keys()
    indices = dict(zip((n for n in range(3393, 3570) if n not in SEQUENCE_EXTRAS), range(168), strict=True))
    rows = []
    for draft in drafts:
        n = draft['message_id']
        clean_row, stored_row = source[n], stored[n]
        source_hex = draft['source_hex']
        assert clean_row.text == stored_row.text == bytes.fromhex(source_hex)
        assert clean_row.text.decode('cp932') == draft['japanese']
        assert source[n - 1].text.decode('cp932') == draft['previous_japanese']
        assert source[n + 1].text.decode('cp932') == draft['next_japanese']
        titles = exact.get(source_hex, [])
        art = None
        if n in indices:
            index = indices[n]
            path = f'/evstill/evstill{index:03d}.pxl'
            raw = clean.read_file(path)
            assert raw == active.read_file(path)
            assert not titles or {title['image_index'] for title in titles} == {index}
            basis = 'exact Gallery Japanese and image argument' if titles else 'ordered sequence and visual match'
            art = dict(image_index=index, path=path, sha256=sha256(raw).hexdigest(), basis=basis,
                       other_gallery_titles_for_image=[title for title in asset_titles.get(index, [])
                                                       if title['clean_hex'] != source_hex])
        previous = draft['english'].removesuffix('{PAD}')
        meaning = draft['source_meaning']
        if n in REVISIONS:
            english, note = REVISIONS[n]
            meaning = REVISED_GLOSSES[n]
        elif titles:
            english, = set(title['English'] for title in titles)
            note = titles[0]['editorial_note']
            meaning = titles[0]['source_meaning']
        else:
            english = previous
            note = RETENTIONS.get(n) or environment_reason(n, english)
        assert english.isascii() and english.strip() == english and english.isprintable()
        rows.append(dict(id=draft['id'], message_ID=n, file_path=current.stage.COMMON,
            source_reference=reference(clean_row), source_Japanese=draft['japanese'], source_hex=source_hex,
            current_reference=reference(stored_row), current_text=stored_row.text.decode('cp932'),
            current_hex=stored_row.text.hex(), previous_draft=previous, english=english, source_meaning=meaning,
            decision='revision' if english != previous else 'retention', localization_note=note,
            speaker='Scene or artwork label', artwork=art, independent_exact_gallery_titles=titles,
            context=dict(previous_source=draft['previous_japanese'], next_source=draft['next_japanese'],
                         opening_sequence=n >= 3570, sequence_extra=n in SEQUENCE_EXTRAS),
            common_display_consumer_verified=False,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))

    assert sum(bool(row['independent_exact_gallery_titles']) for row in rows) == 123
    assert sum(row['artwork'] is not None for row in rows) == 168
    assert all(row['english'] == row['previous_draft'] for row in rows if row['decision'] == 'retention')
    assert not any(word in row['english'] for row in rows for word in ('Raphael', 'Kamil', '{PAD}'))
    assert asset_titles[97][0]['source_Japanese'] == '総見式のマリアたち'
    assert source[3537].text.decode('cp932') == '森03右折ｔ'
    assert source[3551].text.decode('cp932') == 'ジャングル03右折'
    deps = (current.RELEASE, OLD, GALLERY, ROUTING, *sheet_paths)
    return dict(format='dk4-common-scene-label-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', status='editorial-drafts-with-asset-mapping-common-display-pending',
        candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        registered_ARM9_sha256=release['target_ARM9_sha256'], registered_COMMON_sha256=release['target_COMMON_sha256'],
        counts=Counter(row['decision'] for row in rows), exact_native_records=len(rows), artwork_sequence_entries=len(indices),
        actual_COMMON_activations=0, new_dialogue_credit=0, full_goal_complete=False,
        evidence={str(p): b.digest(p) for p in deps}, records=rows)


def main():
    document = build()
    if OUTPUT.exists():
        assert current.base.load(OUTPUT) == document
        print('Checked that the existing scene-label review reproduces exactly.')
    else:
        current.base.save(OUTPUT, document)
    print(f"{document['exact_native_records']} exact stored labels, {document['artwork_sequence_entries']} artwork references, {dict(document['counts'])}")


if __name__ == '__main__':
    main()
