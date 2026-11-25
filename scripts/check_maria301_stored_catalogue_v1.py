"""Check all299 stored Maria bodies through the unchanged native catalogue lookup."""
from scripts.check_hodram_B0_B41_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/Hodram_B0_B41_clean_20261107/': 'work/Maria_B0_B32_clean_20261109/',
    'captain=1': 'captain=3',
    '==388': '==299',
    'all388_stored_effective_body_bindings.json': 'all299_stored_effective_body_bindings.json',
    'all388_ordinary_and_style_bodies_checked': 'all299_ordinary_and_style_bodies_checked',
    '388 stored ordinary and alternate-voice bodies pass': '299 stored ordinary and alternate-voice bodies pass',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-full-buffer-catalogue-guards-current-Maria', 'exec'), globals())
