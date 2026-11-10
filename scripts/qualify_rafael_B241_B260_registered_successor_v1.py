"""Exercise the unchanged transaction guards on the reviewed B241–B260 append."""
from scripts.qualify_rafael_B221_B240_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "set(config['blocks'])|{231}": "set(config['blocks'])|{244}",
    'changed-swan-panel-selector': 'changed-handover-panel-selector',
    'DK4_MES_B223_R0017': 'DK4_MES_B253_R0019',
    'DK4_MES_B221_R0027': 'DK4_MES_B241_R0054',
    "r['block']==224 and r['source_count']==3 and r['source_index']==2":
        "r['block']==251 and r['source_count']==2 and r['source_index']==1",
    'changed-three-choice-caption': 'changed-binary-choice-caption',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-semantic-and-ordered-qualification', 'exec'), globals())
