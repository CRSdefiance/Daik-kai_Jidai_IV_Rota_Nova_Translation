"""Use the planner's normalized lowercase token key for the exact but/I boundary."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')

if __name__ == '__main__':
    before = ROOT / 'guard_and_opening_preferences_v2.json'
    output = ROOT / 'guard_and_opening_preferences_v3.json'
    assert not output.exists()
    doc = deepcopy(load(before))
    row = doc['records']['DK4_MES_B201_R0074']
    assert row['ordinary_boundaries'] == [['but', 'I']]
    row['ordinary_boundaries'] = [['but', 'i']]
    doc.update(previous_preferences=str(before), previous_preferences_sha256=sha(before.read_bytes()),
        preference_key_fix_not_prose_orengine_change=True)
    save(output, doc)
