"""Retain the original captain-control proof when only noncaptain roles are in scope."""
import inspect
from scripts import bind_scoped_clean_roles_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "'captain=3':'captain=CAPTAIN',":
        "'captain=3':'captain=CAPTAIN',\n        \"ctx.execute(env['dynamic'],selectors)\":\"ctx.execute(env['dynamic'],sorted(set(selectors)|{207}))\",",
})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-role-scope-plus-explicit-captain-control','exec'),env)
if __name__=='__main__':env['main']()
