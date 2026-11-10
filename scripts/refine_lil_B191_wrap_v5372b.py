"""Use two safe rows while preserving the full question and every following word."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_wrap_finding_v5372b')
if __name__=='__main__':
    assert not ROOT.exists()
    oldreason='For? completes this exact full question. Its ordinary sentence-boundary soft wrap keeps both the question and following warning intact in two safe rows. All words,216px width,glyphs,guards,pair phase,bounds,controls and one-page checks remain. No global preposition waiver or authored break.'
    reason='In this exact paragraph,the whole question remains together and the following warning begins on the same row. An ordinary complete-word wrap after be uses two substantial safe rows and keeps too late once it is sold out together. All original words,216px width,glyphs,guards,pair phase,bounds,controls and one-page checks remain. No global weak-word waiver or authored break.'
    rows=[derive('dk4tool/dialogue/lil_B191_layout_v2.py','dk4tool/dialogue/lil_B191_layout_v3.py',{
        "and labels[index:index+2]==['for?',\"It'll\"])":"and labels[index:index+2] in (['for?',\"It'll\"],['be','too']))",
        "line 1 ends with weak wrap word 'for?'":"line 1 ends with weak wrap word 'be'",
        "['What are you waiting for?',\"It'll be too late once it's sold out.\"]":"[\"What are you waiting for? It'll be\",\"too late once it's sold out.\"]",
        "after_word='for?'":"after_word='be'",oldreason:reason,
    })]
    rows.append(derive('scripts/plan_lil_B191_layout_v5373.py','scripts/plan_lil_B191_layout_v5373b.py',{
        'lil_B191_layout_v2':'lil_B191_layout_v3','layout_v5373':'layout_v5373b',
    }))
    rows.append(derive('scripts/verify_lil_B191_fonts_v5374.py','scripts/verify_lil_B191_fonts_v5374b.py',{
        'lil_B191_layout_v2':'lil_B191_layout_v3','fonts_v5374':'fonts_v5374b',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'exact_R64_safe_two_row_revision.json',dict(tools=rows,
        initial_complete_sentence_per_row_expectation_rejected_by_native_width_guard=True,
        second_sentence37_characters_exceeds_guarded_row_unchanged=True,
        source_bound_two_row_compromise_after_be_preserves_complete_question_and_warning=True,
        reason=reason,all_words_font_width_guard_metrics_and_other_records_must_stay_exact=True,
        initial_stopped_planner_and_codec_preserved=True,no_credit=True,full_goal_complete=False))
