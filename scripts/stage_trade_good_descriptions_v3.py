"""Use the four-row Price Info geometry proved by the ordinary Lisbon replay."""

from itertools import combinations
from inspect import getsource
from types import FunctionType

from scripts import stage_trade_good_descriptions_v1 as first
from scripts import stage_trade_good_descriptions_v2 as second
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait


ROOT = first.ROOT.with_name('trade_good_descriptions_staged_20261111_v3')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = second.OUTPUT
ROWS_PER_PAGE = 4


def four_rows(words):
    candidates = []
    for i, j, k in combinations(range(1, len(words)), 3):
        rows = tuple(' '.join(part) for part in (words[:i], words[i:j], words[j:k], words[k:]))
        widths = [len(line) for line in rows]
        if not all(17 <= width <= 36 for width in widths):
            continue
        awkward = sum(line.rsplit(' ', 1)[-1].lower() in second.WEAK_ENDS for line in rows)
        balance = sum((width * 4 - sum(widths)) ** 2 for width in widths)
        candidates.append((awkward, balance, rows))
    return min(candidates)[2] if candidates else None


def plan(text):
    lines = first.rows_for(text)
    if len(lines) <= ROWS_PER_PAGE:
        return lines
    words = text.split()
    choices = []
    for stop in range(1, len(words)):
        left, right = ' '.join(words[:stop]), ' '.join(words[stop:])
        if not (76 <= len(left) <= 147 and 27 <= len(right) <= 108):
            continue
        head, tail = four_rows(words[:stop]), first.rows_for(right)
        if head is None or len(tail) > 2:
            continue
        last, next_word = words[stop - 1], words[stop].lower()
        boundary = (0 if last.endswith(('.', '!', '?')) else 1 if last.endswith((',', ';'))
                    else 2 if next_word in second.CLAUSE_STARTS else 3)
        if last.lower() in second.WEAK_ENDS:
            boundary += 2
        choices.append((boundary, abs(len(right) - 51), -len(left), [*head, *tail]))
    return min(choices)[3] if choices else lines


def native_pages(raster, arm, kanji, text):
    return FunctionType(first.native_pages.__code__, vars(first) | {'pagination': aligned_pages})(
        raster, arm, kanji, text)


aligned_pages = FunctionType(first.pagination.__code__, first.pagination.__globals__ | {
    'HEIGHT': 64, 'render': render_portrait,
})


def stage_environment():
    env = vars(first) | globals()
    env['repack'] = FunctionType(first.repack.__code__, env)
    return env


def main():
    assert OUTPUT.exists()
    source = checked_text(getsource(first.main), {
        "g['y'] + 12 <= 48": "g['y'] + 12 <= 64",
        '    sheet_maker = FunctionType(sheets.preview_sheets.__code__, vars(sheets) | {\'ROOT\': ROOT})\n'
        '    views = sheet_maker(labels, pages)':
            "    views = portrait_sheets(ROOT, [(f'{label[\"message_ID\"]} {\" · \".join(label[\"arguments\"])}', page) "
            'for label, page in zip(labels, pages, strict=True)])',
    })
    env = stage_environment()
    exec(compile(source, __file__ + '::confirmed-four-row-price-info', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
