"""Preflight the proposed Baltic trade dialogue with the current native font."""

from types import SimpleNamespace

from PIL import Image, ImageDraw

from scripts import review_hodram_baltic_trade_gameplay_20261121 as dialogue
from scripts.stage_hodram_alexandria_tutorial_20261121 import plan_progressive


ROOT = dialogue.FOLDER
PROOF = ROOT / 'baltic_trade_draft_preflight.json'
SHEET = ROOT / 'baltic_trade_draft_preflight.png'


def main():
    square = dialogue.square
    base, active, native = square.base, square.runs.active, square.native
    assert not PROOF.exists() and not SHEET.exists()
    manuscript, release = map(base.load, (dialogue.REVIEW, active.RELEASE))
    assert manuscript['candidate_sha256'] == release['candidate_sha256'] == base.digest(active.ROM)
    assert release['registry_sha256'] == base.digest(base.REGISTRY)
    image = base.NdsImage.open(active.ROM)
    arm, font = (image.read_file(path) for path in (native.ARM, '/GRP/KANJI.FNT'))
    painter = square.town.clipped_renderer(SimpleNamespace(arm=arm, image=image))
    rows = [row for row in manuscript['records'] if row['decision'] == 'revision']
    assert len(rows) == 4 and all(not row['review']['formatting'] for row in rows)
    sheet = Image.new('RGB', (888, 308), '#263238')
    labels = ImageDraw.Draw(sheet)
    tested = []
    palette = [(239, 231, 200), (0, 8, 0)] + [(98, 97, 98)] * 14
    for i, row in enumerate(rows):
        before = bytes.fromhex(row['registered_reference']['exact_stored_hex'])[1:]
        source = bytes.fromhex(row['source_reference']['exact_stored_hex'])[1:]
        body, plan = plan_progressive(row, row['source_selector'], before, source)
        result = painter(arm, font, body)
        page, = result['pages']
        assert plan['expected_native_pages'] == 1 and result['complete_consumed_bytes'] == len(body)
        assert page['native_independent_plane_equal'] and page['all_bitmap_header_input_canaries_exact']
        plane = bytes.fromhex(page['native_plane_hex'])
        assert len(plane) == 216 * 64
        panel = Image.new('RGB', (216, 64))
        panel.putdata([palette[v] for v in plane])
        x, y = (i % 2) * 444, (i // 2) * 154
        labels.text((x + 4, y + 4), f"{row['id']} · {row['speaker']}", fill='white')
        sheet.paste(panel.resize((432, 128), Image.Resampling.NEAREST), (x + 4, y + 20))
        tested.append(dict(id=row['id'], source_selector=row['source_selector'], english=row['english'],
            automatic_plan=plan, staged_body_hex=body.hex(), native_page_sha256=native.digest(plane)))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], arm9_sha256=native.digest(arm),
        font_sha256=native.digest(font), reviewed_draft=str(dialogue.REVIEW),
        draft_sha256=base.digest(dialogue.REVIEW), tested=tested,
        observed_revised_gameplay=False, installed_and_registered=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET))))
    print('Four draft pages passed the automatic planner and complete native glyph checks.')


if __name__ == '__main__':
    main()
