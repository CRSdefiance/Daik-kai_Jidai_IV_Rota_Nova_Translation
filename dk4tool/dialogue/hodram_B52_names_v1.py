"""Exact actor113 role andmentioned actor34 component;all207 actors/custom-name consumers remain outside this binding."""
from dk4tool.dialogue.hodram_B52_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B52 names:exact source-qualified review andnative/actual scope required')
    if [(r['actor_ID'],r['speaker']) for r in review['records']]!=[(113,'Port Worker')]:
        raise ValueError('B52 names:exact scoped Port Worker identity required')
    for row in review['records']+review['mentioned_components']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B52 names:allfive individual scoped gates required')
    if not review['no_new_name_asset_orall207_name_review_credit'] or review['scoped_actor_IDs']!=[113] or review['mentioned_actor_IDs']!=[34] or [(r['actor_ID'],r['english']) for r in review['mentioned_components']]!=[(34,'Hayreddin')] or not review['no_actor34_actual_header_catalogue_orfull_name_review_claim']:
        raise ValueError('B52 names:exact scoped name preservation andno duplicate all207 credit required')
    return expected
