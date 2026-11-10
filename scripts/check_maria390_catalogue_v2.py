"""Bind all373 effective bodies from the amended stored-verification proof."""
from scripts.check_maria390_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'/stored_v1/stored_native_verification.json':'/stored_v2/stored_native_verification.json'})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-catalogue-guards-amended-storage','exec'),globals())
