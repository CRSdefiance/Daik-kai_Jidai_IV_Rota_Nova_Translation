"""Credit the 135 reviewed Rafael records once after the cumulative verification."""
import re

from scripts.complete_rafael3514_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/rafael3514_Francisca_release_v1': 'work/rafael3649_release_v1',
    'rafael_B241_B260_integrated_final_review_v1.json': 'rafael_B261_B280_integrated_final_review_v1.json',
    'Rafael_SC0_B241_B260_contextual_integrated_20261106': 'Rafael_SC0_B261_B280_contextual_integrated_20261106',
    'Rafael_SC0_B241_B260_clean_20261106': 'Rafael_SC0_B261_B280_clean_20261106',
    '==(692,114,27)': '==(694,114,29)',
    "release['owned_Francisca_name_field_verified'] and release['exact_all_integrated_references_bound']":
        "release['owned_Francisca_name_field_verified'] and release['owned_Plett_Jacob_surnames_verified'] "
        "and release['all_nine_registered_final_stages_preserved'] and release['exact_all_integrated_references_bound']",
    "names['both_name_getters_exact_for_actors_35_and_186']": "names['both_name_getters_exact_for_actors_35_65_68_186_203']",
    "startup['only_owned_Francisca_field_differs_in_ARM9']": "startup['only_owned_Plett_Jacob_surnames_differ_in_ARM9']",
    """    prep=load(release['preparation']);assert len(prep['configs'])==1
    conf=load(prep['configs'][0]);origin=Path(conf['manuscript']);doc=load(origin)""":
        """    prep=load(release['preparation']);assert sha(Path(release['preparation']).read_bytes())==release['preparation_sha256']
    assert sha(Path(prep['config']).read_bytes())==prep['config_sha256']
    conf=load(prep['config']);origin=Path(conf['manuscript']);doc=load(origin)""",
    'all292_individual_five_gates_pass': 'all135_individual_five_gates_pass',
    'scope=dict(source_variants=286,native_body_pages=294,typed_labels=6,observed_source_variants=132,':
        'scope=dict(source_variants=130,native_body_pages=131,typed_labels=5,observed_source_variants=42,',
    "observed_body_pages=135,offline_only_source_variants=154,actual_review=conf['actual'],":
        "observed_body_pages=43,offline_only_source_variants=88,actual_review=conf['actual'],",
    'observed_menu_instances=3,observed_choice_labels=6,offline_only_captions=0':
        'observed_menu_instances=2,observed_choice_labels=5,offline_only_captions=0',
    'Rafael B241–B260 integrated once. All 692 entries, 114 accepted layers, the eight prior stages and the Francisca field, exact patch and own startup pass. Continue with B265–B280 clean drafts.':
        'Rafael B261–B280 integrated once. Rafael3649 preserves the nine prior stages and adds both verified surnames. Exact patch and own startup pass. Continue with the next complete clean Japanese exchanges.',
    'editorial_review_current.Rafael3514_completion_v1.pending.json':
        'editorial_review_current.Rafael3649_completion_v1.pending.json',
    'Credited 292 Rafael B241–B260 reviews once.': 'Credited 135 Rafael B261–B280 reviews once.',
})
counts = {'292': '135', '244': '118', '48': '17', '15067': '15359', '15359': '15494',
          '9171': '9289', '6188': '6205', '15362': '15497'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:292|244|48|15067|15359|9171|6188|15362)(?![0-9])',
                lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__ + '::verified-once-only-credit', 'exec'), globals())
