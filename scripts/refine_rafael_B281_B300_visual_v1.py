"""Bind the visual review's line and page findings to the reviewed dialogue."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B281_B300_v1 import FORMATTING, ROOT


PRIOR = ROOT / 'ordinary_visual_preferences_v2.json'
ATTEMPTS = [ROOT / f'visual_plan_v{version}/automatic_plans.json' for version in (1, 2, 3)]
PREFERENCES = ROOT / 'ordinary_visual_preferences_v6.json'
FIRST_NATIVE = ROOT / 'native_pages_v2/compiled_native_pages.json'
FIRST_SHEETS = ROOT / 'body_review_sheets_v1/sheet_index.json'

CHANT = dict(
    page_clause='it too lies between light and darkness.',
    reason='Keep the conclusion together across all three recitations.',
)
EQUINOX = dict(
    page_clause="to calculate where it'll fall on the spring or fall equinox!",
    line_phrases=['spring or fall equinox!'],
    reason='Keep the timing with the calculation, which carries into the second page.',
)
ORDINARY = {
    'B281_R0072': dict(line_phrases=['been to the Forbidden City?'],
                      reason='Carry the opening question into its destination without stranding the verb.'),
    'B283_R0005': dict(line_phrases=['I need you to track down.'],
                      reason='Keep the job directive intact.'),
    'B284_R0018': dict(line_phrases=['quiet down', 'but here. Take it.'],
                      reason='Keep the phrasal verb and the offer together.'),
    'B286_R0026': dict(page_clause="I'm counting on you.",
                      line_phrases=["when you meet him.", "I'm counting on you."],
                      reason='Keep the warning readable and the final appeal intact at the page turn.'),
    'B287_R0069': dict(one_page=True, line_phrases=['a map that shows the way.'],
                      reason='Keep the rumor on one page with its map lead.'),
    'B287_R0076': dict(line_phrases=['Why not look for it', "if you're curious?"],
                      reason='Keep the verb and the question ending together.'),
    'B290_R0011': dict(one_page=True, line_phrases=['we wanted to thank you.'],
                      reason='Keep the whole offer on one page.'),
    'B293_R0396': CHANT,
    'B293_R0400': CHANT,
    'B294_R0006': dict(line_phrases=["You're {MACRO:FA}, right?", 'The London guild', 'was looking for you.'],
                      reason='Keep the runtime name with the question tag.'),
    'B295_R0013': dict(page_clause='some kind of festival and calling it a ritual...',
                      line_phrases=['calling it a ritual...'],
                      reason='Keep the festival allegation and its description together at the page turn.'),
    'B296_R0013': CHANT,
    'B296_R0145': dict(line_phrases=['How does that tell us which day?'],
                      reason='Keep the objection in one line.'),
    'B296_R0186': dict(line_phrases=['The spring and fall equinoxes!'],
                      reason='Let the brief interjection lead into the complete realization.'),
    'B298_R0039': dict(line_phrases=['work out', 'the spring or fall equinox!'],
                      reason='Keep the calculation verb and the complete time reference together.'),
    'B298_R0046': EQUINOX,
    'B298_R0054': EQUINOX,
    'B299_R0077': dict(line_phrases=["going on here?", 'they were looking for?!'],
                      reason='Keep the two surprised question endings intact.'),
    'B299_R0084': dict(line_phrases=['end up as sacrifices ourselves.'],
                      reason='Keep the phrasal verb with the danger it describes.'),
}
STYLE = {
    '1954_0': dict(line_phrases=['We tried to scare it,', "but it won't run!"],
                   reason='Keep the attempted scare and its result together.'),
    '1954_252': dict(line_phrases=['scare it,'], reason='Keep the attempted scare together.'),
    '2428_168': dict(line_phrases=["Forget it, let's run!"],
                     reason='Keep the call to retreat intact.'),
    '2428_314': dict(line_phrases=["We'd better get out of here!"],
                     reason='Keep the call to retreat intact.'),
    '3074_176': dict(line_phrases=['It looks like everyone made it.'],
                     reason='Keep the breathless relief together.'),
    '3334_186': dict(line_phrases=['out of the woods!'],
                     reason='Keep the report of leaving the woods together.'),
}


def main():
    assert not PREFERENCES.exists()
    manuscript, preferences, sheets = map(load, (FORMATTING, PRIOR, FIRST_SHEETS))
    assert sheets['pages'] == 250 and sheets['native_receipt_sha256'] == digest(FIRST_NATIVE)
    assert len(sheets['sheets']) == 11
    assert all(digest(Path(sheet['path'])) == sheet['sha256'] for sheet in sheets['sheets'])
    rules = {f'DK4_MES_{record}': rule for record, rule in ORDINARY.items()}
    rules.update({f'SC0_B293_STYLE_{record}': rule for record, rule in STYLE.items()})
    rows = {row['id']: row for row in manuscript['records']}
    for record, rule in rules.items():
        row = rows[record]
        phrases = [*rule.get('line_phrases', ())]
        if 'page_clause' in rule:
            phrases.append(rule['page_clause'])
        assert all(phrase in row['english'] for phrase in phrases), record
        assert record not in preferences['records']
        preferences['records'][record] = {**rule, 'bindings': {
            key: sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')
        }}
    preferences.update(previous_preferences_sha256=digest(PRIOR),
                       earlier_plan_attempts={str(path): digest(path) for path in ATTEMPTS},
                       native_visual_sheet_index_sha256=digest(FIRST_SHEETS))
    save(PREFERENCES, preferences)


if __name__ == '__main__':
    main()
