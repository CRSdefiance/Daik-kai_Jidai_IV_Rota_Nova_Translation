"""Bind the Syracuse donor’s first map to its observed Southeast Asian route."""

from inspect import getsource

from scripts import probe_ancient_map_documents_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = prior.ROOT.with_name('ancient_map_current_display_20261111_v2')


def set_condition(arm, raw, request):
    source = checked_text(getsource(prior.set_condition), {
        '(item_number, map_route) == (189, 7)': '(item_number, map_route) == (189, 18)',
    })
    environment = dict(vars(prior))
    exec(compile(source, __file__ + '::observed-syracuse-index', 'exec'), environment)
    return environment['set_condition'](arm, raw, request)


if __name__ == '__main__':
    source = checked_text(getsource(prior.main), {
        'from scripts.probe_ancient_map_documents_v1 import set_condition':
            'from scripts.probe_ancient_map_documents_v2 import set_condition',
    })
    environment = vars(prior) | dict(ROOT=ROOT, __file__=__file__)
    exec(compile(source, __file__ + '::observed-syracuse-document', 'exec'), environment)
    environment['main']()
