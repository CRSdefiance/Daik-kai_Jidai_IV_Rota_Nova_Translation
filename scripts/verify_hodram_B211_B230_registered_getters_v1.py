"""Verify nine preserved original names using the successor's own fresh startup RAM."""
import inspect
from scripts import verify_rafael5186_startup_v1 as previous
from scripts.build_registered_hodram_B211_B230_v1 import GETTERS,PARENT,STAGED,STARTUP
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.verify_getters),{'Rafael5186 own startup':'Hodram B211-B230 successor own startup'})
env={**vars(previous),'GETTERS':GETTERS,'PARENT':PARENT,'STAGED':STAGED,'STARTUP':STARTUP,'__file__':__file__}
exec(compile(source,__file__+'::same-nine-protected-name-getters-own-snapshot','exec'),env)
if __name__=='__main__':env['verify_getters']()
