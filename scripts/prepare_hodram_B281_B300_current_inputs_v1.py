"""Bridge the sealed 384 source drafts to the existing guarded current-text binders."""
from scripts import prepare_hodram_B251_B280_current_inputs_v1 as previous
from scripts.gloss_hodram_B281_B300_clean_v1 import ROOT,PACKET as ELIGIBLE
from scripts.draft_hodram_B281_B300_clean_v2 import OUT as DRAFTS
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'binding_inputs_v1'
source=checked_text(previous.source,{
    "drafts['records_count']==216":"drafts['records_count']==384",
    'all216_logical_drafts_written_before_current_story_English_intake_in_this_batch':
        'all384_logical_drafts_written_before_current_ROM_story_English_intake',
    'all216_clean_meanings_before_English.json':'all384_clean_meanings_before_English.json',
    'metadata_only_schema_bridge_all216_drafts_unchanged':'metadata_only_schema_bridge_all384_drafts_unchanged',
    'len(ordinary)==193':'len(ordinary)==242','meanings=193':'meanings=242',
    'Bound sealed 216 drafts to exact 193 ordinary, 16 style and seven caption inputs.':
        'Bound sealed 384 drafts to exact 242 ordinary, 131 style and 11 caption inputs.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-sealed-source-to-current-input-bridge-new-scope','exec'),env)
if __name__=='__main__':env['main']()
