"""Preserve every viewed original andrefine four phrase flows with automatic wrapping."""
from copy import deepcopy
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.lil_B157_prose_v3755 import REVISIONS
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B157_viewed_flow_v3755')
INPUT=Path('translations/lil_B157_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B157_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));row=next(r for r in doc['records'] if r['source_record_index']==148);before=row['english'];body,note=REVISIONS[148];row.update(english='{SPEAKER:13}'+body,localization_note=note);module=Path('scripts/lil_B157_prose_v3755.py')
    for r in doc['records']:r.update(prose_author_module=str(module),prose_author_module_sha256=sha(module.read_bytes()));r.pop('compiled_hex',None)
    doc.update(prose_author_module=str(module),prose_author_module_sha256=sha(module.read_bytes()),previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()))
    for k in ['layout_QA_proof','layout_QA_proof_sha256','native_formatter_module','native_formatter_module_sha256']:doc.pop(k,None)
    pairs=[derive('dk4tool/dialogue/lil_B157_layout_v1.py','dk4tool/dialogue/lil_B157_layout_v2.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('please','come'),('please','take'),('go','ahead'),('pleased','to')})\n\ndef _word(value):"})]
    pairs.append(derive('scripts/plan_lil_B157_layout_v3753.py','scripts/plan_lil_B157_layout_v3756.py',{'lil_B157_layout_v1':'lil_B157_layout_v2','lil_B157_layout_v3753':'lil_B157_layout_v3756','lil_B157_editorial_manuscript_v1':'lil_B157_editorial_manuscript_v3','lil_B157_editorial_manuscript_v2':'lil_B157_editorial_manuscript_v4'}))
    ROOT.mkdir(parents=True);save(OUTPUT,doc);save(ROOT/'ten_viewed_sheets_and_four_phrase_refinements.json',dict(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),successor=str(OUTPUT),successor_sha256=sha(OUTPUT.read_bytes()),all10_original_native_sheets_viewed=True,findings=[dict(id='DK4_MES_B157_R0058',resolution='Keep Please come together.'),dict(id='DK4_MES_B157_R0142',resolution='Keep Please take together.'),dict(id='DK4_MES_B157_R0148',previous=before,successor=row['english'],resolution='Keep go ahead together and use source-equivalent direct shop first.'),dict(id='DK4_MES_B157_R0299',resolution='Keep the closing greeting Pleased to together.')],tools=pairs,source_meaning_all_retained_wordings_and_all_native_metrics_guards_unchanged=True,no_manual_layout_or_warning_waiver=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
