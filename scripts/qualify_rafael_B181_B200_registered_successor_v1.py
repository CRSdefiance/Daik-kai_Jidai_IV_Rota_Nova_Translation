"""Require the same ten transaction rejections for the exact story and town scope."""
from scripts.qualify_rafael_B170_B176_registered_successor_v1 import source as earlier
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(earlier, {
    'DK4_MES_B176_R0098': 'DK4_MES_B181_R0005',
    'changed-patron-panel-selector': 'changed-Aziza-panel-selector',
    'DK4_MES_B171_R0061': 'DK4_MES_B187_R0015',
    "set(config['blocks'])|{181}": "set(config['blocks'])|{201}",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-ten-semantic-and-order-rejections', 'exec'), globals())
