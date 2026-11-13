"""Keep Carlo’s exchanges on a single page and the sailor’s order intact."""
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import ROOT


MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v3.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v4.json'
ALARM = 'DK4_MES_B173_R0029'
ALARMTEXT = "It is! To the departure office!"
REASON = "The sailor confirms the report and urgently calls Rafael to the departure office."


def main():
    assert not MANUSCRIPT.exists() and not PREFERENCES.exists()
    doc = load(ROOT/'ordinary_formatting_manuscript_v2.json')
    prefs = load(ROOT/'ordinary_visual_preferences_v3.json')
    for ident, phrases in {
        'DK4_MES_B170_R0135': ['these travelers.'],
        'DK4_MES_B170_R0244': ['My wife caught it, too...', 'I lost them both.'],
        'DK4_MES_B170_R0253': ["people's health than business."],
    }.items():
        prefs['records'][ident]['line_phrases'] = phrases
        prefs['records'][ident]['reason'] = 'Keep the complete thought together within a single native page.'
    row = next(r for r in doc['records'] if r['id'] == ALARM)
    assert row['decision'] == 'revision' and row['english'] == "It's true! Come to the departure office, quick!"
    row.update(visual_revision_previous_English=row['english'], english=ALARMTEXT,
               editorial_logical_English=ALARMTEXT, planned_English_markup='{SPEAKER:97}'+ALARMTEXT,
               finding=REASON, localization_note=REASON)
    prefs['records'][ALARM] = dict(line_phrases=['the departure office!'], reason=REASON,
        bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
    doc['source_bound_read_aloud_refinements'].append(ALARM)
    save(MANUSCRIPT, doc)
    save(PREFERENCES, prefs)


if __name__ == '__main__':
    main()
