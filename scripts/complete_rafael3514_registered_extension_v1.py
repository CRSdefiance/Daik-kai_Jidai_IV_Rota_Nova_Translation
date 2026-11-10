"""Credit the final 292 dialogue records once after the registered proofs."""
import re

from scripts.complete_rafael3222_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/Rafael3222_extended_release_verified_v1_20261106': 'work/rafael3514_Francisca_release_v1',
    'rafael_B221_B240_integrated_final_review_v1.json': 'rafael_B241_B260_integrated_final_review_v1.json',
    'Rafael_SC0_B221_B240_contextual_integrated_20261106': 'Rafael_SC0_B241_B260_contextual_integrated_20261106',
    'Rafael_SC0_B221_B240_clean_20261106': 'Rafael_SC0_B241_B260_clean_20261106',
    'own_Fernan_name_getter_verification.json': 'own_registered_name_getters_v1.json',
    "assert release['all_eight_registered_final_stages_preserved'] and release['exact_all_integrated_references_bound']":
        "assert release['all_eight_registered_final_stages_preserved'] and release['owned_Francisca_name_field_verified'] and release['exact_all_integrated_references_bound']",
    "    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']":
        "    assert names['both_name_getters_exact_for_actors_35_and_186']",
    """    for path in ['work/Rafael3222_extended_release_verify_gc_v1_20261106/completion.json',
        'work/Rafael3222_extended_startup_gc_v1_20261106/completion.json',
        'work/Rafael3222_extended_Fernan_gc_v1_20261106/completion.json']:
        t=load(path);assert t['terminal'] and t['completed_without_exception'] and t['all_locked_sources_unchanged']
        assert not t['garbage_collection']['errors']""":
        """    assert startup['only_owned_Francisca_field_differs_in_ARM9'] and startup['frames']==4001
    assert startup['ordinary_title_NewGame_Rafael_Castor_andopening_observed']""",
    '==(690,114,26)': '==(692,114,27)',
    'all270_individual_five_gates_pass': 'all292_individual_five_gates_pass',
    'source_variants=263,native_body_pages=279,typed_labels=7,observed_source_variants=86':
        'source_variants=286,native_body_pages=294,typed_labels=6,observed_source_variants=132',
    'observed_body_pages=94,offline_only_source_variants=177': 'observed_body_pages=135,offline_only_source_variants=154',
    'observed_choice_labels=7': 'observed_choice_labels=6',
    'own_Fernan_name_getters=str(np),own_Fernan_name_getters_sha256=sha(np.read_bytes())':
        'own_name_getters=str(np),own_name_getters_sha256=sha(np.read_bytes())',
    "SC0_sha256=release['target_SC0_sha256'],":
        "SC0_sha256=release['target_SC0_sha256'],ARM9_sha256=release['target_ARM9_sha256'],",
    'Rafael B221–B240 integrated once. All 690 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue with the next complete Rafael exchanges.':
        'Rafael B241–B260 integrated once. All 692 entries, 114 accepted layers, the eight prior stages and the Francisca field, exact patch and own startup pass. Continue with B265–B280 clean drafts.',
    'editorial_review_current.Rafael3222_completion_v1.pending.json':
        'editorial_review_current.Rafael3514_completion_v1.pending.json',
    'Credited 270 Rafael B221–B240 reviews once.': 'Credited 292 Rafael B241–B260 reviews once.',
})
counts = {'270':'292', '221':'244', '49':'48', '14797':'15067', '15067':'15359',
          '8927':'9171', '6140':'6188', '15070':'15362'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:270|221|49|14797|15067|8927|6140|15070)(?![0-9])',
                lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__+'::verified-once-only-editorial-credit', 'exec'), globals())
