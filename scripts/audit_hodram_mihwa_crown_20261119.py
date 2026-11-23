"""Check Hodram's complete Crown replay against the native pages and names."""
from inspect import getsource

from scripts import audit_rafael_iberian_aftermath_20261119 as previous
from scripts import replay_hodram_mihwa_crown_20261119 as play
from scripts import verify_hodram_mihwa_crown_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, build = play.base, play.build
PROOF = play.ROOT / "verified_crown_replay.json"


if __name__ == "__main__":
    source = checked_text(getsource(previous.main), {
        '"route0_English"': '"route1_B89_revised_English"',
        '== 55 and plan["entry_opening_block"] == 44': '== 89 and plan["entry_opening_block"] == 42',
        '(74, 30)': '(29, 18)',
        'image.read_file("/data/SC0.DK4")': 'image.read_file(play.FILE)',
        '.blocks[44]': '.blocks[42]',
        'names_path = build.review.workflow.NAMES': 'names_path = build.review.NAMES',
        'startswith("DK4_MES_B55_")': 'startswith("DK4_MES_B89_")',
        '    assert len(pages) == 6\n    pages[offline.REWARD] = painter["retained_reward_display"]["pages"][0]':
            '    assert len(pages) == 7',
        '("original_SC_cache", 0, 44)': '("original_SC_cache", 1, 42)',
        '    required = {f"DK4_MES_B55_R{n:04}" for n in (12, 24, 36, 40, 44, 54)}\n'
        '    assert required <= observed and observed == pages.keys() & set(speeches)':
            '    assert len(speeches) == 18 and observed == pages.keys()',
        '    transitions = []\n'
        '    for ident in ("DK4_MES_B55_R0036", offline.REWARD):\n'
        '        i = speeches.index(ident)\n'
        '        assert all(dict(words.values())[speeches[j]] != 254 for j in (i - 1, i + 1))\n'
        '        transitions.append(speeches[i - 1:i + 2])\n': '',
        'f"sofala_playback_': 'f"crown_playback_',
        'original_commands_observed=len(observed_commands) - 10, checked_pages=holds,\n'
        '        revised_pages_verified=len(holds) - 1, distinct_modal_transitions=transitions,\n'
        '        retained_reward=offline.REWARD, normal_return_result=finished["result_words"],':
            'original_commands_observed=len(observed_commands) - 8, checked_pages=holds,\n'
            '        revised_pages_verified=len(holds), normal_return_result=finished["result_words"],',
        '{len(holds) - 1} revised pages, the retained reward and the original scene return.':
            '{len(holds)} revised pages and the original scene return.',
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::crown_gameplay_checks", "exec"), scope)
    scope["main"]()
