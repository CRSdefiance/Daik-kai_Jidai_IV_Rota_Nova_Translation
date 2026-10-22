"""Match original genre-card placement inside its native256x192 view."""

import copy
import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_fls_label_batch

ROOT = Path('work/analysis/genre_card_v305')
ROM = Path('out/all_routes_combined_v303_candidate.nds')
BATCH = Path('translations/genre_card_native_viewport_v2.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    canonical, current, clean = [NdsImage.open(p) for p in
                                 ('out/raphael_natural_v2_accepted_base.nds', ROM, 'work/clean.nds')]
    assert sha(ROM.read_bytes()) == 'b9a4af601390a4551ae2c11ab4d06b7f3c8ebc2de6cd5178228becb3aa146107'
    path = '/FLS/logo.fls'
    source = canonical.read_file(path)
    assert source == current.read_file(path)
    a, japanese = FlsArchive(source), FlsArchive(clean.read_file(path))
    index, texture = 3, a.texture(3)
    assert a.records[index][0] >> 16 == 256 and a.records[index][1] & 0xFFFF == 192
    assert (texture.width, texture.height) == (256, 256)
    # Reproduce the old text exactly before changing placement or size.
    old = bytes(texture.indices)
    texture.replace_with_lines(['REKOEITION GAME'], maximum_size=12)
    assert bytes(texture.indices) == old
    record = {'id': 'DK4_GENRE_CARD_NATIVE_HEIGHT_V2', 'asset_index': index,
              'lines': ['REKOEITION GAME'], 'maximum_size': 20,
              'background_index': 0, 'color_index': 15, 'layout_width': 256, 'layout_height': 192,
              'Japanese': 'リコエイションゲーム', 'source_meaning': 'Existing Koei genre designation, followed by game.',
              'localization_note': 'Keep established project spelling; match original centered native view and approximate original ink width with complete English.',
              'clean_texture_sha256': sha(bytes(japanese.texture(index).indices)),
              'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True)}
    batch = {'format': 'dk4-fls-label-batch-v1', 'file_path': path, 'source_file_sha256': sha(source),
             'native_viewport_policy': 'header-size-v2', 'target_locale': 'en-US', 'records': [record],
             'scope': 'Genre lettering in source native256x192 view; all other logo art and palette/metadata retained.'}
    BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    target, ids = apply_fls_label_batch(BATCH, source)
    b = FlsArchive(target)
    assert len(target) == len(source) and a.records == b.records
    start, extent = a.data_offset + a.records[3][4], a.records[3][5]
    assert all(x == y or start <= at < start + extent for at, (x, y) in enumerate(zip(source, target, strict=True)))
    for i in range(a.count):
        x, y = FlsArchive(source).texture(i), b.texture(i)
        assert (x.width, x.height, x.flags, x.palette) == (y.width, y.height, y.flags, y.palette)
        if i != 3:
            assert x.indices == y.indices
    for field in ('layout_height', 'layout_width'):
        bad = copy.deepcopy(batch)
        bad['records'][0][field] = 256 if field == 'layout_height' else 128
        negative = ROOT / (field + '_negative.json')
        negative.write_text(json.dumps(bad, indent=2) + '\n', encoding='utf-8')
        try:
            apply_fls_label_batch(negative, source)
        except ValueError as error:
            assert 'differs from native FLS' in str(error)
        else:
            raise AssertionError('Native-size mismatch was accepted')
    def bounds(t):
        points = [(i % t.width, i // t.width) for i, value in enumerate(t.indices) if max(t.palette[value][:3])]
        return [min(x for x, _ in points), min(y for _, y in points), max(x for x, _ in points) + 1, max(y for _, y in points) + 1]
    proof = {'format': 'dk4-genre-native-view-preparation-v305', 'batch': str(BATCH), 'source_sha256': sha(source),
             'target_sha256': sha(target), 'changed_records': ids,
             'original_Japanese_ink_bounds': bounds(japanese.texture(3)),
             'old_English_ink_bounds': bounds(FlsArchive(source).texture(3)), 'new_English_ink_bounds': bounds(b.texture(3)),
             'native_view': [256, 192], 'stored_view': [256, 256],
             'unchanged_words_metadata_palette_and_other_logo_textures': True,
             'new_word_size_matches_original_ink_width': True, 'two_native_size_negatives_rejected': True,
             'current_registered_release_and_actual_startup_pending': True, 'full_goal_complete': False}
    (ROOT / 'preparation.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'target_logo_research_only.fls').write_bytes(target)
    b.texture(3).render().save(ROOT / 'genre_target.png')
    print('Genre native256x192; same complete English; two size negatives rejected; only one compressed pixel slot changes.')


if __name__ == '__main__':
    main()
