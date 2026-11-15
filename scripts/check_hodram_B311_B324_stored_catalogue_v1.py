"""Bind all387 stored bodies through the unchanged native pre-macro lookup."""
from scripts.check_hodram_B301_B310_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/Hodram_B301_B310_clean_20261107/': 'work/Hodram_B311_B324_clean_20261107/',
    '==225': '==387',
    'all225_stored_effective_body_bindings.json': 'all387_stored_effective_body_bindings.json',
    'all225_ordinary_and_style_bodies_checked': 'all387_ordinary_and_style_bodies_checked',
    '225 stored ordinary and alternate-voice bodies pass': '387 stored ordinary and alternate-voice bodies pass',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-original-lookups-for-all-stored-bodies', 'exec'), globals())
