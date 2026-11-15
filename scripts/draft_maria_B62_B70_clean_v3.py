"""Apply only the two source-faithful acknowledgment refinements using the original guarded writer."""
import inspect
from copy import deepcopy
from pathlib import Path
from scripts import draft_maria_B62_B70_clean_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

DRAFTS=deepcopy(previous.DRAFTS);NOTES=deepcopy(previous.NOTES)
for index in [7,14]:
    DRAFTS[65][index]='Mm-hmm.'
    NOTES[65,index]='Preserve Maria\'s repeated distracted acknowledgment without a predicate implying the tomatoes are apples.'
assert [(b,k) for b,v in DRAFTS.items() for k,t in v.items() if t!=previous.DRAFTS[b][k]]==[(65,7),(65,14)]
source=checked_text(inspect.getsource(previous.main),{
    'B62_B70_independent_drafts_v1.json':'B62_B70_independent_drafts_v3.json',
    '[path,Path(__file__)]':'[path,Path(previous.__file__),Path(__file__)]',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-source-counts-five-pending-gates-andwriter-two-explicit-draft-refinements','exec'),env)
if __name__=='__main__':env['main']()
