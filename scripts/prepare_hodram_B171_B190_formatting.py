"""Prepare all ordinary speech objects without importing legacy line breaks."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_formatting_20261102')
SOURCE = Path('translations/hodram_B171_B190_contextual_editorial_manuscript_v1.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = load(SOURCE)
    assert len(doc['records']) == doc['complete_four_gate_comparisons'] == 435
    rows = []
    for original in doc['records']:
        row = deepcopy(original)
        if row.get('kind') != 'typed-choice-label':
            assert row['source_selector'] != 0 and row.get('native_object_kind') != '4100-style-alternative'
            row['kind'] = 'system-FE' if row['source_selector'] == 254 else 'progressive'
            row['source_record_index'] = row['source_reference']['record_index']
            row['planned_English_markup'] = '{SPEAKER:' + f'{row["source_selector"]:02X}' + '}' + row['english']
            row['source_meaning_gloss'] = row['source_meaning']
            row['complete_clean_exchange_context'] = row['context']
            row['prior_macro_normalized_comparison'] = row['english'] if row['decision'] == 'retention' else None
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        rows.append(row)
    counts = Counter(r['kind'] for r in rows)
    assert counts == {'progressive': 405, 'system-FE': 28, 'typed-choice-label': 2}, counts
    result = {**doc, 'records': rows, 'physical_speech_objects': 433, 'ordinary_speech_objects': 433,
        'typed_choice_objects': 2, 'typed_choice_commands': 1, 'personality_alternatives': 0, 'personality_alias_slots': 0,
        'source_full_manuscript': str(SOURCE), 'source_full_manuscript_sha256': sha(SOURCE.read_bytes()),
        'no_legacy_breaks_orpadding_copied': True, 'new_credit': 0, 'producer_sha256': sha(Path(__file__).read_bytes())}
    ROOT.mkdir(parents=True)
    save(ROOT / 'formatting_input.json', result)
    print('433 speeches (405 progressive / 28 FE) ready for fresh formatting; two captions use their separate consumer.')
