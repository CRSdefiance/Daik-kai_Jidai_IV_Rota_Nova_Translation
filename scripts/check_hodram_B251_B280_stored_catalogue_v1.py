"""Bind each stored B251-B280 body to its original native catalogue lookup."""
from scripts.check_hodram_B231_B250_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/Hodram_B231_B250_clean_20261107/': 'work/Hodram_B251_B280_clean_20261107/',
    '==223': '==209',
    'all223_stored_effective_body_bindings.json': 'all209_stored_effective_body_bindings.json',
    'all223_ordinary_and_style_bodies_checked': 'all209_ordinary_and_style_bodies_checked',
    '223 stored ordinary and alternate-voice bodies pass': '209 stored ordinary and alternate-voice bodies pass',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-source-locked-stored-lookups', 'exec'), globals())
