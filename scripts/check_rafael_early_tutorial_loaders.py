"""Reload SC0; reuse only byte-identical B50 parent cases and unchanged native code."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text


def parent_adapter(prior, old_modes):
    return checked_text(prior['source_owned_parent_adapter'], {
        'source_words, reads, cache_events = {}, [], []':
            "source_words, reads, cache_events = {r['PC']:bytes.fromhex(r['hex']) for r in REUSED_WORDS}, [], []",
        '                for mode in (0, 1):':
            """                if index not in CHANGED_BLOCKS:
                    assert {c['mode'] for c in REUSED_PARENT_CASES[index]}=={0,1}
                    assert all(c['source_block_sha256']==sha(block) and c['route']==route for c in REUSED_PARENT_CASES[index])
                    cases.extend(REUSED_PARENT_CASES[index])
                    continue
                for mode in (0, 1):""",
    })


source = checked_text(Path('scripts/check_pending_scene_loaders.py').read_text(encoding='utf-8'), {
    'work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json':
        'work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/reconstruction_v2/reconstruction.json',
    'work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json':
        'work/analysis/Rafael_B50_loaders_v8152/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
    '/data/SC1.DK4': '/data/SC0.DK4',
    "c['route'] == 1": "c['route'] == 0",
    'changed == set(range(61, 71))': 'changed == {42,43}',
    "'EXPECTED_ACTIONS': 326": "'EXPECTED_ACTIONS': 344",
    "'REUSED_PARENT_CASES': cases": "'REUSED_PARENT_CASES': cases, 'REUSED_WORDS': old_modes['executed_source_words']",
    "compile(prior['source_owned_parent_adapter'],": "compile(parent_adapter(prior,old_modes),",
    "'pending-Hodram-research'": "'pending-Rafael-tutorial-research'",
    'len(fresh) == 20 and len(reused) == 630': 'len(fresh) == 4 and len(reused) == 682',
    "len(loaded['routes'][0]['actions']) == 326": "len(loaded['routes'][0]['actions']) == 344",
    'fresh_whole_archive_loads_andcache_hits=325, fresh_parent_cases=20,':
        'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=4,',
    'exact_reused_parent_cases=630, original_EV1_action_count=326,':
        'exact_reused_parent_cases=682, original_EV0_action_count=344,',
    '325 whole native loads/cache hits;20 fresh and630 exact reused parent cases pass.':
        '343 whole native loads/cache hits;4 fresh and682 exact reused parent cases pass.',
})
exec(compile(source, __file__ + '::same-native-loader-SC0-exact-parent-reuse', 'exec'), globals())
