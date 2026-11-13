"""Verify the nine protected names using this successor's own initialized RAM."""
from scripts import verify_hodram_B251_B280_registered_getters_v1 as previous
from scripts.build_registered_hodram_B281_B300_v1 import GETTERS,PARENT,STAGED,STARTUP
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{'Hodram B251-B280 successor own startup':'Hodram B281-B300 successor own startup'})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-nine-name-getters-own-startup','exec'),env)
if __name__=='__main__':env['verify_getters']()
