"""Check native lookup of all stored ordinary and alternate-voice bodies."""
from scripts.check_rafael_B241_B260_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/Rafael_B241_B260_editorial_20261106/stored_catalogue_all_v1':
        'work/Rafael_B261_B280_clean_20261106/stored_catalogue_all_v1',
    'work/Rafael_B241_B260_editorial_20261106/stored_v1/stored_native_verification.json':
        'work/Rafael_B261_B280_clean_20261106/stored_v2/stored_native_verification.json',
    'work/Rafael_B241_B260_editorial_20261106/current_effective.json/current_effective.json':
        'work/Rafael_B261_B280_clean_20261106/current_v1/current_effective.json',
    '==286': '==130',
    'all286_stored_effective_body_bindings.json': 'all130_stored_effective_body_bindings.json',
    'all286_ordinary_and_style_bodies_checked': 'all130_ordinary_and_style_bodies_checked',
    '286 stored ordinary and alternate-voice bodies pass': '130 stored ordinary and alternate-voice bodies pass',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-original-catalogue-bound-to-130-bodies', 'exec'), globals())
