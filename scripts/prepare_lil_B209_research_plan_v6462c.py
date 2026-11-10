"""Preserve the failed quote preparation and derive the complete source-bound research planner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_layout_tools_v6462c')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/plan_lil_B209_research_v6462.py','scripts/plan_lil_B209_research_v6462c.py',{
        'layout_research_v6462\')':'layout_research_v6462c\')',
        "maximum=8 if long else 4":"maximum=8 if row['id'] in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] else 4",
        "if long and r==3 and not final and words[stop-1]!='Tokugawa,':continue":"if r==3 and not final and row['id'] in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] and words[stop-1]!=('Tokugawa,' if long else 'Asia.'):continue",
        "said'.split())":"said them us me him her'.split())",
        "PAIRS={":"WEAK.update({\"that's\",\"there's\",\"i'll\",\"you've\"})\nPAIRS={",
        "('just','like')}":"('just','like'),('typical','of'),('maybe',\"i'll\"),('come','in'),(\"that's\",'yukihisa')}",
        "weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS))":"particle_in=(row['id']=='DK4_VOICE_B209_C8_T188' and stop>=2 and words[stop-2:stop]==['come','in'])\n            weak=int(not final and (((word in WEAK and not terminal) and not particle_in) or pair in PAIRS))",
        "first_letter_short_intro_row_reason='Word has reached me is a complete introductory clause. The next material contains a long legendary/cursed Muramasa noun phrase. The entire Word has reached me of the legendary string is36 characters and cannot precede a guarded LF within the native phase limit. The scoped planner preserves syntax and names instead of narrowing the viewport or altering prose.'":"first_letter_wrap_reasons_pending_exact_visual_review=True,second_letter_page_boundary='East Asia. / For now,',second_letter_reason='The apparent concealment report completes before the provisional news-passing sentence. Two original four-row native pages are researched without shortening the135-character prose or adding commands.',come_in_particle_boundary_reason='In come in,the final in is a completed phrasal-verb particle;from Yukihisa is the following sender adjunct. Only the exact source-bound style4 introduction receives this grammatical distinction,not a global preposition waiver.'",
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,prior_four_row_second_paragraph_rejection_and_quote_syntax_failure_preserved=True,both_long_letter_paragraphs_research_original_four_row_native_pagination=True,no_prose_words_changed_or_formatting_gates_approved=True,full_goal_complete=False))
