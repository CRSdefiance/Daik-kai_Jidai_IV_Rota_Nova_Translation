"""Exact scoped Hodram/Lil identities;all207 actors/custom-name consumers remain outside this binding."""
from dk4tool.dialogue.hodram_B49_profile_v2 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B49 names:exact source-qualified review andnative/actual scope required')
    if [(r['actor_ID'],r['current_name']) for r in review['records']]!=[(1,'Hodram'),(2,'Lil Argot')]:
        raise ValueError('B49 names:exact two approved identities required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B49 names:allfive individual scoped gates required')
    if review['system_FE_record_IDs']!=['DK4_MES_B49_R0081'] or not review['FE_has_no_personal_actor254_name_orvoice']:
        raise ValueError('B49 names:original FE hasno personal actor254 name orvoice')
    return expected
