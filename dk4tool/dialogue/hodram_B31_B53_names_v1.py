"""Exact two source-qualified identities;all207 actors/custom-name consumers remain outside this binding."""
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B31/B53 names:exact source-qualified review andnative/actual scope required')
    if [(r['actor_ID'],r['speaker']) for r in review['records']]!=[(34,'Barbarossa Hayreddin'),(113,'Port Worker')]:
        raise ValueError('B31/B53 names:exact two approved scoped identities required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B31/B53 names:allfive individual scoped gates required')
    if review['new_name_asset_changes']!=0 or not review['wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open'] or not review['full_name_resolution']['actual_B31_progressive_header_verified'] or not review['full_name_resolution']['full_catalogue_UI_still_unobserved']:
        raise ValueError('B31/B53 names:exact scoped name preservation andno duplicate all207 credit required')
    return expected
