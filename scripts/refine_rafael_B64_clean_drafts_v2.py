"""Retain the first draft;remove two unnecessary stumbles/assertions after whole-exchange reread."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
if __name__=='__main__':
    source=ROOT/'B64_120_logical_English_drafts_v1.json';output=ROOT/'B64_120_logical_English_drafts_v2.json';assert not output.exists()
    doc=deepcopy(load(source));changes=[]
    updates={202:("Um... ...I, uh...","Um... Well, I...",'Keep the apology hesitation asnatural spoken stumbling without adjacent redundant ellipses.'),
        485:('(What can we do ourselves...? There must be something.)','(What can we do to help them...?)',
            'Retain the source open question about their own contribution;remove the extra optimistic assertion added in the first draft.')}
    for row in doc['records']:
        index=row['source_reference']['record_index']
        if index not in updates:continue
        old,new,note=updates[index];assert row['english']==old and row['earlier_English_unconsulted']
        row.update(english=new,localization_note=note)
        assert all(new.count('{MACRO:'+key+'}')==count for key,count in row['source_macros'].items())
        changes.append(dict(id=row['id'],source_reference=row['source_reference'],previous_English=old,English=new,reason=note))
    assert len(changes)==2
    doc.update(previous_draft=str(source),previous_draft_sha256=sha(source.read_bytes()),whole_exchange_refinements=changes,
        all_first_draft_records_andprovenance_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc)
    print('120-source-draft v2:two dialogue refinements;first draft preserved,older English still unread,zero credit.',flush=True)
