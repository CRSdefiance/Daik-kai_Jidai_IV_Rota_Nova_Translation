"""Prepare 352 source-bound speech objects and separate the ten typed menus."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')
SOURCE = Path('translations/hodram_B191_B210_contextual_editorial_manuscript_v1.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = load(SOURCE)
    assert len(doc['records']) == doc['complete_four_gate_comparisons'] == 373
    rows = []
    for original in doc['records']:
        row = deepcopy(original)
        if row.get('kind') != 'typed-choice-label':
            assert row['source_selector'] != 0 and row.get('native_object_kind') != '4100-style-alternative'
            row.update(kind='system-FE' if row['source_selector'] == 254 else 'progressive',
                source_record_index=row['source_reference']['record_index'],
                planned_English_markup='{SPEAKER:' + f'{row["source_selector"]:02X}' + '}' + row['english'],
                source_meaning_gloss=row['source_meaning'], complete_clean_exchange_context=row['context'],
                prior_macro_normalized_comparison=row['english'] if row['decision'] == 'retention' else None)
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        rows.append(row)
    assert Counter(r['kind'] for r in rows) == {'progressive': 316, 'system-FE': 36, 'typed-choice-label': 21}
    ROOT.mkdir(parents=True)
    save(ROOT / 'formatting_input.json', dict(**{**doc, 'records': rows}, physical_speech_objects=352,
        ordinary_speech_objects=352, typed_choice_objects=21, typed_choice_commands=10,
        personality_alternatives=0, personality_alias_slots=0, source_full_manuscript=str(SOURCE),
        source_full_manuscript_sha256=sha(SOURCE.read_bytes()), no_legacy_breaks_orpadding_copied=True,
        producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT / 'initial_preferences.json', dict(records={}, no_visual_findings_before_native_pages=True))
    print('352 speeches (316 progressive/36 FE) prepared for fresh plans; 21 captions remain separate.')
