"""Run the preflighted prefix-extension successor with all prior driver locks."""
from scripts.run_registered_extension_resume_with_gc_v2 import source as previous,restoration,restoration_path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v2.py')":
        "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v3.py')",
    'from scripts.registered_canonical_extension_resume_v2 import STAGES':'from scripts.registered_canonical_extension_resume_v3 import STAGES',
    "Path('scripts/registered_canonical_extension_resume_v2.py'),":
        "Path('scripts/registered_canonical_extension_resume_v2.py'),Path('scripts/registered_canonical_extension_resume_v3.py'),",
    "Path('scripts/resume_extended_release_with_'+stage+'_v2.py')":"Path('scripts/resume_extended_release_with_'+stage+'_v3.py')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-guard-locks-collector-andexplicit-terminal-v3','exec'),globals())
