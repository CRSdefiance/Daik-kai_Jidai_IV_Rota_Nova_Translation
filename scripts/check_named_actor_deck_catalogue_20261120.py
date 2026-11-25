"""Render the nine remaining personal names through both original Deck panel calls."""

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import review_named_actor_catalogue_20261120 as review
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_barmaid_town_labels_20261115 import CALLERS
from scripts.stage_barmaid_town_labels_20261115 import paint


base = review.base
PROOF, SHEET = (review.ROOT / n for n in ('deck_name_planes.json', 'deck_name_planes.png'))


def main():
    assert not PROOF.exists() and not SHEET.exists()
    draft = base.load(review.DRAFT)
    current = draft['runtime']
    ctx = RegisteredRuntime(current['release_proof'], current['startup_proof'], captain=current['captain'])
    assert ctx.receipt() == current
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    guard = bytes(cpu.mem_read(ctx.actor_root, 0x1A04))
    font = GameAsciiFont.from_arm9(ctx.arm)
    rows = []
    sheet = Image.new('RGB', (972, 62 * len(draft['records'])), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(draft['records']):
        ident, english = row['actor_ID'], row['english']
        clauses = []
        for col, caller in enumerate(CALLERS):
            obj = ctx.actor_root + 4 + ident * 32
            panel, result = paint(cpu, font, obj, english, caller, True)
            clauses.append(result)
            x, y = col * 494 + 8, index * 62
            draw.text((x, y + 4), f'{ident}  {english}  {caller[-1]} cells', fill='white')
            line = panel.crop((0, 24, panel.width, 36)).point(lambda p: 25 if p else 245)
            sheet.paste(line.resize((line.width * 2, 24), Image.Resampling.NEAREST), (x, y + 24))
        rows.append(dict(actor_ID=ident, english=english, offline_supplied_actor_Draw_cases=clauses))
    assert len(rows) == 9 and not provider.reads
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == guard
    sheet.save(SHEET)
    base.save(PROOF, dict(runtime=current, rows=rows, draft_sha256=base.digest(review.DRAFT),
        sheet={'path': str(SHEET), 'sha256': base.digest(SHEET)},
        native_full_mask_current_both_widths=True, actual_Deck_selection_verified=False))
    print('Passed 18 complete native Deck name masks using the original callers.')


if __name__ == '__main__':
    main()
