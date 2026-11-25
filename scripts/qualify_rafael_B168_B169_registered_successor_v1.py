"""Prove the normal source, prose, display, and order rejections on the new append."""
from scripts.qualify_rafael_B161_B165_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'DK4_MES_B162_R0006': 'DK4_MES_B168_R0050',
    'changed-FE-selector': 'changed-Sailor-selector',
    "next(r for r in doc['records'] if r['kind'] == 'system-FE')['source_selector'] = 0":
        "next(r for r in doc['records'] if r['id'] == 'DK4_MES_B169_R0184')['source_selector'] = 96",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-ten-semantic-and-order-rejections', 'exec'), globals())
