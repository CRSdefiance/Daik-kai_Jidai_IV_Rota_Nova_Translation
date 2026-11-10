"""Keep the complete get-it/question-tag/laugh unit together instead of orphaning Hah!."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
if __name__=='__main__':
    parent=ROOT/'preferences_v3.json';out=ROOT/'preferences_v4.json';assert not out.exists()
    doc=load(parent);entry=doc['records']['DK4_MES_B82_R0183']
    assert entry['line_phrases']==["don't get it"]
    entry['line_phrases']=['get it, do you? Hah!']
    doc.update(previous_preferences=str(parent),previous_preferences_sha256=sha(parent.read_bytes()),
        refinement_reason='First exact phrase preference stranded the final complete laugh as Hah!. Keep the full get it/tag/laugh unit together and preserve every word.',
        failed_v3_diagnostics=str(ROOT/'automatic_subset_v3/diagnostics.json'),new_credit=0)
    save(out,doc)
