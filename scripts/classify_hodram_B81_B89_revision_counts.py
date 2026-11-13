"""Separate substantive wording/name changes from six punctuation-width revisions."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

FINAL=Path('translations/hodram_B81_B89_contextual_final_review_v1.json')
OUT=Path('work/analysis/Hodram_B81_B89_editorial_20261101/revision_classification.json')
if __name__=='__main__':
    assert not OUT.exists();doc=load(FINAL)
    glyphs={'DK4_MES_B81_R0024':('？','?'),'DK4_MES_B85_R0174':('！！','!!'),
        'DK4_MES_B86_R0066':('！？','!?'),'DK4_MES_B87_R0058':('！','!'),
        'DK4_MES_B88_R0067':('…！','...!'),'DK4_MES_B88_R0129':('？？？','???')}
    rows=[]
    for row in doc['records']:
        if row['id'] in glyphs:
            assert row['decision']=='revision'
            assert (row['prior_macro_normalized_comparison'],row['english'])==glyphs[row['id']]
            category='punctuation-glyph-only'
        else:category='justified-retention' if row['decision']=='retention' else 'wording-or-name-localization'
        rows.append(dict(id=row['id'],file_path=row['file_path'],source_reference=row['source_reference'],
            current_reference=row['current_reference'],category=category))
    assert sum(r['category']=='wording-or-name-localization' for r in rows)==216
    assert sum(r['category']=='justified-retention' for r in rows)==84
    save(OUT,dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),records=rows,
        wording_orname_revisions=216,punctuation_glyph_only_revisions=6,justified_retentions=84,
        additional_Emilio_name_metadata_glyph_fix=1,three_new_draft_page_continuity_findings_resolved=True,
        not_all_wording_revisions_are_runtime_defects=True,validation_passes_add_no_bug_orcompletion_count=True,
        registered_release_andcompletion_credit_pending=True,new_credit=0))
    print('216 wording/name revisions +6 punctuation glyph revisions +84 retentions;one additional name-metadata fix. No new credit.')
