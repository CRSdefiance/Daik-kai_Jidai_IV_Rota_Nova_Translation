"""Credit Rafael B321–B342 once after release registration."""
import re
from scripts.complete_rafael4347_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/rafael4347_release_v1': 'work/rafael4903_release_v1',
    'rafael_B301_B320_integrated_final_review_v1.json': 'rafael_B321_B342_integrated_final_review_v1.json',
    'Rafael_SC0_B301_B320_contextual_integrated_20261106': 'Rafael_SC0_B321_B342_contextual_integrated_20261106',
    'Rafael_SC0_B301_B320_clean_20261106': 'Rafael_SC0_B321_B342_clean_20261106',
    '==(697,114,32)': '==(698,114,33)',
    'all453_individual_five_gates_pass': 'all556_individual_five_gates_pass',
    'scope=dict(source_variants=442,native_body_pages=444,typed_labels=11,observed_source_variants=45,':
        'scope=dict(source_variants=540,native_body_pages=552,typed_labels=16,observed_source_variants=72,',
    "observed_body_pages=47,offline_only_source_variants=397,actual_review=conf['actual'],":
        "observed_body_pages=76,offline_only_source_variants=468,actual_review=conf['actual'],",
    'observed_menu_instances=5,observed_choice_labels=11': 'observed_menu_instances=7,observed_choice_labels=16',
    'Rafael B301–B320 integrated once in Rafael4347.': 'Rafael B321–B342 integrated once in Rafael4903.',
    'editorial_review_current.Rafael4347_completion_v1.pending.json':
        'editorial_review_current.Rafael4903_completion_v1.pending.json',
    'Credited 453 Rafael B301–B320 reviews once.': 'Credited 556 Rafael B321–B342 reviews once.',
})
counts = {'453': '556', '397': '364', '56': '192', '15739': '16192', '16192': '16748',
          '9888': '10252', '6304': '6496', '16195': '16751'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:453|397|56|15739|16192|9888|6304|16195)(?![0-9])',
                lambda match: counts[match[0]], source)


if __name__ == '__main__':
    exec(compile(source, __file__ + '::verified-once-only-credit', 'exec'), globals())
