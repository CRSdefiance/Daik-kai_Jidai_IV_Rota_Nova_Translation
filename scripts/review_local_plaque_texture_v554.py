"""Research only: preserve recoverable original plaque grain at original coordinates."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/plaque_source_review_v554')
ROM = Path('out/all_routes_combined_v546_candidate.nds')
# Conservative source interior rectangles; no bevel or surrounding wallpaper.
SOURCE_INTERIORS = {
    'Fleet Crew': [10, 20, 86, 32],
    'Unassigned': [134, 20, 210, 32],
    'Endurance': [10, 42, 86, 54],
    'Quarters': [10, 111, 62, 122],
    'Cannon': [88, 111, 116, 122],
    'Fore/Aft': [10, 133, 62, 144],
    'Square': [134, 133, 186, 144],
    'Health': [10, 106, 46, 118],
    'Mood': [10, 126, 46, 138],
    'Level': [10, 146, 46, 158],
    'HP': [10, 166, 46, 178],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--conservative', action='store_true')
    conservative = parser.parse_args().conservative
    prefix = 'margin_' if conservative else ''
    ROOT.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds')
    groups = []
    for name, batch_name in [('crew', 'assign_sailors_graphics_v5'),
                             ('person', 'person_info_graphics_v3')]:
        batch = json.loads(Path(f'translations/{batch_name}.json').read_text(encoding='utf-8'))
        data = current.read_file(batch['file_path'])
        original = PxlImage.from_bytes(clean.read_file(batch['file_path']))
        image = PxlImage.from_bytes(data)
        before = PxlImage.from_bytes(data)
        # Resolve exact RGB matches; source index numbers need not share their meaning.
        mapping = {i: next((n for n, rgb in enumerate(image.palette)
                            if rgb == colour), None)
                   for i, colour in enumerate(original.palette)}
        records = []
        allowed = set()
        for row in batch['records']:
            text = row['text']
            if text not in SOURCE_INTERIORS:
                continue
            sx, sy, ex, ey = SOURCE_INTERIORS[text]
            l, t, r, b = row['plaque_box']
            source_ink = [(x, y) for y in range(sy, ey) for x in range(sx, ex)
                          if sum(original.palette[original.indices[y * original.width + x]][:3]) < 200]
            assert source_ink
            # The per-pixel version exposes a ghost of Japanese strokes. Retain a
            # conservative contiguous reconstruction band to avoid glyph-shaped seams.
            protected = [min(x for x, _ in source_ink) - 2,
                         min(y for _, y in source_ink) - 2,
                         max(x for x, _ in source_ink) + 3,
                         max(y for _, y in source_ink) + 3]
            expected, restored, hidden = 0, 0, 0
            source_colours = set()
            for y in range(max(sy, t + 2), min(ey, b - 2)):
                for x in range(max(sx, l + 2), min(ex, r - 2)):
                    pos = y * image.width + x
                    if before.indices[pos] == batch['color_index']:
                        continue
                    if conservative and protected[0] <= x < protected[2] and protected[1] <= y < protected[3]:
                        hidden += 1
                        continue
                    index = original.indices[y * original.width + x]
                    rgb = original.palette[index]
                    if sum(rgb[:3]) < 200:
                        hidden += 1
                        continue
                    # Census: source lettering sums <=123; all11 sampled plaque
                    # interiors have material sums >=286 (first plaque >=303).
                    assert sum(rgb[:3]) >= 286, (text, x, y, rgb)
                    source_colours.add(rgb)
                    assert mapping[index] is not None, (text, rgb)
                    expected += 1
                    restored += image.indices[pos] != mapping[index]
                    image.indices[pos] = mapping[index]
                    allowed.add(pos)
            records.append({'id': row['id'], 'english': text,
                            'source_interior': SOURCE_INTERIORS[text],
                            'localized_plaque': row['plaque_box'],
                            'conservative_protected_Japanese_band': protected if conservative else None,
                            'recoverable_original_background_pixels_exact': expected,
                            'background_pixels_restored': restored,
                            'Japanese_ink_points_retaining_reconstructed_grain': hidden,
                            'source_texture_colours': len(source_colours),
                            'fully_completed': False})
        assert all(a == b for pos, (a, b) in enumerate(zip(before.indices, image.indices, strict=True))
                   if pos not in allowed)
        for row in batch['records']:
            l, t, r, b = row['plaque_box']
            ink_before = {y * image.width + x for y in range(t, b) for x in range(l, r)
                          if before.indices[y * image.width + x] == batch['color_index']}
            ink_after = {y * image.width + x for y in range(t, b) for x in range(l, r)
                         if image.indices[y * image.width + x] == batch['color_index']}
            assert ink_before == ink_after
        output = image.to_bytes()
        assert output[:image.pixels_offset] == data[:before.pixels_offset]
        (ROOT / f'{prefix}{name}_RESEARCH_ONLY.pxl').write_bytes(output)
        sheet = Image.new('RGB', (1050, len(records) * 95 + 30), (40, 45, 50))
        draw = ImageDraw.Draw(sheet)
        for col, label in enumerate(('Original Japanese', 'Current V546', 'Local source texture prototype')):
            draw.text((col * 350 + 5, 5), label, fill='white')
        for n, record in enumerate(records):
            draw.text((5, 30 + n * 95), record['english'], fill='white')
            for col, atlas in enumerate((original, before, image)):
                crop = atlas.render().crop(record['localized_plaque']).convert('RGB')
                sheet.paste(crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST),
                            (col * 350 + 5, 48 + n * 95))
        sheet.save(ROOT / f'{prefix}{name}_local_texture_review.png')
        groups.append({'file_path': batch['file_path'], 'source_sha256': sha(data),
                       'research_only_sha256': sha(output), 'records': records,
                       'all_English_ink_and_existing_bevels_preserved': True,
                       'all_unowned_pixels_header_palette_dimensions_preserved': True})
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'groups': groups, 'production_ROM_changed': False,
             'source_interiors_and_dark_stroke_exclusion_need_visual_review': True,
             'method': 'conservative_text_band' if conservative else 'per_pixel_dark_stroke_exclusion',
             'concealed_pixels_are_not_claimed_as_recovered': True,
             'six_original_pink_stat_backgrounds_excluded_from_wood_recovery': True,
             'native_and_in_game_prototype_verification_pending': True,
             'all18_plaque_entries_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT / f'{prefix}local_texture_prototype_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Research-only local texture restoration:', sum(r['background_pixels_restored'] for g in groups for r in g['records']), 'pixels across11 plaques; all17 complete ink masks retained.')


if __name__ == '__main__':
    main()
