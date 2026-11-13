"""Remove the directly viewed isolated ships row while retaining full pursuit prose."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=ROOT/'visual_preferences_v6.json';output=ROOT/'visual_preferences_v7.json';assert not output.exists()
    doc=deepcopy(load(prior));row=doc['records']['DK4_MES_B70_R0193']
    row.update(page_clause="that we often can't catch them.",
        line_phrases=['maneuverable ships.','When we go after them,','get away'],
        reason='Direct native review found an isolated ships row in the earlier clause plan. Keep maneuverable ships and the complete pursuit condition together, then begin the next page with the whole result clause after so quickly. Preserve all wording and native geometry.',
        directly_viewed_sheet=str(ROOT/'contact_delta_v4/sheets/sheet_1.png'),
        directly_viewed_sheet_sha256=sha((ROOT/'contact_delta_v4/sheets/sheet_1.png').read_bytes()))
    doc.update(previous_preferences=str(prior),previous_preferences_sha256=sha(prior.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc)
