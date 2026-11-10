"""Prove the speech-only transaction rejects invalid source, display and ordering."""
from scripts.qualify_rafael557_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'changed-FU-macro': 'changed-FI-macro',
    "'{MACRO:FU}'": "'{MACRO:FI}'",
    "set(config['blocks'])|{140}": "set(config['blocks'])|{176}",
    'DK4_MES_B154_R0084': 'DK4_MES_B162_R0006',
    'changed-caption-index': 'changed-FE-selector',
    "next(r for r in doc['records'] if r['kind'] == 'typed-choice-label' and r['source_index'] == 1)['source_index'] = 0":
        "next(r for r in doc['records'] if r['kind'] == 'system-FE')['source_selector'] = 0",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::ten-semantic-and-order-rejections', 'exec'), globals())
