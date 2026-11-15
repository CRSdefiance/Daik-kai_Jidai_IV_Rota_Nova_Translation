"""Keep the individual comparison contract with physical-style section keys."""
import inspect
from scripts import save_clean_editorial_comparisons_v1 as previous
from scripts.seal_clean_editorial_prose_stage_v2 import row_key

env={**vars(previous),'row_key':row_key,'__file__':__file__}
exec(compile(inspect.getsource(previous.main),__file__+'::same-individual-comparison-guards-style-keys','exec'),env)
if __name__=='__main__':env['main']()
