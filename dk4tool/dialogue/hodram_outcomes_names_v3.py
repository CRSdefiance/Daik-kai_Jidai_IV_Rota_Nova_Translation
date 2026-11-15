"""Exact scoped Lil identity/name review; broader catalogue and custom names remain outside scope."""
from dk4tool.dialogue.hodram_outcomes_profile_v3 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:
        raise ValueError('Hodram outcome names: exact source-qualified Lil Argot review and native/actual scope required')
    for row in review['records']:
        if row['actor_ID']!=2 or row['current_name']!='Lil Argot' or not all(row['review'].get(k) is True for k in ['source','context','localization','naturalness','formatting']):
            raise ValueError('Hodram outcome names: approved identity and all five scoped gates required')
    if review['system_FE_record_IDs']!=['DK4_MES_B48_R0006'] or not review['FE_is_not_actor254_orpersonal_name']:
        raise ValueError('Hodram outcome names: original FE system notice has no personal speaker')
    return expected
