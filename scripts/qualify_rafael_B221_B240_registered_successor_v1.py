"""Exercise the exact 270-record transaction and unchanged final-stage contracts."""
from scripts.qualify_rafael_B201_B220_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "set(config['blocks'])|{221}": "set(config['blocks'])|{231}",
    'changed-signature-panel-selector': 'changed-swan-panel-selector',
    'DK4_MES_B216_R0074': 'DK4_MES_B223_R0017',
    'DK4_MES_B201_R0006': 'DK4_MES_B221_R0027',
    "r['block']==209 and r['source_index']==2": "r['block']==224 and r['source_count']==3 and r['source_index']==2",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-semantic-and-ordered-qualification', 'exec'), globals())

