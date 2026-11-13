"""Bind every stored final-SC0 speech body to the original catalogue lookup."""
from scripts.check_rafael_B301_B320_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'work/Rafael_B301_B320_clean_20261106/': 'work/Rafael_B321_B342_clean_20261106/',
    '==442': '==540',
    'all442_stored_effective_body_bindings.json': 'all540_stored_effective_body_bindings.json',
    'all442_ordinary_and_style_bodies_checked': 'all540_ordinary_and_style_bodies_checked',
    '442 stored ordinary and alternate-voice bodies pass': '540 stored ordinary and alternate-voice bodies pass',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-original-lookup-for-all-540-stored-bodies', 'exec'), globals())
