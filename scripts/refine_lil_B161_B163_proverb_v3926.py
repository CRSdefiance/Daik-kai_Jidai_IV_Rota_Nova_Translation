"""Keep the source-faithful proverb; distinguish noun will in its complete first clause."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    ROOT=Path('work/analysis/lil_B161_B163_proverb_v3926');assert not ROOT.exists();failed=Path('work/analysis/lil_B161_B163_layout_v3924/all45_paragraph_layout_QA.json');v=read(failed);assert len(v['failures'])==1 and v['failures'][0]['id']=='DK4_MES_B163_R0113';changes={
        'def _terminal_label(value):':'''def _noun_will_at(labels,index):
    # Exact complete first clause: will is a noun, not a stranded auxiliary.
    return (index >= 3 and labels[index].endswith(',')
        and tuple(_word(v) for v in labels[index-3:index+1]) == ('where',"there's",'a','will'))

def _terminal_label(value):''',
        "PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('strawberry','jam')":"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('where',\"there's\"),(\"there's\",'a'),('strawberry','jam')",
        '(end_word in weak and (end_word in BASE_WEAK or not _terminal_label(labels[end])))':'(end_word in weak and not _noun_will_at(labels,end) and (end_word in BASE_WEAK or not _terminal_label(labels[end])))',
        "'_split_pair':_split_pair}":"'_split_pair':_split_pair,'_noun_will_at':_noun_will_at}",
        'if end in STRONG_ENDINGS and end not in qa.WEAK_LINE_ENDINGS and not _terminal_label(value):':'if end in STRONG_ENDINGS and end not in qa.WEAK_LINE_ENDINGS and not _terminal_label(value) and not _noun_will_at(words,len(words)-1):'}
    pairs=[derive('dk4tool/dialogue/lil_B161_B163_layout_v1.py','dk4tool/dialogue/lil_B161_B163_layout_v2.py',changes)]
    pairs.append(derive('scripts/plan_lil_B161_B163_layout_v3924.py','scripts/plan_lil_B161_B163_layout_v3927.py',{'lil_B161_B163_layout_v1':'lil_B161_B163_layout_v2','lil_B161_B163_layout_v3924':'lil_B161_B163_layout_v3927'}))
    pairs.append(derive('scripts/verify_lil_B161_B163_fonts_v3925.py','scripts/verify_lil_B161_B163_fonts_v3928.py',{'lil_B161_B163_layout_v1':'lil_B161_B163_layout_v2','lil_B161_B163_fonts_v3925':'lil_B161_B163_fonts_v3928'}))
    from dk4tool.dialogue import lil_B161_B163_layout_v2 as codec
    positives=[['Where',"there's",'a','will,']];negatives=[['I','will,'],["There's",'a','will,'],['where',"there's",'a','will'],['where',"there's",'the','will,'],['where','there','is','a','will,']];assert all(codec._noun_will_at(x,len(x)-1) for x in positives) and not any(codec._noun_will_at(x,len(x)-1) for x in negatives)
    ROOT.mkdir(parents=True);save(ROOT/'noun_will_phrase_refinement_and_preserved_failed_plan.json',dict(failed_plan=str(failed),failed_plan_sha256=sha(failed.read_bytes()),finding='The first clause of Where there is a will uses will as a noun. A complete comma-terminated clause can end a display row; a stranded auxiliary cannot.',all_authored_words_and_punctuation_unchanged=True,no_source_or_control_or_geometry_change=True,no_wording_glyph_bounds_pagination_macro_or_control_waiver=True,scoped_exact_noun_clause_positive_cases=positives,rejected_nonmatching_auxiliary_or_incomplete_clause_cases=negatives,derived_tools=pairs,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
