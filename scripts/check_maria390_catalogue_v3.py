"""Bind373 effective bodies to the composed amended stored proof."""
from scripts.check_maria390_catalogue_v2 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'/stored_v2/stored_native_verification.json':'/stored_v3/stored_native_verification.json',
    '/stored_catalogue_all_v1':'/stored_catalogue_all_v2'})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-catalogue-guards-wine-amended-storage','exec'),globals())
