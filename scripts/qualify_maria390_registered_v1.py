"""Keep the eight original production-scope rejection and caller-preservation checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria337_registered_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.maria337_release_v1':'dk4tool.patch.maria390_release_v1',
    'scripts.prepare_maria337_registered_v1':'scripts.prepare_maria390_registered_v1',
    "'record_count',336":"'record_count',389",
    "'speech_count',334":"'speech_count',372",
    "conf['blocks']+[137]":"conf['blocks']+[176]",
    "'scoped_name_count',20":"'scoped_name_count',46",
    'exact current route and no continuation owners':'24 complete exchanges/no new controls',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-eight-production-rejections-andpure-caller-guards-390-scope','exec'),globals())
