"""Check native lookups, complete panels and menu returns in Amsterdam Square."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from scripts import checkpoint_amsterdam_square_current_20261114 as original
from scripts import stage_square_country_briefings_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured, shots


base = stage.base
OUTPUT = stage.ROOT / 'gameplay_verification.json'
SHEET = stage.ROOT / 'gameplay_lower_screens.png'
CASES = {'square': ((9701, 136), (10901, 658), (11701, 689), (12501, 689),
                    (13301, 657), (14501, 656), (15301, 656))}
RETURN = (15701, 16101)


def main():
    proof, review = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    sha = base.digest(stage.ROM)
    assert sha == proof['candidate_sha256'] == review['candidate_sha256']
    assert base.digest(stage.MANUSCRIPT) == proof['manuscript_sha256']
    folder = stage.ROOT / 'amsterdam/square'
    original_folder = original.capture.ROOT / 'square'
    capture = SimpleNamespace(ROOT=folder.parent, schedule=original.capture.schedule)
    decision = original.DECISIONS.copy()
    for record in review['records']:
        n = record['message_ID']
        decision[n] = (record['visible_lines'], record['context'], record['localization_note'])
    evidence = {str(p): base.digest(p) for p in (stage.STORED, stage.MANUSCRIPT, Path(__file__))}
    verify = FunctionType(original.observed_panels.__code__, vars(original) | dict(capture=capture, CASES=CASES, DECISIONS=decision))
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    panels = verify(proof, arm, evidence)
    assert {n: len(rows) for n, rows in panels.items() if rows} == {136: 1, 656: 2, 657: 1, 658: 1, 689: 2}
    assert len(panels[689][0]['lines']) == 2
    before_path, after_path = [p / 'capture/capture_report.json' for p in (original_folder, folder)]
    before, after = map(lambda p: shots(base.load(p)), (before_path, after_path))
    evidence[str(before_path)] = base.digest(before_path)
    returns = []
    for frame in RETURN:
        expected, actual = captured(before[frame]), captured(after[frame])
        assert ImageChops.difference(expected, actual).getbbox() is None
        returns.append(dict(frame=frame, observed_complete_menu_pixels_match_prior=after[frame]['PNG_sha256']))
        evidence.update({shot['path']: shot['PNG_sha256'] for shot in (before[frame], after[frame])})

    held = (10901, 11701, 12501, 13301, 14501, 15301, *RETURN)
    page = Image.new('RGB', (512, (192 + 20) * 4), 'white')
    labels = ImageDraw.Draw(page)
    for i, frame in enumerate(held):
        x, y = (i % 2) * 256, (i // 2) * 212
        labels.text((x + 5, y + 4), str(frame), fill='black')
        page.paste(captured(after[frame]).crop((0, 192, 256, 384)), (x, y + 20))
    if not SHEET.exists():
        page.save(SHEET)
    with Image.open(SHEET) as on_disk:
        assert ImageChops.difference(page, on_disk.convert('RGB')).getbbox() is None
    evidence[str(SHEET)] = base.digest(SHEET)
    data = dict(candidate_sha256=sha, complete_holds={n: rows for n, rows in panels.items() if rows},
        transitions=returns, observed_changed_keys=[657, 689],
        offline_only_changed_keys=sorted(set(stage.PROSE) - {657, 689}), actual_emulator=True, ordinary_input=True,
        hardware=False, gameplay_sheet=str(SHEET), sheet_sha256=evidence[str(SHEET)], evidence=evidence)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == data
    else:
        base.save(OUTPUT, data)
    print('Seven complete dialogue masks, six Shopkeeper nameplates, and two original menu returns verified.')


if __name__ == '__main__':
    main()
