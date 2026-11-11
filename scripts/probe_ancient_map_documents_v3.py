"""Submit the four native clue-bit changes through the emulator harness."""

from inspect import getsource

from scripts import probe_ancient_map_documents_v1 as original
from scripts import probe_ancient_map_documents_v2 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = prior.ROOT.with_name('ancient_map_current_display_20261111_v3')


def set_condition(arm, raw, request):
    after, receipt = prior.set_condition(arm, raw, request)
    receipt['changes'] = receipt.pop('changed')
    return after, receipt


if __name__ == '__main__':
    source = checked_text(getsource(original.main), {
        'from scripts.probe_ancient_map_documents_v1 import set_condition':
            'from scripts.probe_ancient_map_documents_v3 import set_condition',
    })
    environment = vars(original) | dict(ROOT=ROOT, __file__=__file__)
    exec(compile(source, __file__ + '::verified-clue-bit-changes', 'exec'), environment)
    environment['main']()
