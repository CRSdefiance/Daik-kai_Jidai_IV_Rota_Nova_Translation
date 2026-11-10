"""Reject eight malformed production inputs and preserve the complete caller ROMs."""
from scripts import qualify_hodram_B251_B280_registered_v2 as previous
from scripts.prepare_hodram_B281_B300_registered_v1 import CONFIG,QUALIFICATION,ROOT
from dk4tool.patch.hodram_b281_b300_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'registered_semantic_checks_v1'
source=checked_text(previous.source,{
    "'record_count',215":"'record_count',383","'speech_count',208":"'speech_count',372",
    "'typed_choice_count',6":"'typed_choice_count',10","'style_count',15":"'style_count',130",
    "conf['blocks']+[250]":"conf['blocks']+[280]","'scoped_name_count',20":"'scoped_name_count',17",
    'all 31 FE bodies':'all 16 FE bodies',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-eight-scope-rejections-and-caller-purity','exec'),env)
if __name__=='__main__':env['main']()
