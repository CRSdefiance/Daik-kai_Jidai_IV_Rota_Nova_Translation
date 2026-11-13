"""Check every stored residual body through the original pre-macro catalogue lookup."""
from scripts.check_rafael_B301_B320_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Rafael_B301_B320_clean_20261106/':'work/Rafael_B0_B34_clean_20261106/',
    "stored['records']+stored['style_records']":"stored['records']+stored.get('style_records',[])",
    '==442':'==283',
    'all442_stored_effective_body_bindings.json':'all283_stored_effective_body_bindings.json',
    'all442_ordinary_and_style_bodies_checked':'all283_ordinary_bodies_checked',
    '442 stored ordinary and alternate-voice bodies pass':'283 stored ordinary bodies pass',
})

if __name__=='__main__':
    exec(compile(source,__file__+'::same-complete-stored-catalogue-check','exec'),globals())
