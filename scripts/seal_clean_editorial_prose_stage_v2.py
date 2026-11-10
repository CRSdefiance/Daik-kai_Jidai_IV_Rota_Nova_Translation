"""Extend the guarded sectioned sealer to complete physical 4100 alternatives."""
import inspect
from scripts import seal_clean_editorial_prose_stage_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def row_key(row):
    if row['kind']=='physical-style-alternative':
        return 'S'+row['id'].split('_STYLE_',1)[1]
    return previous.row_key(row)


source=checked_text(inspect.getsource(previous.main),{
    "contextual_comparison_pending=True,\n                review=":
        "contextual_comparison_pending=True,current_English_comparison_pending=True,\n                review=",
    "source_meaning_file=str(args.input),source_meaning_file_sha256=digest(args.input))":
        "source_meaning_file=str(args.input),source_meaning_file_sha256=digest(args.input),\n        source_meanings=str(args.input),source_meanings_sha256=digest(args.input),\n        current_English_not_consulted=True,whole_clean_exchanges_read_before_drafting=True)",
})
env={**vars(previous),'row_key':row_key,'__file__':__file__}
exec(compile(source,__file__+'::same-exact-source-macro-paragraph-and-unpassed-gate-contract','exec'),env)
if __name__=='__main__':env['main']()
