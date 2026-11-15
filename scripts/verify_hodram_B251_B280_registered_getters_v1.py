"""Verify the nine protected original names from this successor's own startup RAM."""
from scripts import verify_hodram_B231_B250_registered_getters_v1 as previous
from scripts.build_registered_hodram_B251_B280_v1 import GETTERS,PARENT,STAGED,STARTUP
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{'Hodram B231-B250 successor own startup':'Hodram B251-B280 successor own startup'})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-nine-original-name-getters-own-snapshot','exec'),env)
if __name__=='__main__':env['verify_getters']()
