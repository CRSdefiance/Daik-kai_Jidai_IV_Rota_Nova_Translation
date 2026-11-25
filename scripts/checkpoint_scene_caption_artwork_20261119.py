"""Bind stored scene labels to Gallery captions by image as well as Japanese text."""

from collections import Counter, defaultdict
from pathlib import Path
from struct import unpack_from

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.gallery_caption_bounds import validate as validate_gallery
from scripts import checkpoint_shared_display_owners_20261119 as prior
from scripts import register_town_summary_20261119 as current

base, native, stage = current.base, current.native, current.stage
OUTPUT = prior.BOOK / 'scene_caption_artwork_20261119_v1.json'

VARIANTS = {
    3412: 'Both sources describe the close-up of Rafael playing. The linked violin scene supplies the instrument. Retain the shared English caption.',
    3438: 'Both sources identify an injured Hodram. Retain the stored portrait-style phrase and the Gallery’s short statement of the same fact.',
    3462: 'The stored label describes Lil’s disappointment and Clifford coming to meet her. The separate Gallery source names the two people only. Preserve that difference in the English.',
    3480: 'The Japanese differs in phrasing, with the same blooming tulips and large variant. Retain the shared English caption.',
    3497: 'The review ceremony and Maria’s group recur in the surrounding captions. The Gallery source confirms 総見式 for the apparent 総見算 slip. Retain the shared English caption.',
}


