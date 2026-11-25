"""Use the demonstrated FE word budget for the overflowing swan-call panel."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_formatting_v1 import FORMATTING,OUT
from dk4tool.patch.grand_race_menu_release import sha

PREFERENCES=OUT/'swan_FE_preferences_v2.json'

def main():
    assert not PREFERENCES.exists()
    row=next(r for r in load(FORMATTING)['records'] if r['id']=='DK4_MES_B215_R0017')
    assert row['kind']=='system-FE' and row['english']=='Honk! Cluck... Cluck... honk... Honk!'
    save(PREFERENCES,dict(records={row['id']:dict(FE_planning_cells=36,
        bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
        reason='Native FE rendering moved the final exclamation to row 2 despite the host 38-cell plan. Use the already supported 36-cell FE word budget for this exact panel, preserving complete calls and punctuation; physical 228px geometry and all prose remain unchanged.')},
        author_inserted_ordinary_breaks=0,no_prose_or_native_geometry_change=True,
        manuscript=str(FORMATTING),manuscript_sha256=digest(FORMATTING),new_credit=0))

if __name__=='__main__':main()
