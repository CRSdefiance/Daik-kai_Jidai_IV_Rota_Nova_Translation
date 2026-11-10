"""Bind all 225 stored bodies through the unchanged native pre-macro lookup."""
from scripts.check_hodram_B281_B300_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Hodram_B281_B300_clean_20261107/':'work/Hodram_B301_B310_clean_20261107/',
    '==373':'==225',
    'all373_stored_effective_body_bindings.json':'all225_stored_effective_body_bindings.json',
    'all373_ordinary_and_style_bodies_checked':'all225_ordinary_and_style_bodies_checked',
    '373 stored ordinary and alternate-voice bodies pass':'225 stored ordinary and alternate-voice bodies pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-original-lookups-for-all-stored-bodies','exec'),globals())
