"""Reject malformed production scopes while preserving complete caller ROMs."""
from scripts import qualify_hodram_B281_B300_registered_v1 as previous
from scripts.prepare_hodram_B301_B310_registered_v1 import CONFIG,QUALIFICATION,ROOT
from dk4tool.patch.hodram_b301_b310_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'registered_semantic_checks_v1'
source=checked_text(previous.source,{
    "'record_count',383":"'record_count',233",
    "'speech_count',372":"'speech_count',224",
    "'typed_choice_count',10":"'typed_choice_count',8",
    "'style_count',130":"'style_count',151",
    "conf['blocks']+[280]":"conf['blocks']+[300]",
    "'scoped_name_count',17":"'scoped_name_count',7",
    'all 16 FE bodies':'all 8 FE bodies',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-eight-scope-rejections-and-caller-purity','exec'),env)
if __name__=='__main__':env['main']()
