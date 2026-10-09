"""Verify sound titles through native global IDs after COMMON relocation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.bgm_title_tracking import (
    CODE_LOCKS,
    FONT_OFFSET,
    FONT_SIZE,
    apply_probe,
    title_geometry,
)
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
BGM_IDS = range(3251, 3289)
# Constructor initializes selection to 2. Draw adds 0xCB1, calls the
# native accessor 0x0205528C, measures strlen * 6 and centers at x=64.
SELECTOR_CODE_RANGES = ((0x108F9C, 0x109008), (0x109008, 0x10905C),
                        (0x1090C4, 0x1091FC), (0x1091FC, 0x109310),
                        (0x5528C, 0x552A4))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify_components(common, arm9, expected_titles, sfx_slots, baseline_arm9, *, tracking_renderer=False):
    expected_arm9 = apply_probe(baseline_arm9) if tracking_renderer else baseline_arm9
    for lo, hi in SELECTOR_CODE_RANGES:
        if arm9[lo:hi] != expected_arm9[lo:hi]:
            raise ValueError(f'Sound selector code differs at {lo:#x}')
    if tracking_renderer:
        for lo, hi, _ in CODE_LOCKS:
            if arm9[lo:hi] != expected_arm9[lo:hi]:
                raise ValueError('Mapped BGM tracking code differs')
        if arm9[FONT_OFFSET:FONT_OFFSET + FONT_SIZE] != baseline_arm9[FONT_OFFSET:FONT_OFFSET + FONT_SIZE]:
            raise ValueError('Mapped BGM font differs')
    actual = common_message_entries(common, arm9, clean=False)
    for i in BGM_IDS:
        if actual[i].text.rstrip(b' ') != expected_titles[i]:
            raise ValueError(f'Native BGM message {i} differs or loses a character')
        title = expected_titles[i].decode('ascii')
        if not title_geometry(title, 5 if tracking_renderer else 6)['fits_panel']:
            raise ValueError(f'BGM message {i} exceeds its 128-pixel panel')
    for key, offset, expected in sfx_slots:
        if arm9[offset:offset + len(expected)] != expected:
            raise ValueError(f'SFX title {key} differs from the accepted slot')
    return {'status': 'pass', 'native_bgm_titles_checked': 38,
            'sfx_titles_checked': len(sfx_slots),
            'global_message_ids_preserved': True, 'selector_code_unchanged': not tracking_renderer,
            'sound_code_matches_exact_declared_renderer': True,
            'bgm_title_tracking_renderer': tracking_renderer,
            'bgm_ascii_advance': 5 if tracking_renderer else 6,
            'title_panel_width_checked': True,
            'static_track_selection_bounds': [2, 39],
            'static_native_title_id_bounds': [3251, 3288],
            'track_change_and_play_toggle_code_unchanged': True,
            'runtime_selection_and_playback_verified': False,
            'title_meaning_review_required': True}


def verify(candidate: Path, profile: str | None = None):
    if sha(BASE.read_bytes()) != BASE_SHA:
        raise ValueError('Canonical sound baseline differs')
    base, image = NdsImage.open(BASE), NdsImage.open(candidate)
    baseline_arm9 = base.read_file('/__arm9__.bin')
    accepted = common_message_entries(base.read_file('/COMMON/MESFILE.DK4'),
                                      baseline_arm9, clean=False)
    expected = {i: accepted[i].text.rstrip(b' ') for i in BGM_IDS}
    tracking_renderer, reviewed = False, set()
    if profile:
        registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
        path = registry['profiles'][profile].get('common_native_reblocking')
        if path:
            config = json.loads(Path(path).read_text(encoding='utf-8'))
            tracking_renderer = config.get('bgm_title_tracking_renderer', False)
            clean = NdsImage.open('work/clean.nds')
            source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                             clean.read_file('/__arm9__.bin'))
            for declaration in config['manuscripts']:
                raw = Path(declaration['path']).read_bytes()
                if sha(raw) != declaration['sha256']:
                    raise ValueError('Reviewed sound manuscript hash differs')
                payload = json.loads(raw)
                validate_natural_dialogue_batch(payload)
                for row in payload['records']:
                    i = row['message_id']
                    if i not in BGM_IDS:
                        continue
                    if i in reviewed or bytes.fromhex(row['source_hex']) != source[i].text:
                        raise ValueError('Duplicate or changed BGM source')
                    reviewed.add(i)
                    expected[i] = row['english'].removesuffix('{PAD}').encode('ascii')
    batch = json.loads(Path('translations/sound_selector_arm9.json').read_text(encoding='utf-8'))
    slots = []
    for row in batch['records'][1:]:
        offset = row['offset']
        size = len(bytes.fromhex(row['source_hex']))
        declared = row['english'].encode('ascii').ljust(size, b'\0')
        if baseline_arm9[offset:offset + size] != declared:
            raise ValueError('SFX declaration differs from canonical baseline')
        slots.append((row['id'], offset, declared))
    if len(slots) != 57:
        raise ValueError('Incomplete SFX declarations')
    result = verify_components(image.read_file('/COMMON/MESFILE.DK4'),
                               image.read_file('/__arm9__.bin'), expected, slots,
                               baseline_arm9, tracking_renderer=tracking_renderer)
    if tracking_renderer and reviewed != set(BGM_IDS):
        raise ValueError('BGM tracking profile lacks all 38 reviewed title declarations')
    result.update({'reviewed_title_meanings': len(reviewed),
                   'title_meaning_review_required': reviewed != set(BGM_IDS)})
    result.update({'candidate': candidate.as_posix(),
                   'candidate_sha256': sha(candidate.read_bytes()), 'profile': profile})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--profile')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.candidate, args.profile)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
