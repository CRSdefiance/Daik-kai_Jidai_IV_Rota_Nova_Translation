"""Run the unchanged complete-body catalogue checks on the corrected stored target."""
from scripts.check_maria310_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    '/stored_v1/stored_native_verification.json':'/stored_v3/stored_native_verification.json',
    '/stored_catalogue_all_v1':'/stored_catalogue_all_v2',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-native-catalogue-guards310-corrected-target','exec'),globals())
