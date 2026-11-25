"""Apply the exact pre-macro native catalogue lookup to all 234 stored speech bodies."""
from scripts.check_rafael_B201_B220_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Rafael_B201_B220_current2549_20261106': 'Rafael_B221_B240_current2952_20261106',
    '382': '234',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-native-pre-macro-catalogue-lookup', 'exec'), globals())

