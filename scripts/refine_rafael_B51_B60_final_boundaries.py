"""Resolve two remaining noun orpredicate fragments seen in the updated native pages."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')

if __name__=='__main__':
    old=ROOT/'visual_preferences_v3.json';out=ROOT/'visual_preferences_v4.json';assert not out.exists()
    doc=deepcopy(load(old))
    doc['records']['DK4_MES_B60_R0399']['line_phrases']=['enormous profits']
    doc['records']['DK4_MES_B60_R0399']['reason']='The updated native first page stranded profits alone;keep enormous-profits together while retaining the complete conditional on the second page.'
    doc['records']['DK4_MES_B60_R0486']['line_phrases']=['Proof of Conquest is','that little mustached bastard']
    doc['records']['DK4_MES_B60_R0486']['reason']='Keep the factual predicate intact on page1 andthe complete insult noun phrase intact on page2;the conditional intentionally crosses the native page boundary without orphaning is orbastard.'
    doc.update(previous_preferences=str(old),previous_preferences_sha256=sha(old.read_bytes()),
        updated_native_sheets_directly_viewed=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(out,doc);print('Two directly viewed page-boundary refinements saved;no prose orgeometry changes.')
