"""Add explicit formatting inventory to the sealed241 prose manuscript without changing words."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    source=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v2.json')
    output=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v3.json')
    preferences=Path('translations/rafael_B101_B120_visual_preferences_v1.json')
    assert not output.exists() and not preferences.exists()
    old=load(source);doc=deepcopy(old)
    assert len(doc['records'])==241 and doc['all241_individual_four_prose_gates_pass']
    for row in doc['records']:
        row['source_name_term_control_binding_pending']=False
        row['source_name_term_control_andformatting_binding_pending']=True
        row['fresh_formatting_binding_pending']=True
        row['prior_macro_normalized_comparison']=row['current_normalized_logical_English']
    doc.update(physical_speech_objects=229,typed_choice_objects=12,typed_choice_commands=4,
        previous_manuscript=str(source),previous_manuscript_sha256=sha(source.read_bytes()),
        no_source_current_prose_context_decision_orwording_changes=True,
        source_name_terms_resolved_but_combined_name_term_formatting_pending_until_fifth_gate=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in old['records']]
    save(output,doc)
    save(preferences,dict(records={},all_paragraphs_use_qualified_default_formatter_first=True,
        physical_FE_228px_progressive_216px_unchanged=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared241 exact-wording formatting inputs; all fifth gates pending.')
