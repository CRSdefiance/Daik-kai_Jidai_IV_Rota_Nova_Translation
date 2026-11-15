"""Bind all source 4100 role selectors to the current Rafael startup context."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent=Path(__file__).with_name('bind_editorial_dynamic_roles_v2.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    "selectors=sorted({r['source_selector'] for r in records});assert selectors and 207 in selectors":
        "selectors=sorted({r['source_selector'] for r in records});assert len(records)==29 and selectors==[208]",
    "['resolved_actor_ID']==captain==1":"['resolved_actor_ID']==captain==0",
    'ctx=RegisteredRuntime(args.release,args.startup);result=ctx.execute(env[\'dynamic\'],selectors)':
        "ctx=RegisteredRuntime(args.release,args.startup,captain=0);result=ctx.execute(env['dynamic'],[207,*selectors])",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-original-role-proof-with-exact-style-membership','exec'),globals())

