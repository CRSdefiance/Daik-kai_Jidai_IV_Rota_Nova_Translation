"""Distinguish the original tooltip color animation from a graphics regression."""

from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_port_gameplay_v762 import capture
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/tavern_release_v767')
RECT = (60, 242, 104, 258)


def main():
    pa, a, _, before = capture('tavern_editorial_v767_Town_animation_v762')
    pb, b, _, after = capture('tavern_editorial_v767_Town_animation_v767')
    assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and a['core_options'] == b['core_options']
    frames = list(range(10450, 10851)); phases = [{}, {}]; per_frame = [{}, {}]
    for index, source in enumerate((before, after)):
        for f in frames:
            image = Image.open(source[f]['path']).convert('RGB')
            digest = sha(image.crop(RECT).tobytes())
            phases[index].setdefault(digest, []).append(f); per_frame[index][f] = digest
    assert set(phases[0]) == set(phases[1]) and len(phases[0]) == 2
    for f in frames:
        x, y = [Image.open(source[f]['path']).convert('RGB') for source in (before, after)]
        diff = ImageChops.difference(x, y); diff.paste((0, 0, 0), RECT)
        assert diff.getbbox() is None, f
    assert all(per_frame[1][f] == per_frame[0][f + 3] for f in frames[:-3])
    save(ROOT / 'Town_tooltip_animation.json', {'original_report': str(pa), 'candidate_report': str(pb),
        'all401_two_screen_pairs_exact_outside_original_tooltip': frames,
        'tooltip_bounds': RECT, 'original_native_pixel_phase_frames': phases[0],
        'candidate_native_pixel_phase_frames': phases[1],
        'identical_two_original_pixel_variants_no_new_bitmap_palette_or_text': True,
        'candidate_animation_three_frames_ahead': True,
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'scope': 'Ordinary Town return animation only;not a waiver for altered graphics or glyphs elsewhere.'})
    print('401 pairs:every non-tooltip pixel exact;both original tooltip variants match pixel-for-pixel with3-frame phase offset.', flush=True)


if __name__ == '__main__': main()
