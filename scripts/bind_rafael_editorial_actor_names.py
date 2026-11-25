"""Reuse the clean/current intrinsic-name proof with an explicit current Rafael context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_editorial_actor_names.py').read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=0)',
    '    voice_env=dict(original_names.__globals__)':
        "    voice_adapter=checked_text(prior['source_owned_voice_function'],{'assert captain==1':'assert captain==0'})\n    voice_env=dict(original_names.__globals__)",
    "compile(prior['source_owned_voice_function'],": "compile(voice_adapter,",
    'source_owned_clean_adapter=clean_adapter,source_owned_current_adapter=adapter,':
        'source_owned_clean_adapter=clean_adapter,source_owned_current_adapter=adapter,source_owned_voice_function=voice_adapter,',
})
exec(compile(source,__file__+'::same-native-name-ABI-explicit-Rafael','exec'),globals())
