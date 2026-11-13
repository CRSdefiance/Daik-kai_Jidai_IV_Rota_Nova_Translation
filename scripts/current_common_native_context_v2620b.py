"""Extend bounded context to later histories whose deployed payload is already exact."""
from pathlib import Path
source=Path('scripts/current_common_native_context_v2620.py').read_text()
source=source.replace("assert delta==list(range(0x5D4,0x5DC))","assert delta in [[],list(range(0x5D4,0x5DC))]")
old="assert before==bytes.fromhex('8265617469636961')and after==b'Faticia\\0'and self.raw[POOL-BASE+0x5D4:POOL-BASE+0x5DC]==before"
new="assert before==(b'Faticia\\0'if not delta else bytes.fromhex('8265617469636961'))and after==b'Faticia\\0'and self.raw[POOL-BASE:POOL-BASE+123040]==bytes(oldsections[3].data[:-48])"
assert old in source;source=source.replace(old,new)
exec(compile(source,__file__,'exec'),globals())
