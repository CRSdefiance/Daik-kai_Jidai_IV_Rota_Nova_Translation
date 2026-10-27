"""Retain the source's directly-aft wind in idiomatic Shipwright vocabulary."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_astern_v4134d')
INPUT=Path('translations/lil_B167_editorial_manuscript_v8.json')
OUTPUT=Path('translations/lil_B167_editorial_manuscript_v10.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc=deepcopy(read(INPUT));r=next(r for r in doc['records'] if r['source_record_index']==112)
    r['prior_reviewed_English_before_astern_refinement']=r['english']
    assert 'wind right behind you' in r['english']
    r['english']=r['english'].replace('wind right behind you','wind directly astern')
    r['localization_note']+=' Directly astern preserves 真後ろから exactly in established nautical vocabulary suitable for the Shipwright. The agreement, only the rear mast receiving wind, and forward masts being ineffective remain complete. Review it with Manuel\'s mast-order answer and the following rear-quarter explanation. No relationship, condition, speed or angle is invented.'
    r.pop('compiled_hex',None)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),formatting_review_pending=True)
    save(OUTPUT,doc)
    tools=[derive('scripts/plan_lil_B167_layout_v4134c.py','scripts/plan_lil_B167_layout_v4134d.py',{
        'lil_B167_layout_v4134c':'lil_B167_layout_v4134d',
        'lil_B167_editorial_manuscript_v8':'lil_B167_editorial_manuscript_v10',
        'lil_B167_editorial_manuscript_v9':'lil_B167_editorial_manuscript_v11'})]
    tools.append(derive('scripts/verify_lil_B167_fonts_v4134c.py','scripts/verify_lil_B167_fonts_v4134d.py',{
        'lil_B167_fonts_v4134c':'lil_B167_fonts_v4134d',
        'lil_B167_editorial_manuscript_v9':'lil_B167_editorial_manuscript_v11'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_source_wind_and_mast_claims_preserved.json',dict(input=str(INPUT),input_sha256=sha(INPUT.read_bytes()),
        output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),changed_ID=r['id'],tools=tools,
        complete_source_direction_rear_only_and_forward_masts_retained=True,
        no_manual_layout_metric_guard_waiver_ROM_registry_orcredit_change=True,
        previous_failed_plans_and_all_drafts_preserved=True))
    print('R112 directly astern retains the complete source explanation; previous drafts preserved.')
