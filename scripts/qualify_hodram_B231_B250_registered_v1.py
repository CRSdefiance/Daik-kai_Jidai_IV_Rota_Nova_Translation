"""Reject the eight malformed production scopes while preserving both caller ROMs."""
import inspect
from scripts import qualify_hodram_B211_B230_registered_v1 as previous
from scripts.prepare_hodram_B231_B250_registered_v1 import CONFIG,QUALIFICATION,ROOT
from dk4tool.patch.hodram_b231_b250_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'registered_semantic_checks_v1'
source=checked_text(inspect.getsource(previous.main),{
    "'record_count',276":"'record_count',224",
    "'speech_count',269":"'speech_count',222",
    "'typed_choice_count',6":"'typed_choice_count',1",
    "'style_count',28":"'style_count',13",
    "conf['blocks']+[222]":"conf['blocks']+[235]",
    "'scoped_name_count',22":"'scoped_name_count',18",
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-eight-scope-negatives-and-caller-purity','exec'),env)
if __name__=='__main__':env['main']()
