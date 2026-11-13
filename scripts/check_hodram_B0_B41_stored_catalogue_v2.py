"""Apply the existing complete-buffer verifier to the final stored wrap revision."""
from scripts.check_hodram_B0_B41_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'stored_catalogue_all_v1':'stored_catalogue_all_v2',
    '/stored_v1/stored_native_verification.json':'/stored_v2/stored_native_verification.json',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-buffer-lookup-final-stored-records','exec'),globals())
