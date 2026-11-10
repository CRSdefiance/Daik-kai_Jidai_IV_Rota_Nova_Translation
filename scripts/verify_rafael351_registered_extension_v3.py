"""Keep the complete351 verifier and select the preflighted registered resume qualifier."""
from scripts.verify_rafael351_registered_extension_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'scripts.registered_canonical_extension_resume_v2 import qualify,stage_source,STAGES':
    'scripts.registered_canonical_extension_resume_v3 import qualify,stage_source,STAGES'})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-release-andpatch-verification-v3-resume-provenance','exec'),globals())
