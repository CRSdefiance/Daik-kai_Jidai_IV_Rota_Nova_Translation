"""Prefer three readable rows over four short rows using one reviewed ordinary soft wrap."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=ROOT/'visual_preferences_v7.json';output=ROOT/'visual_preferences_v8.json';assert not output.exists()
    doc=deepcopy(load(prior));manuscript=load(ROOT/'formatting_input_v3.json')
    row=next(r for r in manuscript['records'] if r['id']=='DK4_MES_B69_R0143')
    sheet=ROOT/'contact_fresh250_v3/sheets/sheet_3.png'
    reason='The directly viewed four-row layout needlessly broke the thanks-to-you phrase. A complete-word soft wrap after the article the is grammatical, like the existing reviewed For/a examples. Keep all good prose and use three native-width rows. This exact bound line alone is retained; all glyph, control, allocation and bounds checks remain mandatory.'
    doc['records'][row['id']]=dict(
        bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
        ordinary_boundaries=[['the','villagers']],
        QA_line_ending_retention=dict(line_index=1,exact_line="It's all thanks to you that the",reason=reason),
        reason=reason,directly_viewed_sheet=str(sheet),directly_viewed_sheet_sha256=sha(sheet.read_bytes()),
        no_authored_break_orprose_change=True)
    doc.update(previous_preferences=str(prior),previous_preferences_sha256=sha(prior.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc)
