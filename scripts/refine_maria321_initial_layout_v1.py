"""Bind complete-thought page and phrase preferences to the reviewed manuscript."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B196_B215_clean_20261110')
PHRASES = {
    'SC3_B196_STYLE_8_192': ('come in', 'Keep the letter-arrival phrasal verb together.'),
    'SC3_B208_STYLE_8_202': ('come in', 'Keep the letter-arrival phrasal verb together.'),
    'SC3_B209_STYLE_8_192': ('come in', 'Keep the letter-arrival phrasal verb together.'),
    'DK4_MES_B197_R0017': ('feels like', 'Keep the closing comparison together.'),
    'DK4_MES_B197_R0025': ('Medusa Shield', 'Keep the installed item name together.'),
    'DK4_MES_B198_R0019': ('hero here', 'Avoid a sparse opening row in the short hero question.'),
    'DK4_MES_B198_R0043': ('Charles Martel', 'Keep the complete historical name together.'),
    'DK4_MES_B200_R0008': ('overdo it', 'Keep the ordinary warning phrase together.'),
    'DK4_MES_B200_R0015': ('move in', 'Keep the approach-to-the-blade phrasal verb together.'),
    'DK4_MES_B202_R0019': ('Giant Tortoise Shield', 'Keep the installed item name together.'),
    'DK4_MES_B203_R0059': ('Phoenix Bascinet', 'Keep the installed item name together.'),
    'DK4_MES_B204_R0019': ('ship crew', 'Keep ship crew together in the fatigue explanation.'),
    'DK4_MES_B208_R0043': ('pass by', 'Keep the chance passing of the navy together.'),
    'DK4_MES_B209_R0029': ('sum it up', 'Keep the idiomatic summary phrase together.'),
    'DK4_MES_B209_R0048': ('See you around', 'Keep the complete farewell together.'),
    'DK4_MES_B209_R0063': ('five hundred years', 'Keep the boast quantity and time unit together.'),
    'DK4_MES_B211_R0061': ('Jutland Peninsula', 'Keep the complete geographical name together.'),
    'DK4_MES_B212_R0094': ('like a real rose', 'Keep the comparison together without suggesting a real rose is inside the glass.'),
    'DK4_MES_B213_R0064': ('find it', 'Keep the recovery request together.'),
    'DK4_MES_B215_R0158': ('worked out', 'Keep the closing phrasal verb together.'),
}
CLAUSES = {
    'DK4_MES_B196_R0030': 'some two hundred years ago.',
    'DK4_MES_B196_R0039': 'when exhaustion finally claimed their lives.',
    'DK4_MES_B196_R0066': 'I imagine that naturally drew his interest.',
    'DK4_MES_B200_R0015': "That's why you need the strength of mind to face things without fear.",
    'DK4_MES_B206_R0039': 'If you get the chance, do look for it.',
    'DK4_MES_B208_R0043': 'and the merchant fleet narrowly escaped disaster.',
    'DK4_MES_B209_R0045': 'Something like that could come in handy, right?',
    'DK4_MES_B212_R0109': "prices, claiming they're jade or crystal.",
    'DK4_MES_B213_R0107': "Next time I see him, I'll turn him over to the governor's office!",
}


def main():
    out = ROOT/'formatting_v1/page_phrase_preferences_v2.json'
    assert not out.exists()
    docpath = ROOT/'formatting_v1/formatting_input.json'
    rows = {r['id']: r for r in load(docpath)['records']}
    planpath = ROOT/'plan_v1/automatic_plans.json'
    plans = {r['id']: r for r in load(planpath)['records']}
    prefs = load(ROOT/'formatting_v1/initial_preferences.json')
    assert not prefs['records']

    def entry(key):
        row = rows[key]
        return prefs['records'].setdefault(key, dict(bindings={k: sha(row[k].encode()) for k in ['source_hex', 'current_hex', 'english']}))

    for key, (phrase, reason) in PHRASES.items():
        assert rows[key]['english'].count(phrase) == 1
        words = phrase.lower().split()
        e = entry(key)
        e['required_pairs'] = [list(p) for p in zip(words, words[1:])]
        e['reason'] = reason
    for key, clause in CLAUSES.items():
        assert rows[key]['english'].count(clause) == 1
        e = entry(key)
        e['page_clause'] = clause
        e['reason'] = e.get('reason', '') + ' Keep this complete closing thought on one page; avoid a page turn inside its final phrase.'
    key = 'DK4_MES_B197_R0017'
    assert plans[key]['lines'][1] == 'your eyes were drawing me in.'
    entry(key)['QA_line_ending_retention'] = dict(line_index=1, exact_line=plans[key]['lines'][1],
        reason='Drawing me in is a complete phrasal verb and sentence, not an orphaned preposition. Retain this natural sentence boundary; no native display guard is waived.')
    prefs.update(source_owned_preferences=True, no_prose_or_width_change=True,
        no_new_visual_or_native_approval=True, planned_text_review_only=True,
        evidence={str(p): digest(p) for p in [docpath, planpath, Path(__file__)]})
    save(out, prefs)
    print(f'Prepared {len(PHRASES)} phrase preferences, {len(CLAUSES)} page clauses and one exact grammatical retention; native and visual approval pending.')


if __name__ == '__main__':
    main()
