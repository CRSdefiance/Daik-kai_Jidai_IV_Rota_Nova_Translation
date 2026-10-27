"""Prepare approval of the viewed B177 final native planes and unchanged prose."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_approval_preparation_v4622')
assert not ROOT.exists()
source=Path('scripts/approve_lil_B176_native_v4572.py')
text=source.read_text(encoding='utf-8')
start=text.index("'review':'Viewed all10")
end=text.index("'})",start)
old_review=text[start:end]
new_review="'review':'Viewed all ten final native panels across two sheets individually. Owner enthusiasm and red-color passion develop into consuming youthful-love recollection;Cook responds with dry politeness,then practical compliance and casual repeated acknowledgment. The cooking/selling order,encouragement,distinctive laugh and prospective impersonal Genoa notice remain complete. All five retentions stay coherent. Four tightened phrase boundaries keep takes-me-back,consumed-me and start-selling together without changing words or geometry. Every leading/internal/final glyph,punctuation,bounds and single-page consumption passes;the long recollection occupies four complete rows. No added madam,lover,rank,relationship,active boom or earlier location. Offline rendering;actual B177 gameplay remains pending.'"
old_checks="""    assert codec._complete_clause_at('Yes! With a flavor like this,'.split(),5)
    assert not codec._complete_clause_at(['this,'],0)
    assert not codec._complete_clause_at('Buy this,'.split(),1)
    assert not codec._complete_clause_at('With a flavor like this'.split(),4)
"""
new_checks="""    for labels,index in [(['takes','me','back'],0),(['takes','me','back'],1),(['consumed','me'],0),(['start','selling'],0)]:
        assert codec._split_pair(labels,index)
    for labels in [['takes','another'],['consumed','by'],['start','right'],['me','when']]:
        assert not codec._split_pair(labels,0)
"""
tool=derive(source,'scripts/approve_lil_B177_native_v4622.py',{
    'B176':'B177','lil_B176':'lil_B177','lil_B176_layout_v4':'lil_B177_layout_v3',
    'native_approval_v4572':'native_approval_v4622','fonts_v4570':'fonts_v4621',
    "INPUT=Path('translations/lil_B176_editorial_manuscript_v2.json')":
        "INPUT=Path('translations/lil_B177_editorial_manuscript_v4.json')",
    "OUTPUT=Path('translations/lil_B176_editorial_manuscript_v3.json')":
        "OUTPUT=Path('translations/lil_B177_editorial_manuscript_v5.json')",
    '.blocks[176]':'.blocks[177]','block=176':'block=177',
    old_review:new_review,old_checks:new_checks,
    "sum(bool(r.get('qa_waivers')) for r in doc['records'])==3":"sum(bool(r.get('qa_waivers')) for r in doc['records'])==5",
    'narrow_row_count_notes=3':'narrow_row_count_notes=5',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,two_final_native_sheets_individually_viewed=True,
    all_original_prose_unchanged_through_two_narrow_wrap_refinements=True,
    four_positive_four_negative_phrase_boundary_checks_required=True,
    no_gameplay_or_ledger_credit_added=True,full_goal_complete=False))
