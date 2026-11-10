"""Preserve ordered FO/FI substitutions and retain the failed v1 producer unchanged."""
from copy import deepcopy
from pathlib import Path
import inspect
from scripts import draft_maria335_B137_B151_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

DRAFTS=deepcopy(previous.DRAFTS)
DRAFTS[143]=checked_text(DRAFTS[143],{'Could you be FI of FO?':"Could you be FO's FI?"})
DRAFTS[144]=checked_text(DRAFTS[144],{'Admiral FI of FO helped me!':"FO's Admiral FI helped me!"})
DRAFTS[141]=checked_text(DRAFTS[141],{'9|...Admiral...':"9|...Ma'am..."})
DRAFTS[137]=checked_text(DRAFTS[137],{'More old than old hand, I\'d say.':'He looks more like an old man than an old hand.'})
source=checked_text(inspect.getsource(previous.main),{
    'all335_independent_drafts_v1.json':'all335_independent_drafts_v2.json',
    "[path,ROOT/'clean_source_packet.json',Path(__file__)]":"[path,ROOT/'clean_source_packet.json',Path(previous.__file__),Path(__file__)]",
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-clean-source-paragraph-andordered-macro-guards','exec'),env)
if __name__=='__main__':env['main']()
