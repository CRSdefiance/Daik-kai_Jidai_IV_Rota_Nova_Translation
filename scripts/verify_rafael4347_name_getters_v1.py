"""Verify inherited name rendering from Rafael4347's own cold-boot snapshot."""
from scripts import verify_rafael3894_startup_v1 as previous
from scripts.build_registered_rafael4347_v1 import GETTERS, PARENT, STAGED, STARTUP
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    source = checked_text(previous.getters_source, {'Rafael3894': 'Rafael4347'})
    namespace = {**vars(previous), 'GETTERS': GETTERS, 'PARENT': PARENT,
                 'STAGED': STAGED, 'STARTUP': STARTUP, '__file__': __file__}
    exec(compile(source, __file__ + '::own-original-name-getters', 'exec'), namespace)
    namespace['verify_getters']()
