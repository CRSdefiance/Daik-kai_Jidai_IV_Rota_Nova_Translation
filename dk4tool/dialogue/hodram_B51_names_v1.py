"""Exact four source-qualified identities;all207 actors/custom-name consumers remain outside this binding."""
from dk4tool.dialogue.hodram_B51_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B51 names:exact source-qualified review andnative/actual scope required')
    if [(r['actor_ID'],r['speaker']) for r in review['records']]!=[(1,'Hodram Bergstrom'),(16,'Gerhard Adernkatz'),(18,'Charles Rochefort'),(113,'Port Worker')]:
        raise ValueError('B51 names:exact four approved scoped identities required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B51 names:allfive individual scoped gates required')
    if not review['no_new_name_asset_orall207_name_review_credit'] or review['scoped_actor_IDs']!=[1,16,18,113]:
        raise ValueError('B51 names:exact scoped name preservation andno duplicate all207 credit required')
    return expected
