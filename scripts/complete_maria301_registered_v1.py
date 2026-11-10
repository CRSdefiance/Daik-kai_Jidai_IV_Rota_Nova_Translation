"""Credit301 unique Maria reviews once after registered patch andcandidate-owned startup."""
import re
from scripts.complete_hodram_B251_B280_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/hodram_B251_B280_release_v1': 'work/maria301_release_v1',
    'hodram_B251_B280_integrated_final_review_v1.json': 'maria301_integrated_final_review_v1.json',
    'Hodram_SC1_B251_B280_contextual_integrated_20261107': 'Maria_SC3_B0_B32_contextual_integrated_20261109',
    'Hodram_B251_B280_clean_next_20261107': 'Maria_SC3_B0_B32_clean_20261109',
    '==(703,114,38)': '==(709,114,44)',
    "startup['actual_captain_getter']==startup['actual_route_word']==0":
        "startup['actual_captain_getter']==startup['actual_route_word']==3",
    'both_name_getters_exact_for_all9_protected_actors': 'both_name_getters_exact_for_all12_protected_actors',
    'ordinary_title_NewGame_Rafael_Castor_andopening_observed': 'ordinary_title_NewGame_Maria_opening_andHangzhou_observed',
    "'all_five_review_gates_pending')":
        "'all_five_review_gates_pending','name_term_control_consumer_andfresh_formatting_approval_pending')",
    'all216_individual_five_gates_pass': 'all301_individual_five_gates_pass',
    'observed_menu_instances=3,observed_choice_labels=7': 'observed_menu_instances=1,observed_choice_labels=2',
    "SC1_sha256=release['target_SC1_sha256']": "SC3_sha256=release['target_SC3_sha256']",
    'Hodram B251–B280 integrated once over registered B231–B250.':
        'Maria B0–B32 contextual dialogue integrated once over the registered cumulative Hodram residual release.',
    'nine protected original name getters passed.':
        '12 protected original name getters passed. Full editorial scope remains active.',
    'editorial_review_current.Hodram_B251_B280_completion_v1.pending.json':
        'editorial_review_current.Maria301_completion_v1.pending.json',
    'Credited 216 Hodram B251–B280 reviews once.': 'Credited301 Maria reviews once.',
})
counts = {'216':'301','129':'178','87':'123','17533':'19161','17749':'19462','10828':'11710','6921':'7752',
    '17752':'19465','209':'299','212':'303','7':'2','86':'92','88':'96','123':'207','4001':'31000'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m:counts[m[0]],source)
source = checked_text(source, {
    '    ledger[FAMILY]=dict(':
        """    ledger[BATCH].update(all_five_gates_pending=False,all_fifth_formatting_gates_pending=False,
        stored_andrepresentative_gameplay_pending=False,native_display_stored_andrepresentative_gameplay_pending=False,
        registered_integration_pending=False,all301_individual_five_gates_pass=True,
        qualified_scoped_names=36,wrap_improvements=35,justified_layout_retentions=2,
        final_cumulative_integration_complete=True)
    ledger[FAMILY]=dict(""",
})
compile(source,__file__+'::once-only-credit-all-unrelated-ledger-keys-andprefixes-preserved','exec')

if __name__ == '__main__':
    exec(compile(source,__file__+'::registered-Maria301-once-only-credit','exec'),globals())
