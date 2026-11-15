"""Bind the actual three-row candidate instead of weakening its exact-line assertion."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=ROOT/'visual_preferences_v8.json';output=ROOT/'visual_preferences_v9.json';assert not output.exists()
    doc=deepcopy(load(prior))
    row=doc['records']['DK4_MES_B69_R0143']
    row['QA_line_ending_retention']['exact_line']='all thanks to you that the'
    doc.update(previous_preferences=str(prior),previous_preferences_sha256=sha(prior.read_bytes()),
        exact_candidate_from_retained_diagnostic=str(ROOT/'automatic_v9_diagnostic1/automatic_plans.json'),
        no_English_geometry_native_control_orQA_predicate_change=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc)
