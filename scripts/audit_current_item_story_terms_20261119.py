"""Check the changed Glassmaking Guide page and original scene return."""
from inspect import getsource

from scripts import audit_rafael_iberian_aftermath_20261119 as previous
from scripts import replay_current_item_story_terms_20261119 as play
from scripts import verify_current_item_story_terms_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, build = play.base, play.build
PROOF = play.ROOT / "verified_glassmaking_replay.json"
NAMES = build.parent.VERIFY / "current_actor_getters.json"

if __name__ == "__main__":
    source = checked_text(getsource(previous.main), {
        '== 55 and plan["entry_opening_block"] == 44': '== 214 and plan["entry_opening_block"] == 44',
        '(74, 30)': '(26, 19)',
        'names_path = build.review.workflow.NAMES': 'names_path = NAMES',
        'startswith("DK4_MES_B55_")': 'startswith("DK4_MES_B214_")',
        '    assert len(pages) == 6\n    pages[offline.REWARD] = painter["retained_reward_display"]["pages"][0]':
            '    assert set(pages) == {"DK4_MES_B214_R0061"}',
        '    required = {f"DK4_MES_B55_R{n:04}" for n in (12, 24, 36, 40, 44, 54)}\n'
        '    assert required <= observed and observed == pages.keys() & set(speeches)':
            '    assert len(speeches) == 19 and observed == pages.keys()',
        '    transitions = []\n'
        '    for ident in ("DK4_MES_B55_R0036", offline.REWARD):\n'
        '        i = speeches.index(ident)\n'
        '        assert all(dict(words.values())[speeches[j]] != 254 for j in (i - 1, i + 1))\n'
        '        transitions.append(speeches[i - 1:i + 2])\n': '',
        'f"sofala_playback_': 'f"glassmaking_playback_',
        'revised_pages_verified=len(holds) - 1, distinct_modal_transitions=transitions,\n'
        '        retained_reward=offline.REWARD, normal_return_result=finished["result_words"],':
            'revised_pages_verified=len(holds), normal_return_result=finished["result_words"],',
        '{len(holds) - 1} revised pages, the retained reward and the original scene return.':
            '{len(holds)} revised pages and the original scene return.',
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::glassmaking_guide_gameplay", "exec"), scope)
    scope["main"]()
