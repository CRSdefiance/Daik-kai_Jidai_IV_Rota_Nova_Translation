"""Keep Claudio's look-at phrase and the patron's exclamation intact."""
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import ROOT
from scripts.refine_rafael_B170_B176_visual_v1 import MANUSCRIPT, PLAN as PRIOR, PREFERENCES as PRIOR_PREFS
from scripts.source_locked_derivation_v5118 import checked_text


PREFERENCES = ROOT / 'ordinary_visual_preferences_v6.json'
PLAN = ROOT / 'plans_v6/automatic_plans.json'
DELTA_MANUSCRIPT = ROOT / 'final_rows_delta_manuscript_v1.json'
DELTA_PLAN = ROOT / 'final_rows_delta_plan_v1.json'
ID = 'DK4_MES_B171_R0010'
STAGED_SCRIPT = Path('scripts/check_rafael_B171_patron_panels_v1.py')


def prepare():
    assert not PREFERENCES.exists()
    prefs = load(PRIOR_PREFS)
    prefs['records'][ID]['line_phrases'].append('Look at Cristina.')
    save(PREFERENCES, prefs)


def isolate():
    assert not DELTA_MANUSCRIPT.exists() and not DELTA_PLAN.exists()
    doc, old, new = map(load, (MANUSCRIPT, PRIOR, PLAN))
    assert len(old['records']) == len(new['records']) == 187 and not new['failures']
    changes = [b for a,b in zip(old['records'],new['records'],strict=True) if a['encoded_hex'] != b['encoded_hex']]
    assert [r['id'] for r in changes] == [ID]
    assert any('Look at Cristina.' in s for s in changes[0]['lines']) and changes[0]['expected_native_pages'] == 1
    save(DELTA_MANUSCRIPT, {**doc, 'records': [r for r in doc['records'] if r['id']==ID],
                           'physical_speech_objects': 1, 'ordinary_speech_objects': 1})
    save(DELTA_PLAN, {**new, 'records': changes, 'manuscript': str(DELTA_MANUSCRIPT),
                     'manuscript_sha256': sha(DELTA_MANUSCRIPT.read_bytes()), 'complete_plan_sha256': sha(PLAN.read_bytes())})


def staged():
    source = checked_text(STAGED_SCRIPT.read_text(encoding='utf-8'), {
        "OUT = ROOT / 'staged_FE_native_v1'": "OUT = ROOT / 'staged_FE_native_v2'",
        "            shape = [(0, t) for t in (heading, *lines)]":
            "            if ident == 'DK4_MES_B171_R0047' and not any('can she dance!' in line for line in lines):\n"
            "                continue\n"
            "            shape = [(0, t) for t in (heading, *lines)]",
    })
    exec(compile(source, __file__+'::same-exact-staging-with-phrase-continuity', 'exec'), globals())
    before, after = [load(ROOT/f'staged_FE_native_v{v}/staged_display.json') for v in (1,2)]
    changes = [b['id'] for a,b in zip(before['records'],after['records'],strict=True) if a['encoded_hex'] != b['encoded_hex']]
    assert changes == ['DK4_MES_B171_R0047']


if __name__ == '__main__':
    {'--prepare':prepare,'--isolate':isolate,'--staged':staged}[sys.argv[1]]()
