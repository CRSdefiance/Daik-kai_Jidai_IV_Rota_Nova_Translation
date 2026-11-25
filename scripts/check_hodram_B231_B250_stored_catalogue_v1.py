"""Bind every new stored body to the original pre-macro catalogue lookup."""
from scripts.check_hodram_B211_B230_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Hodram_B211_B230_resume_20261106/':'work/Hodram_B231_B250_clean_20261107/',
    '==270':'==223',
    'all270_stored_effective_body_bindings.json':'all223_stored_effective_body_bindings.json',
    'all270_ordinary_and_style_bodies_checked':'all223_ordinary_and_style_bodies_checked',
    '270 stored ordinary and alternate-voice bodies pass':'223 stored ordinary and alternate-voice bodies pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-locked-stored-lookups','exec'),globals())
