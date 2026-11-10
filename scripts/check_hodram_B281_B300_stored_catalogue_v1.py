"""Bind every stored body to the unchanged original pre-macro catalogue lookup."""
from scripts.check_hodram_B251_B280_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Hodram_B251_B280_clean_20261107/':'work/Hodram_B281_B300_clean_20261107/',
    '==209':'==373',
    'all209_stored_effective_body_bindings.json':'all373_stored_effective_body_bindings.json',
    'all209_ordinary_and_style_bodies_checked':'all373_ordinary_and_style_bodies_checked',
    '209 stored ordinary and alternate-voice bodies pass':'373 stored ordinary and alternate-voice bodies pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-original-lookups-for-all-stored-bodies','exec'),globals())
