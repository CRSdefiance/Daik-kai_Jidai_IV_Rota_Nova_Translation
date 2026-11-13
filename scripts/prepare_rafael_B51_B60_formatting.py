"""Prepare every reviewed speech andboth complete menus without copying legacy wraps."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.gloss_rafael_B51_B59_clean import ROOT

OUT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')
FINAL=Path('translations/rafael_B51_B60_contextual_editorial_manuscript_v1.json')
CURRENT=Path('work/analysis/Rafael_B51_B60_current_20261104/current_effective.json')

if __name__=='__main__':
    assert not OUT.exists() and not FINAL.exists()
    source=ROOT/'B51_B60_249_contextual_prose_review_v1.json';doc,current=map(load,[source,CURRENT])
    prior={r['id']:r for g in current['groups'] for r in g['records']};rows=deepcopy(doc['records'])
    speeches=[];captions=[]
    for row in rows:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert not any(t in row['english'] for t in ['\n','{LB','{ALIGN','{PAD}','Ｉ']) and row['english'].isascii()
        if row.get('kind')=='typed-choice-label':
            captions.append(row);continue
        assert all(row[k]==prior[row['id']][k] for k in ['source_reference','current_reference','source_hex','current_hex'])
        assert all(row['english'].count('{MACRO:'+m+'}')==bytes.fromhex(row['source_hex'])[1:].count(m.encode()) for m in ['FI','FA','FO'])
        row.update(kind='system-FE' if row['source_selector']==254 else 'progressive',
            source_record_index=row['source_reference']['record_index'],source_native_extent=row['native_extent'],
            planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'],
            prior_macro_normalized_comparison=row['english'] if row['decision']=='retention' else None,
            current_English_comparison_pending=False,fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=True)
        speeches.append(row)
    assert len(speeches)==245 and len(captions)==4 and sum(r['kind']=='system-FE' for r in speeches)==3
    result=dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',file_path='/data/SC0.DK4',blocks=list(range(51,61)),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        proposed_revisions=102,wording_retentions=147,complete_four_gate_comparisons=249,
        all_formatting_gates_false=True,physical_speech_objects=245,ordinary_speech_objects=242,
        FE_speech_objects=3,typed_choice_objects=4,typed_choice_commands=2,personality_alternatives=0,
        no_legacy_wraps_orpadding_copied=True,registered_release_andcompletion_credit_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [source,CURRENT,ROOT/'B51_B60_source_identity_checkpoint_v1.json',Path(__file__)]})
    save(FINAL,result);OUT.mkdir();save(OUT/'formatting_input.json',dict(**result,source_full_manuscript=str(FINAL),source_full_manuscript_sha256=sha(FINAL.read_bytes())))
    save(OUT/'initial_preferences_v1.json',dict(records={},no_visual_findings_before_native_pages=True))
    print('Prepared249 records:242 progressive/3 FE speeches and4 captions in2 complete menus;all fresh formatting pending.')
