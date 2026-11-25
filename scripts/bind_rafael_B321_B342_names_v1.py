"""Bind exact name fields, reusing matching Rafael3894 getter evidence."""
from pathlib import Path

from scripts import bind_rafael_B181_B200_names_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(Path(previous.__file__).read_text(encoding='utf-8'), {
    "A / 'Rafael_B181_B200_current2165_20261106'": "Path('work/Rafael_B321_B342_clean_20261106')",
    "ROOT / 'current_effective.json'": "ROOT / 'current_v1/current_effective.json'",
    """PRIOR = [A / p for p in (
    'Rafael_B170_B176_current1975_20261105/names_and_terms_v1.json',
    'Rafael_B168_B169_current1860_20261105/names_and_terms.json',
)]""": "PRIOR = [Path('work/Rafael_B301_B320_clean_20261106/names_and_terms_v1.json')]",
    "    actors = sorted({r['source_selector'] for g in current['groups'] for r in g['records']} - {254})":
        """    selectors = {r['source_selector'] for g in current['groups'] for r in g['records']}
    roles = load(ROOT/'roles.json')
    assert roles['runtime'] == ctx.receipt()
    actors = sorted({selector for selector in selectors if selector < 207}
                    | {r['resolved_actor_ID'] for r in roles['native_roles']['rows']})""",
    'assert len(actors) == 29': 'assert actors == [0, 2, 5, 8, 18, 94, 102, 147, 151, 161, 179, 201, 203, 204, 205, 206]',
    "        macro_ascii_lengths=previous_docs[0]['macro_ascii_lengths'],": "",
    '(CURRENT, *PRIOR, Path(__file__))': "(CURRENT, ROOT/'roles.json', *PRIOR, Path(__file__))",
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::exact-source-fields-and-own-runtime-name-getters', 'exec'), globals())