def main():
    assert not OUTPUT.exists()
    release, ledger, previous = map(base.load, (current.RELEASE, base.LEDGER, prior.OUTPUT))
    assert base.digest(current.ROM) == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(prior.current.ROM) == previous['candidate_sha256']
    assert base.digest(stage.CLEAN) == previous['clean_sha256'] == release['clean_input_sha256']
    clean, earlier, active = map(base.NdsImage.open, (stage.CLEAN, prior.current.ROM, current.ROM))
    ja, old, arm = [rom.read_file(stage.ARM) for rom in (clean, earlier, active)]
    assert native.digest(arm) == release['target_ARM9_sha256']
    assert native.digest(active.read_file(stage.COMMON)) == release['target_COMMON_sha256']
    shared = prior.stage.workflow
    original = shared.common_message_entries(clean.read_file(stage.COMMON), ja)
    installed = shared.owned_entries(active.read_file(stage.COMMON), arm, native.digest(arm[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET]))

    # Reuse the previous native route and formatter proofs only for exact inputs.
    code = [(0x28AA8,0x28BAC), (0x29F50,0x29FD4), (0x42C44,0x42C94), (0x42E30,0x42ED4),
            (0x42F4C,0x4300C), (0x432DC,0x432FC), (0x456A0,0x4570C), (0xD5160,0xD55A4)]
    assert all(old[start:end] == arm[start:end] for start, end in code)
    old_font, current_font = map(GameAsciiFont.from_arm9, (old, arm))
    assert all(old_font.decode(c).tobytes() == current_font.decode(c).tobytes() for c in map(chr, range(32, 127)))
    gallery = base.load(prior.GALLERY)['records']
    available = validate_gallery(arm)
    assert available == validate_gallery(old) and len(available) == len(gallery) == 164
    caption_at, display_at = ({(r['route'],r['position']): r for r in rows} for rows in (gallery, available))
    by_image = defaultdict(list)
    display_rows = base.load(prior.ROUTING)['Gallery_tables'][0]['routes']
    for table, route in zip(display_rows, range(4), strict=True):
        image_field = table['table_pointer'] - prior.BASE
        indices = table['image_indices']
        assert old[image_field:image_field+len(indices)*4] == arm[image_field:image_field+len(indices)*4]
        assert tuple(indices) == unpack_from(f'<{len(indices)}I', arm, image_field)
        for position, image in enumerate(indices):
            caption, rendered = caption_at[route,position], display_at[route,position]
            path = f'/evstill/evstill{image:03d}.pxl'
            assert caption['original_scene_image'] == path and all(caption['review'].values())
            assert caption['registered_reference']['field'] == rendered['field']
            assert caption['registered_reference']['pointer'] == rendered['pointer']
            assert caption['english'] == rendered['English']
            by_image[image].append(dict(caption_id=caption['id'], clean_Japanese=caption['source_Japanese'], english=caption['english'],
                source_reference=caption['source_reference'], registered_reference=caption['registered_reference'],
                current_pointer=rendered['pointer'], bounds=rendered['bounds']))
    assert len(by_image) == 159

    scene_labels = {r['message_ID']: r for r in base.load(prior.SCENES)['records']}
    known = {r['message_ID']: r for r in previous['records'] if r['message_ID'] in scene_labels}
    cases = []
    for key, label in scene_labels.items():
        record = known[key]
        assert shared.reference(original[key]) == record['source_reference'] == label['source_reference']
        assert shared.reference(installed[key]) == record['current_reference']
        assert original[key].text.hex() == record['source_hex'] and installed[key].text.hex() == record['current_hex']
        exact = record['independent_gallery_draw_sources']
        art = label['artwork']
        image = art['image_index'] if art else None
        if key == 3492:
            assert image is None and len(exact) == 1 and exact[0]['clean']['image'] == 45
            counterpart = scene_labels[3442]
            assert counterpart['artwork']['image_index'] == 45
            assert counterpart['source_Japanese'] == 'ホドラムとマリア' and label['source_Japanese'] == 'マリアとホドラム'
            image = 45
        caption_rows = by_image.get(image, [])
        if exact:
            assert all(row['clean']['image'] == image for row in exact)
            assert any(r['clean_Japanese'] == label['source_Japanese'] for r in caption_rows)
            status = 'exact_japanese_and_gallery_artwork'
        elif caption_rows:
            assert key in VARIANTS and all(r['clean_Japanese'] != label['source_Japanese'] for r in caption_rows)
            status = 'separate_japanese_titles_for_same_artwork'
        elif art:
            status = 'story_still_outside_gallery_tables'
        elif record.get('opening_artwork_association'):
            status = 'opening_artwork_association'
        else:
            status = 'no_exact_artwork_match_yet'
        cases.append(dict(message_ID=key, disposition=status, source_reference=record['source_reference'],
            current_reference=record['current_reference'], source_Japanese=label['source_Japanese'],
            installed_hex=record['current_hex'], draft_english=label['english'], previous_review=label['review'],
            image_index=image, independent_gallery_captions=caption_rows,
            contextual_decision=VARIANTS.get(key, label['localization_note']),
            storage_display_path='unverified outside the checked independent display paths'))

    tallies = Counter(r['disposition'] for r in cases)
    assert tallies == dict(exact_japanese_and_gallery_artwork=123, separate_japanese_titles_for_same_artwork=5,
        story_still_outside_gallery_tables=41, opening_artwork_association=31, no_exact_artwork_match_yet=14)
    checked_art = sorted(set(by_image) | {r['image_index'] for r in cases if r['image_index'] is not None})
    art_hashes = {}
    for image in checked_art:
        path = f'/evstill/evstill{image:03d}.pxl'
        art = active.read_file(path)
        assert art == earlier.read_file(path)
        art_hashes[path] = native.digest(art)
    dependencies = (current.RELEASE, prior.OUTPUT, prior.GALLERY, prior.ROUTING, prior.SCENES, Path(__file__))
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], prior_sha256=previous['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], disposition_counts=dict(tallies), records=cases,
        identical_gallery_and_still_assets=art_hashes, exact_carried_code_spans=[dict(start=lo,end=hi,sha256=native.digest(arm[lo:hi])) for lo,hi in code],
        prior_gallery_gameplay_reused=True, new_gameplay_runs=0, shared_raw_pending_count=276, new_contextual_credit=0,
        evidence={str(p): base.digest(p) for p in dependencies}, full_goal_complete=False))
    print(f'Classified 214 records by display evidence, including five artwork-linked caption variants and {len(art_hashes)} unchanged stills.')


if __name__ == '__main__':
    main()
