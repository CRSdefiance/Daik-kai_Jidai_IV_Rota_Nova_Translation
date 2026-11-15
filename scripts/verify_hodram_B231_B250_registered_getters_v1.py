"""Verify the nine protected original names using this successor's own startup RAM."""
import inspect
from scripts import verify_rafael5186_startup_v1 as previous
from scripts.build_registered_hodram_B231_B250_v1 import GETTERS,PARENT,STAGED,STARTUP
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.verify_getters),{'Rafael5186 own startup':'Hodram B231-B250 successor own startup'})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-nine-original-name-getters-own-snapshot','exec'),env)
if __name__=='__main__':env['verify_getters']()
