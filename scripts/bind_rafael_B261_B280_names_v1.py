"""Bind source fields and both name consumers on Rafael3514's own startup."""
from pathlib import Path

from scripts import bind_rafael_B181_B200_names_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(Path(previous.__file__).read_text(encoding='utf-8'), {
    "A / 'Rafael_B181_B200_current2165_20261106'": "Path('work/Rafael_B261_B280_clean_20261106')",
    "ROOT / 'current_effective.json'": "ROOT / 'current_v1/current_effective.json'",
    """PRIOR = [A / p for p in (
    'Rafael_B170_B176_current1975_20261105/names_and_terms_v1.json',
    'Rafael_B168_B169_current1860_20261105/names_and_terms.json',
)]""": 'PRIOR = []',
    "    actors = sorted({r['source_selector'] for g in current['groups'] for r in g['records']} - {254})":
        """    selectors = {r['source_selector'] for g in current['groups'] for r in g['records']}
    roles = load(ROOT/'roles.json')
    assert roles['runtime'] == ctx.receipt()
    actors = sorted((selectors - {207,254}) | {r['resolved_actor_ID'] for r in roles['native_roles']['rows']} | {65})
    assert all(actor < 207 for actor in actors)""",
    '    assert len(actors) == 29': '    assert 65 in actors and 151 in actors',
    'exact_prior_ARM9_COMMON_actor_root_and_font=True': 'all_scoped_getters_fresh_on_registered_ARM9=True',
    "        macro_ascii_lengths=previous_docs[0]['macro_ascii_lengths'],": "",
    '(CURRENT, *PRIOR, Path(__file__))': "(CURRENT, ROOT/'roles.json', Path(__file__))",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::all-current-name-fields-and-getters-fresh', 'exec'), globals())
