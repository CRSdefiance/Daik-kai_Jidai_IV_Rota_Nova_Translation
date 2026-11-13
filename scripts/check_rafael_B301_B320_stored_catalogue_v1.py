"""Bind the original native lookup to every stored body in the reviewed scope."""
from scripts.check_rafael_B281_B300_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/Rafael_B281_B300_clean_20261106/': 'work/Rafael_B301_B320_clean_20261106/',
    'stored_v2/stored_native_verification.json': 'stored_v1/stored_native_verification.json',
    '==240': '==442',
    'all240_stored_effective_body_bindings.json': 'all442_stored_effective_body_bindings.json',
    'all240_ordinary_and_style_bodies_checked': 'all442_ordinary_and_style_bodies_checked',
    '240 stored ordinary and alternate-voice bodies pass': '442 stored ordinary and alternate-voice bodies pass',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::all-stored-body-lookups', 'exec'), globals())
