"""Run the explicitly registered resume chain with original locks and collector telemetry."""
from scripts.run_registered_build_with_gc_v3 import source as previous, restoration, restoration_path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "DRIVER=Path('scripts/build_integrated_release_with_Fernan_field.py')":
        "DRIVER=Path('scripts/resume_integrated_release_with_Fernan_field_v1.py')",
    '\ndef memory():': """
from scripts.registered_canonical_checkpoint_resume_v1 import STAGES
DRIVERS += [Path('scripts/build_integrated_release_with_Fernan_field.py'),
    Path('scripts/registered_canonical_checkpoint_resume_v1.py'),
    *[Path('scripts/resume_integrated_release_with_'+stage+'_v1.py') for stage in STAGES]]

def memory():""",
    'no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0,':
        'no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0,explicit_registered_canonical_checkpoint_reuse=True,',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-original-locks-collector-andterminal-with-explicit-resume-driver', 'exec'), globals())
