"""Check both original getters for the nine protected names on this candidate’s own RAM."""
from scripts import verify_hodram_B301_B310_registered_getters_v1 as previous
from scripts.build_registered_hodram_B311_B324_v1 import GETTERS, PARENT, STAGED, STARTUP
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {'Hodram B301-B310 successor own startup':'Hodram B311-B324 successor own startup'})
env = {**previous.env, **globals(), '__file__':__file__}
exec(compile(source,__file__+'::same-nine-protected-names-own-startup-new-candidate','exec'),env)
if __name__ == '__main__':
    env['verify_getters']()
