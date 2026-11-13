"""Open the clue text with the Ancient Map's original Y button."""

from inspect import getsource

from scripts import probe_ancient_map_documents_v1 as original
from scripts import probe_ancient_map_documents_v3 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = prior.ROOT.with_name('ancient_map_current_display_20261111_v4')
COMMANDS = tuple(command | {'buttons': ['Y']} if command.get('until') == 11100 else command
                 for command in original.COMMANDS)
set_condition = prior.set_condition


if __name__ == '__main__':
    source = checked_text(getsource(original.main), {
        'from scripts.probe_ancient_map_documents_v1 import set_condition':
            'from scripts.probe_ancient_map_documents_v4 import set_condition',
    })
    environment = vars(original) | dict(ROOT=ROOT, COMMANDS=COMMANDS, __file__=__file__)
    exec(compile(source, __file__ + '::native-map-hint-button', 'exec'), environment)
    environment['main']()
