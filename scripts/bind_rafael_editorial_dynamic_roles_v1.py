"""Bind ordinary and4100 runtime roles with the original ABI in the own captain0 context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_editorial_dynamic_roles_v2.py').read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=0)',
    '"[\'resolved_actor_ID\']==captain==1"':'"[\'resolved_actor_ID\']==captain==0"',
})
exec(compile(source,__file__+'::same-native-dynamic-roles-source-ordinary-andstyle-selectors-own-Rafael', 'exec'),globals())
