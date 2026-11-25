"""Immutable source/editorial refinements after the first complete native preview."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

OLD=Path('translations/hodram_B81_B89_editorial_manuscript_v1.json')
OUT=Path('translations/hodram_B81_B89_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not OUT.exists()
    doc=deepcopy(load(OLD)); changes=[]
    fixes={
        'DK4_MES_B84_R0012':('Shall we go and watch while we have the chance?',
            'Render the source opportunity and invitation as one natural question. The first draft redundantly introduced the opportunity before asking; this is a prose-cadence refinement, not shortening good text for fit.'),
        'DK4_MES_B85_R0186':("With that awkward stance of yours, you couldn't even beat a child.",
            'Restore the explicit awkward/timid posture in へっぴり腰. This longer, sharper taunt preserves Cristina\'s assessment; it is not fit-driven shortening.'),
    }
    for row in doc['records']:
        if row['id'] not in fixes:continue
        english,note=fixes[row['id']]; before=row['english']
        assert row['decision']=='revision' and not row['review']['formatting']
        prefix=row['planned_English_markup'].split('}',1)[0]+'}'
        row.update(english=english,logical_English=english,planned_English_markup=prefix+english,
            localization_note=row['localization_note']+' '+note,finding=row['finding']+' '+note)
        changes.append(dict(id=row['id'],before=before,after=english,reason=note))
    assert len(changes)==2 and len(doc['records'])==306
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        post_native_visual_prose_refinements=changes,unchanged_records_reused_exactly=304)
    doc['evidence'][str(OLD)]=sha(OLD.read_bytes());doc['evidence'][__file__]=sha(Path(__file__).read_bytes())
    save(OUT,doc);print(dict(records=306,revisions=doc['revised'],retentions=doc['retained'],refined=2,new_credit=0))
