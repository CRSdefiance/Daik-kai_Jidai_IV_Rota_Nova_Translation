"""Bind all299 stored speech bodies through the unchanged original catalogue getter."""
from scripts.check_maria301_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Maria_B0_B32_clean_20261109/':'work/Maria_B58_B70_clean_20261109/',
})
if __name__=='__main__':exec(compile(source,__file__+'::same299-complete-native-buffers-SP-canaries-and4MiB-guards','exec'),globals())
