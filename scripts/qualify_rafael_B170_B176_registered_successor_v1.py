"""Require the usual transaction rejections, including an altered patron control."""
from scripts.qualify_rafael_B168_B169_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'DK4_MES_B168_R0050': 'DK4_MES_B176_R0098',
    'changed-Sailor-selector': 'changed-patron-panel-selector',
    "next(r for r in doc['records'] if r['id'] == 'DK4_MES_B169_R0184')['source_selector'] = 96":
        "next(r for r in doc['records'] if r['id'] == 'DK4_MES_B171_R0061')['source_selector'] = 0",
    "set(config['blocks'])|{176}": "set(config['blocks'])|{181}",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-ten-semantic-and-order-rejections', 'exec'), globals())
