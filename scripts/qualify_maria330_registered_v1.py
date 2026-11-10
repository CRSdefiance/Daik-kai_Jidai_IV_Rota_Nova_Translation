"""Require rejection of eight malformed release scopes with pure caller images."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/qualify_maria328_registered_v1.py').read_text(encoding='utf-8'),{
    'maria328_release_v1':'maria330_release_v1','prepare_maria328_registered_v1':'prepare_maria330_registered_v1',
    "'record_count',327":"'record_count',329","'speech_count',312":"'speech_count',327",
    "'typed_choice_count',14":"'typed_choice_count',1","'style_count',23":"'style_count',34",
    "conf['blocks']+[96],'21 complete source exchanges'":"conf['blocks']+[125],'26 complete source exchanges'",
    "'scoped_name_count',23":"'scoped_name_count',25","'exact current route and continuation owner'":"'exact current route and continuation owners'",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-eight-production-scope-mutation-guards','exec'),globals())
