"""Include both qualified Hangzhou inline aliases without changing any city span."""
import inspect
from scripts import bind_hodram_B0_B41_terms_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{'len(aliases)==9':'len(aliases)==10'})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-source-current-city-guards-both-Hangzhou-aliases','exec'),env)

if __name__=='__main__':env['main']()
