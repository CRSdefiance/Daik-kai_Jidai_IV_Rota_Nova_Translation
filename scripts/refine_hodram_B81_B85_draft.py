"""Correct joined-word drafting errors and retain the exact first manuscript."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('translations/hodram_B81_B85_editorial_prose_v1.json')
OUT=Path('translations/hodram_B81_B85_editorial_prose_v2.json')
EDITS={
'DK4_MES_B81_R0057':"It can't be helped. There are so few people and so little money to work with.",
'DK4_MES_B84_R0012':'We might as well take the opportunity. Shall we go and watch?',
'DK4_MES_B85_R0054':'What, again?! Mom and Dad will try to stop you!',
'DK4_MES_B85_R0083':'Yes, yes, something like that. Before I knew it, Dad and the others had arranged it all without me.',
'DK4_MES_B85_R0105':"I think Mom and Dad want me to stop swinging a sword around all the time and settle down. It's so frustrating.",
}
if __name__=='__main__':
    assert not OUT.exists();doc=load(SOURCE);changed=[]
    for row in doc['records']:
        if row['id'] not in EDITS:continue
        english=EDITS[row['id']];assert row['english']!=english
        changed.append(dict(id=row['id'],before=row['english'],after=english))
        row.update(english=english,logical_English=english,
            planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+english)
        row['draft_refinement']='Correct accidental joined words; explicitly retain the small number of people and money in B81R57.'
    assert len(changed)==5
    doc.update(previous_manuscript=str(SOURCE),previous_manuscript_sha256=sha(SOURCE.read_bytes()),
        draft_refinements=changed,new_credit=0)
    save(OUT,doc);print('Five draft records refined;prior manuscript/producer preserved;135 individual prose decisions retained.')
