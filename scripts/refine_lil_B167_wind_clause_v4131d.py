"""Use natural headwind/tailwind wording while preserving all orientation/angle facts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_wind_clause_v4131d')
INPUT=Path('translations/lil_B167_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B167_editorial_manuscript_v4.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc=deepcopy(read(INPUT))
    row=next(r for r in doc['records'] if r['source_record_index']==75)
    assert row['english'].count('with a following wind')==1
    row['prior_reviewed_English_before_wind_synonym']=row['english']
    row['english']=row['english'].replace('with a following wind','with a tailwind')
    row['localization_note']+=' Tailwind and headwind give this informal explanation a natural paired contrast. Both original wind conditions and the complete angle limitation remain explicit; no performance fact, qualifier or source control is removed.'
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()))
    save(OUTPUT,doc)
    tools=[derive('scripts/plan_lil_B167_layout_v4131c.py','scripts/plan_lil_B167_layout_v4131d.py',{
        'lil_B167_layout_v4131c':'lil_B167_layout_v4131d','lil_B167_editorial_manuscript_v2':'lil_B167_editorial_manuscript_v4',
        'lil_B167_editorial_manuscript_v3':'lil_B167_editorial_manuscript_v5'})]
    tools.append(derive('scripts/verify_lil_B167_fonts_v4132c.py','scripts/verify_lil_B167_fonts_v4132d.py',{
        'lil_B167_fonts_v4132c':'lil_B167_fonts_v4132d','lil_B167_editorial_manuscript_v3':'lil_B167_editorial_manuscript_v5'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_meaning_and_native_metric_preservation.json',dict(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),changed_ID=row['id'],all_source_orientation_wind_and_angle_facts_preserved=True,
        previous_failed_plans_preserved=['work/analysis/lil_B167_layout_v4131/all27_paragraph_layout_QA.json',
            'work/analysis/lil_B167_layout_v4131b/all27_paragraph_layout_QA.json','work/analysis/lil_B167_layout_v4131c/all27_paragraph_layout_QA.json'],
        no_manual_break_padding_native_metric_guard_or_waiver_change=True,tools=tools,no_ROM_registry_ledger_credit_change=True))
    print('B167 complete tailwind/headwind clause recorded;all source facts preserved;no metric or guard change.')
