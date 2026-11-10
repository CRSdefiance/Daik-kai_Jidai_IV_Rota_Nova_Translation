"""Preserve reviewed words while spelling native macro tokens explicitly for formatting."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

SOURCE = Path('translations/rafael_B121_B140_contextual_prose_review_v2.json')
OUT = Path('translations/rafael_B121_B140_formatting_manuscript_v3.json')
PREFERENCES = Path('translations/rafael_B121_B140_visual_preferences_v1.json')

if __name__ == '__main__':
    assert not OUT.exists() and not PREFERENCES.exists()
    old = load(SOURCE); doc = deepcopy(old)
    assert old['all351_individual_four_prose_gates_pass'] and len(old['records']) == 351
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English'] = row['english']
        row['fresh_formatting_binding_pending'] = True
        if row['kind'] == 'typed-choice-label': continue
        counts = row.get('source_macros',{})
        row['english'] = re.sub(r'\b(FI|FA|FO)\b', lambda m:'{MACRO:'+m[0]+'}', row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO)\}',lambda m:m[1],row['english']) == row['editorial_logical_English']
        for macro in ['FI','FA','FO']:
            assert row['english'].count('{MACRO:'+macro+'}') == counts.get(macro,0)
        row['source_record_index'] = row['source_reference'].get('record_index',row['source_reference'].get('physical_record_index'))
        assert isinstance(row['source_record_index'],int)
        row['planned_English_markup'] = '{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
        row['prior_macro_normalized_comparison'] = None
    doc.update(physical_speech_objects=341,ordinary_speech_objects=307,style_physical_speech_objects=34,
        style_command_objects=6,typed_choice_objects=10,typed_choice_commands=5,
        previous_manuscript=str(SOURCE),previous_manuscript_sha256=sha(SOURCE.read_bytes()),
        native_macro_tokens_only_explicitly_marked_no_prose_wording_or_decision_changes=True)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]})
    save(OUT,doc)
    save(PREFERENCES,dict(records={},all_paragraphs_use_qualified_default_formatter_first=True,
        physical_FE_228px_progressive_216px_unchanged=True,
        no_source_specific_guard_budget_orsemantic_preference_inherited_for_changed_text=True,
        author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared351 exact-wording objects:307 ordinary,34 physical styles,10 choices. Native macros explicitly marked; all fifth gates pending.')
