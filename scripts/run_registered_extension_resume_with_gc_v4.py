"""Run the guarded successor with the original locks and new versioned dispatch."""
from scripts.run_registered_extension_resume_with_gc_v3 import source as previous,restoration,restoration_path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v3.py')":
        "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v4.py')",
    'from scripts.registered_canonical_extension_resume_v3 import STAGES':
        'from scripts.registered_canonical_extension_resume_v4 import STAGES',
    "Path('scripts/registered_canonical_extension_resume_v3.py'),":
        "Path('scripts/registered_canonical_extension_resume_v3.py'),Path('scripts/registered_canonical_extension_resume_v4.py'),",
    "Path('scripts/resume_extended_release_with_'+stage+'_v3.py')":
        "Path('scripts/resume_extended_release_with_'+stage+'_v4.py')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-terminal-and-driver-locks-verified-prefix-size','exec'),globals())
