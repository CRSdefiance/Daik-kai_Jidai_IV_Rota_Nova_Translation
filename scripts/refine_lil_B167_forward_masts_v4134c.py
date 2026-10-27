"""Keep the rear-mast contrast clear in natural clauses without changing source mechanics."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_forward_masts_v4134c')
INPUT=Path('translations/lil_B167_editorial_manuscript_v6.json')
OUTPUT=Path('translations/lil_B167_editorial_manuscript_v8.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc=deepcopy(read(INPUT))
    row=next(r for r in doc['records'] if r['source_record_index']==112)
    old="The masts ahead don't do you any good."
    assert row['english'].endswith(old)
    row['prior_reviewed_English_before_forward_mast_refinement']=row['english']
    row['english']=row['english'][:-len(old)]+"The forward masts are no use."
    row['localization_note']+=' Forward masts are no use expresses the complete source claim about the front masts naturally and precisely. Keep the agreement, directly following wind, only-rear-mast explanation and all controls. No condition or causal fact is removed.'
    row.pop('compiled_hex',None)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),formatting_review_pending=True)
    save(OUTPUT,doc)
    tools=[derive('dk4tool/dialogue/lil_B167_layout_v5.py','dk4tool/dialogue/lil_B167_layout_v6.py',{
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('only','the'),('the','rear')})\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B167_layout_v4134b.py','scripts/plan_lil_B167_layout_v4134c.py',{
        'lil_B167_layout_v5':'lil_B167_layout_v6','lil_B167_layout_v4134b':'lil_B167_layout_v4134c',
        'lil_B167_editorial_manuscript_v6':'lil_B167_editorial_manuscript_v8',
        'lil_B167_editorial_manuscript_v7':'lil_B167_editorial_manuscript_v9'}))
    tools.append(derive('scripts/verify_lil_B167_fonts_v4134b.py','scripts/verify_lil_B167_fonts_v4134c.py',{
        'lil_B167_layout_v5':'lil_B167_layout_v6','lil_B167_fonts_v4134b':'lil_B167_fonts_v4134c',
        'lil_B167_editorial_manuscript_v7':'lil_B167_editorial_manuscript_v9'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_facts_and_complete_rear_forward_contrast_preserved.json',dict(previous_manuscript=str(INPUT),
        previous_manuscript_sha256=sha(INPUT.read_bytes()),manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        changed_ID=row['id'],all_source_wind_direction_mast_order_only_rear_and_useless_forward_masts_retained=True,
        tools=tools,all_previous_words_failed_plans_and_native_planes_preserved=True,
        no_manual_break_padding_metrics_guard_waiver_ROM_registry_orcredit_change=True))
    print('R112 forward-mast contrast phrased naturally;all source mechanics and prior artifacts retained.')
