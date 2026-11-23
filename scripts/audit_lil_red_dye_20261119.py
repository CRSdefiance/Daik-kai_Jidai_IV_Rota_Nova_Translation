"""Match the revised Amsterdam opening to its native body and nameplate masks."""
from inspect import getsource
from pathlib import Path

from scripts import audit_rafael_iberian_aftermath_20261119 as previous
from scripts import replay_lil_red_dye_20261119 as play
from scripts import verify_lil_red_dye_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, build = play.base, play.build
NAMES = build.parent.parent.VERIFY / "current_actor_getters.json"
PROOF = play.ROOT / "verified_amsterdam_replay.json"

if __name__ == "__main__":
    source = checked_text(getsource(previous.main), {
        '"route0_English"': '"route2_B129_revised_English"',
        '== 55 and plan["entry_opening_block"] == 44': '== 129 and plan["entry_opening_block"] == 22',
        '(74, 30)': '(45, 27)',
        'image.read_file("/data/SC0.DK4")': 'image.read_file(play.FILE)',
        '.blocks[44]': '.blocks[22]',
        'names_path = build.review.workflow.NAMES': 'names_path = NAMES',
        'startswith("DK4_MES_B55_")': 'startswith("DK4_MES_B129_")',
        '    assert len(pages) == 6\n    pages[offline.REWARD] = painter["retained_reward_display"]["pages"][0]':
            '    assert len(pages) == 2',
        '("original_SC_cache", 0, 44)': '("original_SC_cache", 2, 22)',
        '    required = {f"DK4_MES_B55_R{n:04}" for n in (12, 24, 36, 40, 44, 54)}\n'
        '    assert required <= observed and observed == pages.keys() & set(speeches)':
            '    offline_ids = sorted(set(dict(words.values())) - set(speeches))\n'
            '    assert len(speeches) == 26 and observed == pages.keys()\n'
            '    assert offline_ids == ["DK4_MES_B129_R0123"]',
        '    transitions = []\n'
        '    for ident in ("DK4_MES_B55_R0036", offline.REWARD):\n'
        '        i = speeches.index(ident)\n'
        '        assert all(dict(words.values())[speeches[j]] != 254 for j in (i - 1, i + 1))\n'
        '        transitions.append(speeches[i - 1:i + 2])\n': '',
        'f"sofala_playback_': 'f"amsterdam_playback_',
        'original_commands_observed=len(observed_commands) - 10, checked_pages=holds,\n'
        '        revised_pages_verified=len(holds) - 1, distinct_modal_transitions=transitions,\n'
        '        retained_reward=offline.REWARD, normal_return_result=finished["result_words"],':
            'original_commands_observed=len(observed_commands) - 9, checked_pages=holds,\n'
            '        revised_pages_verified=len(holds), offline_only_in_observed_block=offline_ids, normal_return_result=finished["result_words"],',
        '{len(holds) - 1} revised pages, the retained reward and the original scene return.':
            '{len(holds)} revised pages and the original Amsterdam return.',
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::amsterdam_gameplay_checks", "exec"), scope)
    scope["main"]()
