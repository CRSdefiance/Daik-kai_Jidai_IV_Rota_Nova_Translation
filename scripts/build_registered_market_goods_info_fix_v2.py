"""Preserve the first pre-stage syntax failure and correct only receipt construction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/build_registered_market_goods_info_fix_v1.py').read_text(encoding='utf-8'),{
    "save(RELEASE,{**staged,'manifest':str(MANIFEST),'manifest_sha256':digest(MANIFEST),registry_sha256=digest(REGISTRY),":
        "save(RELEASE,{**staged,**dict(manifest=str(MANIFEST),manifest_sha256=digest(MANIFEST),registry_sha256=digest(REGISTRY),",
    '        full_goal_complete=False})':'        full_goal_complete=False)})',
})
exec(compile(source,__file__+'::same-registered-data-only-stage-andreceipt-construction','exec'),globals())
