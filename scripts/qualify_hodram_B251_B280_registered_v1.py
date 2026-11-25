"""Reject eight malformed production scopes and verify caller purity."""
from scripts import qualify_hodram_B231_B250_registered_v1 as previous
from scripts.prepare_hodram_B251_B280_registered_v1 import CONFIG,QUALIFICATION,ROOT
from dk4tool.patch.hodram_b251_b280_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'registered_semantic_checks_v1'
source=checked_text(previous.source,{
    "'record_count',224":"'record_count',215", "'speech_count',222":"'speech_count',208",
    "'typed_choice_count',1":"'typed_choice_count',6", "'style_count',13":"'style_count',15",
    "conf['blocks']+[235]":"conf['blocks']+[250]", "'scoped_name_count',18":"'scoped_name_count',20",
})
env={**previous.env,**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-eight-negatives-and-caller-purity','exec'),env)
if __name__=='__main__':env['main']()
