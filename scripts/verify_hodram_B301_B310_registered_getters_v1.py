"""Check both original getters for the nine protected names on this successor's RAM."""
from scripts import verify_hodram_B281_B300_registered_getters_v1 as previous
from scripts.build_registered_hodram_B301_B310_v1 import GETTERS,PARENT,STAGED,STARTUP
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{'Hodram B281-B300 successor own startup':'Hodram B301-B310 successor own startup'})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-nine-protected-names-own-startup','exec'),env)
if __name__=='__main__':env['verify_getters']()
