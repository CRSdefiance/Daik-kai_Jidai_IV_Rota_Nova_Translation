"""Recognize source-registered baked layers through the exact canonical baseline."""
from pathlib import Path
from scripts import prepare_promotion_candidate_20261110_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path(previous.__file__).read_text(encoding='utf-8'), {
    "    assert {normalize(x['batch']) for x in stack['accepted_layers']} <= {\n        normalize(x) for x in manifest['batches']}":
    """    assert len(stack['accepted_layers']) == 114
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256']
    explicit = {normalize(x) for x in manifest['batches']}
    for layer in stack['accepted_layers']:
        assert layer['status'] == 'accepted'
        assert layer.get('baked_into_baseline') is True or normalize(layer['batch']) in explicit
""",
})

if __name__ == '__main__':
    env = {**previous.__dict__, '__file__': __file__, '__name__': 'promotion_v3_qualified'}
    exec(compile(source, __file__ + '::canonical-baked-accepted-layer-contract', 'exec'), env)
    env['main']()
