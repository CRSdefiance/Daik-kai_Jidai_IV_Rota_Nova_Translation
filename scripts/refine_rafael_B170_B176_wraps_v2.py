"""Resolve the exact formatter diagnostics without weakening validation."""
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import FORMATTING, ROOT


MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v2.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v3.json'
PROSE = {
    'DK4_MES_B170_R0005': ('My usual order of cinnamon, please.', ('usual order of cinnamon',),
        'Carlo requests his customary quantity with a single natural order.'),
    'DK4_MES_B171_R0103': ("You're all right. To me, you were the old man's granddaughter. From here on out, you're one of us.",
        ("the old man's granddaughter.", "From here on out,"), 'Keep the explicit granddaughter reference and Claudio’s change of attitude.'),
}


def main():
    assert not MANUSCRIPT.exists() and not PREFERENCES.exists()
    doc = load(FORMATTING)
    prefs = load(ROOT / 'ordinary_visual_preferences_v2.json')
    for row in doc['records']:
        if row['id'] not in PROSE:
            continue
        replacement, phrases, note = PROSE[row['id']]
        old = row['english']
        assert row['decision'] == 'revision' and not row['native_literal_tokens'] and old != replacement
        row.update(english=replacement, editorial_logical_English=replacement, finding=note, localization_note=note,
                   visual_revision_previous_English=old, planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+replacement)
        prefs['records'][row['id']] = dict(line_phrases=phrases, reason=note,
            bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
    prefs['records']['DK4_MES_B173_R0029']['line_phrases'] = ['Come to the departure office, quick!']
    prefs['records']['DK4_MES_B176_R0068']['line_phrases'] = ['a way! Yahoo!', "all right, it's all right!"]
    save(MANUSCRIPT, {**doc, 'no_prose_changes_or_manual_breaks': False,
                      'source_bound_read_aloud_refinements': sorted(PROSE), 'no_manual_breaks': True})
    save(PREFERENCES, prefs)


if __name__ == '__main__':
    main()
