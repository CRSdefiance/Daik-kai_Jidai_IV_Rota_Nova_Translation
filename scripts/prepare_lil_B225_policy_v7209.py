"""Freeze a new immutable policy for the fuller R16 opening;preserve policyv1."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_fuller_policy_tools_v7209')
if __name__=='__main__':
    assert not ROOT.exists()
    freeze={'policy_v7195':'policy_v7209','editorial_manuscript_v2.json':'editorial_manuscript_v2b.json','native_review_v7194':'native_review_v7208',"CONTRACT=Path('translations/lil_B225_native_contract_v1.json')":"CONTRACT=Path('translations/lil_B225_native_contract_v2.json')","PROFILE=Path('dk4tool/dialogue/lil_B225_profile_v1.py')":"PROFILE=Path('dk4tool/dialogue/lil_B225_profile_v2.py')","FORMATTER=Path('dk4tool/dialogue/lil_B225_layout_v1.py')":"FORMATTER=Path('dk4tool/dialogue/lil_B225_layout_v2.py')",'layout_v7191b':'layout_v7191c',"changes={'B224':'B225',oldhash:":"changes={'B224':'B225','lil_B224_native_contract_v1.json':'lil_B225_native_contract_v2.json','lil-B224-source-bound-v1':'lil-B225-source-bound-v2',oldhash:","{'B224':'B225','plan_lil_B224_layout_v7142b'":"{'B224':'B225','lil_B224_profile_v1':'lil_B225_profile_v2','lil-B224-source-bound-v1':'lil-B225-source-bound-v2','plan_lil_B224_layout_v7142b'"}
    positive={'policy_validation_v7196':'policy_validation_v7210','editorial_manuscript_v2.json':'editorial_manuscript_v2b.json','lil_B225_profile_v1':'lil_B225_profile_v2','lil_B225_layout_v1':'lil_B225_layout_v2','lil_B225_native_contract_v1':'lil_B225_native_contract_v2'}
    jobs=[('scripts/freeze_lil_B225_policy_v7195.py','scripts/freeze_lil_B225_policy_v7209.py',freeze),('scripts/validate_lil_B225_policy_v7196.py','scripts/validate_lil_B225_policy_v7210.py',positive)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_fuller_policy_and_validation.json',dict(tools=rows,all_previous_policy_versions_preserved=True,new_v2_profile_namespace_andcontract_bound_to_revised_R16_only=True,all13_prose_paragraphs_and14_page_counts_unchanged=True,all_native_geometry_andhigh_integer_constants_preserved=True,new_credit=0,full_goal_complete=False))
