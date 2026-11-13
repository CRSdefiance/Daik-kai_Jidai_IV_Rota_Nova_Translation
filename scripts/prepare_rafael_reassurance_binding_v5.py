"""Bind revised logical prose to its planning input; preserve the earlier sealed draft."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
    for before,after in [(Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v4.json'),Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v5.json')),
                         (root/'formatting_input_v4.json',root/'formatting_input_v5.json')]:
        assert not after.exists();doc=deepcopy(load(before))
        row=next(r for r in doc['records'] if r['id']=='DK4_MES_B69_R0069')
        assert row['english']=='Does it look bad on me?'
        row['logical_English']=row['english']
        if 'planned_English_markup' in row:row['planned_English_markup']='{SPEAKER:FE}'+row['english']
        doc.update(previous_manuscript=str(before),previous_manuscript_sha256=sha(before.read_bytes()),
            source_first_independent_draft_kept_as_historical_not_rewritten=True,
            producer_sha256=sha(Path(__file__).read_bytes()))
        save(after,doc)
    print('Logical/proposed-markup bindings updated; original independent draft andfailed diagnostic plan preserved.')
