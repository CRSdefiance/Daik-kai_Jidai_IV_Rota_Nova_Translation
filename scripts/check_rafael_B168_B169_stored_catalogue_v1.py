"""Check both newly stored blocks through the original full-buffer catalogue lookup."""
from scripts.check_rafael_B166_B167_stored_catalogue_v1 import source as previous, TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael_B166_B167_current1674_20261105': 'Rafael_B168_B169_current1860_20261105',
    'len(rows)==186': 'len(rows)==115',
    'all186_stored_effective_body_bindings.json': 'all115_stored_effective_body_bindings.json',
    '186 stored story bodies pass': '115 stored story bodies pass',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-native-catalogue-lookup', 'exec'), globals())
