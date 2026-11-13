"""Bind the original text lookup to all stored ordinary and alternate-voice bodies."""
from scripts.check_rafael_B261_B280_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/Rafael_B261_B280_clean_20261106/': 'work/Rafael_B281_B300_clean_20261106/',
    '==130': '==240',
    'all130_stored_effective_body_bindings.json': 'all240_stored_effective_body_bindings.json',
    'all130_ordinary_and_style_bodies_checked': 'all240_ordinary_and_style_bodies_checked',
    '130 stored ordinary and alternate-voice bodies pass': '240 stored ordinary and alternate-voice bodies pass',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-original-catalogue-bound-to-240-bodies', 'exec'), globals())
