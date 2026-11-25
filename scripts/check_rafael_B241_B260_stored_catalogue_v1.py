"""Verify the original lookup for all 286 stored ordinary and style bodies."""
from scripts.check_rafael_B221_B240_stored_catalogue_all_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/analysis/Rafael_B221_B240_current2952_20261106': 'work/Rafael_B241_B260_editorial_20261106',
    'work/analysis/Rafael_B221_B240_current2952_20261106/stored_native_v1/stored_native_verification.json':
        'work/Rafael_B241_B260_editorial_20261106/stored_v1/stored_native_verification.json',
    'work/analysis/Rafael_B221_B240_current2952_20261106/current_effective.json':
        'work/Rafael_B241_B260_editorial_20261106/current_effective.json/current_effective.json',
    'len(inputs)==263': 'len(inputs)==286',
    'all263_stored_effective_body_bindings.json': 'all286_stored_effective_body_bindings.json',
    'all263_ordinary_and_style_bodies_checked': 'all286_ordinary_and_style_bodies_checked',
    '263 stored ordinary and alternate-voice bodies pass': '286 stored ordinary and alternate-voice bodies pass',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::complete-native-lookup-for-286-bodies', 'exec'), globals())
