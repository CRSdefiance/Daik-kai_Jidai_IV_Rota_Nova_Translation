"""Keep eight production-scope rejection and caller-preservation guards for mixed305."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria337_registered_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.maria337_release_v1':'dk4tool.patch.maria305_release_v2',
    'scripts.prepare_maria337_registered_v1':'scripts.prepare_maria305_registered_v2',
    "'record_count',336":"'record_count',304",
    "'speech_count',334":"'speech_count',293",
    "conf['blocks']+[137]":"conf['blocks']+[196]",
    "'scoped_name_count',20,'all scoped name gates'":"'scoped_name_count',26,'exact mixed source/native scope'",
    'exact current route and no continuation owners':'route and no new continuation controls',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-eight-production-rejections-andpure-callers-mixed305','exec'),globals())
