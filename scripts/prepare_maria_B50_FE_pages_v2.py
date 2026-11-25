"""Provide the original FE macro adapter's declared BASE binding; preserve the pre-output failure."""
from pathlib import Path
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria_B50_FE_pages_v1.py').read_text(encoding='utf-8'),{
    'macro_env={**expand.__globals__}':"macro_env={**expand.__globals__,'BASE':BASE}",
    'fe_env={**expand.__globals__}':"fe_env={**expand.__globals__,'BASE':BASE}",
})
exec(compile(source,__file__+'::same-source-ownership-andoriginal-native-adapters-declared-BASE','exec'),globals())
