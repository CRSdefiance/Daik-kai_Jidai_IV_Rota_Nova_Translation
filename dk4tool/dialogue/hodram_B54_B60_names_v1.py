"""Exact ten scoped progressive identities;fullcatalogue/all207/custom names remain open."""
from dk4tool.dialogue.hodram_B54_B60_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B54-B60 names:exact source-qualified review andnative/actual scope required')
    if [r['actor_ID'] for r in review['records']]!=[1,20,23,24,36,84,113,114,119,141]:
        raise ValueError('B54-B60 names:exact ten approved scoped identities required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B54-B60 names:allfive individual scoped gates required')
    if not review['wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open'] or not review['full_name_shared_de_ownership_deployment_andconsumers_still_open']:
        raise ValueError('B54-B60 names:exact scoped preservation andopen full-name limits required')
    if review['actual_progressive_actor_IDs']!=[1,23,24,36,84,114,119,141] or review['offline_progressive_actor_IDs']!=[20,113] or review['new_credit']!=0:
        raise ValueError('B54-B60 names:exact actual/offline scope andzero duplicate credit required')
    return expected
