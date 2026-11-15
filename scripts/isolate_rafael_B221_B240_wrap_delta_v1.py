"""Select only records whose encoded speech changed in the contact-sheet refinement."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B221_B240_v1 import FORMATTING, ROOT
from scripts.refine_rafael_B221_B240_wraps_v6 import BASE, PLAN
from scripts.write_rafael_B221_B240_contextual_v1 import digest

MANUSCRIPT = ROOT / 'ordinary_visual_delta_manuscript_v1.json'
DELTA = ROOT / 'ordinary_visual_delta_plan_v1.json'


def main():
    assert not MANUSCRIPT.exists() and not DELTA.exists()
    doc, before, after = map(load, (FORMATTING, BASE, PLAN))
    assert before['manuscript_sha256'] == after['manuscript_sha256'] == digest(FORMATTING)
    assert not after['failures']
    changes = []
    for old, new in zip(before['records'], after['records'], strict=True):
        assert old['id'] == new['id'] and old['logical_English'] == new['logical_English']
        assert old['expected_native_pages'] == new['expected_native_pages']
        assert all(issue['severity'] == 'info' for issue in new['base_QA']['issues'])
        if old['encoded_hex'] != new['encoded_hex']:
            changes.append(new)
    ids = {row['id'] for row in changes}
    assert len(ids) == len(changes) and any(ident.startswith('SC0_') for ident in ids)
    choices = [row for row in doc['records'] if row['id'] in ids]
    assert len(choices) == len(ids)
    save(MANUSCRIPT, {**doc, 'records': choices, 'blocks': sorted({row['block'] for row in choices}),
        'physical_speech_objects': len(ids), 'typed_choice_objects': 0, 'typed_choice_commands': 0})
    save(DELTA, {**after, 'records': changes, 'manuscript': str(MANUSCRIPT),
        'manuscript_sha256': digest(MANUSCRIPT), 'complete_plan': str(PLAN), 'complete_plan_sha256': digest(PLAN)})
    print([(row['id'], row['lines']) for row in changes], flush=True)


if __name__ == '__main__':
    main()

