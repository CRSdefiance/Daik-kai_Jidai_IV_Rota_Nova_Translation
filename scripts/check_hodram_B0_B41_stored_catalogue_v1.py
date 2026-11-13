"""Bind every residual stored body through the unchanged native pre-macro lookup."""
from scripts.check_hodram_B311_B324_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Hodram_B311_B324_clean_20261107/':'work/Hodram_B0_B41_clean_20261107/',
    '==387':'==388',
    'all387_stored_effective_body_bindings.json':'all388_stored_effective_body_bindings.json',
    'all387_ordinary_and_style_bodies_checked':'all388_ordinary_and_style_bodies_checked',
    '387 stored ordinary and alternate-voice bodies pass':'388 stored ordinary and alternate-voice bodies pass',
})

if __name__=='__main__':exec(compile(source,__file__+'::same-original-full-buffer-lookups-for388-stored-bodies','exec'),globals())
