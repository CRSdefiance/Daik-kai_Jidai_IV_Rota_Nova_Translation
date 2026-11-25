"""Run the registered prefix-extension chain with all original source locks and telemetry."""
from scripts.run_registered_checkpoint_resume_with_gc_v1 import source as previous, restoration, restoration_path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "DRIVER=Path('scripts/resume_integrated_release_with_Fernan_field_v1.py')":
        "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v2.py')",
    'from scripts.registered_canonical_checkpoint_resume_v1 import STAGES':
        'from scripts.registered_canonical_extension_resume_v2 import STAGES',
    "Path('scripts/registered_canonical_checkpoint_resume_v1.py'),":
        "Path('scripts/registered_canonical_checkpoint_resume_v1.py'),Path('scripts/registered_canonical_extension_resume_v2.py'),",
    "Path('scripts/resume_integrated_release_with_'+stage+'_v1.py')":
        "Path('scripts/resume_extended_release_with_'+stage+'_v2.py')",
    'explicit_registered_canonical_checkpoint_reuse=True,':
        'explicit_registered_canonical_checkpoint_reuse=True,registered_source_bound_extension_andfresh_original_final_contracts=True,',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-locks-collector-terminal-qualified-prefix-extension','exec'),globals())
