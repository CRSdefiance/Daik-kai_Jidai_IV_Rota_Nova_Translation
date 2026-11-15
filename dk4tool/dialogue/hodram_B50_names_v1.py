"""Exact scoped Lil identity;all207 actors/custom-name consumers remain outside this binding."""
from dk4tool.dialogue.hodram_B50_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B50 names:exact source-qualified review andnative/actual scope required')
    if [(r['actor_ID'],r['current']) for r in review['records']]!=[(2,'Lil Argot')]:
        raise ValueError('B50 names:exact scoped approved Lil identity required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B50 names:allfive individual scoped gates required')
    if not review['no_FE_personal_actor_name']:
        raise ValueError('B50 names:original FE hasno personal actor254 name orvoice')
    return expected
