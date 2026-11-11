"""Verify Hint and both return labels against the exact registered parent."""

from inspect import getsource
from pathlib import Path

from PIL import Image, ImageChops

from scripts import replay_ancient_map_hint_label_v2 as replay
from scripts import verify_ancient_map_hint_label_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = replay.base, replay.stage
OUTPUT = stage.ROOT / 'hint_label_gameplay_verification_v2.json'
RETURN = {11900, 12300, 12700}
STRAY = {(187, 370), (243, 370)}
AFFECTED = (154, 368, 205, 384)


def capture_function():
    source = checked_text(getsource(prior.map_verification.capture), {
        "== original.original.END": "== replay.END",
        "11100, 11500, 11900}": "11100, 11500, 11900, 12300, 12700}",
    })
    env = vars(prior.map_verification) | globals()
    exec(compile(source, __file__ + '::exact-parent-captures', 'exec'), env)
    return env['capture']


def main():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    assert base.digest(stage.parent.ROM) == proof['parent_sha256']
    capture = capture_function()
    left, right = [capture(replay.ROOT / side, proof[sha]) for side, sha in (
        ('parent', 'parent_sha256'), ('hint', 'candidate_sha256'))]
    assert left[0] == right[0] and base.digest(left[2][2]) == base.digest(right[2][2])
    font = stage.parent.stage.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    changed, returns, identical = [], [], []
    for n, old in left[1].items():
        new = right[1][n]
        a, b = [Image.open(row['path']).convert('RGB') for row in (old, new)]
        diff = ImageChops.difference(a, b)
        if n in prior.CHANGED:
            assert diff.getbbox() == AFFECTED
            ink, bounds = prior.locate_label(font, b)
            assert (ink, bounds) == (53, [183, 371, 207, 382])
            assert all(prior.complete_mask(font, 'Back', image, 229, 371, prior.COLOR)[0] == 59
                       for image in (a, b))
            changed.append(dict(frame=n, bounds=bounds, hint_ink=ink, before=old, after=new))
        elif n in RETURN:
            actual = {(x, y) for y in range(384) for x in range(256) if any(diff.getpixel((x, y)))}
            assert actual == STRAY
            assert all(a.getpixel(pt) == prior.COLOR and b.getpixel(pt) == (123, 141, 180) for pt in STRAY)
            for label, x, ink_count in (('Back', 171, 59), ('Select', 217, 72)):
                assert all(prior.complete_mask(font, label, image, x, 371, prior.COLOR)[0] == ink_count
                           for image in (a, b))
            returns.append(dict(frame=n, unchanged_complete_label_ink={'Back': 59, 'Select': 72},
                                cleared_stray_footer_pixels=sorted(STRAY), before=old, after=new))
        else:
            assert not diff.getbbox() and old['framebuffer_sha256'] == new['framebuffer_sha256']
            identical.append(n)
    assert len(changed) == len(returns) == 3 and identical == [9900, 11100]
    evidence = (*left[2], *right[2], stage.PROOF, Path(__file__))
    base.save(OUTPUT, dict(candidate_sha256=proof['candidate_sha256'], parent_sha256=proof['parent_sha256'],
        actual_emulator=True, hardware=False, observed_hint_frames=changed, return_frames=returns,
        whole_frame_matches=identical, four_bit_copied_save_fixture=left[0],
        original_Back_and_Select_masks_exact=True, Hint_box_only=bool(changed),
        evidence={str(path): base.digest(path) for path in evidence}))
    print('Three complete Hint labels and six complete return labels passed. Two stray footer pixels were cleared.')


if __name__ == '__main__':
    main()
