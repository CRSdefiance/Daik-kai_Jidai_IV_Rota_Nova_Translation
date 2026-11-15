"""Bind original style objects andmenus on the explicit own Rafael context."""
from scripts import bind_editorial_current_objects_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    "ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'])":"ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=0)",
})
exec(compile(source,__file__+'::same-complete-native-style-alias-andcaption-binding-own-Rafael', 'exec'),globals())
