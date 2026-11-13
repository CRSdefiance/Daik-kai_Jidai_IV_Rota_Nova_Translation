"""Reject eight malformed production scopes and preserve both caller images."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria337_registered_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.maria337_release_v1':'dk4tool.patch.maria335_B137_B151_release_v1',
    'scripts.prepare_maria337_registered_v1':'scripts.prepare_maria335_B137_B151_registered_v1',
    "'record_count',336":"'record_count',334",
    "'speech_count',334":"'speech_count',332",
    "conf['blocks']+[137]":"conf['blocks']+[152]",
    "'scoped_name_count',20":"'scoped_name_count',25",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-eight-source-scope-rejections-andcaller-inverses','exec'),globals())
