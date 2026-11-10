"""Key different menus in the same block by their exact source command offsets."""
import inspect

from scripts.seal_clean_independent_drafts_v1 import seal
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(seal), {
    'def seal(': 'def seal_offsets(',
    "(r['block'],r['source_index']) for r in labels":
        "(r['source_command_offset'],r['source_index']) for r in labels",
    "choice_drafts[(source['block'],source['source_index'])]":
        "choice_drafts[(source['source_command_offset'],source['source_index'])]",
    "Path(producer),Path(__file__)]":
        "Path(producer),Path(__file__),ORIGINAL]",
})
env = {**seal.__globals__, 'ORIGINAL': seal.__globals__['Path'](seal.__code__.co_filename), '__file__': __file__}
exec(compile(source, __file__ + '::same-clean-seal-exact-menu-command-keys', 'exec'), env)
seal_offsets = env['seal_offsets']
