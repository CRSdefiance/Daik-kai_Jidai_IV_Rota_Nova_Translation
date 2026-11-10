"""Bind both actual ordinary host exits without replaying completed emulator runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/render_maria330_transitions_v1.py').read_text(encoding='utf-8'),{
    'scripts.meaning_maria330_clean_v1':'scripts.meaning_maria337_clean_v1',
    '[(0,22721),(1,11681)]':'[(0,22241),(1,10961)]',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-host-resupply-departure-sailing-bindings','exec'),globals())
