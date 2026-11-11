"""Verify the original Y-button layout and complete localized Hint lettering."""

from pathlib import Path

from PIL import Image, ImageChops

from scripts import replay_ancient_map_hint_label_v1 as replay
from scripts import verify_ancient_map_text_v2 as map_verification
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


stage, base = replay.stage, replay.base
OUTPUT = stage.ROOT / 'hint_label_gameplay_verification.json'
CONTROL = map_verification.ROOT / 'ancient_map'
CHANGED = {10300, 10700, 11500}
BUTTON_BOX = (148, 366, 211, 384)
COLOR = (230, 230, 230)


def locate_label(font, image):
    candidates = []
    for x in range(BUTTON_BOX[0], BUTTON_BOX[2] - 24 + 1):
        for y in range(BUTTON_BOX[1], BUTTON_BOX[3] - 11 + 1):
            try:
                candidates.append(complete_mask(font, 'Hint', image, x, y, COLOR))
            except ValueError:
                continue
    assert len(candidates) == 1, candidates
    return candidates[0]


def main():
    proof = base.load(stage.PROOF)
    control = base.load(map_verification.PROOF)
    bgm = base.load(stage.parent.EVIDENCE)
    assert bgm['parent_sha256'] == control['research_ROM_sha256']
    assert bgm['research_ROM_sha256'] == proof['parent_sha256']
    assert bgm['allocation']['all_unselected_native_copy_spans_exact']
    assert 40 not in bgm['allocation']['touched_blocks']
    a, b = [map_verification.capture(folder, sha) for folder, sha in (
        (CONTROL, control['research_ROM_sha256']), (replay.ROOT, proof['candidate_sha256']))]
    assert a[0] == b[0] and base.digest(a[2][2]) == base.digest(b[2][2])
    font = stage.parent.stage.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    changed, identical = [], []
    for frame, new in b[1].items():
        old = a[1][frame]
        before, after = [Image.open(row['path']).convert('RGB') for row in (old, new)]
        diff = ImageChops.difference(before, after).getbbox()
        if frame not in CHANGED:
            assert not diff and old['framebuffer_sha256'] == new['framebuffer_sha256']
            identical.append(frame)
            continue
        assert diff and diff[0] >= BUTTON_BOX[0] and diff[1] >= BUTTON_BOX[1]
        assert diff[2] <= BUTTON_BOX[2] and diff[3] <= BUTTON_BOX[3]
        ink, bounds = locate_label(font, after)
        changed.append(dict(frame=frame, before=old, after=new, complete_hint_ink=ink, bounds=bounds,
                            changed_rectangle=diff))
    assert len(changed) == 3 and [row['bounds'] for row in changed].count(changed[0]['bounds']) == 3
    evidence = (*a[2], *b[2], stage.PROOF, stage.parent.EVIDENCE, Path(__file__))
    base.save(OUTPUT, dict(candidate_sha256=proof['candidate_sha256'], parent_sha256=proof['parent_sha256'],
        source_record=proof['record']['id'], old_clue_and_both_returns_exact=True,
        changed_frames=changed, unchanged_frames=identical, original_label_uses_terminated_native_text=True,
        actual_emulator=True, hardware=False, fixture_scope='Four temporary clue bits in the copied Syracuse save.',
        evidence={str(path): base.digest(path) for path in evidence}))
    print('All three Hint masks are complete; the original map, clue view and both return paths are exact outside the label.')


if __name__ == '__main__':
    main()
