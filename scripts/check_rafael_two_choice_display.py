"""Keep complete native two-choice checks with the explicit current Rafael context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_editorial_two_choice_display.py').read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=0)',
})
exec(compile(source,__file__+'::same-complete-native-choice-proof-explicit-Rafael','exec'),globals())
