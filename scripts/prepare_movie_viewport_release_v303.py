"""Source-locked full English subtitle layouts in their encoded native widths."""

import copy
import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_fls_label_batch

ROOT = Path('work/analysis/movie_viewport_v303')
ROM = Path('out/all_routes_combined_v299_candidate.nds')
DEFINITIONS = {
    '/FLS/M22.fls': [(1, ["Hey, don't!", "It's too dangerous!"], 'ねえ、ダメだよ！ 無茶だって！',
                      'The speaker tells Lil not to proceed and says the action is too reckless/dangerous.'),
                     (2, ["It's fine, it's fine.", 'Leave it to me!'], 'だいじょーぶ、だいじょーぶ。まっかせなさい！',
                      'Lil reassures the other person twice and tells them to leave it to her.')],
    '/FLS/M24.fls': [(3, ["The ship's here!", 'Report to the captain!'], 'よし、船が来たぞ！！ 船長に報告しろ！！',
                      'The ship arrives; the speaker orders someone to report to the captain.'),
                     (4, ['Looks like a foreign merchant ship!', 'Admiral, your orders?'],
                      '提督！外国籍の商船と思われます！ ご指示を！',
                      'The speaker reports an apparent foreign merchant ship and requests the admiral\'s instructions; inference is retained.')],
}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, canonical, clean = [NdsImage.open(p) for p in (ROM, 'out/raphael_natural_v2_accepted_base.nds', 'work/clean.nds')]
    assert sha(ROM.read_bytes()) == '9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f'
    batches, cases = [], []
    for path, rows in DEFINITIONS.items():
        source = canonical.read_file(path)
        assert source == current.read_file(path)
        original = FlsArchive(clean.read_file(path))
        archive = FlsArchive(source)
        records = []
        for index, english, japanese, meaning in rows:
            native = archive.records[index][0] >> 16
            assert native == (176 if path.endswith('M22.fls') else 216)
            assert archive.records[index][:4] == original.records[index][:4]
            records.append({'id': f'DK4_{Path(path).stem}_NATIVE_VIEWPORT_CARD_{index}', 'asset_index': index,
                            'lines': english, 'maximum_size': 12, 'background_index': 0, 'color_index': 1,
                            'outline_index': 2, 'layout_width': native,
                            'Japanese': japanese, 'source_meaning': meaning,
                            'source_texture_sha256': sha(bytes(original.texture(index).indices)),
                            'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True)})
        batch = {'format': 'dk4-fls-label-batch-v1', 'file_path': path,
                 'source_file_sha256': sha(source), 'native_viewport_policy': 'header-width-v1',
                 'target_locale': 'en-US', 'scope': 'Full source-reviewed captions centered in native FLS width, with complete opaque outlines.',
                 'records': records}
        filename = Path(f'translations/{Path(path).stem.lower()}_native_viewport_subtitles_v1.json')
        filename.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        target, ids = apply_fls_label_batch(filename, source)
        rebuilt = FlsArchive(target)
        owned = {row['asset_index'] for row in records}
        assert len(target) == len(source) and rebuilt.records == archive.records
        spans = [(archive.data_offset + archive.records[i][4], archive.data_offset + sum(archive.records[i][4:6])) for i in owned]
        assert all(a == b or any(lo <= at < hi for lo, hi in spans) for at, (a, b) in enumerate(zip(source, target, strict=True)))
        for index in range(archive.count):
            a, b = archive.texture(index), rebuilt.texture(index)
            assert (a.flags, a.width, a.height, a.palette) == (b.flags, b.width, b.height, b.palette)
            if index not in owned:
                assert a.indices == b.indices
        for row in records:
            bad = copy.deepcopy(batch)
            bad['records'] = [copy.deepcopy(row)]
            bad['records'][0]['layout_width'] = 256
            negative = ROOT / f'{Path(path).stem}_{row["asset_index"]}_wrong_storage_width_negative.json'
            negative.write_text(json.dumps(bad, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            try:
                apply_fls_label_batch(negative, source)
            except ValueError as error:
                assert 'differs from native FLS viewport' in str(error)
            else:
                raise AssertionError('Storage-width subtitle accepted despite narrower native viewport')
        (ROOT / (Path(path).name + '.research_only')).write_bytes(target)
        batches.append(str(filename))
        cases.append({'path': path, 'source_sha256': sha(source), 'target_sha256': sha(target), 'records': ids,
                      'all_metadata_palettes_dimensions_and_other_compressed_slots_exact': True,
                      'wrong_storage_width_negative_cases_rejected': len(records)})
    proof = {'format': 'dk4-native-movie-subtitle-viewport-preparation-v303', 'parent': str(ROM),
             'parent_sha256': sha(ROM.read_bytes()), 'batches': batches, 'cases': cases,
             'all_four_complete_captions_fit_original_compressed_slots': True,
             'full_registered_release_current_movie_playback_and_exact_patch_pending': True,
             'M24_inference_wording_now_source_faithful': True, 'full_goal_complete': False}
    (ROOT / 'preparation.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Four full captions in176/216 native widths; four storage-width negatives rejected; all metadata/other slots exact.')


if __name__ == '__main__':
    main()
