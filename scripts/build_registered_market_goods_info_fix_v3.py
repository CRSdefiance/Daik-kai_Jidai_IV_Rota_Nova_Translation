"""Recover the exact pre-parse driver draft; preserve both earlier pre-stage failures."""
import hashlib
from pathlib import Path

raw=Path('scripts/build_registered_market_goods_info_fix_v1.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='674121ce0ad485e236c33abe17b87cda836ca53331422872cdf430b17a4b713e'
source=raw.decode('utf-8')
replacements={
    "save(RELEASE,{**staged,'manifest':str(MANIFEST),'manifest_sha256':digest(MANIFEST),registry_sha256=digest(REGISTRY),":
        "save(RELEASE,{**staged,**dict(manifest=str(MANIFEST),manifest_sha256=digest(MANIFEST),registry_sha256=digest(REGISTRY),",
    '        full_goal_complete=False})':'        full_goal_complete=False)})',
}
for before,after in replacements.items():
    assert source.count(before)==1
    source=source.replace(before,after)
exec(compile(source,__file__+'::exact-hash-guarded-syntax-only-recovery','exec'),globals())
