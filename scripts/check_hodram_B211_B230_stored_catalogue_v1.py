"""Bind every stored ordinary and voice-table body to the original pre-macro lookup."""
from scripts.check_rafael_B301_B320_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Rafael_B301_B320_clean_20261106/':'work/Hodram_B211_B230_resume_20261106/',
    'captain=0':'captain=1',
    '==442':'==270',
    'all442_stored_effective_body_bindings.json':'all270_stored_effective_body_bindings.json',
    'all442_ordinary_and_style_bodies_checked':'all270_ordinary_and_style_bodies_checked',
    '442 stored ordinary and alternate-voice bodies pass':'270 stored ordinary and alternate-voice bodies pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-locked-all-stored-lookups','exec'),globals())
