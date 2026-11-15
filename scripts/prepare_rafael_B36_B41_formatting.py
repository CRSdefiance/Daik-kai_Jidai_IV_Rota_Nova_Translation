"""Consolidate the 175 individual comparisons and prepare unwrapped formatting input."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
OUT=Path('work/analysis/Rafael_B36_B41_formatting_20261104')
FINAL=Path('translations/rafael_B36_B41_contextual_editorial_manuscript_v1.json')
CURRENT=Path('work/analysis/Rafael_B36_B41_current_20261104/current_effective.json')

if __name__=='__main__':
    assert not OUT.exists() and not FINAL.exists()
    parts=[ROOT/'B36_B37_92_whole_exchange_comparison_v1.json',ROOT/'B38_B41_83_whole_exchange_comparison_v1.json']
    rows=[deepcopy(r) for p in parts for r in load(p)['records']]
    current=load(CURRENT)
    prior={r['id']:r for g in current['groups'] for r in g['records']}
    assert len(rows)==len(prior)==175 and len({r['id'] for r in rows})==175
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(76,99)
    for row in rows:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert all(row[k]==prior[row['id']][k] for k in ['source_reference','current_reference','source_hex','current_hex'])
        assert not any(t in row['english'] for t in ['\n','{LB','{ALIGN','{PAD}','Ｉ'])
        assert all(row['english'].count('{MACRO:'+m+'}')==bytes.fromhex(row['source_hex'])[1:].count(m.encode()) for m in ['FI','FA','FO','FU'])
        row.update(kind='progressive',source_record_index=row['source_reference']['record_index'],source_native_extent=row['native_extent'],
            planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'],
            prior_macro_normalized_comparison=row['english'] if row['decision']=='retention' else None,
            current_English_comparison_pending=False,fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=True)
    glyphs=[r['id'] for r in rows if r.get('wording_retention_with_scoped_glyph_fix')]
    assert glyphs==['DK4_MES_B37_R0099','DK4_MES_B39_R0024']
    doc=dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        file_path='/data/SC0.DK4',blocks=list(range(36,42)),current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],review_gates=['source','context','localization','naturalness','formatting'],
        records=rows,proposed_revisions=76,wording_retentions=99,complete_four_gate_comparisons=175,all_formatting_gates_false=True,
        proposed_display_only_glyph_corrections=glyphs,two_catalogue_name_field_artifacts_separately_pending=True,
        registered_release_andcompletion_credit_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*parts,CURRENT,ROOT/'B36_B41_source_identity_andFU_checkpoint_v1.json',Path(__file__)]})
    save(FINAL,doc)
    OUT.mkdir()
    save(OUT/'formatting_input.json',dict(**doc,physical_speech_objects=175,ordinary_speech_objects=175,typed_choice_objects=0,
        personality_alternatives=0,no_legacy_wraps_orpadding_copied=True,source_full_manuscript=str(FINAL),source_full_manuscript_sha256=sha(FINAL.read_bytes())))
    save(OUT/'initial_preferences_v1.json',dict(records={},no_visual_findings_before_native_pages=True))
    print('175 individual prose reviews:76 revisions/99 retentions;two scoped I glyph fixes;fresh formatting pending.')
