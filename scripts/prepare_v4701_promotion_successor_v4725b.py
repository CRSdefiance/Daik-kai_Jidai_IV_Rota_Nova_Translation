"""Preserve the pre-write failure and compare ILNK blocks as their bytes values."""
from pathlib import Path
import hashlib
import json

source = Path('scripts/promote_v4701_checkpoint_v4725.py')
target = Path('scripts/promote_v4701_checkpoint_v4725b.py')
assert not target.exists()
text = source.read_text(encoding='utf-8')
changes = {
    "AUDIT = ROOT / 'work/analysis/promotion_v4725'": "AUDIT = ROOT / 'work/analysis/promotion_v4725b'",
    'if a.data != b.data]': 'if a != b]',
}
for old,new in changes.items():
    assert text.count(old) == 1, old
    text = text.replace(old,new)
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8',newline='\n')
print(json.dumps(dict(successor=str(target),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    correction='IlnkContainer.blocks contains bytes, not objects with a data attribute.',
    failure_before_audit_package_or_metadata_writes=True,replacements=len(changes))))
