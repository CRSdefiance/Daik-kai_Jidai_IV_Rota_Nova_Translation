"""Correct the source-bound complete locative boundary without editing words or guards."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B183_locative_wrap_v4939')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B183_layout_v1.py','dk4tool/dialogue/lil_B183_layout_v2.py',{
        'No global helper orprevious profile is modified.':
        'The exact B183 successor recognizes complete locative over there as a valid boundary. There remains weak elsewhere. No global helper orprevious profile is modified.',
        'source=inspect.getsource(layout._balanced_wrap)':
        "def _complete_locative_at(labels,index):\n    # In this exchange over there completes the preceding noun phrase.\n    # It is not the existential there of a stranded there is.\n    return index>=1 and tuple(_word(v) for v in labels[index-1:index+1])==('over','there')\n\nsource=inspect.getsource(layout._balanced_wrap)",
        "end_word in weak and not _noun_will_at(labels,end) and (end_word in BASE_WEAK":
        "end_word in weak and not _noun_will_at(labels,end) and not _complete_locative_at(labels,end) and (end_word in BASE_WEAK",
        "'_noun_will_at':_noun_will_at}":"'_noun_will_at':_noun_will_at,'_complete_locative_at':_complete_locative_at}",
        'and not _noun_will_at(words,len(words)-1):':'and not _noun_will_at(words,len(words)-1) and not _complete_locative_at(words,len(words)-1):'
    }))
    tools.append(derive('scripts/plan_lil_B183_layout_v4936.py','scripts/plan_lil_B183_layout_v4940.py',{
        'lil_B183_layout_v1':'lil_B183_layout_v2','layout_v4936':'layout_v4940',
        'lil_B183_editorial_manuscript_v2':'lil_B183_editorial_manuscript_v4'}))
    tools.append(derive('scripts/verify_lil_B183_fonts_v4937.py','scripts/verify_lil_B183_fonts_v4941.py',{
        'lil_B183_layout_v1':'lil_B183_layout_v2','fonts_v4937':'fonts_v4941',
        'lil_B183_editorial_manuscript_v2':'lil_B183_editorial_manuscript_v4'}))
    tools.append(derive('scripts/approve_lil_B183_native_v4938.py','scripts/approve_lil_B183_native_v4942.py',{
        'lil_B183_layout_v1':'lil_B183_layout_v2','native_approval_v4938':'native_approval_v4942','fonts_v4937':'fonts_v4941',
        'lil_B183_editorial_manuscript_v2':'lil_B183_editorial_manuscript_v4',
        'lil_B183_editorial_manuscript_v3':'lil_B183_editorial_manuscript_v5',
        'no_new_phrase_exception_shared_metric_guard_or_manual_break=True':
        'complete_source_supported_locative_boundary_reviewed=True,no_shared_metric_guard_or_manual_break_change=True',
        "    validate_natural_dialogue_batch(doc)":
        "    comparison=read('work/analysis/lil_B183_locative_wrap_v4939/before_after_all25_semantic_and_layout_comparison.json')\n    assert comparison['only_changed_record_IDs']==['DK4_MES_B183_R0035'] and comparison['all25_words_controls_and_prose_unchanged']\n    doc['source_bound_wrap_refinement_proof']='work/analysis/lil_B183_locative_wrap_v4939/before_after_all25_semantic_and_layout_comparison.json'\n    doc['source_bound_wrap_refinement_proof_sha256']=sha(Path(doc['source_bound_wrap_refinement_proof']).read_bytes())\n    validate_natural_dialogue_batch(doc)"
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_refinement.json',dict(tools=tools,
        finding='R0035 question fits one row but broad weak-there classification shifts its break backward.',
        complete_locative_boundary='That one over there',source_support='それより、あっちの方がいい作品に決まっておる',
        existing_sourcebound_STRONG_ENDINGS_and_PROTECTED_BOUNDARIES_lists_unchanged=True,
        no_prose_source_command_shared_helper_metric_width_guard_or_manual_break_change=True,
        earlier_versions_and_native_proofs_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B183 v2 locative-boundary successor;all wording,width,guards and historical versions preserved.')
