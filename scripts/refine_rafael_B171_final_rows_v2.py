"""Keep Claudio's complete thought on one page without dropping his seafaring joke."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


BASE = Path('scripts/refine_rafael_B171_final_rows_v1.py')
source = checked_text(BASE.read_text(encoding='utf-8'), {
    'import MANUSCRIPT, PLAN as PRIOR': 'import MANUSCRIPT as PRIOR_DOC, PLAN as PRIOR',
    "PREFERENCES = ROOT / 'ordinary_visual_preferences_v6.json'": 
        "MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v5.json'\nPREFERENCES = ROOT / 'ordinary_visual_preferences_v7.json'",
    "'plans_v6/automatic_plans.json'": "'plans_v7/automatic_plans.json'",
    "    prefs['records'][ID]['line_phrases'].append('Look at Cristina.')":
        "    doc = load(PRIOR_DOC)\n"
        "    r = next(r for r in doc['records'] if r['id']==ID)\n"
        "    old = r['english']\n"
        "    assert old.startswith('What are you talking about? A man of the sea')\n"
        "    new = 'Come on.' + old[len('What are you talking about?'):]\n"
        "    note = 'Give Claudio a conversational rebuttal and keep the seafaring boast that Rafael challenges.'\n"
        "    r.update(english=new, editorial_logical_English=new, planned_English_markup='{SPEAKER:05}'+new,\n"
        "             visual_revision_previous_English=old, finding=note, localization_note=note)\n"
        "    prefs['records'][ID]['line_phrases'].append('Look at Cristina.')\n"
        "    prefs['records'][ID]['bindings']['english']=sha(new.encode('utf-8'))\n"
        "    prefs['records'][ID]['one_page']=True\n"
        "    save(MANUSCRIPT,doc)",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::complete-thought-one-page', 'exec'), globals())
